import streamlit as st
import graphviz

def mostrar_fases(fasesList, fase2col, estados: dict | None):
    dot = graphviz.Digraph()
    dot.attr(rankdir="LR")  # horizontal

    if not estados:  # 🚨 caso sin datos
        for fase in fasesList:
            dot.node(fase, fase, style="filled", fillcolor="lightgrey", shape="box")
        for i in range(len(fasesList)-1):
            dot.edge(fasesList[i], fasesList[i+1])
        st.graphviz_chart(dot)
        return

    # --- caso normal ---
    fases_completadas = []
    for fase in fasesList:
        col = fase2col[fase]
        if estados.get(col):  # si tiene fecha
            fases_completadas.append(fase)

    # La siguiente fase pendiente (primera sin fecha después de las verdes)
    siguiente = None
    for fase in fasesList:
        if fase not in fases_completadas:
            siguiente = fase
            break

    # Crear nodos con colores
    for fase in fasesList:
        if fase in fases_completadas:
            dot.node(fase, fase, style="filled", fillcolor="lightgreen", shape="box")
        elif fase == siguiente:
            dot.node(fase, fase, style="filled", fillcolor="yellow", shape="box")
        else:
            dot.node(fase, fase, style="filled", fillcolor="mistyrose", shape="box")

    # Conectar nodos en orden
    for i in range(len(fasesList)-1):
        dot.edge(fasesList[i], fasesList[i+1])

    st.graphviz_chart(dot)