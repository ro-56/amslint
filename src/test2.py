import re

def ID_detection (code,indent):
    ID_list = []
    
    #regex to detect every identifier and retrieve everything inside of it (check https://regex101.com/r/dU5fO8/33)
    re_id = r'(?s)(?:^|\n)\s{'+str(indent)+'}(\w+)\s(\w*)\s\{(\n\s+.+?)\n\s{'+str(indent)+'}\}'
    
    aaaa = re.finditer(re_id, code)

    for match in re.finditer(re_id, code):
        
        ID_list.append( {"name": match.groups()[1],
                        "type": match.groups()[0],
                        "start": match.start(),
                        "end": match.end(),
                        "code": match.groups()[2]})
    
    return ID_list
def ID_conversion(ID_code, level=4):
    ID_list = ID_detection(ID_code,level)
    return ID_list


file = 'DynamicDataExchange.ams'
function_code = open(file, 'r').read()
function_code = function_code.replace('\t',' '*4)
first_list = ID_detection(function_code,0) 

# indent = 0
# for i in first_list:
#     ID_list = ID_detection(i["code"], indent)
#regex to detect every identifier and retrieve everything inside of it (check https://regex101.com/r/dU5fO8/33)
    
def make_list(code,indent=0):
    ID_list = []
    re_id = r'(?s)(?:^|\n)\s{'+str(indent)+'}(\w+)\s(\w*)\s\{(\n\s+.+?)\n\s{'+str(indent)+'}\}'
    for match in re.finditer(re_id, code):
        # ID_list.append({
        #     'name': match.groups()[1],
        #     'type': match.groups()[0],
        #     'child': make_list(match.groups()[2], indent+4)
        #     })
        print(match.groups()[2])

    return ID_list

lisa = make_list(function_code)
with open('out.json', 'w') as f:
    f.write(str(lisa))

