import unittest
import os
from src.data_loader import SuppliesDataLoader

class TestSuppliesDataLoader(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        self.loader = SuppliesDataLoader(self.data_dir)

    def test_load_and_combine(self):
        df = self.loader.load_and_combine()
        self.assertFalse(df.empty)
        self.assertIn('part_number', df.columns)  # Intel/NXP CSVs

    def test_get_up_to_date_products(self):
        df = self.loader.get_up_to_date_products()
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()
