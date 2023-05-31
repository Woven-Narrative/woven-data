from openai.embeddings_utils import cosine_similarity
from openai.embeddings_utils import get_embedding
import streamlit as st
import pandas as pd
import openai
import numpy as np
import requests
embedding_model = "text-embedding-ada-002"

def embed_request(query):
    embedding = get_embedding(query, engine=embedding_model)
    return embedding

def eval_individual_texts(query, text_list):
    """
    Please summarize the response. 
    Also, which elements of the response are those which were asked for
    in the query? Highlight them.
    Return a string of text with the response.
    """
    prompt_intro = """Here are some criteria and an excerpt about a mining project. Can you please
                      summarize the key points about the mining project mentioned in 
                      the excerpt and tell me how many of
                      my criteria this project fulfills?
                      \n\n###\n\n"""
    prompt = prompt_intro + f"My criteria are {query}. \n\n###\n\n" \
        " The project info is: \n\n###\n\n "
    r_list = []
    for t in text_list:
        r = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": t}
                ]
            )
        r_list.append(r['choices'][0]['message']['content'])
    return r_list

def eval_list_texts(query, responses, n = 5):
    """
    Given a list of project summaries, return the n most relevant
    The most relevant should be decided by how much they fit the criteria
    Return a list of the most relevant texts, and why they're relevant
    """
    delimiter = ' | '
    split_list = delimiter.join(responses)
    final_eval_prompt = 'Please read through the following mining project summaries and recommend the top 5 based on the number of criteria that they meet. '
    prompt = f"My criteria are {query}. \n\n###\n\n" \
        " The project info is: \n\n###\n\n "
    r = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": prompt + final_eval_prompt},
            {"role": "user", "content": split_list}
            ]
    )
    return r['choices'][0]['message']['content']

def make_query(query):
    df = read_df()
    user_embedding = embed_request(query)
    embed_comps = compare_embeddings(user_embedding, df, 15)
    text_summaries = eval_individual_texts(query, embed_comps)
    response = eval_list_texts(query, text_summaries)
    return response

# cache to prevent multiple calls to the API
@st.cache
def match_documents(match_threshold: float, match_count: int, query_embedding: str, baseurl: str, token: str): 
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
            'apikey': token,
            'Authorization': 'Bearer ' + token
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
