import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, forms,feedbackFormsTabla
st.set_page_config(page_title="Feedback Seguimiento", page_icon="📨")
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")
if not token:
    st.error("Acceso no válido")
    st.stop()
if not tipo_form:
    st.error("⚠️ Error de acceso. El link es incorrecto.")
    st.stop()

if tipo_form != forms[2]:
    st.error(f"❌ Error de acceso. El link es incorrecto.")
    st.stop()
feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o no corresponde a este formulario.")
    st.stop()

st.title("Seguimiento breve")
practica_id = feedback["practica_id"]
# Preguntas Escala 1-5
motivacion = st.slider("Me siento motivado/a", 1, 5, 3)
novedad = st.slider("Estoy aprendiendo cosas nuevas", 1, 5, 3)
carga = st.slider("La carga de tareas es adecuada", 1, 5, 3)
comodidad = st.slider("Me siento cómodo/a en la empresa", 1, 5, 3)

continuar = st.radio("¿Te gustaría continuar en esta empresa?", ["Sí", "No", "No lo sé"])
comentarios = st.text_area("¿Algo que te preocupe o quieras comentar?")

if st.button("Enviar"):
    respuestas_json = {
        "tipo": tipo_form,
        "metricas": {"motivacion": motivacion, "aprendizaje": novedad, "carga": carga, "comodidad": comodidad},
        "continuidad": continuar,
        "comentarios": comentarios
    }
    payload = {"feedback_form_id": feedback["feedback_form_id"], "practica_id": practica_id, "respuestas_json": respuestas_json}
    upsert(feedbackResponseTabla, payload, keys=["feedback_form_id", "practica_id"])
    update(feedbackFormsTabla,
            {
                "practica_id": practica_id,
                "estado": "Completado",
                "fecha_respuesta": "now()"
            },
            {"practica_id": practica_id, "tipo_form": tipo_form})
    st.success("¡Gracias! Tu respuesta ha sido enviada.")