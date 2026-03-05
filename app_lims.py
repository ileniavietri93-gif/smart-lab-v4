import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILOS (DASHBOARD DARK MODE) ---
st.set_page_config(page_title="LIMS IA Alpha v10.2", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    /* Fondo de operaciones y textos básicos */
    .stApp { background-color: #030508; color: #a1b0b8; font-family: 'JetBrains Mono', monospace; }
    
    /* 1. CAJAS DE LOS KPIs (Métricas) */
    .stMetric { 
        background: rgba(10, 15, 25, 0.9) !important;
        border: 1px solid #1f2937 !important;
        border-top: 3px solid #00ffcc !important;
        padding: 15px; 
        border-radius: 2px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
    }
    
    /* Títulos de las cajas (Muestras, Carga CPU, etc.) - Cyan brillante */
    div[data-testid="stMetricLabel"] p { 
        color: #00ffcc !important; 
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8em !important; 
        font-weight: 800 !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Números de las cajas - Blanco nuclear */
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.4); 
    }

    /* 2. TÍTULOS DE SECCIÓN */
    h1, h2, h3, h4, .stSubheader, [data-testid="stHeader"], .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { 
        color: #ffffff !important; 
        font-family: 'Orbitron', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* 3. ARREGLO DE LAS ADVERTENCIAS Y ALERTAS */
    div[data-testid="stAlert"] { 
        background-color: #111827 !important; 
        border: 1px solid #ef4444 !important; /* Rojo emergencia */
        border-radius: 4px !important;
    }
    div[data-testid="stAlert"] * { 
        color: #ffffff !important; 
    }

    /* 4. CHATBOT: Forzar texto en blanco para máxima legibilidad */
    div[data-testid="stChatMessageContent"], 
    div[data-testid="stChatMessageContent"] p, 
    div[data-testid="stChatMessageContent"] div {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.05em;
    }

    /* Estilo de los botones industriales */
    .stButton>button { 
        border-radius: 2px; 
        background: transparent;
        border: 1px solid #00ffcc;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        transform: scale(1.05); 
        background-color: rgba(0, 255, 204, 0.1);
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.5); 
    }
    
    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { background-color: #030508; }
    .stTabs [data-baseweb="tab"] { color: #e2e8f0; font-family: 'Orbitron', sans-serif; font-size: 0.8em; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #3b82f6; }

    /* Estilo para los textos en Plots (fuerza visibilidad) */
    .xtick text, .ytick text, .ztick text { fill: white !important; font-family: 'JetBrains Mono' !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER DE OPERACIONES DE MISIÓN CRÍTICA ---
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    st.markdown("<h1>🧬 BIO-DIGITAL OS <span style='color:#00ffcc; font-size:0.5em;'>ALPHA_V10.2</span></h1>", unsafe_allow_html=True)
    st.caption("AI-POWERED LABORATORY SIMULATION AND CONTROL CORE // SYSTEMS NOMINAL")
with c2:
    st.markdown(f"<div style='text-align:right; color:#00ffcc; font-family:Orbitron; padding-top:20px;'>{time.strftime('%H:%M:%S')} UTC</div>", unsafe_allow_html=True)
st.divider()

# --- PANEL LATERAL TÉCNICO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103322.png", width=60)
    st.markdown("### 🎛️ PANEL DE CONTROL")
    simular_alerta = st.toggle("SIMULAR FALLO TÉRMICO (ESTRÉS)", key="alerta_simulada")
    seguridad = st.toggle("BLOQUEO CUÁNTICO", value=True)
    st.markdown("---")
    if simular_alerta:
        st.error("ALERTA: SOBRECALENTAMIENTO EN EL SECTOR 7B")
    else:
        st.info("LATENCIA: 4.2ms // PAQUETES: 100% // STATUS: SECURE")

# --- KPIs CON EFECTO GLOW NEÓN ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("🧬 MUESTRAS", "12,450", delta="Prioridad A1")
k2.metric("⚡ CARGA CPU IA", "94.2%", delta="Nominal")
k3.metric("🌡️ TEMP. GENERAL", "48.5°C" if simular_alerta else "21.5°C", delta="+27.0°C" if simular_alerta else "-0.2°C", delta_color="inverse")
k4.metric("🛡️ ESTADO RED IOT", "SECURE" if seguridad else "OPEN", delta="Cifrado" if seguridad else "Vulnerable")

# --- GEMELO DIGITAL: PROYECCIÓN SOBRE PLANO REAL Y SUPERFICIE 3D ---
col_gemelo, col_sankey = st.columns(2)

with col_gemelo:
    st.markdown("### 🌐 Gemelo Digital // Planta")
    tab_2d, tab_3d = st.tabs(["🗺️ Isométrico (Overlay IoT)", "🌋 Topografía de Datos"])
    
    with tab_2d:
        st.caption("Overlay térmico sobre plano técnico real.")
        res = 60
        z_2d = np.random.uniform(20.5, 21.5, size=(res, res))
        if simular_alerta:
            for i in range(res):
                for j in range(res):
                    dist = np.sqrt((i-res//2)**2 + (j-res*2//3)**2)
                    if dist < 15: z_2d[i,j] = 50 - dist*1.5

        fig_2d = go.Figure()
        fig_2d.add_trace(go.Heatmap(
            z=z_2d, 
            colorscale='Inferno' if simular_alerta else 'Tealgrn',
            opacity=0.45, 
            zsmooth='best', 
            showscale=True,
            colorbar=dict(title="°C", tickcolor="white", tickfont=dict(color="white"))
        ))
        
        nombre_imagen = "plano_isometrico.png" 
        if os.path.exists(nombre_imagen):
            imagen_fondo = Image.open(nombre_imagen)
            fig_2d.add_layout_image(dict(
                source=imagen_fondo, 
                xref="x", yref="y", x=0, y=res, sizex=res, sizey=res,
                sizing="stretch", opacity=0.8, layer="below"
            ))
        
        fig_2d.update_layout(
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_2d, use_container_width=True)
        
    with tab_3d:
        st.caption("Vista topográfica pura de los datos térmicos IoT.")
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        xGrid, yGrid = np.meshgrid(y, x)
        z_3d = np.sin(xGrid) * 0.1 + np.cos(yGrid) * 0.1 + 21
        if simular_alerta: z_3d = z_3d + 30 * np.exp(-(xGrid**2 + yGrid**2) / 2)
            
        fig3d = go.Figure(data=[go.Surface(
            z=z_3d, 
            colorscale='Inferno' if simular_alerta else 'Tealgrn', 
            showscale=False,
            contours = {"z": {"show": True, "start": 22, "end": 50, "size": 2, "color":"white"}}
        )])
        
        fig3d.update_layout(
            scene=dict(
                xaxis_title='X (m)', yaxis_title='
        
