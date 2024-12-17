import streamlit as st

import requests
from api import send_message, print_stream_message, request_message
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

requests.get(
    url="http://localhost:8080/v1/api/"
)

with st.sidebar:
    if st.button("로그인"):
        login()

message = st.chat_input("askanything")

if message:
    send_message(message, "human")

    request_message(message, print_stream_message)

