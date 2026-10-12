import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, feedbackFormsTabla, formsTutorEmpresa

st.set_page_config(page_title="Feedback Inicial Tutor", page_icon="📨")
#http://localhost:8501/feedback_inicial_tutor?token=TOKEN&tipo=feedback_inicial_tutor
# --- 1. Lógica de Parámetros y Seguridad ---
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token or not tipo_form or tipo_form != formsTutorEmpresa[0]:
    st.error("⚠️ Acceso no válido o link incorrecto.")
    st.stop()

feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o es incorrecto.")
    st.stop()

# Extracción de datos
practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]

st.title("Feedback inicial del tutor de empresa")

# --- 2. EL FORMULARIO ---
with st.form("feedback_inicial_tutor_form"):
    # 1. Datos generales
    st.subheader("Datos generales del tutor/a de prácticas en la empresa")
    col1, col2 = st.columns(2)
    with col1:
        nombre_tutor = st.text_input("Nombre y Apellidos")
        st.text_input("Empresa", value=feedback["empresa"], disabled=True)
    with col2:
        dni_tutor = st.text_input("DNI")
        st.text_input("Alumno asignado", value=feedback["alumno"], disabled=True)

    st.divider()

    # 2. Onboarding e integración
    st.subheader("Onboarding e integración")
    st.write("Escala 1–5 (Muy en desacuerdo → Muy de acuerdo)")
    presentado = st.slider("El alumno/a fue correctamente presentado al equipo", 1, 5, 3)
    funciones = st.slider("Tiene claras sus funciones iniciales", 1, 5, 3)
    normas = st.slider("Comprende las normas básicas de la empresa", 1, 5, 3)
    adaptacion = st.slider("Se adaptó adecuadamente al entorno de trabajo", 1, 5, 3)

    # 3. Actitud y predisposición
    st.subheader("Actitud y predisposición")
    interes = st.slider("Muestra interés por aprender", 1, 5, 3)
    actitud = st.slider("Tiene buena actitud frente al trabajo", 1, 5, 3)
    puntualidad = st.slider("Es puntual y responsable", 1, 5, 3)
    acepta_feedback = st.slider("Acepta indicaciones y feedback", 1, 5, 3)

    # 4. Primer ajuste
    st.subheader("Primer ajuste")
    nivel_adecuado = st.radio("¿El nivel inicial del alumno/a es adecuado para las tareas asignadas?", ["Sí", "Parcialmente", "No"], horizontal=True)
    ajustar = st.text_area("¿Hay algo que considere importante ajustar o reforzar en esta etapa inicial?")

    # 5. Acompañamiento
    st.subheader("Acompañamiento")
    herramientas = st.radio("¿Consideras que cuentas con las herramientas necesarias para acompañar al alumno/a?", ["Sí", "No"], horizontal=True)
    detalle_herramientas = st.text_area("Si respondiste no, cuéntanos por qué:")
    apoyo_centro = st.radio("¿Necesita apoyo adicional del centro educativo?", ["No", "Sí"], horizontal=True)
    detalle_apoyo = st.text_area("Si respondiste sí, especifica:")

    # Botón de envío
    submit = st.form_submit_button("Enviar Formulario")

# --- 3. LÓGICA POST-SUBMIT ---
if submit:
    errores = []
    if not nombre_tutor.strip(): errores.append("Por favor, indica tu nombre y apellidos.")
    if not dni_tutor.strip(): errores.append("Por favor, indica tu DNI.")
    if herramientas == "No" and not detalle_herramientas.strip(): errores.append("Has marcado que no cuentas con las herramientas necesarias, por favor explica por qué.")
    if apoyo_centro == "Sí" and not detalle_apoyo.strip(): errores.append("Has marcado que necesitas apoyo del centro, por favor especifica.")

    if errores:
        for error in errores:
            st.warning(error)
    else:
        with st.spinner("⏳ Enviando formulario, por favor espera..."):
            respuestas_json = {
                "tipo": tipo_form,
                "datos_tutor": {
                    "nombre": nombre_tutor,
                    "dni": dni_tutor
                },
                "onboarding": {
                    "presentado": presentado,
                    "funciones": funciones,
                    "normas": normas,
                    "adaptacion": adaptacion
                },
                "actitud": {
                    "interes": interes,
                    "actitud": actitud,
                    "puntualidad": puntualidad,
                    "acepta_feedback": acepta_feedback
                },
                "primer_ajuste": {
                    "nivel_adecuado": nivel_adecuado,
                    "ajustar": ajustar
                },
                "acompanamiento": {
                    "herramientas": herramientas,
                    "detalle_herramientas": detalle_herramientas,
                    "apoyo_centro": apoyo_centro,
                    "detalle_apoyo": detalle_apoyo
                }
            }

            payload = {
                "feedback_form_id": feedback_form_id,
                "practica_id": practica_id,
                "respuestas_json": respuestas_json
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

                st.success("✅ ¡Gracias! Tu respuesta ha sido enviada.")
                st.balloons()
            except Exception as e:
                st.error(f"Hubo un error al guardar: {e}")
