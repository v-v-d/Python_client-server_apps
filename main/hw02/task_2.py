"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате
JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными
"""
import json


def read_from_json(filename):
    """Loads Json to python dict via context manager"""
    with open(filename) as file:
        return json.load(file)


def get_orders_list(orders_dict):
    """Returns orders list from orders dict"""
    return orders_dict.get('orders')


def get_order(keys, values):
    """Returns order dict from keys and values"""
    return dict(zip(keys, values))


def write_to_json(filename, data):
    """Dumps python dict to JSON with indent=4 via context manager"""
    with open(filename, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(data, indent=4))


def update_orders(orders_dict, orders):
    """Updates current orders list and returns it"""
    orders_dict['orders'] = orders
    return orders_dict


if __name__ == '__main__':
    FILENAME = 'orders.json'
    KEYS = ['item', 'quantity', 'price', 'buyer', 'date']
    PRODUCT_1 = ['product1', 10, 100500, 'Homer', '12.01.2020']
    PRODUCT_2 = ['product2', 20, 100500, 'Bart', '13.01.2020']
    PRODUCT_3 = ['product3', 30, 100500, 'Marge', '14.01.2020']
    PRODUCTS = (PRODUCT_1, PRODUCT_2, PRODUCT_3)

    ORDERS = read_from_json(FILENAME)
    ORDER_LIST = get_orders_list(ORDERS)

    for product in PRODUCTS:
        ORDER_LIST.append(get_order(KEYS, product))

    write_to_json(FILENAME, update_orders(ORDERS, ORDER_LIST))
