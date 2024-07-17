import requests
import streamlit as st

from src.logger import logging
from src.exception import ScriptWritingException

def get_bedrock_response(script_content):
    try:
        logging.info("'main': Post request to the backend API with given data")
        response = requests.post(
            "https://um2uyx1zb5.execute-api.us-east-1.amazonaws.com/dev/analyze_script",
            json={
                'script_content': script_content
            }
        )
        logging.info(f"'main': Request response: {response}")
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

st.title('Script Writing Assistant')

suggestions = ""

with st.form("my_form"):
    st.write("Fill the input fields below: ")
    script_content = st.text_input('Enter the script content here: ')
    logging.info(f"'main': Script content: {script_content}")

    submitted = st.form_submit_button("Submit")
    if submitted:
        logging.info("'main': Data submitted, now invoking the Backend API")
        suggestions = get_bedrock_response(script_content)
        logging.info(f"'main': Generated response: {suggestions}")
        if 'error' in suggestions:
            st.error(f"Error: {suggestions['error']}")
        else:
            st.write(suggestions)

def get_finalyzed_response(improved_script_content):
    try:
        logging.info("'main': Post request to the backend API with given data")
        response = requests.post(
            "https://r6w9fqv8d2.execute-api.us-east-1.amazonaws.com/dev/finalize_script",
            json={
                'improved_script_content': improved_script_content,
                'suggestion': suggestions
            }
        )
        logging.info(f"'main': Request response: {response}")
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

with st.form("my_form2"):
    st.write("Fill the input fields below: ")
    improved_script_content = st.text_input('Enter the improved script content here: ')
    logging.info(f"'main': Script content: {improved_script_content}")

    submitted = st.form_submit_button("Submit")
    if submitted:
        logging.info("'main': Data submitted, now invoking the Backend API")
        final_script = get_finalyzed_response(improved_script_content)
        logging.info(f"'main': Final script: {final_script}")
        if 'error' in final_script:
            st.error(f"Error: {final_script['error']}")
        else:
            st.write(final_script)



