import httpx
import requests
import socket
import streamlit as st

SERVER_URL = "http://localhost:8080/api/v1"


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

def request_chatroom(room_user_id):
    print(room_user_id)
    url = SERVER_URL + "/chat/"
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    body = { "roomUserId": room_user_id }
    response = requests.post(url=url, headers=headers, data=body)
    print(response)
    print(response.status_code)
    print(response.text)

def ip():
    return socket.gethostbyname(socket.getfqdn())

def request_message(message, cb):
    url = SERVER_URL + "/chat/stream"
    body = {
        "content": (None, message),
        "userId": ip()
    }
    response = requests.post(url=url,  files=body)
    result = response.json()
    return result["msg"]
    # with httpx.stream(method="POST", url=url, files=body) as r:
    #     if r.status_code == 200:
    #         cb(r)
    #     else:
    #         print(f"에러 발생: HTTP {r.status_code} - {r.text}")

def request_create_vectorstore(file):
    url = SERVER_URL + "/chat/create_vectorstore"

def request_login(userId, userPwd):
    url = SERVER_URL + "/auth/login"
    body = {"userId": userId, "userPwd": userPwd}
