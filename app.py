# =========================================================
# SEZIONE IMPORT
# =========================================================
import streamlit as st
import pandas as pd
import datetime
import time
from deep_translator import MyMemoryTranslator
from streamlit_gsheets import GSheetsConnection
from zoneinfo import ZoneInfo
# =========================================================
# NAVIGAZIONE E ROUTER PRINCIPALE (App / Admin)
# =========================================================
st.sidebar.title("🧭 Navigazione")
scelta_pagina = st.sidebar.radio("Accedi a:", ["⚙️ Generatore", "🔒 Admin"])

if scelta_pagina == "🔒 Admin":
    # Se non siamo ancora autenticati come admin, mostriamo il box centrato
    if "admin_autenticato" not in st.session_state:
        st.session_state.admin_autenticato = False

    if not st.session_state.admin_autenticato:
        # Colonne spaziatrici per centrare il login admin perfettamente nello schermo
        col_spaz_sx, col_admin_centro, col_spaz_dx = st.columns([1, 1.5, 1])
        
        with col_admin_centro:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center;'>🔐 Area Riservata</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: gray; font-size: 0.9rem;'>Inserisci la password di amministrazione</p>", unsafe_allow_html=True)
                
                with st.form("form_login_admin"):
                    password_inserita = st.text_input("Password Admin:", type="password")
                    btn_login_admin = st.form_submit_button("Accedi al Pannello", use_container_width=True)
                    
                    password_corretta = st.secrets.get("admin_password", "reg2026")
                    
                    if btn_login_admin:
                        if password_inserita == password_corretta:
                            st.session_state.admin_autenticato = True
                            st.rerun()
                        else:
                            st.error("❌ Password errata. Accesso negato.")
        st.stop()

    # --- PANNELLO ADMIN (AUTENTICATO) ---
    st.title("🛠️ Pannello Amministrazione - Gestione Segnalazioni")
    st.markdown("---")
    
    # Pulsante per uscire dall'area admin
    if st.sidebar.button("🔒 Logout Admin", use_container_width=True):
        st.session_state.admin_autenticato = False
        st.rerun()

    try:
        conn_admin = st.connection("gsheets_segnalazioni", type=GSheetsConnection)
        df_segnalazioni = conn_admin.read(ttl=0)
        
        if df_segnalazioni is None or df_segnalazioni.empty:
            st.info("📭 Nessuna segnalazione presente nel Google Sheet al momento.")
        else:
            st.subheader("📋 Gestione ed Eliminazione Rapida Richieste")
            st.markdown("Spunta le caselle a sinistra delle richieste che desideri rimuovere definitivamente:")
            
            # Intestazione tabella interattiva
            col_i0, col_i1, col_i2, col_i3, col_i4, col_i5 = st.columns([0.6, 1.5, 1.2, 1.5, 2.5, 1.2])
            with col_i0: st.markdown("**Az.**")
            with col_i1: st.markdown("**Timestamp**")
            with col_i2: st.markdown("**Utente**")
            with col_i3: st.markdown("**Tipo**")
            with col_i4: st.markdown("**Descrizione**")
            with col_i5: st.markdown("**Stato**")
            st.markdown("---")
            
            indici_da_eliminare = []

            for idx, row in df_segnalazioni.iterrows():
                c_chk, c_ts, c_ut, c_tipo, c_desc, c_stato = st.columns([0.6, 1.5, 1.2, 1.5, 2.5, 1.2])
                
                with c_chk:
                    if st.checkbox("Seleziona", key=f"chk_del_{idx}", label_visibility="collapsed"):
                        indici_da_eliminare.append(idx)
                with c_ts:
                    st.text(str(row.get("Timestamp", "")))
                with c_ut:
                    st.text(str(row.get("Utente", "")))
                with c_tipo:
                    st.text(str(row.get("Tipo", "")))
                with c_desc:
                    st.text(str(row.get("Descrizione", "")))
                with c_stato:
                    st.text(str(row.get("Stato", "")))
                
                st.divider()

            if indici_da_eliminare:
                if st.button("🗑️ Elimina Definitivamente Selezionati", type="primary"):
                    try:
                        df_aggiornato = df_segnalazioni.drop(indici_da_eliminare).reset_index(drop=True)
                        conn_admin.update(data=df_aggiornato)
                        st.success("🎉 Segnalazioni selezionate eliminate con successo!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Errore durante l'aggiornamento del foglio: {e}")
            else:
                st.info("💡 Spunta almeno una casella nella lista per abilitare l'eliminazione.")
            
    except Exception as e:
        st.error(f"⚠️ Errore di comunicazione con Google Sheets: {e}")
        
    st.stop()
# =========================================================
# 0. CONFIGURAZIONE PAGINA E CREDENZIALI DI ACCREDITAMENTO
# =========================================================
st.set_page_config(page_title="Technical Generator v2.0", layout="wide")

# Database utenti autorizzati (Puoi mappare i tuoi colleghi qui o spostarlo su GSheets)
UTENTI_AUTORIZZATI = {
    "admin": {"password": "reg2026", "nome": "Amministratore di Sistema"},
    "pierluigi.giorgi": {"password": "pierluigigiorgi", "nome": "Pierluigi Giorgi (Ufficio Tecnico)"},
    "gaia.gualtieri": {"password": "gaiagualtieri", "nome": "Gaia Gualtieri (Ufficio Tecnico)"},
    "emanuela.bois": {"password": "emanuelabois", "nome": "Emanuela Bois (Ufficio Tecnico)"},
    "andrea.parrini": {"password": "andreaparrini", "nome": "Andrea Parrini (Ufficio Tecnico)"},
    "gianfranco.palmisano": {"password": "gianfrancopalmisano", "nome": "Gianfranco Palmisano (Ufficio Tecnico)"},
    "giuseppe.pieri": {"password": "giuseppepieri", "nome": "Giuseppe Pieri (Ufficio Tecnico)"},
    "carlo.castellani": {"password": "carlocastellani", "nome": "Carlo Castellani (Ufficio Tecnico)"},
    "enrico.sarti": {"password": "enricosarti", "nome": "Enrico Sarti (Ufficio Tecnico)"}
}

