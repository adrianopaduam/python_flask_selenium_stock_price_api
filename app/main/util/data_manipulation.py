""" Data manipulation routines """


def format_stock(stock):
    """
    Formats stock in required formatting
    """
    parsed_stock = {
        "symbol": stock['symbol'],
        "name": stock['name'],
        "price": f"{stock['price']:.2f}",
    }

    return parsed_stock
