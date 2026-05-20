import streamlit as st
from PIL import Image
import tempfile
import os
import sys

# =========================
# FIX IMPORT PATH
# =========================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# =========================
# IMPORTS
# =========================

from utils.predictor import predict_image
from utils.translations import translations

from database.db import (
    create_table,
    insert_prediction,
    fetch_history
)

from styles import apply_dark_theme

from auth import (
    login_page,
    register_page
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Crop Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# APPLY THEME
# =========================

apply_dark_theme()

# =========================
# CREATE DATABASE
# =========================

create_table()

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# =========================
# AUTHENTICATION
# =========================

if not st.session_state.logged_in:

    st.title("🌱 Crop Disease Detection")

    auth_option = st.sidebar.radio(
        "Authentication",
        ["Login", "Register"]
    )

    if auth_option == "Login":

        login_page()

    else:

        register_page()

    st.stop()

# =========================
# LANGUAGE SELECTOR
# =========================

language = st.sidebar.selectbox(
    "🌐 Select Language",
    ["English", "Hindi", "Marathi"]
)

text = translations[language]

# =========================
# SIDEBAR
# =========================

st.sidebar.markdown("## 🌱 Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        text["home"],
        text["detection"],
        text["history"]
    ]
)

st.sidebar.success(
    f"👤 {st.session_state.username}"
)

# ============================================================
# HOME PAGE
# ============================================================

