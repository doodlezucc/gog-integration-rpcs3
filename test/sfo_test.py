import unittest

from src.sfo import decode_sfo_file


class TestSfoDecoder(unittest.TestCase):
    def test_wipeout_sfo(self):
        sfo = decode_sfo_file("test/wipeout.sfo")

        self.assertEqual(sfo.title, "WipEout® HD Fury")
        self.assertEqual(sfo.app_version, "02.00")
        self.assertEqual(sfo.category, "DG")  # "Disc Game"


if __name__ == "__main__":
    unittest.main()
