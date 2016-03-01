import unittest
import hash


class TestMD5(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(hash.md5(''), 'd41d8cd98f00b204e9800998ecf8427e')


if __name__ == '__main__':
    unittest.main()
