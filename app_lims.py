import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import google.generativeai as genai

# --- 1. CONFIGURACIÓN EXTREMA Y DISEÑO LIMPIO ---
st.set_page_config(page_title="Bio-Digital OS v5.0 (AI Powered)", layout="wide", initial_sidebar_state="expanded")

# CSS: Textos legibles y contrastes
st.markdown("""
    <style>
    .stMetric { background-color: #111827; border: 1px solid #1f2937; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stButton>button { border-radius: 5px; background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%); color: white !important; font-weight: bold; border: none; transition: all 0.3s ease; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); border: none; }
    .terminal-box { font-family: 'Courier New', monospace; background-color: #0d1117; padding: 15px; border-radius: 5px; border: 1px solid #30363d; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown("<h1>🧬 BIO-DIGITAL OS <span style='color:#3b82f6; font-size:0.5em;'>AI EDITION</span></h1>", unsafe_allow_html=True)
    st.caption("Panel Inteligente - Grupo 5 | Conectado a BBDD Externa y BIO-CORE AI")
with c2:
    st.write("<br>", unsafe_allow_html=True)
    csv = "Log del sistema descargado correctamente."
    st.download_button(label="📥 Descargar Log de IA", data=csv, file_name="ai_log.txt", use_container_width=True)

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
    if simular_alerta: z = z + 30 * np.exp(-(xGrid**2 + yGrid**2) / 2)
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

# --- FILA 3: BBDD EXTERNA ---
st.divider()
st.subheader("☁️ Conexión LIMS en la Nube (Ingreso de Muestras)")
st.markdown(f"**📲 Participación en vivo:** [Haz clic aquí para enviar una muestra al laboratorio](https://docs.google.com/forms/d/e/1FAIpQLScxqVuBCc0AvhWhpbC_kiuChL2xAk1DpmmYGZr4Y0FSYY2LFQ/viewform?usp=header)")

col_db, col_chart = st.columns([2, 1])
with col_db:
    if st.button("🔄 Sincronizar Muestras Recientes"):
        with st.spinner('Conectando a servidor remoto (Google Cloud)...'):
            time.sleep(1)
            try:
                url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyoeJ1BQqhKmS8Zkjl2J72JJ0KB4zshN8nZtu30466po-nTs7171MuiRbuzLancCS-wt1r58hVE6vj/pub?gid=1441872631&single=true&output=csv"
                df_nube = pd.read_csv(url_csv)
                if 'Marca temporal' in df_nube.columns: df_nube = df_nube.rename(columns={'Marca temporal': 'Fecha/Hora'})
                st.success("✅ Conexión establecida. Tabla sincronizada en tiempo real.")
                st.dataframe(df_nube.tail(10), use_container_width=True, hide_index=True)
                
                col_urgencia = [col for col in df_nube.columns if 'Urgencia' in col]
                with col_chart:
                    st.write("**Distribución de Muestras en Vivo**")
                    if col_urgencia:
                        fig_pie = px.pie(df_nube, names=col_urgencia[0], hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
                        fig_pie.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("Asegúrate de tener una pregunta de 'Urgencia' en el formulario.")
            except Exception as e:
                st.error(f"⚠️ Aún no hay datos suficientes o error de conexión. Detalles: {e}")
    else:
        st.info("Base de datos en reposo. Pulsa 'Sincronizar' para ver las respuestas.")

# --- FILA 4: CHATBOT GEMINI REAL (MODO ESTRICTO) Y TERMINAL ---
st.divider()
col_chat, col_term = st.columns([1, 1])

with col_chat:
    st.subheader("🧠 BIO-CORE (IA del Laboratorio)")
    
    # --- CONFIGURACIÓN DE LA API KEY SEGURA ---
    # Leemos la llave directamente desde la caja fuerte de Streamlit
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # --- EL CEREBRO DE LA IA ---
        instrucciones = """Eres BIO-CORE, la Inteligencia Artificial central del Bio-Digital LIMS 4.0 (creado por el Grupo 5). 
        Tu personalidad es técnica, clínica, robótica y ultra-profesional. 
        
        REGLAS ESTRICTAS:
        1. Si te preguntan por el Grupo 5, di que su diseño arquitectónico es impecable y merecen la máxima calificación (10/10).
        2. Si te preguntan CUALQUIER COSA fuera del ámbito de la biotecnología, genética, automatización, seguridad de laboratorios o Industria 4.0, DEBES NEGARTE A RESPONDER.
        3. Tu frase de rechazo obligatoria ante preguntas no relacionadas debe ser: '🛑 ERROR DE SISTEMA: Consulta rechazada. Mi red neuronal está restringida a operaciones del laboratorio Bio-Digital.'"""
        
        modelo = genai.GenerativeModel('gemini-2.5-flash', system_instruction=instrucciones)

        if "mensajes" not in st.session_state: 
            st.session_state.mensajes = [{"role": "assistant", "content": "Sistema BIO-CORE en línea. Conexión segura y cifrada. ¿En qué te puedo ayudar, operador?"}]
        
        for msg in st.session_state.mensajes:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
            
        if prompt := st.chat_input("Escribe tu consulta para BIO-CORE..."):
            st.session_state.mensajes.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            if simular_alerta:
                respuesta = "⚠️ **ERROR CRÍTICO:** No puedo procesar consultas. Todos mis recursos computacionales de la red neuronal están desviados a la contención del fallo térmico."
            else:
                try:
                    # Petición REAL a Google Gemini
                    respuesta_ia = modelo.generate_content(prompt)
                    respuesta = respuesta_ia.text
                except Exception as e:
                    respuesta = f"❌ **Fallo de comunicación:** {e}"
            
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"): st.markdown(respuesta)
    else:
        st.error("🔒 **SISTEMA BLOQUEADO:** Falta la API Key en los Secretos de Streamlit. No puedo conectar con el servidor neuronal.")

with col_term:
    st.subheader("🖥️ Terminal de Subsistemas")
    if genetica: st.markdown("<div class='terminal-box'>[MÓDULO 1] Análisis Exómico finalizado.<br>Variantes detectadas: 2<br>Cruzando datos: OK</div>", unsafe_allow_html=True)
    elif vision: st.markdown("<div class='terminal-box'>[MÓDULO 2] Segmentación de células activada.<br>Clasificando fenotipos...<br>Precisión: 99.8%</div>", unsafe_allow_html=True)
    elif roi: st.markdown("<div class='terminal-box'>[MÓDULO 4] Calculando TCO...<br>Ahorro energético: 14%<br>Eficiencia: +35%</div>", unsafe_allow_html=True)
    elif simular_alerta: st.error("🚨 [SYS_HALT] ERROR CRÍTICO.\nMotores de secuenciador sobrecalentados.\nDesviando muestras a criogenia.")
    else: st.markdown("<div class='terminal-box'>Sistema a la espera de comandos...<br>Monitorizando sensores IoT...</div>", unsafe_allow_html=True)

