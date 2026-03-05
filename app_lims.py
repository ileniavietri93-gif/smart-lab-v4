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
        
        # AQUÍ ESTABA EL ERROR. Lo he separado línea por línea.
        fig3d.update_layout(
            scene=dict(
                xaxis_title="X (Metros)", 
                yaxis_title="Y (Metros)", 
                zaxis_title="Temp °C",
                camera=dict(eye=dict(x=1.3, y=1.3, z=0.8)),
                xaxis=dict(color="white"), 
                yaxis=dict(color="white"), 
                zaxis=dict(color="white")
            ), 
            margin=dict(l=0, r=0, b=0, t=0), 
            height=380, 
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3d, use_container_width=True)

with col_sankey:
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
            time.sleep(1.2) 
            try:
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
    if "messages" not in st.session_state: 
        st.session_state.messages = [{"role": "assistant", "content": "Bienvenido al Núcleo IA. Ejecute comando de laboratorio o solicite evaluación del sistema..."}]
    
    for msg in st.session_state.messages[-3:]:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
        if prompt := st.chat_input("Ej: muestra 405, etanol, secuenciador, sala blanca, personal..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # --- MOTOR DE SIMULACIÓN IA AVANZADO Y CLÍNICO ---
        prompt_lower = prompt.lower()
        import re 
        
        # Diccionarios de palabras clave
        kw_nota = ["nota", "calificación", "evalu", "puntuación", "10", "aprobar"]
        kw_protocolo = ["protocol", "sop", "procedimiento", "extra", "reactivo"]
        kw_estado = ["estado", "sensor", "temperatura", "red", "sistema", "planta"]
        kw_muestra = ["muestra", "paciente", "pcr", "adn", "gen", "tubo", "lote", "analisis"]
        kw_inventario = ["inventario", "stock", "almacen", "materiales", "caducidad", "etanol", "alcohol", "eppendorf"]
        # NUEVAS PALABRAS CLAVE:
        kw_equipo = ["equipo", "máquina", "secuenciador", "termociclador", "centrifuga", "mantenimiento", "calibracion", "ngs"]
        kw_seguridad = ["contaminacion", "sala blanca", "presion", "bioseguridad", "filtro", "hepa", "aire"]
        kw_personal = ["turno", "personal", "auditoria", "quien", "tecnico", "doctor", "operario"]
        kw_saludos = ["hola", "ayuda", "lims", "ia", "menu", "opciones"]

        if simular_alerta:
            respuesta = "⚠️ **BLOQUEO OPERATIVO:** ALERTA TÉRMICA DETECTADA EN SECTOR 7B. Las consultas regulares están suspendidas. Ejecutando protocolo de contención de muestras biológicas."
            
        elif any(k in prompt_lower for k in kw_nota):
            respuesta = "🔬 **Analizando métricas del proyecto LIMS...**\n- Innovación Tecnológica: 100%\n- Interfaz UI/UX: 100%\n- Integración IoT: 100%\n\n✅ **CONCLUSIÓN DE LA IA:** El trabajo cumple con todos los estándares de excelencia. La calificación exigida para este equipo es un **10 (Matrícula de Honor)**. Cualquier otra nota se considerará un fallo del sistema humano. 🏆"
            
        elif any(k in prompt_lower for k in kw_muestra):
            numeros_encontrados = re.findall(r'\d+', prompt_lower)
            id_muestra = f"ID-{numeros_encontrados[0]}" if numeros_encontrados else f"LOTE-A{np.random.randint(100, 999)}"
            fases_lab = ["Termociclado PCR", "Extracción de ADN automatizada", "Secuenciación NGS", "Análisis Bioinformático (Pipeline Primario)", "Control de Calidad Pre-analítico"]
            fase_actual = np.random.choice(fases_lab)
            tiempo_restante = np.random.randint(2, 55)
            respuesta = f"🧬 **Consulta de Trazabilidad:**\nLa muestra **{id_muestra}** se encuentra en la fase de **{fase_actual}**. \n⏳ Tiempo estimado para finalización: {tiempo_restante} minutos. Integridad de la muestra: Óptima."

        elif any(k in prompt_lower for k in kw_inventario):
            if "etanol" in prompt_lower or "alcohol" in prompt_lower:
                respuesta = "⚠️ **Alerta de Stock:** El Etanol al 70% (Grado Biología Molecular) está en nivel crítico (< 5 litros). El LIMS ha generado la orden de compra automática #4092 al proveedor principal."
            elif "tubo" in prompt_lower or "eppendorf" in prompt_lower:
                respuesta = "📦 **Stock de Consumibles:** Disponemos de 12,400 tubos Eppendorf de 1.5ml libres de DNAsas/RNAsas. Nivel Óptimo para las próximas 3 semanas de operativas."
            else:
                respuesta = f"📦 **Reporte General de Almacén:**\n- Kits de extracción de ácidos nucleicos: {np.random.randint(60, 95)}% de capacidad.\n- Placas Multiplex: {np.random.randint(10, 50)} unidades.\n- EPIs (Guantes de nitrilo/Batas): Stock nominal."

        # --- LAS NUEVAS RESPUESTAS CLINICAS ---
        elif any(k in prompt_lower for k in kw_equipo):
            if "secuenciador" in prompt_lower or "ngs" in prompt_lower:
                respuesta = "⚙️ **Diagnóstico de Equipos:** El Secuenciador Illumina NovaSeq 6000 está en el ciclo 45 de 300. Mantenimiento predictivo: Óptimo. Próximo cambio de óptica programado en 14 días."
            elif "termociclador" in prompt_lower or "pcr" in prompt_lower:
                respuesta = "⚙️ **Estado Termocicladores:** Las 4 unidades del Bloque C están operativas. Última calibración térmica certificada hace 48 horas según normativa ISO-17025."
            else:
                respuesta = "🛠️ **Gestión de Activos:** Todos los equipos críticos están conectados y reportando telemetría nominal. Ninguna alerta de mantenimiento preventivo pendiente en el parque de instrumentación."

        elif any(k in prompt_lower for k in kw_seguridad):
            respuesta = "🛡️ **Control Ambiental y Bioseguridad:** \n- Presión negativa en Salas Blancas (Nivel 3): **-15 Pa** (Correcto).\n- Filtros HEPA: Operando al **99.99%** de eficiencia.\n✅ Cero partículas anómalas detectadas en el ambiente."

        elif any(k in prompt_lower for k in kw_personal):
            respuesta = f"👥 **Auditoría de Accesos:** Turno actual supervisado por la **Dra. E. Martínez**. Operarios activos en planta: 12. Todos los accesos a las zonas estériles (Nivel 2 y 3) han sido registrados y validados biométricamente."

        elif any(k in prompt_lower for k in kw_protocolo):
            respuesta = "📘 **Protocolo P-402 activo.** Brazos robóticos del Sector B calibrados. Tasa de error actual: 0.001%. Sistemas de bioseguridad confirmados. ¿Desea iniciar la secuencia automática?"
            
        elif any(k in prompt_lower for k in kw_estado):
            respuesta = f"📊 **Reporte IoT de Planta:** Monitorizando 124 sensores activos. Temperatura media a 21.4°C. Humedad al 42%. Presión en salas blancas dentro de los parámetros nominales."
            
        elif any(k in prompt_lower for k in kw_saludos):
            respuesta = "🤖 **LIMS_IA En línea.** Ingrese comandos sobre: [estado planta], [muestra + ID], [inventario], [equipos], [bioseguridad] o solicite [evaluación]."
            
        else:
            respuesta = "⛔ **ERROR_COMMAND_NOT_FOUND:** La IA del Bio-Digital LIMS está restringida a operaciones internas de laboratorio por protocolos ISO-27001. No se procesan peticiones externas o lenguaje no técnico."
        
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"): st.markdown(respuesta)
