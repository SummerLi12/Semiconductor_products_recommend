import unittest
from src.recommender import SuppliesRecommender
from unittest.mock import MagicMock

class TestSuppliesRecommender(unittest.TestCase):
    def setUp(self):
        # Mock retriever and API key/model
        self.mock_retriever = MagicMock()
        self.api_key = "fake_key"
        self.model_name = "fake_model"
        self.recommender = SuppliesRecommender(self.mock_retriever, self.api_key, self.model_name)

    def test_get_recommendation(self):
        # Mock the QA chain's return value
        self.recommender.qa_chain = MagicMock(return_value={"result": "Recommended product"})
        result = self.recommender.get_recommendation("test query")
        self.assertEqual(result, "Recommended product")

if __name__ == '__main__':
    unittest.main()
