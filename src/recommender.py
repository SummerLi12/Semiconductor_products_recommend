#retrival 
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_Semiconductor_supplies_prompt


class SuppliesRecommender:
    def __init__(self,retriever,api_key:str,model_name:str):
        self.llm = ChatGroq(api_key=api_key,model=model_name,temperature=0)
        self.prompt = get_Semiconductor_supplies_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type = "stuff",
            retriever = retriever,
            chain_type_kwargs = {"prompt":self.prompt},
            return_source_documents = True
        )

    def get_recommendation(self,query:str):
        return self.qa_chain({"query":query})