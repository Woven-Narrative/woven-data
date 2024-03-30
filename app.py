import streamlit as st
from datetime import date
import pandas as pd
from database import Database
from annotated_text import annotated_text

# Defining The Application UI
def main():        

    # needs to be called first
    st.set_page_config(
        page_title="Woven Mining",
        page_icon=":pick:",
        layout="wide",
    )

    url = st.secrets["XATA_DATABASE_URL"]
    key = st.secrets["XATA_API_KEY"]
   
    # setup filters

    db = Database(url, key)
    
    df = pd.DataFrame(columns=['Project', 'Company', 'Date', 'LLM Response'])
    
    # these are stored and used in queries
    filters = {
        "resource_type":[],
        "geography": [],
        "company":[],
        "start_date":date(2017, 7, 6),
        "end_date":date(2023, 7, 6),
        "development_stage":"",
        "is_operating":True,
        "return_max":50
    }    
    
    # Sidebar ===============================
    
    # mine type
    # how does the company set their reserve price vs market price
    # have market prices for resources selected on the screen    
    
    st.markdown(
        """
        <style>
            em {
                text-decoration: none;
                background: #ffffb3;
                padding: 3px 6px;
                color: #000;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:                

        st.title("A Sample of Woven Mining's Technical Reports Dataset")

        st.markdown("## **Filters (Not Implemented):**")
        
        #filters["is_operating"] = st.checkbox("Site Is Operating", value=True)
        
        filters["resource_type"] = st.multiselect(
            'Resource Type(s)',
            ['Gold', 'Copper', 'Lithuim', 'Coal',"Urnanium",
             "Cobalt","Zinc","Nickle","Iron","Silver",
             "Aluminum","Tin","Palladium","Chromite",
             "Vanadium","Titanium","Zirconium"
             ]
        )
        
        filters["company"] = st.multiselect(
            'Companies(s)',
            ['Tribeca Resources','Agnico Eagle','Alamos Gold','Kinross Gold','Teck Resources','Barrick','Glencore',
             'Rio Tinto','Anglo American','Yamana Gold','Silvercorp Metals','SSR Mining','Newmont',
             'Hudbay Minerals','B2Gold Corp','American Lithium']
        )
        
        filters["start_date"] = st.date_input(
                                "Start Date",
                                date(2017, 7, 6))
                                
        filters["end_date"] = st.date_input(
                                "End Date",
                                date(2020, 7, 6))                    

        filters["geography"] = st.multiselect(
            'Geographies(s)',
            ['Canada','Australia','United States','Chile','Mexico','Peru','Congo','South Africa','Germany','China',
             'France','United Kingdom','Indonesia'
             'Bolivia','Angola','Sierra Leon']
        )
        
        #filters["return_max"] = st.number_input("Max Response Length:", step=1, max_value=100, min_value=1)

    # Main Area ===============================
    
    st.title("NI 43-101 Explorer") 
        
    user_input = st.text_area(
        "Enter Search Text", 
        value="", 
        height=1, 
        key="user_input"
    )

    if st.button('Search'):
        # Here you can call your function using the user's input
        response = db.search_summarys(searchtext=user_input)    
        #st.dataframe(df, use_container_width=True)
        for file in response:
            st.markdown(f"#### {file}")
            rows = response[file]
            for row in rows:
                st.markdown(row, unsafe_allow_html=True)
            #annotated_text(v)

        #st.write(response)

# run the app
if "__main__" == __name__:
    main()
