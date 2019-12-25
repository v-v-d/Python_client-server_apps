# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
# кириллице.
# Решил задачу через модуль requests. Код выглядит намного компактней, чем использование subprocess.Popen()

import requests

resources = ('https://yandex.ru', 'https://youtube.com')

for resource in resources:
    print(requests.get(resource).content.decode())
