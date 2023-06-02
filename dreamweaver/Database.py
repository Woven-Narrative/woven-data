import requests
import pandas as pd
import streamlit as st

class Database:
    
    def __init__(self) -> None:
        self.token = st.secrets["PUBLICKEY"]
        self.baseurl = st.secrets["URL"]
    
    # cache to prevent multiple calls to the API
    @st.cache
    def get_similar_documents(self, match_threshold: float, match_count: int, query_embedding: str, baseurl: str, token: str): 
        """
        Returns a set of matched DB rows based on the files cosine similarity.
        Match threshold is the minimum match score you want in your responses.
        Match count is the max number of rows you want returned.
        base url is the supabase url, token is the secret token.
        query embeddings is the openai embedding that you want to compare to the docs.
        """
        
        # prepare the elements of the request
        headers = {
                'Content-Type': 'application/json',
                'apikey': self.token,
                'Authorization': 'Bearer ' + self.token
                }
        url = baseurl + "/rest/v1/rpc/match_documents"
        body_json = {
                'match_threshold':match_threshold,
                'match_count':match_count,
                'query_embedding':query_embedding
                }
        
        # make the request
        response = requests.post(url, 
                                headers=headers,
                                json=body_json)

        # check and return response
        if (response.ok):
            normalized = pd.json_normalize(response.json())         
            return normalized
        else:
            return response.status_code