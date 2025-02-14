import unittest
from app.utils import add

class TestMain(unittest.TestCase):
    def test_main_function(self):
        self.assertEqual(add(5, 5), 10)
        self.assertEqual(add(-2, 2), 0)
        self.assertEqual(add(3, 7), 10)

if __name__ == "__main__":
    unittest.main()
