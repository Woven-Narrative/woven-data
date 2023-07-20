"""
To Run:
streamlit run SearchDemo.py
"""
import streamlit as st
from datetime import date
import pandas as pd
from dreamweaver import chains

# Defining The Application UI
def main():    
    
    st.set_page_config(
        page_title="Woven Mining Project Search",
        page_icon=":pick:",
        layout="wide",
    )
    
    df = pd.DataFrame(columns=['Project', 'Company', 'Date', 'LLM Response'])
    
    # these are stored and used in queries
    filters = {
        "resource_type":[],
        "geography": [],
        "company":[],
        "start_date":date(2017, 7, 6),
        "end_date":date(2022, 7, 6),
        "development_stage":"",
        "is_operating":True,
        "return_max":10
    }
    
    # temp var to show us what the request looks like in development
    request = {}
    
    # Sidebar ===============================
    
    with st.sidebar:        
        
        st.markdown("# **Project Filters:**")
        
        filters["is_operating"] = st.checkbox("Site Is Operating", value=True)
        
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
            ['Agnico Eagle','Alamos Gold','Kinross Gold','Teck Resources','Barrick','Glencore',
             'Rio Tinto','Anglo American','Yamana Gold','Silvercorp Metals','SSR Mining','Newmont',
             'Hudbay Minerals','B2Gold Corp','American Lithium']
        )
        
        filters["start_date"] = st.date_input(
                                "Start Date",
                                date(2017, 7, 6))
                                
        filters["start_date"] = st.date_input(
                                "End Date",
                                date(2020, 7, 6))                    

        filters["geography"] = st.multiselect(
            'Geographies(s)',
            ['Canada','United States','Mexico','Congo','South Africa','Germany',
             'Columbia','Chile','Peru','France','United Kingdom','Australia',
             'Bolivia','Angola','Sierra Leon']
        )
        
        filters["return_max"] = st.number_input("Max Response Length:", 
                                                step=1, 
                                                max_value=100, 
                                                min_value=1
                                            )

    # Main Area ===============================
    
    st.title("Woven Mining Project Search") 
        
    user_input = st.text_area(
        "Describe The Criteria of your Project:", 
        value="", 
        height=100, 
        key="user_input"
    )

    st.markdown("""        
        Examples:
        
        *Copper projects that have their own power supplies.*
        
        *Gold mines that have produced over 10 MT.* 
    """
    )

    if st.button('Search'):
        # Here you can call your function using the user's input
        response = chains.find_similar_projects(criteria=user_input, filters=filters)
        request = filters
        # here is where you use the prompt and filters to call a chain
    
    st.dataframe(df, use_container_width=True)
    
    st.json(request)
    
    st.write(response.type)

# run the app
if "__main__" == __name__:
    main()