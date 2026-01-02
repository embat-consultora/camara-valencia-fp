import streamlit as st
from modules.data_base import getPracticaByToken, upsert,update
from variables import feedbackResponseTabla, forms, feedbackFormsTabla

st.set_page_config(page_title="Feedback Cierre", page_icon="📨")

token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token:
    st.error("Acceso no válido")
    st.stop()
if not tipo_form:
    st.error("⚠️ Error de acceso. El link es incorrecto.")
    st.stop()

if tipo_form != forms[3]:
    st.error(f"❌ Error de acceso. El link es incorrecto.")
    st.stop()
# -------------------------------
# Traer datos obligatorios desde la práctica
# -------------------------------
feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o no corresponde a este formulario.")
    st.stop()
practica_id = feedback["practica_id"]
st.title("Cierre y balance final")

# 1. Evaluación Global
st.subheader("Evaluación global")
positiva = st.slider("La experiencia fue positiva", 1, 5, 3)
utilidad = st.slider("Aprendí habilidades útiles", 1, 5, 3)
acompanamiento_final = st.slider("Me sentí acompañado/a", 1, 5, 3)
recomendar = st.slider("Recomendaría esta empresa", 1, 5, 3)

# 2. Competencias
st.subheader("Desarrollo de competencias")
c_resp = st.slider("Responsabilidad y compromiso", 1, 5, 3)
c_equipo = st.slider("Trabajo en equipo", 1, 5, 3)
c_com = st.slider("Comunicación", 1, 5, 3)
c_auto = st.slider("Autonomía", 1, 5, 3)

# 3. Impacto y Empleabilidad
st.subheader("Impacto y Futuro")
preparado = st.radio("¿Te sientes más preparado/a para trabajar?", ["Sí", "Parcialmente", "No"])
orientacion = st.radio("¿Influyó en tu orientación profesional?", ["Me reafirmaron", "Me hicieron replantear", "No influyeron"])
continuidad = st.radio("¿Te ofrecieron continuidad?", ["Sí", "No", "Se conversó informalmente"])

# 4. Cualitativo
st.subheader("Cierre")
valioso = st.text_area("¿Qué fue lo más valioso?")
mejora_fp = st.text_area("¿Qué mejorarías del programa?")
consejo = st.text_area("¿Qué consejo le darías a un/a futuro/a alumno/a?")

if st.button("Enviar"):
    respuestas_json = {
        "tipo": tipo_form,
        "evaluacion_global": {"positiva": positiva, "utilidad": utilidad, "acompanamiento": acompanamiento_final, "recomendar": recomendar},
        "competencias": {"compromiso": c_resp, "equipo": c_equipo, "comunicacion": c_com, "autonomia": c_auto},
        "empleabilidad": {"preparado": preparado, "orientacion": orientacion, "oferta_continuidad": continuidad},
        "cualitativo": {"valioso": valioso, "mejora_fp": mejora_fp, "consejo": consejo}
    }
    payload = {"feedback_form_id": feedback["feedback_form_id"], "practica_id": feedback["practica_id"], "respuestas_json": respuestas_json}
    upsert(feedbackResponseTabla, payload, keys=["feedback_form_id", "practica_id"])
    update(feedbackFormsTabla,
            {
                "practica_id": practica_id,
                "estado": "Completado",
                "fecha_respuesta": "now()"
            },
            {"practica_id": practica_id, "tipo_form": tipo_form})
    st.balloons()
    st.success("¡Felicidades por terminar tus prácticas!")