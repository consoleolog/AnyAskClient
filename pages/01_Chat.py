# import streamlit as st
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables import RunnableWithMessageHistory
#
# from client.providers import Provider
#
# st.session_state["messages"] = []
#
# st.title("")
#
# inputs = st.chat_input("")
#
# def save_message(store, message, role):
#     store.append({"message": message, "role": role})
#
# def send_message(message, role, save=True):
#     with st.chat_message(role):
#         st.markdown(message)
#     if save:
#         save_message(st.session_state["messages"],message, role)
#
#
#
# prompt = ChatPromptTemplate.from_messages([
#     ("system","say in korean"),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human","{input}")
# ])
# chain = prompt | Provider.model
# # with_message_store = RunnableWithMessageHistory(
# #     chain,
# #     get_message_store,
# #     input_messages_key="input",
# #     history_messages_key="chat_history",
# # )