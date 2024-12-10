import json
import os
import uuid

import streamlit as st
import requests
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_unstructured import UnstructuredLoader

from logger import CustomLogger

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

logger = CustomLogger.get_logger(__name__)

st.set_page_config(
    page_title="Home",
    page_icon="🤖",
)

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)

chat_message_history = SQLChatMessageHistory(
    session_id=str(uuid.uuid4()),
    connection=os.getenv("DB_URL")
)
def chat_history(x):
    return chat_message_history.messages

def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})
    if role == "human":
        chat_message_history.add_user_message(message)
    elif role == "ai":
        chat_message_history.add_ai_message(message)

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history():
    for message in st.session_state["messages"]:
        send_message(
            message["message"],
            message["role"],
            save=False,
        )

def get_link(search_text):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-Key": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }
    payload = json.dumps({"q": search_text})
    response = requests.post(url=url, headers=headers, data=payload)
    result = response.json()

    links = []

    for r in result["organic"]:
        links.append(r["link"])
    logger.debug(links)
    return links

if "messages" not in st.session_state:
    st.session_state["messages"] = []

paint_history()

inputs = st.chat_input("ask anything..")

with st.sidebar:
    file = st.file_uploader(
        "클릭해보싈?",
        type=["pdf", "txt", "docx"],
    )

if file:
    if not os.path.exists(f"{os.getcwd()}/file"):
        os.mkdir(f"{os.getcwd()}/file")
    file_content = file.read()
    file_path = f"{os.getcwd()}/file/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    loader = UnstructuredLoader(file_path)

    def docs(x):
        d = loader.load()
        return d

    if docs(None):
        send_message("준비 완료 이제 물어보셈", "ai", False)

    template = ChatPromptTemplate.from_messages([
        ("system", """
        Context 를 참고해서 사용자의 질문에 답변해
        Context : {context}

        ChatHistory : {chat_history}
        """),
        ("human", "question: {question}")
    ])
    model = ChatOpenAI(model="gpt-4o-mini", callbacks=[ChatCallbackHandler()], streaming=True, cache=False)
    chain = {
                "context": docs,
                "chat_history": chat_history,
                "question": RunnablePassthrough(),
            } | template | model

    if inputs:

        send_message(inputs, "human")


        with st.chat_message("ai"):
            chain.invoke({"question": inputs})
if inputs:
        logger.info(inputs)

        # Web 기반 검색을 요청 했을 때
        if inputs.startswith("/web"):
            question = inputs.replace("/web", "")
            send_message(question, "human")

            template = ChatPromptTemplate.from_messages([
                ("system", """"
                너는 지금 사용자의 요구에 맞춰서 검색을 도와줘야해
                검색어를 추천해줘
                ChatHistory : {chat_history}
                """),
                ("human", "{question}")
            ])
            model = ChatOpenAI(model="gpt-4o-mini")

            result = (template | model | StrOutputParser()).invoke({
                "question": question,
                "chat_history": chat_message_history.messages
            })

            logger.debug("search text : " + result)

            links = get_link(question)

            for link in links:
                logger.info(f"Processing link: {link}")
                loader = WebBaseLoader(link)
                docs = loader.load()

                logger.debug(docs[0].page_content)

                logger.debug(f"Loaded docs for link: {link}")

                template = ChatPromptTemplate.from_messages([
                    ("system", """
                    Context에 사용자의 질문에 대한 해답이 있으면 해당 부분을 정리해
                    Context: {context}

                    ChatHistory: {chat_history}
                    """),
                    ("human", "question: {question}")
                ])
                model = ChatOpenAI(model="gpt-4o-mini", callbacks=[ChatCallbackHandler()], streaming=True, cache=False )

                # 결과 생성 및 출력
                with st.chat_message("ai"):

                    result = (template | model).invoke({
                        "question": question,
                        "context": docs,
                        "chat_history": chat_message_history.messages
                    })
                    logger.debug(f"Result for link {link}: {result}")
        # # 일반 요청
        # else:
        #     with st.chat_message("ai"):
        #         template = ChatPromptTemplate.from_messages([
        #             ("system", """
        #             ChatHistory : {chat_history}
        #             """),
        #             ("human", "{question}")
        #         ])
        #         chain = template | model
        #         chain.invoke({
        #             "question": inputs,
        #             "chat_history": chat_message_history.messages
        #         })

