"""
To Run:
streamlit run SearchDemo.py
"""

import streamlit as st
import openai
import utils

# Defining The Application Variables
with open ('env.txt', 'r') as f:
    api_key = f.read()
openai.api_key = api_key
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
        response = utils.make_query(user_input)
        # Write the result to the page
        st.write(response)

# run the app
if "__main__" == __name__:
    main()