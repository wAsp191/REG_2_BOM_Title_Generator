# =========================================================
# SEZIONE IMPORT
# =========================================================
import datetime
import time
from zoneinfo import ZoneInfo

from deep_translator import MyMemoryTranslator
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# =========================================================
# NAVIGAZIONE E ROUTER PRINCIPALE (App / Admin)
# =========================================================
st.sidebar.title("🧭 Navigazione")
scelta_pagina = st.sidebar.radio("Vai a:", ["⚙️ Generatore", "🔒 Pannello Admin"])

if scelta_pagina == "🔒 Pannello Admin":
  # Se non siamo ancora autenticati come admin, mostriamo il box centrato
  if "admin_autenticato" not in st.session_state:
    st.session_state.admin_autenticato = False

  if not st.session_state.admin_autenticato:
    # Colonne spaziatrici per centrare il login admin perfettamente nello schermo
    col_spaz_sx, col_admin_centro, col_spaz_dx = st.columns([1, 1.5, 1])

    with col_admin_centro:
      with st.container(border=True):
        st.markdown(
            "<h2 style='text-align: center;'>🔐 Area Riservata</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: gray; font-size: 0.9rem;'>Inserisci"
            " la password di amministrazione</p>",
            unsafe_allow_html=True,
        )

        with st.form("form_login_admin"):
          password_inserita = st.text_input("Password Admin:", type="password")
          btn_login_admin = st.form_submit_button(
              "Accedi al Pannello", use_container_width=True
          )

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
      st.info(
          "📭 Nessuna segnalazione presente nel Google Sheet al momento."
      )
    else:
      st.subheader("📋 Gestione ed Eliminazione Rapida Richieste")
      st.markdown(
          "Spunta le caselle a sinistra delle richieste che desideri rimuovere"
          " definitivamente:"
      )

      # Intestazione tabella interattiva
      col_i0, col_i1, col_i2, col_i3, col_i4, col_i5 = st.columns(
          [0.6, 1.5, 1.2, 1.5, 2.5, 1.2]
      )
      with col_i0:
        st.markdown("**Az.**")
      with col_i1:
        st.markdown("**Timestamp**")
      with col_i2:
        st.markdown("**Utente**")
      with col_i3:
        st.markdown("**Tipo**")
      with col_i4:
        st.markdown("**Descrizione**")
      with col_i5:
        st.markdown("**Stato**")
      st.markdown("---")

      indici_da_eliminare = []

      for idx, row in df_segnalazioni.iterrows():
        c_chk, c_ts, c_ut, c_tipo, c_desc, c_stato = st.columns(
            [0.6, 1.5, 1.2, 1.5, 2.5, 1.2]
        )

        with c_chk:
          if st.checkbox(
              "Seleziona", key=f"chk_del_{idx}", label_visibility="collapsed"
          ):
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
        if st.button(
            "🗑️ Elimina Definitivamente Selezionati", type="primary"
        ):
          try:
            df_aggiornato = df_segnalazioni.drop(
                indici_da_eliminare
            ).reset_index(drop=True)
            conn_admin.update(data=df_aggiornato)
            st.success("🎉 Segnalazioni selezionate eliminate con successo!")
            st.rerun()
          except Exception as e:
            st.error(f"⚠️ Errore durante l'aggiornamento del foglio: {e}")
      else:
        st.info(
            "💡 Spunta almeno una casella nella lista per abilitare"
            " l'eliminazione."
        )

  except Exception as e:
    st.error(f"⚠️ Errore di comunicazione con Google Sheets: {e}")

  st.stop()

# =========================================================
# 0. CONFIGURAZIONE PAGINA E CREDENZIALI DI ACCREDITAMENTO
# =========================================================
st.set_page_config(page_title="Technical Generator v2.0", layout="wide")

