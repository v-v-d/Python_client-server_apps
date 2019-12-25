# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.

import chardet

strings = ('сетевое программирование', 'сокет', 'декоратор')

with open('test_file.txt', 'w', encoding='utf-8') as file:
    file.write(', '.join(strings))

with open('test_file.txt', encoding='utf-8') as file:
    text = file.read()
    encoding = chardet.detect(text.encode())['encoding']
    print(encoding, text)
