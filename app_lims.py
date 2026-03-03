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
    
    /* 1. CAJAS DE LOS KPIs (Métricas) */
    .stMetric { 
        background-color: #111827; 
        border: 1px solid #1f2937; 
        border-left: 4px solid #00ffcc; 
        padding: 15px; 
        border-radius: 5px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
    }
    
    /* 2. TÍTULOS DE LAS CAJAS (Muestras, Carga CPU, etc.) */
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] > div,
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] span,
    div[data-testid="stMetricLabel"] label { 
        color: #00ffcc !important; 
        font-size: 1.15em !important; 
        font-weight: 800 !important; 
    }
    
    /* 3. NÚMEROS GRANDES (Blanco puro con brillo) */
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div { 
        color: #ffffff !important; 
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.8); 
    }

    /* 4. DELTAS (Los porcentajes pequeñitos de abajo) */
    div[data-testid="stMetricDelta"] > div {
        font-weight: bold !important;
    }

    /* 5. ARREGLO DE LAS ADVERTENCIAS (Alerts, Warnings, Errors) */
    div[data-testid="stAlert"] { 
        background-color: #111827 !important; 
        border: 1px solid #3b82f6 !important; 
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"] * { 
        color: #ffffff !important; 
        font-weight: 500 !important;
        font-size: 1.05em !important;
    }

    /* Estilo de los botones */
    .stButton>button { border-radius: 5px; background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%); border: none; font-weight: bold; transition: all 0.3s ease; color: white !important;}
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
    
    /* Pestañas (Tabs) */
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
    tab_2d, tab_3d = st.tabs(["🗺️ Plano Cenital (Cámara Térmica)", "🌋 Gráfico 3D de Datos"])
    
    with tab_2d:
        st.caption("Monitorización térmica sobre plano técnico.")
        
        # Generamos el Heatmap
        res = 60
        z_2d = np.random.uniform(20.5, 21.5, size=(res, res)) # Ruido de fondo suave
        if simular_alerta:
            for i in range(res):
                for j in range(res):
                    dist = np.sqrt((i-30)**2 + (j-45)**2)
                    if dist < 20: z_2d[i,j] = 50 - dist*1.5

        fig_2d = go.Figure()
        
        # AJUSTE 1: Bajamos la opacidad a 0.35 para que sea casi transparente
        fig_2d.add_trace(go.Heatmap(
            z=z_2d, 
            colorscale='Inferno' if simular_alerta else 'Viridis',
            opacity=0.35, 
            zsmooth='best', 
            showscale=False
        ))
        
        # IMAGEN DE FONDO
        nombre_imagen = "plano_isometrico.png" 
        if os.path.exists(nombre_imagen):
            imagen_fondo = Image.open(nombre_imagen)
            fig_2d.add_layout_image(dict(
                source=imagen_fondo,
                xref="x", yref="y", x=0, y=res, sizex=res, sizey=res,
                sizing="stretch", opacity=0.8, layer="below"
            ))
        else:
            st.warning(f"⚠️ No se encuentra la imagen '{nombre_imagen}' en GitHub.")
        
        # Ocultamos ejes solo en el 2D para que parezca una pantalla limpia
        fig_2d.update_layout(
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_2d, use_container_width=True)
        
    with tab_3d:
        st.caption("Vista de datos térmicos con ejes y cuadrícula de referencia.")
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        xGrid, yGrid = np.meshgrid(y, x)
        z_3d = np.sin(xGrid) * 0.1 + np.cos(yGrid) * 0.1 + 21
        if simular_alerta: z_3d = z_3d + 30 * np.exp(-(xGrid**2 + yGrid**2) / 2)
            
        fig3d = go.Figure(data=[go.Surface(
            z=z_3d, 
            colorscale='Inferno' if simular_alerta else 'Viridis', 
            showscale=False
        )])
        
        # AJUSTE 2: Restauramos los títulos de los ejes y la "caja" matemática 3D
        fig3d.update_layout(
            scene=dict(
                xaxis_title='Eje X (Metros)', 
                yaxis_title='Eje Y (Metros)', 
                zaxis_title='Temp °C',
                camera=dict(eye=dict(x=1.3, y=1.3, z=0.8))
            ), 
            margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3d, use_container_width=True)

with col_sankey:
    st.subheader("⛓️ Trazabilidad: Flujo de Muestras")
    if simular_alerta:
        fuentes, destinos, valores = [0, 1, 1, 2, 2], [1, 2, 4, 4, 3], [100, 20, 80, 20, 0]
    else:
        fuentes, destinos, valores = [0, 1, 2, 3], [1, 2, 3, 5], [100, 95, 90, 85]
        
    fig_sankey = go.Figure(data=[go.Sankey(
        # MAGIA AQUÍ: Forzamos el color, tamaño y fuente de las letras del gráfico
        textfont = dict(color="#ffffff", size=14, family="Arial"),
        node = dict(
            pad=20, 
            thickness=20, 
            line=dict(color="#1f2937", width=1), 
            label=["Recepción", "Extracción", "PCR", "Secuenciadores", "Emergencia (Neveras)", "IA Diagnóstico"], 
            # He oscurecido un poco los nodos para que el texto blanco contraste al máximo
            color=["#2563eb", "#2563eb", "#2563eb", "#ef4444" if simular_alerta else "#2563eb", "#06b6d4", "#10b981"]
        ),
        link = dict(
            source=fuentes, target=destinos, value=valores, 
            color="rgba(59, 130, 246, 0.3)" # Transparencia sutil para que no tape el texto
        )
    )])
    
    fig_sankey.update_layout(
        height=380, 
        margin=dict(l=10, r=10, b=10, t=10), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)'
    )
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
                url_base_datos = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv" 
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













