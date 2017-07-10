import unittest


class ExampleTest(unittest.TestCase):

    '''Verify that tests are running - make test should return failure'''

    def test(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
