'''
Автотест архиватора 7z
Файл с негативными тестами
'''

import yaml
from checkers import checkout_negative


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_nstep1(self, make_folders, clear_folders, make_files, make_bad_arh):
        #test neg 1 - разархивация поврежденного архива
        assert checkout_negative("cd {}; 7z e broken_arh.{} -o{} -y".format(data["folder_neg"],
                                                                            data["type"],
                                                                            data["folder_in"]), "ERRORS"), "test negative 1 FAIL"


    def test_nstep2(self, make_bad_arh):
        #test neg 2 -тестирование файла в поврежденном архиве
        assert checkout_negative("cd {}; 7z t broken_arh.{}".format(data["folder_neg"], data["type"]),
                                 "ERRORS"), "test negative 2 FAIL"