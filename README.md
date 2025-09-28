 # Semiconductor Product Recommender System

 ## Introduction

An intelligent recommendation system that helps users discover semiconductor products, sensors, and MCUs based on natural language queries. This project leverages a Retrieval-Augmented Generation (RAG) pipeline with a Large Language Model (LLM) to provide accurate and contextually relevant product suggestions.

The application is built with a Streamlit web interface, making it interactive and user-friendly.

 <!-- It's a good idea to add a screenshot of your app here! -->

## ✨ Features

- **Natural Language Queries**: Ask for products in plain English (e.g., "low-power MCU with Bluetooth 5.0 and AEC-Q100 certification").
- **RAG-Powered Recommendations**: Utilizes a vector database (ChromaDB) and the Groq LPU Inference Engine for fast, accurate, and context-aware product recommendations.
- **Interactive Web UI**: A clean and intuitive interface built with Streamlit.
- **Downloadable Results**: Export recommendation results to a CSV file for offline analysis.
- **Automatic Data Updates**: A scheduled script runs daily to check for and integrate new product data.
- **Update History**: The UI displays a history of when the product database was last updated and what new items were added.

## ⚙️ Architecture

The system is built around a classic RAG pipeline:

1.  **Data Loading**: Product data is loaded from local CSV files (`Intel`, `NXP`, `TSMC` datasets).
2.  **Vector Store**: The product information is processed and stored as vector embeddings in a **ChromaDB** database using `all-MiniLM-L6-v2` embeddings.
3.  **User Query**: The user enters a query through the Streamlit UI.
4.  **Retrieval**: The system retrieves the most relevant product documents from ChromaDB based on the user's query.
5.  **Generation**: The retrieved documents (context) and the original query are passed to a **Groq**-powered LLM (`llama-3.1-8b-instant`) using a structured prompt.
6.  **Response**: The LLM generates a detailed, formatted recommendation, which is then displayed to the user.

### Tech Stack

- **Backend & ML**: Python, LangChain, Pandas
- **LLM & Embeddings**: Groq, HuggingFace Transformers
- **Vector Database**: ChromaDB
- **Frontend**: Streamlit
- **Scheduling**: `schedule`

## 📂 Project Structure

```bash
chipsandsensors-recommender/
├── app/
│   └── app.py                # Streamlit web application
├── config/
│   └── config.py             # Configuration for API keys, models, paths
├── data/
│   ├── *.csv                 # Source product datasets
│   └── *.json                # Update history and info
├── pipeline/
│   ├── pipeline.py           # Main RAG pipeline orchestration
│   └── test_pipeline.py      # Script to test the pipeline
├── src/
│   ├── data_loader.py        # Loads data from CSVs and fetches updates
│   ├── recommender.py        # Contains the RetrievalQA chain
│   ├── vector_store.py       # Builds and manages the ChromaDB vector store
│   └── prompt_template.py    # Defines the prompt for the LLM
├── tests/
│   └── test_*.py             # Unit tests for components
├── .env                      # Environment variables (API keys)
├── .gitignore                # Files and directories to ignore
├── auto_update.py            # Standalone script for daily data updates
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory (or inside the `server` folder, depending on your setup). You can copy the `example.env` file if one is provided.

```
# .env
DATABASE_URL="mongodb://localhost:27017/my_awesome_app_db"
PORT=5000
```

### 4. Install Dependencies and Run

You will need two separate terminal windows: one for the backend server and one for the frontend client.

**Terminal 1: Run the Backend**
```bash
# Navigate to the server folder (if you have one)
# cd server

npm install
npm run dev
```
> The backend API should now be running on `http://localhost:5000`.

**Terminal 2: Run the Frontend**
```bash
# Navigate to the client folder (if you have one)
# cd client

npm install
npm start
```
> The frontend application should now be running and open in your browser at `http://localhost:3000`.

## Contributing

 We welcome contributions! Please see `CONTRIBUTING.md` for details on how to contribute to this project.

 ## License

 This project is licensed under the [Your License Name] - see the `LICENSE.md` file for details.

 ## Contact

 If you have any questions or suggestions, feel free to reach out:
 *   **Your Name/Team:** [Your Name or Team Name]
 *   **Email:** [your.email@example.com]
 *   **Project Link:** [https://github.com/your-username/my-awesome-app]
