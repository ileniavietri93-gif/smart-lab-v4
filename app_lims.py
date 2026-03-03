import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="Bio-Digital OS v5.0", layout="wide", initial_sidebar_state="expanded")

# Inyectamos el CSS correctamente dentro de st.markdown
st.markdown("""
    <style>
    /* 1. FONDO Y TEXTO BASE */
    .main { 
        background-color: #0b0f19; 
        color: #e2e8f0; 
        font-family: 'Courier New', Courier, monospace;
    }

    /* 2. TÍTULOS PRINCIPALES (H1, H2, H3) - Blanco brillante con sombra */
    h1, h2, h3, .stSubheader, [data-testid="stHeader"] { 
        color: #ffffff !important; 
        font-family: 'Arial', sans-serif;
        text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.3);
        font-weight: 700 !important;
    }

    /* 3. CAJAS DE LOS KPIs (Métricas) */
    .stMetric { 
        background-color: #111827; 
        border: 1px solid #1f2937; 
        border-left: 4px solid #00ffcc; 
        padding: 15px; 
        border-radius: 5px; 
    }
    
    /* Títulos de las cajas (Muestras, Carga CPU, etc.) - Cyan neón */
    div[data-testid="stMetricLabel"] p { 
        color: #00ffcc !important; 
        font-size: 1.1em !important; 
        font-weight: 800 !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Números de las cajas - Blanco nuclear */
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5); 
    }

    /* 4. TEXTOS DE CAPTION Y LABELS */
    .stCaption, label, .stMarkdown p {
        color: #cbd5e1 !important; 
        font-size: 1.05em !important;
    }

    /* 5. ALERTAS */
    div[data-testid="stAlert"] { 
        background-color: #111827 !important; 
        border: 1px solid #3b82f6 !important; 
    }
    div[data-testid="stAlert"] * { 
        color: #ffffff !important; 
    }

    /* BOTONES */
    .stButton>button { 
        border-radius: 5px; 
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%); 
        color: white !important;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    st.markdown("<h1>🧬 BIO-DIGITAL OS <span style='color:#3b82f6; font-size:0.5em;'>v5.0 3D TWIN</span></h1>", unsafe_allow_html=True)

st.divider()

# --- PANEL LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103322.png", width=60)
    st.markdown("### 🎛️ PANEL DE CONTROL")
    genetica = st.button("🧬 Módulo Genética")
    vision = st.button("👁️ Módulo Visión 3D")
    seguridad = st.toggle("🛡️ Encriptación Cuántica")
    roi = st.button("💰 Módulo ROI")
    st.markdown("---")
    simular_alerta = st.toggle("🚨 FALLO DEL SISTEMA (LIMS)")

# --- KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("🧬 Muestras", "12,450", delta="Prioridad 1" if simular_alerta else "+312 hoy")
k2.metric("⚡ Carga CPU IA", "94.2%", delta="Sobrecarga" if simular_alerta else "-2.1%", delta_color="inverse")
k3.metric("🌡️ Temp. General", "48.5°C" if simular_alerta else "21.5°C", delta="+27.0°C" if simular_alerta else "-0.2°C", delta_color="inverse")
k4.metric("🛡️ Integridad Red", "100%" if seguridad else "82%", delta="Encriptado" if seguridad else "Riesgo Medio")

# --- GEMELO DIGITAL Y TRAZABILIDAD ---
st.markdown("### 🌐 Gemelo Digital y Trazabilidad") # Título con visibilidad forzada
col_gemelo, col_sankey = st.columns(2)

with col_gemelo:
    tab_2d, tab_3d = st.tabs(["🗺️ Plano Cenital", "🌋 Gráfico 3D"])
    with tab_2d:
        res = 60
        z_2d = np.random.uniform(20.5, 21.5, size=(res, res))
        if simular_alerta:
            for i in range(res):
                for j in range(res):
                    dist = np.sqrt((i-30)**2 + (j-45)**2)
                    if dist < 20: z_2d[i,j] = 50 - dist*1.5
        fig_2d = go.Figure()
        fig_2d.add_trace(go.Heatmap(z=z_2d, colorscale='Inferno' if simular_alerta else 'Viridis', opacity=0.35, zsmooth='best', showscale=False))
        nombre_imagen = "plano_isometrico.png"
        if os.path.exists(nombre_imagen):
            imagen_fondo = Image.open(nombre_imagen)
            fig_2d.add_layout_image(dict(source=imagen_fondo, xref="x", yref="y", x=0, y=res, sizex=res, sizey=res, sizing="stretch", opacity=0.8, layer="below"))
        fig_2d.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_2d, use_container_width=True)
    with tab_3d:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        xGrid, yGrid = np.meshgrid(y, x)
        z_3d = np.sin(xGrid) * 0.1 + np.cos(yGrid) * 0.1 + 21
        if simular_alerta: z_3d = z_3d + 30 * np.exp(-(xGrid**2 + yGrid**2) / 2)
        fig3d = go.Figure(data=[go.Surface(z=z_3d, colorscale='Inferno' if simular_alerta else 'Viridis', showscale=False)])
        fig3d.update_layout(scene=dict(xaxis_title='Eje X', yaxis_title='Eje Y', zaxis_title='Temp °C', xaxis=dict(color="white"), yaxis=dict(color="white"), zaxis=dict(color="white")),










