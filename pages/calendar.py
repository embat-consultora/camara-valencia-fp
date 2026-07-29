import streamlit as st
import datetime
import calendar
import io
import matplotlib.pyplot as plt
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Calendario de Formaciones", layout="wide")

# 1. Base de datos de festivos fijos perpetuos (Mapeados por tupla: (mes, día))
# Esto permite que funcione automáticamente para 2026, 2027, 2030, etc.
FESTIVOS_FIJOS = {
    (1, 1): "Año Nuevo",
    (1, 6): "Epifanía del Señor",
    (3, 19): "San José",
    (5, 1): "Fiesta del Trabajo",
    (6, 24): "San Juan",
    (8, 15): "Asunción de la Virgen",
    (10, 9): "Día de la Comunitat Valenciana",
    (10, 12): "Fiesta Nacional de España",
    (12, 8): "Inmaculada Concepción",
    (12, 25): "Navidad"
}

# NOTA: Los festivos variables (como Viernes Santo o Lunes de Pascua) cambian año a año.
# Para evitar añadir librerías pesadas como 'holidays', calculamos las fechas exactas de la Pascua 
# de forma matemática usando el algoritmo de Gauss (válido hasta el año 2099).
def obtener_festivos_variables(year):
    # Algoritmo de Gauss para calcular el Domingo de Resurrección
    a = year % 19
    b = year % 4
    c = year % 7
    d = (19 * a + 24) % 30
    e = (2 * b + 4 * c + 6 * d + 5) % 7
    dias = 22 + d + e
    
    if dias > 31:
        mes_pascua = 4
        dia_pascua = dias - 31
    else:
        mes_pascua = 3
        dia_pascua = dias
        
    domingo_resurreccion = datetime.date(year, mes_pascua, dia_pascua)
    
    # Restamos y sumamos días relativos para Viernes Santo y Lunes de Pascua
    viernes_santo = domingo_resurreccion - datetime.timedelta(days=2)
    lunes_pascua = domingo_resurreccion + datetime.timedelta(days=1)
    
    return {
        viernes_santo: "Viernes Santo",
        lunes_pascua: "Lunes de Pascua"
    }

MESES_ES = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL", 5: "MAYO", 6: "JUNIO",
    7: "JULIO", 8: "AGOSTO", 9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}

if "dias_no_laborables" not in st.session_state:
    st.session_state.dias_no_laborables = set()

# Rango automático: hoy y 90 días después (independientemente del año actual)
hoy = datetime.date.today()
noventa_dias_despues = hoy + datetime.timedelta(days=90)

st.title("📅 Configuración del Calendario de Formaciones")

# --- PANEL DE CONTROL ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Rango y Horarios")
    params = st.query_params
    
    fecha_inicio = st.date_input("Fecha de Inicio", value=hoy)
    fecha_fin = st.date_input("Fecha de Fin", value=noventa_dias_despues)
    
    val_horas = float(params.get("horas")) if "horas" in params else 7.0
    horas_estandar = st.number_input("Horas por día (Lunes a Jueves)", value=val_horas, step=0.5)
    
    viernes_diferente = st.checkbox("¿El horario del Viernes es diferente?")
    if viernes_diferente:
        horas_viernes = st.number_input("Horas los Viernes", value=max(0.0, horas_estandar - 1.0), step=0.5)
    else:
        horas_viernes = horas_estandar

with col2:
    st.subheader("🚫 Excepciones / Días No Laborables")
    nuevo_dia = st.date_input("Seleccionar fecha festiva o puente", value=fecha_inicio)
    if st.button("Añadir Día No Laborable"):
        st.session_state.dias_no_laborables.add(nuevo_dia)
    
    if st.session_state.dias_no_laborables:
        st.write("**Días excluidos:**")
        dias_a_eliminar = []
        for dia in sorted(st.session_state.dias_no_laborables):
            cd1, cd2 = st.columns([3, 1])
            cd1.write(f"• {dia.strftime('%d/%m/%Y')}")
            if cd2.button("🗑️", key=f"del_{dia}"):
                dias_a_eliminar.append(dia)
        for dia in dias_a_eliminar:
            st.session_state.dias_no_laborables.remove(dia)
            st.rerun()

st.markdown("---")

