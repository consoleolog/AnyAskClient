import json

import requests
import streamlit as st
from streamlit.runtime.state import SessionStateProxy

def create_chat_session_state(p_session_state: SessionStateProxy):
    if not p_session_state["messages"]:
        p_session_state["messages"] = []
        return p_session_state["messages"]
    else:
        return p_session_state["messages"]

def save_message(message: str, role: str) -> None:
    """세션 상태에 메시지 저장"""
    st.session_state["chat_history"].append({"message": message, "role": role})

def send_message(message: str, role: str) -> None:
    """메시지 UI 표시 및 저장"""
    with st.chat_message(role):
        st.markdown(message)
    save_message(message, role)

def send_file_ui(file_name: str, role: str) -> None:
    """파일 전송 UI"""
    with st.chat_message(role):
        st.markdown(f"[{file_name} 다운로드](./downloads/{file_name})")
    save_message(f"파일 전송: {file_name}", role)

def load_history() -> None:
    """저장된 채팅 기록 불러오기"""
    for history in st.session_state["chat_history"]:
        send_message(history["message"], history["role"])

def request_llm(message):
    url = "http://localhost:80/streaming_async/chat"

    headers = {
        "Content-Type": "application/json;charset=utf-8",
    }

    data = {"message": message}

    response = requests.post(url=url, headers=headers, data=json.dumps(data), stream=True)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").strip()
            if decoded_line.startswith("data:"):
                yield json.loads(decoded_line[5:])  # Remove "data:" prefix and parse JSON
