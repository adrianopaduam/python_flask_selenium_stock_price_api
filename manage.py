import sys
import unittest
from decouple import config

from app.main import create_app

app = create_app()


def run():
    app.run(host=config('HOST'), port=config("PORT"))


def test():
    """
    Unitary tests execution
    """
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    if 'test' in sys.argv:
        test()
    else:
        run()
