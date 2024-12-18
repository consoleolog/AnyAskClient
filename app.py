import time

import streamlit as st
import socket
import requests
from api import send_message, print_stream_message, request_message, request_chatroom
from login import login

st.set_page_config(
    page_title="Home",
    page_icon="🤖",
)

style = """
<style>
@import url(https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css);
html, body, [class*="css"]  {
            font-family: 'NanumSquare', 'sans-serif';
}
</style>
"""
st.markdown(style, unsafe_allow_html=True)


with st.sidebar:
    if st.button("로그인"):
        login()


message = st.chat_input("App Page")
SERVER_URL = "http://localhost:8080/api/v1"

r = requests.get(SERVER_URL + "/chat/")
print(r.text)

if message:
    send_message(message, "human")

    res = request_message(message, None)

    # url = SERVER_URL + "/chat/ai"
    # headers = {
    #     "Content-Type": "application/json;charset=UTF-8",
    #     "credential": "include"
    # }
    # body = {
    #     "content": res,
    #     "user_id": ""
    # }
    #
    # requests.post(url=url, headers=headers, data=body)

    def stream_data():
        for word in res.split(" "):
            yield word + " "
            time.sleep(0.02)

    with st.chat_message("ai"):
        st.write_stream(stream_data)
