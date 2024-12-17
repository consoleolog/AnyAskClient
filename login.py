import os

import streamlit as st


@st.dialog("로그인")
def login():

    userId = st.text_input("id",placeholder="아이디를 입력하세요.")
    userPwd = st.text_input("pwd",placeholder="비밀번호를 입력하세요.")

    if st.button("Login"):
        print(userId)
        print(userPwd)

    st.divider()

    st.markdown("[![kakao login](http://localhost:8501/app/static/kakao_login.png)](http://localhost:8080/oauth2/authorization/kakao)")
