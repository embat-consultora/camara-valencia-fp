import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, formsTutorEmpresa, feedbackFormsTabla

st.set_page_config(page_title="Feedback Adaptación Tutor", page_icon="📨")

# --- Lógica de Validación (Fuera del form para no procesar accesos inválidos) ---
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token or not tipo_form or tipo_form != formsTutorEmpresa[1]:
    st.error("⚠️ Acceso no válido o link incorrecto.")
    st.stop()

feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o es incorrecto.")
    st.stop()

practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]

st.title("Feedback de adaptación del tutor")

# --- FORMULARIO PRINCIPAL ---
with st.form("feedback_adaptacion_tutor_form"):
    st.subheader("Datos generales")
    st.text_input("Empresa", value=feedback["empresa"], disabled=True)
    st.text_input("Alumno", value=feedback["alumno"], disabled=True)

    # 1. Adaptación al puesto
    st.subheader("Adaptación al puesto")
    tareas = st.slider("Comprende sus tareas y responsabilidades", 1, 5, 3)
    indicaciones = st.slider("Ejecuta correctamente las indicaciones recibidas", 1, 5, 3)
    integracion = st.slider("Se integra bien al equipo", 1, 5, 3)
    ritmo = st.slider("El ritmo de aprendizaje es adecuado", 1, 5, 3)

    # 2. Desempeño general
    st.subheader("Desempeño general")
    calidad = st.slider("Calidad del trabajo realizado", 1, 5, 3)
    autonomia = st.slider("Autonomía progresiva", 1, 5, 3)
    organizacion = st.slider("Organización del trabajo", 1, 5, 3)
    detalle = st.slider("Atención al detalle", 1, 5, 3)

    # 3. Aprendizaje y evolución
    st.subheader("Aprendizaje y evolución")
    evolucion = st.select_slider(
        "¿Ha mostrado evolución desde el inicio?",
        options=["Ninguna", "Poca", "Bastante", "Mucha"], value="Bastante"
    )
    progreso = st.text_area("¿En qué aspectos nota mayor progreso?")

    # 4. Acompañamiento y feedback
    st.subheader("Acompañamiento y feedback")
    feedback_regular = st.slider("El alumno/a recibe feedback de forma regular", 1, 5, 3)
    correcciones = st.slider("Responde positivamente a las correcciones", 1, 5, 3)

    # 5. Evaluación general
    st.subheader("Evaluación general")
    puntuacion_global = st.slider("En una escala del 1 al 10, ¿cómo evaluaría el desempeño hasta ahora?", 1, 10, 7)
    volveria = st.radio("¿Volvería a recibir a este alumno/a en prácticas?", ["Sí", "No", "Aún no lo sé"], horizontal=True)
    punto_atencion = st.text_area("¿Hay algún punto de atención que deberíamos conocer desde el centro? (opcional)")

    # Botón de envío específico del formulario
    submit_button = st.form_submit_button("Enviar")

# --- PROCESAMIENTO POST-ENVÍO ---
if submit_button:
    with st.spinner("Guardando tu respuesta..."):
        respuestas_json = {
            "tipo": tipo_form,
            "puntuacion_global": puntuacion_global,
            "adaptacion": {"tareas": tareas, "indicaciones": indicaciones, "integracion": integracion, "ritmo": ritmo},
            "desempeno": {"calidad": calidad, "autonomia": autonomia, "organizacion": organizacion, "detalle": detalle},
            "aprendizaje": {"evolucion": evolucion, "progreso": progreso},
            "acompanamiento": {"feedback_regular": feedback_regular, "correcciones": correcciones},
            "evaluacion_general": {"volveria": volveria, "punto_atencion": punto_atencion}
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

            st.success("✅ ¡Gracias! Tu respuesta ha sido enviada correctamente.")
            st.balloons()
        except Exception as e:
            st.error(f"Hubo un error al guardar: {e}")
