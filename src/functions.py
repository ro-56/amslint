import re
import os
import pdb

def output_global_rst(global_rst,file,fileNames):

    if not os.path.exists('api/'):
       os.makedirs('api/')
       
    for k in range(len(fileNames)):
      if file.find('/') != -1:
        out = open('api/' + '/'.join(file.split('.ams')[0].split('/')[0:-1])+"/"+ fileNames[k] +".rst",'w+')
      else:
        out = open('api/' + fileNames[k] +".rst",'w+')
      out.write(global_rst[k])
      out.close()


def ID_detection (code,indent):

    '''
        Output a list of dictionnaires containing all Identifiers with [Name + type + code] for a given indent level 
        
        :argument code: string to be scanned
        :argument indent: value, in number of spaces, of the indent
        
        :return ID_list: list of dictionnaires containing all Identifiers with [Name + type + code] for a given indent level 
    '''
    ID_list = []
    
    #regex to detect every identifier and retrieve everything inside of it (check https://regex101.com/r/dU5fO8/33)
    re_id = r'(?s)(?:^|\n)\s{'+str(indent)+'}(\w+)\s(\w*)\s\{(\n\s+.+?)\n\s{'+str(indent)+'}\}'
    
    for match in re.finditer(re_id, code):
        
        ID_list.append( {"name": match.groups()[1],
                        "type": match.groups()[0],
                        "start": match.start(),
                        "end": match.end(),
                        "code": match.groups()[2]})
    
    return ID_list

def write_indexDomain(indexDomain, isIndex=0):
    
    indices = indexDomain.split('|')[0]
    if len(indexDomain.split('|'))-1:
        domainCondition = indexDomain.split('|')[1]
    else:
        domainCondition = ''
    exceptions = ['if','and','or','then','else']
    re_index = re.compile(r'[\w:]+')
    indices = [x for x in re_index.findall(indices) if x not in exceptions]
    rst = ""
    if not isIndex:
        rst+= " "*4 +":attribute IndexDomain: (" 
    else:
        rst+= " "*4 +":attribute Index: (" 
        
    for index in indices:
    
        rst+= ":aimms:index:`" + index + "`, " 
    
    rst = rst.rstrip(', ') + ")" 
    if domainCondition:
        rst+= " | " + domainCondition
    rst+= "\n"
    
    return rst
 
def write_arguments(arguments, arguments_with_body, level, attribute_list_to_ignore):
    #pdb.set_trace()
    rst = ""
    # Exception list for arguments without body '{}' that we still want to output with an aimms code-block (TODO: inline code)
    exception_list = ['Comment','InitialData','Definition', 'BodyCall', 'Body']

    # first build each argument without body found
    for i in range(len(arguments)):
        if arguments[i][0] not in attribute_list_to_ignore:
          if arguments[i][0] in exception_list: #if an exception, go to the next arguments_with_body block      
              arguments[i] = [arguments[i][0],'\n'+' '*(level+4) + arguments[i][1]]
              arguments_with_body.insert(0,arguments[i])
          elif arguments[i][0] == 'IndexDomain':
              rst+= write_indexDomain(arguments[i][1])
          elif arguments[i][0] == 'Index':
              rst+= write_indexDomain(arguments[i][1],1)
          elif arguments[i][0] == 'Text':
              rst+= " "*4 + ":attribute Text: " + arguments[i][1].strip('"').replace('\\','') + "\n" 
          elif arguments[i][0] == 'Range':
              rst+= " "*4 + ":attribute Range: :aimms:set:`"+arguments[i][1]+"`\n" 
          elif arguments[i][0] == 'SubsetOf':
              rst+= " "*4 + ":attribute SubsetOf: :aimms:set:`"+arguments[i][1]+"`\n"
          elif arguments[i][0] == 'Arguments':
              pass
          else:
              rst+= " "*4 + ":attribute " + arguments[i][0] + ": " + arguments[i][1] + "\n"
              
          rst+= "\n"

    # then build each argument with a body found
    for i in range(len(arguments_with_body)):
        # rst+= " "*4 + ":attribute " + arguments_with_body[i][0] + ": " + "\n"
        # rst+= "\n"
        if arguments_with_body[i][0] not in attribute_list_to_ignore:
          if arguments_with_body[i][0] == 'Comment':
              rst_buffer= '\n' + ' '*(level+4) + arguments_with_body[i][1].strip('\n').strip(' ').strip('\"').replace('\\"','\"').replace("\\'","\'") # removes escape signs in front of quotes, removes opening/closing comment quotes.
              rst+=  rst_buffer.replace('\n'+' '*level,'\n') # de-indentation
              rst+= "\n"
          else:
              pass
              # rst+= " "*4 + "    .. code-block:: aimms\n"
              # rst+= " "*8 + arguments_with_body[i][1].replace('\n','\n    ') #indentation
              # rst+= "\n"
    
    return rst

