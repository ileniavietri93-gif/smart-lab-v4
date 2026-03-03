import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os
from PIL import Image

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(page_title="LIMS IA - CONTROL SYSTEM", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: ESTÉTICA DE CONTROL MILITAR / CIENTÍFICO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    /* Fondo de pantalla de operaciones */
    .stApp { background-color: #030508; color: #a1b0b8; font-family: 'JetBrains Mono', monospace; }

    /* Contenedores con efecto de profundidad */
    .stMetric { 
        background: rgba(10, 15, 25, 0.95) !important;
        border: 1px solid #1c2b36 !important;
        border-top: 3px solid #00e5ff !important;
        padding: 15px !important;
        border-radius: 2px !important;
    }

    /* Títulos de datos neón */
    div[data-testid="stMetricLabel"] p { 
        color: #5e7d8a !important; 
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem !important;
        letter-spacing: 2px;
    }
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }

    /* Encabezados de Sección */
    h1, h2, h3 { 
        font-family: 'Orbitron', sans-serif;
        color: #ffffff !important; 
        letter-spacing: 3px;
        text-transform: uppercase;
        border-bottom: 1px solid #1c2b36;
        padding-bottom: 10px;
    }

    /* Pestañas funcionales */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; gap: 5px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #0a0f19 !important;
        border: 1px solid #1c2b36 !important;
        color: #5e7d8a !important;
        font-size: 0.8rem;
    }
    .stTabs [aria-selected="true"] { border-color: #00e5ff !important; color: #00e5ff !important; }

    /* Personalización de botones industriales */
    .stButton>button {
        width: 100%;
        background: transparent;
        color: #00e5ff;
        border: 1px solid #00e5ff;
        border-radius: 0px;
        font-family: 'Orbitron', sans-serif;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(0, 229, 255, 0.1);
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER DE OPERACIONES ---
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown("# 🖥️ LIMS_IA // CORE_V8.0")
    st.caption("ESTADO: SINCRONIZADO // UBICACIÓN: SECTOR ALFA-9 // SEGURIDAD: NIVEL 5 ACTIVADO")
with c2:
    st.markdown(f"<div style='text-align:right; color:#00e5ff; font-family:Orbitron;'>{time.strftime('%H:%M:%S')} UTC</div>", unsafe_allow_html=True)

st.divider()

# --- PANEL LATERAL TÉCNICO ---
with st.sidebar:
    st.markdown("### 🎛️ CONTROL DE SUBSISTEMAS")
    simular_alerta = st.toggle("TEST DE ESTRÉS TÉRMICO")
    encriptacion = st.toggle("CIFRADO CUÁNTICO", value=True)
    st.markdown("---")
    st.markdown("### 🛰️ TELEMETRÍA IOT")
    st.code("LATENCY: 0.04ms\nUPLINK: ACTIVE\nINTEGRITY: 100%", language="bash")

# --- DASHBOARD DE MÉTRICAS CRÍTICAS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("FLUJO DE MUESTRAS", "12,450.0", "NOMINAL")
m2.metric("PROCESAMIENTO IA", "98.8%", "-1.2%" if not simular_alerta else "CRITICAL")
m3.metric("NÚCLEO TÉRMICO", "48.2°C" if simular_alerta else "21.4°C", "+26.8°" if simular_alerta else "STABLE", delta_color="inverse")
m4.metric("ESTADO DE RED", "SECURE" if encriptacion else "OPEN", "Q-BIT ACTIVE")

# --- EL GEMELO DIGITAL IA ---
col_map, col_data = st.columns([1.2, 0.8])

with col_map:
    st.markdown("### 🗺️ ANÁLISIS ISOMÉTRICO // DIGITAL TWIN")
    t1, t2 = st.tabs(["VISTA TÉRMICA 2D", "TOPOGRAFÍA DE DATOS 3D"])
    
    with t1:
        res = 50
        z = np.random.uniform(20.5, 21.5, size=(res, res))
        if simular_alerta:
            # Simulación de anomalía en el sector de reactores
            z[20:35, 10:25] += 20 + np.random.normal(0, 2, (15, 15))
        
        fig2 = go.Figure(data=go.Heatmap(z=z, colorscale='Cividis' if not simular_alerta else 'Hot', zsmooth='best', showscale=False))
        
        # Carga de plano local
        nombre_img = "plano_isometrico.png"
        if os.path.exists(nombre_img):
            img = Image.open(nombre_img)
            fig2.add_layout_image(dict(source=img, xref="x", yref="y", x=0, y=res, sizex=res, sizey=res, sizing="stretch", opacity=0.6, layer="below"))
        
        fig2.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=450, xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    with t2:
        # Gráfico 3D de alta precisión
        x, y = np.meshgrid(np.linspace(-3, 3, 40), np.linspace(-3, 3, 40))
        z_3d = np.exp(-(x**2 + y**2))
        if simular_alerta: z_3d *= 8
        
        fig3 = go.Figure(data=[go.Surface(z=z_3d, colorscale='Cividis', showscale=False)])
        fig3.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), margin=dict(l=0,r=0,b=0,t=0), height=450, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

with col_data:
    st.markdown("### 📊 DIAGNÓSTICO DE IA")
    # Indicador de Salud del Sistema (Gauge Profesional)
    val_salud = 38 if simular_alerta else 96
    fig_salud = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = val_salud,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "#00e5ff"},
            'bar': {'color': "#00e5ff"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [{'range': [0, 40], 'color': 'rgba(255, 0, 0, 0.3)'}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig_salud.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#ffffff", 'family': "Orbitron"}, height=350)
    st.plotly_chart(fig_salud, use_container_width=True)
    
    st.markdown("#### ⌨️ SISTEMA DE REGISTRO // LOGS")
    log_txt = f"> [{time.strftime('%H:%M')}] SYNC_CLOUD: SUCCESS\n> [{time.strftime('%H:%M')}] IA_SCAN: NOMINAL"
    if simular_alerta:
        log_txt += f"\n> [{time.strftime('%H:%M')}] ALERT: THERMAL_OVERHEAT_S7\n> [{time.strftime('%H:%M')}] ACTION: VENT_ACTIVE"
    st.code(log_txt, language="bash")

# --- CONEXIÓN DE DATOS ---
st.divider()
st.markdown("### ☁️ CLOUD LIMS // DATA INTEGRATION")
if st.button("EJECUTAR SINCRONIZACIÓN DE MUESTRAS"):
    with st.spinner("ACCEDIENDO A SERVIDORES CENTRALES..."):
        time.sleep(1.2)
        try:
            url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv"
            df = pd.read_csv(url)
            st.dataframe(df.style.set_properties(**{'background-color': '#0a0f19', 'color': '#00e5ff', 'border-color': '#1c2b36'}), use_container_width=True)
        except:
            st.error("ERROR_CODE: 404 // DATABASE_NOT_FOUND")


