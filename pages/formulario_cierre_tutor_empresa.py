import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, forms, feedbackFormsTabla

st.set_page_config(page_title="Formulario Cierre para Empresas", page_icon="📨")

# --- Lógica de Validación (Fuera del form para no procesar accesos inválidos) ---
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token or not tipo_form or tipo_form != forms[3]:
    st.error("⚠️ Acceso no válido o link incorrecto.")
    st.stop()

feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o es incorrecto.")
    st.stop()

practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]

st.title("Formulario Cierre de Formación - Empresa")

# --- FORMULARIO PRINCIPAL ---
# Usamos clear_on_submit=False para que el usuario vea su confirmación al final
with st.form("feedback_form"):
    st.subheader("Datos generales")
    st.text_input("Empresa", value=feedback["empresa"], disabled=True)
    st.text_input("Alumno", value=feedback["alumno"], disabled=True)

    # --- Valoración cualitativa del tutor de empresa ---
    st.subheader("Valoración cualitativa del tutor de empresa")

    # 1
    actitud = st.radio(
        "1) Valoración de la actitud del alumnado durante su periodo en la empresa: "
        "Puntualidad, iniciativa, responsabilidad...",
        options=[0, 1, 2, 3, 4, 5],
        horizontal=True,
    )

    # 2
    seguimiento_tutor_centro = st.radio(
        "2) Valoración del seguimiento realizado por el tutor del centro educativo",
        options=[0, 1, 2, 3, 4, 5],
        horizontal=True,
    )

    # 3
    valoracion_general = st.radio(
        "3) Valoración general del desarrollo de la formación",
        options=[0, 1, 2, 3, 4, 5],
        horizontal=True,
    )

    # 4
    aspectos_positivos = st.text_area(
        "4) Aspectos positivos. (Destaque, al menos, un aspecto positivo de su "
        "participación en el proceso de formación.)"
    )

    # 5
    propuestas_mejora = st.text_area(
        "5) Propuestas de mejora. (Desde su punto de vista, indique, al menos, "
        "una propuesta respecto al proceso de formación del alumnado.)"
    )

    # --- Valoración cuantitativa sobre la inserción laboral ---
    st.subheader("Valoración cuantitativa sobre la inserción laboral")

    # 6
    oferta_relacion_laboral = st.radio(
        "6) ¿Se le ha ofrecido al alumno la posibilidad de mantener una relación "
        "laboral con la empresa/organismo?",
        options=["Sí", "No"],
        horizontal=True,
    )

    # 7 (aplica si la respuesta a 6 es "No")
    motivo_no_oferta = st.radio(
        "7) En caso de NO en la pregunta 6... ¿Por qué motivo?",
        options=[
            "a) Actualmente no se dispone de necesidad de contratación... pero "
            "tendría en cuenta al alumno/a para futuros puestos.",
            "b) El alumno/a no presenta las habilidades y capacidades suficientes "
            "para poder optar a un puesto correspondiente a su formación y perfil.",
            "c) Se trata de un organismo público en el que no es posible la "
            "contratación directa.",
        ],
    )

    # 8 (aplica si la respuesta a 6 es "Sí")
    tipo_contrato = st.radio(
        "8) En caso de SÍ en la pregunta 6... ¿Qué tipo de contrato?",
        options=["a) Contratación laboral indefinida", "b) Contratación temporal"],
    )

    # 9 (aplica si la respuesta a 6 es "Sí")
    alumno_acepto_oferta = st.radio(
        "9) En caso de SÍ en la pregunta 6... ¿Ha aceptado el alumno la oferta?",
        options=["Sí", "No"],
        horizontal=True,
    )

    # 10 (aplica si la respuesta a 9 es "No")
    motivo_no_aceptacion = st.radio(
        "10) En caso de NO en la pregunta 9... ¿Por qué motivo?",
        options=[
            "a) No le interesan las condiciones",
            "b) Desea seguir estudiando y no puede compaginar",
            "c) Otros",
        ],
    )

    # 11 (aplica si la respuesta a 10 es "c) Otros")
    detalle_otros_motivo = st.text_area(
        '11) En caso de "Otros" en la pregunta 10, detallar el motivo'
    )

    # 12
    recomendaria_contratacion = st.radio(
        "12) ¿Recomendaría a otra empresa/institución la contratación del alumno/a?",
        options=["Sí", "No"],
        horizontal=True,
    )

    # 13 (aplica si la respuesta a 12 es "No")
    motivo_no_recomendacion = st.text_area(
        "13) En caso de NO en la pregunta 12... ¿Por qué motivo?"
    )

    # Botón de envío específico del formulario
    submit_button = st.form_submit_button("Enviar")

# --- PROCESAMIENTO POST-ENVÍO ---
if submit_button:
    with st.spinner("Guardando tu respuesta..."):
        respuestas_json = {
            "tipo": tipo_form,
            "valoracion_tutor_empresa": {
                "actitud_alumnado": actitud,
                "seguimiento_tutor_centro": seguimiento_tutor_centro,
                "valoracion_general_formacion": valoracion_general,
                "aspectos_positivos": aspectos_positivos,
                "propuestas_mejora": propuestas_mejora,
            },
            "insercion_laboral": {
                "oferta_relacion_laboral": oferta_relacion_laboral,
                "motivo_no_oferta": motivo_no_oferta,
                "tipo_contrato": tipo_contrato,
                "alumno_acepto_oferta": alumno_acepto_oferta,
                "motivo_no_aceptacion": motivo_no_aceptacion,
                "detalle_otros_motivo": detalle_otros_motivo,
                "recomendaria_contratacion": recomendaria_contratacion,
                "motivo_no_recomendacion": motivo_no_recomendacion,
            },
        }

        payload = {
            "feedback_form_id": feedback_form_id,
            "practica_id": practica_id,
            "respuestas_json": respuestas_json,
        }

        try:
            upsert(feedbackResponseTabla, payload, keys=["feedback_form_id", "practica_id"])
            update(feedbackFormsTabla,
                {
                    "practica_id": practica_id,
                    "estado": "Completado",
                    "fecha_respuesta": "now()"
                },
                {"practica_id": practica_id, "tipo_form": tipo_form})

            st.success("✅ ¡Gracias! Tu respuesta ha sido enviada correctamente.")
            st.balloons()  # Un toque de UX extra
        except Exception as e:
            st.error(f"Hubo un error al guardar: {e}")