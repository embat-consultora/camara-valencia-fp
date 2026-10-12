import streamlit as st
from modules.data_base import getPracticaByToken, upsert, update
from variables import feedbackResponseTabla, formsTutorEmpresa, feedbackFormsTabla

st.set_page_config(page_title="Feedback Cierre Tutor", page_icon="📨")

# --- Lógica de Validación (Fuera del form para no procesar accesos inválidos) ---
token = st.query_params.get("token")
tipo_form = st.query_params.get("tipo")

if not token or not tipo_form or tipo_form != formsTutorEmpresa[2]:
    st.error("⚠️ Acceso no válido o link incorrecto.")
    st.stop()

feedback = getPracticaByToken(token, tipo_form)
if feedback is None:
    st.error("🚫 Acceso no válido: El token ha expirado o es incorrecto.")
    st.stop()

practica_id = feedback["practica_id"]
feedback_form_id = feedback["feedback_form_id"]

st.title("Cierre y balance final del tutor")

# --- FORMULARIO PRINCIPAL ---
with st.form("feedback_cierre_tutor_form"):
    st.subheader("Datos generales")
    st.text_input("Empresa", value=feedback["empresa"], disabled=True)
    st.text_input("Alumno", value=feedback["alumno"], disabled=True)

    # 1. Evaluación global
    st.subheader("Evaluación global")
    positiva = st.slider("La experiencia de prácticas fue positiva", 1, 5, 3)
    aporto_valor = st.slider("El alumno/a aportó valor al equipo", 1, 5, 3)
    acompanamiento_centro = st.slider("El acompañamiento del centro fue adecuado", 1, 5, 3)
    alineado = st.slider("El programa de FP Dual está bien alineado con la realidad empresarial", 1, 5, 3)

    # 2. Desarrollo de competencias
    st.subheader("Desarrollo de competencias (transversales)")
    c_resp = st.slider("Responsabilidad y compromiso", 1, 5, 3)
    c_equipo = st.slider("Trabajo en equipo", 1, 5, 3)
    c_com = st.slider("Comunicación", 1, 5, 3)
    c_auto = st.slider("Autonomía", 1, 5, 3)
    c_aprendizaje = st.slider("Capacidad de aprendizaje", 1, 5, 3)
    c_adaptacion = st.slider("Adaptación al entorno laboral", 1, 5, 3)

    # 3. Impacto en la empresa
    st.subheader("Impacto en la empresa")
    nivel_final = st.radio("El alumno/a alcanzó un nivel acorde al final del proceso", ["Sí", "Parcialmente", "No"], horizontal=True)
    tipo_tareas = st.radio("¿Qué tipo de tareas pudo asumir al final?", ["Básicas", "Operativas con supervisión", "Operativas con autonomía"], horizontal=True)

    # 4. Empleabilidad y proyección
    st.subheader("Empleabilidad y proyección")
    incorporacion = st.radio("¿Consideraría al alumno/a para una futura incorporación?", ["Sí", "No", "Tal vez"], horizontal=True)
    condiciones = st.radio("¿En qué condiciones?", ["Prácticas extendidas", "Contrato", "Otra modalidad"], horizontal=True)

    # 5. Cierre cualitativo
    st.subheader("Cierre cualitativo")
    fortalezas = st.text_area("¿Cuáles fueron las principales fortalezas del alumno/a?")
    a_desarrollar = st.text_area("¿Qué aspectos debería seguir desarrollando?")
    mejora_fp = st.text_area("¿Qué mejorarías del programa de FP Dual desde la mirada empresa?")

    # Botón de envío específico del formulario
    submit_button = st.form_submit_button("Enviar")

# --- PROCESAMIENTO POST-ENVÍO ---
if submit_button:
    with st.spinner("Guardando tu balance final..."):
        empleabilidad = {"incorporacion": incorporacion}
        if incorporacion != "No":
            empleabilidad["condiciones"] = condiciones

        respuestas_json = {
            "tipo": tipo_form,
            "evaluacion_global": {"positiva": positiva, "aporto_valor": aporto_valor, "acompanamiento_centro": acompanamiento_centro, "alineado": alineado},
            "competencias": {"compromiso": c_resp, "equipo": c_equipo, "comunicacion": c_com, "autonomia": c_auto, "aprendizaje": c_aprendizaje, "adaptacion": c_adaptacion},
            "impacto": {"nivel_final": nivel_final, "tipo_tareas": tipo_tareas},
            "empleabilidad": empleabilidad,
            "cualitativo": {"fortalezas": fortalezas, "a_desarrollar": a_desarrollar, "mejora_fp": mejora_fp}
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

            st.success("✅ ¡Gracias por tu tiempo y compromiso! Tu respuesta ha sido enviada correctamente.")
            st.balloons()
        except Exception as e:
            st.error(f"Hubo un error al guardar: {e}")
