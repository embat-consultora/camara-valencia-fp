import streamlit as st
import pandas as pd
import os
from modules.data_base import get, getEqual, update, upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import empresasTabla, necesidadFP, estados,fasesEmpresa, empresaEstadosTabla,fase2colEmpresa,opciones_motivo,bodyEmailsEmpresa,contactoEmpresaTabla
from datetime import datetime
from modules.emailSender import send_email
from modules.grafico_helper import mostrar_fases
import re
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Prácticas", page_icon="🚀")
st.markdown(
    "<h2 style='text-align: center;'>PRÁCTICAS</h2>",
    unsafe_allow_html=True
)
