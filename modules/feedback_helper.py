import streamlit as st

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

    elif tipo == "feedback_inicial_tutor":
        vals = list(data["onboarding"].values()) + list(data["actitud"].values())
        score_final = round((sum(vals) / len(vals)), 1)
        titulo_display = "Inicial Tutor"

    elif tipo == "feedback_adaptacion_tutor":
        vals = list(data["adaptacion"].values()) + list(data["desempeno"].values()) + list(data["acompanamiento"].values())
        score_final = round((sum(vals) / len(vals)), 1)
        titulo_display = "Adaptación Tutor"

    elif tipo == "feedback_cierre_tutor":
        vals = list(data["evaluacion_global"].values()) + list(data["competencias"].values())
        score_final = round((sum(vals) / len(vals)), 1)
        titulo_display = "Cierre Tutor"
    else:
        titulo_display = titulo_default

    # 3. RENDERIZADO VISUAL
    with st.container(border=True):
        st.markdown(f"<h4 style='text-align:center; color:#555; margin-bottom:-10px;'>{titulo_display}</h4>", unsafe_allow_html=True)
        
        # Puntuación promedio (escala 0-5, mismos umbrales que antes)
        if score_final < 2:
            color_barra, color_texto, nivel = "#F7AB54", "#D9822B", "A mejorar"   # Naranja
        elif score_final < 3.5:
            color_barra, color_texto, nivel = "#FFE15C", "#B8960C", "Regular"     # Amarillo
        else:
            color_barra, color_texto, nivel = "#82D992", "#3A9E52", "Bueno"       # Verde
        porcentaje = max(0, min(score_final / 5 * 100, 100))
        st.markdown(f"""
            <div style="text-align:center; margin:14px 0 6px;">
                <span style="font-size:44px; font-weight:700; line-height:1; color:{color_texto};">{score_final:.1f}</span>
                <span style="font-size:16px; color:#999;"> / 5</span>
                <div style="font-size:12px; font-weight:600; color:{color_texto}; text-transform:uppercase; letter-spacing:1px; margin-top:4px;">{nivel}</div>
            </div>
            <div style="background:#EEE; height:10px; border-radius:5px; overflow:hidden; margin:0 4px 12px;">
                <div style="width:{porcentaje}%; height:100%; background:{color_barra}; border-radius:5px;"></div>
            </div>
        """, unsafe_allow_html=True)

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

        elif tipo == "feedback_inicial_tutor":
            draw_info("Nivel inicial", data["primer_ajuste"]["nivel_adecuado"],
                      subtext=f"Ajustar: {data['primer_ajuste']['ajustar']}",
                      color=color_ok if data["primer_ajuste"]["nivel_adecuado"] == "Sí" else color_bad, icon="🎯")
            draw_info("Herramientas", data["acompanamiento"]["herramientas"],
                      subtext=data["acompanamiento"]["detalle_herramientas"] if data["acompanamiento"]["herramientas"] == "No" else None,
                      color=color_ok if data["acompanamiento"]["herramientas"] == "Sí" else color_bad, icon="🧰")
            necesita_apoyo = data["acompanamiento"]["apoyo_centro"] == "Sí"
            draw_info("Apoyo del centro", data["acompanamiento"]["apoyo_centro"],
                      subtext=data["acompanamiento"]["detalle_apoyo"] if necesita_apoyo else None,
                      color=color_bad if necesita_apoyo else color_ok, icon="🚨")

        elif tipo == "feedback_adaptacion_tutor":
            draw_info("Evolución", data["aprendizaje"]["evolucion"],
                      subtext=f"Progreso: {data['aprendizaje']['progreso']}", icon="📈")
            draw_info("Desempeño", f"{data['puntuacion_global']}/10", icon="⭐")
            draw_info("Volvería a recibirlo", data["evaluacion_general"]["volveria"],
                      subtext=f"Atención: {data['evaluacion_general']['punto_atencion']}", icon="🔄")

        elif tipo == "feedback_cierre_tutor":
            draw_info("Nivel final", data["impacto"]["nivel_final"],
                      subtext=f"Tareas: {data['impacto']['tipo_tareas']}",
                      color=color_ok if data["impacto"]["nivel_final"] == "Sí" else color_bad, icon="🏁")
            draw_info("Incorporación", data["empleabilidad"]["incorporacion"],
                      subtext=f"Condiciones: {data['empleabilidad']['condiciones']}" if data["empleabilidad"].get("condiciones") else None, icon="💼")
            draw_info("Fortalezas", "",
                      subtext=data["cualitativo"]["fortalezas"], icon="💪")