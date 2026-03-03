import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
from PIL import Image

# --- 1. CONFIGURACION Y ESTILOS ---
st.set_page_config(page_title="Bio-Digital OS v6.0", layout="wide", initial_sidebar_state="expanded")

# Inyeccion de CSS con forzado de colores
st.markdown("""
    <style>
    /* FORZAR FONDO OSCURO EN TODA LA APP */
    .stApp {
        background-color: #0b0f19;
    }
    .main { 
        background-color: #0b0f19; 
        color: #e2e8f0; 
    }

    /* TITULOS: Blanco sobre fondo oscuro forzado */
    h1, h2, h3, h4, .stSubheader, [data-testid="stHeader"], .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { 
        color: #ffffff !important; 
        font-family: 'Arial', sans-serif;
        font-weight: 800 !important;
        margin-bottom: 10px;
    }

    /* SUBTITULOS O TITULOS SECUNDARIOS - Color Cyan para asegurar contraste */
    .stMarkdown h3 {
        color: #00ffcc !important;
    }

    /* CAJAS DE LOS KPIs */
    .stMetric { 
        background-color: #111827 !important; 
        border: 1px solid #1f2937; 
        border-left: 4px solid #00ffcc; 
    }
    
    /* Titulos internos de las cajas (Muestras, etc) */
    div[data-testid="stMetricLabel"] p { 
        color: #00ffcc !important; 
        font-weight: bold !important;
    }
    
    /* Numeros grandes */
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
    }

    /* TABLAS Y PESTAÑAS */
    .stTabs [data-baseweb="tab-list"] { background-color: #0b0f19; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    
    /* AJUSTE PARA EL HEADER DE STREAMLIT */
    header[data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
# Usamos un contenedor con fondo específico para el titulo
st.markdown("<div style='background-color:#111827; padding:20px; border-radius:10px; border:1px solid #1f2937;'>"
            "<h1 style='margin:0; color:white;'>🧬 BIO-DIGITAL OS <span style='color:#3b82f6; font-size:0.5em;'>v6.0 PRO</span></h1>"
            "</div>", unsafe_allow_html=True)

st.divider()

# --- PANEL LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103322.png", width=60)
    st.markdown("### PANEL DE CONTROL")
    genetica = st.button("🧬 Módulo Genética")
    vision = st.button("👁️ Módulo Visión 3D")
    seguridad = st.toggle("🛡️ Encriptación Cuántica")
    roi = st.button("💰 Módulo ROI")
    st.markdown("---")
    simular_alerta = st.toggle("🚨 FALLO DEL SISTEMA (LIMS)")

# --- KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("🧬 MUESTRAS", "12,450", delta="Prioridad 1" if simular_alerta else "+312 hoy")
k2.metric("⚡ CARGA CPU IA", "94.2%", delta="Sobrecarga" if simular_alerta else "-2.1%", delta_color="inverse")
k3.metric("🌡️ TEMP. GENERAL", "48.5°C" if simular_alerta else "21.5°C", delta="+27.0°C" if simular_alerta else "-0.2°C", delta_color="inverse")
k4.metric("🛡️ RED IOT", "100%" if seguridad else "82%", delta="Encriptado" if seguridad else "Riesgo Medio")

# --- GEMELO DIGITAL Y TRAZABILIDAD ---
c_left, c_right = st.columns(2)

with c_left:
    st.markdown("### 🌐 Gemelo Digital")
    tab1, tab2 = st.tabs(["🗺️ Plano Cenital", "🌋 Gráfico 3D"])
    with tab1:
        res = 60
        z_2d = np.random.uniform(20.5, 21.5, size=(res, res))
        if simular_alerta:
            for i in range(res):
                for j in range(res):
                    dist = np.sqrt((i-30)**2 + (j-45)**2)
                    if dist < 20: z_2d[i,j] = 50 - dist*1.5
        fig2 = go.Figure(data=go.Heatmap(z=z_2d, colorscale='Inferno' if simular_alerta else 'Viridis', opacity=0.4, zsmooth='best', showscale=False))
        nombre_img = "plano_isometrico.png"
        if os.path.exists(nombre_img):
            img = Image.open(nombre_img)
            fig2.add_layout_image(dict(source=img, xref="x", yref="y", x=0, y=res, sizex=res, sizey=res, sizing="stretch", opacity=0.7, layer="below"))
        fig2.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), margin=dict(l=0, r=0, b=0, t=0), height=350, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    with tab2:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        xG, yG = np.meshgrid(y, x)
        z_3 = np.sin(xG) * 0.1 + np.cos(yG) * 0.1 + 21
        if simular_alerta: z_3 += 30 * np.exp(-(xG**2 + yG**2) / 2)
        fig3 = go.Figure(data=[go.Surface(z=z_3, colorscale='Inferno' if simular_alerta else 'Viridis')])
        fig3.update_layout(scene=dict(xaxis=dict(color="white"), yaxis=dict(color="white"), zaxis=dict(color="white")), margin=dict(l=0, r=0, b=0, t=0), height=350, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

with c_right:
    st.markdown("### ⛓️ Trazabilidad")
    fuentes, destinos, valores = ([0, 1, 1, 2, 2], [1, 2, 4, 4, 3], [100, 20, 80, 20, 0]) if simular_alerta else ([0, 1, 2, 3], [1, 2, 3, 5], [100, 95, 90, 85])
    fig_s = go.Figure(data=[go.Sankey(
        textfont = dict(color="white", size=12),
        node = dict(pad=15, thickness=20, label=["Recepción", "Extracción", "PCR", "Secuenciadores", "Emergencia", "IA"], color="blue"),
        link = dict(source=fuentes, target=destinos, value=valores, color="rgba(59, 130, 246, 0.4)")
    )])
    fig_s.update_layout(height=400, margin=dict(l=10, r=10, b=10, t=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_s, use_container_width=True)

st.divider()

# --- BASE DE DATOS ---
st.markdown("### ☁️ Cloud LIMS")
c_db1, c_db2 = st.columns([2, 1])

with c_db1:
    if st.button("🔄 Sincronizar Base de Datos"):
        try:
            url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv"
            df = pd.read_csv(url)
            st.success("Sincronización Exitosa")
            st.dataframe(df, use_container_width=True)
            with c_db2:
                st.markdown("#### Estabilidad Térmica")
                fig_t = px.line(y=np.random.normal(21, 0.5, 20), title="Sensor Local")
                fig_t.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
                st.plotly_chart(fig_t, use_container_width=True)
        except:
            st.error("Error de conexión")

# --- FINAL ---
st.divider()
c_bot, c_term = st.columns(2)
with c_bot:
    st.markdown("### 💬 IA Assistant")
    st.chat_input("Consulta...")
with c_term:
    st.markdown("### 🖥️ Terminal LIMS")
    st.code(">>> Monitorizando sensores...\n>>> Estado: Sistemas OK" if not simular_alerta else ">>> ALERTA: SOBRECALENTAMIENTO", language="bash")




