'''
Автотест архиватора 7z
Файл с позитивными тестами
'''

import yaml
from checkers import checkout, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files):
        #test1 - создание архива
        res1 = checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                    data["folder_out"]), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arh.{}".format(data["type"]))
        assert res1 and res2, "test1 FAIL"


    def test_step2(selt, clear_folders, make_files):
        #test2 - разархивация (+ создание архива)
        res = []
        res.append(checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                        data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arh.{} -o{} -y".format(data["folder_out"],
                                                                data["type"],
                                                                data["folder_in"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_in"]), item))
        assert all(res), "test2 FAIL"


    def test_step3(self):
        #test3 - проверка целостности архива
        assert checkout("cd {}; 7z t arh.{}".format(data["folder_out"],
                                                    data["type"]), "Everything is Ok"), "test3 FAIL"


    def test_step4(self):
        #test4 - обновление файлов в архиве
        assert checkout("cd {}; 7z u arh.{}".format(data["folder_from"],
                                                    data["type"]), "Everything is Ok"), "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        #test5 - список содержимого архива
        res = []
        res.append(checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                        data["folder_out"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arh.{}".format(data["folder_out"],
                                                            data["type"]), item))
        assert all(res), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        #test6 - извлечение файлов с полными путями
        res = []
        res.append(checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                        data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arh.{} -o{} -y".format(data["folder_out"],
                                                                data["type"],
                                                                data["folder_in"]), "Everything is Ok"))

        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_in"]), item))

        res.append(checkout("ls {}".format(data["folder_in"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_in"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"


    def test_step7(self):
        #test7 - удаление файлов из архива
        assert checkout("cd {}; 7z d arh.{}".format(data["folder_out"],
                                                    data["type"]), "Everything is Ok"), "test7 FAIL"


    def test_step8(self, clear_folders, make_files):
        #test8 - проверка хэша
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_from"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_from"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_from"], item), hash))
        assert all(res), "test8 FAIL"