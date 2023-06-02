from openai.embeddings_utils import get_embedding
import openai
import streamlit as st

class LLM:
    
    def __init__(self):
        # Defining The Application Variables
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        self.embedding_model = "text-embedding-ada-002"
    
    def embed_request(self, query):
        embedding = get_embedding(query, engine=self.embedding_model)
        return embedding
    
    #def chat_complete(prompt)
    
    #def openai.ChatCompletion.create(
    #                model = "gpt-3.5-turbo",
    #                messages = [
    #                    {"role": "system", "content": prompt},
    #                    {"role": "user", "content": t}
    #                ]
    #            )
    
    # other things we might ask the LLM to do