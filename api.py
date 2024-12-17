import httpx
import requests
import streamlit as st

SERVER_URL = "http://localhost:8080/v1/api"


def send_message(message, role):
    with st.chat_message(role):
        st.markdown(message)

def print_stream_message(response):
    with st.chat_message("ai"):
        message_box = st.empty()
        result = ""
        for chunk in response.iter_text():
            result += chunk
            message_box.markdown(result)

def request_message(message, cb):
    url = SERVER_URL + "/chat/stream"
    body = {"content": (None, message)}

    with httpx.stream(method="POST", url=url, files=body) as r:
        if r.status_code == 200:
            cb(r)
        else:
            print(f"에러 발생: HTTP {r.status_code} - {r.text}")

def request_create_vectorstore(file):
    url = SERVER_URL + "/chat/create_vectorstore"

def request_login(userId, userPwd):
    url = SERVER_URL + "/auth/login"
    body = {"userId": userId, "userPwd": userPwd}
