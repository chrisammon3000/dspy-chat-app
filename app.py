import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import streamlit as st
from src.chat import respond_cot, ConversationContext, UserInteraction

# state = st.session_state

st.title("DSPy Chatbot")

# initialize conversation context
if "context" not in st.session_state:
    st.session_state["context"] = ConversationContext(window_size=10)

# initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "interaction" not in st.session_state:
    st.session_state["interaction"] = UserInteraction()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter message..."):

    st.session_state["interaction"].message = prompt

    # add user to chat history
    st.session_state.messages.append(st.session_state["interaction"].serialize_by_role()[0])

    # display user input in chat container
    with st.chat_message("user"):
        st.markdown(st.session_state["interaction"].message)

    # display assistant responses in chat container
    with st.chat_message("assistant"):

        # get assistant response
        st.session_state["interaction"].response = respond_cot(
            context=st.session_state["context"].render(),
            message=st.session_state["interaction"].message
            ).response
        
        st.markdown(st.session_state["interaction"].response)

    # add assistant to chat history
    st.session_state.messages.append(st.session_state["interaction"].serialize_by_role()[1])

    # update conversation context
    st.session_state["context"].update(st.session_state["interaction"])

    # reinitialize interaction
    st.session_state["interaction"] = UserInteraction()