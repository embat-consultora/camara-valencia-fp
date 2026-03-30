import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, forms, feedbackFormsTabla

st.set_page_config(page_title="Feedback Adaptación", page_icon="📨")

# --- Lógica de Validación (Fuera del form para no procesar accesos inválidos) ---
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token or not tipo_form or tipo_form != forms[1]:
    st.error("⚠️ Acceso no válido o link incorrecto.")
    st.stop()

feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o es incorrecto.")
    st.stop()

practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]

st.title("Feedback de adaptación")

# --- FORMULARIO PRINCIPAL ---
# Usamos clear_on_submit=False para que el usuario vea su confirmación al final
with st.form("feedback_form"):
    st.subheader("Datos generales")
    st.text_input("Empresa", value=feedback["empresa"], disabled=True)
    st.text_input("Alumno", value=feedback["alumno"], disabled=True)

    # 1. Adaptación al puesto
    st.subheader("Adaptación al puesto")
    tareas = st.slider("Entiendo bien mis tareas", 1, 5, 3)
    valor = st.slider("Siento que estoy aportando valor", 1, 5, 3)
    ritmo = st.slider("El ritmo de trabajo es adecuado", 1, 5, 3)
    integracion = st.slider("Me siento integrado/a al equipo", 1, 5, 3)

    # 2. Aprendizaje
    st.subheader("Aprendizaje")
    nivel_aprendizaje = st.select_slider(
        "¿Estás aprendiendo cosas relacionadas con tu especialidad?", 
        options=["Nada", "Poco", "Bastante", "Mucho"], value="Bastante"
    )
    complemento = st.slider("Lo que hago complementa lo aprendido en el centro", 1, 5, 3)
    feedback_recibido = st.slider("Recibo feedback sobre mi trabajo", 1, 5, 3)
    que_aprendio = st.text_area("¿Qué aprendiste hasta ahora que no sabías antes?")

    # 3. Acompañamiento
    st.subheader("Acompañamiento")
    tutor_claro = st.radio("Tengo un tutor/a o referente claro en la empresa", ["Sí", "No"])
    acompanado = st.slider("Me siento acompañado/a en el proceso", 1, 5, 3)

    # 4. Satisfacción
    st.subheader("Satisfacción general")
    experiencia_global = st.slider("Evaluación de tu experiencia hasta ahora", 1, 10, 7)
    mejoras = st.text_area("¿Qué mejorarías de la experiencia de la formación de empresa?")

    # Botón de envío específico del formulario
    submit_button = st.form_submit_button("Enviar")

# --- PROCESAMIENTO POST-ENVÍO ---
if submit_button:
    with st.spinner("Guardando tu respuesta..."):
        respuestas_json = {
            "tipo": tipo_form,
            "puntuacion_global": experiencia_global,
            "adaptacion": {"tareas": tareas, "valor": valor, "ritmo": ritmo, "integracion": integracion},
            "aprendizaje": {
                "nivel": nivel_aprendizaje, 
                "complemento": complemento, 
                "feedback": feedback_recibido,
                "detalle": que_aprendio
            },
            "acompanamiento": {"tutor_claro": tutor_claro, "acompanado": acompanado},
            "mejoras": mejoras
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
            st.balloons() # Un toque de UX extra
        except Exception as e:
            st.error(f"Hubo un error al guardar: {e}")