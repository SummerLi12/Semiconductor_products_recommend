import os
from dotenv import load_dotenv # read from .env file about api key and token to the environment

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"