if page == text["home"]:

    st.markdown(f"""
    <div style="
        padding-top:10px;
        padding-bottom:25px;
    ">

    <h1 style="
        color:white;
        font-size:55px;
        margin-bottom:5px;
        font-weight:700;
    ">
    🌱 {text["title"]}
    </h1>

    <p style="
        color:#cbd5e1;
        font-size:22px;
        margin-top:0px;
    ">
    {text["subtitle"]}
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )

    # =====================================================
    # FEATURE CARDS
    # =====================================================

    if language == "English":

        feature_cards = [
            ("📷", "Camera Support"),
            ("🦠", "Disease Detection"),
            ("📊", "Confidence Score"),
            ("💡", "Treatment Solutions"),
            ("🗂", "Prediction History"),
            ("🌐", "Multi-language")
        ]

        quick_title = "Quick Actions"

        btn1 = "Detect Disease"
        btn2 = "View History"
        btn3 = "Refresh Dashboard"

    elif language == "Hindi":

        feature_cards = [
            ("📷", "कैमरा सपोर्ट"),
            ("🦠", "रोग पहचान"),
            ("📊", "विश्वास स्तर"),
            ("💡", "उपचार समाधान"),
            ("🗂", "पूर्वानुमान इतिहास"),
            ("🌐", "बहुभाषी समर्थन")
        ]

        quick_title = "त्वरित विकल्प"

        btn1 = "रोग पहचान"
        btn2 = "इतिहास देखें"
        btn3 = "डैशबोर्ड रीफ्रेश"

    else:

        feature_cards = [
            ("📷", "कॅमेरा सपोर्ट"),
            ("🦠", "रोग ओळख"),
            ("📊", "विश्वास पातळी"),
            ("💡", "उपचार उपाय"),
            ("🗂", "पूर्वीचा इतिहास"),
            ("🌐", "अनेक भाषा समर्थन")
        ]

        quick_title = "जलद पर्याय"

        btn1 = "रोग ओळखा"
        btn2 = "इतिहास पहा"
        btn3 = "डॅशबोर्ड रीफ्रेश"

    # =====================================================
    # FEATURE CARDS ROW 1
    # =====================================================

    col1, col2, col3 = st.columns(3)

    first_row = feature_cards[:3]

    for col, card in zip(
        [col1, col2, col3],
        first_row
    ):

        icon, text_card = card

        with col:

            st.markdown(f"""
            <div style="
                background:rgba(30,41,59,0.88);
                padding:25px;
                border-radius:18px;
                border:1px solid #334155;
                text-align:center;
                height:150px;
                margin-bottom:20px;
            ">

            <div style="
                font-size:42px;
                margin-bottom:12px;
            ">
            {icon}
            </div>

            <h3 style="
                color:white;
                font-size:20px;
                margin-top:10px;
            ">
            {text_card}
            </h3>

            </div>
            """,
            unsafe_allow_html=True
            )

    # =====================================================
    # FEATURE CARDS ROW 2
    # =====================================================

    col4, col5, col6 = st.columns(3)

    second_row = feature_cards[3:]

    for col, card in zip(
        [col4, col5, col6],
        second_row
    ):

        icon, text_card = card

        with col:

            st.markdown(f"""
            <div style="
                background:rgba(30,41,59,0.88);
                padding:25px;
                border-radius:18px;
                border:1px solid #334155;
                text-align:center;
                height:150px;
                margin-bottom:25px;
            ">

            <div style="
                font-size:42px;
                margin-bottom:12px;
            ">
            {icon}
            </div>

            <h3 style="
                color:white;
                font-size:20px;
                margin-top:10px;
            ">
            {text_card}
            </h3>

            </div>
            """,
            unsafe_allow_html=True
            )

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.markdown(f"""
    <div style="
        background:rgba(30,41,59,0.88);
        padding:25px;
        border-radius:18px;
        border:1px solid #334155;
        margin-top:15px;
        margin-bottom:20px;
    ">

    <h2 style="
        color:white;
        margin-bottom:10px;
    ">
    ⚡ {quick_title}
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    with b1:

        st.button(
            btn1,
            use_container_width=True
        )

    with b2:

        st.button(
            btn2,
            use_container_width=True
        )

    with b3:

        st.button(
            btn3,
            use_container_width=True
        )

# ============================================================
# DISEASE DETECTION PAGE
# ============================================================

elif page == text["detection"]:

    st.title(f"🦠 {text['detection']}")

    st.markdown(f"""
    <div class="custom-card">

    <p style="
        font-size:18px;
        color:#d1d5db;
    ">
    {text["upload_text"]}
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )

    crop = st.selectbox(
        text["select_crop"],
        ["Tomato", "Potato", "Pepper"]
    )

    uploaded_file = st.file_uploader(
        text["upload_image"],
        type=["jpg", "jpeg", "png"]
    )

    camera_image = st.camera_input(
        text["camera"]
    )

    if uploaded_file is not None or camera_image is not None:

        image_source = None

        if uploaded_file is not None:

            image_source = uploaded_file

        elif camera_image is not None:

            image_source = camera_image

        image = Image.open(image_source)

        st.image(
            image,
            caption="Leaf Image",
            use_container_width=True
        )

        if st.button(text["predict_button"]):

            with st.spinner("Analyzing image..."):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".jpg"
                ) as tmp_file:

                    tmp_file.write(
                        image_source.read()
                    )

                    temp_image_path = tmp_file.name

                try:

                    result = predict_image(
                        temp_image_path
                    )

                    insert_prediction(

                        image_source.name
                        if hasattr(image_source, "name")
                        else "camera_capture.jpg",

                        result["disease"],
                        result["confidence"],
                        result["solution"]
                    )

                    st.success(
                        "Prediction Complete!"
                    )

                    st.markdown("""
                    <div class="custom-card">
                    """,
                    unsafe_allow_html=True
                    )

                    st.subheader(
                        text["prediction_result"]
                    )

                    st.write(
                        f"### 🦠 {text['disease']}: {result['disease']}"
                    )

                    st.write(
                        f"### 📊 {text['confidence']}: {result['confidence']}%"
                    )

                    st.write(
                        f"### 💡 {text['solution']}: {result['solution']}"
                    )

                    confidence = float(
                        result["confidence"]
                    )

                    st.progress(
                        int(confidence)
                    )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )

                finally:

                    if os.path.exists(
                        temp_image_path
                    ):

                        os.remove(
                            temp_image_path
                        )

# ============================================================
# HISTORY PAGE
# ============================================================

elif page == text["history"]:

    st.title(f"📜 {text['history']}")

    history = fetch_history()

    if history:

        for row in history:

            st.markdown(f"""
            <div class="custom-card">

            <h4>📌 Image: {row[1]}</h4>

            <p>🦠 {text["disease"]}: {row[2]}</p>

            <p>📊 {text["confidence"]}: {row[3]}%</p>

            <p>💡 {text["solution"]}: {row[4]}</p>

            <p>⏰ Time: {row[5]}</p>

            </div>
            """,
            unsafe_allow_html=True
            )

    else:

        st.info(
            text["history_empty"]
        )