# Database utenti autorizzati
UTENTI_AUTORIZZATI = {
    "admin": {"password": "reg2026", "nome": "Amministratore di Sistema"},
    "pierluigi.giorgi": {
        "password": "pierluigigiorgi",
        "nome": "Pierluigi Giorgi (Ufficio Tecnico)",
    },
    "gaia.gualtieri": {
        "password": "gaiagualtieri",
        "nome": "Gaia Gualtieri (Ufficio Tecnico)",
    },
    "emanuela.bois": {
        "password": "emanuelabois",
        "nome": "Emanuela Bois (Ufficio Tecnico)",
    },
    "andrea.parrini": {
        "password": "andreaparrini",
        "nome": "Andrea Parrini (Ufficio Tecnico)",
    },
    "gianfranco.palmisano": {
        "password": "gianfrancopalmisano",
        "nome": "Gianfranco Palmisano (Ufficio Tecnico)",
    },
    "giuseppe.pieri": {
        "password": "giuseppepieri",
        "nome": "Giuseppe Pieri (Ufficio Tecnico)",
    },
    "carlo.castellani": {
        "password": "carlocastellani",
        "nome": "Carlo Castellani (Ufficio Tecnico)",
    },
    "enrico.sarti": {
        "password": "enricosarti",
        "nome": "Enrico Sarti (Ufficio Tecnico)",
    },
}

# CSS personalizzato per la compattezza
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2.0rem !important;
            padding-bottom: 0rem !important;
        }
        [data-testid="stVerticalBlock"] > div {
            flex-direction: column;
            gap: 0.15rem !important;
        }
        h1 { margin-bottom: -0.8rem !important; font-size: 1.6rem !important; }
        h2 { margin-bottom: -0.6rem !important; font-size: 1.2rem !important; }
        h3 { margin-bottom: -0.4rem !important; font-size: 1.0rem !important; }
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
            font-size: 1.05rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMarkdownContainer"] p {
            font-size: 0.95rem !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            margin-bottom: 6px !important;
            padding: 3px 0px !important;
            transition: all 0.2s ease;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Gestione dello stato di autenticazione
if "autenticato" not in st.session_state:
  st.session_state.autenticato = False
if "utente_corrente" not in st.session_state:
  st.session_state.utente_corrente = ""

# --- SCHERMATA DI LOGIN INIZIALE (CENTRATA) ---
if not st.session_state.autenticato:
  col_spazio_sx, col_login_centro, col_spazio_dx = st.columns([1, 1.5, 1])

  with col_login_centro:
    with st.container(border=True):
      st.markdown(
          "<h2 style='text-align: center;'>🔐 Accesso - REG 2.0</h2>",
          unsafe_allow_html=True,
      )
      st.markdown(
          "<p style='text-align: center; color: gray; font-size: 0.9rem;'>Inserisci"
          " le tue credenziali</p>",
          unsafe_allow_html=True,
      )

      with st.form("form_login"):
        username_input = st.text_input("Username").strip().lower()
        password_input = st.text_input("Password", type="password")
        btn_login = st.form_submit_button("🔑 Accedi", use_container_width=True)

        if btn_login:
          if (
              username_input in UTENTI_AUTORIZZATI
              and UTENTI_AUTORIZZATI[username_input]["password"]
              == password_input
          ):
            st.session_state.autenticato = True
            st.session_state.utente_corrente = UTENTI_AUTORIZZATI[
                username_input
            ]["nome"]
            st.rerun()
          else:
            st.error("❌ Credenziali non valide. Riprova.")

  st.stop()

# Notifica toast post-reset
if st.session_state.get("reset_eseguito"):
  st.toast("Interfaccia pulita!", icon="✨")
  st.session_state["reset_eseguito"] = False


def activate_reset():
  defaults = {
      "comp_tags": [],
      "selectbox_part": None,
      "extra_tags": [],
      "check_1090": False,
      "check_assembled": False,
      "stringa_stabile": "",
      "tags_stabili": [],
  }
  text_keys = [
      "dim_l",
      "dim_l_gen",
      "dim_p",
      "dim_h",
      "dim_dia",
      "dim_dia_gen",
      "dim_s",
      "extra_text",
      "stringa_editabile",
      "input_manuale",
  ]
  for key, val in defaults.items():
    st.session_state[key] = val
  for key in text_keys:
    if key in st.session_state:
      st.session_state[key] = ""
  for key in list(st.session_state.keys()):
    if key.startswith(("manual_", "sub_")):
      del st.session_state[key]
  st.session_state["reset_eseguito"] = True


