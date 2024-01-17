# 🦙📚 LlamaIndex - Chat with the property docs

Build a chatbot powered by LlamaIndex that augments GPT 3.5 with the contents of the Streamlit docs (or your own data).

## Overview of the App

<img src="app.png" width="75%">

- Takes user queries via Streamlit's `st.chat_input` and displays both user queries and model responses with `st.chat_message`
- Uses LlamaIndex to load and index data and create a chat engine that will retrieve context from that data to respond to each user query


## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

~~## Try out the app~~

~~Once the app is loaded, enter your question about the Streamlit library and wait for a response.~~

## Original Repo
[Build a chatbot with custom data sources, powered by LlamaIndex](https://github.com/carolinedlu/llamaindex-chat-with-streamlit-docs/tree/main?ref=blog.streamlit.io)
