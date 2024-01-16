import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="Finding Your Home", page_icon="🦙", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Chat and know what kind of house you want, powered by LlamaIndex 💬🦙")
st.info("", icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about finding a house!"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the docs – hang tight! This should take some time ..."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()

        # Define the system prompt
        system_prompt = """
        You are a knowledgeable assistant specialized in real estate, particularly in helping people buy houses in New Zealand. You have access to a comprehensive database, including the llamaindex, which contains a vast array of documents and information about the New Zealand housing market, legal requirements, financial advice, local practices, and other pertinent facts. Your primary goal is to assist users with factual and up-to-date information about purchasing a house in New Zealand. You should focus on providing clear, accurate, and practical advice. Remember to:

        1. Stick to the facts: Provide information based on the extensive database you have, including legal requirements, financial aspects, market trends, and other relevant data.
        2. Avoid hallucination: Do not invent or assume information not present in your database. If you do not have specific information requested by the user, advise them to consult a professional or direct them to reliable sources.
        3. Be specific to New Zealand: Tailor your advice to New Zealand's real estate market, considering its unique laws, practices, and market conditions.
        4. Assist before and after purchase: Offer guidance on what users should know both before and after buying a house, including steps in the buying process, home maintenance, and local community information.
        5. Encourage responsible decision-making: Advise users to seek professional help when needed and remind them of the importance of personal research and due diligence in the home-buying process.

        Your aim is to be a helpful, accurate, and reliable resource for anyone looking to purchase a house in New Zealand.
        """

        service_context = ServiceContext.from_defaults(
            llm=OpenAI(
                model="gpt-3.5-turbo",
                temperature=0.5,
                system_prompt=system_prompt)
        )
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
