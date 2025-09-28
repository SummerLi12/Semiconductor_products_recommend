from src.data_loader import SuppliesDataLoader
from src.vector_store import VectorStoreBuilder
from src.recommender import SuppliesRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
import os

class SemiconductorProductRecommendationPipeline:
    def __init__(self, data_dir="data", vectorstore_dir="chroma_db", csv_path=None):
        self.data_dir = data_dir
        self.vectorstore_dir = vectorstore_dir
        self.csv_path = csv_path or os.path.join(data_dir, "combined_products.csv")
        self._ensure_data()
        self._ensure_vectorstore()
        self._init_recommender()

    def _ensure_data(self):
        loader = SuppliesDataLoader(self.data_dir)
        df = loader.get_up_to_date_products()
        df.to_csv(self.csv_path, index=False)

    def _ensure_vectorstore(self):
        builder = VectorStoreBuilder(self.csv_path, self.vectorstore_dir)
        builder.build_and_save_vectorstore()
        self.vectorstore = builder.load_vector_store()

    def _init_recommender(self):
        retriever = self.vectorstore.as_retriever()
        self.recommender = SuppliesRecommender(retriever, GROQ_API_KEY, MODEL_NAME)

    def recommend(self, query):
        return self.recommender.get_recommendation(query)
