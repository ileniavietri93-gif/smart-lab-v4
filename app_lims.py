import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILOS (DASHBOARD DARK MODE) ---
st.set_page_config(page_title="LIMS IA Alpha v10.0", layout="wide", initial_sidebar_state="collapsed")

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

    /* 3. ARREGLO DE LAS ADVERTENCIAS */
    div[data-testid="stAlert"] { 
        background-color: #111827 !important; 
        border: 1px solid #ef4444 !important; /* Rojo emergencia */
        border-radius: 4px !important;
    }
    div[data-testid="stAlert"] * { 
        color: #ffffff !important; 
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
    st.markdown("<h1>🧬 BIO-DIGITAL OS <span style='color:#00ffcc; font-size:0.5em;'>ALPHA_V10.0</span></h1>", unsafe_allow_html=True)
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
        st.snow()
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
        
        # 1. Generamos el Mapa de Calor (Heatmap)
        res = 60
        z_2d = np.random.uniform(20.5, 21.5, size=(res, res)) # Ruido de fondo suave
        if simular_alerta:
            # Foco de calor en el lado derecho
            for i in range(res):
                for j in range(res):
                    dist = np.sqrt((i-res//2)**2 + (j-res*2//3)**2)
                    if dist < 15: z_2d[i,j] = 50 - dist*1.5

        fig_2d = go.Figure()
        
        # Capa 1: EL HEATMAP CON TRANSPARENCIA (opacity=0.45)
        # Usamos zsmooth='best' para el difuminado técnico
        fig_2d.add_trace(go.Heatmap(
            z=z_2d, 
            colorscale='Inferno' if simular_alerta else 'Tealgrn',
            opacity=0.45, 
            zsmooth='best', 
            showscale=True,
            colorbar=dict(title="°C", tickcolor="white", font=dict(color="white"))
        ))
        
        # Capa 2: LA IMAGEN LOCAL plano_isometrico.png COMO FONDO (Si existe)
        # Esto soluciona tu problema: carga la imagen y la pone DEBAJO del color
        nombre_imagen = "plano_isometrico.png" 
        if os.path.exists(nombre_imagen):
            imagen_fondo = Image.open(nombre_imagen)
            fig_2d.add_layout_image(dict(
                source=imagen_fondo, # Python PIL procesa la imagen local
                xref="x", yref="y", x=0, y=res, sizex=res, sizey=res,
                sizing="stretch", opacity=0.8, layer="below"
            ))
        else:
            st.warning(f"⚠️ No se encuentra '{nombre_imagen}' en GitHub. Usando mapa sin plano.")
        
        # Ocultamos ejes para que parezca una pantalla de radar
        fig_2d.update_layout(
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_2d, use_container_width=True)
        
    with tab_3d:
        st.caption("Vista topográfica pura de los datos térmicos IoT. Rótala con el ratón.")
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
        
        # Mostramos la caja matemática para que parezca un simulador
        fig3d.update_layout(
            scene=dict(
                xaxis_title='X (Metros)', 
                yaxis_title='Y (Metros)', 
                zaxis_title='Temp °C',
                camera=dict(eye=dict(x=1.3, y=1.3, z=0.8)),
                xaxis=dict(color="white"),
                yaxis=dict(color="white"),
                zaxis=dict(color="white")
            ), 
            margin=dict(l=0, r=0, b=0, t=0), height=380, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3d, use_container_width=True)

with col_sankey:
    # EL DIAGRAMA SANKEY SIGUE SIENDO VITAL PARA LA TRAZABILIDAD
    st.subheader("⛓️ TRAZABILIDAD IOT")
    if simular_alerta:
        fuentes, destinos, valores = [0, 1, 1, 2, 2], [1, 2, 4, 4, 3], [100, 20, 80, 20, 0]
    else:
        fuentes, destinos, valores = [0, 1, 2, 3], [1, 2, 3, 5], [100, 95, 90, 85]
        
    fig_sankey = go.Figure(data=[go.Sankey(
        textfont = dict(color="#ffffff", size=14, family="Arial"),
        node = dict(pad=15, thickness=20, line=dict(color="white", width=0.5), label=["Recepción", "Extracción", "PCR", "Secuenciadores", "Emergencia (Neveras)", "IA Diagnóstico"], color=["blue", "blue", "blue", "red" if simular_alerta else "blue", "cyan", "green"]),
        link = dict(source=fuentes, target=destinos, value=valores, color="rgba(100, 150, 250, 0.4)")
    )])
    fig_sankey.update_layout(height=400, margin=dict(l=10, r=10, b=10, t=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_sankey, use_container_width=True)

st.divider()

# --- CONEXIÓN A GOOGLE SHEETS (CLOUD LIMS) + TELEMETRÍA ---
st.subheader("☁️ CLOUD LIMS // DATA INTEGRATION")
col_db1, col_db2 = st.columns([2, 1])

with col_db1:
    if st.button("🔄 Sincronizar Servidor Cloud Hospitalario"):
        with st.spinner('Petición API en curso... Conectando a servidores seguros...'):
            time.sleep(1.2) # Pausa dramática
            try:
                # !!! ATENCIÓN: TU ENLACE AQUÍ !!!
                url_base_datos = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv" 
                df_nube = pd.read_csv(url_base_datos)
                st.success(f"CONEXIÓN OK: {len(df_nube)} registros sincronizados desde la nube.")
                st.dataframe(df_nube, use_container_width=True, hide_index=True)
                
                with col_db2:
                    st.write("#### 📊 ANÁLISIS DE ESTABILIDAD")
                    t_data = np.linspace(0, 10, 20)
                    temp_base = 21.5 + np.random.normal(0, 0.2, 20)
                    if simular_alerta: temp_base[15:] += 15
                    fig_tel = go.Figure()
                    fig_tel.add_trace(go.Scatter(x=t_data, y=temp_base, mode='lines+markers', line=dict(color='#00ffcc', width=3)))
                    fig_tel.add_hrect(y0=20, y1=23, fillcolor="green", opacity=0.1, line_width=0)
                    fig_tel.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), xaxis=dict(color="white"), yaxis=dict(color="white"))
                    st.plotly_chart(fig_tel, use_container_width=True)
            except Exception as e:
                st.error(f"⚠️ Error de enlace Cloud. Revisa el enlace CSV en GitHub.")

# --- SECCIÓN FINAL: ASISTENTE IA Y TERMINAL ---
st.divider()
col_chat, col_output = st.columns([1, 1])

with col_chat:
    st.subheader("💬 NÚCLEO COGNITIVO IA LIMS")
    if "messages" not in st.session_state: st.session_state.messages = [{"role": "assistant", "content": "Bienvenido al Núcleo IA del LIMS. Ejecute comando o solicite protocolo..."}]
    # Mostramos los últimos mensajes para que no colapse la pantalla
    for msg in st.session_state.messages[-3:]:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Consulta protocolos..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # RESPUESTA IA REACTIVA
        if simular_alerta:
            respuesta = "⚠️ BLOQUEO OPERATIVO: ALERTA TÉRMICA DETECTADA EN SECTOR 7B. Consultas suspendidas. Protocolo de emergencia activado."
        else:
            respuesta = f"Análisis de '{prompt}': Sistemas operativos nominales. Proceso de validación completado con éxito."
        
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"): st.markdown(respuesta)
        #st.rerun() # Eliminamos rerun para evitar doble carga

with col_output:
    st.subheader("🖥️ TERMINAL DE SUBSISTEMAS")
    # Usamos un bloque de código puro para mayor realismo
    terminal_txt = f"""
    [{time.strftime('%H:%M:%S')}] LIMS CORE INITIALIZED... OK
    [{time.strftime('%H:%M:%S')}] IOT SENSOR NETWORK: CONNECTED
    """
    if simular_alerta:
        terminal_txt += f"[{time.strftime('%H:%M:%S')}] ALERT: THERMAL OVERLOAD DETECTED\n"
        terminal_txt += f"[{time.strftime('%H:%M:%S')}] ACTION: EXECUTING SECTOR ISOLATION"
    else:
        terminal_txt += f"[{time.strftime('%H:%M:%S')}] ALL SYSTEMS NOMINAL..."
        
    st.code(terminal_txt, language="bash")