# CSS personalizzato per la compattezza
st.markdown("""
    <style>
        .block-container {
            padding-top: 2.5rem !important;
            padding-bottom: 0rem !important;
        }
        [data-testid="stVerticalBlock"] > div {
            flex-direction: column;
            gap: 0.12rem !important;
        }
        h1 { margin-bottom: -1rem !important; font-size: 1.6rem !important; }
        h2 { margin-bottom: -0.8rem !important; font-size: 1.2rem !important; }
        h3 { margin-bottom: -0.5rem !important; font-size: 1.0rem !important; }
        hr {
            margin-top: 0.35rem !important;
            margin-bottom: 0.35rem !important;
        }
        div[data-baseweb="select"] > div, 
        div[data-testid="stTextInput"] > div > div > input {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            min-height: 1.6rem !important;
        }
        [data-testid="stWidgetLabel"] p {
            font-size: 1.4rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMarkdownContainer"] p {
            font-size: 1.1rem !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            margin-bottom: 8px !important;
            padding: 4px 0px !important;
            transition: all 0.2s ease;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Gestione dello stato di autenticazione
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False
if "utente_corrente" not in st.session_state:
    st.session_state.utente_corrente = ""

# --- SCHERMATA DI LOGIN INIZIALE (CENTRATA) ---
if not st.session_state.autenticato:
    # Colonne spaziatrici per centrare il form orizzontalmente nello schermo
    col_spazio_sx, col_login_centro, col_spazio_dx = st.columns([1, 1.5, 1])
    
    with col_login_centro:
        # Contenitore con bordo per dare un effetto "card" pulito e professionale
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🔐 Accesso - REG 2.0</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray; font-size: 0.9rem;'>Inserisci le tue credenziali</p>", unsafe_allow_html=True)
            
            with st.form("form_login"):
                username_input = st.text_input("Username").strip().lower()
                password_input = st.text_input("Password", type="password")
                btn_login = st.form_submit_button("🔑 Accedi", use_container_width=True)
                
                if btn_login:
                    if username_input in UTENTI_AUTORIZZATI and UTENTI_AUTORIZZATI[username_input]["password"] == password_input:
                        st.session_state.autenticato = True
                        st.session_state.utente_corrente = UTENTI_AUTORIZZATI[username_input]["nome"]
                        st.rerun()
                    else:
                        st.error("❌ Credenziali non valide. Riprova.")
                        
    st.stop()  # Blocca l'esecuzione dell'app se non si è loggati

# Notifica toast post-reset
if st.session_state.get('reset_eseguito'):
    st.toast("Interfaccia pulita!", icon="✨")
    st.session_state['reset_eseguito'] = False

def activate_reset():
    defaults = {
        'comp_tags': None,
        'selectbox_part': None,
        'extra_tags': [],
        'check_1090': False,
        'check_assembled': False,
        'stringa_stabile': "",
        'tags_stabili': []
    }
    text_keys = ['dim_l', 'dim_l_gen', 'dim_p', 'dim_h', 'dim_dia', 'dim_dia_gen', 'dim_s', 'extra_text', 'stringa_editabile', 'input_manuale']
    for key, val in defaults.items():
        st.session_state[key] = val
    for key in text_keys:
        if key in st.session_state:
            st.session_state[key] = ""
    for key in list(st.session_state.keys()):
        if key.startswith(("manual_", "sub_")):
            del st.session_state[key]
    st.session_state['reset_eseguito'] = True

# =========================================================
# 1. DIZIONARI, PILLS E DATABASE CENTRALIZZATO
# =========================================================
COPPIE_INCOMPATIBILI = [
    {"Statico", "Antisismico"}, {"Angolo aperto", "Angolo chiuso"},
    {"Portante", "Non portante"}, {"Singolo", "Doppio"},
    {"Per ripiano in vetro", "Per ripiano in legno"}, {"Con serratura", "Senza serratura"},
    {"Passo 25", "Passo 50"}, {"L50", "L55"}, {"Scorrevoli", "A saracinesca"},
    {"Per attacco montante", "Per attacco fiancata"}, {"Superiore", "Tra ripiani di base"},
    {"Dritto", "Inclinato"}, {"Cromato", "Verniciato"},
    {"Multibarra", "Multilame", "In rete"}, {"Profilo a L", "Profilo a U"},
    {"Per ripiano di base", "Per fiancata"}, {"Terminale", "Centrale"},
    {"Liscio", "Liscia", "Forato", "Forata", "In filo"}, {"Zincato", "Verniciata"}
]

GLOSSARIO_TECNICO = {
    "mensola": "BRACKET", "mensole": "BRACKETS", "gondola": "GONDOLA",
    "spalla": "FRAME", "innesto": "COUPLING", "montante": "UPRIGHT",
    "per": "FOR", "losanga": "LOSANGA", "cancelletto": "GATE", "vasca": "TANK"
}

SUB_OPTIONS_CONFIG = {
    "VPA (+)": {"Serie S": "S SERIES", "Serie SS": "SS SERIES", "Serie M": "M SERIES", "Serie L": "L SERIES"},
    "Con distanziale (+)": {"L100": "S100", "L150": "S150", "L200": "S200", "L250": "S250"},
    "Numero diagonali (+)": {"Doppie": "DD", "Triple": "TD", "Quadruple": "QD"},
    "Sezione (+)": {"L55": "L55", "L80 Z/S": "L80 Z/S", "L80 Z/M": "L80 Z/M", "L100 Z/S": "L100 Z/S", "L100 Z/M": "L100 Z/M", "L120 Z/S": "L120 Z/S", "70X30": "70X30", "90X30": "90X30", "30X30": "30X30"},
    "Tipologia di mensola (+)": {"Mensola saldata a filo superiore": "UPPER BRACKET", "Mensola saldata a filo inferiore": "LOWER BRACKET"},
    "Compatibilità piede di base (+)": {"Per piede H90": "FOR H90 BASE FOOT", "Per piede H100": "FOR H100 BASE FOOT", "Per piede H150": "FOR H150 BASE FOOT"},
    "Attacco gancio (+)": {"Attacco barra": "HOOK FOR BAR", "Attacco multilame": "HOOK FOR MULTISTRIP", "Attacco pannello forato": "HOOK FOR SLOTTED PANEL"},
    "Orientamento (+)": {"Destra": "RIGHT", "Sinistra": "LEFT"},
    "Posizioni multiple (+)": {"1 posizione": "1 POSITION", "2 posizioni": "2 POSITIONS", "3 posizioni": "3 POSITIONS"},
    "Altezza piede (+)": {"H90": "H90", "H100": "H100", "H150": "H150"},
    "Predisposto per montante (+)": {"L80": "FOR L80 UPRIGHT", "L100/L120": "FOR L100/L120 UPRIGHT"},
    "Numero tasche (+)": {"1 Tasca": "1 POCKET", "2 Tasche": "2 POCKETS"},
    "Numero gradoni (+)": {"1 gradone": "1 STEP", "2 gradoni": "2 STEPS", "3 gradoni": "3 STEPS"},
    "Asimmetrica (+)": {"AS240": "AS240", "AS340": "AS340", "AS440": "AS440"}
}

EXTRA_CON_INPUT_MANUALE = ["Sezione circolare", "Sezione quadrata"]

MATERIALI_CONFIG = {
    "METAL COMP": {"METAL": "METAL", "ZINCATO": "GALVANIZED", "INOX": "STAINLESS STEEL", "ALLUMINIO": "ALUMINIUM"},
    "WOOD COMP": {"LAMINATO": "LAMINATED", "NOBILITATO": "MELAMINE", "TRUCIOLARE": "OSB", "HPL": "HPL"},
    "PLASTIC COMP": {"PLX": "PLX", "POLICARBONATO": "POLYCARBONATE", "PVC": "PVC", "GOMMA": "RUBBER"},
    "GLASS COMP": {"VETRO TEMPRATO": "TEMPERED", "VETRO SATINATO": "SATIN"},
    "FASTENER": {"NERO": "", "ZINCATO": "GALVANIZED", "BRUNITO": "BURNISHED"},
    "ASSEMBLY": {}
}

# --- GRUPPI DI PILLS ISOLATI ---
PILLS_COMP = {
    "A pinza": "GRIPPED", 
    "A saracinesca": "SHUTTER", 
    "A seggiola": "L-SHAPED PROFILE",
    "Adesivo": "ADHESIVE",
    "Altezza piede (+)": "",
    "Angolo aperto": "EXTERNAL CORNER",
    "Angolo chiuso": "INNER CORNER",
    "Antisgancio": "ANTI-RELEASE",
    "Antisismico": "ANTI-SEISMIC",
    "Antiurto": "SHOCKPROOF",
    "Asolato": "SLOTTED",
    "Attacco gancio (+)": "",
    "Attacco montante": "HOOK ONTO UPRIGHT",
    "Bordi smussati": "CHAMFERED EDGES",
    "Centrale": "CENTRAL",
    "Colorato": "COLORED",
    "Compatibilità piede di base (+)": "",
    "Completa di paracolpo ABS": "WITH ABS BUFFER",
    "Con asola centrale": "WITH CENTRAL SLOT",
    "Con collegamento superiore": "WITH UPPER CONNECTION",
    "Con componente saldato": "WITH WELDED ELEMENT",
    "Con distanziale (+)": "WITH SPACER",
    "Con finestra": "WITH WINDOW",
    "Con foro serratura": "WITH LOCK HOLE",
    "Con guide RAM": "WITH RAM GUIDE",
    "Con illuminazione": "WITH LIGHTING",
    "Con inserti filettati": "WITH RIVET",
    "Con lati bordati": "WITH EDGED SIDES",
    "Con mensole": "WITH BRACKET",
    "Con mensole saldate": "WITH WELDING BRACKET",
    "Con piega frontale": "WITH DOWNWARD",
    "Con portaprezzo": "WITH TICKET-HOLDER",
    "Con rinforzo": "REINFORCED",
    "Con ruote": "WITH WHEELS",
    "Con scasso": "WITH RECESS",
    "Con serratura": "WITH LOCK",
    "Con tasca oscillante": "WITH LIFT-UP POCKET",
    "Con viteria": "WITH SCREWS",
    "Con viteria saldata": "WITH WELDING SCREWS",
    "Cromato": "CHROMED",
    "Di collegamento": "CONNECTING",
    "Doppio": "DOUBLE",
    "Dritto": "STRAIGHT",
    "Forato": "PERFORATED",
    "Fresata": "MILLING",
    "Gondola": "GONDOLA",
    "Illuminato": "ILLUMINATED",
    "Impilabile": "STACKABLE",
    "In filo": "WIRE",
    "In rete": "MESH",
    "Inclinata": "INCLINED",
    "Inclinato": "SLOPING",
    "Liscio": "PLAIN",
    "Minirack": "MINIRACK", "Multibarra": "MULTIBAR", "Multilame": "MULTISTRIP", "Nervata": "RIBBED",
    "Nervato": "RIBBED",
    "Non portante": "NON LOAD-BEARING",
    "Numero diagonali (+)": "",
    "Orientamento (+)": "",
    "Passo 25": "PITCH 25", "Passo 50": "PITCH 50",
    "Per Top legno": "FOR TOP SHELF",
    "Per attacco fiancata": "HOOK ONTO SIDE-PANEL",
    "Per controventatura": "FOR CROSS-WALL",
    "Per crociera verticale": "FOR VERTICAL CROSS-WALL",
    "Per fiancata": "FOR SIDE PANEL",
    "Per montante M70": "FOR M70 UPRIGHT", "Per montante M90": "FOR M90 UPRIGHT",
    "Per ripiano": "FOR SHELF", "Per ripiano di base": "FOR BASE SHELF", "Per ripiano in legno": "FOR WOODEN SHELF", "Per ripiano in vetro": "FOR GLASS SHELF",
    "Piegato": "BENT", "Piegato-saldato": "BENT AND WELDED",
    "Portante": "LOAD-BEARING",
    "Posizioni multiple (+)": "",
    "Predisposto per montante (+)": "", "Predisposto per portaprezzo": "ACCEPTS TICKET-HOLDER",
    "Profilo a L": "L-SHAPED", "Profilo a U": "U-SHAPED",
    "Regolabile": "ADJUSTABLE",
    "Rinforzata": "REINFORCED",
    "Rovescio": "REVERSE",
    "Sagomata": "SHAPED",
    "Saldata": "WELDED",
    "Scantonato": "NOTCHED",
    "Scorrevoli": "SLIDING",
    "Semicircolare": "SEMICIRCULAR",
    "Senza serratura": "WITHOUT LOCK",
    "Serigrafata": "SILKSCREENED",
    "Sezione (+)": "",
    "Sezione a C": "C-PROFILE",
    "Sezione circolare": "CIRCULAR SECTION", "Sezione quadrata": "SQUARE SECTION",
    "Singolo": "SINGLE",
    "Statico": "STATIC",
    "Stondata": "ROUNDED",
    "Su due livelli": "TWO LEVELS",
    "Su ruote": "ON WHEELS",
    "Superiore": "TOP",
    "Terminale": "END",
    "Tipologia di mensola (+)": "",
    "Tra ripiani di base": "INTER-BASE SHELF",
    "Trapezoidale": "SLOPING",
    "Trasparente": "TRANSPARENT",
    "VPA (+)": "VPA",
    "Verniciato": "PAINTED"
}

PILLS_FASTNER = {
    "Autobloccante": "SELF-LOCKING",
    "Autoperforanti": "SELF-DRILLING",
    "Con testa": "WITH HEAD",
    "Dentellata": "SERRATED LOCK",
    "Elastica": "GROWER",
    "Fascia Larga": "WIDE BAND",
    "Flangiato": "FLANGED",
    "Senza testa": "WITHOUT HEAD",
    "Testa Bombata": "ROUND HEAD",
    "Testa a croce": "CROSS HEAD",
    "Testa esagonale": "HEX HEAD",
    "Testa esagono incassato": "HEXAGON SOCKET HEAD",
    "Testa svasata": "COUNTERSUNK HEAD"
}

PILLS_ASSEMBLY = {
    "Antisismico": "SEISMIC-RESISTANT",
    "Asimmetrica (+)": "",
    "Attacco montante": "ONTO THE UPRIGHT",
    "Centrale": "CENTRAL",
    "Con ante scorrevoli": "WITH SLIDING DOOR",
    "Con batticarrello": "WITH TROLLEY BEATER",
    "Con ganci": "WITH HOOKS",
    "Con illuminazione": "WITH LIGHTING",
    "Con macchine di pagamento": "WITH GLORY MACHINES PAYMENT",
    "Con mensole saldate": "WITH WELDED BRACKETS",
    "Con portaprezzo in filo": "WITH PRICE-HOLDER WIRE",
    "Con rete divisoria": "WITH DIVIDING NET",
    "Con ripiani": "WITH SHELF",
    "Con ripiani inclinati": "WITH INCLINED SHELF",
    "Con ruote": "WITH WHEELS",
    "Forato": "PERFORATED",
    "Mobile": "MOBILE",
    "Numero diagonali (+)": "",
    "Numero gradoni (+)": "",
    "Numero tasche (+)": "",
    "Per alimenti": "FOR FOOD",
    "Per casse automatiche": "FOR SELF PAY",
    "Rotante": "ROTATING",
    "Sezione (+)": "",
    "Terminale": "END",
    "Verniciata": "POWDER COATED",
    "Zincato": "GALVANIZED"
}

# Mappa di associazione tra la macro-categoria e il suo dizionario di pills specifico
MAPPA_PILLS_CATEGORIA = {
    "METAL COMP": PILLS_COMP,
    "WOOD COMP": PILLS_COMP,
    "PLASTIC COMP": PILLS_COMP,
    "GLASS COMP": PILLS_COMP,
    "FASTENER": PILLS_FASTNER,
    "ASSEMBLY": PILLS_ASSEMBLY
}
DATABASE = {
    "METAL COMP": {
        "macro_en": "METAL COMPONENT",
        "Particolari": {
            "Piede di base": ["BASE FOOT", "PILLS_COMP", "FOOT"],
            "Porta cartello": ["SIGN HOLDER", "PILLS_COMP", "SIGN HOLDER"],
            "Zoccolatura": ["PLINTH", "PILLS_COMP", "PLINTH"],
            "Pannello rivestimento": ["BACK PANEL", "PILLS_COMP", "PANEL"],
            "Copripiede": ["FOOT COVER", "PILLS_COMP", "COVER"],
            "Chiusura": ["COVER", "PILLS_COMP", "COVER"],
            "Fiancata laterale": ["SIDE PANEL", "PILLS_COMP", "SIDE-PANEL"],
            "Mensola": ["BRACKET", "PILLS_COMP", "BRACKET"],
            "Ripiano": ["SHELF", "PILLS_COMP", "SHELF"],
            "Cesto in filo": ["WIRE-BASKET", "PILLS_COMP", "BASKET"],
            "Cielino": ["CANOPY", "PILLS_COMP", "CANOPY"],
            "Corrente": ["BEAM", "PILLS_COMP", "BEAM"],
            "Diagonale": ["DIAGONAL", "PILLS_COMP", "DIAGONAL"],
            "Distanziale": ["SPACER", "PILLS_COMP", "SPACER"],
            "Gancio": ["HOOK", "PILLS_COMP", "HOOK"],
            "Profilo": ["PROFILE", "PILLS_COMP", "PROFILE"],
            "Rinforzo": ["STIFFENER", "PILLS_COMP", "STIFFENER"],
            "Staffa": ["PLATE", "PILLS_COMP", "PLATE"],
            "Anta/sportello": ["DOOR", "PILLS_COMP", "DOOR"],
            "Piastra di fissaggio": ["FIXING PLATE", "PILLS_COMP", "PLATE"],
            "Cassetto estraibile": ["PULL-OUT DRAWER", "PILLS_COMP", "DRAWER"],
            "Coprimontante": ["UPRIGHT-COVER", "PILLS_COMP", "COVER"],
            "Pedana di base": ["BASE PLATFORM", "PILLS_COMP", "BASE"],
            "Divisorio": ["DIVIDER", "PILLS_COMP", "DIVIDER"],
            "Frontalino": ["RISER", "PILLS_COMP", "RISER"],
            "Compensazione": ["FILLER PIECE", "PILLS_COMP", "SPACER"],
            "Controventatura": ["BRACING", "PILLS_COMP", "BRACING"],
            "Traversino": ["CROSS BAR", "PILLS_COMP", "CROSS BAR"],
            "Tubolare": ["TUBULAR", "PILLS_COMP", "BAR"],
            "Filo": ["WIRE", "PILLS_COMP", "WIRE"],
            "Montante": ["UPRIGHT", "PILLS_COMP", "UPRIGHT"],
            "Lamiera generica": ["SHEET METAL", "PILLS_COMP", "GENERIC SHEET METAL"],
            "Pannello frontale": ["FRONT PANEL", "PILLS_COMP", "PANEL"],
            "Adattatore": ["ADAPTER", "PILLS_COMP", "ADAPTER"],
            "Canalina passa cavi": ["CABLE TRAY", "PILLS_COMP", "ESA"],
            "Vasca": ["TANK", "PILLS_COMP", "TANK"],
            "Tamponamento": ["BUFFER PANEL", "PILLS_COMP", "BUFFER"],
            "Protezione": ["PROTECTION FOR PERFORATED SHELF", "PILLS_COMP", "PROTECTION"],
            "Portaprezzo": ["TICKET-HOLDER", "PILLS_COMP", "TICKET-HOLDER"]
        }
    },
    "WOOD COMP": {
        "macro_en": "WOOD COMPONENT",
        "Particolari": {
            "Ripiano Legno": ["WOODEN SHELF", "PILLS_COMP", "SHELF"],
            "Anta/sportello": ["DOOR", "PILLS_COMP", "DOOR"],
            "Schienale Legno": ["WOODEN BACK", "PILLS_COMP", "PANEL"],
            "Cielino": ["WOODEN CANOPY", "PILLS_COMP", "CANOPY"],
            "Zoccolatura": ["WOODEN PLINTH", "PILLS_COMP", "PLINTH"],
            "Fiancata": ["WOODEN SIDE PANEL", "PILLS_COMP", "SIDE PANEL"],
            "Copripiede": ["WOODEN FOOT-COVER", "PILLS_COMP", "COVER"],
            "Coprimontante": ["WOODEN UPRIGHT-COVER", "PILLS_COMP", "COVER"],
            "Compensazione": ["WOODEN FILLER PIECE", "PILLS_COMP", "SPACER"],
            "Tamponamento": ["BUFFER PANEL", "PILLS_COMP", "BUFFER"],
            "Mobiletto in legno": ["WOODEN CABINET", "PILLS_COMP", "CABINET"],
            "Asta in legno": ["WOODEN ROD", "PILLS_COMP", "ROD"]
        }
    },
    "PLASTIC COMP": {
        "macro_en": "PLASTIC COMPONENT",
        "Particolari": {
            "Tappo": ["PLASTIC CAP", "PILLS_COMP", "CAP"],
            "Guarnizione": ["GASKET", "PILLS_COMP", "ACCESSORY"],
            "Cerniera": ["HINGE", "PILLS_COMP", "ACCESSORY"],
            "Divisorio": ["DIVIDER", "PILLS_COMP", "DIVIDER"],
            "Frontalino": ["RISER", "PILLS_COMP", "RISER"],
            "Pannello": ["PANEL", "PILLS_COMP", "PANEL"],
            "Anta": ["DOOR", "PILLS_COMP", "DOOR"],
            "Portaprezzo": ["TICKET-HOLDER", "PILLS_COMP", "TICKET-HOLDER"]
        }
    },
    "GLASS COMP": {
        "macro_en": "GLASS COMPONENT",
        "Particolari": {
            "Ripiano": ["GLASS SHELF", "PILLS_COMP", "SHELF"],
            "Anta": ["GLASS DOOR", "PILLS_COMP", "DOOR"],
            "Cancelletto": ["GLASS ARM", "PILLS_COMP", "ARM"],
            "Chiusura": ["COVER", "PILLS_COMP", "COVER"]
        }
    },
    "FASTENER": {
        "macro_en": "FASTENER",
        "Particolari": {
            "Vite": ["SCREW", "PILLS_FASTNER", "SCREW"],
            "Bullone": ["BOLT", "PILLS_FASTNER", "FASTENER"],
            "Rondella": ["WASHER", "PILLS_FASTNER", "WASHER"],
            "Dado": ["NUT", "PILLS_FASTNER", "NUT"],
            "Inserti filettati": ["RIVET", "PILLS_FASTNER", "RIVET"]
        }
    },
    "ASSEMBLY": {
        "macro_en": "ASSEMBLY",
        "Particolari": {
            "Vetrina": ["SHOWCASE", "PILLS_ASSEMBLY", "SHOWCASE"],
            "Espositore": ["DISPLAY", "PILLS_ASSEMBLY", "DISPLAY"],
            "Totem": ["TOTEM", "PILLS_ASSEMBLY", "DISPLAY"],
            "Spalla": ["FRAME", "PILLS_ASSEMBLY", "FRAME"],
            "Controventatura": ["CROSS-BRACING", "PILLS_ASSEMBLY", "CROSS-BRACING"],
            "Banco espositore di legno": ["WOODEN DESK", "PILLS_ASSEMBLY", "DESK"],
            "Avancassa": ["IMPULSE UNIT", "PILLS_ASSEMBLY", "DISPLAY"],
            "Cassettiera": ["CHEST OF DRAWERS", "PILLS_ASSEMBLY", "DRAWER"],
            "Espositore riviste": ["DISPLAY FOR MAGAZINE", "PILLS_ASSEMBLY", "DISPLAY"],
            "Cassa pagamento automatico": ["SELF CHECKOUT", "PILLS_ASSEMBLY", "SELF CHECKOUT (SCO)"],
            "Espositore a gradoni": ["STEPLADDER DISPLAY", "PILLS_ASSEMBLY", "DISPLAY"],
            "Telaio saldato": ["METAL WELDMENT", "PILLS_ASSEMBLY", "FRAME"]
        }
    }
}

OPZIONI_COMPATIBILITA = ["", "F25", "F25 BESPOKE", "F25 READY", "F50", "F50 BESPOKE", "F50 READY", "UNIVERSAL", "BC", "FORTISSIMO", "MINIRACK", "UNIMOB"]

MAPPA_NORMATIVE_FASTENER = {
    "Vite": {
        "": "", "DIN 912 - Testa cilindrica": "DIN 912", "DIN 933 - Esagonale filetto totale": "DIN 933",
        "DIN 931 - Esagonale filetto parziale": "DIN 931", "DIN 7991 - Testa svasata esagono incassato": "DIN 7991",
        "ISO 7380 - Testa bombata esagono incassato": "ISO 7380", "DIN 571 - Tirafondo per legno": "DIN 571",
        "DIN 7504-K - Autoperforante Esagonale": "DIN 7504-K", "DIN 7504-N - Autoperforante Bombata": "DIN 7504-N",
        "DIN 7504-P - Autoperforante Svasata": "DIN 7504-P"
    },
    "Dado": {"": "", "DIN 934 - Esagonale standard": "DIN 934", "DIN 985 - Autobloccante nylon": "DIN 985", "DIN 6923 - Flangiato zigrinato": "DIN 6923"},
    "Rondella": {"": "", "DIN 125 - Piana standard": "DIN 125", "DIN 9021 - Fascia larga": "DIN 9021", "DIN 6798 - Dentellata": "DIN 6798", "DIN 127 - Grower (elastica)": "DIN 127"},
    "Bullone": {"": ""}, "Inserti filettati": {"": ""}
}

TERMINI_ANTICIPATI = [
    "CENTRAL", "LEFT", "RIGHT", "REINFORCED", "INTERNAL", "EXTERNAL", "STATIC", "ADJUSTABLE", "SEISMIC",
    "MULTIBAR", "MULTISTRIP", "TOP", "INTER-BASE SHELF", "ROUNDED", "SLOPING", "SHAPED", "CONNECTING", "SHUTTER", "COUPLING",
    "WIRE", "GRIPPED", "CHROMED", "PAINTED", "MESH", "SLIDING", "CURVED", "STRAIGHT", "MILLING", "WIRE-BASKET",
    "SEMICIRCULAR", "SINGLE", "DOUBLE", "END", "L-SHAPED", "U-SHAPED", "SERRATED LOCK", "ROTATING", "CTR", "UPRIGHT-GRAFT"
]

# =========================================================
# 2. INTERFACCIA UTENTE (Layout & Logica)
# =========================================================

# --- MAPPA CATEGORIE -> PILLS SPECIFICI ---
MAPPA_PILLS_CATEGORIA = {
    "METAL COMP": PILLS_COMP,
    "WOOD COMP": PILLS_COMP,      # Modificalo se crei un PILLS_WOOD dedicato
    "PLASTIC COMP": PILLS_COMP,   # Modificalo se crei un PILLS_PLASTIC dedicato
    "GLASS COMP": PILLS_COMP,     # Modificalo se crei un PILLS_GLASS dedicato
    "FASTENER": PILLS_FASTNER,
    "ASSEMBLY": PILLS_ASSEMBLY
}

if "mat_en" not in st.session_state: 
    st.session_state.mat_en = ""

# --- HEADER RISTRUTTURATO (Suggerimenti a SX, Titolo al CENTRO, Reset a DX) ---
col_s, col_t, col_r = st.columns([1.5, 2.5, 1], vertical_alignment="bottom")

with col_s:
    # Segnalazioni spostate comodamente a sinistra
    with st.expander("💡 Invia Suggerimento / Richiesta"):
        with st.form("form_segnalazione_top"):
            tipo_segnalazione = st.selectbox("Tipo richiesta", ["Nuovo Particolare", "Nuovo Pill (+)", "Nuova Traduzione", "Altro"])
            dettaglio_richiesta = st.text_area("Descrivi la modifica:", placeholder="Es. Vorrei inserire...", height=80)
            btn_invia_top = st.form_submit_button("📩 Invia", use_container_width=True)
            
            if btn_invia_top:
                if not dettaglio_richiesta.strip():
                    st.warning("⚠️ Inserisci una descrizione.")
                else:
                    try:
                        conn_s = st.connection("gsheets_segnalazioni", type=GSheetsConnection)
                        
                        # --- MODIFICA QUI: Usiamo ZoneInfo per l'orario italiano perfetto ---
                        orario_italiano = datetime.datetime.now(ZoneInfo("Europe/Rome"))
                        
                        nuovo_fb = {
                            "Timestamp": orario_italiano.strftime("%Y-%m-%d %H:%M:%S"),
                            "Utente": st.session_state.utente_corrente,
                            "Tipo": tipo_segnalazione,
                            "Descrizione": dettaglio_richiesta.strip(),
                            "Stato": "DA PROCESSARE"
                        }
                        df_s = conn_s.read(ttl=0)
                        df_agg = pd.concat([df_s, pd.DataFrame([nuovo_fb])], ignore_index=True)
                        conn_s.update(data=df_agg)
                        st.success("🎉 Richiesta inviata con successo!")
                    except Exception as e:
                        st.error(f"⚠️ Errore di registrazione: {e}")  # Corretto il piccolo typo nel blocco except precedente!

with col_t: 
    # Titolo perfettamente centrato con markdown HTML pulito
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="margin: 0; font-size: 1.8rem;">⚙️ REG - Title Generator</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 0.85rem; color: gray; margin-top: 4px;'>Utente attivo: <b>{st.session_state.utente_corrente}</b></p>", unsafe_allow_html=True)

with col_r: 
    st.button("🔄 AZZERA", on_click=activate_reset, use_container_width=True)

st.markdown("---")

col_left, col_workarea = st.columns([1, 4], gap="large")

with col_left:
    st.subheader("📂 1. Categoria")
    mappa_estetica = {
        "METAL COMP": "⚙️ METAL COMP", "WOOD COMP": "🪵 WOOD COMP", 
        "PLASTIC COMP": "🧪 PLASTIC COMP", "GLASS COMP": "🧊 GLASS COMP", 
        "FASTENER": "🔩 FASTENER", "ASSEMBLY": "🏛️ ASSEMBLY"
    }
    macro_it = st.radio(
        "Seleziona categoria:", 
        options=list(DATABASE.keys()), 
        format_func=lambda x: mappa_estetica.get(x, x), 
        key="radio_macro", 
        label_visibility="collapsed"
    )

with col_workarea:
    st.subheader("🛠️ 2. Configurazione Base")
    c_mat, c_search = st.columns([1, 1.5])
    
    with c_mat:
        if "ASSEMBLY" in macro_it.upper(): 
            st.toggle("ASSEMBLATO", key="check_assembled")
            st.session_state.mat_en = "" 
        else:
            materiali_disponibili = MATERIALI_CONFIG.get(macro_it, {})
            if materiali_disponibili:
                mat_it = st.radio("Materiale:", options=list(materiali_disponibili.keys()), horizontal=True, key="mat_radio")
                temp_mat_en = materiali_disponibili[mat_it]
                
                if mat_it.upper() == "ZINCATO":
                    tipo_zinc = st.radio("Tipo zincatura:", ["A FREDDO (Zinc Plated)", "A CALDO (Galvanized)"], horizontal=True, key="zinc_type_radio")
                    st.session_state.mat_en = "ZINC PLATED" if "A FREDDO" in tipo_zinc else "GALVANIZED"
                else:
                    st.session_state.mat_en = temp_mat_en

    with c_search:
        part_info = DATABASE.get(macro_it, {}).get("Particolari", {})
        scelta_part_it = st.selectbox(
            "Cerca dettaglio:", 
            options=sorted(list(part_info.keys())), 
            index=None, 
            placeholder="Cerca componente...", 
            format_func=lambda x: f"🔧 {x} ({part_info[x][0]})" if x else "Seleziona...", 
            key="selectbox_part"
        )

    st.markdown("---")
    
# --- SEZIONE 3: EXTRA E NOTE (FILTRATI PER CATEGORIA) ---
    st.subheader("✨ 3. Extra e Note")
    st.session_state.conflitto_attivo = False 

    if scelta_part_it:
        # Pescaggio pulito e mirato dei pills basato esclusivamente sulla categoria attiva
        dizionario_corrente_pills = MAPPA_PILLS_CATEGORIA.get(macro_it, PILLS_COMP)
        extra_options = list(dizionario_corrente_pills.keys())
        
        if extra_options:
            st.markdown(f"**Caratteristiche ({macro_it} - Seleziona):**")
            
            tag_selezionati = st.multiselect(
                "Caratteristiche specifiche:",
                options=sorted(extra_options),
                key="extra_tags",
                label_visibility="collapsed",
                placeholder=f"Cerca caratteristiche per {macro_it}..."
            )
            
            tags_scelti_raw = tag_selezionati
            tags_scelti_upper = [str(t).upper().strip() for t in tags_scelti_raw]
            
            conflitto_rilevato = False
            messaggio_errore = ""

            for gruppo in COPPIE_INCOMPATIBILI:
                gruppo_upper = [str(elemento).upper().strip() for elemento in gruppo]
                intersezione = set(gruppo_upper).intersection(set(tags_scelti_upper))
                if len(intersezione) > 1:
                    conflitto_rilevato = True
                    nomi_originali = [t for t in tags_scelti_raw if str(t).upper().strip() in intersezione]
                    messaggio_errore = f"⚠️ **Conflitto rilevato**: Non puoi combinare **{', '.join(nomi_originali)}**."
                    break

            if conflitto_rilevato:
                st.session_state.conflitto_attivo = True
                st.error(messaggio_errore)

        # Gestione Sotto-Opzioni (+)
        tags_attuali = st.session_state.get("extra_tags", [])
        pills_con_plus = [t for t in tags_attuali if t.endswith("(+)")]
        if pills_con_plus:
            st.markdown("---")
            st.markdown("⚙️️ **Configurazione Dettagli Opzionali (+):**")
            for pill_p in pills_con_plus:
                sub_dict = SUB_OPTIONS_CONFIG.get(pill_p, {})
                if sub_dict:
                    st.selectbox(
                        f"Seleziona variante per **{pill_p}**:",
                        options=list(sub_dict.keys()),
                        key=f"sub_{pill_p}"
                    )
                elif pill_p in EXTRA_CON_INPUT_MANUALE:
                    st.text_input(
                        f"Inserisci valore per **{pill_p}**:",
                        key=f"manual_{pill_p}"
                    )

    st.markdown("---")
    
    # --- SEZIONE 4: MISURE E NOTE LIBERE ---
    st.subheader("📏 4. Dimensioni e Note")
    c_dim1, c_dim2, c_dim3, c_dim4 = st.columns(4)
    with c_dim1: st.text_input("Lunghezza (L):", key="dim_l")
    with c_dim2: st.text_input("Profondità (P):", key="dim_p")
    with c_dim3: st.text_input("Altezza (H):", key="dim_h")
    with c_dim4: st.text_input("Diametro / Spessore (Ø/S):", key="dim_dia")

    if scelta_part_it in MAPPA_NORMATIVE_FASTENER:
        norme_disp = MAPPA_NORMATIVE_FASTENER[scelta_part_it]
        st.selectbox("Normativa di riferimento:", options=list(norme_disp.keys()), key="norm_select")

    st.text_input("Note libere (es. 'con ruote', 'verniciato'):", key="extra_text")
    
    st.markdown("**Tag di compatibilità:**")
    st.pills(
        "Modello compatibilità:",
        options=[opz for opz in OPZIONI_COMPATIBILITA if opz != ""],
        key="comp_tags",
        label_visibility="collapsed"
    )
    
    st.checkbox("Aggiungi marcatura (UNI EN 1090-1)", key="check_1090")

# =========================================================
# 3. LOGICA DI GENERAZIONE (MOTORE DI CALCOLO)
# =========================================================
st.divider()

def traduci_note(testo):
    if not testo: return ""
    glossario_locale = {
        "mensola": "BRACKET", "mensole": "BRACKETS", "gondola": "GONDOLA",
        "spalla": "FRAME", "innesto": "COUPLING", "montante": "UPRIGHT", 
        "losanga": "LOSANGA", "rivestimento": "BACK PANEL", "cancelletto": "GATE", 
        "vasca": "TANK", "con ruote": "WITH WHEELS", "senza ruote": "WITHOUT WHEELS", 
        "rinforzato": "REINFORCED", "verniciato": "PAINTED", "zincato": "GALVANIZED", 
        "superiore": "UPPER", "trasparente": "TRANSPARENT"
    }
    testo_elaborato = testo.lower().strip()
    for it, en in glossario_locale.items():
        if it in testo_elaborato:
            testo_elaborato = testo_elaborato.replace(it, en)
    try:
        traduzione = MyMemoryTranslator(source='it-IT', target='en-US').translate(testo_elaborato)
        if traduzione and "too many requests" not in traduzione.lower():
            return traduzione.upper()
    except Exception:
        pass
    return testo_elaborato.upper()

conflitto_bloccante = st.session_state.get("conflitto_attivo", False)

if st.button("🚀 GENERA STRINGA FINALE", use_container_width=True, disabled=conflitto_bloccante):
    if scelta_part_it:
        part_db = DATABASE.get(macro_it, {}).get("Particolari", {}).get(scelta_part_it, ["", "PILLS_VUOTO", ""])
        part_en = part_db[0].upper()
        dict_extra_db = TUTTI_I_PILLS_GLOBALE
        
        lista_prima = []
        lista_dopo = []
        tags_selezionati = st.session_state.get('extra_tags', [])
        
        if tags_selezionati:
            for tag_master in tags_selezionati:
                if tag_master in SUB_OPTIONS_CONFIG:
                    chiave_sub = st.session_state.get(f"sub_{tag_master}", "")
                    traduzione = SUB_OPTIONS_CONFIG[tag_master].get(chiave_sub, chiave_sub).upper()
                elif tag_master in EXTRA_CON_INPUT_MANUALE:
                    traduzione = st.session_state.get(f"manual_{tag_master}", "").upper()
                else:
                    traduzione = dict_extra_db.get(tag_master, tag_master).upper()
                
                if traduzione in TERMINI_ANTICIPATI:
                    lista_prima.append(traduzione)
                else:
                    lista_dopo.append(traduzione)

        dim_list = []
        L = st.session_state.get("dim_l", "").strip()
        P = st.session_state.get("dim_p", "").strip()
        H = st.session_state.get("dim_h", "").strip()
        D = st.session_state.get("dim_dia", "").strip()

        if L: dim_list.append(f"L{L.upper()}")
        if P: dim_list.append(f"P{P.upper()}")
        if H: dim_list.append(f"H{H.upper()}")
        if D:
            prefix_d = "M" if (macro_it == "FASTENER" and not D.upper().startswith("M")) else "Ø"
            dim_list.append(f"{prefix_d}{D.upper()}")
        
        dim_str = " ".join(dim_list)
        norma_sel = st.session_state.get("norm_select", "")
        norma_str = MAPPA_NORMATIVE_FASTENER.get(scelta_part_it, {}).get(norma_sel, "")

        note_it = st.session_state.get("extra_text", "").strip()
        note_en = traduci_note(note_it)

        if macro_it == "ASSEMBLY":
            prefix_base = "ASSEMBLED" if st.session_state.get("check_assembled") else ""
        else:
            prefix_base = st.session_state.get("mat_en", "").upper()

        elementi_prefisso = [prefix_base] + lista_prima
        prefisso_lista = [p.strip().upper() for p in elementi_prefisso if p.strip()]
        prefix_completo = " ".join(prefisso_lista)
        part_en_upper = part_en.strip().upper()
        
        parole_prefisso = set(prefix_completo.split())
        parole_componente = set(part_en_upper.split())

        if parole_prefisso and (parole_prefisso.issubset(parole_componente) or part_en_upper.startswith(prefix_completo)):
            core = part_en_upper
        else:
            core = f"{prefix_completo} {part_en_upper}".strip()
        
        info_aggiuntive = []
        if lista_dopo: info_aggiuntive.append(" ".join(lista_dopo))
        if dim_str: info_aggiuntive.append(dim_str)
        if norma_str: info_aggiuntive.append(norma_str)
        
        corpo = f"{core} {' '.join(info_aggiuntive)}".strip()
        
        if note_en:
            corpo = f"{corpo}, {note_en}"
            
        comp_tag = st.session_state.get("comp_tags", "").strip().upper()
        if comp_tag:
            corpo = f"{corpo} - {comp_tag}"
            
        if st.session_state.get("check_1090"):
            corpo += " (UNI EN 1090-1)"

        stringa_definitiva = " ".join(corpo.split()).upper()
        st.session_state['stringa_stabile'] = stringa_definitiva
        st.session_state['tags_stabili'] = [macro_it, scelta_part_it] + tags_selezionati

# =========================================================
# 4. OUTPUT E MONITORAGGIO
# =========================================================
def sincronizza_modifica():
    if 'input_manuale' in st.session_state:
        st.session_state['stringa_stabile'] = st.session_state['input_manuale'].upper()

risultato_container = st.container()

if st.session_state.get('stringa_stabile'):
    with risultato_container:
        st.markdown("---")
        col_titolo, col_opt = st.columns([4, 1])
        with col_titolo:
            st.subheader("📋 Risultato Finale")
        
        modifica_attiva = col_opt.toggle("✏️ Modifica", key="toggle_manual_edit")

        if modifica_attiva:
            if "input_manuale" not in st.session_state:
                st.session_state["input_manuale"] = st.session_state["stringa_stabile"]
            
            st.text_input(
                "Modifica manuale stringa:", 
                key="input_manuale",
                on_change=sincronizza_modifica,
                label_visibility="collapsed"
            )
        else:
            st.code(st.session_state['stringa_stabile'], language=None)

        stringa_attuale = st.session_state['stringa_stabile']
        lunghezza = len(stringa_attuale)
        perc = min(lunghezza / 100, 1.0)
        
        if lunghezza > 100:
            st.error(f"⚠️ LIMITE CRITICO: {lunghezza}/100")
        elif lunghezza >= 90:
            st.warning(f"🟡 ATTENZIONE: {lunghezza}/100")
        else:
            st.markdown(f"<p style='color: #00cc66; font-size: 0.8rem; margin-bottom: -10px;'>✅ Lunghezza ottimale: {lunghezza}/100</p>", unsafe_allow_html=True)
        
        st.progress(perc)
