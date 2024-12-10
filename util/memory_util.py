from langchain_postgres import PostgresChatMessageHistory

from client.providers import Provider


def create_message_store():
    PostgresChatMessageHistory(Provider.sync_connection, Provider.message_store_table_name)

def init(store, session_id):
    if Provider.message_store_table_name not in store:
        pass