import streamlit as st

from dto.chat_message import ChatMessage
from util.chat_util import send_message, request_llm, load_history

st.set_page_config(
    page_title="Chat",
    page_icon="📤",
)
st.title("a")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

with st.sidebar:
    file = st.file_uploader(
        "Upload file",
        type=["docx","pptx","pdf"]
    )

message = st.chat_input("Ask anything")

load_history()

if message:
    send_message(message=message, role="human")

    with st.chat_message("ai"):
        ai_message_container = st.empty()
        ai_message_text = ""
        for chunk in request_llm(message):
            ai_message_text += chunk["message"]
            ai_message_container.markdown(ai_message_text)