import unittest
from src.vector_store import VectorStoreBuilder
import os

class TestVectorStoreBuilder(unittest.TestCase):
    def setUp(self):
        self.csv_path = os.path.join(os.path.dirname(__file__), '../data/Intel_sensors_semiconductors_MCUs_full_dataset.csv')
        self.persist_dir = os.path.join(os.path.dirname(__file__), '../chroma_db_test')
        self.builder = VectorStoreBuilder(self.csv_path, self.persist_dir)

    def test_build_and_save_vectorstore(self):
        self.builder.build_and_save_vectorstore()
        # Check if persist_dir is created and not empty
        self.assertTrue(os.path.exists(self.persist_dir))
        self.assertTrue(len(os.listdir(self.persist_dir)) > 0)

    def test_load_vector_store(self):
        db = self.builder.load_vector_store()
        self.assertIsNotNone(db)

if __name__ == '__main__':
    unittest.main()
