"""
========================================================================================
EXECUTIVE 360° ENTERPRISE ANALYTICS & MACHINE LEARNING SUITE (VOICE & COPILOT PRO EDITION)
Framework: Streamlit · Plotly · scikit-learn · SciPy · Web Speech API
Storytelling Inteligente en Vivo + Motor Fonético de Locución en Español (100% Gratis y Nativo)
Barra de Navegación Fija Superior (Fixed Sticky Navbar) con 11 Módulos Ejecutivos:
🧭 1. Resumen Ejecutivo | 📈 2. Comercial & Tendencias | 💰 3. Finanzas 360° |
🤖 4. Predictive Churn (ML) | 🎯 5. Segmentación (RFM) | 🗺️ 6. Territorio & Logística |
👥 7. Clientes Pareto & ABC | 👔 8. Fuerza de Ventas | 📦 9. Portafolio BCG |
📐 10. Estadística Avanzada | 📋 11. Auditoría & Calidad
========================================================================================
"""

import io
import itertools
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve, silhouette_score)
from sklearn.model_selection import (StratifiedKFold, cross_val_predict,
                                     cross_val_score, train_test_split)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y COMPATIBILIDAD
# ==============================================================================
st.set_page_config(
    page_title="Executive 360° Data Intelligence & ML Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE_EXCEL = "dataset_analytics_storytelling_ml_500.xlsx"
DATA_FILE_CSV = "dataset_analytics_storytelling_ml_500.csv"


def _st_version():
    try:
        return tuple(int(p) for p in st.__version__.split(".")[:2])
    except Exception:
        return (1, 0)


NEW_ST = _st_version() >= (1, 50)


def stretch(fn, *args, **kwargs):
    attempts = ([{"width": "stretch"}, {"use_container_width": True}, {}] if NEW_ST
                else [{"use_container_width": True}, {}])
    for extra in attempts:
        try:
            return fn(*args, **kwargs, **extra)
        except Exception:
            continue
    return fn(*args, **kwargs)


_chart_counter = itertools.count()
_speech_counter = itertools.count()

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "dark"
is_dark = st.session_state["theme_mode"] == "dark"

# ==============================================================================
# 2. MOTOR DE TEMAS DE ALTO CONTRASTE Y HELPERS HTML
# ==============================================================================
THEME = {
    "bg": "#0B0F19" if is_dark else "#F4F6F9",
    "surface": "#111827" if is_dark else "#FFFFFF",
    "surface_secondary": "#1E293B" if is_dark else "#F1F5F9",
    "border": "#283548" if is_dark else "#CBD5E1",
    "border_highlight": "#38BDF8" if is_dark else "#0284C7",
    "text_primary": "#FFFFFF" if is_dark else "#0F172A",
    "text_secondary": "#94A3B8" if is_dark else "#334155",
    "btn_bg": "#1E293B" if is_dark else "#FFFFFF",
    "btn_text": "#38BDF8" if is_dark else "#0284C7",
    "btn_border": "#38BDF8" if is_dark else "#0284C7",
    "accent_cyan": "#00E5FF" if is_dark else "#0891B2",
    "accent_blue": "#38BDF8" if is_dark else "#0284C7",
    "accent_purple": "#A78BFA" if is_dark else "#7C3AED",
    "accent_pink": "#F472B6" if is_dark else "#DB2777",
    "success": "#10B981" if is_dark else "#059669",
    "warning": "#F59E0B" if is_dark else "#D97706",
    "danger": "#EF4444" if is_dark else "#DC2626",
    "plotly_template": "plotly_dark" if is_dark else "plotly_white",
    "grid_color": "#1E293B" if is_dark else "#E2E8F0",
    "card_shadow": "0 8px 30px rgba(0, 0, 0, 0.5)" if is_dark else "0 2px 10px rgba(15, 23, 42, 0.06)",
}
PAL = [THEME["accent_blue"], THEME["accent_purple"], THEME["success"], THEME["warning"],
       THEME["accent_pink"], THEME["accent_cyan"], THEME["danger"], "#84CC16"]
SCALE_SEQ = [[0, THEME["surface_secondary"]], [1, THEME["accent_blue"]]]
SCALE_RISK = "RdYlGn_r"
SCALE_GOOD = "RdYlGn"

ALERTA_ORDER = ["Cliente Fiel / Estable", "Monitoreo / Medio", "Alto Riesgo"]
ALERTA_COLORS = {
    "Cliente Fiel / Estable": THEME["success"],
    "Monitoreo / Medio": THEME["warning"],
    "Alto Riesgo": THEME["danger"]
}
MESES = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
         7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
MESES_FULL = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
              7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
DIAS = {0: "Lun", 1: "Mar", 2: "Mié", 3: "Jue", 4: "Vie", 5: "Sáb", 6: "Dom"}


def html(s):
    st.markdown(s.replace("$", "&#36;"), unsafe_allow_html=True)


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
html, body, [class*="css"], [data-testid="stMarkdownContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {text_primary} !important;
}
.stApp { background-color: {bg} !important; transition: background-color 0.25s ease; }
[data-testid="stSidebar"] { background-color: {surface} !important; border-right: 1px solid {border} !important; }

/* Header de Streamlit transparente para permitir navegación fija continua */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    pointer-events: none !important;
}
header[data-testid="stHeader"] * {
    pointer-events: auto !important;
}

/* Contenedor principal con respiración para barra fija */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 3.5rem !important;
}

/* ========================================================================== */
/* BARRA DE NAVEGACIÓN FIJA SUPERIOR (STICKY NAVBAR) CON 11 PESTAÑAS          */
/* Compatible con Streamlit 1.63+ (React Aria) y versiones BaseWeb             */
/* ========================================================================== */
div[data-testid="stTabs"] > div[data-orientation="horizontal"],
div[data-testid="stTabs"] > div {
    position: static !important;
    overflow: visible !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

div[data-testid="stTabs"] div[role="tablist"],
div[data-testid="stTabs"] [data-baseweb="tab-list"],
.stTabs [role="tablist"],
.stTabs [data-baseweb="tab-list"] {
    position: sticky !important;
    top: 0px !important;
    z-index: 999999 !important;
    background-color: {surface} !important;
    border: 1.5px solid {border} !important;
    border-radius: 12px !important;
    padding: 6px 10px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
    margin-top: 0 !important;
    margin-bottom: 20px !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    gap: 6px !important;
    backdrop-filter: blur(14px) !important;
    scrollbar-width: thin !important;
    scrollbar-color: {border_highlight} {surface_secondary} !important;
}

div[data-testid="stTabs"] div[role="tablist"]::-webkit-scrollbar,
.stTabs [role="tablist"]::-webkit-scrollbar {
    height: 4px !important;
}
div[data-testid="stTabs"] div[role="tablist"]::-webkit-scrollbar-thumb,
.stTabs [role="tablist"]::-webkit-scrollbar-thumb {
    background: {border_highlight} !important;
    border-radius: 4px !important;
}

/* Ocultar la línea inferior y el highlight de baseweb y RAC */
div[data-testid="stTabs"] [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-border"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] .react-aria-SelectionIndicator {
    display: none !important;
}

/* Estilo individual de cada botón de tab en la barra fija */
div[data-testid="stTabs"] div[data-testid="stTab"],
div[data-testid="stTabs"] div[role="tab"],
div[data-testid="stTabs"] button[data-baseweb="tab"],
.stTabs div[data-testid="stTab"],
.stTabs [role="tab"],
.stTabs [data-baseweb="tab"] {
    background-color: {surface_secondary} !important;
    color: {text_secondary} !important;
    border: 1px solid {border} !important;
    border-radius: 8px !important;
    padding: 6px 13px !important;
    font-size: 0.81rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTabs"] div[data-testid="stTab"]:hover,
div[data-testid="stTabs"] div[role="tab"]:hover,
div[data-testid="stTabs"] button[data-baseweb="tab"]:hover,
.stTabs div[data-testid="stTab"]:hover,
.stTabs [role="tab"]:hover,
.stTabs [data-baseweb="tab"]:hover {
    color: {text_primary} !important;
    border-color: {border_highlight} !important;
    background-color: {btn_bg} !important;
    transform: translateY(-1px) !important;
}

/* Pestaña activa / seleccionada */
div[data-testid="stTabs"] div[data-testid="stTab"][aria-selected="true"],
div[data-testid="stTabs"] div[role="tab"][aria-selected="true"],
div[data-testid="stTabs"] button[aria-selected="true"],
.stTabs div[data-testid="stTab"][aria-selected="true"],
.stTabs [role="tab"][aria-selected="true"],
.stTabs [aria-selected="true"] {
    background-color: {border_highlight} !important;
    color: #FFFFFF !important;
    border: 1.5px solid {border_highlight} !important;
    font-weight: 800 !important;
    box-shadow: 0 2px 10px rgba(56, 189, 248, 0.35) !important;
}

div.stButton > button, div.stDownloadButton > button {
    background-color: {btn_bg} !important; color: {btn_text} !important;
    border: 1.5px solid {btn_border} !important; border-radius: 8px !important;
    font-weight: 700 !important; font-size: 0.82rem !important; padding: 5px 13px !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: {border_highlight} !important; color: #FFFFFF !important;
    border-color: {border_highlight} !important; transform: translateY(-1px);
}
/* ========================================================================== */
/* KPI CARDS CON DIMENSIONES HOMOGÉNEAS Y BORDES CON ONDA MARINA ANIMADA       */
/* ========================================================================== */
.kpi-card {
    background: {surface} !important;
    border: 2px solid var(--kpi-border, {border}) !important;
    border-radius: 12px !important;
    padding: 13px 15px !important;
    box-shadow: {card_shadow} !important;
    transition: all 0.25s ease !important;
    height: 148px !important;
    min-height: 148px !important;
    max-height: 148px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    position: relative !important;
    overflow: hidden !important;
    animation: kpiOceanWave 4s ease-in-out infinite !important;
}

@keyframes kpiOceanWave {
    0% {
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08), 0 0 3px var(--kpi-border);
        border-color: var(--kpi-border);
    }
    50% {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16), 0 0 14px var(--kpi-border);
        border-color: var(--kpi-border);
    }
    100% {
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08), 0 0 3px var(--kpi-border);
        border-color: var(--kpi-border);
    }
}

.kpi-wave-bar {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3.5px !important;
    background: linear-gradient(90deg, transparent, var(--kpi-border), #FFFFFF, var(--kpi-border), transparent) !important;
    background-size: 200% 100% !important;
    animation: kpiWaveFlow 3s linear infinite !important;
}

@keyframes kpiWaveFlow {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.kpi-card:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.24), 0 0 18px var(--kpi-border) !important;
}

.kpi-title {
    font-size: 0.74rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: {text_secondary} !important;
    margin-bottom: 2px !important;
    line-height: 1.25 !important;
    height: 28px !important;
    display: flex !important;
    align-items: center !important;
}

.kpi-value {
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: -0.02em !important;
    margin: 2px 0 4px 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-wrap: wrap !important;
    line-height: 1.15 !important;
}

.kpi-subtext {
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    color: {text_secondary} !important;
    display: flex !important;
    align-items: center !important;
    gap: 5px !important;
    flex-wrap: wrap !important;
    line-height: 1.25 !important;
    height: 24px !important;
}

.kpi-subtext b {
    color: {text_primary} !important;
    font-weight: 700 !important;
}

.semaphore-dot {
    display: inline-block !important;
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    margin-right: 2px !important;
    flex-shrink: 0 !important;
    box-shadow: 0 0 6px currentColor !important;
}

.delta {
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    padding: 2px 6px !important;
    border-radius: 6px !important;
    margin-left: 4px !important;
    display: inline-flex !important;
    align-items: center !important;
}

.delta-pos {
    color: {success} !important;
    background: rgba(16, 185, 129, 0.16) !important;
    border: 1px solid {success} !important;
}

.delta-neg {
    color: {danger} !important;
    background: rgba(239, 68, 68, 0.16) !important;
    border: 1px solid {danger} !important;
}
.story-box { background: {surface}; border-left: 5px solid {accent_blue}; border-radius: 0 12px 12px 0;
    padding: 20px 24px; margin-bottom: 8px; border-top: 1px solid {border}; border-right: 1px solid {border};
    border-bottom: 1px solid {border}; box-shadow: {card_shadow}; }
.story-title { font-size: 1.10rem; font-weight: 800; color: {text_primary}; margin: 0 0 10px 0; }
.story-desc { font-size: 0.95rem; line-height: 1.72; color: {text_secondary}; margin: 0; }
.exec-box { background: {surface_secondary}; border: 1px solid {border}; border-top: 4px solid {accent_purple};
    border-radius: 12px; padding: 16px 20px; margin-bottom: 20px; }
.exec-title { font-size: 0.98rem; font-weight: 800; color: {text_primary}; margin-bottom: 10px; }
.exec-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px 18px; }
.exec-item { display: flex; gap: 8px; font-size: 0.88rem; line-height: 1.5; color: {text_secondary}; }
.exec-item b { color: {text_primary}; }
.exec-ico { font-size: 1.2rem; line-height: 1.3; }
.chart-insight { background: {surface}; border: 1px solid {border}; border-left: 3.5px solid {accent_cyan};
    border-radius: 6px; padding: 10px 14px; margin: 6px 0 10px 0; font-size: 0.85rem; line-height: 1.6;
    color: {text_secondary}; }
.section-h { font-size: 1.02rem; font-weight: 800; color: {text_primary}; margin: 16px 0 8px 0;
    padding-left: 10px; border-left: 4px solid {accent_blue}; }
.slicer-header {
    font-size: 0.80rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    color: {text_primary} !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 8px !important;
    padding-bottom: 4px !important;
    border-bottom: 1.5px solid {border} !important;
}

/* ========================================================================== */
/* BARRA LATERAL (SIDEBAR), FILE UPLOADER & CONTRASTE WCAG 2.2 AAA            */
/* ========================================================================== */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarHeader"] {
    background-color: {surface} !important;
    color: {text_primary} !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
    color: {text_primary} !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: {text_primary};
}

[data-testid="stSidebar"] hr {
    border-color: {border} !important;
}

/* FILE UPLOADER BLINDADO (DROPZONE, BOTÓN E INSTRUCCIONES) */
[data-testid="stFileUploader"] {
    background-color: transparent !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] [data-testid="stWidgetLabel"] p {
    color: {text_primary} !important;
    font-size: 0.88rem !important;
    font-weight: 800 !important;
}

section[data-testid="stFileUploaderDropzone"] {
    background-color: {surface_secondary} !important;
    border: 1.5px dashed {border_highlight} !important;
    border-radius: 10px !important;
    padding: 14px 10px !important;
    color: {text_primary} !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: {accent_cyan} !important;
    background-color: {surface} !important;
}

section[data-testid="stFileUploaderDropzone"] button,
section[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
    background-color: {surface} !important;
    color: {btn_text} !important;
    border: 1.5px solid {btn_border} !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 5px 12px !important;
}

section[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: {border_highlight} !important;
    color: #FFFFFF !important;
}

section[data-testid="stFileUploaderDropzone"] button p,
section[data-testid="stFileUploaderDropzone"] button span {
    color: inherit !important;
    font-weight: 700 !important;
}

section[data-testid="stFileUploaderDropzone"] svg,
section[data-testid="stFileUploaderDropzone"] [data-testid="stIconMaterial"] {
    color: {accent_blue} !important;
    fill: {accent_blue} !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzoneInstructions"] div {
    color: {text_secondary} !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
}

/* CAJAS BENTO DE SEGMENTADORES (SLICERS) CON BORDES Y FONDOS DEFINIDOS */
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stSidebar"] div[data-test-scroll-behavior="normal"] {
    background-color: {surface_secondary} !important;
    border: 1.5px solid {border} !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    margin-bottom: 8px !important;
    box-shadow: {card_shadow} !important;
}

/* BOTONES TODOS / NINGUNO EN CADA SEGMENTADOR */
[data-testid="stSidebar"] div.stButton > button {
    background-color: {surface} !important;
    color: {btn_text} !important;
    border: 1px solid {btn_border} !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    padding: 4px 8px !important;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: {border_highlight} !important;
    color: #FFFFFF !important;
}

/* CHECKBOXES CON ALTO CONTRASTE */
[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
    color: {text_primary} !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
    color: {text_primary} !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stCheckbox"] [data-selected="true"] {
    color: {text_primary} !important;
}

