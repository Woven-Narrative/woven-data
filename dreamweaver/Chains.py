import streamlit as st
import pandas as pd
import math
import requests
from langchain import PromptTemplate
from openai.embeddings_utils import get_embedding
import openai
from langchain.llms import OpenAI
import psycopg2

class Chains():
    
    ## Global Variables & Settings =========================================
    
    def __init__(self):                
        self.openai_api_key = st.secrets["OPENAI_API_KEY"]
        openai.api_key = self.openai_api_key
        self.embedding_model = "text-embedding-ada-002"
        self.dbpassword = st.secrets["DB_PASSWORD"]

    ## Language Models =====================================================
    
    def get_llm_obj(self):
        """
        The langchain class that can be used to interact with an LLM.
        """
        return OpenAI(openai_api_key=self.openai_api_key)

    def generate_embedding(self, query):
        """
        Get the embedding for a query from open ai.
        """    
        try:
            embedding = get_embedding(query, engine=self.embedding_model)
            return embedding
        except Exception as e:
            print(e)
            return None        
    
    ## Database Queries ====================================================
    
    def db_match_documents(self, match_threshold: float, match_count: int, text_embedding: str): 
        """
        Returns a set of matched DB rows based on the files cosine similarity.
        Match threshold is the minimum match score you want in your responses.
        Match count is the max number of rows you want returned.
        base url is the supabase url, token is the secret token.
        query embeddings is the openai embedding that you want to compare to the docs.
        """        

        # Connect to the database
        conn = psycopg2.connect(
            host='db.ygekpgxfilepvvgfdbhr.supabase.co',
            database='postgres',
            user='postgres',
            password=self.dbpassword,
            port='5432'    
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a query
        cur.execute(f"""
        select
            filename,
            filetxt,
            1 - (embeddings <=> '{text_embedding}') as similarity
        from summary_embd
        where 1 - (embeddings <=> '{text_embedding}') > {match_threshold}
        order by similarity desc
        limit {match_count};
        """)

        # Fetch the results
        rows = cur.fetchall()
        
        # turn into df
        column_names = [desc[0] for desc in cur.description]        
        df = pd.DataFrame(rows, columns=column_names)

        response_df = df[["filename","filetxt"]]

        # Close your cursor and connection
        cur.close()
        conn.close()

        # Now you can work with the DataFrame
        return response_df        

    ## Chains ==============================================================
    def find_similar_projects(self, criteria: str, filters: dict):
        """
        Find and return similar projects based on the similarity of a users criteria to
        a filtered list of projects. Filters provided in a dictionary by the user.
        """                    
        num_to_return = filters["return_max"]
        
        # increase the request count - will be filtered down
        db_match_count = math.floor(num_to_return * 1.5)
        
        # embedding user question
        user_embedding = self.generate_embedding(query=criteria)
        
        # request similar documents with filtering
        similar_documents_df = self.db_match_documents(match_threshold=0.75, 
                                                       match_count=db_match_count, 
                                                       text_embedding=user_embedding)        
        
        return similar_documents_df
    
    def refine_results(self):
        
        # get the llm object
        open_ai_llm = self.get_llm_obj()
        
        # Step 2: Generate a list of summaries - based on their criteria
        
        filtering_prompt_tempalte = """/
        Given criteria and an excerpt about a mining project. Can you please
        summarize the key points about the mining project mentioned in 
        the excerpt and tell me how many of my criteria this project fulfills?
        
        My criteria are: 
        
        {user_criteria}
        
        Excerpt about the mining project:
        
        {project_description}
        
        """        
        prompt_1 = PromptTemplate.from_template(filtering_prompt_tempalte)
                
        document_summaries = []            
                
        for document_text in similar_documents_df["filetxt"].tolist():
            prompt_1.format(user_criteria=criteria, project_description=document_text)
            prompt_1_response = "\n\n###\n\n" + open_ai_llm(prompt_1)    
            document_summaries.append(prompt_1_response)
        
        # Step 3: filter down to the top n results
        
        template_2 = """/
        Please read through the following mining project summaries and 
        recommend the top {number} based on the number of criteria that they meet. 
        
        My criteria are {user_criteria}.
        
        Each project summary below is seperated by triple hashtags: 
        
        {projects} 
        
        """                                    
        
        # have LLM filter down to most relavent x results        
        
        prompt_2 = PromptTemplate.from_template(template_2)
        
        prompt_2.format(user_criteria=criteria, projects=document_summaries, number=num_to_return)
        
        final_response = open_ai_llm(prompt_2)
        
        return final_response
