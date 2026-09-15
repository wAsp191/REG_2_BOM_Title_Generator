# --- SEZIONE IMPORT ---
import streamlit as st
import pandas as pd
import datetime
import time
from difflib import get_close_matches
from deep_translator import MyMemoryTranslator
from streamlit_gsheets import GSheetsConnection

# =========================================================
# 0. CONFIGURAZIONE PAGINA E LOGICA RESET
# =========================================================

# Spostiamo set_page_config come primissima istruzione per evitare errori
st.set_page_config(page_title="Technical Generator v8.7", layout="wide")

# CSS per compattare l'interfaccia
st.markdown("""
    <style>
        /* 1. Riduciamo il padding superiore della pagina */
        .block-container {
            padding-top: 3.0rem !important;
            padding-bottom: 0rem !important;
        }

        /* 2. Compattiamo lo spazio tra ogni elemento (widget) */
        [data-testid="stVerticalBlock"] > div {
            flex-direction: column;
            gap: 0.12rem !important; /* Riduce il buco tra un widget e l'altro */
        }

        /* 3. Riduciamo l'altezza dei titoli */
        h1 { margin-bottom: -1rem !important; font-size: 1.6rem !important; }
        h2 { margin-bottom: -0.8rem !important; font-size: 1.2rem !important; }
        h3 { margin-bottom: -0.5rem !important; font-size: 1.0rem !important; }

        /* 4. Compattiamo i divisori (st.divider / st.markdown("---")) */
        hr {
            margin-top: 0.35rem !important;
            margin-bottom: 0.35rem !important;
        }

        /* 5. Trick per ridurre lo spazio sotto le label dei widget */
        .st-emotion-cache-1p3m0jg {
            margin-bottom: -0.8rem !important;
        }

        /* 6. Riduciamo lo spazio interno ai widget (Selectbox, Text Input) */
        div[data-baseweb="select"] > div, 
        div[data-testid="stTextInput"] > div > div > input {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            min-height: 1.6rem !important;
        }
        
        /* 7. Nascondiamo lo spazio extra dei Pills */
        [data-testid="stPills"] {
            margin-top: -0.5rem !important;
        }
        /* 8. Ingrandimento scritte Categorie (st.radio) */
        [data-testid="stWidgetLabel"] p {
            font-size: 1.6rem !important; /* Ingrandisce la label del widget */
            font-weight: 700 !important;
        }

        [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem !important; /* Ingrandisce le opzioni del radio (Metal Comp, etc) */
        }
        
        /* Ottimizzazione spazio tra le opzioni del radio per non farle accavallare */
        [data-testid="stAudioRadio"] div {
            gap: 0.5rem !important;
        }

        /* 9. Distanziamento verticale tra le opzioni del Radio (Categorie) */
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            margin-bottom: 12px !important; /* Aggiunge spazio sotto ogni categoria */
            padding: 5px 0px !important;    /* Dà un po' di respiro interno */
            transition: all 0.2s ease;      /* Effetto fluido al passaggio del mouse */
        }

        /* Opzionale: un leggero effetto hover per capire cosa stiamo selezionando */
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# CONTROLLO TOAST: Eseguito ad ogni ricaricamento
if st.session_state.get('reset_eseguito'):
    st.toast("Interfaccia pulita!", icon="✨")
    st.session_state['reset_eseguito'] = False

# --- LOGICA DI RESET OTTIMIZZATA ---
def activate_reset():
    """
    Reset centralizzato dello stato. 
    Nota: Non chiamiamo st.rerun() qui perché usata come callback 'on_click',
    evitando l'avviso 'no-op'.
    """
    
    # 1. Valori di default
    defaults = {
        'comp_tags': None,
        'selectbox_part': None,
        'extra_tags': [],
        'check_1090': False,
        'check_assembled': False,
        'stringa_stabile': "",
        'tags_stabili': []
    }

    text_keys = [
        'dim_l', 'dim_l_gen', 'dim_p', 'dim_h', 
        'dim_dia', 'dim_dia_gen', 'dim_s', 'extra_text', 
        'stringa_editabile', 'input_manuale'
    ]

    # 2. Esecuzione Reset Session State
    for key, val in defaults.items():
        st.session_state[key] = val
        
    for key in text_keys:
        if key in st.session_state:
            st.session_state[key] = ""

    # 3. Pulizia chiavi dinamiche
    for key in list(st.session_state.keys()):
        if key.startswith(("manual_", "sub_")):
            del st.session_state[key]

    # 4. Flag per attivare il toast al termine del refresh automatico
    st.session_state['reset_eseguito'] = True
