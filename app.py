import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import streamlit as st
from src.chat import respond_cot, ConversationContext, UserInteraction

st.title("DSPy Chatbot")

# # set default model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# initialize conversation context
if "context" not in st.session_state:
    st.session_state["context"] = ConversationContext(window_size=5)

# initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = st.session_state["context"].content

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter message..."):

    # add user to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # display assistant responses in chat container
    with st.chat_message("assistant"):
        # stream = client.chat.completions.create(
        #     model=st.session_state["openai_model"],
        #     messages=[
        #         {
        #             "role": m["role"],
        #             "content": m["content"]
        #         } for m in st.session_state.messages
        #     ],
        #     stream=True
        # )

        # response = st.write_stream(stream)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })