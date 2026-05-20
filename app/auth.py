import streamlit as st

from database.auth_db import (
    create_users_table,
    register_user,
    login_user
)

create_users_table()


def login_page():

    st.subheader("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login Successful")
            st.rerun()

        else:

            st.error("Invalid Credentials")


def register_page():

    st.subheader("📝 Register")

    username = st.text_input("Create Username")

    password = st.text_input(
        "Create Password",
        type="password"
    )

    if st.button("Register"):

        success = register_user(username, password)

        if success:

            st.success("Registration Successful")

        else:

            st.error("Username already exists")