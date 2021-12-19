""""""


from amslint.preprocessing.amsfile import AMSFile, Identifier, Atribute


def test_AMSFile():
    file = AMSFile("tests/test_files/test_file.ams", auto_initialize=0)
    assert file is not None


def test_get_contents():
    file = AMSFile("tests/test_files/test_file_2.ams")
    expected = [
        Identifier(name='Main_basic', type='Model', line=3,
                   parent_type='', attributes=[]),
        Identifier(name='MainExecution', type='Procedure', line=23,
                   parent_type='Model', attributes=[]),
        Identifier(name='Public_Section', type='Section', line=4,
                   parent_type='Model', attributes=[]),
        Identifier(name='Procedure_1', type='Procedure', line=5,
                   parent_type='Section', attributes=[]),
        Identifier(name='Function_1', type='Function', line=6,
                   parent_type='Section', attributes=[]),
        Identifier(name='Decl_02', type='DeclarationSection', line=7,
                   parent_type='Section', attributes=[]),
        Identifier(name='Section_2', type='Section', line=8,
                   parent_type='Section', attributes=[]),
        Identifier(name='Module_1', type='Module', line=9,
                   parent_type='Section', attributes=[Atribute(type='Prefix', value='m1', line=10)]),
        Identifier(name='ExtProcedure_2', type='ExternalProcedure', line=12,
                   parent_type='Section', attributes=[Atribute(type='DllName', value='"dll_name"', line=13)]),
        Identifier(name='DB_Procedure_1', type='DatabaseProcedure', line=15,
                   parent_type='Section', attributes=[Atribute(type='DataSource', value='"datasource"', line=16),
                                                      Atribute(type='SqlQuery', value='"query"', line=17)]),
        Identifier(name='ExtFunction_2', type='ExternalFunction', line=19,
                   parent_type='Section', attributes=[Atribute(type='DllName', value='"dll_name"', line=20)]),
    ]
    for item in expected:
        assert item in file.identifiers
