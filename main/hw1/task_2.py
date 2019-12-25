# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

b_strings = (b'class', b'function', b'method')

for b_str in b_strings:
    print(type(b_str), b_str, len(b_str))
