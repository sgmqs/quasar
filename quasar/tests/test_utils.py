import unittest

from ..utils import strip_str, now_minus_hours


class UtilsTest(unittest.TestCase):

    def test_strip_str(self):
        string = "just a normal string"
        self.assertEqual(strip_str(string), string)

        string = "a <string> with \some' characters"
        output = "a string with some characters"
        self.assertEqual(strip_str(string), output)

        string = None
        self.assertEqual(strip_str(string), "")
        string = "None"
        self.assertEqual(strip_str(string), "")
        string = ""
        self.assertEqual(strip_str(string), "")

    def test_now_minus_hours(self):
        import time
        from datetime import datetime as dt

        now = now_minus_hours(0)
        also_now = dt.fromtimestamp(int(time.time())).isoformat()
        self.assertEqual(now, also_now)

        ago = now_minus_hours(5)
        also_ago = dt.fromtimestamp(int(time.time()) - 5 * 3600).isoformat()
        self.assertEqual(ago, also_ago)

        none = now_minus_hours(None)
        self.assertIsNone(none)

if __name__ == '__main__':
    unittest.main()
