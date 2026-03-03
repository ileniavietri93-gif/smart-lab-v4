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
    /* Fondo general y textos básicos */
    .main { background-color: #0b0f19; color: #00ffcc; font-family: 'Courier New', Courier, monospace;}
    h1, h2, h3 { color: #ffffff !important; font-family: 'Arial', sans-serif;}
    
    /* Diseño de las cajas de los KPIs */
    .stMetric { background-color: #111827; border: 1px solid #1f2937; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    
    /* MAGIA AQUÍ: Forzar los números grandes a BLANCO puro y con brillo */
    div[data-testid="stMetricValue"] { color: #ffffff !important; text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.4); }
    
    /* Forzar los títulos de arriba de los números a gris claro/blanco */
    div[data-testid="stMetricLabel"] p { color: #e2e8f0 !important; font-size: 1.1em !important; }

    /* Estilo de los botones */
    .stButton>button { border-radius: 5px; background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%); border: none; font-weight: bold; transition: all 0.3s ease; color: white !important;}
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
    
    /* Estilo de las pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { background-color: #0b0f19; }
    .stTabs [data-baseweb="tab"] { color: #e2e8f0; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #3b82f6; }
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

# --- EL NUEVO GEMELO DIGITAL: ISOMÉTRICO 3D REALISTA + DATA 3D ---
col_gemelo, col_sankey = st.columns(2)

with col_gemelo:
    # Usamos pestañas para separar la vista Isométrica (la "App") de la Topografía de Datos
    tab_iso, tab_3d = st.tabs(["🗺️ Isométrico 3D: Planta (Overlay IoT Real)", "🌋 Topografía Térmica: Datos raw 3D"])
    
    with tab_iso:
        st.caption("Mapa Térmico de Sensores IoT superpuesto sobre plano isométrico real.")
        
        # INTENTAMOS CARGAR LA IMAGEN ISOMÉTRICA LOCAL
        if os.path.exists("plano_isometrico.png"):
            img_iso = Image.open("plano_isometrico.png")
            # Obtenemos dimensiones para ajustar la resolución del heatmap
            ancho_img, alto_img = img_iso.size
        else:
            st.error("⚠️ No se encuentra 'plano_isometrico.png' en la carpeta. Usando mapa de calor sin plano.")
            img_iso = None

        # Generamos el Heatmap (Alta resolución para el overlay)
        res = 60
        z_iso = np.random.uniform(20, 22, size=(res, res)) # Ruido de fondo
        if simular_alerta:
            # Creamos una "mancha" de calor en la zona central-derecha (ej: secuenciador)
            for i in range(res):
                for j in range(res):
                    dist = np.sqrt((i-res//2)**2 + (j-res*2//3)**2)
                    if dist < 15: z_iso[i,j] = 50 - dist*2

        fig_iso = go.Figure()
        
        # Capa 1: El Heatmap con Opacidad del 60%
        fig_iso.add_trace(go.Heatmap(
            z=z_iso, 
            colorscale='Hot' if simular_alerta else 'Viridis',
            opacity=0.6 if img_iso else 1.0, 
            showscale=True,
            colorbar=dict(ticksuffix="°C")
        ))
        
        # Capa 2: La Imagen Isométrica 3D por debajo
        if img_iso:
            fig_iso.add_layout_image(dict(
                source=img_iso, # Python PIL procesa la imagen local
                xref="x", yref="y", x=0, y=res, sizex=res, sizey=res,
                sizing="stretch", opacity=0.9, layer="below"
            ))
        
        fig_iso.update_layout(
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_iso, use_container_width=True)
        
    with tab_3d:
        # MANTENEMOS EL "VOLCÁN" 3D DE DATOS RAW (Por si acaso)
        st.caption("Vista topográfica pura de los datos térmicos IoT. Rótala con el ratón.")
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        xGrid, yGrid = np.meshgrid(y, x)
        z_3d = np.sin(xGrid) * 0.1 + np.cos(yGrid) * 0.1 + 21
        if simular_alerta: z_3d = z_3d + 30 * np.exp(-(xGrid**2 + yGrid**2) / 2)
            
        fig3d = go.Figure(data=[go.Surface(z=z_3d, colorscale='Hot' if simular_alerta else 'Viridis', showscale=False)])
        fig3d.update_layout(scene=dict(xaxis_title='X (Metros)', yaxis_title='Y (Metros)', zaxis_title='Temp °C', camera=dict(eye=dict(x=1.3, y=1.3, z=1.1))), margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3d, use_container_width=True)

with col_sankey:
    # EL DIAGRAMA SANKEY SIGUE SIENDO VITAL PARA LA TRAZABILIDAD
    st.subheader("⛓️ Trazabilidad: Flujo de Muestras")
    if simular_alerta:
        fuentes, destinos, valores = [0, 1, 1, 2, 2], [1, 2, 4, 4, 3], [100, 20, 80, 20, 0]
    else:
        fuentes, destinos, valores = [0, 1, 2, 3], [1, 2, 3, 5], [100, 95, 90, 85]
        
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=["Recepción", "Extracción", "PCR", "Secuenciadores", "Emergencia (Neveras)", "IA Diagnóstico"], color=["blue", "blue", "blue", "red" if simular_alerta else "blue", "cyan", "green"]),
        link = dict(source=fuentes, target=destinos, value=valores, color="rgba(100, 150, 250, 0.4)")
    )])
    fig_sankey.update_layout(height=400, margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_sankey, use_container_width=True)

st.divider()

# --- CONEXIÓN A GOOGLE SHEETS (CLOUD) ---
st.subheader("☁️ Cloud LIMS: Conexión a Base de Datos Externa")
col_db1, col_db2 = st.columns([2, 1])

with col_db1:
    if st.button("🔄 Sincronizar con Google Sheets (Live)"):
        with st.spinner('Petición API en curso...'):
            time.sleep(1.5) # Pausa dramática
            try:
                # !!! ATENCIÓN: PEGA TU ENLACE AQUÍ !!!
                url_base_datos = "https://docs.google.com/spreadsheets/d/1d4-bVcEzF2ToagSJJYGMnTzXHVEJmOkn_CUGEzCBZXo/edit?usp=sharing" 
                df_nube = pd.read_csv(url_base_datos)
                st.success(f"✅ Conexión establecida. {len(df_nube)} muestras sincronizadas.")
                st.dataframe(df_nube, use_container_width=True, hide_index=True)
                
                with col_db2:
                    st.write("#### 📊 Distribución de Urgencias")
                    columna_grafico = df_nube.columns[1] if len(df_nube.columns) > 1 else df_nube.columns[0]
                    fig_pie = px.pie(df_nube, names=columna_grafico, hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
                    fig_pie.update_layout(height=280, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
                    st.plotly_chart(fig_pie, use_container_width=True)
            except Exception as e:
                st.error(f"⚠️ Error de conexión Cloud. Revisa el enlace CSV.")

# --- CHATBOT Y CONSOLA DE TERMINAL ---
st.divider()
col_chat, col_output = st.columns([1, 1])

with col_chat:
    st.subheader("💬 Asistente IA del LIMS")
    if "mensajes" not in st.session_state: st.session_state.mensajes = [{"role": "assistant", "content": "Hola, soy el núcleo del Bio-Digital LIMS. ¿En qué te ayudo?"}]
    for msg in st.session_state.mensajes[-2:]:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Ej: Protocolo de emergencia..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        respuesta = "⚠️ SISTEMA AISLADO POR FALLO CRÍTICO." if simular_alerta else f"Análisis de '{prompt}': Sistemas operativos al 94% de eficiencia. No se requieren acciones manuales."
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
        st.rerun()

with col_output:
    st.subheader("🖥️ Terminal de Subsistemas")
    terminal_box = st.container(height=230, border=True)
    with terminal_box:
        if genetica: st.success(">>> [MÓDULO 1] Variantes identificadas en BRCA1. OK")
        elif vision: st.warning(">>> [MÓDULO 2] Segmentación bacteriana completa. Detección de colonias irregulares.")
        elif roi: st.info(">>> [MÓDULO 4] TCO calculado. ROI proyectado: 145% anual.")
        elif simular_alerta: st.error(">>> [SYS_HALT] FATAL ERROR 0x00B. Motores sobrecalentados. Protocolo criogénico activado.")
        else: st.write(">>> Monitorizando sensores IoT de planta...\n>>> Esperando comandos de operadores.")