# --- PROCESAMIENTO Y RENDERIZADO EN PANTALLA PRINCIPAL ---
if fecha_inicio > fecha_fin:
    st.error("Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
else:
    start_month, start_year = fecha_inicio.month, fecha_inicio.year
    end_month, end_year = fecha_fin.month, fecha_fin.year
    
    meses_lista = []
    current_year, current_month = start_year, start_month
    while (current_year, current_month) <= (end_year, end_month):
        meses_lista.append((current_year, current_month))
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

    st.markdown("### 📄 Vista Previa del Calendario")
    
    cal_cols = st.columns(2)
    total_horas_periodo = 0.0

    # Dibujamos las tablas HTML interactivas en la página principal
    for idx, (yr, msh) in enumerate(meses_lista):
        # Generar los festivos variables específicos del año que estamos iterando
        festivos_variables_año = obtener_festivos_variables(yr)
        
        with cal_cols[idx % 2]:
            st.markdown(f"##### 📅 {MESES_ES[msh]} - {yr}")
            
            cal_obj = calendar.Calendar(firstweekday=0)
            mes_matriz = cal_obj.monthdayscalendar(yr, msh)
            
            dias_laborables_normales = 0
            dias_viernes = 0
            
            tabla_html = "<table style='width:100%; text-align:center; border-collapse:collapse; font-size:14px;'>"
            tabla_html += "<tr style='background-color:#f3f4f6;'><th>L</th><th>M</th><th>X</th><th>J</th><th>V</th><th style='color:red;'>S</th><th style='color:red;'>D</th></tr>"
            
            for semana in mes_matriz:
                tabla_html += "<tr>"
                for dia_idx, dia in enumerate(semana):
                    if dia == 0:
                        tabla_html += "<td style='background-color:#f9fafb;'></td>"
                    else:
                        fecha_actual = datetime.date(yr, msh, dia)
                        tupla_mes_dia = (msh, dia)
                        estilo = ""
                        
                        if fecha_actual < fecha_inicio or fecha_actual > fecha_fin:
                            estilo = "background-color: #f3f4f6; color: #9ca3af;"
                        elif dia_idx >= 5:
                            estilo = "background-color: #a5b4fc; font-weight: bold;"
                        # Verificación dinámica de festivos fijos y variables del año en curso
                        elif tupla_mes_dia in FESTIVOS_FIJOS or fecha_actual in festivos_variables_año:
                            estilo = "background-color: #fca5a5;"
                        elif fecha_actual in st.session_state.dias_no_laborables:
                            estilo = "background-color: #fcd34d;"
                        else:
                            if dia_idx == 4: # Viernes
                                estilo = "background-color: #93c5fd; font-weight: bold;"
                                dias_viernes += 1
                            else: # Lunes a Jueves
                                estilo = "background-color: #c7d2fe; font-weight: bold;"
                                dias_laborables_normales += 1
                            
                        tabla_html += f"<td style='padding:8px; border:1px solid #e5e7eb; {estilo}'>{dia}</td>"
                tabla_html += "</tr>"
            tabla_html += "</table>"
            
            st.markdown(tabla_html, unsafe_allow_html=True)
            
            # Cómputo de horas del mes actual
            horas_totales_mes = (dias_laborables_normales * horas_estandar) + (dias_viernes * horas_viernes)
            total_horas_periodo += horas_totales_mes
            
            st.caption(f"**{dias_laborables_normales}** días L-J ({horas_estandar}h) + **{dias_viernes}** viernes ({horas_viernes}h) = **{horas_totales_mes:.1f} horas**")

    st.markdown("---")
    
    # --- RESUMEN FINAL Y LEYENDA ---
    st.subheader(f"📊 TOTAL PERIODO DE FORMACIONES: {total_horas_periodo:.2f} HORAS")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.write(f"**Fecha de inicio:** {fecha_inicio.strftime('%d/%m/%Y')}")
        st.write(f"**Fecha de fin:** {fecha_fin.strftime('%d/%m/%Y')}")
    
    with col_r2:
        st.markdown("""
        <div style='font-size:12px; line-height:20px;'>
            <span style='background-color:#c7d2fe; padding:2px 8px; border-radius:4px; margin-right:5px;'></span> Lunes a Jueves
            <span style='background-color:#93c5fd; padding:2px 8px; border-radius:4px; margin-right:5px;'></span> Viernes Diferenciado
            <span style='background-color:#a5b4fc; padding:2px 8px; border-radius:4px; margin-right:5px;'></span> Fin de semana
            <span style='background-color:#fca5a5; padding:2px 8px; border-radius:4px; margin-right:5px;'></span> Festivo Oficial
            <span style='background-color:#fcd34d; padding:2px 8px; border-radius:4px; margin-right:5px;'></span> No laborable (Usuario)
        </div>
        """, unsafe_allow_html=True)

    # --- GENERACIÓN DE IMAGEN MULTIAÑO ---
    def procesar_foto_calendario():
        num_meses = len(meses_lista)
        fig, axs = plt.subplots(nrows=(num_meses + 1) // 2, ncols=2, figsize=(14, 4.2 * ((num_meses + 1) // 2) + 1))
        axs = axs.flatten() if num_meses > 1 else [axs]
        
        img_total_horas = 0.0
        
        for idx, (yr, msh) in enumerate(meses_lista):
            festivos_variables_año = obtener_festivos_variables(yr)
            ax = axs[idx]
            ax.axis('off')
            
            cal_obj = calendar.Calendar(firstweekday=0)
            mes_matriz = cal_obj.monthdayscalendar(yr, msh)
            
            celdas_texto = []
            celdas_colores = []
            horas_mes = 0.0
            
            for semana in mes_matriz:
                fila_texto = []
                fila_colores = []
                for dia_idx, dia in enumerate(semana):
                    if dia == 0:
                        fila_texto.append("")
                        fila_colores.append("#ffffff")
                    else:
                        fecha_actual = datetime.date(yr, msh, dia)
                        tupla_mes_dia = (msh, dia)
                        fila_texto.append(str(dia))
                        
                        if fecha_actual < fecha_inicio or fecha_actual > fecha_fin:
                            fila_colores.append("#f3f4f6")
                        elif dia_idx >= 5:
                            fila_colores.append("#a5b4fc")
                        elif tupla_mes_dia in FESTIVOS_FIJOS or fecha_actual in festivos_variables_año:
                            fila_colores.append("#fca5a5")
                        elif fecha_actual in st.session_state.dias_no_laborables:
                            fila_colores.append("#fcd34d")
                        else:
                            if dia_idx == 4:
                                horas_mes += horas_viernes
                                img_total_horas += horas_viernes
                                fila_colores.append("#93c5fd")
                            else:
                                horas_mes += horas_estandar
                                img_total_horas += horas_estandar
                                fila_colores.append("#c7d2fe")
                                
                celdas_texto.append(fila_texto)
                celdas_colores.append(fila_colores)
            
            tabla = ax.table(cellText=celdas_texto, colLabels=['L', 'M', 'X', 'J', 'V', 'S', 'D'], loc='center', cellLoc='center')
            tabla.auto_set_font_size(False)
            tabla.set_fontsize(10)
            tabla.scale(1, 1.8)
            
            for (fila, columna), celda in tabla.get_celld().items():
                if fila > 0:
                    color_celda = celdas_colores[fila - 1][columna]
                    celda.set_facecolor(color_celda)
                else:
                    celda.set_facecolor("#f3f4f6")
            
            ax.set_title(f"{MESES_ES[msh]} {yr} \n (Total Mes: {horas_mes:.1f} h)", fontsize=12, fontweight='bold', color='#1e3a8a', pad=8)

        for j in range(num_meses, len(axs)):
            fig.delaxes(axs[j])
            
        info_encabezado = f"CALENDARIO DE FORMACIONES EN EMPRESA\nPeriodo: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}   |   Total Computado: {img_total_horas:.1f} Horas"
        fig.suptitle(info_encabezado, fontsize=13, fontweight='bold', y=0.98, bbox=dict(facecolor='#eff6ff', alpha=0.8, boxstyle='round,pad=0.5'))
        
        plt.tight_layout(rect=[0, 0, 1, 0.93])
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        return buf

    imagen_lista = procesar_foto_calendario()

    st.markdown("##")
    st.download_button(
        label="📥 Descargar Calendario como Imagen (PNG)",
        data=imagen_lista.getvalue(),
        file_name=f"Calendario_Formaciones_{fecha_inicio.strftime('%Y%m%d')}.png",
        mime="image/png",
        type="primary",
        use_container_width=True
    )