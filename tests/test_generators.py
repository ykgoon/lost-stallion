import unittest
import random
import sys
import os

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generators import map_trigram, get_random_hexagram

class TestStoryGenerator(unittest.TestCase):

    def test_map_trigram(self):
        # Test Heaven trigram (111)
        self.assertEqual(map_trigram("799"), "乾")

        # Test Lake trigram (110)
        self.assertEqual(map_trigram("798"), "兌")

        # Test Fire trigram (101)
        self.assertEqual(map_trigram("789"), "離")

        # Test Thunder trigram (100)
        self.assertEqual(map_trigram("788"), "震")

        # Test Wind trigram (011)
        self.assertEqual(map_trigram("679"), "巽")

        # Test Water trigram (010)
        self.assertEqual(map_trigram("678"), "坎")

        # Test Mountain trigram (001)
        self.assertEqual(map_trigram("669"), "艮")

        # Test Earth trigram (000)
        self.assertEqual(map_trigram("668"), "坤")

        # Test that all valid inputs produce a known trigram
        # Any 3-digit string with digits from 6-9 should produce a valid trigram
        self.assertIn(map_trigram("678"), ["乾", "兌", "離", "震", "巽", "坎", "艮", "坤"])

    def test_get_random_hexagram(self):
        # Test that the function returns a 6-digit string
        hexagram = get_random_hexagram()
        self.assertEqual(len(hexagram), 6)
        self.assertTrue(all(digit in "6789" for digit in hexagram))

if __name__ == '__main__':
    unittest.main()
