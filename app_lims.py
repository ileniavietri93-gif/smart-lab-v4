import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
from PIL import Image

# --- 1. CONFIGURACION Y ESTILOS ---
st.set_page_config(page_title="Bio-Digital OS v5.0", layout="wide", initial_sidebar_state="expanded")

# Inyectamos el CSS correctamente
st.markdown("""
    <style>
    /* 1. FONDO Y TEXTO BASE */
    .main { 
        background-color: #0b0f19; 
        color: #e2e8f0; 
        font-family: 'Courier New', Courier, monospace;
    }

    /* 2. TITULOS PRINCIPALES - Blanco brillante */
    h1, h2, h3, .stSubheader, [data-testid="stHeader"] { 
        color: #ffffff !important; 
        font-family: 'Arial', sans-serif;
        text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.3);
        font-weight: 700 !important;
    }

    /* 3. CAJAS DE LOS KPIs */
    .stMetric { 
        background-color: #111827; 
        border: 1px solid #1f2937; 
        border-left: 4px solid #00ffcc; 
        padding: 15px; 
        border-radius: 5px; 
    }
    
    /* Titulos de las cajas - Cyan neon */
    div[data-testid="stMetricLabel"] p { 
        color: #00ffcc !important; 
        font-size: 1.1em !important; 
        font-weight: 800 !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Numeros de las cajas - Blanco nuclear */
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5); 
    }

    /* 4. TEXTOS SECUNDARIOS */
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








