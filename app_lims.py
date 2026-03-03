import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
from PIL import Image

# --- 1. CONFIGURACIÓN EXTREMA Y ESTILOS (DASHBOARD DARK MODE) ---
st.set_page_config(page_title="Bio-Digital OS v5.0", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #00ffcc; font-family: 'Courier New', Courier, monospace;}
    h1, h2, h3 { color: #ffffff !important; font-family: 'Arial', sans-serif;}
    .stMetric { background-color: #111827; border: 1px solid #1f2937; border-left: 4px solid #00ffcc; padding: 15px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    div[data-testid="stMetricLabel"] p { color: #00ffcc !important; font-size: 1.15em !important; font-weight: 800 !important; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.8); }
    div[data-testid="stAlert"] { background-color: #111827 !important; border: 1px solid #3b82f6 !important; border-radius: 8px !important; }
    div[data-testid="stAlert"] * { color: #ffffff !important; }
    .stButton>button { border-radius: 5px; background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%); border: none; font-weight: bold; color: white !important;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    st.markdown("<h1>🧬 BIO-DIGITAL OS <span style='color:#3b82f6; font-size:0.5em;'>v5.0 3D DIGITAL TWIN EDITION</span></h1>", unsafe_allow_html=True)

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
        fig3d.update_layout(scene=dict(xaxis_title='Eje X', yaxis_title='Eje Y', zaxis_title='Temp °C'), margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3d, use_container_width=True)

with col_sankey:
    st.subheader("⛓️ Trazabilidad: Flujo de Muestras")
    fuentes, destinos, valores = ([0, 1, 1, 2, 2], [1, 2, 4, 4, 3], [100, 20, 80, 20, 0]) if simular_alerta else ([0, 1, 2, 3], [1, 2, 3, 5], [100, 95, 90, 85])
    fig_sankey = go.Figure(data=[go.Sankey(
        textfont = dict(color="#ffffff", size=14),
        node = dict(pad=20, thickness=20, label=["Recepción", "Extracción", "PCR", "Secuenciadores", "Emergencia", "IA Diagnóstico"], color=["#2563eb", "#2563eb", "#2563eb", "#ef4444" if simular_alerta else "#2563eb", "#06b6d4", "#10b981"]),
        link = dict(source=fuentes, target=destinos, value=valores, color="rgba(59, 130, 246, 0.3)")
    )])
    fig_sankey.update_layout(height=380, margin=dict(l=10, r=10, b=10, t=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sankey, use_container_width=True)

st.divider()

# --- CONEXIÓN CLOUD Y TELEMETRÍA ---
st.subheader("☁️ Cloud LIMS: Conexión a Base de Datos Externa")
col_db1, col_db2 = st.columns([2, 1])

with col_db1:
    if st.button("🔄 Sincronizar con Servidor Hospitalario"):
        with st.spinner('Sincronizando...'):
            time.sleep(1.5)
            try:
                url_base_datos = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv"
                df_nube = pd.read_csv(url_base_datos)
                st.success(f"✅ Sincronizado: {len(df_nube)} registros.")
                st.dataframe(df_nube, use_container_width=True, hide_index=True)
                
                with col_db2:
                    st.write("#### 📊 Análisis de Estabilidad")
                    t_data = np.linspace(0, 10, 20)
                    temp_base = 21.5 + np.random.normal(0, 0.2, 20)
                    if simular_alerta: temp_base[15:] += 15
                    fig_tel = go.Figure()
                    fig_tel.add_trace(go.Scatter(x=t_data, y=temp_base, mode='lines+markers', line=dict(color='#00ffcc', width=3)))
                    fig_tel.add_hrect(y0=20, y1=23, fillcolor="green", opacity=0.1, line_width=0)
                    fig_tel.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
                    st.plotly_chart(fig_tel, use_container_width=True)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# --- SECCIÓN FINAL ---
st.divider()
col_chat, col_output = st.columns([1, 1])

with col_chat:
    st.subheader("💬 Asistente IA")
    if "mensajes" not in st.session_state: st.session_state.mensajes = [{"role": "assistant", "content": "Hola, soy el núcleo del Bio-Digital LIMS."}]
    for msg in st.session_state.mensajes[-2:]:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Consulta a la IA..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        res = "⚠️ BLOQUEO POR FALLO CRÍTICO." if simular_alerta else f"Análisis de '{prompt}': Sistemas OK."
        st.session_state.mensajes.append({"role": "assistant", "content": res})
        st.rerun()

with col_output:
    st.subheader("🖥️ Terminal")
    with st.container(height=230, border=True):
        if genetica: st.success(">>> [MÓDULO 1] Variantes BRCA1 detectadas.")
        elif vision: st.warning(">>> [MÓDULO 2] Conteo de colonias irregular.")
        elif roi: st.info(">>> [MÓDULO 4] ROI proyectado: 145%.")
        elif simular_alerta: st.error(">>> [HALT] SOBRECALENTAMIENTO.")
        else: st.write(">>> Monitorizando sensores IoT...")

















