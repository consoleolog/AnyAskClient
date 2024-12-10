import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import FAISS
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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

def embed_file(file):
    file_content = file.read()
    file_path = f"{os.getcwd()}/cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    loader = UnstructuredLoader(file_path)
    docs = loader.load()
    print(docs[12])
    return docs


st.set_page_config(
    page_title="Document",
    page_icon="📃",
)

def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})


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


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer the question using ONLY the following context. 
            Context: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

st.title("문서")


with st.sidebar:
    file = st.file_uploader(
        "Upload a .txt .pdf or .docx file",
        type=["pdf", "txt", "docx"],
    )

if file:
    docs = embed_file(file)
    summarize_chain = load_summarize_chain(model, chain_type="stuff")
    def get_docs(x):
        return summarize_chain.invoke(docs)
    send_message("이제 물어보셈", "ai", save=False)
    paint_history()
    message = st.chat_input("물어보셈")
    if message:
        send_message(message, "human")
        chain = (
                {
                    "context":  get_docs,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | model
        )
        with st.chat_message("ai"):
            chain.invoke({
                "question": message
            })


else:
    st.session_state["messages"] = []