"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата
"""
import yaml


def write_to_yaml(filename, data):
    """Dumps python dict to stylish unicode YAML via context manager"""
    with open(filename, 'w', encoding='UTF-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def read_from_yaml(filename):
    """Loads YAML to python dict via context manager"""
    with open(filename, encoding='UTF-8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    DICT_TO_YAML = {
        'items': ['computer', 'printer', 'keyboard', 'mouse'],
        'items_price': {
            'computer': '200€',
            'printer': '70€',
            'keyboard': '10€',
            'mouse': '5€',
        },
        'items_qty': 4,
    }

    FILENAME = 'file.yml'
    write_to_yaml(FILENAME, DICT_TO_YAML)
    print(DICT_TO_YAML == read_from_yaml(FILENAME))
