import openai
import LLM

class Prompt:        
    
    def summarize_and_eval_texts(self, user_query, text_list) -> list:
        """
        Summarize the response and returns a list of the results.
        Also, which elements of the response are those which were asked for
        in the query? Highlight them.
        
        Parameters
        ----------
        user_query : str
            The initial question posed by the user.
            
        text_list : list[str]
            A list of text related to the users question.
        
        >> Return a string of text with the response.
        """
        prompt_intro = """Here are some criteria and an excerpt about a mining project. Can you please
                        summarize the key points about the mining project mentioned in 
                        the excerpt and tell me how many of
                        my criteria this project fulfills?
                        \n\n###\n\n"""
                        
        prompt = prompt_intro + f"My criteria are {user_query}. \n\n###\n\n" \
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

    def eval_list_texts(self, query, responses, n = 5):
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