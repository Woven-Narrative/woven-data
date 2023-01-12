"""
To Run:
streamlit run SearchDemo.py
"""

import streamlit as st
import pandas as pd
import requests

# Defining The Application Variables

token = st.secrets["PUBLICKEY"]
baseurl = st.secrets["URL"]
search_phrase_endpoint = st.secrets["SEARCHPHRASE_ENDPOINT"]

headers = {'Content-Type': 'application/json',
            'apikey': token,
            'Authorization': 'Bearer ' + token}

# Defining The Application Functions

def clean_df(df) -> pd.DataFrame:
    df_cleaned = df[["company","date","filename"]]
    df_cleaned = df_cleaned.rename(columns={"filename": "File", "company": "Company", "date": "Date"})
    return df_cleaned

def search_metrics(df) -> dict:
    company_count = df["Company"].nunique()
    record_count = df["File"].count()
    return {"companies":str(company_count), "rows":str(record_count)}

# cache to prevent multiple calls to the API
@st.cache
def search_phrase(phrase: str):        
    url = baseurl + search_phrase_endpoint        
    response = requests.post(url, 
                            headers=headers,
                            json={'phrase_input': phrase})
    #st.write(url)
    #st.write(response)
    # check and return response
    if (response.ok):
        normalized = pd.json_normalize(response.json())         
        return normalized
    else:
        return response.status_code    

# Defining The Application UI

def main():    
    
    st.title("Smart Search Demo")    

    with st.sidebar:
        st.header("Search Parameters :pick:")
        st.subheader("Use the following tool to search for phrases in the Woven Mining database of NI 43-101 technical reports.")
        text = st.text_input("Enter a phrase to search for:")

    if st.sidebar.button('Search Phrase'):
        if text != "":        
            # search for the term and clean response
            raw_data = search_phrase(str(text))            
            if(not raw_data.empty):
                cleaned_df = clean_df(raw_data)
                # compute metrics
                metrics = search_metrics(cleaned_df)            
                # cols for metrics
                col1, col2 = st.columns(2)
                col1.metric(label="Total Files", value=metrics["rows"])
                col2.metric(label="Unique Companies", value=metrics["companies"])
                # display results
                st.write(cleaned_df)
            else:
                st.write('No results found...')
        else:
            st.sidebar.write('Needs a phrase to search for...')
                
    with st.sidebar:
        st.write("#")                                     
        st.write("#### Created By Woven Mining Inc.")

# run the app
if "__main__" == __name__:
    main()