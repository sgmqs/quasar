import unittest

class ExampleTest(unittest.TestCase):

    '''Fails to verify that tests are running'''
    def test(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()