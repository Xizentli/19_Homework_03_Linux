'''
файл с фикстурами
'''

import random
import pytest
import string
import yaml
from datetime import datetime
from checkers import checkout, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    # создание тестовых каталогов
    return checkout("mkdir {} {} {} {}".format(data["folder_in"],
                                               data["folder_out"],
                                               data["folder_from"],
                                               data["folder_neg"]), "")


@pytest.fixture()
def clear_folders():
    # отчищение тестовых каталогов
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"],
                                                        data["folder_out"],
                                                        data["folder_from"],
                                                        data["folder_neg"]), "")


@pytest.fixture()
def make_files():
    # создание тестовых файлов
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_from"],
                                                                                           filename,
                                                                                           data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    # создание подкаталога и файла в нем
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_from"], subfoldername), ""):
        return None, None
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_from"],
                                                                                              subfoldername,
                                                                                              filename), ""):
        return subfoldername, None
    else:
        return subfoldername, filename


@pytest.fixture(autouse=True)
def print_time():
    # выводит время текущее время перед стартом теста и сразу после завершения теста
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arh():
    # создание архива и его повреждение
    checkout("cd {}; 7z a {}/broken_arh".format(data["folder_from"], data["folder_neg"]), "")
    checkout("truncate -s 1 {}/broken_arh.{}".format(data["folder_neg"],
                                                     data["type"]), "Everything is Ok")
    yield "broken_arh"
    checkout("rm -f {}/broken_arh.{}".format(data["folder_neg"], data["type"]), "")


@pytest.fixture(autouse=True)
def stat_lig():
    # запись дополнительной информации о работе тестов в файл
    yield
    time = datetime.now().strftime("%H:%M:%S.%f")
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count: {} size: {} load: {}' >> stat.txt".format(time,
                                                                              data["count"],
                                                                              data["bs"],
                                                                              stat), "")