# =========================================================
# 1. DIZIONARI, PILLS E DATABASE CENTRALIZZATO
# =========================================================
COPPIE_INCOMPATIBILI = [
    {"Statico", "Antisismico"},
    {"Angolo aperto", "Angolo chiuso"},
    {"Portante", "Non portante"},
    {"Singolo", "Doppio"},
    {"Per ripiano in vetro", "Per ripiano in legno"},
    {"Con serratura", "Senza serratura"},
    {"Passo 25", "Passo 50"},
    {"L50", "L55"},
    {"Scorrevoli", "A saracinesca"},
    {"Per attacco montante", "Per attacco fiancata"},
    {"Superiore", "Tra ripiani di base"},
    {"Dritto", "Inclinato"},
    {"Cromato", "Verniciato"},
    {"Multibarra", "Multilame", "In rete"},
    {"Profilo a L", "Profilo a U"},
    {"Per ripiano di base", "Per fiancata"},
    {"Terminale", "Centrale"},
    {"Liscio", "Liscia", "Forato", "Forata", "In filo"},
    {"Zincato", "Verniciata"},
]

GLOSSARIO_TECNICO = {
    "mensola": "BRACKET",
    "mensole": "BRACKETS",
    "gondola": "GONDOLA",
    "spalla": "FRAME",
    "innesto": "COUPLING",
    "montante": "UPRIGHT",
    "per": "FOR",
    "losanga": "LOSANGA",
    "cancelletto": "GATE",
    "vasca": "TANK",
}

SUB_OPTIONS_CONFIG = {
    "VPA (+)": {
        "Serie S": "S SERIES",
        "Serie SS": "SS SERIES",
        "Serie M": "M SERIES",
        "Serie L": "L SERIES",
    },
    "Con distanziale (+)": {
        "L100": "S100",
        "L150": "S150",
        "L200": "S200",
        "L250": "S250",
    },
    "Numero diagonali (+)": {
        "Doppie": "DD",
        "Triple": "TD",
        "Quadruple": "QD",
    },
    "Sezione (+)": {
        "L55": "L55",
        "L80 Z/S": "L80 Z/S",
        "L80 Z/M": "L80 Z/M",
        "L100 Z/S": "L100 Z/S",
        "L100 Z/M": "L100 Z/M",
        "L120 Z/S": "L120 Z/S",
        "70X30": "70X30",
        "90X30": "90X30",
        "30X30": "30X30",
    },
    "Tipologia di mensola (+)": {
        "Mensola saldata a filo superiore": "UPPER BRACKET",
        "Mensola saldata a filo inferiore": "LOWER BRACKET",
    },
    "Compatibilità piede di base (+)": {
        "Per piede H90": "FOR H90 BASE FOOT",
        "Per piede H100": "FOR H100 BASE FOOT",
        "Per piede H150": "FOR H150 BASE FOOT",
    },
    "Attacco gancio (+)": {
        "Attacco barra": "HOOK FOR BAR",
        "Attacco multilame": "HOOK FOR MULTISTRIP",
        "Attacco pannello forato": "HOOK FOR SLOTTED PANEL",
    },
    "Orientamento (+)": {"Destra": "RIGHT", "Sinistra": "LEFT"},
    "Posizioni multiple (+)": {
        "1 posizione": "1 POSITION",
        "2 posizioni": "2 POSITIONS",
        "3 posizioni": "3 POSITIONS",
    },
    "Altezza piede (+)": {"H90": "H90", "H100": "H100", "H150": "H150"},
    "Predisposto per montante (+)": {
        "L80": "FOR L80 UPRIGHT",
        "L100/L120": "FOR L100/L120 UPRIGHT",
    },
    "Numero tasche (+)": {"1 Tasca": "1 POCKET", "2 Tasche": "2 POCKETS"},
    "Numero gradoni (+)": {
        "1 gradone": "1 STEP",
        "2 gradoni": "2 STEPS",
        "3 gradoni": "3 STEPS",
    },
    "Asimmetrica (+)": {"AS240": "AS240", "AS340": "AS340", "AS440": "AS440"},
}

