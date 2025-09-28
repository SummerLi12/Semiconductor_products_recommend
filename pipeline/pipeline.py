import os
import logging
from src.data_loader import SuppliesDataLoader
from src.vector_store import VectorStoreBuilder
from src.recommender import SuppliesRecommender
from config.config import GROQ_API_KEY, MODEL_NAME

# --- Setup Logger ---
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("SemiconductorPipeline")

class SemiconductorProductRecommendationPipeline:
    def __init__(self, data_dir="data", vectorstore_dir="chroma_db", csv_path=None):
        self.data_dir = data_dir
        self.vectorstore_dir = vectorstore_dir
        self.csv_path = csv_path or os.path.join(data_dir, "combined_products.csv")

        logger.info("Initializing SemiconductorProductRecommendationPipeline...")

        self._ensure_data()
        self._ensure_vectorstore()
        self._init_recommender()

        logger.info("✅ Pipeline initialized successfully.")

    def _ensure_data(self):
        logger.info("Loading and updating product data...")
        loader = SuppliesDataLoader(self.data_dir)
        df = loader.get_up_to_date_products()
        df.to_csv(self.csv_path, index=False)
        logger.info(f"✅ Data loaded and saved to {self.csv_path} ({len(df)} records).")

    def _ensure_vectorstore(self):
        logger.info("Building vector store...")
        builder = VectorStoreBuilder(self.csv_path, self.vectorstore_dir)
        builder.build_and_save_vectorstore()
        self.vectorstore = builder.load_vector_store()
        logger.info(f"✅ Vector store built and saved at {self.vectorstore_dir}")

    def _init_recommender(self):
        logger.info("Initializing recommender...")
        retriever = self.vectorstore.as_retriever()
        self.recommender = SuppliesRecommender(retriever, GROQ_API_KEY, MODEL_NAME)
        logger.info("✅ Recommender initialized successfully.")

    def recommend(self, query):
        logger.info(f"Running recommendation for query: '{query}'")
        try:
            result = self.recommender.get_recommendation(query)
            logger.info("✅ Recommendation generated successfully.")
            return result
        except Exception as e:
            logger.error(f"❌ Error during recommendation: {e}", exc_info=True)
            raise
