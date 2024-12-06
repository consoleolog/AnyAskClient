import streamlit as st
from streamlit.runtime.state import SessionStateProxy

def create_chat_session_state(p_session_state: SessionStateProxy):
    if not p_session_state["messages"]:
        p_session_state["messages"] = []
        return p_session_state["messages"]
    else:
        return p_session_state["messages"]

#
# url = "http://localhost:8080/api/chat/room"
#
# header = {"Content-Type": "application/json;charset=UTF-8"}
#
# if len(st.session_state["chat_history"]) == 0:
#     data = {
#         "regUser": "vxhpbjx45ft9tq_83ie4df_ccev5_kxuoqu3ttg66yg8wqvq-g",
#         "title": message
#     }
#     response = requests.post(url=url, headers=header, json=data)
#
#     result = response.json()