EXTRA_CON_INPUT_MANUALE = ["Sezione circolare", "Sezione quadrata"]

MATERIALI_CONFIG = {
    "METAL COMP": {
        "NESSUNO": "",
        "METAL": "METAL",
        "ZINCATO": "GALVANIZED",
        "INOX": "STAINLESS STEEL",
        "ALLUMINIO": "ALUMINIUM",
    },
    "WOOD COMP": {
        "NESSUNO": "",
        "LAMINATO": "LAMINATED",
        "NOBILITATO": "MELAMINE",
        "TRUCIOLARE": "OSB",
        "HPL": "HPL",
    },
    "PLASTIC COMP": {
        "NESSUNO": "",
        "PLX": "PLX",
        "POLICARBONATO": "POLYCARBONATE",
        "PVC": "PVC",
        "GOMMA": "RUBBER",
    },
    "GLASS COMP": {
        "NESSUNO": "",
        "VETRO TEMPRATO": "TEMPERED",
        "VETRO SATINATO": "SATIN",
    },
    "FASTENER": {
        "NESSUNO": "",
        "NERO": "",
        "ZINCATO": "GALVANIZED",
        "BRUNITO": "BURNISHED",
    },
    "ASSEMBLY": {},
}

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
    "Minirack": "MINIRACK",
    "Multibarra": "MULTIBAR",
    "Multilame": "MULTISTRIP",
    "Nervata": "RIBBED",
    "Nervato": "RIBBED",
    "Non portante": "NON LOAD-BEARING",
    "Numero diagonali (+)": "",
    "Orientamento (+)": "",
    "Passo 25": "PITCH 25",
    "Passo 50": "PITCH 50",
    "Per Top legno": "FOR TOP SHELF",
    "Per attacco fiancata": "HOOK ONTO SIDE-PANEL",
    "Per controventatura": "FOR CROSS-WALL",
    "Per crociera verticale": "FOR VERTICAL CROSS-WALL",
    "Per fiancata": "FOR SIDE PANEL",
    "Per montante M70": "FOR M70 UPRIGHT",
    "Per montante M90": "FOR M90 UPRIGHT",
    "Per ripiano": "FOR SHELF",
    "Per ripiano di base": "FOR BASE SHELF",
    "Per ripiano in legno": "FOR WOODEN SHELF",
    "Per ripiano in vetro": "FOR GLASS SHELF",
    "Piegato": "BENT",
    "Piegato-saldato": "BENT AND WELDED",
    "Portante": "LOAD-BEARING",
    "Posizioni multiple (+)": "",
    "Predisposto per montante (+)": "",
    "Predisposto per portaprezzo": "ACCEPTS TICKET-HOLDER",
    "Profilo a L": "L-SHAPED",
    "Profilo a U": "U-SHAPED",
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
    "Sezione circolare": "CIRCULAR SECTION",
    "Sezione quadrata": "SQUARE SECTION",
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
    "Verniciato": "PAINTED",
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
    "Testa svasata": "COUNTERSUNK HEAD",
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
    "Zincato": "GALVANIZED",
}

MAPPA_PILLS_CATEGORIA = {
    "METAL COMP": PILLS_COMP,
    "WOOD COMP": PILLS_COMP,
    "PLASTIC COMP": PILLS_COMP,
    "GLASS COMP": PILLS_COMP,
    "FASTENER": PILLS_FASTNER,
    "ASSEMBLY": PILLS_ASSEMBLY,
}

