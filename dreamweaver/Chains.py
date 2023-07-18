import streamlit as st
import pandas as pd
import math
from .database import Database
from .languagemodel import LanguageModel
from langchain import PromptTemplate

class Chains:

    @staticmethod
    def find_similar_projects(self, criteria: str, filters: dict) -> pd.DataFrame:
        """
        Find and return similar projects based on the similarity of a users criteria to
        a filtered list of projects. Filters provided in a dictionary by the user.
        """
        
        # Step 1: get the top n results - based on embedding similarity
        
        num_to_return = filters["return_max"]
        
        # increase the request count - will be filtered down
        db_match_count = math.floor(num_to_return * 1.5)
        
        # embedding user question
        user_embedding = LanguageModel.embed_request(criteria)
        
        # request similar documents with filtering
        similar_documents_df = Database.get_similar_documents(match_threshold=0.75, 
                                                              match_count=db_match_count, 
                                                              text_embedding=str(user_embedding))        
        
        # get the llm object
        llm = LanguageModel.get_llm()
        
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
                
        for t in similar_documents_df["text"].tolist():
            prompt_1.format(user_criteria="colorful socks", projects=similar_documents_df)    
            document_summaries.append(llm(prompt_1))                        
        
        # Step 3: filter down to the top n results
        
        template_2 = """/
        Please read through the following mining project summaries and 
        recommend the top {number} based on the number of criteria that they meet. 
        
        My criteria are {user_criteria}.
        
        Each project summary below is seperated by triple hashtags: 
        
        {projects}                 
        
        """                                    
        
        # have LLM filter down to most relavent x results        
        
        response = "the top summaries"
        
        return response
