from xata.client import XataClient
import streamlit as st
from pandas import DataFrame

class Database:

    def __init__(self, db_url, db_key) -> None:
        self.xata = XataClient(api_key=db_key, db_url=db_url)

    def search_summarys(self, searchtext: str) -> dict:

        # fuzzieness is the number of bad characters search will forgive in a match
        results = self.xata.data().search_table("summary_sections_rows",{
            "query": searchtext,
            "target": ['filename','summary'],            
            "fuzziness": 1,        
            "prefix": "phrase",
            "page": {"size": 20, "offset": 0}
        })

        clean_results_df = self.format_search_results(results, searchtext)

        return clean_results_df
    
    def format_search_results(self, results: dict, searchtext: str) -> dict:

        base_results_dict = {}

        # Extracting relevant data into lists
        for file in results["records"]:
            name = file["filename"].replace(".txt","")
            base_results_dict[name] = file["xata"]["highlight"]["summary"]            

        # create annotated text tuple
        for file in base_results_dict:
            foundtexts = base_results_dict[file]
            newtextlines = []
            for line in foundtexts:  
                replacedline = line.replace("<em>", '<em class="highlight">')    
                newtextlines.append(replacedline)
            base_results_dict[file] = newtextlines

        return base_results_dict