OPZIONI_COMPATIBILITA = [
    "",
    "F25",
    "F25 BESPOKE",
    "F25 READY",
    "F50",
    "F50 BESPOKE",
    "F50 READY",
    "UNIVERSAL",
    "BC",
    "FORTISSIMO",
    "MINIRACK",
    "UNIMOB",
]

MAPPA_NORMATIVE_FASTENER = {
    "Vite": ["DIN 912", "DIN 933", "DIN 7991", "ISO 7380", "UNI 5931"],
    "Dado": ["DIN 934", "DIN 985", "DIN 6923", "UNI 5588"],
    "Rondella": ["DIN 125", "DIN 9021", "DIN 6798", "UNI 6592"],
    "Bullone": ["DIN 603", "DIN 931", "ISO 4014"],
    "Inserti filettati": ["UNI 8896", "DIN 7965"],
}

TERMINI_ANTICIPATI = ["RIGHT", "LEFT", "UPPER", "LOWER", "SINGLE", "DOUBLE"]

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
            "Lamiera generica": [
                "SHEET METAL",
                "PILLS_COMP",
                "GENERIC SHEET METAL",
            ],
            "Pannello frontale": ["FRONT PANEL", "PILLS_COMP", "PANEL"],
            "Adattatore": ["ADAPTER", "PILLS_COMP", "ADAPTER"],
            "Canalina passa cavi": ["CABLE TRAY", "PILLS_COMP", "ESA"],
            "Vasca": ["TANK", "PILLS_COMP", "TANK"],
            "Tamponamento": ["BUFFER PANEL", "PILLS_COMP", "BUFFER"],
            "Protezione": [
                "PROTECTION FOR PERFORATED SHELF",
                "PILLS_COMP",
                "PROTECTION",
            ],
            "Portaprezzo": ["TICKET-HOLDER", "PILLS_COMP", "TICKET-HOLDER"],
        },
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
            "Asta in legno": ["WOODEN ROD", "PILLS_COMP", "ROD"],
        },
    },
    "PLASTIC COMP": {
        "macro_en": "PLASTIC COMPONENT",
        "Particolari": {
            "Tappo": ["PLASTIC CAP", "PILLS_COMP", "CAP"],
            "Guarnizione": ["GASKET", "PILLS_COMP", "ACCESSORY"],
            "Cerniera": ["HINGE", "PILLS_COMP", "ACCESSORY"],
            "Divisorio": ["DIVIDER", "PILLS_COMP", "DIVIDER"],
            "Portaprezzo": ["TICKET-HOLDER", "PILLS_COMP", "TICKET-HOLDER"],
            "Pannello in plexiglass": ["PLEXIGLASS PANEL", "PILLS_COMP", "PANEL"],
        },
    },
    "GLASS COMP": {
        "macro_en": "GLASS COMPONENT",
        "Particolari": {
            "Ripiano Vetro": ["GLASS SHELF", "PILLS_COMP", "SHELF"],
            "Anta Vetro": ["GLASS DOOR", "PILLS_COMP", "DOOR"],
            "Pannello Vetro": ["GLASS PANEL", "PILLS_COMP", "PANEL"],
        },
    },
    "FASTENER": {
        "macro_en": "FASTENER",
        "Particolari": {
            "Vite": ["SCREW", "PILLS_FASTNER", "FASTENER"],
            "Dado": ["NUT", "PILLS_FASTNER", "FASTENER"],
            "Rondella": ["WASHER", "PILLS_FASTNER", "FASTENER"],
            "Bullone": ["BOLT", "PILLS_FASTNER", "FASTENER"],
            "Inserti filettati": ["THREADED INSERT", "PILLS_FASTNER", "FASTENER"],
        },
    },
    "ASSEMBLY": {
        "macro_en": "ASSEMBLY",
        "Particolari": {
            "Scaffale composito": ["SHELVING UNIT", "PILLS_ASSEMBLY", "ASSEMBLY"],
            "Mobile cassa": ["CHECKOUT COUNTER", "PILLS_ASSEMBLY", "ASSEMBLY"],
            "Espositore": ["DISPLAY UNIT", "PILLS_ASSEMBLY", "ASSEMBLY"],
            "Banco da lavoro": ["WORKBENCH", "PILLS_ASSEMBLY", "ASSEMBLY"],
            "Carrello": ["TROLLEY", "PILLS_ASSEMBLY", "ASSEMBLY"],
        },
    },
}

