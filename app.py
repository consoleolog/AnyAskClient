import streamlit as st
from websocket import create_connection, WebSocketConnectionClosedException
import threading
import base64
import json

from dto.chat_message import ChatMessage

st.set_page_config(
    page_title="Streamlit WebSocket File Chat",
    page_icon="📤",
)
st.title("a")

WEBSOCKET_URL = "ws://127.0.0.1:8089/ws"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

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

# def receive_messages(ws):
#     while True:
#         try:
#             message = ws.recv()
#             parsed_message = json.loads(message)
#
#             if parsed_message["type"] == "text":
#                 send_message(parsed_message["content"], "ai")
#             elif parsed_message["type"] == "file":
#                 file_name = parsed_message["file_name"]
#                 file_data = base64.b64decode(parsed_message["content"])
#
#                 # 파일 저장
#                 with open(f"./downloads/{file_name}", "wb") as f:
#                     f.write(file_data)
#                 send_file_ui(file_name, "ai")
#         except WebSocketConnectionClosedException:
#             break
#         except Exception as e:
#             print("Error receiving message:", e)
#             break
#

try:
    ws = create_connection(WEBSOCKET_URL,5)
    # threading.Thread(target=receive_messages, args=(ws,)).start()
except Exception as e:
    st.error("WebSocket 연결에 실패했습니다.")
    ws = None

# st.title("")
#
uploaded_file = st.file_uploader("파일을 업로드하세요")
if uploaded_file and ws:
    file_data = uploaded_file.read()
    file_name = uploaded_file.name

    chat_message = ChatMessage(
        type="file",
        name=file_name,
        content=base64.b64encode(file_data).decode('utf-8')
    )

    # Send message
    ws.send(json.dumps(chat_message.__dict__()))

    # Wait for response
    response = ws.recv()
    st.write(response)
