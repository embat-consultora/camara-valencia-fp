import streamlit as st
def st_custom_message(text, color="#3498db", fontColor="#000000",emoji="💬"):
    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:15px;
            border-radius:10px;
            color:{fontColor};
            font-weight:500;
            margin-bottom:10px;
        ">
            {emoji} {text}
        </div>
        """,
        unsafe_allow_html=True
    )