# =========================================================
# 2. INTERFACCIA UTENTE PRINCIPALE (Layout & Logica)
# =========================================================

# --- INTESTAZIONE APP ---
col_head_sx, col_head_cx, col_head_dx = st.columns([1.2, 2.5, 0.8])

with col_head_sx:
  with st.expander("💡 Invia Suggerimento / Segnalazione"):
    with st.form("form_segnalazione_user"):
      tipo_segnalazione = st.selectbox(
          "Tipo:", ["Suggerimento", "Segnalazione Errore", "Altro"]
      )
      descrizione_segnalazione = st.text_area("Descrizione:")
      btn_invia_segnalazione = st.form_submit_button(
          "📨 Invia", use_container_width=True
      )

      if btn_invia_segnalazione and descrizione_segnalazione.strip():
        try:
          conn_seg = st.connection(
              "gsheets_segnalazioni", type=GSheetsConnection
          )
          df_att = conn_seg.read(ttl=0)

          ora_locale = (
              datetime.datetime.now(ZoneInfo("Europe/Rome")).strftime(
                  "%Y-%m-%d %H:%M:%S"
              )
          )
          nuova_riga = pd.DataFrame([{
              "Timestamp": ora_locale,
              "Utente": st.session_state.utente_corrente,
              "Tipo": tipo_segnalazione,
              "Descrizione": descrizione_segnalazione.strip(),
              "Stato": "In attesa",
          }])

          df_finale = (
              pd.concat([df_att, nuova_riga], ignore_index=True)
              if df_att is not None
              else nuova_riga
          )
          conn_seg.update(data=df_finale)
          st.success("✨ Segnalazione inviata con successo!")
        except Exception as err:
          st.error(f"⚠️ Errore durante l'invio: {err}")

with col_head_cx:
  st.title("⚙️ REG - Technical Title Generator v2.0")
  st.caption(f"👤 Utente collegato: **{st.session_state.utente_corrente}**")

with col_head_dx:
  st.write("")
  if st.button(
      "🔄 AZZERA INTERFACCIA",
      type="secondary",
      use_container_width=True,
      on_click=activate_reset,
  ):
    pass

st.markdown("---")

# =========================================================
# WORKAREA A DUE COLONNE
# =========================================================
col_left, col_workarea = st.columns([1, 2.8], gap="large")

# --- COLONNA DI SINISTRA: SELEZIONE MACRO E PROPRIETÀ BASE ---
with col_left:
  st.subheader("📂 1. Macro Categoria")

  mappa_estetica = {
      "METAL COMP": "⚙️ METAL COMP",
      "WOOD COMP": "🪵 WOOD COMP",
      "PLASTIC COMP": "🧪 PLASTIC COMP",
      "GLASS COMP": "🧊 GLASS COMP",
      "FASTENER": "🔩 FASTENER",
      "ASSEMBLY": "🏗️ ASSEMBLY",
  }

  cat_scelta = st.radio(
      "Seleziona Categoria:",
      options=list(mappa_estetica.keys()),
      format_func=lambda x: mappa_estetica[x],
      key="radio_macro_cat",
  )

  st.divider()

  st.subheader("🧩 2. Particolare")
  particolari_disponibili = list(DATABASE[cat_scelta]["Particolari"].keys())
  part_scelto = st.selectbox(
      "Seleziona Particolare:",
      options=particolari_disponibili,
      key="selectbox_part",
  )

  st.divider()

  st.subheader("🎨 3. Materiale & Finitura")
  mat_options = MATERIALI_CONFIG.get(cat_scelta, {})
  if mat_options:
    materiale_scelto = st.selectbox(
        "Materiale/Finitura:", options=list(mat_options.keys()), key="select_mat"
    )
  else:
    materiale_scelto = "NESSUNO"
    st.info("Nessun materiale aggiuntivo per questa categoria.")

  st.divider()

  st.subheader("⚙️ 4. Compatibilità & Normative")
  compatibilita_scelta = st.selectbox(
      "Sistema / Compatibilità:",
      options=OPZIONI_COMPATIBILITA,
      key="select_compat",
  )

  normativa_scelta = ""
  if cat_scelta == "FASTENER" and part_scelto in MAPPA_NORMATIVE_FASTENER:
    normativa_scelta = st.selectbox(
        "Normativa:",
        options=[""] + MAPPA_NORMATIVE_FASTENER[part_scelto],
        key="select_norma",
    )

  st.divider()

  check_1090 = st.checkbox(
      "Certificazione EN 1090",
      value=st.session_state.get("check_1090", False),
      key="check_1090",
  )
  check_assembled = st.checkbox(
      "Fornito Montato (ASSEMBLED)",
      value=st.session_state.get("check_assembled", False),
      key="check_assembled",
  )


