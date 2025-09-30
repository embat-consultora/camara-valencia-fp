import streamlit as st
import json
from modules.data_base import getEqual, getOrdered, upsert,add
from variables import (
    formFieldsTabla,
    formTabla,
    empresasTabla,
    alumnosTabla,
    necesidadFP,
    alumnoEstadosTabla,
    empresaEstadosTabla
)
from datetime import datetime
st.set_page_config(page_title="Formulario", page_icon="🏢")
# Obtener form_id desde query param
form_id = st.query_params.get("form")

# Obtener nombre del form
form = getEqual(formTabla, "id", form_id)
form_name = form[0]["nombre"] or "Formulario"
form_desc = form[0].get("descripcion") or "Por favor, completa el siguiente formulario."
st.title(form_name)
st.subheader(form_desc)
# Obtener campos del form
fields = getOrdered(formFieldsTabla, "form", form_id, "order_index")

answers = {}
for field in fields:
    label = field["label"]
    ftype = field["type"]

    if ftype == "Texto":
        answers[field["id"]] = st.text_input(label)

    elif ftype == "Si/No":
        answers[field["id"]] = st.radio(label, ["Sí", "No"])

    elif ftype == "Cantidad":
        answers[field["id"]] = st.number_input(label, min_value=0, step=1)

    elif ftype == "Opciones":
        opts = json.loads(field.get("options") or "[]")
        selected = []

        with st.expander(label):   # 👈 la pregunta como expander
            if isinstance(opts, dict):
                # Opciones agrupadas → cada grupo con sus checkboxes
                for group, values in opts.items():
                    st.markdown(f"**{group}**")
                    for v in values:
                        if st.checkbox(v, key=f"{field['id']}_{group}_{v}"):
                            selected.append(v)
            else:
                # Opciones simples → checkboxes en lista
                for v in opts:
                    if st.checkbox(v, key=f"{field['id']}_{v}"):
                        selected.append(v)

        answers[field["id"]] = selected

    elif ftype == "OpcionesConCantidad":
        opts = json.loads(field.get("options") or "[]")
        selected = {}

        with st.expander(label):   # 👈 la pregunta como expander
            if isinstance(opts, dict):
                for group, values in opts.items():
                    st.markdown(f"*{group}*")
                    for v in values:
                        col1, col2 = st.columns([2,1])
                        with col1:
                            check = st.checkbox(v, key=f"{field['id']}_{group}_{v}")
                        if check:
                            with col2:
                                cantidad = st.number_input(
                                    "Cantidad",
                                    min_value=0,
                                    step=1,
                                    key=f"num_{field['id']}_{group}_{v}"
                                )
                                selected[v] = cantidad
            else:
                for v in opts:
                    col1, col2 = st.columns([2,1])
                    with col1:
                        check = st.checkbox(v, key=f"{field['id']}_{v}")
                    if check:
                        with col2:
                            cantidad = st.number_input(
                                "Cantidad",
                                min_value=0,
                                step=1,
                                key=f"num_{field['id']}_{v}"
                            )
                            selected[v] = cantidad

        answers[field["id"]] = selected

# Guardar
if st.button("Enviar formulario"):
    fecha_envio = datetime.now().isoformat()
    data_by_category = {
        "Empresa": {},
        "Alumno": {},
        "FP": {}
    }

    # Armar los diccionarios
    for field in fields:
        fid = field["id"]
        value = answers.get(fid)
        category = field.get("category")
        column = field.get("columnName")

        if not value or not category or not column:
            continue

        if category == "FP":
            data_by_category["FP"][column] = value
        elif category in ["Empresa", "Alumno"]:
            data_by_category[category][column] = value

    # Guardar Empresa
    if data_by_category["Empresa"]:
        data_by_category["FP"]["empresa"] = data_by_category["Empresa"].get("CIF", "N/A")
        res = upsert(empresasTabla, data_by_category["Empresa"], keys=["CIF"])
        upsert(
            empresaEstadosTabla,
            {"empresa": res.data[0]["CIF"], "form_completo": fecha_envio},
            keys=["empresa"]
        )

    # Guardar Alumno
    if data_by_category["Alumno"]:
       res = upsert(alumnosTabla, data_by_category["Alumno"], keys=["NIA"])
       upsert(alumnoEstadosTabla,{"alumno": res.data[0]["NIA"], "form_completo": fecha_envio},
                            keys=["alumno"])
    # Guardar FP (todo el dict como JSON)
    if data_by_category["FP"]:
        data_by_category["FP"]["estado"] = "Activo"
        add(necesidadFP, data_by_category["FP"])

    st.success("Formulario enviado correctamente")