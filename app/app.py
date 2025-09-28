import streamlit as st
from dotenv import load_dotenv
import sys
import os
import json
import pandas as pd
import re

# --- Setup path for pipeline import ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.pipeline import SemiconductorProductRecommendationPipeline

# --- Streamlit Page Config ---
st.set_page_config(page_title="Semiconductor Product Recommender", layout="wide")

load_dotenv()

@st.cache_resource
def init_pipeline():
    return SemiconductorProductRecommendationPipeline()

pipeline = init_pipeline()

st.title("Semiconductor Product Recommender System")

# --- Layout: Search/Recommendation (left), Update History (right) ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("🔍 Product Search & Recommendation")
    query = st.text_input("Enter your product requirements (e.g., search for LiDAR and radar sensors with AEC-Q100 certification,low-power MCU, industrial sensor, etc.)")

    if query:
        with st.spinner("Fetching recommendations for you....."):
            result = pipeline.recommend(query)
            response_text = result.get("result", "Could not retrieve recommendations.")
            source_documents = result.get("source_documents", [])

            st.markdown("### Recommendations")
            st.write(response_text)

            # --- Build DataFrame for CSV ---
            products_df = None

            # 1. Try to parse structured product blocks
            product_blocks = re.findall(
                r'\*\*Product Title:\*\*\s*(.*?)\s*\n'
                r'(?:\s*\*\*Summary:\*\*\s*(.*?)\n)?'
                r'(?:\s*\*\*Reasoning.*?:\*\*\s*(.*?)\n)?'
                r'(?:\s*\*\*Key Features.*?:\*\*\s*(.*?)(?=\n\n|\Z))?',
                response_text,
                re.DOTALL
            )

            parsed = []
            for idx, block in enumerate(product_blocks, start=1):
                record = {"Rank": idx, "Product Title": block[0].strip()}
                if block[1]:
                    record["Summary"] = block[1].strip()
                if block[2]:
                    record["Reasoning"] = block[2].strip()
                if block[3]:
                    record["Key Features"] = block[3].strip().replace("\n", " ")
                parsed.append(record)

            products_df = pd.DataFrame(parsed)

            # 2. Fallback if no structured matches → split by numbering
            if products_df.empty:
                product_blocks = re.split(r'\n?\d+\.\s+', response_text)
                product_blocks = [p.strip() for p in product_blocks if p.strip()]

                # Skip intro text if it doesn’t look like a product
                if product_blocks and not product_blocks[0].lower().startswith(("**product title", "cyw", "nrf", "esp", "stm", "ti", "nxp", "bosch")):
                    product_blocks = product_blocks[1:]

                parsed = [{"Rank": idx, "Product Title": block} for idx, block in enumerate(product_blocks, start=1)]
                products_df = pd.DataFrame(parsed)

            # 3. Always add the query column
            products_df.insert(0, "User Query", query)

            # 4. Clean up
            if "row" in products_df.columns:
                products_df = products_df.drop(columns=["row"])

            # --- CSV Download ---
            csv = products_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Recommendations as CSV",
                data=csv,
                file_name="semiconductor_recommendations.csv",
                mime="text/csv",
            )

with right_col:
    # --- Show update info ---
    update_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'update_info.json'))
    if os.path.exists(update_info_path):
        with open(update_info_path, 'r', encoding='utf-8') as f:
            update_info = json.load(f)
        if update_info:
            st.info(f"**Last update:** {update_info['last_update_time']} | **New items added:** {update_info['new_items_count']}")
            if update_info['new_items_count'] > 0:
                if st.button('Review New Products', key='review_new_products'):
                    st.markdown('### Newly Added Products')
                    st.dataframe(update_info['new_products'])

    # --- Show update history ---
    update_history_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'update_history.json'))
    if os.path.exists(update_history_path):
        with open(update_history_path, 'r', encoding='utf-8') as f:
            update_history = json.load(f)
        if update_history and len(update_history) > 1:
            st.markdown('---')
            st.subheader('🕒 Product Update History')
            for event in reversed(update_history):
                if event['new_items_count'] > 0:
                    cols = st.columns([1, 2, 2])
                    with cols[0]:
                        st.markdown(f"<span style='font-size:2em;'>📦</span>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"<b>{event['update_time']}</b>")
                    with cols[2]:
                        st.markdown(
                            f"<span style='background-color:#e0f7fa; color:#00796b; padding:4px 10px; border-radius:8px; font-weight:bold;'>+{event['new_items_count']} new</span>",
                            unsafe_allow_html=True
                        )
                    with st.expander('Show new products', expanded=False):
                        st.dataframe(event['new_products'])
