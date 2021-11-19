import sys
from datetime import datetime
import functions as f
import re
import pdb

try:
    file = sys.argv[1]
except:
    print ("Error : You must give a AMS file as an argument")
    sys.exit()
 
################ SCRIPT OPTIONS ###############

# skip any identifier that contains no comment, except if it contains nested identifier containing comments 
skip_undocumented_id = True 
# Potential identifier attributes that you would like to ignore
attribute_list_to_ignore = ['DllName','Encoding'] 

################ END SCRIPT OPTIONS ###############
 
# Read code
function_code = open(file, 'r').read()
aimms_module_id = ['Module','LibraryModule']
aimms_nested_id = ['Procedure','Function','ExternalFunction','DatabaseProcedure','ExternalProcedure']

global_rst = []
fileNames = []
currentPrefix = ''

# Added this to keep track of (nested) comments
re_comment = re.compile(r'\n\s+Comment:\s(.+);')
re_comment_with_body = re.compile(r'(?s)\n\s+(Comment):\s\{(.*?)\s+\}')

# replace 1 tab by 4 spaces in function_code
function_code = function_code.replace('\t',' '*4)

first_list = f.ID_detection(function_code,0)   

print ("\n" + str(datetime.now()) + " Started..\n")

for i in first_list:

    rst, ID_list, prefix = f.ID_conversion(i["code"], i["type"], i["name"], 4, skip_undocumented_id, attribute_list_to_ignore)
    if len(first_list)==1:
      fileNames.append("index")
    else:
      fileNames.append(i["name"])
    global_rst += [rst]

    # Build TOC tree for potential subsections
    global_rst[-1] += ".. toctree::\n\n   "
    for i_loc in ID_list:
        if i_loc["type"] == "Section":
        
            # If no comments in Section, do not create a toctree entry
            comment = re_comment.findall(i_loc["code"])
            comment_with_body = re_comment_with_body.findall(i_loc["code"])
            if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:
              global_rst[-1] += i_loc["name"] + "\n   "
    currentPrefix = prefix

    for i2 in ID_list:
        
        # Save potential Section name to create independent file later on
        if i2["type"] == "Section":
          # If no comments in Section, do not create a new file
          comment = re_comment.findall(i2["code"])
          comment_with_body = re_comment_with_body.findall(i2["code"])
          if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:
            fileNames.append(i2["name"])
            global_rst.append("") # Creates a new item at the end of the list
            skip = 0
          else: 
            skip = 1
        if skip: continue
        rst, ID_sublist, prefix = f.ID_conversion(i2["code"], i2["type"], i2["name"], 8, skip_undocumented_id, attribute_list_to_ignore)
        
        # build up of the prefix
        if currentPrefix and prefix:
          currentPrefix += "::" + prefix
        else:
          currentPrefix += prefix
          
        if i["type"] in aimms_nested_id:
            # if parent type is a procedure for example (nested id), than indent the rst
            global_rst[-1] += rst.replace('\n','\n    ')
        elif i2["type"] == "Section" and currentPrefix and (len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id):
            # if this section is nested in a module or library, set the module prefix for the file
            global_rst[-1] = ".. aimms:module:: " + currentPrefix + "\n\n" + global_rst[-1] + rst
        else:
            global_rst[-1] += rst
        
        # Build TOC tree for potential subsections
        global_rst[-1] += ".. toctree::\n\n   "
        for i_loc in ID_sublist:
            if i_loc["type"] == "Section":
              # If no comments in Section, do not create a toctree entry
              comment = re_comment.findall(i_loc["code"])
              comment_with_body = re_comment_with_body.findall(i_loc["code"])
              if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:
                global_rst[-1] += i_loc["name"] + "\n   "
                
        for i3 in ID_sublist:
        
            # Save potential Section name to create independent file later on
            if i3["type"] == "Section":
              # If no comments in Section, do not create a new file
              comment = re_comment.findall(i3["code"])
              comment_with_body = re_comment_with_body.findall(i3["code"])
              if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:
                fileNames.append(i3["name"])
                global_rst.append("") # Creates a new item at the end of the list
              
            rst, ID_subsublist, prefix = f.ID_conversion(i3["code"], i3["type"], i3["name"], 12, skip_undocumented_id, attribute_list_to_ignore)
            if currentPrefix and prefix:
              currentPrefix += "::" + prefix
            else:
              currentPrefix += prefix
              
            if i2["type"] in aimms_nested_id:
                global_rst[-1] += rst.replace('\n','\n    ')
            elif i3["type"] == "Section" and currentPrefix and (len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id):
            
              # if this section is nested in a module or library, set the module prefix for the file
              global_rst[-1] = ".. aimms:module:: " + currentPrefix + "\n\n" + global_rst[-1] + rst
            else:
                global_rst[-1] += rst
                
            # Build TOC tree for potential subsections
            global_rst[-1] += ".. toctree::\n\n   "
            for i_loc in ID_subsublist:
                if i_loc["type"] == "Section":
                  # If no comments in Section, do not create a toctree entry
                  comment = re_comment.findall(i_loc["code"])
                  comment_with_body = re_comment_with_body.findall(i_loc["code"])
                  if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:
                    global_rst[-1] += i_loc["name"] + "\n   "

            for i4 in ID_subsublist:

                # Save potential Section name to create independent file later on
                if i4["type"] == "Section":
                  # If no comments in Section, do not create a new file
                  comment = re_comment.findall(i4["code"])
                  comment_with_body = re_comment_with_body.findall(i4["code"])
                  if len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id:
                    fileNames.append(i4["name"])
                    global_rst.append("") # Creates a new item at the end of the list
                  
                rst, ID_subsubsublist, prefix = f.ID_conversion(i4["code"], i4["type"], i4["name"], 16, skip_undocumented_id, attribute_list_to_ignore)
                if currentPrefix and prefix:
                  currentPrefix += "::" + prefix
                else:
                  currentPrefix += prefix
         
                if i3["type"] in aimms_nested_id:
                    # if parent type is a procedure for example (nested id), than indent the rst
                    global_rst[-1] += rst.replace('\n','\n    ')
                elif i4["type"] == "Section" and currentPrefix and (len(comment) != 0 or len(comment_with_body) != 0 or not skip_undocumented_id):
                    # if this section is nested in a module or library, set the module prefix for the file
                    global_rst[-1] = ".. aimms:module:: " + currentPrefix + "\n\n" + global_rst[-1] + rst
                else:
                    global_rst[-1] += rst    
                    
                for i5 in ID_subsubsublist:
                    rst, ID_subsubsubsublist, prefix = f.ID_conversion(i5["code"], i5["type"], i5["name"], 20, skip_undocumented_id, attribute_list_to_ignore)
                    if i4["type"] in aimms_nested_id:
                        global_rst[-1] += rst.replace('\n','\n    ')
                    else:
                        global_rst[-1] += rst
                
f.output_global_rst(global_rst,file,fileNames)
print (str(datetime.now()) + " Done !")