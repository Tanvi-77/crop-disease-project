import streamlit as st

def apply_dark_theme():

    st.markdown(
        """
        <style>

        /* =========================
           MAIN APP
        ========================== */

        .stApp {
            background: linear-gradient(
                135deg,
                #0f172a,
                #111827,
                #1e293b
            );
            color: white;
        }

        /* =========================
           TEXT COLORS
        ========================== */

        h1, h2, h3, h4, h5, h6,
        p, label, span, div {
            color: white !important;
        }

        /* =========================
           SIDEBAR
        ========================== */

        section[data-testid="stSidebar"] {
            background-color: #020617;
            border-right: 1px solid #1e293b;
        }

        /* =========================
           BUTTONS
        ========================== */

        .stButton > button {
            width: 100%;
            background: linear-gradient(
                90deg,
                #22c55e,
                #16a34a
            );

            color: white;
            border: none;
            border-radius: 12px;

            padding: 12px;

            font-weight: bold;
            font-size: 16px;

            transition: 0.3s ease;
        }

        .stButton > button:hover {

            transform: scale(1.02);

            background: linear-gradient(
                90deg,
                #16a34a,
                #15803d
            );
        }

        /* =========================
           INPUT FIELDS
        ========================== */

        .stTextInput input,
        .stSelectbox div,
        .stFileUploader,
        textarea {

            background-color: #1e293b !important;

            color: white !important;

            border-radius: 10px !important;

            border: 1px solid #334155 !important;
        }

        /* =========================
           SELECTBOX TEXT
        ========================== */

        div[data-baseweb="select"] > div {
            background-color: #1e293b !important;
            color: white !important;
        }

        /* =========================
           FILE UPLOADER
        ========================== */

        section[data-testid="stFileUploader"] {
            background-color: #111827;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #334155;
        }

        /* =========================
           METRICS / CARDS
        ========================== */

        .custom-card {

            background-color: rgba(
                30,
                41,
                59,
                0.7
            );

            padding: 20px;

            border-radius: 16px;

            border: 1px solid #334155;

            backdrop-filter: blur(10px);

            margin-bottom: 20px;
        }

        /* =========================
           SUCCESS BOX
        ========================== */

        div[data-testid="stAlert"] {

            border-radius: 12px;
        }

        /* =========================
           SCROLLBAR
        ========================== */

        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #0f172a;
        }

        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 10px;
        }

        /* =========================
           PROGRESS BAR
        ========================== */

        div[data-testid="stProgressBar"] > div > div {
            background-color: #22c55e;
        }

        </style>
        """,
        unsafe_allow_html=True
    )