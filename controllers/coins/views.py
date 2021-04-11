import ujson


def get_coins():
    """ Get support coins """

    with open('db/detail_symbols.json', 'r') as file:
        cache_symbols = ujson.loads(file.read())
        return cache_symbols, 200
