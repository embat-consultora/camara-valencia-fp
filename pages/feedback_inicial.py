import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, feedbackFormsTabla, forms

st.set_page_config(page_title="Feedback Inicial", page_icon="📨")
#http://localhost:8501/feedback_inicial?token=2a6aa3a62d6a47b1868793f78f6f1ce9&tipo=feedback_inicial
# --- 1. Lógica de Parámetros y Seguridad ---
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token or not tipo_form or tipo_form != forms[0]:
    st.error("⚠️ Acceso no válido o link incorrecto.")
    st.stop()

feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o es incorrecto.")
    st.stop()

# Extracción de datos
practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]

st.title("Formulario de seguimiento – Primera semana")

# --- 2. EL FORMULARIO (Evita recargas constantes) ---
with st.form("main_feedback_form"):
    st.subheader("Datos generales")
    col1, col2 = st.columns(2) # Opcional: Para que no ocupe tanto espacio vertical
    with col1:
        st.text_input("Empresa", value=feedback["empresa"], disabled=True)
        st.text_input("Alumno", value=feedback["alumno"], disabled=True)
    with col2:
        st.text_input("Fecha de inicio", value=feedback["fecha_inicio"], disabled=True)
        st.text_input("Ciclo Formativo", value=feedback["ciclo"], disabled=True)
    
    st.text_input("Área / Departamento", value=feedback["area"], disabled=True)

    st.divider()

    st.subheader("Inicio y acogida")
    acogida = st.slider("Me sentí bien recibido/a", 1, 5, 3)
    funciones = st.slider("Me explicaron mis funciones", 1, 5, 3)
    dudas = st.slider("Sé a quién acudir si tengo dudas", 1, 5, 3)
    comodidad = st.slider("Me siento cómodo/a en el entorno de trabajo", 1, 5, 3)
    mejor = st.text_area("¿Qué fue lo mejor de tu primera semana?")

    st.subheader("Expectativas")
    alineado = st.radio("¿La formación cumple tus expectativas?", ["Sí", "Parcialmente", "No"], horizontal=True)
    aprender = st.text_area("¿Qué te gustaría aprender?")

    st.subheader("Primeras alertas")
    alertas = st.radio("¿Has tenido alguna dificultad?", ["No", "Sí"], horizontal=True)
    detalle_alerta = st.text_area("Si respondiste sí, explica:")

    # Botón de envío
    submit = st.form_submit_button("Enviar Formulario")

# --- 3. LÓGICA POST-SUBMIT ---
if submit:
    # Validación manual al intentar enviar
    errores = []
    if not mejor.strip(): errores.append("Por favor, cuéntanos qué fue lo mejor de tu semana.")
    if alertas == "Sí" and not detalle_alerta.strip(): errores.append("Has marcado que tienes dificultades, por favor descríbelas.")

    if errores:
        for error in errores:
            st.warning(error)
    else:
        with st.spinner("⏳ Enviando formulario, por favor espera..."):
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

            # Ejecución de DB
            res = upsert(feedbackResponseTabla, payload, keys=["feedback_form_id", "practica_id"])
            update(feedbackFormsTabla,
                {
                    "practica_id": practica_id,
                    "estado": "Completado",
                    "fecha_respuesta": "now()"
                },
                {"practica_id": practica_id, "tipo_form": tipo_form})
            
            # Verificación de respuesta
            if (isinstance(res, dict) and res.get("status_code", 200) >= 400) or (hasattr(res, "error") and res.error):
                st.error("Ocurrió un error al enviar. Por favor, inténtalo de nuevo.")
            else:
                st.success("✅ ¡Gracias! Tu respuesta ha sido enviada.")
                st.balloons()