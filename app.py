import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import streamlit as st
from src.chat import respond_cot, ConversationContext, UserInteraction

state = st.session_state

st.title("DSPy Chatbot")

# initialize conversation context
if "context" not in state:
    state["context"] = ConversationContext(window_size=10)

# initialize chat history
if "messages" not in state:
    state["messages"] = []

if "interaction" not in state:
    state["interaction"] = UserInteraction()

# Display chat messages from history on app rerun
for message in state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter message..."):

    state["interaction"].message = prompt

    # add user to chat history
    state.messages.append(state["interaction"].serialize_by_role()[0])

    # display user input in chat container
    with st.chat_message("user"):
        st.markdown(state["interaction"].message)

    # display assistant responses in chat container
    with st.chat_message("assistant"):

        # get assistant response
        state["interaction"].response = respond_cot(
            context=state["context"].render(),
            message=state["interaction"].message
            ).response
        
        st.markdown(state["interaction"].response)

    # add assistant to chat history
    state.messages.append(state["interaction"].serialize_by_role()[1])

    # update conversation context
    state["context"].update(state["interaction"])

    # reinitialize interaction
    state["interaction"] = UserInteraction()

    