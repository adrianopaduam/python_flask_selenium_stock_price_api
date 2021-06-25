import unittest

from app.main.util.data_manipulation import format_stock


class TestInformationManipulation(unittest.TestCase):

    def test_stock_formatting(self):

        original_stock = {
            "price": 1234.3,
            "name": "Test",
            "symbol": "TST.SYMB"
        }

        target_stock = {
            "symbol": "TST.SYMB",
            "name": "Test",
            "price": "1234.30"
        }

        self.assertDictEqual(
            format_stock(original_stock),
            target_stock
        )


if __name__ == '__main__':
    unittest.main()
