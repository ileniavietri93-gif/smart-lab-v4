import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os
from PIL import Image

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(page_title="LIMS IA - CONTROL SYSTEM", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: INTERFAZ DE CRISTAL LÍQUIDO IA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    .stApp { background-color: #030508; color: #a1b0b8; font-family: 'JetBrains Mono', monospace; }

    /* Contenedores Estilo Rack de Servidores */
    .stMetric { 
        background: rgba(10, 15, 25, 0.95) !important;
        border: 1px solid #1c2b36 !important;
        border-left: 5px solid #00e5ff !important;
        border-radius: 2px !important;
    }

    div[data-testid="stMetricLabel"] p { color: #5e7d8a !important; font-family: 'Orbitron', sans-serif; font-size: 0.7rem !important; letter-spacing: 2px; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; text-shadow: 0 0 10px rgba(0, 229, 255, 0.5); }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #ffffff !important; letter-spacing: 2px; }

    /* Chat de IA Profesional */
    .stChatMessage { background: rgba(17, 25, 40, 0.8) !important; border: 1px solid #1c2b36 !important; border-radius: 5px !important; }
    
    /* Botones y Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #5e7d8a !important; }
    .stTabs [aria-selected="true"] { color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown("<h1 style='margin:0;'>🖥️ LIMS_IA // CORE CONTROL</h1>", unsafe_allow_html=True)
    st.caption("AI-POWERED LABORATORY MANAGEMENT SYSTEM // v9.0")
with c2:
    st.markdown(f"<div style='text-align:right; color:#00e5ff; font-family:Orbitron; padding-top:20px;'>{time.strftime('%H:%M:%S')} UTC</div>", unsafe_allow_html=True)

st.divider()

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.markdown("### 🛠️ SUBSISTEMAS")
    simular_alerta = st.toggle("TEST DE ESTRÉS TÉRMICO")
    encriptacion = st.toggle("CIFRADO CUÁNTICO", value=True)
    st.markdown("---")
    if st.button("🔄 REINICIAR IA"):
        st.session_state.messages = []
        st.rerun()

# --- KPIs ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("FLUJO MUESTRAS", "12,450", "+12.5%")
m2.metric("IA LOAD", "98.8%", "STABLE")
m3.metric("CORE TEMP", "48.2°C" if simular_alerta else "21.4°C", "+26.8°" if simular_alerta else "NOMINAL", delta_color="inverse")
m4.metric("RED IOT", "SECURE", "AES-256")

# --- BLOQUE CENTRAL: GEMELO DIGITAL 3D ---
st.markdown("### 🏔️ TOPOGRAFÍA TÉRMICA EN TIEMPO REAL (GEMELO DIGITAL)")
col_3d, col_2d = st.columns([1.4, 0.6])

with col_3d:
    # --- GRÁFICA TÉRMICA 3D REACTIVA ---
    x_range = np.linspace(-5, 5, 50)
    y_range = np.linspace(-5, 5, 50)
    x, y = np.meshgrid(x_range, y_range)
    
    # Base de temperatura normal (ruido sutil)
    z = np.random.uniform(20.5, 21.5, size=x.shape)
    
    if simular_alerta:
        # Generar "montaña" térmica espectacular en el centro
        z += 30 * np.exp(-(x**2 + y**2) / 2) # Efecto Gaussiano de calor
    
    fig3d = go.Figure(data=[go.Surface(
        z=z, 
        colorscale='Hot' if simular_alerta else 'Viridis',
        showscale=False,
        contours = {"z": {"show": True, "start": 20, "end": 60, "size": 2, "color":"white"}}
    )])
    
    fig3d.update_layout(
        scene=dict(
            xaxis_title='EJE X', yaxis_title='EJE Y', zaxis_title='TEMP °C',
            xaxis=dict(backgroundcolor="rgb(5, 7, 10)", gridcolor="gray", showbackground=True),
            yaxis=dict(backgroundcolor="rgb(5, 7, 10)", gridcolor="gray", showbackground=True),
            zaxis=dict(backgroundcolor="rgb(5, 7, 10)", gridcolor="gray", showbackground=True, range=[15, 60] if simular_alerta else [15, 30]),
        ),
        margin=dict(l=0, r=0, b=0, t=0), 
        height=500,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig3d, use_container_width=True)

with col_2d:
    st.markdown("#### 📡 MAPA DE CALOR 2D")
    fig2d = go.Figure(data=go.Heatmap(z=z, colorscale='Hot' if simular_alerta else 'Viridis', showscale=False))
    fig2d.update_layout(xaxis_visible=False, yaxis_visible=False, margin=dict(l=0, r=0, b=0, t=0), height=250, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2d, use_container_width=True)
    
    st.markdown("#### 🖥️ TERMINAL")
    st.code(f"> MONITORING...\n> " + ("ALERTA TÉRMICA!" if simular_alerta else "SYSTEMS NOMINAL"), language="bash")

st.divider()

# --- BLOQUE FINAL: IA CONVERSACIONAL Y DATOS ---
c_chat, c_data = st.columns([1, 1])

with c_chat:
    st.markdown("### 💬 NÚCLEO COGNITIVO IA")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Sistema LIMS listo. ¿Qué protocolo desea ejecutar?"}]

    # Mostrar mensajes previos (limitado a los últimos 4 por espacio)
    for msg in st.session_state.messages[-4:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escriba comando o consulta a la IA..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if simular_alerta:
                response = "⚠️ ERROR CRÍTICO: El núcleo térmico excede los 45°C. Protocolo de seguridad activado. Consultas suspendidas."
            else:
                response = f"Analizando '{prompt}'... Sincronizando con base de datos LIMS. Estado del laboratorio: Óptimo."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with c_data:
    st.markdown("### ☁️ CLOUD DATABASE SYNC")
    if st.button("📥 SINCRONIZAR CON NUBE"):
        try:
            url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv"
            df = pd.read_csv(url)
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            st.success("DATOS HOSPITALARIOS ACTUALIZADOS")
        except:
            st.error("FALLO DE CONEXIÓN")


