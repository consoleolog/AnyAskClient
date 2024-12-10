import os

import psycopg
import streamlit as st
from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_postgres import PostgresChatMessageHistory

## ENVIRONMENT SETTING ##
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
table_name="message_store"
session_id = str("72f7c036-d42a-4616-a97d-65116ade55ee")
sync_connection = psycopg.connect(os.getenv("DB_URL"))

st.session_state["chat_history"] = []

## SESSION STATE SETTING ##
store = {}
PostgresChatMessageHistory.create_tables(sync_connection, table_name)
message_store = PostgresChatMessageHistory(
    table_name,
    session_id,
    sync_connection=sync_connection,
)

## OPENAI MODEL SETTING ##
class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)

model = ChatOpenAI(
    model_name="gpt-4o-mini",
    streaming=True,
    callbacks=[ChatCallbackHandler()]
)

## FUNCTIONS ##
def get_message_store(session_id):
    if session_id not in store:
        store[session_id] = PostgresChatMessageHistory(
            table_name,
            session_id,
            sync_connection=sync_connection,
        )
    return store[session_id]

def save_message(message, role):
    st.session_state["chat_history"].append({"message": message, "role": role})

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)

def paint_history(store, session_id):
    if store[session_id] is None:
        return

    for msg in store[session_id].get_messages():
        if type(msg) == HumanMessage:
            send_message(msg.content, "human")
        elif type(msg) == AIMessage:
            send_message(msg.content, "ai")


## PAGE SETTING ##

st.title("")

# paint_history(store=store, session_id=session_id)

message = st.chat_input("any ask...")

if message:
    send_message(message=message, role="human")

    prompt = ChatPromptTemplate.from_messages([
        ("system","say in korean"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{input}")
    ])
    chain = prompt | model
    with_message_store = RunnableWithMessageHistory(
        chain,
        get_message_store,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    with st.chat_message("ai"):
        response = with_message_store.invoke(
            {"input": message, },
            config={"configurable": {"session_id": session_id, }, },
        )
