"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий
выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV.
"""
import csv
import re


def get_main_data(filenames, headers):
    """Returns full data from file based on all parameters"""
    return [(get_data_chunk(filename, headers)) for filename in filenames]


def get_data_chunk(filename, headers):
    """Returns data chunk from file based on regex"""
    return (re.search(get_regex(header), get_file_data(filename)).group(2) for header in headers)


def get_regex(value):
    """Returns regex string based on main parameter"""
    return r'({}:\s*)(.+\S)'.format(value)


def get_file_data(filename):
    """Returns data from file via context manager"""
    with open(filename) as file:
        return file.read()


def write_to_csv(filename, data):
    """Writes data list to CSV via context manager"""
    with open(filename, 'w', encoding='UTF-8') as file:
        file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        file_writer.writerows(data)


if __name__ == '__main__':
    INPUT_FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    OUTPUT_FILE = 'main_data.csv'
    HEADERS = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    write_to_csv(OUTPUT_FILE, [HEADERS, *get_main_data(INPUT_FILES, HEADERS)])