# --- COLONNA DI DESTRA: PILLS, DIMENSIONI E TITOLO GENERATO ---
with col_workarea:
  st.subheader("🏷️ 5. Caratteristiche & Proprietà (Pills)")

  diz_pills_categoria = MAPPA_PILLS_CATEGORIA.get(cat_scelta, {})

  # Calcolo pill disabilitate per incompatibilità
  tags_selezionati_correnti = st.session_state.get("comp_tags", [])
  if not isinstance(tags_selezionati_correnti, list):
    tags_selezionati_correnti = []

  # Filtro pills incompatibili
  pills_disponibili = list(diz_pills_categoria.keys())

  tags_scelti = st.multiselect(
      "Seleziona Tag Caratteristiche:",
      options=pills_disponibili,
      default=[t for t in tags_selezionati_correnti if t in pills_disponibili],
      key="comp_tags",
  )

  # Gestione sotto-opzioni dinamiche (+) e input manuali extra
  sotto_opzioni_tradotte = []
  input_manuali_extra = []

  if tags_scelti:
    col_sub1, col_sub2 = st.columns(2)

    for i, tag in enumerate(tags_scelti):
      # Se il tag richiede sotto-opzioni (+)
      if tag in SUB_OPTIONS_CONFIG:
        sub_cfg = SUB_OPTIONS_CONFIG[tag]
        with col_sub1 if i % 2 == 0 else col_sub2:
          sub_val = st.selectbox(
              f"Specifica per '{tag}':",
              options=list(sub_cfg.keys()),
              key=f"sub_{tag}",
          )
          if sub_val:
            sotto_opzioni_tradotte.append(sub_cfg[sub_val])

      # Se il tag richiede input manuale specifico
      if tag in EXTRA_CON_INPUT_MANUALE:
        with col_sub1 if i % 2 == 0 else col_sub2:
          val_man = st.text_input(
              f"Valore per '{tag}':", key=f"manual_{tag}"
          ).strip()
          if val_man:
            input_manuali_extra.append(f"{tag.upper()}: {val_man}")

  st.divider()

  st.subheader("📏 6. Dimensioni (mm)")

  col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
  with col_d1:
    dim_l = st.text_input(
        "L (Lunghezza):",
        value=st.session_state.get("dim_l", ""),
        key="dim_l",
        placeholder="es. 1000",
    )
  with col_d2:
    dim_p = st.text_input(
        "P (Profondità):",
        value=st.session_state.get("dim_p", ""),
        key="dim_p",
        placeholder="es. 400",
    )
  with col_d3:
    dim_h = st.text_input(
        "H (Altezza):",
        value=st.session_state.get("dim_h", ""),
        key="dim_h",
        placeholder="es. 2000",
    )
  with col_d4:
    dim_s = st.text_input(
        "S (Spessore):",
        value=st.session_state.get("dim_s", ""),
        key="dim_s",
        placeholder="es. 1.5",
    )
  with col_d5:
    dim_dia = st.text_input(
        "Ø (Diametro):",
        value=st.session_state.get("dim_dia", ""),
        key="dim_dia",
        placeholder="es. 20",
    )

  extra_text = st.text_input(
      "Note Extra / Testo Libero (opzionale):",
      value=st.session_state.get("extra_text", ""),
      key="extra_text",
      placeholder="es. Personalizzato per cliente XYZ",
  )

  st.divider()

  # =========================================================
  # 3. LOGICA DI COSTRUZIONE DEL TITOLO TECNICO
  # =========================================================
  st.subheader("✨ 7. Titolo Tecnico Generato")

  # 1. Nome base in Inglese
  info_part = DATABASE[cat_scelta]["Particolari"][part_scelto]
  nome_base_en = info_part[0]

  # 2. Traduzione Pill selezionate
  pills_tradotte = []
  for t in tags_scelti:
    code_en = diz_pills_categoria.get(t, "")
    if code_en:
      pills_tradotte.append(code_en)

  # Unione con sotto-opzioni (+)
  tutti_caratteristiche = pills_tradotte + sotto_opzioni_tradotte

  # Re-ordering: anticipa i termini direzionali/strutturali principali
  caratteristiche_anticipate = [
      c for c in tutti_caratteristiche if c in TERMINI_ANTICIPATI
  ]
  caratteristiche_restanti = [
      c for c in tutti_caratteristiche if c not in TERMINI_ANTICIPATI
  ]
  caratteristiche_ordinate = (
      caratteristiche_anticipate + caratteristiche_restanti
  )

  # 3. Formattazione Dimensioni
  stringa_dimensioni = ""
  parti_dim = []
  if dim_l.strip():
    parti_dim.append(f"L={dim_l.strip()}")
  if dim_p.strip():
    parti_dim.append(f"P={dim_p.strip()}")
  if dim_h.strip():
    parti_dim.append(f"H={dim_h.strip()}")
  if dim_s.strip():
    parti_dim.append(f"S={dim_s.strip()}MM")
  if dim_dia.strip():
    parti_dim.append(f"Ø{dim_dia.strip()}MM")

  if parti_dim:
    stringa_dimensioni = " ".join(parti_dim)

  # 4. Traduzione Materiale
  mat_tradotto = mat_options.get(materiale_scelto, "")

  # 5. Assemblaggio Finale
  elementi_titolo = [nome_base_en]

  if compatibilita_scelta:
    elementi_titolo.append(compatibilita_scelta)

  if caratteristiche_ordinate:
    elementi_titolo.extend(caratteristiche_ordinate)

  if input_manuali_extra:
    elementi_titolo.extend(input_manuali_extra)

  if stringa_dimensioni:
    elementi_titolo.append(stringa_dimensioni)

  if mat_tradotto:
    elementi_titolo.append(mat_tradotto)

  if normativa_scelta:
    elementi_titolo.append(normativa_scelta)

  if check_1090:
    elementi_titolo.append("EN 1090")

  if check_assembled:
    elementi_titolo.append("ASSEMBLED")

  if extra_text.strip():
    elementi_titolo.append(extra_text.strip().upper())

  # Pulizia e formattazione finale
  titolo_generato_grezzo = " ".join(elementi_titolo)
  titolo_generato = " ".join(titolo_generato_grezzo.split()).upper()

  # Output modificabile dall'utente
  titolo_finale = st.text_input(
      "Titolo generato (modificabile):",
      value=titolo_generato,
      key="stringa_editabile",
  )

  # Card di anteprima elegante
  with st.container(border=True):
    st.markdown("#### 📋 Anteprima Titolo Finale:")
    st.code(titolo_finale, language="text")

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
      if st.button("📋 Copia negli Appunti", use_container_width=True):
        st.toast("Titolo pronto per la copia!", icon="✅")
