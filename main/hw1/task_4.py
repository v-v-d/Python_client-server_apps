# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

strings = ('разработка', 'администрирование', 'protocol', 'standard')

for s in strings:
    b_str = s.encode()
    print(f'{b_str.decode()}, {b_str}')
