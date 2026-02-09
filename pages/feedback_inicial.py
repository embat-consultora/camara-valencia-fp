import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, feedbackFormsTabla,forms

# -------------------------------
# Leer parámetros de URL
# -------------------------------
st.set_page_config(page_title="Feedback Inicial", page_icon="📨")
#http://localhost:8501/feedback_inicial?token=2a6aa3a62d6a47b1868793f78f6f1ce9&tipo=feedback_inicial
#http://localhost:8501/?token=1f064716d453483fb2c9941bd8ff0139&tipo=feedback_inicial
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token:
    st.error("Acceso no válido")
    st.stop()
if not tipo_form:
    st.error("⚠️ Error de acceso. El link es incorrecto.")
    st.stop()

if tipo_form != forms[0]:
    st.error(f"❌ Error de acceso. El link es incorrecto.")
    st.stop()
# -------------------------------
# Traer datos obligatorios desde la práctica
# -------------------------------
feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o no corresponde a este formulario.")
    st.stop()

# -------------------------------
# Precargar datos
# -------------------------------

ciclo = feedback["ciclo"]
area = feedback["area"]
fecha_inicio = feedback["fecha_inicio"]
empresa = feedback["empresa"]
alumno = feedback["alumno"]  # dict con {nombre, tutor, especialidad, ...}
practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]  # si lo tenés

st.title("Formulario de seguimiento – Primera semana")

# -------- FORMULARIO DIRECTO (sin st.form) --------

st.subheader("Datos generales")
st.write("Información básica de la formación en Empresa y el alumno, ya precargada.")
empresa_input = st.text_input("Empresa", value=empresa, disabled=True)
alumno_input = st.text_input("Alumno", value=alumno, disabled=True)
fecha_inicio_input = st.text_input("Fecha de inicio", value=fecha_inicio, disabled=True)
especialidad = st.text_input("Ciclo Formativo", value=ciclo, disabled=True)
area_input = st.text_input("Área / Departamento", value=area, disabled=True)

st.subheader("Inicio y acogida")
st.write("Valora cómo fue tu primer contacto con la empresa y tu integración inicial.")
acogida = st.slider("Me sentí bien recibido/a", 1, 5, 3)
funciones = st.slider("Me explicaron mis funciones", 1, 5, 3)
dudas = st.slider("Sé a quién acudir si tengo dudas", 1, 5, 3)
comodidad = st.slider("Me siento cómodo/a en el entorno de trabajo", 1, 5, 3)
mejor = st.text_area("¿Qué fue lo mejor de tu primera semana?")

st.subheader("Expectativas")
st.write("Reflexiona sobre si la formación cumple con tus expectativas y qué te gustaría aprender.")
alineado = st.radio("¿La formación cumple tus expectativas?", ["Sí", "Parcialmente", "No"])
aprender = st.text_area("¿Qué te gustaría aprender?")

st.subheader("Primeras alertas")
st.write("Indica si has tenido dificultades iniciales y describe si necesitas apoyo.")
alertas = st.radio("¿Has tenido alguna dificultad?", ["No", "Sí"])
detalle_alerta = ""
if alertas == "Sí":
    detalle_alerta = st.text_area("Si respondiste sí, explica:")

# -------------------------------
# Validación mínima antes de enviar
# -------------------------------
missing = []
if not mejor.strip(): missing.append("Lo mejor de la semana")
if alineado not in ["Sí", "Parcialmente", "No"]: missing.append("Expectativas")
if alertas == "Sí" and not detalle_alerta.strip(): missing.append("Detalle de alertas")

if missing:
    st.info("Completa los campos obligatorios: " + ", ".join(missing))

can_submit = len(missing) == 0
submit = st.button("Enviar", disabled=not can_submit)

# -------------------------------
# Guardar respuestas como JSON
# -------------------------------
with st.spinner("⏳ Enviando formulario, por favor espera..."):
    if submit:
        # Construir JSON de respuestas
        respuestas_json = {
            "tipo": tipo_form,
            "inicio_acogida": {
                "acogida": acogida,
                "funciones": funciones,
                "dudas": dudas,
                "comodidad": comodidad,
                "mejor": mejor
            },
            "expectativas": {
                "alineado": alineado,
                "aprender": aprender
            },
            "primeras_alertas": {
                "alertas": alertas,
                "detalle_alerta": detalle_alerta
            }
        }

        payload = {
            "feedback_form_id": feedback_form_id,
            "practica_id": practica_id,
            "respuestas_json": respuestas_json
        }

        res = upsert(feedbackResponseTabla, payload, keys=["feedback_form_id", "practica_id"])
        update(feedbackFormsTabla,
            {
                "practica_id": practica_id,
                "estado": "Completado",
                "fecha_respuesta": "now()"
            },
            {"practica_id": practica_id, "tipo_form": tipo_form})
        if isinstance(res, dict) and res.get("status_code", 200) >= 400:
            st.error(f"Ocurrió un error al enviar: {res.get('error')}")
        elif hasattr(res, "error") and res.error:  # si tu upsert retorna un objeto con error
            st.error(f"Ocurrió un error al enviar: {res.error}")
        else:
            st.success("¡Gracias! Tu respuesta ha sido enviada.")