def ID_conversion(ID_code, type, name, level=4, skip_undocumented_id=True, attribute_list_to_ignore=[]):
    '''
        for a given AIMMS identifier ``type`` and ``name``, nested code ``ID_code`` in AMS format and a given indentation level ``level``, outputs a nicely formatted RST string, plus the rest of the unprocessed nested identifiers on the next indentation level (tab=4spaces).
        
        :argument ID_code: string to be converted in AMS format
        :argument type: Type of the current AIMMS Identifier to build
        :argument name: Name of the current AIMMS Identifier to build
        :argument level: Indentation level (# of spaces) the ID_code must be scanned
        :argument skip_undocumented_id: If set to True, the current AIMMS Identifier will not be written if it doesn't contain any comment. If potential nested identifiers do contain comments, this current AIMMS Identifier it will be written.
        
        :return rst: String containing the conversion
        :return ID_list: remaining list of nested IDs to convert inside 
        
        .. todo::
            
            constraints, variables, mathprogram
        
    '''

    #initialize next ID list
    ID_list = []
    #initialize underlining markers for table of content heirarchy of library, modules, sections... As you may see, it's not infinite ! :) we are limited to 6 levels (should be enough, but who knows)
    SectionUnderliningMarkers = ['#','*','-','^','"','+'] 
    #initialize rst
    rst = "\n"

    #detect every argument, with or without body, if any
    re_arg = re.compile(r'\n\s{'+str(level)+'}(\w+):\s(.+);')
    re_arg_with_body = re.compile(r'(?s)\n\s{'+str(level)+'}(\w+):\s\{(.*?)\s{'+str(level)+'}\}')
    
    arguments = re_arg.findall(ID_code)
    arguments_with_body = re_arg_with_body.findall(ID_code)
    prefix=''
    
    # Added this to keep track of (nested) comments
    re_comment = re.compile(r'\n\s+Comment:\s(.+);')
    re_comment_with_body = re.compile(r'(?s)\n\s+(Comment):\s\{(.*?)\s+\}')
    
    comment = re_comment.findall(ID_code)
    comment_with_body = re_comment_with_body.findall(ID_code)
    
    # Check if any comment is part of the code of the current identifier. If yes, the current identifier will be written in the RST output.

    if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:

        if type == 'LibraryModule' or type == 'Module':
            
            rst+= '\n' + type +' '+ name.replace('_',' ') + '\n' + SectionUnderliningMarkers[int(min((level-4)/4,len(SectionUnderliningMarkers)-1))]*(len(type)+1+len(name)) + '\n\n'
            
            rst+= ".. aimms:librarymodule:: " + name + "\n\n"
            
            # build prefix and Interface in a fancy way before the rest
            arguments_buffer = []
            arguments_buffer.extend(arguments)
            for arg in arguments_buffer:
                if arg[0] == 'Prefix' and arg[0] not in attribute_list_to_ignore:
                    rst+= " "*4 + ":attribute " + arg[0] + ": ``" + arg[1] + "``\n"
                    rst+= "\n"
                    prefix = arg[1]
                    arguments.remove(arg)
                elif arg[0] == 'Interface' and arg[0] not in attribute_list_to_ignore:
                    rst+= " "*4 + ":attribute " + arg[0] + ": :doc:`" + arg[1] + "`\n"
                    rst+= "\n"
                    arguments.remove(arg)
       
            #write the rest !
            rst+= write_arguments(arguments,arguments_with_body,level,attribute_list_to_ignore)

            # Specify the namespace
            if prefix: #a library module can be without prefix
                rst+= ".. aimms:module:: " + prefix + "\n\n"
       
        elif type == 'Model' or type == 'Section':
            
            rst+= '\n' + name.replace('_',' ') + '\n' + SectionUnderliningMarkers[int(min((level-4)/4,len(SectionUnderliningMarkers)-1))]*(len(type)+1+len(name)) + '\n\n'
        
        
        elif type == 'DeclarationSection':


            rst = rst # do nothing
     
    #    if type == 'Procedure' or 'StringParameter':

        elif type == 'Set':
        
            rst+= '.. aimms:'+type.lower()+':: ' + name + '\n\n'
            
            indices = []
            for arg in arguments:
                if arg[0] == 'Index' and arg[0] not in attribute_list_to_ignore:
                    indices = arg[1].strip('(').strip(')').split(',')
            
            rst+= write_arguments(arguments,arguments_with_body,level,attribute_list_to_ignore)
            rst+= "\n"
            if indices:
                for index in indices:
                    rst+= " "*4 +'.. aimms:index:: ' + index + '\n\n'
                    
                    rst+= " "*8 + ":attribute Range: :aimms:set:`"+name+"`\n"
                    rst+= "\n"            
       
        else:
            
            # Search for potential AIMMS arguments to be appended
            aimms_arguments = [i[1] for i in arguments if i[0] == "Arguments"]
            
            # If some AIMMS arguments are part of the definition of this identifier, append them to the declaration signature
            if aimms_arguments:
              rst+= '.. aimms:'+type.lower()+':: ' + name + aimms_arguments[0] + '\n\n' 
            else:
              rst+= '.. aimms:'+type.lower()+':: ' + name +  '\n\n'
                    
            rst+= write_arguments(arguments,arguments_with_body,level,attribute_list_to_ignore)
            
            
    
    
    
    ID_list = ID_detection(ID_code,level)
    
    return rst, ID_list, prefix
