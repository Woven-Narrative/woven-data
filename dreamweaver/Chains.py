import streamlit as st
import pandas as pd
import numpy as np

def make_query(query):
    #df = read_df()
    user_embedding = embed_request(query)
    embed_comps = compare_embeddings(user_embedding, df, 15)
    text_summaries = eval_individual_texts(query, embed_comps)
    response = eval_list_texts(query, text_summaries)
    return response
   
def supabase_match_documents(query: str, baseurl: str, token: str, return_count: int):
    """
    Use the supabase match_documents endpoint to request similar documents then check them with chat gpt before returning.
    """
    user_embedding = embed_request(query)
    # just set it as threshold 0.78 to see what happens
    result = match_documents(match_threshold=0.78, match_count=return_count, query_embedding=user_embedding, baseurl=baseurl, token=token)
    #
    # add additional steps here !!
    #
    return result
