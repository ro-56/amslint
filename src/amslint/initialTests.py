#regex to detect every identifier and retrieve everything inside of it (check https://regex101.com/r/dU5fO8/33)
import re
indented_text = ''
with open('src/amslint/ams.ams') as f:
    indented_text = f.read()
import pprint as pp

def make_list(code,indent_level=0, indent_bumb=1):
    ID_list = []
    re_id = r'(?s)(?:^|\n)\s{'+str(indent_level)+'}(\w+)\s(\w*)\s\{\n(\s+.+?)\n\s{'+str(indent_level)+'}\}'
    for match in re.finditer(re_id, code):
        itm = {
            'type': match.groups()[0],
            'name': match.groups()[1],
            }
        re_oneLineAttb_id = r'(?s)(?:\n)\s{'+str(indent_level+indent_bumb)+'}(\w+):\s(\w+);'
        a = match.groups()[2]
        for attMatch in re.finditer(re_oneLineAttb_id, a):
            itm[attMatch.groups()[0]] = attMatch.groups()[1]
        
        b = match.groups()[2]
        re_multiLineAttb_id = r'(?s)(?:^|\n)\s{'+str(indent_level+indent_bumb)+'}(\w+):\s\{\n\s+(.+?)\n\s{'+str(indent_level+indent_bumb)+'}\}'
        for attMatch in re.finditer(re_multiLineAttb_id, b):
            itm[attMatch.groups()[0]] = attMatch.groups()[1]
        
        itm['child'] = make_list(match.groups()[2],indent_level+indent_bumb)
        ID_list.append(itm)
        # print(match.groups()[2])
        # print()
        # pp.pprint(match.groups())
        # print()

    return ID_list


indented_text = indented_text.replace('\t', '    ')
lisa = make_list(indented_text)
with open('src/amslint/out.json', 'w') as f:
    f.write(str(lisa))
