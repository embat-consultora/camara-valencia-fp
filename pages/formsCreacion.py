import streamlit as st
import json
import os
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.data_base import get, add, getOrdered, update, getEqual
from variables import formTabla, formFieldsTabla, tipoCampo,categoria

apply_page_config()
make_sidebar()

base_url = os.getenv("URL")

st.set_page_config(page_title="Formularios", page_icon="🏢")

st.markdown(
    "<h2 style='text-align: center;'>Formularios</h2>",
    unsafe_allow_html=True
)
st.write("Selecciona el formulario que deseas completar o visualizar:")

forms = get(formTabla)
form_names = {f["id"]: f["nombre"] for f in forms}

col1, col2, col3 = st.columns([3, 2, 1])
with col1: 
    form_choice = st.selectbox("Selecciona un formulario", ["Nuevo"] + list(form_names.values()))

if form_choice == "Nuevo":
    new_name = st.text_input("Nombre del nuevo formulario")
    new_description = st.text_input("Descripción ")
    if st.button("Crear formulario"):
        if new_name.strip():
            new_form = add(formTabla, {"nombre": new_name, "descripcion": new_description}).data[0]
            st.success(f"Formulario '{new_name}' creado")
            st.rerun()
else:
    # --- Identificar el formulario seleccionado ---
    form_id = [fid for fid, name in form_names.items() if name == form_choice][0]

        # Traer info del form
    form = getEqual(formTabla, "id", form_id)
    form_nombre = form[0].get("nombre") or ""
    form_desc = form[0].get("descripcion") or ""

    st.subheader("Editar datos del formulario")

    new_form_name = st.text_input("Nombre del formulario", form_nombre, key=f"form_name_{form_id}")
    new_form_desc = st.text_area("Descripción del formulario", form_desc, key=f"form_desc_{form_id}")

    if st.button("Actualizar Formulario"):
        update(formTabla, {"nombre": new_form_name, "descripcion": new_form_desc}, {"id":form_id})
        st.success("Formulario actualizado")
        st.rerun()

    st.subheader(f"Editando formulario: {form_choice}")
    st.markdown(f"[Abrir formulario]({base_url}forms?form={form_id})")

    # --- Obtener campos existentes ---
    fields = getOrdered(formFieldsTabla, "form", form_id, "order_index")
    if fields:
        st.write("Campos existentes:")
        for field in fields:
            with st.expander(f"{field['order_index']}. {field['label']} ({field['type']})"):
                new_label = st.text_input("Etiqueta", field["label"], key=f"label_{field['id']}")
                new_type = st.selectbox(
                    "Tipo",
                    tipoCampo,
                    index=tipoCampo.index(field["type"]) if field["type"] in tipoCampo else 0,
                    key=f"type_{field['id']}"
                )
                colRequired, colCategory = st.columns(2)
                with colRequired:
                    new_required = st.checkbox("¿Obligatorio?", value=field["required"], key=f"req_{field['id']}")
                with colCategory:
                    category = st.selectbox(
                    "Categoría",
                    categoria,
                    index=categoria.index(field["category"]) if field["category"] in categoria else 0,
                    key=f"category_{field['id']}"
                )
                new_options = None
                if new_type in ["Opciones", "OpcionesConCantidad"]:
                    try:
                        existing_opts = json.loads(field.get("options") or "[]")
                    except Exception:
                        existing_opts = []

                    if isinstance(existing_opts, dict):
                        st.markdown("### Opciones agrupadas")
                        for g, opts in existing_opts.items():
                            st.markdown(f"**{g}** → {', '.join(opts)}")
                        raw_json = st.text_area(
                            "Editar opciones agrupadas (JSON)",
                            json.dumps(existing_opts, ensure_ascii=False, indent=2),
                            key=f"opts_grouped_{field['id']}"
                        )
                        try:
                            new_options = json.loads(raw_json)
                        except:
                            st.error("El JSON no es válido")
                    else:
                        st.markdown("### Opciones simples")
                        raw_options = st.text_area(
                            "Opciones (coma separadas)",
                            ",".join(existing_opts),
                            key=f"opts_simple_{field['id']}"
                        )
                        new_options = [o.strip() for o in raw_options.split(",") if o.strip()]


                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Actualizar", key=f"upd_{field['id']}"):
                        update_data = {
                            "label": new_label,
                            "type": new_type,
                            "required": new_required,
                            "category": category
                        }
                        if new_options is not None:
                            update_data["options"] = json.dumps(new_options, ensure_ascii=False)

                        update(formFieldsTabla, update_data, {"id": field["id"] })
                        st.success("Campo actualizado")
                        st.rerun()
                with col_b:
                    if st.button("Eliminar", key=f"del_{field['id']}"):
                        from modules.data_base import delete
                        delete(formFieldsTabla, "id", field["id"])
                        st.warning("Campo eliminado")
                        st.rerun()
    else:
        st.info("Este formulario no tiene campos aún.")

    st.divider()
    st.subheader("Agregar un nuevo campo")

    # --- Inputs para nuevo campo ---
    label = st.text_input("Etiqueta (label) del campo")
    field_type = st.selectbox("Tipo de campo", tipoCampo)
    colRequiredNew, colCategoryNew = st.columns(2)
    with colRequiredNew:
        required = st.checkbox("¿Es obligatorio?", value=True)
    with colCategoryNew:
        category = st.selectbox(
        "Categoría",
        categoria
    )
    options = None
    if field_type in ["Opciones", "OpcionesConCantidad"]:
        st.markdown("### Opciones simples o agrupadas")

        if "grouped_options" not in st.session_state:
            st.session_state.grouped_options = {}

        group_name = st.text_input("Título del grupo (si querés agrupar)", key="new_group_name")
        group_values = st.text_area("Opciones de este grupo (coma separadas)", key="new_group_values")

        if st.button("Agregar grupo"):
            if group_name.strip() and group_values.strip():
                opts = [o.strip() for o in group_values.split(",") if o.strip()]
                st.session_state.grouped_options[group_name] = opts
                st.success(f"Grupo '{group_name}' agregado con {len(opts)} opciones")

        if st.session_state.grouped_options:
            st.write("Grupos agregados:")
            for g, opts in st.session_state.grouped_options.items():
                st.markdown(f"**{g}** → {', '.join(opts)}")
            options = st.session_state.grouped_options
        else:
            raw_options = st.text_area("Opciones simples (coma separadas)", "Opción A,Opción B,Opción C", key="new_opts_simple")
            options = [o.strip() for o in raw_options.split(",") if o.strip()]

    if st.button("Agregar campo"):
        order_index = len(fields) + 1
        field_data = {
            "form": form_id,
            "label": label,
            "type": field_type,
            "required": required,
            "order_index": order_index,
            "category": category
        }
        if options:
            field_data["options"] = json.dumps(options, ensure_ascii=False)

        add(formFieldsTabla, field_data)
        st.success("Campo agregado")
        st.rerun()
