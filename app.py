import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

st.set_page_config(page_title="RAG Chat App")
st.title('RAG Chat App')

openai.api_key = st.secrets['auth_key']
#openai_api_key = st.sidebar.text_input('OpenAI API Key')
#openai_model = st.sidebar.selectbox('AI model', ('gpt-3.5-turbo', 'gpt-4o-mini'),)
#openai_temp = st.sidebar.slider('Temperature', min_value=0.1, max_value=0.8, value=0.2)
openai_prompt = st.sidebar.text_area('OpenAI Prompt', """You are an expert on ERP Project Management and project risk management. Assume that all questions are related to managing projects. Keep your answers technical and based on facts – do not hallucinate features.""", 
                                     height=204)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about ERP Project Management",
        }
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        system_prompt=openai_prompt,
    )
    with st.container(height-none, border=True):
      container.write("Input data: ", docs)
      
    index = VectorStoreIndex.from_documents(docs)
    return index

index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = st.session_state.chat_engine.stream_chat(prompt)
        st.write_stream(response_stream.response_gen)
        message = {"role": "assistant", "content": response_stream.response}
        # Add response to message history
        st.session_state.messages.append(message)

