# class Node:
#     def __init__(self, indented_line):
#         self.children = []
#         self.level = len(indented_line) - len(indented_line.lstrip())
#         self.text = indented_line.strip()

#     def add_children(self, nodes):
#         childlevel = nodes[0].level
#         while nodes:
#             node = nodes.pop(0)
#             if node.level == childlevel: # add node as a child
#                 self.children.append(node)
#             elif node.level > childlevel: # add nodes as grandchildren of the last child
#                 nodes.insert(0,node)
#                 self.children[-1].add_children(nodes)
#             elif node.level <= self.level: # this node is a sibling, no more children
#                 nodes.insert(0,node)
#                 return

#     def as_dict(self):
#         if len(self.children) > 1:
#             return {self.text: [node.as_dict() for node in self.children]}
#         elif len(self.children) == 1:
#             return {self.text: self.children[0].as_dict()}
#         else:
#             return self.text

# indented_text = \
# """
# ## ams_version=1.0

# LibraryModule Library_AimmsXLLibrary {
# 	Prefix: axll;
# 	Interface: PublicSection;
# 	Comment: {
# 		"This library allows you to read from and write to .xlsx or .xls (Excel) files.
		
# 		The library does not need Excel to be installed on the machine and works both in Windows and Linux.
		
# 		The library can only read and write the file formats .xlsx and .xls, but is not capable of 
# 		evaluating any formula or macro that is contained in it. For that you need Excel itself.
		
# 		The functions in this library do not use a return value to indicate success or failure.
# 		Instead, the functions are created to be used in combination with the error handling mechanisms in AIMMS.
# 		That is why it is highly recommended to place all function calls within a :any:`block-onerror-endblock <block>` context,
# 		so that you can easily handle the warnings and errors that might occur during the usage of these
# 		functions.
		
# 		A typical usage looks like:
		
# 		  .. code::
		
# 		    block
	
# 			  axll::OpenWorkbook(mybook.xlsx);
		  
# 			  ! .. read or write the sheets in the workbook ..
		  
# 		    onerror err do
		  
# 			  ! .. handle the error or warning ..
		  
# 			  errh::MarkAsHandled(err);
		  
# 		    endblock;
		  
# 		    axll::CloseAllWorkbooks;  ! save and close any open workbook"
# 	}
# 	Section PrivateSection {
# 		Function LibraryDirectory {
# 			Arguments: libraryName;
# 			Range: string;
# 			Body: {
# 				if DirectoryOfLibraryProject(libraryName, LibraryDirectory) <> 1 then
# 					LibraryDirectory := libraryName;
# 				endif;
# 			}
# 			StringParameter libraryName {
# 				Property: Input;
# 			}
# 		}
# 		Function DLLDirectory {
# 			Arguments: libraryName;
# 			Range: string;
# 			Body: {
# 				DLLDirectory := LibraryDirectory(libraryName) +"DLL" + if (AimmsStringConstants('Platform') = "Windows") then "\\" else "/" endif;
# 			}
# 			StringParameter libraryName {
# 				Property: Input;
# 			}
# 		}
# 		Function DLLPath {
# 			Arguments: (libraryName,dllName);
# 			Range: string;
# 			Body: {
# 				DLLPath := DLLDirectory(libraryName) + dllName + if (AimmsStringConstants('Platform') = "Windows") then ".dll" else ".so" endif;
# 			}
# 			StringParameter libraryName {
# 				Property: Input;
# 			}
# 			StringParameter dllName {
# 				Property: Input;
# 			}
# 		}
# 		Procedure PreLibraryTermination {
# 			Body: {
# 				::Library_AimmsXLLibrary::closeAllWorkBooks;
# 				return 1;
# 			}
# 		}
# 		Section CommonDeclarations {
# 			ElementParameter STR_ENCODING {
# 				Range: AllCharacterEncodings;
# 				Property: NoSave;
# 				Definition: {
# 					if AimmsStringConstants('Platform') = "Windows" then
# 						'UTF-16LE'
# 					else
# 						'UTF-32LE'
# 					endif
# 				}
# 			}
# 			StringParameter DLL_NAME {
# 				Property: NoSave;
# 				Definition: DLLPath("AimmsXLLibrary", "AimmsXLLibrary");
# 			}
# 		}
# 	}
# }

# """

# root = Node('root')
# root.add_children([Node(line) for line in indented_text.splitlines() if line.strip()])
# d = root.as_dict()['root']
# import pprint as pp
# pp.pprint(d)

# with open("test3.txt", 'w') as f:
#     f.write(str(d))
indented_text = ''
with open('src/amslint/ams.ams') as f:
    indented_text = f.readlines()

level = [0 for _ in range(len(indented_text))]

for i, str_ in enumerate(indented_text):
    for c, _ in enumerate(str_):
        if str_[c] == '\t':
            level[i] += 1
        if str_[c] != '\t':
            break

pass