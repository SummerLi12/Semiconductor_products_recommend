import streamlit as st
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.pipeline import SemiconductorProductRecommendationPipeline

st.set_page_config(page_title="Semiconductor Product Recommender", layout="wide")

load_dotenv()

@st.cache_resource
def init_pipeline():
    return SemiconductorProductRecommendationPipeline()

pipeline = init_pipeline()

st.title("Semiconductor Product Recommender System")

query = st.text_input("Enter your product requirements (e.g., low-power MCU, industrial sensor, etc.)")
if query:
    with st.spinner("Fetching recommendations for you....."):
        response = pipeline.recommend(query)
        st.markdown("### Recommendations")
        st.write(response)