import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(page_title="RAG Chat App")
st.title('RAG Chat App')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
openai_model = st.sidebar.selectbox('AI model', ('gpt-3.5-turbo', 'gpt-4o-mini'),)
openai_temp = st.sidebar.slider('Temperature', min_value=0.1, max_value=0.8, value=0.2)
openai_prompt = st.sidebar.text_input('OpenAI prompt')

def generate_response(input_text):
  llm = OpenAI(openai_temp, openai_api_key=openai_api_key)
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'Enter your question here...')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(text)
      
