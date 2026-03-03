import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN EXTREMA Y DISEÑO LIMPIO ---
st.set_page_config(page_title="Bio-Digital OS v4.0", layout="wide", initial_sidebar_state="expanded")

# CSS Corregido: Textos legibles y contrastes perfectos
st.markdown("""
    <style>
    /* Eliminado el color global que rompía las alertas */
    .stMetric { background-color: #111827; border: 1px solid #1f2937; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stButton>button { border-radius: 5px; background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%); color: white !important; font-weight: bold; border: none; transition: all 0.3s ease; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); border: none; }
    /* Ajuste de consola para que parezca una pantalla de código legible */
    .terminal-box { font-family: 'Courier New', monospace; background-color: #0d1117; padding: 15px; border-radius: 5px; border: 1px solid #30363d; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown("<h1>🧬 BIO-DIGITAL OS <span style='color:#3b82f6; font-size:0.5em;'>CLOUD EDITION</span></h1>", unsafe_allow_html=True)
    st.caption("Panel de Control Inteligente - Grupo 5 | Conectado a Base de Datos Externa")
with c2:
    st.write("<br>", unsafe_allow_html=True)
    csv = "Log del sistema descargado correctamente."
    st.download_button(label="📥 Descargar Log de IA", data=csv, file_name="ai_log.txt", use_container_width=True)

st.divider()

# --- PANEL LATERAL: LOS 5 ROLES ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103322.png", width=60)
    st.markdown("### 🎛️ PANEL DE CONTROL")
    
    genetica = st.button("🧬 Módulo Genética")
    vision = st.button("👁️ Módulo Visión 3D")
    seguridad = st.toggle("🛡️ Encriptación Cuántica")
    roi = st.button("💰 Módulo ROI")
        
    st.markdown("---")
    st.markdown("### ⚠️ OVERRIDE MANUAL")
    simular_alerta = st.toggle("🚨 FALLO DEL SISTEMA (LIMS)")

# --- FILA 1: KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("🧬 Muestras Procesadas", "12,450", delta="Prioridad 1 Activa" if simular_alerta else "+312 hoy")
k2.metric("⚡ Carga IA", "94.2%", delta="Sobrecarga" if simular_alerta else "-2.1%", delta_color="inverse")
k3.metric("🌡️ Estabilidad Térmica", "48°C" if simular_alerta else "21.5°C", delta="+26.5°C" if simular_alerta else "-0.2°C", delta_color="inverse")
k4.metric("🛡️ Integridad Datos", "100%" if seguridad else "82%", delta="Encriptado" if seguridad else "Riesgo Medio")

# --- FILA 2: EFECTO WOW (3D Y SANKEY) ---
col_3d, col_sankey = st.columns(2)

with col_3d:
    st.subheader("🌋 Digital Twin 3D (Termografía)")
    x = np.linspace(-5, 5, 50); y = np.linspace(-5, 5, 50)
    xGrid, yGrid = np.meshgrid(y, x)
    z = np.sin(xGrid) * 0.1 + np.cos(yGrid) * 0.1 + 21
    
    if simular_alerta: z = z + 30 * np.exp(-(xGrid**2 + yGrid**2) / 2) # Volcán de calor
        
    fig3d = go.Figure(data=[go.Surface(z=z, colorscale='Inferno' if simular_alerta else 'Teal', showscale=False)])
    fig3d.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Temp °C', camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))), margin=dict(l=0, r=0, b=0, t=0), height=350, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3d, use_container_width=True)

with col_sankey:
    st.subheader("⛓️ Trazabilidad: Flujo de Muestras")
    if simular_alerta:
        fuentes = [0, 1, 1, 2, 2]; destinos = [1, 2, 4, 4, 3]; valores = [100, 20, 80, 20, 0]
    else:
        fuentes = [0, 1, 2, 3]; destinos = [1, 2, 3, 5]; valores = [100, 95, 90, 85]
        
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=["Recepción", "Extracción", "PCR", "Secuenciadores", "Neveras Emergencia", "IA Diagnóstico"], color=["blue", "blue", "blue", "red" if simular_alerta else "blue", "cyan", "green"]),
        link = dict(source=fuentes, target=destinos, value=valores, color="rgba(100, 150, 250, 0.4)")
    )])
    fig_sankey.update_layout(height=350, margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_sankey, use_container_width=True)

# --- FILA 3: BASE DE DATOS EXTERNA (GOOGLE SHEETS) ---
st.divider()
st.subheader("☁️ Conexión LIMS en la Nube (Google Sheets API)")
st.write("Sincronización en tiempo real con la base de datos externa del hospital.")

col_db, col_chart = st.columns([2, 1])

with col_db:
    if st.button("🔄 Sincronizar Base de Datos Externa"):
        with st.spinner('Conectando a servidor remoto (Google Cloud)...'):
            time.sleep(1) # Simula tiempo de red
            try:
                # AQUÍ ESTÁ TU ENLACE REAL
                url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?output=csv"
                df_nube = pd.read_csv(url_csv)
                
                st.success("✅ Conexión establecida. Tabla sincronizada.")
                st.dataframe(df_nube, use_container_width=True, hide_index=True)
                
                # Gráfica automática basada en tu hoja (Si pusiste la columna 'Urgencia')
                with col_chart:
                    st.write("**Distribución de Muestras en Vivo**")
                    if 'Urgencia' in df_nube.columns:
                        fig_pie = px.pie(df_nube, names='Urgencia', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
                        fig_pie.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("La columna 'Urgencia' no se detectó para el gráfico. Se muestra solo la tabla.")
            except Exception as e:
                st.error(f"⚠️ Error de conexión: {e}")
    else:
        st.info("Base de datos en reposo. Pulsa 'Sincronizar' para extraer los datos en vivo.")

# --- FILA 4: CHATBOT Y TERMINAL DE ALERTAS (LEGILES) ---
st.divider()
col_chat, col_term = st.columns([1, 1])

with col_chat:
    st.subheader("💬 Asistente IA")
    if "mensajes" not in st.session_state: st.session_state.mensajes = [{"role": "assistant", "content": "Sistema LIMS conectado. ¿En qué puedo ayudarte?"}]
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Escribe una consulta..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        respuesta = "⚠️ NO PUEDO PROCESAR. FALLO CRÍTICO." if simular_alerta else f"Análisis de '{prompt}' completado. Todo en orden."
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"): st.markdown(respuesta)

with col_term:
    st.subheader("🖥️ Terminal de Subsistemas")
    # Usamos markdown con HTML para simular una terminal hacker limpia y legible
    if genetica: st.markdown("<div class='terminal-box'>[MÓDULO 1] Análisis Exómico finalizado.<br>Variantes detectadas: 2<br>Cruzando datos: OK</div>", unsafe_allow_html=True)
    elif vision: st.markdown("<div class='terminal-box'>[MÓDULO 2] Segmentación de células activada.<br>Clasificando fenotipos...<br>Precisión: 99.8%</div>", unsafe_allow_html=True)
    elif roi: st.markdown("<div class='terminal-box'>[MÓDULO 4] Calculando TCO...<br>Ahorro energético: 14%<br>Eficiencia: +35%</div>", unsafe_allow_html=True)
    elif simular_alerta: st.error("🚨 [SYS_HALT] ERROR CRÍTICO.\nMotores de secuenciador sobrecalentados.\nDesviando muestras a criogenia.")
    else: st.markdown("<div class='terminal-box'>Sistema a la espera de comandos...<br>Monitorizando sensores IoT...</div>", unsafe_allow_html=True)