from openai.embeddings_utils import get_embedding
import openai
import streamlit as st
from langchain.llms import OpenAI

class LanguageModel:
    
    def __init__(self):
        # Defining The Application Variables
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        self.embedding_model = "text-embedding-ada-002"

    @staticmethod
    def get_llm():
        """
        The langchain class that can be used to interact with an LLM.
        """
        return OpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"])

    @staticmethod
    def embed_request(self, query):
        embedding = get_embedding(query, engine=self.embedding_model)
        return embedding