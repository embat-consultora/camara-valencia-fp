import streamlit as st
from modules.data_base import get, getEqual, getEquals
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import practicaTabla
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Prácticas", page_icon="🚀")
st.markdown(
    "<h2 style='text-align: center;'>PRÁCTICAS</h2>",
    unsafe_allow_html=True
)
practicas = get(practicaTabla)
st.dataframe(practicas)