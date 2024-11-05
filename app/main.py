"""Streamlit app."""
from typing import List
import requests
import streamlit as st
from app.env_settings import API_URL

st.set_page_config(page_title="Fitness Scheduling Assistant", page_icon="🏋️‍♀️")
st.title("Fitness Scheduling Assistant")

def call_ml_services(messages: List[dict]) -> dict:
    """Call ML services."""
    url = f"{API_URL}/message/create"
    ml_response = requests.post(
        url,
        json={
            "messages": messages
        },
        timeout=30
        )

    return ml_response.json()["message"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! I'm Sam, your personal fitness assistant. How are you doing today?"
            }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Type a message..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner("typing..."):
        response = call_ml_services(st.session_state.messages)
        with st.chat_message(response["role"]):
            st.markdown(response["content"])

        st.session_state.messages.append(response)