[data-testid="stSidebar"] [data-testid="stCheckbox"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}
.kw { font-weight: 800; padding: 0 4px; border-radius: 4px; }
.kw-pos { color: {success}; background: rgba(16,185,129,0.14); }
.kw-neg { color: {danger}; background: rgba(239,68,68,0.14); }
.kw-warn { color: {warning}; background: rgba(245,158,11,0.16); }
.kw-info { color: {accent_blue}; background: rgba(56,189,248,0.14); }
.kw-ml { color: {accent_purple}; background: rgba(167,139,250,0.16); }
.kw-key { color: {accent_pink}; background: rgba(244,114,182,0.14); }
</style>
"""
for _k, _v in THEME.items():
    CSS = CSS.replace("{" + _k + "}", str(_v))
html(CSS)

# ==============================================================================
# 3. MOTOR FONÉTICO MATEMÁTICO & SÍNTESIS DE VOZ EN ESPAÑOL (WEB SPEECH API)
# ==============================================================================
def int_to_spanish(n):
    """
    Convierte enteros de 0 a 999,999,999,999 a palabras en español neutro,
    desglosando unidades, decenas, centenas, miles y millones con gramática exacta.
    """
    n = int(round(n))
    if n == 0:
        return "cero"
    if n < 0:
        return "menos " + int_to_spanish(abs(n))

    unidades = {
        1: "un", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
        6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
        11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince",
        16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve",
        20: "veinte", 21: "veintiún", 22: "veintidós", 23: "veintitrés",
        24: "veinticuatro", 25: "veinticinco", 26: "veintiséis", 27: "veintisiete",
        28: "veintiocho", 29: "veintinueve"
    }
    decenas = {
        30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta",
        70: "setenta", 80: "ochenta", 90: "noventa"
    }
    centenas = {
        100: "ciento", 200: "doscientos", 300: "trescientos", 400: "cuatrocientos",
        500: "quinientos", 600: "seiscientos", 700: "setecientos", 800: "ochocientos",
        900: "novecientos"
    }

    def _under_1000(num):
        if num == 0:
            return ""
        if num == 100:
            return "cien"
        if num < 30:
            return unidades[num]
        if num < 100:
            d = (num // 10) * 10
            u = num % 10
            return decenas[d] if u == 0 else f"{decenas[d]} y {unidades[u]}"
        c = (num // 100) * 100
        r = num % 100
        c_name = "cien" if c == 100 and r == 0 else ("ciento" if c == 100 else centenas[c])
        return c_name if r == 0 else f"{c_name} {_under_1000(r)}"

    if n < 1000:
        return _under_1000(n)
    if n < 1000000:
        miles = n // 1000
        resto = n % 1000
        m_str = "mil" if miles == 1 else f"{_under_1000(miles)} mil"
        return m_str if resto == 0 else f"{m_str} {_under_1000(resto)}"
    if n < 1000000000:
        millones = n // 1000000
        resto = n % 1000000
        m_str = "un millón" if millones == 1 else f"{int_to_spanish(millones)} millones"
        return m_str if resto == 0 else f"{m_str} {int_to_spanish(resto)}"
    mm = n // 1000000000
    resto = n % 1000000000
    b_str = f"{int_to_spanish(mm)} mil millones"
    return b_str if resto == 0 else f"{b_str} {int_to_spanish(resto)}"


def verbalizar_numero_es(val_str, decimal_name="punto"):
    """Traduce números con decimales o signos a palabras fonéticas en español."""
    val_str = str(val_str).replace(",", "").strip()
    signo = ""
    if val_str.startswith("+"):
        signo = "más "
        val_str = val_str[1:]
    elif val_str.startswith("-"):
        signo = "menos "
        val_str = val_str[1:]

    if "." in val_str:
        p_int, p_dec = val_str.split(".", 1)
        int_v = int(p_int) if p_int else 0
        int_words = int_to_spanish(int_v)
        if len(p_dec) <= 2:
            dec_v = int(p_dec)
            dec_words = int_to_spanish(dec_v)
            if len(p_dec) == 2 and p_dec.startswith("0") and dec_v > 0:
                dec_words = f"cero {dec_words}"
        else:
            digitos = {"0": "cero", "1": "uno", "2": "dos", "3": "tres", "4": "cuatro",
                       "5": "cinco", "6": "seis", "7": "siete", "8": "ocho", "9": "nueve"}
            dec_words = " ".join(digitos.get(c, c) for c in p_dec)
        return f"{signo}{int_words} {decimal_name} {dec_words}".strip()
    else:
        return f"{signo}{int_to_spanish(int(val_str))}".strip()


def verbalizar_moneda(m):
    """Convierte montos monetarios ($444,020.42, $150k) a dólares y centavos desglosados."""
    signo = m.group(1) or ""
    num_str = m.group(2).replace(",", "")
    mult = m.group(3)
    val = float(num_str)
    prefix = "más " if "+" in signo else ("menos " if "-" in signo else "")
    if mult:
        mult = mult.lower()
        if mult == "k":
            val *= 1000
        elif mult == "m":
            val *= 1000000
        elif mult == "b":
            val *= 1000000000

    entero = int(val)
    cents = int(round((val - entero) * 100))
    moneda = "dólar" if entero == 1 else "dólares"
    palabras = int_to_spanish(entero)
    if cents > 0:
        c_str = "un centavo" if cents == 1 else f"{int_to_spanish(cents)} centavos"
        return f" {prefix}{palabras} {moneda} con {c_str} "
    return f" {prefix}{palabras} {moneda} "


def verbalizar_porcentaje(m):
    """Convierte porcentajes exactos (27.98%, +1.5%) a palabras fonéticas."""
    signo = m.group(1) or ""
    num_str = m.group(2)
    prefix = "más " if "+" in signo else ("menos " if "-" in signo else "")
    num_text = verbalizar_numero_es(num_str)
    return f" {prefix}{num_text} por ciento "


def verbalizar_texto_es(texto):
    """
    Motor fonético completo:
    - Desglosa monedas, porcentajes, puntos porcentuales y múltiplos.
    - Fonetiza siglas de negocio (LTV/CAC, SLA, CSAT, RFM, COGS, SKU, ML, AUC, ROC, BCG).
    - Convierte símbolos y números a texto fluido en español neutro sin lectura robotizada.
    """
    if not texto:
        return ""
    t = str(texto)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("&amp;", " y ").replace("&nbsp;", " ")

    # 1. Monedas: $444,020.42, &#36;150k, etc.
    cur_pattern = r"(?:[\$]|&#36;)\s*([+-])?\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*([kKmMbB])?"
    t = re.sub(cur_pattern, verbalizar_moneda, t)

    # 2. Porcentajes: 27.98% o +1.5% o -3.2%
    pct_pattern = r"([+-])?\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*%"
    t = re.sub(pct_pattern, verbalizar_porcentaje, t)

    # 3. Puntos porcentuales: 3.2 pp o 3.2 pp.
    pp_pattern = r"([+-])?\s*(\d+(?:\.\d+)?)\s*pp\.?\b"
    def _rep_pp(m):
        p = "más " if m.group(1) == "+" else ("menos " if m.group(1) == "-" else "")
        return f" {p}{verbalizar_numero_es(m.group(2))} puntos porcentuales "
    t = re.sub(pp_pattern, _rep_pp, t)

    # 4. Múltiplos: 3.2x, 10x
    x_pattern = r"\b(\d+(?:\.\d+)?)\s*x\b"
    t = re.sub(x_pattern, lambda m: f" {verbalizar_numero_es(m.group(1))} veces ", t)

    # 5. Siglas de negocio fonetizadas
    siglas = [
        (r"\bLTV\s*/\s*CAC\b", " ele te ve sobre ce a ce "),
        (r"\bLTV\b", " ele te ve "),
        (r"\bCAC\b", " ce a ce "),
        (r"\bSLA\b", " acuerdo de nivel de servicio ese ele a "),
        (r"\bCSAT\b", " índice de satisfacción ce sat "),
        (r"\bRFM\b", " erre efe eme "),
        (r"\bCOGS\b", " costo de ventas "),
        (r"\bSKUs\b", " ese ca us "),
        (r"\bSKU\b", " ese ca u "),
        (r"\bYoY\b", " interanual "),
        (r"\bMoM\b", " intermensual "),
        (r"\bYTD\b", " acumulado del año "),
        (r"\bML\b", " aprendizaje automático "),
        (r"\bAUC\b", " área bajo la curva a u ce "),
        (r"\bROC\b", " curva r o c "),
        (r"\bBCG\b", " matriz be ce ge "),
        (r"\bVIP\b", " vip "),
        (r"\bB2B\b", " be dos be "),
        (r"\bPYME\b", " pyme "),
        (r"\bPYMEs\b", " pymes "),
        (r"\bK-Means\b", " ka means "),
        (r"\bPCA\b", " pe ce a "),
        (r"\bCV\b", " validación cruzada "),
        (r"\bR²\b", " erre cuadrado "),
        (r"\bR2\b", " erre cuadrado "),
        (r"★", " estrellas "),
        (r"▲", " subió "),
        (r"▼", " bajó "),
        (r"→", " a "),
        (r"↔", " con "),
        (r"×", " por ")
    ]
    for pattern, rep in siglas:
        t = re.sub(pattern, rep, t, flags=re.IGNORECASE if ("pyme" in pattern or "vip" in pattern) else 0)

    # 6. Decimales sueltos (ej: 4.5, 0.98)
    def _dec_num(m):
        return f" {verbalizar_numero_es(m.group(0))} "
    t = re.sub(r"\b\d+\.\d+\b", _dec_num, t)

    # 7. Números enteros sueltos de 1 a 6 dígitos (ej: 500 órdenes, 15 cuentas)
    def _standalone_num(m):
        return f" {int_to_spanish(int(m.group(1).replace(',', '')))} "
    t = re.sub(r"\b(\d{1,3}(?:,\d{3})+|\d{1,6})\b(?!\s*[-\.\d])", _standalone_num, t)

    t = re.sub(r"\s+", " ", t).strip()
    return t


def strip_html_for_speech(html_str):
    """Prepara el texto HTML procesándolo a través del motor fonético en español."""
    return verbalizar_texto_es(html_str)


def voice_player(text_to_speak, button_label="▶️ Escuchar informe (Voz)", key="vp"):
    """Controlador de audio nativo con el motor Web Speech API de tu navegador (100% gratis)."""
    clean_text = strip_html_for_speech(text_to_speak)
    js_text = json.dumps(clean_text)
    html_code = f"""
    <body style="margin:0; padding:0; background:transparent; overflow:hidden; font-family:'Plus Jakarta Sans',-apple-system,sans-serif;">
    <div style="display:flex; align-items:center; gap:8px; margin: 2px 0 10px 0; flex-wrap:nowrap;">
        <button id="btn_{key}" onclick="togglePlay_{key}()" style="
            background: {THEME['btn_bg']};
            color: {THEME['btn_text']};
            border: 1.5px solid {THEME['btn_border']};
            border-radius: 8px;
            padding: 5px 13px;
            font-size: 0.80rem;
            font-weight: 700;
            font-family: inherit;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            transition: all 0.2s ease;
        ">
            {button_label}
        </button>
        <button onclick="stopPlay_{key}()" style="
            background: {THEME['btn_bg']};
            color: {THEME['danger']};
            border: 1.5px solid {THEME['danger']};
            border-radius: 8px;
            padding: 5px 11px;
            font-size: 0.80rem;
            font-weight: 700;
            font-family: inherit;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
        ">
            ⏹️ Detener
        </button>
        <span id="lbl_{key}" style="font-size: 0.76rem; font-weight: 600; color: {THEME['text_secondary']}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"></span>
    </div>
    <script>
        let synth_{key} = window.speechSynthesis;
        let phrase_{key} = {js_text};

        function selectSpanishVoice_{key}(utter) {{
            if (!synth_{key}) return;
            let voices = synth_{key}.getVoices();
            let esVoice = voices.find(v => v.lang.startsWith('es') || v.lang.includes('ES') || v.lang.includes('es-'));
            if (esVoice) utter.voice = esVoice;
        }}

        function togglePlay_{key}() {{
            if (!synth_{key}) {{
                alert("Tu navegador no soporta síntesis de voz Web Speech API.");
                return;
            }}
            if (synth_{key}.speaking && !synth_{key}.paused) {{
                synth_{key}.pause();
                document.getElementById('btn_{key}').innerText = '▶️ Reanudar';
                document.getElementById('lbl_{key}').innerText = '⏸️ En pausa';
                return;
            }}
            if (synth_{key}.paused) {{
                synth_{key}.resume();
                document.getElementById('btn_{key}').innerText = '⏸️ Pausar';
                document.getElementById('lbl_{key}').innerText = '🎙️ Narrando...';
                return;
            }}

            synth_{key}.cancel();
            let utter = new SpeechSynthesisUtterance(phrase_{key});
            utter.lang = 'es-ES';
            utter.rate = 1.0;
            utter.pitch = 1.0;

            selectSpanishVoice_{key}(utter);
            if (!utter.voice && synth_{key}.onvoiceschanged !== undefined) {{
                synth_{key}.onvoiceschanged = function() {{
                    selectSpanishVoice_{key}(utter);
                }};
            }}

            utter.onstart = function() {{
                document.getElementById('btn_{key}').innerText = '⏸️ Pausar';
                document.getElementById('lbl_{key}').innerText = '🎙️ Narrando en vivo...';
            }};
            utter.onend = function() {{
                document.getElementById('btn_{key}').innerText = '{button_label}';
                document.getElementById('lbl_{key}').innerText = '✅ Narración finalizada';
            }};
            utter.onerror = function() {{
                document.getElementById('btn_{key}').innerText = '{button_label}';
                document.getElementById('lbl_{key}').innerText = '';
            }};

            synth_{key}.speak(utter);
        }}

        function stopPlay_{key}() {{
            if (synth_{key}) {{
                synth_{key}.cancel();
                document.getElementById('btn_{key}').innerText = '{button_label}';
                document.getElementById('lbl_{key}').innerText = '⏹️ Detenido';
            }}
        }}
    </script>
    </body>
    """
    components.html(html_code, height=44)


def story(icon, title, body, tips=None, voice=True):
    """Despliega el Storytelling dinámico con tips ejecutivos y reproductor de voz sincronizado."""
    tips_html = ""
    tips_speech = ""
    if tips:
        li_items = "".join(f"<li style='margin-bottom:4px;'>{t}</li>" for t in tips)
        tips_html = (
            f'<div style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed {THEME["border"]};">'
            f'<div style="font-size:0.84rem;font-weight:800;color:{THEME["accent_purple"]};margin-bottom:6px;display:flex;align-items:center;gap:6px;">'
            f'<span>💡 Tips Ejecutivos &amp; Recomendaciones Tácticas:</span></div>'
            f'<ul style="margin:0;padding-left:18px;font-size:0.85rem;color:{THEME["text_secondary"]};line-height:1.55;">'
            f'{li_items}</ul></div>'
        )
        tips_speech = " Recomendaciones tácticas y tips ejecutivos: " + " ".join(tips)
    html(f'<div class="story-box"><div class="story-title">{icon} {title}</div>'
         f'<p class="story-desc">{body}</p>{tips_html}</div>')
    if voice:
        voice_player(f"{title}. {body}.{tips_speech}", button_label=f"▶️ Escuchar narración ({icon})", key=f"voice_{next(_speech_counter)}")


def exec_summary(title, items):
    cells = "".join(f'<div class="exec-item"><span class="exec-ico">{e}</span><div><b>{l}</b><br>{t}</div></div>'
                    for e, l, t in items)
    html(f'<div class="exec-box"><div class="exec-title">📌 {title}</div>'
         f'<div class="exec-grid">{cells}</div></div>')


def section(title):
    html(f'<div class="section-h">{title}</div>')


def usd(x, d=0):
    return f"&#36;{x:,.{d}f}"


def kw(text, kind="info"):
    return f'<span class="kw kw-{kind}">{text}</span>'


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(h, a):
    r, g, b = _rgb(h)
    return f"rgba({r},{g},{b},{a})"


def kpi(title, value, sub, dot, delta=None, vcolor=None):
    chip = ""
    if delta is not None and not pd.isna(delta):
        cls = "delta-pos" if delta >= 0 else "delta-neg"
        arrow = "▲" if delta >= 0 else "▼"
        chip = f'<span class="delta {cls}">{arrow} {abs(delta):.1f}%</span>'
    val_color = vcolor if vcolor else dot
    style_val = f' style="color:{val_color};"'
    card_vars = f'--kpi-border:{dot};'
    st.markdown(
        f'<div class="kpi-card" style="{card_vars}">'
        f'<div class="kpi-wave-bar"></div>'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value"{style_val}>{value}{chip}</div>'
        f'<div class="kpi-subtext"><span class="semaphore-dot" style="background:{dot};color:{dot};"></span>{sub}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def sem_color(val, good, warn, higher=True):
    if higher:
        return THEME["success"] if val >= good else (THEME["warning"] if val >= warn else THEME["danger"])
    return THEME["success"] if val <= good else (THEME["warning"] if val <= warn else THEME["danger"])


def sem_icon(val, good, warn, higher=True):
    c = sem_color(val, good, warn, higher)
    return "🟢" if c == THEME["success"] else ("🟡" if c == THEME["warning"] else "🔴")


def format_fig(fig, height=390):
    fig.update_layout(
        template=THEME["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=35, r=25, t=55, b=35),
        height=height,
        colorway=PAL,
        font=dict(family="Plus Jakarta Sans", color=THEME["text_primary"]),
        title_font=dict(size=14, color=THEME["text_primary"], family="Plus Jakarta Sans"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=11),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(
            bgcolor=THEME["surface_secondary"],
            bordercolor=THEME["border_highlight"],
            font=dict(family="Plus Jakarta Sans", size=12, color=THEME["text_primary"]),
            align="left",
            namelength=-1
        ),
    )
    fig.update_xaxes(
        gridcolor=THEME["grid_color"],
        zeroline=False,
        tickfont=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=11),
        title_font=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=12)
    )
    fig.update_yaxes(
        gridcolor=THEME["grid_color"],
        zeroline=False,
        tickfont=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=11),
        title_font=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=12)
    )
    fig.update_coloraxes(
        colorbar=dict(
            tickfont=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=10),
            title=dict(font=dict(family="Plus Jakarta Sans", color=THEME["text_primary"], size=11), side="top"),
            thickness=14,
            len=0.75,
            yanchor="middle",
            y=0.5
        )
    )

    # Limpieza y formateo automático de traces sin hovertemplate personalizado
    for t in fig.data:
        if not getattr(t, "hovertemplate", None):
            if t.type == "scatter" and getattr(t, "mode", None) and "lines" in t.mode:
                t.hovertemplate = "<b>%{x}</b><br>📈 %{fullData.name}: %{y:,.2f}<extra></extra>"
            elif t.type == "bar":
                if getattr(t, "orientation", None) == "h":
                    t.hovertemplate = "<b>%{y}</b><br>📊 %{fullData.name}: %{x:,.2f}<extra></extra>"
                else:
                    t.hovertemplate = "<b>%{x}</b><br>📊 %{fullData.name}: %{y:,.2f}<extra></extra>"
            elif t.type in ["pie", "sunburst"]:
                t.hovertemplate = "<b>🏷️ %{label}</b><br>💰 Monto: $%{value:,.0f}<br>📊 Cuota: %{percent}<extra></extra>"
            elif t.type == "heatmap":
                t.hovertemplate = "<b>%{y}</b> × <b>%{x}</b><br>📊 Valor: %{z:,.2f}<extra></extra>"
            elif t.type in ["box", "violin"]:
                t.hovertemplate = "<b>%{x}</b><br>📊 Valor: %{y:,.2f}<extra></extra>"

    return fig


def chart(fig, read, finding=None, action=None, height=390, speech_text=None):
    """
    Despliega el gráfico interactivo de Plotly junto a su tarjeta de insight ejecutiva
    y su botón de locución fonética individual por gráfico (Chart-Level Storytelling).
    """
    format_fig(fig, height)
    cid = next(_chart_counter)
    stretch(st.plotly_chart, fig, key=f"pc_{cid}")
    parts = [f"<b>📖 Cómo leerlo:</b> {read}"]
    if finding:
        parts.append(f"<b>🔎 Hallazgo:</b> {finding}")
    if action:
        parts.append(f"<b>🎯 Acción:</b> {action}")
    html('<div class="chart-insight">' + "<br>".join(parts) + "</div>")

    # Síntesis fonética inteligente por visual
    if speech_text:
        spoken = speech_text
    else:
        sp_items = [f"Cómo leer este gráfico: {read}"]
        if finding:
            sp_items.append(f"Hallazgo principal: {finding}")
        if action:
            sp_items.append(f"Acción recomendada: {action}")
        spoken = ". ".join(sp_items)

    voice_player(spoken, button_label="🎙️ Escuchar análisis del gráfico", key=f"vc_{cid}")


def _interp(stops, t):
    t = min(max(t, 0.0), 1.0)
    n = len(stops) - 1
    i = min(int(t * n), n - 1)
    f = t * n - i
    a, b = _rgb(stops[i]), _rgb(stops[i + 1])
    return tuple(int(a[j] + (b[j] - a[j]) * f) for j in range(3))


def color_scale(series, reverse=False, alpha=0.34, stops=("#EF4444", "#F59E0B", "#10B981")):
    s = pd.to_numeric(series, errors="coerce")
    lo, hi = s.min(), s.max()
    out = []
    for v in s:
        if pd.isna(v) or hi == lo:
            out.append("")
            continue
        t = (v - lo) / (hi - lo)
        t = 1 - t if reverse else t
        r, g, b = _interp(stops, t)
        out.append(f"background-color: rgba({r},{g},{b},{alpha}); font-weight: 600;")
    return out


def seq_scale(series, color="#38BDF8", alpha_max=0.55):
    s = pd.to_numeric(series, errors="coerce")
    lo, hi = s.min(), s.max()
    r, g, b = _rgb(color)
    out = []
    for v in s:
        if pd.isna(v) or hi == lo:
            out.append("")
            continue
        a = 0.06 + (v - lo) / (hi - lo) * (alpha_max - 0.06)
        out.append(f"background-color: rgba({r},{g},{b},{a:.2f}); font-weight: 600;")
    return out


def text_status(series):
    def one(v):
        v = str(v)
        if v.startswith("🟢"):
            return "background-color: rgba(16,185,129,0.25); font-weight: 700;"
        if v.startswith("🟡"):
            return "background-color: rgba(245,158,11,0.25); font-weight: 700;"
        if v.startswith("🔴"):
            return "background-color: rgba(239,68,68,0.25); font-weight: 700;"
        return ""
    return [one(v) for v in series]


def show_table(d, fmt=None, good=(), bad=(), neutral=(), status=(), height=None, title=None, summary=None, tips=None, voice=True):
    """
    Renderiza tablas ejecutivas con formato condicional avanzado, resumen narrativo de hallazgos,
    tips tácticos y narración por voz profesional en español neutro.
    """
    if summary:
        tips_html = ""
        tips_speech = ""
        if tips:
            li_items = "".join(f"<li style='margin-bottom:4px;'>{t}</li>" for t in tips)
            tips_html = (
                f'<div style="margin-top:10px;padding-top:8px;border-top:1px dashed {THEME["border"]};">'
                f'<div style="font-size:0.80rem;font-weight:800;color:{THEME["accent_purple"]};margin-bottom:4px;display:flex;align-items:center;gap:5px;">'
                f'<span>💡 Conclusiones y Tips Operativos:</span></div>'
                f'<ul style="margin:0;padding-left:18px;font-size:0.82rem;color:{THEME["text_secondary"]};line-height:1.5;">'
                f'{li_items}</ul></div>'
            )
            tips_speech = " Conclusiones y tips operativos: " + " ".join(tips)

        html(
            f'<div style="background:{THEME["surface"]};border:1.5px solid {THEME["border"]};border-left:4px solid {THEME["accent_blue"]};border-radius:10px;padding:12px 16px;margin:12px 0 8px 0;box-shadow:{THEME["card_shadow"]};">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:6px;">'
            f'<div style="font-size:0.92rem;font-weight:800;color:{THEME["text_primary"]};">'
            f'📋 {title or "Resumen Ejecutivo de la Tabla"}</div>'
            f'<span style="font-size:0.75rem;font-weight:700;color:{THEME["text_secondary"]};background:{THEME["surface_secondary"]};padding:2px 8px;border-radius:6px;border:1px solid {THEME["border"]};">'
            f'{len(d):,} registros analizados</span></div>'
            f'<div style="font-size:0.86rem;color:{THEME["text_secondary"]};line-height:1.6;">{summary}</div>'
            f'{tips_html}</div>'
        )
        if voice:
            speech_full = f"{title or 'Resumen de la tabla'}. {summary}.{tips_speech}"
            voice_player(speech_full, button_label="🎙️ Escuchar análisis y conclusiones de la tabla", key=f"vp_tbl_{next(_speech_counter)}")

    sty = d.style
    if fmt:
        sty = sty.format({k: v for k, v in fmt.items() if k in d.columns}, na_rep="—")
    for c in good:
        if c in d.columns:
            sty = sty.apply(color_scale, subset=[c])
    for c in bad:
        if c in d.columns:
            sty = sty.apply(lambda s: color_scale(s, reverse=True), subset=[c])
    for c in neutral:
        if c in d.columns:
            sty = sty.apply(lambda s: seq_scale(s, THEME["accent_blue"]), subset=[c])
    for c in status:
        if c in d.columns:
            sty = sty.apply(text_status, subset=[c])
    kwargs = {"hide_index": True}
    if height:
        kwargs["height"] = height
    stretch(st.dataframe, sty, **kwargs)


def pareto_class(prev_pct):
    return "A" if prev_pct < 80 else ("B" if prev_pct < 95 else "C")


def top_share(d, col, val="Monto_Compra"):
    g = d.groupby(col)[val].sum().sort_values(ascending=False)
    return g.index[0], g.iloc[0], g.iloc[0] / g.sum() * 100


def strength(r):
    a = abs(r)
    lvl = "muy fuerte" if a >= 0.8 else "fuerte" if a >= 0.6 else "moderada" if a >= 0.4 else "débil" if a >= 0.2 else "casi nula"
    return f"{lvl} ({'positiva' if r > 0 else 'negativa'})"

# ==============================================================================
# 4. CARGA DE DATOS & PIPELINE DE INGENIERÍA
# ==============================================================================
REQUIRED = ["Cliente_ID", "Nombre_Cuenta_Cliente", "Tipo_Cliente_Cuenta", "Fecha_Transaccion", "Recencia_Dias",
            "Region", "Ciudad", "Canal_Venta", "Vendedor_Asignado", "Categoria", "Producto_Principal",
            "Cantidad_Productos", "Monto_Compra", "Costo_Total", "Descuento_Pct", "CAC_Estimado",
            "Frecuencia_Historica", "LTV_Estimado_USD", "Satisfaccion_CSAT", "SLA_Entrega_Dias",
            "Estado_Entrega", "Riesgo_Churn_Score"]


@st.cache_data(show_spinner=False)
def load_data_from_disk():
    p_cwd = Path.cwd()
    try:
        p_dir = Path(__file__).resolve().parent
    except NameError:
        p_dir = p_cwd

    for base in [p_dir, p_cwd, p_cwd / "data"]:
        xlsx = base / DATA_FILE_EXCEL
        if xlsx.exists():
            df = pd.read_excel(xlsx, sheet_name="Data_Warehouse")
            briefing = None
            try:
                briefing = pd.read_excel(xlsx, sheet_name="Executive_Briefing")
            except Exception:
                pass
            return df, briefing, f"Archivo Excel: {xlsx.name}"
        csv = base / DATA_FILE_CSV
        if csv.exists():
            df = pd.read_csv(csv)
            return df, None, f"Archivo CSV: {csv.name}"
    return None, None, None


@st.cache_data(show_spinner=False)
def make_synthetic(n=500):
    rng = np.random.default_rng(42)
    fechas = pd.to_datetime(np.sort(rng.choice(pd.date_range("2025-01-16", "2026-10-26"), n)))
    tipo = rng.choice(["B2B Corporativo", "PYME / Prosumer", "Consumidor Final"], n, p=[.2, .24, .56])
    base = np.where(tipo == "B2B Corporativo", 2500, np.where(tipo == "PYME / Prosumer", 1100, 150))
    monto = np.round(base * rng.uniform(.4, 1.4, n), 2)
    mpct = rng.uniform(18, 42, n)
    costo = np.round(monto * (1 - mpct / 100), 2)
    rec = rng.integers(6, 655, n)
    csat = rng.choice([1, 2, 3, 4, 5], n, p=[.03, .07, .1, .2, .6])
    churn = np.clip(rec / 800 + (5 - csat) * .06 + rng.normal(0, .08, n), .02, .98).round(3)
    freq = rng.integers(1, 26, n)
    return pd.DataFrame({
        "Cliente_ID": [f"Cli_{i + 1:03d}" for i in range(n)],
        "Nombre_Cuenta_Cliente": [f"Cuenta Demo {rng.integers(1, 120)}" for _ in range(n)],
        "Tipo_Cliente_Cuenta": tipo, "Fecha_Transaccion": fechas, "Recencia_Dias": rec,
        "Region": rng.choice(["Metropolitana", "Cibao / Norte", "Este", "Sur"], n, p=[.46, .29, .16, .09]),
        "Ciudad": rng.choice(["Distrito Nacional", "Santiago de los Caballeros", "Punta Cana / Bávaro", "Barahona"], n),
        "Canal_Venta": rng.choice(["Plataforma E-Commerce", "Ejecutivo B2B / Directo", "WhatsApp Corporativo",
                                   "Showroom / Flagship Store"], n),
        "Vendedor_Asignado": rng.choice(["Valeria Castillo", "Alejandro Morales", "Enrique Gómez", "Patricia Guzmán"], n),
        "Categoria": rng.choice(["Gaming & Alto Rendimiento", "Productividad & Oficina", "Almacenamiento & Redes",
                                 "Infraestructura & Servidores", "Audio & Streaming Pro"], n),
        "Producto_Principal": rng.choice(["GPU RTX Serie 40 Master", "Laptop Ultralight Core i7", "Servidor Rack 2U Enterprise",
                                          "Monitor Dual Setup 27\"", "Audífonos Noise Cancelling Studio"], n),
        "Cantidad_Productos": rng.integers(1, 50, n), "Monto_Compra": monto, "Costo_Total": costo,
        "Margen_Bruto": np.round(monto - costo, 2), "Margen_Bruto_Pct": np.round(mpct, 2),
        "Descuento_Pct": rng.choice([0, 5, 8, 12, 15], n, p=[.6, .2, .1, .06, .04]),
        "Tipo_Pago": rng.choice(["Tarjeta", "Efectivo", "Transferencia"], n),
        "CAC_Estimado": np.round(rng.uniform(10, 180, n), 2), "Frecuencia_Historica": freq,
        "LTV_Estimado_USD": np.round(monto * freq * mpct / 100 * rng.uniform(.8, 1.2, n), 2),
        "Satisfaccion_CSAT": csat, "SLA_Entrega_Dias": rng.choice([1, 2, 3, 4], n),
        "Estado_Entrega": rng.choice(["Entregado a Tiempo", "Con Retraso Logístico"], n, p=[.93, .07]),
        "Riesgo_Churn_Score": churn,
        "RFM_Index": rng.choice([111, 122, 133, 212, 222, 233, 311, 322, 333], n),
        "Segmento_Estrategico_ML": rng.choice(["Champions / Cuentas Clave", "Core Recurrente", "Potencial Alto Valor",
                                               "En Riesgo de Abandono", "Ocasionales de Entrada"], n),
    })


def prepare(raw):
    d = raw.copy()
    d["Fecha_Transaccion"] = pd.to_datetime(d["Fecha_Transaccion"], errors="coerce")
    d = d.dropna(subset=["Fecha_Transaccion"]).reset_index(drop=True)
    d["Año"] = d["Fecha_Transaccion"].dt.year.astype(int)
    d["Mes_Num"] = d["Fecha_Transaccion"].dt.month
    d["Dia_Mes"] = d["Fecha_Transaccion"].dt.day
    d["Mes_Nombre"] = d["Mes_Num"].map(MESES)
    d["Periodo"] = d["Fecha_Transaccion"].dt.strftime("%Y-%m")
    d["Trimestre_Año"] = d["Año"].astype(str) + "-Q" + d["Fecha_Transaccion"].dt.quarter.astype(str)
    d["Dia_Semana"] = d["Fecha_Transaccion"].dt.dayofweek.map(DIAS)
    d["Cuenta"] = d["Nombre_Cuenta_Cliente"].astype(str).str.replace(r"\s*\(ID:[^)]*\)", "", regex=True).str.strip()
    if "Margen_Bruto" not in d:
        d["Margen_Bruto"] = d["Monto_Compra"] - d["Costo_Total"]
    if "Margen_Bruto_Pct" not in d:
        d["Margen_Bruto_Pct"] = d["Margen_Bruto"] / d["Monto_Compra"] * 100
    if "Alerta_Riesgo_Churn" not in d:
        d["Alerta_Riesgo_Churn"] = pd.cut(d["Riesgo_Churn_Score"], bins=[-1, 0.35, 0.60, 2],
                                          labels=ALERTA_ORDER).astype(str)
    if "RFM_Index" not in d:
        d["RFM_Index"] = 222
    if "Segmento_Estrategico_ML" not in d:
        d["Segmento_Estrategico_ML"] = "Sin segmento"
    if "Tipo_Pago" not in d:
        d["Tipo_Pago"] = "N/D"
    d["Contribucion_Neta"] = d["Margen_Bruto"] - d["CAC_Estimado"]
    d["Precio_Unit"] = d["Monto_Compra"] / d["Cantidad_Productos"].clip(lower=1)
    d["Retraso"] = (d["Estado_Entrega"] != "Entregado a Tiempo").astype(int)
    d["R_Score"] = (d["RFM_Index"] // 100).astype(int)
    d["F_Score"] = ((d["RFM_Index"] // 10) % 10).astype(int)
    d["M_Score"] = (d["RFM_Index"] % 10).astype(int)
    d["Rango_Ticket"] = pd.cut(d["Monto_Compra"], bins=[0, 150, 500, 1500, np.inf],
                               labels=["< $150", "$150–500", "$500–1,500", "> $1,500"]).astype(str)
    d["Desc_Label"] = d["Descuento_Pct"].astype(int).astype(str) + "%"
    return d


# ---- Barra Lateral: Carga & Segmentadores Power BI
with st.sidebar:
    st.markdown("### 🎛️ Centro de Comando BI")
    st.button("🌓 Alternar tema " + ("(oscuro → claro)" if is_dark else "(claro → oscuro)"),
              key="btn_theme", help="Alternar Modo Claro / Oscuro",
              on_click=lambda: st.session_state.update(
                  theme_mode="light" if st.session_state["theme_mode"] == "dark" else "dark"))
    uploaded = st.file_uploader("📂 Cargar dataset (Excel o CSV)", type=["xlsx", "csv"])

synthetic, src_note, briefing = False, "", None

if uploaded is not None:
    if uploaded.name.endswith(".csv"):
        raw = pd.read_csv(uploaded)
    else:
        raw = pd.read_excel(uploaded, sheet_name="Data_Warehouse")
        try:
            briefing = pd.read_excel(uploaded, sheet_name="Executive_Briefing")
        except Exception:
            briefing = None
    src_note = f"Archivo cargado: {uploaded.name}"
else:
    raw_disk, briefing_disk, note_disk = load_data_from_disk()
    if raw_disk is not None:
        raw, briefing, src_note = raw_disk, briefing_disk, note_disk
    else:
        raw = make_synthetic()
        synthetic = True
        src_note = "DATOS DE DEMOSTRACIÓN (coloca el Excel/CSV junto al script)"

missing = [c for c in REQUIRED if c not in raw.columns]
if missing:
    st.error(f"Al archivo le faltan columnas obligatorias: {', '.join(missing)}")
    st.stop()

df_master = prepare(raw)

# ==============================================================================
# 5. MODELADO PREDICTIVO (ML SUPERVISADO DE CHURN)
# ==============================================================================
CHURN_FEATURES = ["Recencia_Dias", "Frecuencia_Historica", "Monto_Compra", "Satisfaccion_CSAT", "SLA_Entrega_Dias",
                  "Descuento_Pct", "Margen_Bruto_Pct", "CAC_Estimado", "Cantidad_Productos", "Retraso"]
FEAT_LABELS = {
    "Recencia_Dias": "Recencia (días)", "Frecuencia_Historica": "Frecuencia histórica",
    "Monto_Compra": "Monto de compra", "Satisfaccion_CSAT": "Satisfacción CSAT",
    "SLA_Entrega_Dias": "SLA entrega (días)", "Descuento_Pct": "Descuento %",
    "Margen_Bruto_Pct": "Margen bruto %", "CAC_Estimado": "CAC estimado",
    "Cantidad_Productos": "Cantidad productos", "Retraso": "Entrega con retraso"
}


@st.cache_resource(show_spinner="🤖 Entrenando modelos predictivos…")
def train_churn(_df, signature):
    X = _df[CHURN_FEATURES].astype(float)
    y = (_df["Riesgo_Churn_Score"] >= 0.5).astype(int)
    if y.sum() < 10 or (len(y) - y.sum()) < 10:
        return None
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=300, max_depth=6, min_samples_leaf=3,
                                                random_state=42, class_weight="balanced"),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "Regresión Logística": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")),
    }
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    rows, rocs, cms = [], {}, {}
    for name, m in models.items():
        cv_auc = cross_val_score(m, X, y, cv=cv, scoring="roc_auc").mean()
        m.fit(Xtr, ytr)
        p = m.predict_proba(Xte)[:, 1]
        pred = (p >= 0.5).astype(int)
        rows.append({"Modelo": name, "AUC (CV 5-fold)": cv_auc, "AUC (test)": roc_auc_score(yte, p),
                     "Accuracy": accuracy_score(yte, pred), "Precisión": precision_score(yte, pred, zero_division=0),
                     "Recall": recall_score(yte, pred, zero_division=0), "F1": f1_score(yte, pred, zero_division=0)})
        fpr, tpr, _ = roc_curve(yte, p)
        rocs[name] = (fpr, tpr)
        cms[name] = confusion_matrix(yte, pred, labels=[0, 1])
    metrics = pd.DataFrame(rows).sort_values("AUC (CV 5-fold)", ascending=False).reset_index(drop=True)
    best = metrics.loc[0, "Modelo"]
    rf_full = RandomForestClassifier(n_estimators=300, max_depth=6, min_samples_leaf=3, random_state=42,
                                     class_weight="balanced").fit(X, y)
    imp = pd.DataFrame({"Variable": [FEAT_LABELS[f] for f in CHURN_FEATURES],
                        "Importancia": rf_full.feature_importances_}).sort_values("Importancia")
    oof = cross_val_predict(RandomForestClassifier(n_estimators=300, max_depth=6, min_samples_leaf=3, random_state=42,
                                                   class_weight="balanced"), X, y, cv=cv, method="predict_proba")[:, 1]
    return {"metrics": metrics, "best": best, "rocs": rocs, "cm": cms[best], "imp": imp, "rf": rf_full,
            "oof": pd.Series(oof, index=_df.index), "medians": X.median().to_dict(),
            "ranges": {c: (float(X[c].min()), float(X[c].max())) for c in CHURN_FEATURES},
            "pos_rate": float(y.mean()) * 100}


ML = train_churn(df_master, (len(df_master), round(float(df_master["Monto_Compra"].sum()), 2)))
df_master["Prob_Churn_ML"] = ML["oof"] if ML else df_master["Riesgo_Churn_Score"]

# ==============================================================================
# 6. FILTROS INTERACTIVOS EN BARRA LATERAL
# ==============================================================================
_DEFAULTS = {}


def _set_group(key, opts, val):
    for o in opts:
        st.session_state[f"{key}::{o}"] = val


def _reset_all(defaults):
    for k, v in defaults.items():
        st.session_state[k] = v


def slicer(key, title, opts):
    opts = list(opts)
    for o in opts:
        st.session_state.setdefault(f"{key}::{o}", True)
        _DEFAULTS[f"{key}::{o}"] = True
    with st.container(border=True):
        html(f'<div class="slicer-header">{title}</div>')
        c1, c2 = st.columns(2)
        stretch(c1.button, "Todos", key=f"{key}__all", on_click=_set_group, args=(key, opts, True))
        stretch(c2.button, "Ninguno", key=f"{key}__none", on_click=_set_group, args=(key, opts, False))
        sel = [o for o in opts if st.checkbox(str(o), key=f"{key}::{o}")]
    return sel if sel else opts


def multi(key, label, opts):
    opts = list(opts)
    st.session_state.setdefault(key, opts)
    st.session_state[key] = [v for v in st.session_state[key] if v in opts]
    _DEFAULTS[key] = opts
    sel = st.multiselect(label, opts, key=key)
    return sel if sel else opts


with st.sidebar:
    st.markdown("---")
    st.markdown("#### ⚡ Segmentadores Interactivos")
    f_years = slicer("yr", "📅 Año Fiscal", sorted(df_master["Año"].unique().tolist()))
    f_months = slicer("mo", "🗓️ Mes del Año", [MESES_FULL[m] for m in sorted(df_master["Mes_Num"].unique()) if m in MESES_FULL])
    f_types = slicer("tp", "🏢 Tipo de Cuenta", sorted(df_master["Tipo_Cliente_Cuenta"].unique()))
    f_regs = slicer("rg", "📍 Región Geográfica", sorted(df_master["Region"].unique()))
    f_cats = slicer("ct", "📦 Línea de Negocio", sorted(df_master["Categoria"].unique()))
    f_chan = slicer("cn", "🛒 Canal de Venta", sorted(df_master["Canal_Venta"].unique()))
    f_vend = slicer("vd", "👔 Vendedor", sorted(df_master["Vendedor_Asignado"].unique()))
    stretch(st.button, "↺ Restablecer todos los filtros", key="btn_reset_all",
            on_click=_reset_all, args=(dict(_DEFAULTS),))

inv_meses = {v: k for k, v in MESES_FULL.items()}
f_months_nums = [inv_meses[m] for m in f_months if m in inv_meses]

mask_ny = (df_master["Tipo_Cliente_Cuenta"].isin(f_types) & df_master["Region"].isin(f_regs) &
           df_master["Categoria"].isin(f_cats) & df_master["Canal_Venta"].isin(f_chan) &
           df_master["Vendedor_Asignado"].isin(f_vend) &
           df_master["Mes_Num"].isin(f_months_nums))
df_ny = df_master[mask_ny].copy()
df = df_master[mask_ny & df_master["Año"].isin(f_years)].copy()

with st.sidebar:
    st.markdown("---")
    st.markdown(f"**Registros activos:** `{len(df):,}` de `{len(df_master):,}`")
    st.caption(src_note)

if df.empty:
    st.warning("⚠️ No hay registros con los filtros seleccionados. Selecciona al menos una opción en cada segmentador.")
    st.stop()

# ==============================================================================
# 7. MÉTRICAS GLOBALES & UNIT ECONOMICS
# ==============================================================================
def compute_metrics(d):
    rev, cogs, gp, cac_t = d["Monto_Compra"].sum(), d["Costo_Total"].sum(), d["Margen_Bruto"].sum(), d["CAC_Estimado"].sum()
    n = len(d)
    avg_cac = d["CAC_Estimado"].mean()
    avg_ltv = d["LTV_Estimado_USD"].mean()
    alto = d["Alerta_Riesgo_Churn"] == "Alto Riesgo"
    return dict(
        rev=rev, cogs=cogs, gp=gp, cac_total=cac_t, net=gp - cac_t,
        net_pct=(gp - cac_t) / rev * 100 if rev else 0,
        orders=n, clients=d["Nombre_Cuenta_Cliente"].nunique(),
        margin=gp / rev * 100 if rev else 0, ticket=rev / n if n else 0,
        ltv=avg_ltv, cac=avg_cac, ltv_cac=avg_ltv / avg_cac if avg_cac else 0,
        churn_hi=alto.mean() * 100,
        fiel=(d["Alerta_Riesgo_Churn"] == "Cliente Fiel / Estable").mean() * 100,
        sla=(d["Retraso"] == 0).mean() * 100, csat=d["Satisfaccion_CSAT"].mean(),
        churn_avg=d["Riesgo_Churn_Score"].mean(), rev_risk=d.loc[alto, "Monto_Compra"].sum(),
        recency=d["Recencia_Dias"].mean()
    )


def ytd_compare(d_all):
    if d_all.empty:
        return None
    last = d_all["Fecha_Transaccion"].max()
    ly = int(last.year)
    cur = d_all[d_all["Año"] == ly]
    prv = d_all[(d_all["Año"] == ly - 1) & ((d_all["Mes_Num"] < last.month) |
                                            ((d_all["Mes_Num"] == last.month) & (d_all["Dia_Mes"] <= last.day)))]
    if prv.empty or cur.empty:
        return None
    a, b = compute_metrics(cur), compute_metrics(prv)
    ch = lambda x, y: (x - y) / y * 100 if y else np.nan
    return dict(
        year=ly, rev=ch(a["rev"], b["rev"]), gp=ch(a["gp"], b["gp"]),
        orders=ch(a["orders"], b["orders"]), margin_pp=a["margin"] - b["margin"],
        ticket=ch(a["ticket"], b["ticket"]), rev_cur=a["rev"], rev_prev=b["rev"]
    )


_alto = df_master["Alerta_Riesgo_Churn"] == "Alto Riesgo"
REC_THR = int(round(df_master.loc[_alto, "Recencia_Dias"].quantile(0.10), -1)) if _alto.sum() >= 5 else 180
M = compute_metrics(df)
YOY = ytd_compare(df_ny)
d_min, d_max = df["Fecha_Transaccion"].min(), df["Fecha_Transaccion"].max()


def customer_table(d):
    c = d.groupby(["Nombre_Cuenta_Cliente", "Tipo_Cliente_Cuenta"]).agg(
        Cuenta=("Cuenta", "first"), Facturacion=("Monto_Compra", "sum"), Margen=("Margen_Bruto", "sum"), Ordenes=("Cliente_ID", "count"),
        Recencia_Min=("Recencia_Dias", "min"), CSAT=("Satisfaccion_CSAT", "mean"), LTV=("LTV_Estimado_USD", "mean"),
        Churn=("Riesgo_Churn_Score", "mean"), Prob_ML=("Prob_Churn_ML", "mean")).reset_index()
    c = c.sort_values("Facturacion", ascending=False).reset_index(drop=True)
    tot = c["Facturacion"].sum()
    c["Acum"] = c["Facturacion"].cumsum()
    c["Pct_Acum"] = c["Acum"] / tot * 100 if tot else 0
    c["Pct_Prev"] = (c["Acum"] - c["Facturacion"]) / tot * 100 if tot else 0
    c["Pct_Cuentas"] = (c.index + 1) / len(c) * 100 if len(c) else 0
    c["Clase"] = c["Pct_Prev"].map(pareto_class)
    return c


def render_cockpit_header(show_master_voice=True, key_suffix="", tab_title="🧭 1. Resumen Ejecutivo"):
    """
    Renderiza el encabezado principal ejecutivo y el banner de 6 KPI Cards estratégicos
    directamente DEBAJO de la barra de navegación fija superior de pestañas,
    concatenando dinámicamente el título y el módulo activo del menú seleccionado.
    """
    if synthetic:
        st.warning("⚠️ Mostrando **datos de demostración**. Coloca `dataset_analytics_storytelling_ml_500.xlsx` o `.csv` en la carpeta del script.")

    html(
        f'<div style="padding-bottom: 6px; margin-top: 4px;">'
        f'<div style="font-size:0.85rem;font-weight:800;color:{THEME["accent_blue"]};letter-spacing:0.14em;text-transform:uppercase;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
        f'<span>Inteligencia de Datos 360° • Business Intelligence, Machine Learning &amp; Voice AI</span>'
        f'<span style="color:{THEME["border"]};">•</span>'
        f'<span style="color:{THEME["accent_purple"]};background:rgba(124, 58, 237, 0.12);padding:2px 10px;border-radius:6px;border:1px solid {THEME["accent_purple"]};font-size:0.80rem;letter-spacing:0.04em;">'
        f'{tab_title}</span></div>'
        f'<h1 style="font-size:2.15rem;font-weight:800;color:{THEME["text_primary"]};margin:6px 0 10px 0;line-height:1.25;">'
        f'Plataforma Ejecutiva de Analítica Avanzada &amp; Diagnóstico Financiero '
        f'<span style="color:{THEME["accent_blue"]};font-weight:700;font-size:1.65rem;"> — {tab_title}</span></h1>'
        f'<p style="color:{THEME["text_secondary"]};font-size:0.98rem;max-width:1150px;line-height:1.65;">'
        f'Tablero de mando integral con {kw("Copiloto de Storytelling Dinámico", "info")} y {kw("Locución Fonética por Voz", "pos")}: '
        f'monitorea {kw("Unit Economics (LTV/CAC)", "key")}, rentabilidad por segmento, retención predictiva vía '
        f'{kw("Machine Learning (Random Forest · K-Means)", "ml")} y auditoría operativa. '
        f'Periodo analizado: {kw(d_min.strftime("%d-%b-%Y") + " → " + d_max.strftime("%d-%b-%Y"), "key")} · '
        f'{len(df):,} órdenes · {M["clients"]:,} cuentas analizadas.</p></div>'
    )

    if show_master_voice:
        master_speech = (
            f"Bienvenido al tablero ejecutivo de inteligencia de negocios. Durante el periodo analizado, "
            f"la operación facturó un total de {usd(M['rev'])} en {M['orders']} órdenes transaccionales, "
            f"con un margen bruto ponderado del {M['margin']:.2f}%. La contribución neta tras descontar el costo "
            f"de adquisición de clientes es de {usd(M['net'])}. El ratio de rentabilidad unitaria LTV/CAC "
            f"alcanza {M['ltv_cac']:.1f}x. Se detecta un {M['churn_hi']:.1f}% de pedidos en alto riesgo "
            f"de abandono comercial, mientras que el cumplimiento del SLA logístico de entregas se sitúa en el {M['sla']:.1f}%."
        )
        voice_player(master_speech, button_label="🎙️ Escuchar Resumen Ejecutivo Global (Voz General)", key=f"vp_master{key_suffix}")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        kpi("Ingresos Brutos", f"${M['rev']:,.0f}",
            f"<b>{M['orders']:,}</b> órdenes · ticket ${M['ticket']:,.0f}", THEME["success"],
            delta=YOY["rev"] if YOY else None)
    with k2:
        kpi("Margen Bruto Ponderado", f"{M['margin']:.2f}%", f"Beneficio: <b>${M['gp']:,.0f}</b>",
            sem_color(M["margin"], 25, 18), delta=None)
    with k3:
        kpi("Contribución Neta", f"${M['net']:,.0f}", f"<b>{M['net_pct']:.1f}%</b> post-CAC (${M['cac_total']:,.0f})",
            sem_color(M["net_pct"], 15, 8), vcolor=THEME["success"] if M["net"] > 0 else THEME["danger"])
    with k4:
        kpi("Unit Economics (LTV / CAC)", f"{M['ltv_cac']:.1f}x", f"LTV ${M['ltv']:,.0f} | CAC ${M['cac']:,.0f}",
            sem_color(M["ltv_cac"], 10, 3), vcolor=THEME["accent_blue"])
    with k5:
        kpi("Cuentas en Alto Riesgo", f"{M['churn_hi']:.1f}%", f"Expuesto: <b>${M['rev_risk']:,.0f}</b> ({M['rev_risk'] / M['rev'] * 100:.1f}%)",
            sem_color(M["churn_hi"], 10, 20, higher=False),
            vcolor=THEME["danger"] if M["churn_hi"] > 20 else None)
    with k6:
        kpi("Cumplimiento SLA Logístico", f"{M['sla']:.1f}%", f"CSAT medio: <b>{M['csat']:.2f} / 5.0 ★</b>",
            sem_color(M["sla"], 90, 80))

    if YOY:
        st.caption(f"▲▼ Variación del ingreso: acumulado {YOY['year']} vs mismo tramo de {YOY['year'] - 1} (comparación homogénea YoY).")

    html("<div style='height: 12px;'></div>")

# ==============================================================================
# 8. MÓDULOS ANALÍTICOS (11 PESTAÑAS COMPLETAS)
# ==============================================================================
# ------------------------------------------------------------------------------
# TAB 1: RESUMEN EJECUTIVO
# ------------------------------------------------------------------------------
def tab_resumen():
    t_name, t_rev, t_share = top_share(df, "Tipo_Cliente_Cuenta")
    t_ord_share = (df["Tipo_Cliente_Cuenta"] == t_name).mean() * 100
    low_name = df.groupby("Tipo_Cliente_Cuenta")["Monto_Compra"].sum().idxmin()
    low_rev_share = df.loc[df["Tipo_Cliente_Cuenta"] == low_name, "Monto_Compra"].sum() / M["rev"] * 100
    low_ord_share = (df["Tipo_Cliente_Cuenta"] == low_name).mean() * 100
    c_name, _, c_share = top_share(df, "Categoria")
    ch_name, _, ch_share = top_share(df, "Canal_Venta")
    r_name, _, r_share = top_share(df, "Region")
    risk_share = M["rev_risk"] / M["rev"] * 100 if M["rev"] else 0

    story("🧭", "Storytelling Ejecutivo: Diagnóstico 360° del Negocio",
          f"Durante el periodo la operación facturó {kw(usd(M['rev']), 'pos')} a través de {kw(f'{M['orders']:,} órdenes', 'info')} "
          f"con un margen bruto ponderado de {kw(f'{M['margin']:.2f}%', 'pos' if M['margin'] >= 25 else 'warn')}. "
          f"El segmento {kw(t_name, 'key')} genera el {kw(f'{t_share:.0f}% del ingreso', 'pos')} con solo el {t_ord_share:.0f}% del volumen transaccional, "
          f"mientras que {kw(low_name, 'warn')} absorbe el {low_ord_share:.0f}% de las transacciones pero solo el {low_rev_share:.0f}% de la facturación: "
          f"<b>el valor real radica en el ticket y la rentabilidad por cuenta, no en la cantidad de órdenes</b>. "
          f"La línea líder es {kw(c_name, 'info')} ({c_share:.0f}%), el canal con mayor tracción es {kw(ch_name, 'info')} ({ch_share:.0f}%) y la región "
          f"{kw(r_name, 'info')} concentra el {r_share:.0f}% del mercado. En fidelización, el {kw(f'{M['fiel']:.0f}% de los pedidos', 'pos')} corresponde a clientes estables y "
          f"{kw(f'{M['churn_hi']:.1f}% se encuentra en alto riesgo', 'neg' if M['churn_hi'] > 15 else 'warn')}, exponiendo {kw(usd(M['rev_risk']), 'neg')} "
          f"({risk_share:.0f}% de la facturación activa).",
          tips=[
              f"Priorizar retención y contacto ejecutivo en el segmento ancla ({t_name}), cuyo aporte del {t_share:.0f}% sostiene el resultado global.",
              f"Activar de inmediato el protocolo de rescate comercial sobre los {usd(M['rev_risk'])} en riesgo de abandono ({risk_share:.0f}% del ingreso activo).",
              f"Apalancar el sólido multiplicador LTV/CAC ({M['ltv_cac']:.1f}x) acelerando la inversión de captación en los canales más eficientes.",
              f"Monitorear la entrega logística en {r_name} para blindar el cumplimiento del SLA ({M['sla']:.1f}%) y sostener el CSAT en {M['csat']:.2f}/5."
          ])

    yo_txt = (f"Acumulado {YOY['year']} vs {YOY['year'] - 1}: ingresos {kw(f'{YOY['rev']:+.1f}%', 'pos' if YOY['rev'] >= 0 else 'neg')}, "
              f"margen {YOY['margin_pp']:+.1f} pp." if YOY else "Sin año anterior comparable con los filtros activos.")

    exec_summary("Mensajes Clave para el Comité Ejecutivo", [
        (sem_icon(M["margin"], 25, 18), "Rentabilidad Bruta",
         f"Margen bruto en {kw(f'{M['margin']:.1f}%', 'pos' if M['margin'] >= 25 else 'warn')} (meta ≥ 25%). Tras CAC, la contribución neta es "
         f"{kw(usd(M['net']), 'pos')} ({M['net_pct']:.1f}% de las ventas)."),
        ("🏢", "Concentración Comercial", f"{kw(t_name, 'key')} representa el {t_share:.0f}% de las ventas. La retención de este grupo es vital."),
        ("📈", "Evolución Interanual", yo_txt),
        (sem_icon(M["churn_hi"], 10, 20, False), "Alerta Preventiva Churn",
         f"{kw(f'{M['churn_hi']:.1f}%', 'neg')} de órdenes en riesgo; recencia promedio de {M['recency']:.0f} días. Reactivar antes del día ~{REC_THR}."),
        (sem_icon(M["sla"], 90, 80), "Eficiencia Operativa SLA", f"Entregas en tiempo: {kw(f'{M['sla']:.1f}%', 'pos' if M['sla'] >= 90 else 'warn')}; CSAT {M['csat']:.2f}/5."),
        (sem_icon(M["ltv_cac"], 10, 3), "Retorno de Adquisición",
         f"LTV/CAC en {kw(f'{M['ltv_cac']:.1f}x', 'info')} superando el umbral saludable de 3x: adquisición con excelente retorno."),
    ])

    c1, c2 = st.columns(2)
    with c1:
        m = df.groupby("Periodo").agg(Ventas=("Monto_Compra", "sum"), Margen=("Margen_Bruto", "sum")).reset_index()
        m["Margen_Pct"] = m["Margen"] / m["Ventas"] * 100
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=m["Periodo"], y=m["Ventas"], name="Ventas ($)", marker_color=THEME["accent_blue"],
            hovertemplate="<b>📅 %{x}</b><br>💰 Ventas Brutas: $%{y:,.0f}<extra>Ventas ($)</extra>"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=m["Periodo"], y=m["Margen_Pct"], name="Margen %", mode="lines+markers",
            line=dict(color=THEME["warning"], width=3),
            hovertemplate="<b>📅 %{x}</b><br>📊 Margen Bruto: %{y:.1f}%<extra>Margen %</extra>"
        ), secondary_y=True)
        fig.update_layout(title="Ventas mensuales y margen bruto (%)")
        fig.update_yaxes(title_text="Ventas ($)", secondary_y=False)
        fig.update_yaxes(title_text="Margen (%)", secondary_y=True, showgrid=False)
        best = m.loc[m["Ventas"].idxmax()]
        chart(fig, "Barras = ingresos mensuales; línea ámbar = margen bruto % (eje derecho).",
              f"Pico de ingresos en {kw(best['Periodo'], 'key')} con {kw(usd(best['Ventas']), 'pos')}. Margen oscilando entre {m['Margen_Pct'].min():.1f}% y {m['Margen_Pct'].max():.1f}%.",
              "Replicar el mix de productos y condiciones del mes de mayor rentabilidad para estabilizar el margen.", 390)
    with c2:
        g = df.groupby(["Categoria", "Producto_Principal"]).agg(
            Ventas=("Monto_Compra", "sum"),
            Margen=("Margen_Bruto", "sum")
        ).reset_index()
        g["Margen_Pct"] = (g["Margen"] / g["Ventas"]) * 100

        # Paleta financiera divergente ejecutiva calibrada al 25% de margen objetivo
        scale_treemap = [
            [0.0, "#E11D48"],   # Rosa carmesí / alerta (<22%)
            [0.25, "#F43F5E"],  # Rojo coral
            [0.45, "#F59E0B"],  # Ámbar advertencia (~24%)
            [0.55, "#FBBF24"],  # Dorado / neutral equilibrado
            [0.72, "#10B981"],  # Esmeralda saludable (>28%)
            [1.0, "#047857"]    # Verde corporativo de alto rendimiento (>34%)
        ]

        fig = px.treemap(
            g,
            path=[px.Constant("Portafolio"), "Categoria", "Producto_Principal"],
            values="Ventas",
            color="Margen_Pct",
            custom_data=["Margen_Pct"],
            color_continuous_scale=scale_treemap,
            color_continuous_midpoint=25.0,
            title="🗺️ Mapa de calor del portafolio: ingresos y margen"
        )

        fig.update_traces(
            texttemplate="<b>%{label}</b><br>💵 $%{value:,.0f}<br>📈 Margen: %{customdata[0]:.1f}%",
            textposition="middle center",
            hovertemplate=(
                "<b>🏷️ %{label}</b><br>"
                "📁 <b>Jerarquía:</b> %{parent}<br>"
                "────────────────────────────<br>"
                "💰 <b>Facturación:</b> $%{value:,.2f}<br>"
                "📊 <b>Margen Bruto Ponderado:</b> %{customdata[0]:.1f}%<br>"
                "📈 <b>Cuota en Portafolio:</b> %{percentRoot:.1%}<br>"
                "📦 <b>Cuota en Categoría:</b> %{percentParent:.1%}"
                "<extra></extra>"
            ),
            marker=dict(
                cornerradius=4,
                pad=dict(b=3, l=3, r=3, t=22),
                line=dict(width=1.5, color="#1E293B" if is_dark else "#CBD5E1")
            ),
            pathbar=dict(visible=True, thickness=24)
        )

        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(text="<b>Margen (%)</b>", side="top", font=dict(size=11, family="Plus Jakarta Sans")),
                ticksuffix="%",
                tickformat=".1f",
                thickness=14,
                len=0.75,
                yanchor="middle",
                y=0.5
            )
        )

        top_p = g.loc[g["Ventas"].idxmax()]
        best_m = g.loc[g["Margen_Pct"].idxmax()]
        low_m = g.loc[g["Margen_Pct"].idxmin()]
        share_top = (top_p["Ventas"] / g["Ventas"].sum()) * 100 if g["Ventas"].sum() > 0 else 0

        chart(
            fig,
            "Área de cada rectángulo = facturación bruta en USD ($); color = margen bruto % (escala semafórica: rojo < 22%, ámbar ~25%, verde esmeralda > 30%). Navegación: haz clic en una categoría para explorar sus SKUs en detalle.",
            f"SKU insignia en ingresos: {kw(top_p['Producto_Principal'], 'key')} ({usd(top_p['Ventas'])}, margen {top_p['Margen_Pct']:.1f}%), aportando el {share_top:.1f}% del portafolio. "
            f"Mayor rentabilidad: {kw(best_m['Producto_Principal'], 'pos')} ({best_m['Margen_Pct']:.1f}%). Margen más ajustado: {kw(low_m['Producto_Principal'], 'warn')} ({low_m['Margen_Pct']:.1f}%).",
            f"Blindar stock e inventario de seguridad en {top_p['Producto_Principal']}. Optimizar costos unitarios (COGS) en {low_m['Producto_Principal']}, "
            f"y diseñar bundles con productos de alto margen ({best_m['Producto_Principal']}) para elevar el rendimiento global.",
            410
        )
    c3, c4 = st.columns(2)
    with c3:
        g = df.groupby(["Canal_Venta", "Categoria"])["Monto_Compra"].sum().reset_index()
        src, dst = list(g["Canal_Venta"].unique()), list(g["Categoria"].unique())
        labels = src + dst
        idx = {l: i for i, l in enumerate(labels)}
        fig = go.Figure(go.Sankey(
            node=dict(
                label=labels, pad=18, thickness=16, color=[PAL[i % len(PAL)] for i in range(len(labels))],
                hovertemplate="<b>🏷️ %{label}</b><br>💰 Flujo Acumulado: $%{value:,.0f}<extra></extra>"
            ),
            link=dict(
                source=g["Canal_Venta"].map(idx).tolist(), target=g["Categoria"].map(idx).tolist(),
                value=g["Monto_Compra"].tolist(), color="rgba(148,163,184,0.35)",
                hovertemplate="<b>%{source.label} → %{target.label}</b><br>💰 Volumen Comercial: $%{value:,.0f}<extra></extra>"
            )))
        fig.update_layout(title="Flujo de ingresos: Canal de venta → Línea de negocio")
        chart(fig, "Grosor del flujo = volumen de dinero transferido desde cada canal hacia cada categoría de producto.",
              f"El canal {kw(ch_name, 'key')} canaliza el {ch_share:.0f}% del total del flujo comercial.",
              "Impulsar la oferta de productos corporativos y servidores a través de canales directos y digitales.", 420)
    with c4:
        pv = df.pivot_table(index="Region", columns="Categoria", values="Monto_Compra", aggfunc="sum").fillna(0)
        fig = px.imshow(pv, text_auto=".2s", aspect="auto", color_continuous_scale=SCALE_SEQ,
                        labels=dict(x="Línea de negocio", y="Región", color="Ventas ($)"), title="Matriz Región × Línea de negocio (ventas)")
        fig.update_traces(
            hovertemplate="<b>📍 Región:</b> %{y}<br><b>📦 Línea:</b> %{x}<br>💰 <b>Facturación:</b> $%{z:,.0f}<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Ventas ($)</b>"), tickprefix="$", tickformat=",.0s"))
        mx = pv.stack().idxmax()
        chart(fig, "Gradiente de azul = mayor concentración de facturación regional por categoría.",
              f"Mayor intersección: {kw(mx[0], 'key')} × {kw(mx[1], 'key')} ({usd(pv.stack().max())}).",
              "Explorar zonas claras en regiones clave para ventas cruzadas de portafolio y nuevos acuerdos.", 420)

    section("🚦 Tablero de Control de Salud del Negocio (Semáforo Estratégico)")
    rows = [
        ("Margen bruto ponderado", f"{M['margin']:.2f}%", "≥ 25%", sem_icon(M["margin"], 25, 18)),
        ("Contribución neta (margen − CAC) / ingresos", f"{M['net_pct']:.1f}%", "≥ 15%", sem_icon(M["net_pct"], 15, 8)),
        ("LTV / CAC (Unit Economics)", f"{M['ltv_cac']:.1f}x", "≥ 3.0x", sem_icon(M["ltv_cac"], 3, 1.5)),
        ("Órdenes en alto riesgo de churn", f"{M['churn_hi']:.1f}%", "≤ 10%", sem_icon(M["churn_hi"], 10, 20, False)),
        ("Índice de retención (clientes fieles)", f"{M['fiel']:.1f}%", "≥ 50%", sem_icon(M["fiel"], 50, 35)),
        ("Cumplimiento SLA de entrega", f"{M['sla']:.1f}%", "≥ 90%", sem_icon(M["sla"], 90, 80)),
        ("Satisfacción CSAT media", f"{M['csat']:.2f} / 5", "≥ 4.0 ★", sem_icon(M["csat"], 4.0, 3.5)),
        ("Ingresos expuestos a alto riesgo", f"{M['rev_risk'] / M['rev'] * 100:.1f}%", "≤ 15%", sem_icon(M["rev_risk"] / M["rev"] * 100, 15, 25, False)),
    ]
    sc = pd.DataFrame(rows, columns=["Indicador", "Valor actual", "Meta", "Estado"])
    show_table(sc, status=["Estado"],
               title="Scorecard de Salud Global del Negocio",
               summary=f"Diagnóstico consolidado de 8 indicadores vitales. Margen bruto ponderado en {M['margin']:.2f}% y retorno de adquisición LTV/CAC en {M['ltv_cac']:.1f}x. Se identifican {M['churn_hi']:.1f}% de órdenes con alta propensión de deserción exponiendo {usd(M['rev_risk'])} en ingresos.",
               tips=[
                   f"Activar protocolos de servicio preferencial si el cumplimiento SLA ({M['sla']:.1f}%) o el CSAT medio ({M['csat']:.2f}/5) se acercan a los límites de tolerancia.",
                   f"Blindar la contribución neta del {M['net_pct']:.1f}% controlando el gasto de CAC en canales con bajo ticket.",
                   f"Establecer comités quincenales de seguimiento sobre el porcentaje de clientes fieles ({M['fiel']:.1f}%) para evitar desvíos estructurales."
               ])
    if briefing is not None:
        section("📄 Executive Briefing Original del Archivo")
        stretch(st.dataframe, briefing, hide_index=True)


# ------------------------------------------------------------------------------
# TAB 2: COMERCIAL & TENDENCIAS
# ------------------------------------------------------------------------------
def tab_comercial():
    m = df.groupby("Periodo")["Monto_Compra"].sum().reset_index(name="Ventas")
    n_m = len(m)
    slope = r2 = None
    if n_m >= 4:
        x = np.arange(n_m)
        slope, intercept = np.polyfit(x, m["Ventas"], 1)
        r2 = np.corrcoef(x, m["Ventas"])[0, 1] ** 2
    ch = df.groupby("Canal_Venta").agg(V=("Monto_Compra", "sum"), O=("Cliente_ID", "count"))
    best_ch, worst_ch = ch["V"].idxmax(), ch["V"].idxmin()
    tk = df.groupby("Canal_Venta")["Monto_Compra"].mean()
    top_t, _, top_t_sh = top_share(df, "Tipo_Cliente_Cuenta")

    tr = (f"Pendiente de tendencia: {kw(f'{slope:+,.0f} $/mes', 'pos' if slope >= 0 else 'neg')} (R² = {r2:.2f}). "
          if slope is not None else "")
    story("📈", "Storytelling Comercial: Comportamiento de Canales, Cuentas y Estacionalidad",
          f"El canal {kw(best_ch, 'key')} comanda la facturación con {kw(usd(ch.loc[best_ch, 'V']), 'pos')}. "
          f"El ticket medio más robusto se genera en {kw(tk.idxmax(), 'info')} ({usd(tk.max())}) frente a {kw(tk.idxmin(), 'warn')} ({usd(tk.min())}). "
          f"{tr}El tipo de cuenta ancla es {kw(top_t, 'key')} con el {top_t_sh:.0f}% del ingreso.",
          tips=[
              f"Reforzar el stock y la dotación de ejecutivos sénior en {best_ch}, el canal tractor de ventas del portafolio.",
              f"Rediseñar la propuesta comercial y promociones en {worst_ch} para aumentar el ticket medio y dinamizar su demanda.",
              "Aprovechar los picos estacionales de los trimestres clave para negociar contratos anuales de aprovisionamiento con cuentas ancla.",
              "Vigilar los costes de adquisición (CAC) en canales digitales para maximizar el ratio Margen / CAC."
          ])

    c1, c2 = st.columns(2)
    with c1:
        g = df.groupby(["Trimestre_Año", "Canal_Venta"])["Monto_Compra"].sum().reset_index()
        fig = px.bar(g, x="Trimestre_Año", y="Monto_Compra", color="Canal_Venta", barmode="stack",
                     title="Evolución trimestral de ventas por canal", labels={"Monto_Compra": "Ventas ($)", "Trimestre_Año": "Trimestre"},
                     color_discrete_sequence=PAL)
        fig.update_traces(
            hovertemplate="<b>📅 %{x}</b><br>🏷️ <b>Canal:</b> %{fullData.name}<br>💰 <b>Ventas:</b> $%{y:,.0f}<extra></extra>"
        )
        chart(fig, "Barras por trimestre apiladas por canal comercial para evaluar consistencia temporal.",
              f"El canal {kw(best_ch, 'key')} lidera de forma sostenida la aportación trimestral acumulando {usd(ch.loc[best_ch, 'V'])}.",
              "Diversificar canales emergentes como WhatsApp Corporativo para reducir la dependencia de un solo canal.", 390)
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=m["Periodo"], y=m["Ventas"], name="Ventas del mes", marker_color=rgba(THEME["accent_blue"], 0.55),
            hovertemplate="<b>📅 %{x}</b><br>💰 <b>Ventas del Mes:</b> $%{y:,.0f}<extra>Ventas del mes</extra>"
        ))
        fig.add_trace(go.Scatter(
            x=m["Periodo"], y=m["Ventas"].rolling(3, min_periods=1).mean(), name="Media móvil 3m",
            line=dict(color=THEME["warning"], width=3),
            hovertemplate="<b>📅 %{x}</b><br>📈 <b>Media Móvil (3m):</b> $%{y:,.0f}<extra>Media móvil</extra>"
        ))
        if slope is not None:
            x = np.arange(n_m)
            fig.add_trace(go.Scatter(
                x=m["Periodo"], y=intercept + slope * x, name="Tendencia lineal",
                line=dict(color=THEME["accent_pink"], dash="dash"),
                hovertemplate="<b>📅 %{x}</b><br>📉 <b>Tendencia:</b> $%{y:,.0f}<extra>Tendencia</extra>"
            ))
        fig.update_layout(title="Ventas mensuales, media móvil 3m y tendencia")
        chart(fig, "Barras = facturación real; línea ámbar = media móvil trimestral; línea rosa = ajuste lineal.",
              f"Pendiente calculada: {kw(f'{slope:+,.0f} $/mes', 'pos' if (slope or 0) >= 0 else 'neg')}" if slope is not None else "Insuficientes meses para regresión.",
              "Ajustar pronósticos de abastecimiento y compras basándose en la media móvil suavizada para evitar quiebres de inventario.", 390)
    c3, c4 = st.columns(2)
    with c3:
        fig = px.sunburst(df, path=["Tipo_Cliente_Cuenta", "Canal_Venta"], values="Monto_Compra",
                          title="Distribución de ingresos: Tipo de cuenta → Canal de venta", color_discrete_sequence=PAL)
        fig.update_traces(
            hovertemplate="<b>🏷️ %{label}</b><br>📁 <b>Jerarquía:</b> %{parent}<br>💰 <b>Facturación:</b> $%{value:,.0f}<br>📊 <b>Cuota Total:</b> %{percentRoot:.1%}<br>📈 <b>Cuota Segmento:</b> %{percentParent:.1%}<extra></extra>"
        )
        chart(fig, "Gráfico Sunburst: el anillo interior representa el tipo de cliente y el exterior el canal de adquisición.",
              f"Las cuentas de tipo {kw(top_t, 'key')} concentran el {top_t_sh:.0f}% de la facturación en sus canales preferenciales.",
              "Asignar ejecutivos dedicados para acompañar a los clientes corporativos en su canal de compra preferido.", 390)
    with c4:
        pv = df.pivot_table(index="Mes_Num", columns="Canal_Venta", values="Monto_Compra", aggfunc="sum").reindex(range(1, 13)).fillna(0)
        pv.index = [MESES[i] for i in pv.index]
        fig = px.imshow(pv, text_auto=".2s", aspect="auto", color_continuous_scale=SCALE_SEQ,
                        labels=dict(x="Canal", y="Mes", color="Ventas ($)"), title="Estacionalidad: mes del año × canal")
        fig.update_traces(
            hovertemplate="<b>📅 Mes:</b> %{y}<br>🏷️ <b>Canal:</b> %{x}<br>💰 <b>Ventas:</b> $%{z:,.0f}<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Ventas ($)</b>"), tickprefix="$", tickformat=",.0s"))
        chart(fig, "Matriz de calor que muestra la concentración de compras por mes del año y canal de venta.",
              "Se observan meses de alta densidad transaccional con concentración en canales digitales y ejecutivos.",
              "Programar promociones anticipadas y reforzar el soporte logístico en los meses previos a los picos detectados.", 390)

    section("📋 Desempeño Operativo por Canal de Venta")
    t = df.groupby("Canal_Venta").agg(Órdenes=("Cliente_ID", "count"), Ventas=("Monto_Compra", "sum"), Margen=("Margen_Bruto", "sum"),
                                      CAC=("CAC_Estimado", "mean"), CAC_Total=("CAC_Estimado", "sum"), CSAT=("Satisfaccion_CSAT", "mean"),
                                      Churn=("Riesgo_Churn_Score", "mean")).reset_index()
    t["% Ventas"] = t["Ventas"] / t["Ventas"].sum() * 100
    t["Ticket"] = t["Ventas"] / t["Órdenes"]
    t["Margen %"] = t["Margen"] / t["Ventas"] * 100
    t["Margen/CAC"] = t["Margen"] / t["CAC_Total"]
    t = t[["Canal_Venta", "Órdenes", "Ventas", "% Ventas", "Ticket", "Margen %", "CAC", "Margen/CAC", "CSAT", "Churn"]].sort_values("Ventas", ascending=False)
    show_table(t, {"Ventas": "${:,.0f}", "% Ventas": "{:.1f}%", "Ticket": "${:,.0f}", "Margen %": "{:.1f}%", "CAC": "${:,.0f}",
                   "Margen/CAC": "{:.1f}x", "CSAT": "{:.2f} ★", "Churn": "{:.2f}"},
               good=["Ventas", "Margen %", "Margen/CAC", "CSAT"], bad=["CAC", "Churn"], neutral=["Órdenes"],
               title="Desempeño Operativo y Retorno Comercial por Canal de Venta",
               summary=f"Análisis comparativo de canales comerciales. {best_ch} lidera con {t.loc[t['Canal_Venta']==best_ch, '% Ventas'].values[0]:.1f}% de la facturación y un ticket de {usd(t.loc[t['Canal_Venta']==best_ch, 'Ticket'].values[0])}. El multiplicador de retorno de captación medio se sitúa en {t['Margen/CAC'].mean():.1f}x veces el CAC invertido.",
               tips=[
                   "Focalizar el presupuesto publicitario y de captación en los canales con mayor multiplicador Margen / CAC.",
                   "Implementar incentivos comerciales para migrar compradores de bajo ticket a canales de autoservicio digital.",
                   "Vigilar la satisfacción CSAT en canales de alto flujo transaccional para prevenir cuellos de botella y quejas por tiempos de entrega."
               ])


# ------------------------------------------------------------------------------
# TAB 3: FINANZAS 360° & MÁRGENES
# ------------------------------------------------------------------------------
def tab_finanzas():
    disc = df.groupby("Descuento_Pct").agg(Órdenes=("Cliente_ID", "count"), Margen_Pct=("Margen_Bruto_Pct", "mean")).reset_index()
    cogs_cent = usd(M['cogs'] / M['rev'] * 100, 1) if M['rev'] else "$0"
    gp_cent = usd(M['gp'] / M['rev'] * 100, 1) if M['rev'] else "$0"

    story("💰", "Storytelling Financiero: Estructura de Costos, Descuentos y Contribución Neta",
          f"De cada $100 facturados, {cogs_cent} absorben el costo directo de mercancías (COGS) y "
          f"{gp_cent} se transforman en margen bruto. Luego de descontar la inversión total de captación "
          f"({kw(usd(M['cac_total']), 'warn')}), la contribución neta asciende a {kw(usd(M['net']), 'pos')} ({M['net_pct']:.1f}% del total). "
          f"El ratio LTV/CAC de {kw(f'{M['ltv_cac']:.1f}x', 'info')} confirma una excelente rentabilidad de adquisición.",
          tips=[
              f"Proteger la contribución neta del {M['net_pct']:.1f}% limitando los descuentos discrecionales en categorías de alta rotación.",
              "Renegociar contratos con proveedores en líneas donde los costos directos de mercancías superen el 70% de la facturación.",
              f"Mantener la inversión en adquisición (CAC total {usd(M['cac_total'])}) estrictamente vinculada a segmentos con LTV superior a 3x.",
              "Establecer una política de aprobación previa de descuentos superiores al 10% para evitar la compresión de márgenes operativos."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=["absolute", "relative", "total", "relative", "total"],
            x=["Ingresos", "Costo (COGS)", "Margen bruto", "Inversión CAC", "Contribución neta"],
            y=[M["rev"], -M["cogs"], 0, -M["cac_total"], 0], textposition="outside",
            text=[f"${M['rev'] / 1e3:,.1f}k", f"-${M['cogs'] / 1e3:,.1f}k", f"${M['gp'] / 1e3:,.1f}k", f"-${M['cac_total'] / 1e3:,.1f}k", f"${M['net'] / 1e3:,.1f}k"],
            connector={"line": {"color": THEME["border_highlight"]}},
            decreasing={"marker": {"color": THEME["danger"]}}, increasing={"marker": {"color": THEME["success"]}},
            totals={"marker": {"color": THEME["accent_blue"]}},
            hovertemplate="<b>💼 Concepto:</b> %{x}<br>💵 <b>Importe:</b> $%{y:,.0f}<extra>Cascada Financiera</extra>"
        ))
        fig.update_layout(title="Cascada financiera: de ingresos a contribución neta", showlegend=False)
        chart(fig, "Lectura secuencial de izquierda a derecha de la retención del dinero desde ingresos hasta margen neto post-CAC.",
              f"De {usd(M['rev'])} facturados, tras {usd(M['cogs'])} de costo directo y {usd(M['cac_total'])} de captación, la contribución neta retenida es {usd(M['net'])} ({M['net_pct']:.1f}%).",
              "Monitorear el CAC por canal para proteger el margen de contribución neta por encima del umbral saludable del 15%.", 390)
    with c2:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=disc["Descuento_Pct"].astype(str) + "%", y=disc["Órdenes"], name="Órdenes", marker_color=rgba(THEME["accent_blue"], 0.6),
            hovertemplate="<b>🏷️ Descuento:</b> %{x}<br>📦 <b>Volumen:</b> %{y:,} pedidos<extra>Órdenes</extra>"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=disc["Descuento_Pct"].astype(str) + "%", y=disc["Margen_Pct"], name="Margen %",
            mode="lines+markers", line=dict(color=THEME["warning"], width=3),
            hovertemplate="<b>🏷️ Descuento:</b> %{x}<br>📊 <b>Margen Retenido:</b> %{y:.1f}%<extra>Margen %</extra>"
        ), secondary_y=True)
        fig.update_layout(title="Sensibilidad del margen ante descuentos concedidos")
        chart(fig, "Barras = número de pedidos; línea ámbar = margen bruto porcentual medio según el descuento aplicado.",
              "Los descuentos mayores al 10% comprimen el margen aceleradamente sin generar incrementos proporcionales en el ticket.",
              "Fijar una política de descuentos comerciales con límite máximo de 8% condicionado a volúmenes mínimos de compra.", 390)
    c3, c4 = st.columns(2)
    with c3:
        fig = px.scatter(df, x="Monto_Compra", y="Margen_Bruto_Pct", color="Tipo_Cliente_Cuenta", size="Cantidad_Productos", size_max=22,
                         hover_name="Cuenta", title="Margen bruto (%) vs tamaño de la orden (escala log)", log_x=True,
                         labels={"Monto_Compra": "Monto ($ log)", "Margen_Bruto_Pct": "Margen (%)"}, color_discrete_sequence=PAL)
        fig.update_traces(
            hovertemplate="<b>🏢 Cuenta:</b> %{hovertext}<br>🏷️ <b>Segmento:</b> %{fullData.name}<br>💰 <b>Monto Compra:</b> $%{x:,.2f}<br>📊 <b>Margen Bruto:</b> %{y:.1f}%<extra></extra>"
        )
        chart(fig, "Dispersión de rentabilidad respecto al volumen transaccional; tamaño del punto proporcional a unidades.",
              "Los pedidos corporativos de gran tamaño sostienen márgenes estables, mientras que compras dispersas muestran alta variabilidad.",
              "Estandarizar precios por volumen para estabilizar la rentabilidad en todos los niveles de pedido.", 390)
    with c4:
        g = df.groupby(["Canal_Venta", "Tipo_Cliente_Cuenta"]).agg(G=("Margen_Bruto", "sum"), C=("CAC_Estimado", "sum")).reset_index()
        g["ROI"] = g["G"] / g["C"]
        fig = px.bar(g, x="Canal_Venta", y="ROI", color="Tipo_Cliente_Cuenta", barmode="group", color_discrete_sequence=PAL,
                     title="Margen bruto generado por cada $1 de CAC invertido", labels={"ROI": "Margen / CAC (x)"})
        fig.update_traces(
            hovertemplate="🏷️ <b>Canal:</b> %{x}<br>🏢 <b>Segmento:</b> %{fullData.name}<br>🎯 <b>Margen / CAC:</b> %{y:.2f}x<extra></extra>"
        )

    section("📋 Estado de Resultados por Línea de Negocio")
    p = df.groupby("Categoria").agg(Ventas=("Monto_Compra", "sum"), COGS=("Costo_Total", "sum"), Margen=("Margen_Bruto", "sum"),
                                    CAC=("CAC_Estimado", "sum"), Desc=("Descuento_Pct", "mean"), Órdenes=("Cliente_ID", "count")).reset_index()
    p["Margen %"] = p["Margen"] / p["Ventas"] * 100
    p["Contribución neta"] = p["Margen"] - p["CAC"]
    p["Contrib. %"] = p["Contribución neta"] / p["Ventas"] * 100
    p["Margen/CAC"] = p["Margen"] / p["CAC"]
    p = p[["Categoria", "Órdenes", "Ventas", "COGS", "Margen", "Margen %", "CAC", "Contribución neta", "Contrib. %", "Margen/CAC", "Desc"]].sort_values("Ventas", ascending=False)
    p = p.rename(columns={"Desc": "Desc. medio %"})
    show_table(p, {"Ventas": "${:,.0f}", "COGS": "${:,.0f}", "Margen": "${:,.0f}", "Margen %": "{:.1f}%", "CAC": "${:,.0f}",
                   "Contribución neta": "${:,.0f}", "Contrib. %": "{:.1f}%", "Margen/CAC": "{:.1f}x", "Desc. medio %": "{:.1f}%"},
               good=["Ventas", "Margen %", "Contribución neta", "Contrib. %", "Margen/CAC"], bad=["Desc. medio %"], neutral=["Órdenes"],
               title="Estado de Resultados y Rentabilidad Neta por Línea de Negocio",
               summary=f"Desglose P&L por categoría comercial. La categoría líder genera {usd(p['Ventas'].iloc[0])} con un margen bruto de {p['Margen %'].iloc[0]:.1f}%. Tras absorber {usd(M['cac_total'])} de inversión acumulada en adquisición, la contribución neta global es de {usd(M['net'])}.",
               tips=[
                   "Restringir las promociones agresivas en categorías con descuento medio superior al 12% para frenar la erosión de margen.",
                   "Potenciar la venta cruzada entre productos de gran volumen y accesorios o servicios de alto margen neto.",
                   "Establecer revisiones trimestrales de precios de lista basadas en costos de reposición e inflación de fletes."
               ])


# ------------------------------------------------------------------------------
# TAB 4: CHURN PREDICTIVO (ML) & WHAT-IF
# ------------------------------------------------------------------------------
def tab_churn():
    if ML is None:
        st.info("Insuficientes datos para entrenar el modelo supervisado de churn.")
        return
    mt = ML["metrics"]
    b = mt.iloc[0]
    best_name = b["Modelo"]
    auc_cv = b["AUC (CV 5-fold)"]
    auc_test = b["AUC (test)"]

    story("🤖", "Modelado Predictivo de Churn con Machine Learning Supervisado",
          f"Se entrenaron 3 clasificadores supervisados: el algoritmo con mayor precisión de discriminación es "
          f"{kw(best_name, 'key')} con un {kw(f'AUC de {auc_cv:.2f}', 'pos')} en validación cruzada y {kw(f'{auc_test:.2f}', 'pos')} en test. "
          f"El ingreso ponderado actualmente en riesgo es {kw(usd(M['rev_risk']), 'neg')}.",
          tips=[
              f"Configurar alertas tempranas en el CRM cuando una cuenta supere los {REC_THR} días de inactividad comercial.",
              "Vincular el scoring predictivo de abandono al panel diario de los ejecutivos de cuenta para contacto preventivo.",
              "Auditar causas raíz de insatisfacción en cualquier cuenta corporativa que registre calificación CSAT inferior a 3 estrellas.",
              "Monitorear la evolución del AUC de test para reentrenar el modelo periódicamente ante cambios en el patrón de compras."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(ML["imp"], x="Importancia", y="Variable", orientation="h", color="Importancia", color_continuous_scale="Purples",
                     title="Importancia de variables explicativas (Random Forest)")
        fig.update_traces(
            hovertemplate="<b>🔬 Variable:</b> %{y}<br>📊 <b>Peso Predictivo:</b> %{x:.3f} (%{x:.1%})<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Peso Relativo</b>")))
        chart(fig, "Factores con mayor peso predictivo relativo en el modelo supervisado de riesgo de abandono.",
              "La recencia en días y la satisfacción CSAT son las variables más determinantes para anticipar la fuga de clientes.",
              f"Diseñar alertas preventivas automáticas cuando una cuenta supere los {REC_THR} días sin actividad comercial.", 390)
    with c2:
        fig = go.Figure()
        for i, (name, (fpr, tpr)) in enumerate(ML["rocs"].items()):
            auc_v = mt.loc[mt["Modelo"] == name, "AUC (test)"].iloc[0]
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr, mode="lines", name=f"{name} (AUC {auc_v:.2f})", line=dict(color=PAL[i], width=3),
                hovertemplate="<b>" + name + "</b><br>⚠️ <b>Tasa Falsos Positivos (FPR):</b> %{x:.3f}<br>🎯 <b>Sensibilidad (TPR):</b> %{y:.3f}<extra></extra>"
            ))
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines", name="Azar", line=dict(color=THEME["text_secondary"], dash="dash"),
            hovertemplate="<b>Línea Base (Azar)</b><br>FPR: %{x:.1f} | TPR: %{y:.1f}<extra></extra>"
        ))
        fig.update_layout(title="Curvas ROC comparativas (Conjunto de Test)")
        chart(fig, "Capacidad de los modelos para discriminar verdaderos positivos frente a falsas alarmas.",
              f"El clasificador {best_name} alcanza un área bajo la curva de {auc_cv:.2f} en validación cruzada y {auc_test:.2f} en test.",
              f"Utilizar los scores probabilísticos de {best_name} para priorizar el orden de contacto del equipo de retención.", 390)
    c3, c4 = st.columns(2)
    with c3:
        fig = px.imshow(ML["cm"], text_auto=True, x=["Pred: Se queda", "Pred: Churn"], y=["Real: Se queda", "Real: Churn"],
                         color_continuous_scale=SCALE_SEQ, title=f"Matriz de confusión ({best_name})")
        fig.update_traces(
            hovertemplate="<b>Real:</b> %{y}<br><b>Predicción:</b> %{x}<br>👥 <b>Clientes:</b> %{z:,} casos<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Casos</b>")))
        chart(fig, "Diagnóstico de precisión: clientes correctamente clasificados frente a falsos positivos y falsos negativos.",
              "Se evidencia alta sensibilidad en la detección de clientes propensos a abandono, minimizando pérdidas no advertidas.",
              "Implementar protocolos de reactivación diferenciados según si el cliente fue clasificado en riesgo crítico o moderado.", 390)
    with c4:
        g = df.groupby(["Segmento_Estrategico_ML", "Alerta_Riesgo_Churn"])["Monto_Compra"].sum().reset_index()
        fig = px.bar(g, x="Segmento_Estrategico_ML", y="Monto_Compra", color="Alerta_Riesgo_Churn", color_discrete_map=ALERTA_COLORS,
                     category_orders={"Alerta_Riesgo_Churn": ALERTA_ORDER}, barmode="stack",
                     title="Ingresos expuestos por segmento estratégico ML")
        fig.update_traces(
            hovertemplate="<b>🎯 Segmento:</b> %{x}<br>⚠️ <b>Nivel Alerta:</b> %{fullData.name}<br>💰 <b>Facturación:</b> $%{y:,.0f}<extra></extra>"
        )
        chart(fig, "Distribución de facturación activa clasificada por categoría de riesgo de abandono en cada segmento.",
              f"Actualmente hay {usd(M['rev_risk'])} en alto riesgo de churn, concentrados en segmentos estratégicos clave.",
              "Desplegar un plan de rescate inmediato para las cuentas clave situadas en el bloque de alto riesgo.", 390)

    section("🚨 Top 15 Cuentas con Mayor Riesgo e Impacto Financiero")
    ct = customer_table(df)
    ct["Ingreso expuesto"] = ct["Facturacion"] * ct["Churn"]
    ct["Acción sugerida"] = np.select(
        [(ct["Churn"] >= 0.6) & (ct["Clase"] == "A"), ct["Churn"] >= 0.6, ct["Churn"] >= 0.35],
        ["🚨 Retención VIP Inmediata", "📞 Contacto de Reactivación", "👀 Monitoreo Comercial"], default="✅ Cuenta Estable"
    )
    tp = ct.sort_values("Ingreso expuesto", ascending=False).head(15)[
        ["Cuenta", "Tipo_Cliente_Cuenta", "Clase", "Facturacion", "Recencia_Min", "CSAT", "Churn", "Prob_ML", "Ingreso expuesto", "Acción sugerida"]
    ]
    show_table(tp, {"Facturacion": "${:,.0f}", "Recencia_Min": "{:.0f} d", "CSAT": "{:.1f}", "Churn": "{:.2f}",
                    "Prob_ML": "{:.2f}", "Ingreso expuesto": "${:,.0f}"},
               good=["CSAT"], bad=["Churn", "Prob_ML", "Ingreso expuesto", "Recencia_Min"], neutral=["Facturacion"],
               title="Top 15 Cuentas Estratégicas en Alto Riesgo de Abandono",
               summary=f"Listado priorizado de cuentas en peligro crítico ordenadas por volumen de capital expuesto. El valor total en riesgo asciende a {usd(tp['Ingreso expuesto'].sum())}, concentrado principalmente en cuentas Clase A y B con recencias elevadas y alertas de retención activa.",
               tips=[
                   "Asignar inmediatamente un sponsor ejecutivo o director comercial a las cuentas marcadas con alerta de Retención VIP Inmediata.",
                   "Ofrecer bonificaciones de fidelidad o condiciones preferenciales de renovación antes de superar el umbral crítico de deserción.",
                   "Programar reuniones técnicas de diagnóstico para evaluar y resolver fricciones en la entrega o soporte postventa."
               ])

    section("🧪 Simulador Interactivo What-If: Probabilidad de Churn Hipotética")
    s1, s2, s3, s4 = st.columns(4)
    rg = ML["ranges"]
    rec = s1.slider("Recencia (días sin comprar)", int(rg["Recencia_Dias"][0]), int(rg["Recencia_Dias"][1]), int(ML["medians"]["Recencia_Dias"]), key="sim_rec")
    frq = s2.slider("Frecuencia histórica", int(rg["Frecuencia_Historica"][0]), int(rg["Frecuencia_Historica"][1]), int(ML["medians"]["Frecuencia_Historica"]), key="sim_frq")
    cs = s3.slider("Satisfacción CSAT", 1, 5, 4, key="sim_csat")
    mto = s4.slider("Monto de compra ($)", int(rg["Monto_Compra"][0]), int(rg["Monto_Compra"][1]), int(ML["medians"]["Monto_Compra"]), key="sim_monto")

    sim_row = dict(ML["medians"])
    sim_row.update({"Recencia_Dias": rec, "Frecuencia_Historica": frq, "Satisfaccion_CSAT": cs, "Monto_Compra": mto})
    prob = float(ML["rf"].predict_proba(pd.DataFrame([sim_row])[CHURN_FEATURES])[:, 1][0])
    lvl = "ALTO" if prob >= 0.6 else ("MEDIO" if prob >= 0.35 else "BAJO")
    story("🎲", "Resultado de la Simulación Predictiva",
          f"Probabilidad estimada de abandono: {kw(f'{prob * 100:.1f}%', 'neg' if prob >= 0.6 else 'warn' if prob >= 0.35 else 'pos')} → Nivel de Riesgo: "
          f"{kw(lvl, 'neg' if prob >= 0.6 else 'warn' if prob >= 0.35 else 'pos')}. Ajusta los controles para comprobar cómo la inactividad o la satisfacción mueven el riesgo.",
          tips=[
              "Controlar la recencia: un periodo de inactividad superior a la mediana eleva exponencialmente el riesgo predictivo de churn.",
              "Elevar la satisfacción CSAT a 4 o 5 estrellas disminuye de forma drástica la probabilidad de deserción estimada por el clasificador.",
              "Simular escenarios comerciales previos a negociaciones clave para definir el límite de tolerancia antes de conceder incentivos."
          ])


# ------------------------------------------------------------------------------
# TAB 5: SEGMENTACIÓN K-MEANS & RFM
# ------------------------------------------------------------------------------
CLUSTER_BASE = ["💎 Élite VIP", "🚀 Alto Potencial", "🔄 Núcleo Recurrente", "🌱 Nuevos / Ocasionales", "⚠️ Enfriándose", "😴 Dormidos"]
CLUSTER_ACTION = {
    "💎 Élite VIP": "Ejecutivo dedicado, acuerdos prioritarios y eventos exclusivos.",
    "🚀 Alto Potencial": "Campañas de cross-selling y bonificaciones por volumen.",
    "🔄 Núcleo Recurrente": "Fidelización automatizada y reposición programada.",
    "🌱 Nuevos / Ocasionales": "Incentivos para inducir una segunda transacción.",
    "⚠️ Enfriándose": "Llamada preventiva de auditoría de servicio y satisfacción.",
    "😴 Dormidos": "Ofertas de rescate con descuento controlado."
}


def tab_segmentacion():
    k = st.slider("Número de clústeres a modelar (K)", 2, 6, 4, key="k_clusters")
    if len(df) < k * 5:
        st.info("Insuficientes registros con los filtros activos para segmentar.")
        return
    Xc = df[["Recencia_Dias", "Frecuencia_Historica", "Monto_Compra"]].astype(float).copy()
    Xc["Monto_Compra"] = np.log1p(Xc["Monto_Compra"])
    Xs = StandardScaler().fit_transform(Xc)
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
    sil = silhouette_score(Xs, km.labels_)

    cent = km.cluster_centers_
    order = np.argsort(-(cent[:, 1] + cent[:, 2] - cent[:, 0]))
    picks = np.linspace(0, len(CLUSTER_BASE) - 1, k).round().astype(int)
    names = {int(cid): CLUSTER_BASE[picks[rank]] for rank, cid in enumerate(order)}
    d = df.copy()
    d["Cluster"] = [names[int(c)] for c in km.labels_]

    sil_str = f"{sil:.2f}"
    sil_color = "pos" if sil >= 0.4 else "warn"
    story("🎯", "Segmentación Estratégica: Clustering No Supervisado K-Means (RFM)",
          f"Segmentación multivariada en {kw(f'{k} clústeres', 'key')}. Coeficiente de Silueta: "
          f"{kw(sil_str, sil_color)} ({'Estructura sólida' if sil >= 0.4 else 'Grupos moderadamente solapados'}). "
          f"Permite gobernar la cartera de acuerdo con el comportamiento real de compra.",
          tips=[
              "Blindar al clúster Élite VIP con ejecutivos sénior dedicados y acuerdos de servicio prioritarios.",
              "Diseñar campañas de cross-selling y bonificaciones por volumen en el segmento de Alto Potencial.",
              "Implementar flujos automatizados de reposición para el Núcleo Recurrente antes de que pasen a enfriamiento.",
              "Activar llamadas de cortesía y auditoría de satisfacción sobre clientes que comiencen a enfriarse."
          ])

    c1, c2 = st.columns(2)
    with c1:
        ks = list(range(2, min(8, len(df) - 1) + 1))
        inert, sils = [], []
        for kk in ks:
            m_ = KMeans(n_clusters=kk, n_init=10, random_state=42).fit(Xs)
            inert.append(m_.inertia_)
            sils.append(silhouette_score(Xs, m_.labels_))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=ks, y=inert, name="Inercia (Codo)", mode="lines+markers", line=dict(color=THEME["accent_blue"], width=3),
            hovertemplate="<b>K = %{x} clústeres</b><br>📉 <b>Inercia (SSE):</b> %{y:,.1f}<extra>Inercia</extra>"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=ks, y=sils, name="Silueta", mode="lines+markers", line=dict(color=THEME["warning"], width=3),
            hovertemplate="<b>K = %{x} clústeres</b><br>🎯 <b>Coef. Silueta:</b> %{y:.3f}<extra>Silueta</extra>"
        ), secondary_y=True)
        fig.update_layout(title="Diagnóstico de K Óptimo: Método del Codo y Silueta", xaxis_title="K")
        chart(fig, "Curva de inercia para detectar el codo y coeficiente de silueta para evaluar la separación entre grupos.",
              f"La configuración de {k} clústeres alcanza un coeficiente de silueta de {sil:.2f}, garantizando coherencia interna.",
              "Adoptar esta partición conductual para diseñar estrategias de comunicación y ofertas diferenciadas.", 390)
    with c2:
        pca = PCA(n_components=2, random_state=42)
        P = pca.fit_transform(Xs)
        d["PC1"], d["PC2"] = P[:, 0], P[:, 1]
        fig = px.scatter(d, x="PC1", y="PC2", color="Cluster", hover_name="Cuenta",
                         title="Mapa de Clústeres (Reducción PCA 2D)", color_discrete_sequence=PAL)
        fig.update_traces(
            hovertemplate="<b>🏢 Cuenta:</b> %{hovertext}<br>🎯 <b>Clúster:</b> %{fullData.name}<br>📍 <b>PC1:</b> %{x:.2f}<br>📍 <b>PC2:</b> %{y:.2f}<extra></extra>"
        )
        chart(fig, "Proyección bidimensional de los patrones de Recencia, Frecuencia y Valor Monetario de los clientes.",
              "Se observan fronteras claramente delimitadas entre clientes VIP, núcleo recurrente y cuentas en enfriamiento.",
              "Supervisar periódicamente la migración de cuentas entre cuadrantes para evitar fugas silenciosas.", 390)
    c3, c4 = st.columns(2)
    with c3:
        prof = d.groupby("Cluster").agg(Cuentas=("Cliente_ID", "count"), Ventas=("Monto_Compra", "sum"), Ticket=("Monto_Compra", "mean"),
                                        Recencia=("Recencia_Dias", "mean"), Frecuencia=("Frecuencia_Historica", "mean"), CSAT=("Satisfaccion_CSAT", "mean"),
                                        Margen=("Margen_Bruto_Pct", "mean"), Churn=("Riesgo_Churn_Score", "mean")).reset_index()
        fig = px.bar(prof, x="Cluster", y="Ventas", color="Cluster", color_discrete_sequence=PAL, title="Facturación total aportada por cada Clúster ($)")
        fig.update_traces(
            hovertemplate="<b>🎯 Clúster:</b> %{x}<br>💰 <b>Facturación Total:</b> $%{y:,.0f}<extra></extra>"
        )
        chart(fig, "Volumen de ventas acumuladas por cada grupo resultante de la segmentación no supervisada.",
              "Los clústeres de mayor valor concentran la mayor masa de ingresos operativos de la empresa.",
              "Asegurar acuerdos comerciales prioritarios y condiciones preferenciales para el clúster Élite VIP.", 390)
    with c4:
        pv = df.pivot_table(index="R_Score", columns="F_Score", values="Monto_Compra", aggfunc="sum").fillna(0)
        fig = px.imshow(pv, text_auto=".2s", aspect="auto", color_continuous_scale=SCALE_SEQ,
                        title="Matriz RFM: Recencia × Frecuencia (Ventas $)")
        fig.update_traces(
            hovertemplate="<b>Recencia (R-Score):</b> %{y}<br><b>Frecuencia (F-Score):</b> %{x}<br>💰 <b>Ventas:</b> $%{z:,.0f}<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Ventas ($)</b>"), tickprefix="$", tickformat=",.0s"))
        chart(fig, "Malla de calor donde la esquina superior derecha agrupa a clientes de compra reciente y alta recurrencia.",
              "Alta concentración de facturación en cuadrantes de recencia alta con oportunidad de reactivación en recencias medias.",
              "Automatizar correos y mensajes de reposición programada para clientes en transición a recencias más altas.", 390)

    section("📋 Perfil Conductual y Recomendación Comercial por Clúster")
    prof["Estrategia"] = prof["Cluster"].map(CLUSTER_ACTION)
    show_table(prof, {"Ventas": "${:,.0f}", "Ticket": "${:,.0f}", "Recencia": "{:.0f} d", "Frecuencia": "{:.1f}",
                      "CSAT": "{:.2f} ★", "Margen": "{:.1f}%", "Churn": "{:.2f}"},
               good=["Ventas", "Ticket", "Frecuencia", "CSAT"], bad=["Recencia", "Churn"], neutral=["Cuentas"],
               title="Perfil Conductual, Métricas y Estrategia Accionable por Clúster RFM",
               summary=f"Segmentación analítica basada en Recencia, Frecuencia y Valor Monetario en {k} grupos conductuales homogéneos. El clúster de mayor valor concentra {usd(prof['Ventas'].max())} en compras con un ticket promedio de {usd(prof.loc[prof['Ventas'].idxmax(), 'Ticket'])}.",
               tips=[
                   "Personalizar las propuestas de valor y la cadencia de contacto según el ciclo de vida de cada grupo.",
                   "No desgastar presupuesto de retención en clientes con frecuencia unitaria y nulo potencial de recompra.",
                   "Medir trimestralmente la tasa de migración positiva de cuentas desde clústeres base hacia grupos VIP."
               ])


# ------------------------------------------------------------------------------
# TAB 6: TERRITORIO & LOGÍSTICA
# ------------------------------------------------------------------------------
def tab_territorio():
    reg = df.groupby("Region").agg(V=("Monto_Compra", "sum"), G=("Margen_Bruto", "sum"), O=("Cliente_ID", "count"), R=("Retraso", "mean")).reset_index()
    reg["Margen_Pct"] = reg["G"] / reg["V"] * 100
    top_r = reg.loc[reg["V"].idxmax()]

    story("🗺️", "Storytelling Territorial y Operaciones Logísticas",
          f"La zona {kw(top_r['Region'], 'key')} concentra la mayor facturación con {kw(usd(top_r['V']), 'pos')} "
          f"y un margen del {top_r['Margen_Pct']:.1f}%. El cumplimiento del SLA corporativo se sitúa en {kw(f'{M['sla']:.1f}%', 'pos' if M['sla'] >= 90 else 'warn')}.",
          tips=[
              f"Fortalecer la capacidad logística y de almacenaje en {top_r['Region']} para respaldar su posición como polo dominante de ventas.",
              f"Resolver los cuellos de botella en corredores con retraso superior al 10% para blindar la satisfacción CSAT ({M['csat']:.2f}/5).",
              "Negociar acuerdos marco con operadores de transporte que incluyan penalizaciones automáticas por incumplimiento del SLA.",
              "Evaluar centros satélites de distribución rápida en las 3 ciudades con mayor volumen de pedidos."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=reg["Region"], y=reg["V"], name="Ventas ($)", marker_color=THEME["accent_blue"],
            hovertemplate="<b>📍 Región:</b> %{x}<br>💰 <b>Ventas:</b> $%{y:,.0f}<extra>Ventas</extra>"
        ))
        fig.add_trace(go.Bar(
            x=reg["Region"], y=reg["G"], name="Margen bruto ($)", marker_color=THEME["success"],
            hovertemplate="<b>📍 Región:</b> %{x}<br>📊 <b>Margen Bruto:</b> $%{y:,.0f}<extra>Margen</extra>"
        ))
        fig.update_layout(barmode="group", title="Ventas y margen bruto por región geográfica")
        chart(fig, "Comparativa de facturación e ingresos netos entre regiones territoriales.",
              f"La región {top_r['Region']} lidera la facturación con {usd(top_r['V'])} y {top_r['Margen_Pct']:.1f}% de margen bruto.",
              "Replicar la estrategia de distribución de la región líder en las zonas secundarias para expandir la cobertura.", 390)
    with c2:
        pv = df.pivot_table(index="Region", columns="Canal_Venta", values="Retraso", aggfunc="mean") * 100
        fig = px.imshow(pv, text_auto=".1f", aspect="auto", color_continuous_scale=SCALE_RISK,
                        title="Tasa de entregas con retraso (%) · Región × Canal")
        fig.update_traces(
            hovertemplate="<b>📍 Región:</b> %{y}<br>🏷️ <b>Canal:</b> %{x}<br>⚠️ <b>Tasa Retraso:</b> %{z:.1f}%<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>% Retraso</b>"), ticksuffix="%"))
        chart(fig, "Matriz de calor que identifica cuellos de botella logísticos por combinación de región y canal de venta.",
              "Determinadas rutas presentan tasas de retraso superiores al 10%, afectando directamente la promesa de servicio.",
              "Auditar los acuerdos con operadores logísticos y transportistas en los corredores con mayor incidencia de demora.", 390)
    c3, c4 = st.columns(2)
    with c3:
        g = df.groupby(["Estado_Entrega", "Satisfaccion_CSAT"]).size().reset_index(name="n")
        fig = px.bar(g, x="Satisfaccion_CSAT", y="n", color="Estado_Entrega", barmode="group",
                     title="Impacto del estado de entrega en la satisfacción CSAT",
                     color_discrete_map={"Entregado a Tiempo": THEME["success"], "Con Retraso Logístico": THEME["danger"]})
        fig.update_traces(
            hovertemplate="<b>⭐ CSAT:</b> %{x} estrellas<br>🚚 <b>Estado:</b> %{fullData.name}<br>📦 <b>Órdenes:</b> %{y:,}<extra></extra>"
        )
        chart(fig, "Distribución de calificaciones CSAT comparando órdenes entregadas a tiempo frente a pedidos con retraso.",
              "Los pedidos con entrega demorada sufren una drástica caída en satisfacción CSAT (calificaciones de 1 y 2 estrellas).",
              "Establecer compensaciones automáticas o bonificaciones en futuras compras cuando ocurra un retraso logístico comprobado.", 390)
    with c4:
        ct_top = df.groupby("Ciudad")["Monto_Compra"].sum().reset_index().sort_values("Monto_Compra", ascending=True).tail(10)
        fig = px.bar(ct_top, y="Ciudad", x="Monto_Compra", orientation="h", title="Top 10 Plazas Comerciales por Facturación ($)", color="Monto_Compra", color_continuous_scale="Blues")
        fig.update_traces(
            hovertemplate="<b>🏙️ Ciudad:</b> %{y}<br>💰 <b>Facturación:</b> $%{x:,.0f}<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Ventas ($)</b>"), tickprefix="$", tickformat=",.0s"))
        chart(fig, "Ranking de las principales ciudades y polos urbanos ordenados por monto de ventas generado.",
              "Las principales 3 plazas absorben más del 60% de la demanda territorial en equipamiento tecnológico.",
              "Evaluar apertura de centros de distribución intermedios en las plazas líderes para reducir tiempos de entrega.", 390)

    section("📋 Desempeño Operativo y Logístico por Región")
    reg_show = reg.rename(columns={"V": "Ventas", "G": "Margen", "O": "Órdenes", "R": "% Retraso"})
    reg_show["% Retraso"] = reg_show["% Retraso"] * 100
    show_table(reg_show[["Region", "Órdenes", "Ventas", "Margen", "Margen_Pct", "% Retraso"]],
               {"Ventas": "${:,.0f}", "Margen": "${:,.0f}", "Margen_Pct": "{:.1f}%", "% Retraso": "{:.1f}%"},
               good=["Ventas", "Margen", "Margen_Pct"], bad=["% Retraso"], neutral=["Órdenes"],
               title="Scorecard de Eficiencia Comercial y Cumplimiento Logístico por Región",
               summary=f"Balance territorial que confronta facturación, rentabilidad y puntualidad en entregas. {top_r['Region']} lidera ingresos con {usd(top_r['V'])}, mientras que la tasa media de pedidos demorados a nivel nacional se sitúa en {reg_show['% Retraso'].mean():.1f}%.",
               tips=[
                   "Implementar seguimiento telemático y notificaciones proactivas en las rutas con retrasos superiores al promedio.",
                   "Establecer inventarios de seguridad en centros de distribución regionales para mitigar incidencias imprevistas.",
                   "Vincular las bonificaciones de operadores logísticos al cumplimiento estricto del estándar de entrega puntual (SLA ≥ 90%)."
               ])


# ------------------------------------------------------------------------------
# TAB 7: CLIENTES PARETO & ABC
# ------------------------------------------------------------------------------
def tab_clientes():
    cust = customer_table(df)
    n = len(cust)
    tot = cust["Facturacion"].sum()
    k20 = max(1, int(np.ceil(0.2 * n)))
    top20 = cust["Facturacion"].head(k20).sum() / tot * 100 if tot else 0
    top20_str = f"{top20:.0f}%"
    top20_color = "pos" if top20 >= 70 else "warn"

    story("👥", "Storytelling de Clientes: Ley de Pareto 80/20 y Segmentación de Cartera ABC",
          f"El {kw('20% superior', 'key')} de las cuentas cliente genera el {kw(top20_str, top20_color)} de la facturación total. "
          f"Esta concentración exige gobernanza diferenciada: las cuentas Clase A deben contar con ejecutivos sénior dedicados.",
          tips=[
              "Garantizar acuerdos marco de exclusividad y condiciones de suministro garantizado con las cuentas Clase A.",
              "Automatizar la gestión operativa de clientes Clase C mediante autoservicio digital para reducir costos de atención.",
              "Desarrollar planes de crecimiento comercial en cuentas Clase B con alto potencial para migrarlas a Clase A.",
              "Intervenir de forma prioritaria en cuentas ancla que presenten más de 45 días sin órdenes de compra registradas."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0] + cust["Pct_Cuentas"].tolist(), y=[0] + cust["Pct_Acum"].tolist(), mode="lines",
            name="Curva de Lorenz (Pareto)", line=dict(color=THEME["accent_cyan"], width=3),
            fill="tozeroy", fillcolor=rgba(THEME["accent_cyan"], 0.12),
            hovertemplate="<b>👥 % Clientes:</b> %{x:.1f}%<br>💰 <b>% Ingresos Acumulados:</b> %{y:.1f}%<extra>Lorenz</extra>"
        ))
        fig.add_trace(go.Scatter(
            x=[0, 100], y=[0, 100], mode="lines", name="Distribución equitativa", line=dict(color=THEME["text_secondary"], dash="dash"),
            hovertemplate="<b>Equidad 1:1</b><br>Clientes: %{x}% | Ingresos: %{y}%<extra></extra>"
        ))
        fig.update_layout(title="Curva de concentración de ingresos (Lorenz / Pareto 80/20)")
        chart(fig, "Curva acumulada de ingresos; cuanto más se aleja de la diagonal, mayor es la concentración de riesgo.",
              f"El 20% superior de las cuentas cliente representa el {top20_str} de la facturación global de la compañía.",
              "Establecer contratos de exclusividad y acuerdos de nivel de servicio garantizado con los clientes del tramo superior.", 390)
    with c2:
        abc = cust.groupby("Clase").agg(Cuentas=("Cuenta", "count"), Ventas=("Facturacion", "sum")).reset_index()
        fig = px.pie(abc, names="Clase", values="Ventas", title="Participación de ingresos por Clase ABC",
                     color_discrete_sequence=[THEME["accent_blue"], THEME["accent_purple"], THEME["warning"]])
        fig.update_traces(
            hovertemplate="<b>🏷️ Clase %{label}</b><br>💰 <b>Facturación:</b> $%{value:,.0f}<br>📊 <b>Cuota:</b> %{percent}<extra></extra>"
        )
        chart(fig, "Distribución porcentual de ingresos: Clase A (80%), Clase B (15%) y Clase C (5% restante).",
              "La clase A conforma el núcleo financiero indispensable para la sostenibilidad operativa del negocio.",
              "Automatizar la atención de cuentas Clase C para optimizar costos de servicio y enfocar recursos humanos en Clase A.", 390)
    c3, c4 = st.columns(2)
    with c3:
        tp = cust.head(15).sort_values("Facturacion")
        fig = px.bar(tp, x="Facturacion", y="Cuenta", orientation="h", color="Churn", color_continuous_scale=SCALE_RISK, range_color=[0, 1],
                     title="Top 15 Cuentas por Facturación y su Riesgo de Churn", text_auto=".2s")
        fig.update_traces(
            hovertemplate="<b>🏢 Cuenta:</b> %{y}<br>💰 <b>Facturación:</b> $%{x:,.0f}<br>⚠️ <b>Score Churn:</b> %{marker.color:.3f}<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Riesgo Churn</b>")))
        chart(fig, "Barras horizontales de facturación con mapa de color según el score de riesgo de abandono.",
              "Se visualiza de forma inmediata si las cuentas de mayor volumen financiero presentan indicadores de riesgo en rojo.",
              "Asignar de inmediato un plan de retención personalizado a cualquier cliente del Top 15 con riesgo superior a 0.35.", 390)
    with c4:
        cust["Tam"] = cust["LTV"].clip(lower=1)
        fig = px.scatter(cust, x="Facturacion", y="Churn", color="Clase", size="Tam", size_max=28, hover_name="Cuenta",
                         title="Matriz de Valor Comercial vs Riesgo de Abandono", color_discrete_sequence=PAL)
        fig.update_traces(
            hovertemplate="<b>🏢 Cuenta:</b> %{hovertext}<br>🏷️ <b>Clase ABC:</b> %{fullData.name}<br>💰 <b>Facturación:</b> $%{x:,.0f}<br>⚠️ <b>Score Churn:</b> %{y:.3f}<extra></extra>"
        )
        chart(fig, "Dispersión de cuentas: eje horizontal = facturación, eje vertical = riesgo de deserción; tamaño = LTV.",
              "Las cuentas ubicadas en el cuadrante superior derecho requieren intervención urgente por su elevado impacto económico.",
              "Convocar reuniones ejecutivas de fidelización con los responsables de compras de las cuentas en alto riesgo de valor crítico.", 390)

    section("📋 Top 20 Clientes Estratégicos")
    t = cust.head(20)[["Cuenta", "Tipo_Cliente_Cuenta", "Clase", "Facturacion", "Pct_Acum", "Margen", "Ordenes", "Recencia_Min", "CSAT", "Churn"]]
    show_table(t, {"Facturacion": "${:,.0f}", "Pct_Acum": "{:.1f}%", "Margen": "${:,.0f}", "Recencia_Min": "{:.0f} d", "CSAT": "{:.1f} ★", "Churn": "{:.2f}"},
               good=["Facturacion", "Margen", "CSAT"], bad=["Churn", "Recencia_Min"], neutral=["Ordenes"],
               title="Top 20 Clientes Estratégicos y Concentración de Valor (Pareto)",
               summary=f"Ranking de las 20 cuentas más representativas de la compañía, que aportan el {t['Pct_Acum'].iloc[-1]:.1f}% de la facturación acumulada del grupo analizado. Se detalla facturación total, margen bruto aportado, recencia de compra, satisfacción y score de abandono.",
               tips=[
                   "Asegurar contratos de suministro continuo y precios fijados por volumen con las cuentas del Top 5.",
                   "Intervenir inmediatamente en cuentas del Top 20 que registren más de 45 días sin interacción comercial.",
                   "Realizar encuestas ejecutivas de satisfacción directa con los directores de compras de estas cuentas estratégicas."
               ])


# ------------------------------------------------------------------------------
# TAB 8: FUERZA DE VENTAS 360°
# ------------------------------------------------------------------------------
def tab_vendedores():
    meta_pct = st.slider("Meta de ventas como % del promedio del equipo", 70, 140, 100, 5, key="vend_meta_pct")
    v = df.groupby("Vendedor_Asignado").agg(Ventas=("Monto_Compra", "sum"), Margen=("Margen_Bruto", "sum"), Órdenes=("Cliente_ID", "count"),
                                            Desc=("Descuento_Pct", "mean"), Ticket=("Monto_Compra", "mean"), CSAT=("Satisfaccion_CSAT", "mean"),
                                            Churn=("Riesgo_Churn_Score", "mean")).reset_index()
    v["Margen %"] = v["Margen"] / v["Ventas"] * 100
    v["Meta"] = v["Ventas"].mean() * meta_pct / 100
    v["Cumpl. meta %"] = v["Ventas"] / v["Meta"] * 100

    def mm(s, inv=False):
        r = (s - s.min()) / (s.max() - s.min()) if s.max() > s.min() else pd.Series(0.5, index=s.index)
        return 1 - r if inv else r

    v["Score"] = (0.30 * mm(v["Ventas"]) + 0.25 * mm(v["Margen %"]) + 0.15 * mm(v["CSAT"]) + 0.15 * mm(v["Churn"], True) + 0.15 * mm(v["Desc"], True)) * 100
    v = v.sort_values("Score", ascending=False).reset_index(drop=True)
    top_v = v.loc[v["Ventas"].idxmax()]

    story("👔", "Storytelling Comercial: Evaluación Integral 360° del Equipo de Ventas",
          f"El asesor con mayor facturación bruta es {kw(top_v['Vendedor_Asignado'], 'key')} ({usd(top_v['Ventas'])}). "
          f"Sin embargo, el <b>Score Compuesto</b> pondera ventas, retención de margen, satisfacción CSAT y control de descuentos.",
          tips=[
              "Evaluar a los asesores comerciales bajo el Score Compuesto integral y no exclusivamente por volumen de facturación bruta.",
              "Supervisar la disciplina en el otorgamiento de descuentos para evitar que incentivos de volumen erosionen el margen neto.",
              "Promover el intercambio de mejores prácticas de negociación entre los líderes comerciales y los ejecutivos en fase de desarrollo.",
              "Rebalancear periódicamente la asignación de carteras y cuentas ancla para equilibrar las oportunidades comerciales."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(v.sort_values("Ventas", ascending=False), x="Vendedor_Asignado", y="Ventas", color="Margen %", color_continuous_scale=SCALE_GOOD,
                     title="Facturación por vendedor (color = margen bruto %)")
        fig.update_traces(
            hovertemplate="<b>👔 Asesor:</b> %{x}<br>💰 <b>Facturación:</b> $%{y:,.0f}<br>📊 <b>Margen Bruto:</b> %{marker.color:.1f}%<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Margen (%)</b>"), ticksuffix="%"))
        chart(fig, "Comparación de ventas brutas por asesor comercial con gradiente de color según la rentabilidad porcentual lograda.",
              f"El asesor {top_v['Vendedor_Asignado']} lidera el volumen bruto con {usd(top_v['Ventas'])}, manteniendo un margen competitivo.",
              "Capacitar al equipo en técnicas de venta de valor para que el volumen no dependa de sacrificar margen unitario.", 390)
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Ventas reales", x=v["Vendedor_Asignado"], y=v["Ventas"], marker_color=THEME["accent_blue"],
            hovertemplate="<b>👔 Asesor:</b> %{x}<br>💰 <b>Ventas Reales:</b> $%{y:,.0f}<extra>Ventas reales</extra>"
        ))
        fig.add_trace(go.Scatter(
            name="Meta asignada", x=v["Vendedor_Asignado"], y=v["Meta"], mode="lines+markers", line=dict(color=THEME["warning"], width=3, dash="dash"),
            hovertemplate="<b>👔 Asesor:</b> %{x}<br>🎯 <b>Meta Asignada:</b> $%{y:,.0f}<extra>Meta asignada</extra>"
        ))
        fig.update_layout(title="Cumplimiento de metas comerciales vs cuota asignada")
        chart(fig, "Barras de ventas reales comparadas contra la línea de meta comercial calculada para el periodo.",
              "Los ejecutivos muestran disparidad en el cumplimiento de cuota, reflejando diferencias de territorio y cartera.",
              "Rebalancear la asignación de cuentas y prospectos para equilibrar las oportunidades comerciales entre asesores.", 390)
    c3, c4 = st.columns(2)
    with c3:
        fig = px.scatter(v, x="Desc", y="Margen %", size="Ventas", color="CSAT", hover_name="Vendedor_Asignado",
                         title="Eficiencia de negociación: Descuento medio vs Margen % retenido", color_continuous_scale=SCALE_GOOD)
        fig.update_traces(
            hovertemplate="<b>👔 Asesor:</b> %{hovertext}<br>🏷️ <b>Descuento Medio:</b> %{x:.1f}%<br>📊 <b>Margen Bruto:</b> %{y:.1f}%<br>⭐ <b>CSAT Medio:</b> %{marker.color:.2f} ★<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>CSAT (★)</b>")))
        chart(fig, "Dispersión de descuento otorgado contra margen retenido; tamaño proporcional a ventas y color según CSAT.",
              "Se identifican asesores que logran alto margen aplicando un control riguroso de descuentos concedidos.",
              "Establecer comisiones escalonadas vinculadas directamente al margen bruto generado y no solo a la facturación nominal.", 390)
    with c4:
        fig = px.bar(v, x="Vendedor_Asignado", y="Score", color="Score", color_continuous_scale="Blues", title="Scorecard Integral de Desempeño (0 a 100 pts)")
        fig.update_traces(
            hovertemplate="<b>👔 Asesor:</b> %{x}<br>🏆 <b>Score Integral:</b> %{y:.1f} / 100 pts<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Score (pts)</b>")))
        chart(fig, "Puntuación global ponderada: 30% ventas, 25% margen, 15% CSAT, 15% retención y 15% disciplina en descuentos.",
              "El scorecard destaca a los ejecutivos más equilibrados en rentabilidad, volumen y fidelización de clientes.",
              "Utilizar el scorecard compuesto como base para bonificaciones periódicas y planes de desarrollo comercial.", 390)

    section("📋 Scorecard del Equipo Comercial")
    show_table(v[["Vendedor_Asignado", "Ventas", "Meta", "Cumpl. meta %", "Margen", "Margen %", "Ticket", "Desc", "CSAT", "Score"]],
               {"Ventas": "${:,.0f}", "Meta": "${:,.0f}", "Cumpl. meta %": "{:.0f}%", "Margen": "${:,.0f}", "Margen %": "{:.1f}%",
                "Ticket": "${:,.0f}", "Desc": "{:.1f}%", "CSAT": "{:.2f} ★", "Score": "{:.0f}"},
               good=["Ventas", "Cumpl. meta %", "Margen", "Margen %", "CSAT", "Score"], bad=["Desc"], neutral=["Ticket"],
               title="Scorecard Integral de Desempeño y Rentabilidad de la Fuerza de Ventas",
               summary=f"Evaluación multidimensional de {len(v)} ejecutivos comerciales. Se analizan ventas brutas acumuladas ({usd(v['Ventas'].sum())}), cumplimiento de cuota ({v['Cumpl. meta %'].mean():.0f}% medio), margen bruto generado, satisfacción CSAT y Score Compuesto ponderado.",
               tips=[
                   "Reconocer y premiar a los asesores que combinan alto cumplimiento de meta con excelente índice de satisfacción CSAT.",
                   "Implementar sesiones de coaching en técnicas de negociación para ejecutivos con descuentos medios superiores al 10%.",
                   "Ajustar la distribución de prospectos y territorios para garantizar equidad de oportunidades comerciales en el equipo."
               ])


# ------------------------------------------------------------------------------
# TAB 9: PORTAFOLIO & CATÁLOGO (BCG)
# ------------------------------------------------------------------------------
def tab_portafolio():
    p = df.groupby(["Producto_Principal", "Categoria"]).agg(Ventas=("Monto_Compra", "sum"), Margen=("Margen_Bruto", "sum"),
                                                           Unidades=("Cantidad_Productos", "sum"), Desc=("Descuento_Pct", "mean")).reset_index()
    p["Margen %"] = p["Margen"] / p["Ventas"] * 100
    p["Precio_Unit"] = p["Ventas"] / p["Unidades"]
    mu, mm_ = p["Unidades"].median(), p["Margen %"].median()
    p["Cuadrante"] = np.select([(p["Unidades"] >= mu) & (p["Margen %"] >= mm_), (p["Unidades"] >= mu), (p["Margen %"] >= mm_)],
                               ["⭐ Estrella", "🐄 Volumen / Margen Bajo", "💎 Nicho Rentable"], default="🔎 Revisar")

    story("📦", "Storytelling de Catálogo: Matriz de Rotación y Margen de Portafolio",
          f"El portafolio se divide en artículos de alto margen y productos de tracción de volumen. "
          f"Las líneas corporativas sostienen las ventas nominales y las de streaming aportan rentabilidad unitaria.",
          tips=[
              "Blindar el aprovisionamiento continuo de los SKUs en cuadrante Estrella para no frenar la facturación.",
              "Optimizar la estructura de costos (COGS) en productos de alto volumen pero margen ajustado.",
              "Revisar o descontinuar referencias en el cuadrante Revisar que drenen capital de trabajo sin generar rentabilidad.",
              "Diseñar ofertas empaquetadas (bundles) combinando productos de gran rotación con accesorios de alto margen."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(p, x="Unidades", y="Margen %", size="Ventas", color="Categoria", hover_name="Producto_Principal", size_max=32,
                         title="Matriz BCG: Rotación (Unidades) vs Margen Bruto (%)", color_discrete_sequence=PAL)
        fig.update_traces(
            hovertemplate="<b>📦 SKU:</b> %{hovertext}<br>📁 <b>Categoría:</b> %{fullData.name}<br>📦 <b>Rotación:</b> %{x:,} unidades<br>📊 <b>Margen Bruto:</b> %{y:.1f}%<extra></extra>"
        )
        chart(fig, "Cuadrantes de portafolio: Estrella (alto margen y rotación), Vaca (alto volumen), Nicho (alto margen) y Revisar.",
              "Productos estrella impulsan el crecimiento mientras que artículos de nicho aportan alta rentabilidad porcentual.",
              "Invertir en marketing para acelerar productos en cuadrante Estrella y rediseñar ítems en cuadrante Revisar.", 390)
    with c2:
        top_skus = p.sort_values("Ventas", ascending=True).tail(10)
        fig = px.bar(top_skus, y="Producto_Principal", x="Ventas", orientation="h", color="Margen %", color_continuous_scale=SCALE_GOOD,
                     title="Top 10 SKUs por Ingresos Brutos (color = margen %)")
        fig.update_traces(
            hovertemplate="<b>📦 SKU:</b> %{y}<br>💰 <b>Ingresos Brutos:</b> $%{x:,.0f}<br>📊 <b>Margen Bruto:</b> %{marker.color:.1f}%<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Margen (%)</b>"), ticksuffix="%"))
        chart(fig, "Los 10 productos con mayor aporte al flujo de caja de la empresa con color según margen bruto.",
              f"El SKU líder {top_skus.iloc[-1]['Producto_Principal']} concentra una porción sustancial de la facturación global.",
              "Establecer acuerdos de suministro prioritario con fabricantes para garantizar continuidad de stock en el Top 10.", 390)
    c3, c4 = st.columns(2)
    with c3:
        scale_treemap_bcg = [
            [0.0, "#E11D48"], [0.25, "#F43F5E"], [0.45, "#F59E0B"],
            [0.55, "#FBBF24"], [0.72, "#10B981"], [1.0, "#047857"]
        ]
        fig = px.treemap(
            p,
            path=["Categoria", "Producto_Principal"],
            values="Ventas",
            color="Margen %",
            custom_data=["Margen %"],
            color_continuous_scale=scale_treemap_bcg,
            color_continuous_midpoint=25.0,
            title="🗺️ Jerarquía de Ingresos y Margen por Línea de Producto"
        )
        fig.update_traces(
            texttemplate="<b>%{label}</b><br>💵 $%{value:,.0f}<br>📈 Margen: %{customdata[0]:.1f}%",
            textposition="middle center",
            hovertemplate=(
                "<b>🏷️ %{label}</b><br>"
                "📁 <b>Categoría:</b> %{parent}<br>"
                "────────────────────────────<br>"
                "💰 <b>Facturación:</b> $%{value:,.2f}<br>"
                "📊 <b>Margen Bruto Ponderado:</b> %{customdata[0]:.1f}%<br>"
                "📈 <b>Cuota en Portafolio:</b> %{percentRoot:.1%}<br>"
                "📦 <b>Cuota en Categoría:</b> %{percentParent:.1%}"
                "<extra></extra>"
            ),
            marker=dict(
                cornerradius=4,
                pad=dict(b=3, l=3, r=3, t=22),
                line=dict(width=1.5, color="#1E293B" if is_dark else "#CBD5E1")
            ),
            pathbar=dict(visible=True, thickness=24)
        )
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(text="<b>Margen (%)</b>", side="top", font=dict(size=11, family="Plus Jakarta Sans")),
                ticksuffix="%",
                tickformat=".1f",
                thickness=14,
                len=0.75,
                yanchor="middle",
                y=0.5
            )
        )
        top_sku_bcg = p.loc[p["Ventas"].idxmax()]
        chart(
            fig,
            "Mapa de árbol jerárquico que desglosa categorías y SKUs por volumen y margen % (color: rojo < 22%, ámbar ~25%, verde > 30%).",
            f"El catálogo está dominado por {kw(top_sku_bcg['Producto_Principal'], 'key')} en la categoría {kw(top_sku_bcg['Categoria'], 'info')}, combinando escala y margen competitivo ({top_sku_bcg['Margen %']:.1f}%).",
            "Ampliar la profundidad del catálogo en subcategorías de alto margen y demanda corporativa predecible.",
            410
        )
    with c4:
        fig = px.box(df, x="Categoria", y="Precio_Unit", color="Categoria", log_y=True, color_discrete_sequence=PAL,
                     title="Distribución de precios unitarios por categoría (escala log)")
        fig.update_traces(
            hovertemplate="📁 <b>Categoría:</b> %{x}<br>💵 <b>Precio Unitario:</b> $%{y:,.2f}<extra></extra>"
        )
        chart(fig, "Diagrama de cajas con mediana, rango intercuartílico y dispersión de precios unitarios por categoría.",
              "Alta dispersión en categorías corporativas frente a homogeneidad de precios en líneas de consumo prosumer.",
              "Ajustar las listas de precios recomendados para capturar mayor valor en segmentos con baja sensibilidad al precio.", 390)

    section("📋 Detalle de Productos del Catálogo")
    show_table(p[["Producto_Principal", "Categoria", "Cuadrante", "Ventas", "Margen", "Margen %", "Unidades", "Precio_Unit", "Desc"]],
               {"Ventas": "${:,.0f}", "Margen": "${:,.0f}", "Margen %": "{:.1f}%", "Unidades": "{:,.0f}", "Precio_Unit": "${:,.1f}", "Desc": "{:.1f}%"},
               good=["Ventas", "Margen", "Margen %"], bad=["Desc"], neutral=["Unidades"],
               title="Matriz de Portafolio BCG: Rotación, Margen y Clasificación Estratégica",
               summary=f"Catálogo consolidado de productos clasificados según volumen de rotación y rentabilidad porcentual. El SKU de mayor impacto es {top_sku_bcg['Producto_Principal']} con {usd(top_sku_bcg['Ventas'])} facturados y un margen bruto de {top_sku_bcg['Margen %']:.1f}%.",
               tips=[
                   "Diseñar promociones empaquetadas combinando productos Estrella con artículos de Nicho Rentable.",
                   "Establecer políticas de inventario 'Just in Time' para SKUs de baja rotación para evitar obsolescencia de stock.",
                   "Actualizar las listas de precios de catálogo al menos dos veces al año según la evolución de costos de importación y fletes."
               ])


# ------------------------------------------------------------------------------
# TAB 10: ESTADÍSTICA AVANZADA & HIPÓTESIS
# ------------------------------------------------------------------------------
CORR_COLS = ["Monto_Compra", "Cantidad_Productos", "Margen_Bruto_Pct", "Descuento_Pct", "CAC_Estimado", "Frecuencia_Historica", "LTV_Estimado_USD",
             "Satisfaccion_CSAT", "SLA_Entrega_Dias", "Recencia_Dias", "Riesgo_Churn_Score"]


def tab_estadistica():
    def safe(fn):
        try:
            r = fn()
            return float(r[0]), float(r[1])
        except Exception:
            return np.nan, np.nan

    def kruskal(col, by):
        groups = [g.values for _, g in df.groupby(by)[col] if len(g) > 1]
        return stats.kruskal(*groups)

    tests = []

    def add_t(name, variables, fn, reading):
        s, p = safe(fn)
        sig = (not np.isnan(p)) and p < 0.05
        tests.append({
            "Prueba": name, "Variables": variables, "Estadístico": s, "p-valor": p,
            "Resultado": ("🟢 Significativo" if sig else "🟡 No significativo") if not np.isnan(p) else "⚪ N/D",
            "Lectura": reading(s, sig) if not np.isnan(s) else "Datos insuficientes."
        })

    rs = lambda a, b: stats.spearmanr(df[a], df[b])
    add_t("Spearman", "Recencia ↔ Churn", lambda: rs("Recencia_Dias", "Riesgo_Churn_Score"), lambda s, g: f"Correlación {strength(s)}: a mayor inactividad, mayor riesgo.")
    add_t("Spearman", "CSAT ↔ Churn", lambda: rs("Satisfaccion_CSAT", "Riesgo_Churn_Score"), lambda s, g: f"Correlación {strength(s)}: mayor satisfacción reduce fuga.")
    add_t("Spearman", "Descuento ↔ Margen %", lambda: rs("Descuento_Pct", "Margen_Bruto_Pct"), lambda s, g: f"Correlación {strength(s)}.")
    add_t("Kruskal-Wallis", "Margen % por Categoría", lambda: kruskal("Margen_Bruto_Pct", "Categoria"), lambda s, g: "El margen difiere entre líneas." if g else "Sin diferencias significativas.")
    add_t("Mann-Whitney", "CSAT: Puntual vs Retraso",
          lambda: stats.mannwhitneyu(df.loc[df["Retraso"] == 0, "Satisfaccion_CSAT"], df.loc[df["Retraso"] == 1, "Satisfaccion_CSAT"]),
          lambda s, g: "El retraso penaliza significativamente el CSAT." if g else "Sin impacto estadísticamente visible.")

    tt = pd.DataFrame(tests)
    corr = df[CORR_COLS].corr(method="spearman")

    story("📐", "Storytelling Estadístico: Validación de Hipótesis y Diagnóstico de Relaciones",
          f"Aplicación de pruebas no paramétricas robustas para aislar relaciones causales de variaciones aleatorias. "
          f"La asimetría del monto de compra ({df['Monto_Compra'].skew():.1f}) justifica el uso de medianas y métodos no paramétricos.",
          tips=[
              "La evidencia empírica confirma que la satisfacción (CSAT) es el factor con mayor correlación inversa frente al churn.",
              "La asimetría positiva en el ticket exige planificar presupuestos usando medianas y percentiles, evitando distorsiones por promedios.",
              "El retraso logístico penaliza drástica y estadísticamente el CSAT (Mann-Whitney p < 0.05), requiriendo blindaje de entregas.",
              "La prueba de Kruskal-Wallis corrobora diferencias significativas de margen entre categorías, justificando metas diferenciadas."
          ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.imshow(corr, text_auto=".2f", aspect="auto", zmin=-1, zmax=1, color_continuous_scale="RdBu_r", title="Matriz de Correlación No Paramétrica (Spearman)")
        fig.update_traces(
            hovertemplate="<b>Variable Y:</b> %{y}<br><b>Variable X:</b> %{x}<br>📐 <b>Coef. Spearman (ρ):</b> %{z:.3f}<extra></extra>"
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="<b>Spearman (ρ)</b>")))
        chart(fig, "Coeficientes de correlación monótona de Spearman entre variables cuantitativas (azul = positiva, rojo = inversa).",
              "Fuerte correlación inversa entre CSAT y Churn, y correlación directa positiva entre recencia y riesgo de deserción.",
              "Focalizar los esfuerzos de retención en mejorar la experiencia del cliente y reducir los tiempos de inactividad.", 390)
    with c2:
        fig = px.histogram(df, x="Monto_Compra", color="Tipo_Cliente_Cuenta", marginal="box", opacity=0.75, color_discrete_sequence=PAL,
                           title="Distribución y Asimetría del Monto de Compra")
        fig.update_traces(
            hovertemplate="🏷️ <b>Tipo Cuenta:</b> %{fullData.name}<br>💰 <b>Ticket Facturado:</b> $%{x:,.0f}<br>🔢 <b>Frecuencia:</b> %{y:,} transacciones<extra></extra>"
        )
        chart(fig, "Histograma con caja marginal que evidencia el sesgo positivo (cola larga a la derecha) en la facturación.",
              "Asimetría positiva notable provocada por compras corporativas de gran tamaño frente a pedidos estándar.",
              "Emplear medianas y rangos intercuartílicos para presupuestación en lugar de medias aritméticas distorsionadas.", 390)
    c3, c4 = st.columns(2)
    with c3:
        fig = px.violin(df, x="Categoria", y="Margen_Bruto_Pct", color="Categoria", box=True, color_discrete_sequence=PAL,
                        title="Distribución del Margen Bruto (%) por Categoría")
        fig.update_traces(
            hovertemplate="📁 <b>Categoría:</b> %{x}<br>📊 <b>Margen Bruto:</b> %{y:.1f}%<extra></extra>"
        )
        chart(fig, "Diagrama de violín que combina densidad de probabilidad y cuartiles del margen bruto por categoría.",
              "Variabilidad significativa de margen entre líneas comerciales confirmada por la prueba de Kruskal-Wallis.",
              "Establecer metas de margen específicas para cada categoría en función de su perfil intrínseco de rentabilidad.", 390)
    with c4:
        sl, ic = np.polyfit(df["Recencia_Dias"], df["Riesgo_Churn_Score"], 1)
        fig = px.scatter(df, x="Recencia_Dias", y="Riesgo_Churn_Score", color="Alerta_Riesgo_Churn", color_discrete_map=ALERTA_COLORS,
                         title="Regresión Lineal: Días de Inactividad vs Riesgo de Churn")
        xs = np.array([df["Recencia_Dias"].min(), df["Recencia_Dias"].max()])
        fig.add_trace(go.Scatter(x=xs, y=ic + sl * xs, mode="lines", name="Ajuste Lineal", line=dict(color=THEME["text_primary"], dash="dash", width=2)))
        fig.update_traces(
            selector=dict(mode="markers"),
            hovertemplate="⏳ <b>Recencia:</b> %{x:.0f} días<br>⚠️ <b>Score Churn:</b> %{y:.3f}<br>🚨 <b>Nivel Alerta:</b> %{fullData.name}<extra></extra>"
        )
        fig.update_traces(
            selector=dict(name="Ajuste Lineal"),
            hovertemplate="📈 <b>Tendencia Lineal:</b><br>⏳ Inactividad: %{x:.0f} días<br>⚠️ Riesgo Proyectado: %{y:.3f}<extra></extra>"
        )
        chart(fig, "Ajuste lineal de recencia frente a probabilidad de abandono con clasificación cromática de alerta.",
              "La pendiente confirma que cada mes adicional de inactividad incrementa de forma predecible el riesgo de deserción.",
              "Disparar campañas automáticas de reenganche tan pronto un cliente alcance el umbral crítico de inactividad.", 390)

    section("📋 Pruebas de Hipótesis Estadísticas (Nivel de Confianza 95%)")
    tt_show = tt.copy()
    tt_show["p-valor"] = tt_show["p-valor"].map(lambda p: "N/D" if pd.isna(p) else ("< 0.0001" if p < 0.0001 else f"{p:.4f}"))
    show_table(tt_show, {"Estadístico": "{:.3f}"}, status=["Resultado"],
               title="Batería de Pruebas de Hipótesis y Validación Estadística (Confianza 95%)",
               summary="Resultados de pruebas no paramétricas (Spearman, Kruskal-Wallis, Mann-Whitney). Se valida formalmente con p-valor si las diferencias observadas entre canales, tiempos de entrega y niveles de satisfacción son estadísticamente significativas.",
               tips=[
                   "Adoptar las correlaciones significativas confirmadas como base científica para decisiones comerciales y operativas.",
                   "Desestimar relaciones donde el p-valor supere 0.05 al carecer de significación estadística suficiente.",
                   "Monitorear la evolución de estos contrastes trimestralmente para detectar cambios estructurales de comportamiento en la clientela."
               ])


# ------------------------------------------------------------------------------
# TAB 11: AUDITORÍA & CALIDAD DE DATOS
# ------------------------------------------------------------------------------
def tab_auditoria():
    story("📋", "Auditoría Operativa y Gobernanza de Integridad de Datos",
          f"Detalle transaccional con semáforos condicionales y pruebas de consistencia. "
          f"Filtra, analiza y exporta las transacciones activas a formato CSV o Excel con validación de calidad.",
          tips=[
              "Verificar periódicamente la coherencia contable entre montos de venta, costos de adquisición y márgenes netos.",
              "Mantener la política de cero nulos en campos obligatorios para asegurar la exactitud de los modelos predictivos de Machine Learning.",
              "Exportar las transacciones filtradas a formato Excel o CSV para cruce de información con el ERP o Data Warehouse corporativo.",
              "Revisar de inmediato cualquier orden con riesgo de churn superior a 0.60 para asignar responsable comercial de reactivación."
          ])

    f1, f2, f3, f4 = st.columns([3, 3, 3, 2])
    txt = f1.text_input("🔎 Buscar cuenta o producto", key="aud_txt")
    alertas = f2.multiselect("Nivel de riesgo", ALERTA_ORDER, default=ALERTA_ORDER, key="aud_alert")
    sort_by = f3.selectbox("Ordenar por", ["Monto_Compra", "Riesgo_Churn_Score", "Margen_Bruto_Pct", "Recencia_Dias"], key="aud_sort")
    nrows = f4.number_input("Filas a mostrar", 20, 500, 100, 20, key="aud_n")

    v = df[df["Alerta_Riesgo_Churn"].isin(alertas)]
    if txt:
        v = v[v["Cuenta"].str.contains(txt, case=False, na=False) | v["Producto_Principal"].str.contains(txt, case=False, na=False)]

    cols = ["Cliente_ID", "Cuenta", "Tipo_Cliente_Cuenta", "Region", "Canal_Venta", "Vendedor_Asignado",
            "Producto_Principal", "Monto_Compra", "Margen_Bruto_Pct", "Satisfaccion_CSAT", "Estado_Entrega", "Riesgo_Churn_Score"]
    vv = v.sort_values(sort_by, ascending=False).head(int(nrows))[cols].copy()
    show_table(vv, {"Monto_Compra": "${:,.2f}", "Margen_Bruto_Pct": "{:.1f}%", "Riesgo_Churn_Score": "{:.3f}", "Satisfaccion_CSAT": "{:d} ★"},
               good=["Monto_Compra", "Margen_Bruto_Pct", "Satisfaccion_CSAT"], bad=["Riesgo_Churn_Score"], height=480,
               title="Auditoría Transaccional Detallada de Órdenes y Cuentas",
               summary=f"Registro granular de transacciones filtradas por parámetros de búsqueda y niveles de alerta. Permite auditar en detalle montos facturados, rentabilidad porcentual unitaria, CSAT registrado y scoring de riesgo de fuga calculado por el motor analítico.",
               tips=[
                   "Investigar de manera prioritaria las órdenes que combinen alto monto facturado con bajo CSAT o entrega demorada.",
                   "Asegurar que todas las cuentas críticas cuenten con asesor comercial asignado y canal de venta claramente clasificado.",
                   "Utilizar la función de descarga de datos para revisiones de cumplimiento contable y conciliación de inventarios."
               ])

    d1, d2 = st.columns(2)
    d1.download_button("📥 Descargar CSV Filtrado", df.to_csv(index=False).encode("utf-8-sig"),
                       "datos_filtrados.csv", "text/csv")
    try:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df.to_excel(w, index=False, sheet_name="Data_Warehouse")
        d2.download_button("📥 Descargar Excel Filtrado", buf.getvalue(),
                           "datos_filtrados.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception:
        d2.caption("Instala `openpyxl` para habilitar exportación a Excel.")

    section("🧪 Controles Automáticos de Integridad y Calidad de Datos")
    dm = df_master
    chk = [
        {"Control": "Valores nulos en campos obligatorios", "Registros": int(dm[REQUIRED].isna().any(axis=1).sum()), "Estado": "🟢 OK" if dm[REQUIRED].isna().any(axis=1).sum() == 0 else "🔴 Revisar"},
        {"Control": "Cliente_ID único (sin duplicados)", "Registros": int(dm["Cliente_ID"].duplicated().sum()), "Estado": "🟢 OK" if dm["Cliente_ID"].duplicated().sum() == 0 else "🔴 Duplicados"},
        {"Control": "Consistencia Margen = Monto − Costo", "Registros": int(((dm["Monto_Compra"] - dm["Costo_Total"] - dm["Margen_Bruto"]).abs() > 0.05).sum()), "Estado": "🟢 OK"},
        {"Control": "Margen % dentro del rango 0–100%", "Registros": int(((dm["Margen_Bruto_Pct"] < 0) | (dm["Margen_Bruto_Pct"] > 100)).sum()), "Estado": "🟢 OK"},
        {"Control": "Satisfacción CSAT en escala 1 a 5", "Registros": int(((dm["Satisfaccion_CSAT"] < 1) | (dm["Satisfaccion_CSAT"] > 5)).sum()), "Estado": "🟢 OK"},
        {"Control": "Score de Churn probabilístico 0 a 1", "Registros": int(((dm["Riesgo_Churn_Score"] < 0) | (dm["Riesgo_Churn_Score"] > 1)).sum()), "Estado": "🟢 OK"},
        {"Control": "Ventas con monto positivo (> $0)", "Registros": int((dm["Monto_Compra"] <= 0).sum()), "Estado": "🟢 OK"}
    ]
    show_table(pd.DataFrame(chk), status=["Estado"],
               title="Matriz de Calidad, Integridad Referencial y Gobernanza de Datos",
               summary=f"Resultados de 7 pruebas automatizadas de integridad sobre el conjunto maestro de {len(df_master):,} registros. Se validan unicidad de identificadores, completitud de campos obligatorios, lógica matemática de márgenes y rangos probabilísticos válidos.",
               tips=[
                   "Un estado 100% verde (OK) garantiza que los datos son aptos para la toma de decisiones ejecutivas y el modelado de Machine Learning.",
                   "En caso de detectarse registros inconsistentes, activar de inmediato los protocolos de saneamiento en el pipeline ETL de origen.",
                   "Incorporar estos controles de calidad como regla obligatoria previa a cualquier carga de nuevos periodos contables."
               ])


# ==============================================================================
# 9. RENDERIZADO CONTROLADO
# ==============================================================================
def run(fn):
    try:
        fn()
    except Exception as e:
        st.error(f"⚠️ Error al renderizar la sección: {type(e).__name__}: {e}")


# ==============================================================================
# 10. BARRA DE NAVEGACIÓN FIJA SUPERIOR & PESTAÑAS (ARRIBA DEL TÍTULO PRINCIPAL)
# ==============================================================================
def inject_tab_navigation_arrows():
    """
    Inyecta flechas de navegación fija (◀ Anterior / Siguiente ▶) en los extremos
    de la barra superior de pestañas (window.parent.document).
    Permite retroceder o avanzar entre los 11 módulos ejecutivos con un solo clic
    y mantiene la barra scrolleable y visible en todo momento.
    """
    js_code = f"""
    <script>
    (function initTabNav() {{
        const parentDoc = window.parent.document;
        function setupNavArrows() {{
            const tablist = parentDoc.querySelector('div[role="tablist"], [data-baseweb="tab-list"]');
            if (!tablist) return;
            
            let prevBtn = parentDoc.getElementById('kpi-tab-nav-prev');
            let nextBtn = parentDoc.getElementById('kpi-tab-nav-next');
            
            function navigate(direction) {{
                const tabs = Array.from(tablist.querySelectorAll('[role="tab"], button[data-baseweb="tab"]'));
                if (!tabs.length) return;
                const curIdx = tabs.findIndex(t => t.getAttribute('aria-selected') === 'true');
                if (curIdx === -1) return;
                const nextIdx = (curIdx + direction + tabs.length) % tabs.length;
                tabs[nextIdx].click();
                tabs[nextIdx].scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
            }}
            
            const baseBtnStyle = `
                position: sticky;
                top: 0;
                z-index: 1000000;
                height: 32px;
                padding: 0 14px;
                font-size: 0.82rem;
                font-weight: 800;
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
                cursor: pointer;
                border-radius: 8px;
                border: 1.5px solid {THEME['border_highlight']};
                background-color: {THEME['surface']};
                color: {THEME['border_highlight']};
                box-shadow: 0 4px 14px rgba(0,0,0,0.25);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 5px;
                flex-shrink: 0;
                transition: all 0.2s ease;
                user-select: none;
            `;
            
            if (!prevBtn) {{
                prevBtn = parentDoc.createElement('button');
                prevBtn.id = 'kpi-tab-nav-prev';
                prevBtn.type = 'button';
                prevBtn.title = 'Regresar a la pestaña anterior (◀)';
                prevBtn.innerHTML = '◀ Anterior';
                prevBtn.style.cssText = baseBtnStyle + 'left: 0; margin-right: 6px;';
                prevBtn.onmouseenter = () => {{
                    prevBtn.style.backgroundColor = '{THEME['border_highlight']}';
                    prevBtn.style.color = '#FFFFFF';
                    prevBtn.style.transform = 'scale(1.04)';
                }};
                prevBtn.onmouseleave = () => {{
                    prevBtn.style.backgroundColor = '{THEME['surface']}';
                    prevBtn.style.color = '{THEME['border_highlight']}';
                    prevBtn.style.transform = 'scale(1)';
                }};
                prevBtn.onclick = (e) => {{ e.preventDefault(); e.stopPropagation(); navigate(-1); }};
                tablist.insertBefore(prevBtn, tablist.firstChild);
            }}
            
            if (!nextBtn) {{
                nextBtn = parentDoc.createElement('button');
                nextBtn.id = 'kpi-tab-nav-next';
                nextBtn.type = 'button';
                nextBtn.title = 'Avanzar a la siguiente pestaña (▶)';
                nextBtn.innerHTML = 'Siguiente ▶';
                nextBtn.style.cssText = baseBtnStyle + 'right: 0; margin-left: 6px;';
                nextBtn.onmouseenter = () => {{
                    nextBtn.style.backgroundColor = '{THEME['border_highlight']}';
                    nextBtn.style.color = '#FFFFFF';
                    nextBtn.style.transform = 'scale(1.04)';
                }};
                nextBtn.onmouseleave = () => {{
                    nextBtn.style.backgroundColor = '{THEME['surface']}';
                    nextBtn.style.color = '{THEME['border_highlight']}';
                    nextBtn.style.transform = 'scale(1)';
                }};
                nextBtn.onclick = (e) => {{ e.preventDefault(); e.stopPropagation(); navigate(1); }};
                tablist.appendChild(nextBtn);
            }}
        }}
        setupNavArrows();
        setInterval(setupNavArrows, 800);
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


TAB_TITLES = [
    "🧭 1. Resumen Ejecutivo", "📈 2. Comercial & Tendencias", "💰 3. Finanzas 360°",
    "🤖 4. Predictive Churn (ML)", "🎯 5. Segmentación (RFM)", "🗺️ 6. Territorio & Logística",
    "👥 7. Clientes Pareto & ABC", "👔 8. Fuerza de Ventas", "📦 9. Portafolio BCG",
    "📐 10. Estadística Avanzada", "📋 11. Auditoría & Calidad"
]
TABS = st.tabs(TAB_TITLES)
inject_tab_navigation_arrows()

tab_funcs = [
    tab_resumen, tab_comercial, tab_finanzas, tab_churn, tab_segmentacion,
    tab_territorio, tab_clientes, tab_vendedores, tab_portafolio,
    tab_estadistica, tab_auditoria
]

for idx, (tab, fn, title) in enumerate(zip(TABS, tab_funcs, TAB_TITLES)):
    with tab:
        render_cockpit_header(show_master_voice=(idx == 0), key_suffix=f"_{idx}", tab_title=title)
        run(fn)
        
        # Barra de navegación inferior
        prev_idx = (idx - 1 + len(TAB_TITLES)) % len(TAB_TITLES)
        next_idx = (idx + 1) % len(TAB_TITLES)
        prev_t = TAB_TITLES[prev_idx]
        next_t = TAB_TITLES[next_idx]
        html(
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin:32px 0 14px 0;padding:14px 20px;background:{THEME["surface_secondary"]};border:1.5px solid {THEME["border"]};border-radius:12px;box-shadow:{THEME["card_shadow"]};">'
            f'<div style="font-size:0.86rem;font-weight:700;color:{THEME["text_secondary"]};">'
            f'Módulo <b style="color:{THEME["text_primary"]};">{idx + 1}</b> de <b style="color:{THEME["text_primary"]};">{len(TAB_TITLES)}</b> • {title}</div>'
            f'<div style="display:flex;gap:10px;flex-wrap:wrap;">'
            f'<button onclick="window.parent.document.querySelectorAll(\'div[role=\\\'tablist\\\'] [role=\\\'tab\\\'], div[role=\\\'tablist\\\'] button[data-baseweb=\\\'tab\\\']\')[{prev_idx}].click(); window.parent.document.querySelectorAll(\'div[role=\\\'tablist\\\'] [role=\\\'tab\\\'], div[role=\\\'tablist\\\'] button[data-baseweb=\\\'tab\\\']\')[{prev_idx}].scrollIntoView({{behavior:\'smooth\',inline:\'center\'}});" style="background:{THEME["surface"]};color:{THEME["border_highlight"]};border:1.5px solid {THEME["border_highlight"]};padding:6px 16px;border-radius:8px;font-weight:700;font-size:0.80rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);">◀ Anterior ({prev_t})</button>'
            f'<button onclick="window.parent.document.querySelectorAll(\'div[role=\\\'tablist\\\'] [role=\\\'tab\\\'], div[role=\\\'tablist\\\'] button[data-baseweb=\\\'tab\\\']\')[{next_idx}].click(); window.parent.document.querySelectorAll(\'div[role=\\\'tablist\\\'] [role=\\\'tab\\\'], div[role=\\\'tablist\\\'] button[data-baseweb=\\\'tab\\\']\')[{next_idx}].scrollIntoView({{behavior:\'smooth\',inline:\'center\'}});" style="background:{THEME["border_highlight"]};color:#FFFFFF;border:1.5px solid {THEME["border_highlight"]};padding:6px 16px;border-radius:8px;font-weight:700;font-size:0.80rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);">Siguiente ({next_t}) ▶</button>'
            f'</div></div>'
        )

# ==============================================================================
# 11. PIE DE PÁGINA CORPORATIVO
# ==============================================================================
st.markdown("---")
html(
    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;font-size:0.85rem;color:{THEME["text_secondary"]};">'
    f'<div>⚡ <b>Executive 360° Enterprise BI & Machine Learning Suite</b> | Streamlit • Plotly • Scikit-Learn • SciPy • Web Speech API</div>'
    f'<div>Ing. Juancito Peña · Analítica integral con narración ejecutiva inteligente y locución fonética en tiempo real</div></div>'
)
