import streamlit as st
import plotly.graph_objects as go

def render_feedback_card(data, titulo_default="Feedback"):
    # 1. MANEJO DE SIN DATOS
    if not data:
        with st.container(border=True):
            st.markdown(f"<h4 style='text-align:center; color:#888;'>{titulo_default}</h4>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center; padding:40px 0; opacity:0.3;'><span style='font-size:40px;'>📊</span><br>Sin feedback</div>", unsafe_allow_html=True)
        return

    # 2. LÓGICA DE CÁLCULO Y TÍTULOS SEGÚN TIPO
    tipo = data.get("tipo", "")
    score_final = 0.0
    
    # Colores base
    color_ok = "#82D992"
    color_bad = "#F7AB54"

    if tipo == "feedback_inicial":
        # Escala 0-5
        puntos = 5 if data["expectativas"]["alineado"] == "Sí" else 0
        acogida_keys = ["dudas", "acogida", "comodidad", "funciones"]
        vals_acogida = [data["inicio_acogida"][k] for k in acogida_keys]
        for v in vals_acogida:
            puntos += 5 if v > 3 else (2.5 if v == 3 else 0)
        puntos += 5 if data["primeras_alertas"]["alertas"] == "No" else 0
        score_final = round(puntos / 6, 1)
        promedio_acogida = sum(vals_acogida) / len(vals_acogida)
        titulo_display = "Inicial"

    elif tipo == "feedback_adaptacion":
        vals = list(data["adaptacion"].values()) + [data["aprendizaje"]["complemento"], data["aprendizaje"]["feedback"]]
        score_final = round((sum(vals) / len(vals)), 1)
        titulo_display = "Adaptación"

    elif tipo == "feedback_seguimiento":
        vals = list(data["metricas"].values())
        score_final = round((sum(vals) / len(vals)), 1)
        titulo_display = "Seguimiento"

    elif tipo == "feedback_cierre":
        vals = list(data["evaluacion_global"].values()) + list(data["competencias"].values())
        score_final = round((sum(vals) / len(vals)), 1)
        titulo_display = "Cierre"
    else:
        titulo_display = titulo_default

    # 3. RENDERIZADO VISUAL
    with st.container(border=True):
        st.markdown(f"<h4 style='text-align:center; color:#555; margin-bottom:-10px;'>{titulo_display}</h4>", unsafe_allow_html=True)
        
        # Gauge Chart (AJUSTADO A ESCALA 0-5 Y NUEVOS UMBRALES)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score_final,
            number = {'font': {'size': 40}, 'valueformat': '.1f'},
            gauge = {
                'axis': {'range': [0, 5], 'tickvals': [0, 2, 3.5, 5]},
                'bar': {'color': "#444", 'thickness': 0.15},
                'steps': [
                    {'range': [0, 2], 'color': "#F7AB54"},    # Naranja
                    {'range': [2, 3.5], 'color': "#FFE15C"},  # Amarillo
                    {'range': [3.5, 5], 'color': "#82D992"}   # Verde
                ],
            }
        ))
        fig.update_layout(height=180, margin=dict(l=25, r=25, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # --- FUNCIÓN INTERNA DE FILAS (Mantenida) ---
        def draw_info(label, value, subtext=None, color="#333", icon=""):
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <span style="font-size: 13px; font-weight: bold;">{icon} {label}</span>
                    <span style="font-size: 13px; color: {color}; font-weight: bold;">{value}</span>
                </div>
            """, unsafe_allow_html=True)
            if subtext and subtext.strip():
                st.markdown(f"<div style='font-size: 11px; color: #666; font-style: italic; margin-bottom: 5px;'>{subtext}</div>", unsafe_allow_html=True)

        # --- SECCIONES SEGÚN TIPO (Mantenida) ---
        if tipo == "feedback_inicial":
            draw_info("Expectativas", data["expectativas"]["alineado"], 
                      subtext=f"Aprender: {data['expectativas']['aprender']}", 
                      color=color_ok if data["expectativas"]["alineado"] == "Sí" else color_bad, icon="🎯")
            draw_info("Promedio Acogida", f"{promedio_acogida}/5.0", 
                      subtext=f"Lo mejor: {data['inicio_acogida']['mejor']}", icon="🏠")
            hay_alerta = data["primeras_alertas"]["alertas"] == "Sí"
            draw_info("Alertas", data["primeras_alertas"]["alertas"], 
                      subtext=data["primeras_alertas"]["detalle_alerta"] if hay_alerta else None, 
                      color=color_bad if hay_alerta else color_ok, icon="🚨")

        elif tipo == "feedback_adaptacion":
            draw_info("Aprendizaje", data["aprendizaje"]["nivel"], 
                      subtext=f"Aprendió: {data['aprendizaje']['detalle']}", icon="📚")
            draw_info("Integración", f"{data['adaptacion']['integracion']}/5", icon="👥")
            draw_info("Tutor Claro", data["acompanamiento"]["tutor_claro"], 
                      subtext=f"Mejoras: {data['mejoras']}", icon="👤")

        elif tipo == "feedback_seguimiento":
            draw_info("Motivación", f"{data['metricas']['motivacion']}/5", icon="🔥")
            draw_info("Carga", f"{data['metricas']['carga']}/5", icon="⚖️")
            draw_info("Continuaría", data["continuidad"], 
                      subtext=f"Nota: {data['comentarios']}", icon="🔄")

        elif tipo == "feedback_cierre":
            draw_info("Global", f"{data['evaluacion_global']['positiva']}/5", 
                      subtext=f"Valioso: {data['cualitativo']['valioso']}", icon="⭐")
            draw_info("Empleabilidad", data["empleabilidad"]["preparado"], icon="💼")
            draw_info("Continuidad", data["empleabilidad"]["oferta_continuidad"], 
                      subtext=f"Consejo: {data['cualitativo']['consejo']}", icon="🚀")