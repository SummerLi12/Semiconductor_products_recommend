Welcome to our customer-focused platform : 

you could find easily the semiconductor products here to meet your needs
Save the recommendation items into CVS file for use later and keep getting updated time to time about the products.

1. create .env file with this code and api key and token will be provided in the presentation file

GROQ_API_KEY=""
HUGGINGFACEHUB_API_TOKEN=""

2. Install Dependencies and Run

pip install -r requirements.txt

3 run below code on the terminal

streamlit run app/app.py


for gcp: make sure in environment to run 
source venv/bin/activate
streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0
then navigate to http://34.45.1.125:8501/
