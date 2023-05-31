"""
To Run:
streamlit run SearchDemo.py
"""
import streamlit as st
import openai
import dreamweaver.utils as utils

# Defining The Application Variables
openai.api_key = st.secrets["OPENAI_API_KEY"]
token = st.secrets["PUBLICKEY"]
baseurl = st.secrets["URL"]

# Defining The Application UI
def main():    
    
    st.title("Woven Mining Project Search")    

    user_input = st.text_area(
        "Describe the criteria of your project", 
        value="", 
        height=300, 
        key="user_input"
    )

    if st.button('Search'):
        # Here you can call your function using the user's input
        #response = utils.make_query(user_input)
        response = utils.query_supabase(query=user_input, baseurl=baseurl, token=token, return_count=15)
        # Write the result to the page
        st.write(response)

# run the app
if "__main__" == __name__:
    main()