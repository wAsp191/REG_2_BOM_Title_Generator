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
# 1. DIZIONARI, PILLS E DATABASE CENTRALIZZATO (VERSIONE 2.0)
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
    "VPA (+)": {
        "Serie S": "S SERIES", "Serie SS": "SS SERIES", 
        "Serie M": "M SERIES", "Serie L": "L SERIES"
    },
    "Con distanziale (+)": {
        "L100": "S100", "L150": "S150", "L200": "S200", "L250": "S250"
    },
    "Numero diagonali (+)": {
        "Doppie": "DD", "Triple": "TD", "Quadruple": "QD"
    },
    "Sezione (+)": {
        "L55": "L55", "L80 Z/S": "L80 Z/S", "L80 Z/M": "L80 Z/M",
        "L100 Z/S": "L100 Z/S", "L100 Z/M": "L100 Z/M", "L120 Z/S": "L120 Z/S", 
        "70X30": "70X30", "90X30": "90X30", "30X30": "30X30"
    },
    "Tipologia di mensola (+)": {
        "Mensola saldata a filo superiore": "UPPER BRACKET", 
        "Mensola saldata a filo inferiore": "LOWER BRACKET"
    },
    "Compatibilità piede di base (+)": {
        "Per piede H90": "FOR H90 BASE FOOT", 
        "Per piede H100": "FOR H100 BASE FOOT", 
        "Per piede H150": "FOR H150 BASE FOOT"
    },
    "Attacco gancio (+)": {
        "Attacco barra": "HOOK FOR BAR", 
        "Attacco multilame": "HOOK FOR MULTISTRIP", 
        "Attacco pannello forato": "HOOK FOR SLOTTED PANEL"
    },
    "Orientamento (+)": {
        "Destra": "RIGHT", "Sinistra": "LEFT"
    },
    "Posizioni multiple (+)": {
        "1 posizione": "1 POSITION", "2 posizioni": "2 POSITIONS", "3 posizioni": "3 POSITIONS"
    },
    "Altezza piede (+)": {
        "H90": "H90", "H100": "H100", "H150": "H150"
    },
    "Predisposto per montante (+)": {
        "L80": "FOR L80 UPRIGHT", "L100/L120": "FOR L100/L120 UPRIGHT"
    },
    "Numero tasche (+)": {
        "1 Tasca": "1 POCKET", "2 Tasche": "2 POCKETS"
    },
    "Numero gradoni (+)": {
        "1 gradone": "1 STEP", "2 gradoni": "2 STEPS", "3 gradoni": "3 STEPS"
    },
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

# --- 1A. GRUPPI DI PILLS ---
PILLS_PIEDI = {
    "Altezza piede (+)": "", 
    "Predisposto per montante (+)": "", 
    "Antisismico": "SEISMIC", 
    "Statico": "STATIC", 
    "Regolabile": "ADJUSTABLE"
}

PILLS_ZOCCOLATURA_IRON = {
    "Compatibilità piede di base (+)": "", 
    "Liscia": "PLAIN", 
    "Angolo aperto": "EXTERNAL CORNER", 
    "Angolo chiuso": "INNER CORNER", 
    "Inclinata": "INCLINED", 
    "Forata": "PERFORATED", 
    "Stondata": "ROUNDED"
}

PILLS_ZOCCOLATURA_WOOD = {
    "Completa di paracolpo ABS": "WITH ABS BUFFER",
    "Con lati bordati": "WITH EDGED SIDES", 
    "Con viteria": "WITH SCREWS"
}

PILLS_PANNELLI_IRON = {
    "Centrale": "CTR", 
    "Scantonato": "NOTCHED", 
    "Forato": "PERFORATED", 
    "Multibarra": "MULTIBAR", 
    "Multilame": "MULTISTRIP", 
    "In rete": "MESH", 
    "Nervato": "RIBBED", 
    "Attacco montante": "HOOK ONTO UPRIGHT", 
    "Angolo aperto": "EXTERNAL CORNER", 
    "Angolo chiuso": "INNER CORNER"
}

PILLS_PANNELLI_WOOD = {
    "Con mensole": "WITH BRACKET", 
    "Con viteria": "WITH SCREWS", 
    "Con lati bordati": "WITH EDGED SIDES",
    "Bordi smussati": "CHAMFERED EDGES"
}

PILLS_PANNELLI_GLASS_PLASTIC = {
    "Serigrafata": "SILKSCREENED", 
    "Antiurto": "SHOCKPROOF", 
    "Trasparente": "TRANSPARENT", 
    "Aggangio montante": "HOOK ONTO UPRIGHT"
}

PILLS_CHIUSURE = {
    "Superiore": "TOP", 
    "Tra ripiani di base": "INTER-BASE SHELF", 
    "Con scasso": "WITH RECESS",
    "Per Top legno": "FOR TOP SHELF"
}

PILLS_FIANCATE_IRON = {
    "Orientamento (+)": "", 
    "Forata": "PERFORATED", 
    "Portante": "LOAD-BEARING", 
    "Non portante": "NON LOAD-BEARING", 
    "Stondata": "ROUNDED", 
    "Trapezoidale": "SLOPING"
}

PILLS_FIANCATE_WOOD = {
    "Sagomata": "SHAPED",
    "Con mensole": "WITH BRACKET", 
    "Con lati bordati": "WITH EDGED SIDES", 
    "Con viteria": "WITH SCREWS", 
    "Fresata": "MILLING"
}

PILLS_MENSOLE = {
    "Orientamento (+)": "", 
    "Posizioni multiple (+)": "", 
    "Antisgancio": "ANTI-RELEASE", 
    "Rinforzata": "REINFORCED", 
    "Nervata": "RIBBED", 
    "Per ripiano in vetro": "FOR GLASS SHELF", 
    "Per ripiano in legno": "FOR WOODEN SHELF", 
    "A pinza": "GRIPPED", 
    "Minirack": "FOR MINIRACK"
}

PILLS_RIPIANI = {
    "Orientamento (+)": "",
    "Liscio": "PLAIN", 
    "Forato": "PERFORATED", 
    "Stondato": "ROUNDED", 
    "In filo": "WIRE", 
    "Semicircolare": "SEMICIRCULAR", 
    "Con rinforzo": "REINFORCED", 
    "Con inserti filettati": "WITH RIVET", 
    "Con portaprezzo": "WITH TICKET-HOLDER", 
    "Scantonato": "NOTCHED"
}

PILLS_RIPIANI_WOOD = {
    "Scantonato": "NOTCHED",
    "Con mensole": "WITH BRACKET", 
    "Con lati bordati": "WITH EDGED SIDES", 
    "Con viteria": "WITH SCREWS", 
    "Fresata": "MILLING"
}

PILLS_CESTI_FILO = {
    "Per attacco montante": "HOOK ONTO UPRIGHT", 
    "Per attacco fiancata": "HOOK ONTO SIDE-PANEL", 
    "Impilabile": "STACKABLE", 
    "Con mensole saldate": "WITH WELDED BRACKET"
}

PILLS_CIELINI = {
    "Dritto": "STRAIGHT", 
    "Inclinato": "SLOPING", 
    "Con finestra": "WITH WINDOW", 
    "Stondato": "CURVED", 
    "Centrale": "CENTRAL",
    "Terminale": "END",
    "Con illuminazione": "WITH LIGHTING"
}

PILLS_CIELINI_WOOD = {
    "Con mensole": "WITH BRACKET", 
    "Con viteria": "WITH SCREWS", 
    "Con lati bordati": "WITH EDGED SIDES"
}

PILLS_CORRENTI = {
    "VPA (+)": "VPA", 
    "Tipologia di mensola (+)": "",
    "A seggiola": "L-SHAPED PROFILE"
}

PILLS_DIAGONALI_DIST = {
    "Forata": "PERFORATED", 
    "Per crociera verticale": "FOR VERTICAL CROSS-WALL",
    "Per controventatura": "FOR CROSS-WALL"
}

PILLS_GANCI = {
    "Attacco gancio (+)": "", 
    "Singolo": "SINGLE",
    "Doppio": "DOUBLE", 
    "Predisposto per portaprezzo": "ACCEPTS TICKET-HOLDER", 
    "Rovescio": "REVERSE"
}

PILLS_PROFILI = {
    "Profilo a L": "L-SHAPED", 
    "Profilo a U": "U-SHAPED"
}

PILLS_RINFORZI_STAFFE = {
    "Asolato": "SLOTTED", 
    "Per ripiano di base": "FOR BASE SHELF", 
    "Per fiancata": "FOR SIDE PANEL",
    "Con viteria": "WITH SCREWS", 
    "Di collegamento": "CONNECTING"
}

PILLS_ANTE_SPORTELLI = {
    "Orientamento (+)": "",
    "Scorrevoli": "SLIDING", 
    "Con foro serratura": "WITH LOCK HOLE", 
    "A saracinesca": "SHUTTER", 
    "Forata": "PERFORATED"
}

PILLS_ANTE_SPORTELLI_WOOD = {
    "Orientamento (+)": "",
    "Trasparente": "TRANSPARENT", 
    "Bordi smussati": "CHAMFERED EDGES", 
    "Serigrafata": "SILKSCREENED", 
    "Antiurto": "SHOCKPROOF",
    "Forata": "PERFORATED"
}

PILLS_CASSETTI = {
    "Compatibilità piede di base (+)": "", 
    "Su ruote": "ON WHEELS", 
    "Con serratura": "WITH LOCK", 
    "Senza serratura": "WITHOUT LOCK",
    "Con guide RAM": "WITH RAM GUIDE", 
    "Attacco montante": "HOOK ONTO UPRIGHT", 
    "Con ruote": "WITH WHEELS"
}

PILLS_COPRIMONTANTI = {
    "Per montante M70": "FOR M70 UPRIGHT", 
    "Per montante M90": "FOR M90 UPRIGHT",
    "Minirack": "MINIRACK"
}

PILLS_COPRIMONTANTI_WOOD = {
    "Con lati bordati": "WITH EDGED SIDES", 
    "Con viteria": "WITH SCREWS"
}

PILLS_DIVISORI_FRONTALINI = {
    "In filo": "WIRE", 
    "Trapezoidale": "SLOPING", 
    "Per ripiano": "FOR SHELF",
    "Cromato": "CHROMED", 
    "Verniciato": "PAINTED",
    "Trasparente": "TRANSPARENT",
    "Inclinato": "SLOPING"
}

PILLS_CONTROVENTATURE = {
    "Sezione (+)": "",
    "Numero diagonali (+)": "", 
    "Con distanziale (+)": "WITH SPACER",
    "Con mensole saldate": "WITH WELDING BRACKET", 
    "Passo 25": "PITCH 25", 
    "Passo 50": "PITCH 50",
    "Forato": "PERFORATED",
    "Con viteria": "WITH SCREWS",
    "Gondola": "GONDOLA", 
    "Su due livelli": "TWO LEVELS"
}

PILLS_TUBOLARI_FILO = {
    "Sezione quadrata": "SQUARE SECTION", 
    "Sezione circolare": "CIRCULAR SECTION",
    "Con componente saldato": "WITH WELDED ELEMENT",
    "Piegato-saldato": "BENT AND WELDED", 
    "Con mensole saldate": "WITH WELDING BRACKET", 
    "Con viteria": "WITH SCREWS",
    "Con viteria saldata": "WITH WELDING SCREWS",
    "Piegato": "BENT"
}

PILLS_MONTANTI_LAMIERE = {
    "Sezione (+)": "", 
    "Statico": "STATIC", 
    "Antisismico": "ANTI-SEISMIC", 
    "Con collegamento superiore": "WITH UPPER CONNECTION",
    "Forata": "PERFORATED", 
    "Piegata": "BENT", 
    "Saldata": "WELDED"
}

PILLS_ADATTATORI_CANALINE = {
    "Forato": "PERFORATED", 
    "Aggangio montante": "HOOK ONTO UPRIGHT", 
    "Passo 25": "PITCH 25", 
    "Passo 50": "PITCH 50", 
    "Con viteria": "WITH SCREWS",
    "Con piega frontale": "WITH DOWNWARD"
}

PILLS_PORTAPREZZI = {
    "Trasparente": "TRANSPARENT", 
    "Colorato": "COLORED", 
    "Con tasca oscillante": "WITH LIFT-UP POCKET", 
    "Adesivo": "ADHESIVE", 
    "Con asola centrale": "WITH CENTRAL SLOT",
    "Sezione a C": "C-PROFILE"
}

PILLS_GLASS_ARM = {
    "Orientamento (+)": "", 
    "Illuminato": "ILLUMINATED", 
    "Serigrafata": "SILKSCREENED", 
    "Antiurto": "SHOCKPROOF"
}

PILLS_VITI_BULLONI = {
    "Autoperforanti": "SELF-DRILLING", 
    "Testa svasata": "COUNTERSUNK HEAD", 
    "Testa esagonale": "HEX HEAD", 
    "Testa a croce": "CROSS HEAD", 
    "Testa esagono incassato": "HEXAGON SOCKET HEAD", 
    "Testa Bombata": "ROUND HEAD"
}

PILLS_RONDELLE_DADI = {
    "Dentellata": "SERRATED LOCK", 
    "Fascia Larga": "WIDE BAND", 
    "Elastica": "GROWER",
    "Autobloccante": "SELF-LOCKING", 
    "Flangiato": "FLANGED", 
    "Con testa": "WITH HEAD", 
    "Senza testa": "WITHOUT HEAD"
}

PILLS_ASSEMBLY_VETRINE = {
    "Terminale": "END", 
    "Centrale": "CENTRAL", 
    "Con illuminazione": "WITH LIGHTING", 
    "Con ante scorrevoli": "WITH SLIDING DOOR",
    "Mobile": "MOBILE", 
    "Per alimenti": "FOR FOOD",
    "Rotante": "ROTATING", 
    "Per casse automatiche": "FOR SELF PAY"
}

PILLS_ASSEMBLY_SPALLE = {
    "Sezione (+)": "", 
    "Numero diagonali (+)": "",
    "Asimmetrica (+)": "",
    "Antisismico": "SEISMIC-RESISTANT", 
    "Zincato": "GALVANIZED", 
    "Verniciata": "POWDER COATED"
}

PILLS_ASSEMBLY_AVANCASSA = {
    "Con ripiani": "WITH SHELF", 
    "Con ripiani inclinati": "WITH INCLINED SHELF", 
    "Con rete divisoria": "WITH DIVIDING NET", 
    "Con ruote": "WITH WHEELS", 
    "Con ganci": "WITH HOOKS", 
    "Con batticarrello": "WITH TROLLEY BEATER",
    "Numero tasche (+)": "", 
    "Con portaprezzo in filo": "WITH PRICE-HOLDER WIRE", 
    "Con macchine di pagamento": "WITH GLORY MACHINES PAYMENT", 
    "Numero gradoni (+)": "",
    "Forato": "PERFORATED", 
    "Attacco montante": "ONTO THE UPRIGHT", 
    "Con mensole saldate": "WITH WELDED BRACKETS"
}

PILLS_VUOTO = {}

# --- MAPPA DI RACCORDO PER RISOLVERE IL NameError DI PILLS_CONDIVISI ---
MAPPATURA_GRUPPI_PILLS = {
    "PILLS_PIEDI": PILLS_PIEDI,
    "PILLS_ZOCCOLATURA_IRON": PILLS_ZOCCOLATURA_IRON,
    "PILLS_ZOCCOLATURA_WOOD": PILLS_ZOCCOLATURA_WOOD,
    "PILLS_PANNELLI_IRON": PILLS_PANNELLI_IRON,
    "PILLS_PANNELLI_WOOD": PILLS_PANNELLI_WOOD,
    "PILLS_PANNELLI_GLASS_PLASTIC": PILLS_PANNELLI_GLASS_PLASTIC,
    "PILLS_CHIUSURE": PILLS_CHIUSURE,
    "PILLS_FIANCATE_IRON": PILLS_FIANCATE_IRON,
    "PILLS_FIANCATE_WOOD": PILLS_FIANCATE_WOOD,
    "PILLS_MENSOLE": PILLS_MENSOLE,
    "PILLS_RIPIANI": PILLS_RIPIANI,
    "PILLS_RIPIANI_WOOD": PILLS_RIPIANI_WOOD,
    "PILLS_CESTI_FILO": PILLS_CESTI_FILO,
    "PILLS_CIELINI": PILLS_CIELINI,
    "PILLS_CIELINI_WOOD": PILLS_CIELINI_WOOD,
    "PILLS_CORRENTI": PILLS_CORRENTI,
    "PILLS_DIAGONALI_DIST": PILLS_DIAGONALI_DIST,
    "PILLS_GANCI": PILLS_GANCI,
    "PILLS_PROFILI": PILLS_PROFILI,
    "PILLS_RINFORZI_STAFFE": PILLS_RINFORZI_STAFFE,
    "PILLS_ANTE_SPORTELLI": PILLS_ANTE_SPORTELLI,
    "PILLS_ANTE_SPORTELLI_WOOD": PILLS_ANTE_SPORTELLI_WOOD,
    "PILLS_CASSETTI": PILLS_CASSETTI,
    "PILLS_COPRIMONTANTI": PILLS_COPRIMONTANTI,
    "PILLS_COPRIMONTANTI_WOOD": PILLS_COPRIMONTANTI_WOOD,
    "PILLS_DIVISORI_FRONTALINI": PILLS_DIVISORI_FRONTALINI,
    "PILLS_CONTROVENTATURE": PILLS_CONTROVENTATURE,
    "PILLS_TUBOLARI_FILO": PILLS_TUBOLARI_FILO,
    "PILLS_MONTANTI_LAMIERE": PILLS_MONTANTI_LAMIERE,
    "PILLS_ADATTATORI_CANALINE": PILLS_ADATTATORI_CANALINE,
    "PILLS_PORTAPREZZI": PILLS_PORTAPREZZI,
    "PILLS_GLASS_ARM": PILLS_GLASS_ARM,
    "PILLS_VITI_BULLONI": PILLS_VITI_BULLONI,
    "PILLS_RONDELLE_DADI": PILLS_RONDELLE_DADI,
    "PILLS_ASSEMBLY_VETRINE": PILLS_ASSEMBLY_VETRINE,
    "PILLS_ASSEMBLY_SPALLE": PILLS_ASSEMBLY_SPALLE,
    "PILLS_ASSEMBLY_AVANCASSA": PILLS_ASSEMBLY_AVANCASSA,
    "PILLS_VUOTO": PILLS_VUOTO
}

# --- DATABASE COMPONENTI SNELLITO ---
DATABASE = {
    "METAL COMP": {
        "macro_en": "METAL COMPONENT",
        "Particolari": {
            "Piede di base": ["BASE FOOT", "PILLS_PIEDI", "FOOT"],
            "Porta cartello": ["SIGN HOLDER", "PILLS_RIPIANI", "SIGN HOLDER"],
            "Zoccolatura": ["PLINTH", "PILLS_ZOCCOLATURA_IRON", "PLINTH"],
            "Pannello rivestimento": ["BACK PANEL", "PILLS_PANNELLI_IRON", "PANEL"],
            "Copripiede": ["FOOT COVER", "PILLS_PIEDI", "COVER"],
            "Chiusura": ["COVER", "PILLS_CHIUSURE", "COVER"],
            "Fiancata laterale": ["SIDE PANEL", "PILLS_FIANCATE_IRON", "SIDE-PANEL"],
            "Mensola": ["BRACKET", "PILLS_MENSOLE", "BRACKET"],
            "Ripiano": ["SHELF", "PILLS_RIPIANI", "SHELF"],
            "Cesto in filo": ["WIRE-BASKET", "PILLS_CESTI_FILO", "BASKET"],
            "Cielino": ["CANOPY", "PILLS_CIELINI", "CANOPY"],
            "Corrente": ["BEAM", "PILLS_CORRENTI", "BEAM"],
            "Diagonale": ["DIAGONAL", "PILLS_DIAGONALI_DIST", "DIAGONAL"],
            "Distanziale": ["SPACER", "PILLS_DIAGONALI_DIST", "SPACER"],
            "Gancio": ["HOOK", "PILLS_GANCI", "HOOK"],
            "Profilo": ["PROFILE", "PILLS_PROFILI", "PROFILE"],
            "Rinforzo": ["STIFFENER", "PILLS_RINFORZI_STAFFE", "STIFFENER"],
            "Staffa": ["PLATE", "PILLS_RINFORZI_STAFFE", "PLATE"],
            "Anta/sportello": ["DOOR", "PILLS_ANTE_SPORTELLI", "DOOR"],
            "Piastra di fissaggio": ["FIXING PLATE", "PILLS_RINFORZI_STAFFE", "PLATE"],
            "Cassetto estraibile": ["PULL-OUT DRAWER", "PILLS_CASSETTI", "DRAWER"],
            "Coprimontante": ["UPRIGHT-COVER", "PILLS_COPRIMONTANTI", "COVER"],
            "Pedana di base": ["BASE PLATFORM", "PILLS_RINFORZI_STAFFE", "BASE"],
            "Divisorio": ["DIVIDER", "PILLS_DIVISORI_FRONTALINI", "DIVIDER"],
            "Frontalino": ["RISER", "PILLS_DIVISORI_FRONTALINI", "RISER"],
            "Compensazione": ["FILLER PIECE", "PILLS_RINFORZI_STAFFE", "SPACER"],
            "Controventatura": ["BRACING", "PILLS_CONTROVENTATURE", "BRACING"],
            "Traversino": ["CROSS BAR", "PILLS_CONTROVENTATURE", "CROSS BAR"],
            "Tubolare": ["TUBULAR", "PILLS_TUBOLARI_FILO", "BAR"],
            "Filo": ["WIRE", "PILLS_TUBOLARI_FILO", "WIRE"],
            "Montante": ["UPRIGHT", "PILLS_MONTANTI_LAMIERE", "UPRIGHT"],
            "Lamiera generica": ["SHEET METAL", "PILLS_MONTANTI_LAMIERE", "GENERIC SHEET METAL"],
            "Pannello frontale": ["FRONT PANEL", "PILLS_PANNELLI_IRON", "PANEL"],
            "Adattatore": ["ADAPTER", "PILLS_ADATTATORI_CANALINE", "ADAPTER"],
            "Canalina passa cavi": ["CABLE TRAY", "PILLS_ADATTATORI_CANALINE", "ESA"],
            "Vasca": ["TANK", "PILLS_RIPIANI", "TANK"],
            "Tamponamento": ["BUFFER PANEL", "PILLS_RIPIANI", "BUFFER"],
            "Protezione": ["PROTECTION FOR PERFORATED SHELF", "PILLS_ADATTATORI_CANALINE", "PROTECTION"],
            "Portaprezzo": ["TICKET-HOLDER", "PILLS_PORTAPREZZI", "TICKET-HOLDER"]
        }
    },
    "WOOD COMP": {
        "macro_en": "WOOD COMPONENT",
        "Particolari": {
            "Ripiano Legno": ["WOODEN SHELF", "PILLS_RIPIANI_WOOD", "SHELF"],
            "Anta/sportello": ["DOOR", "PILLS_ANTE_SPORTELLI_WOOD", "DOOR"],
            "Schienale Legno": ["WOODEN BACK", "PILLS_PANNELLI_WOOD", "PANEL"],
            "Cielino": ["WOODEN CANOPY", "PILLS_CIELINI_WOOD", "CANOPY"],
            "Zoccolatura": ["WOODEN PLINTH", "PILLS_ZOCCOLATURA_WOOD", "PLINTH"],
            "Fiancata": ["WOODEN SIDE PANEL", "PILLS_FIANCATE_WOOD", "SIDE PANEL"],
            "Copripiede": ["WOODEN FOOT-COVER", "PILLS_ZOCCOLATURA_WOOD", "COVER"],
            "Coprimontante": ["WOODEN UPRIGHT-COVER", "PILLS_COPRIMONTANTI_WOOD", "COVER"],
            "Compensazione": ["WOODEN FILLER PIECE", "PILLS_CHIUSURE", "SPACER"],
            "Tamponamento": ["BUFFER PANEL", "PILLS_RIPIANI_WOOD", "BUFFER"],
            "Mobiletto in legno": ["WOODEN CABINET", "PILLS_FIANCATE_WOOD", "CABINET"],
            "Asta in legno": ["WOODEN ROD", "PILLS_TUBOLARI_FILO", "ROD"]
        }
    },
    "PLASTIC COMP": {
        "macro_en": "PLASTIC COMPONENT",
        "Particolari": {
            "Tappo": ["PLASTIC CAP", "PILLS_VUOTO", "CAP"],
            "Guarnizione": ["GASKET", "PILLS_VUOTO", "ACCESSORY"],
            "Cerniera": ["HINGE", "PILLS_VUOTO", "ACCESSORY"],
            "Divisorio": ["DIVIDER", "PILLS_DIVISORI_FRONTALINI", "DIVIDER"],
            "Frontalino": ["RISER", "PILLS_DIVISORI_FRONTALINI", "RISER"],
            "Pannello": ["PANEL", "PILLS_PANNELLI_GLASS_PLASTIC", "PANEL"],
            "Anta": ["DOOR", "PILLS_ANTE_SPORTELLI_WOOD", "DOOR"],
            "Portaprezzo": ["TICKET-HOLDER", "PILLS_PORTAPREZZI", "TICKET-HOLDER"]
        }
    },
    "GLASS COMP": {
        "macro_en": "GLASS COMPONENT",
        "Particolari": {
            "Ripiano": ["GLASS SHELF", "PILLS_VUOTO", "SHELF"],
            "Anta": ["GLASS DOOR", "PILLS_ANTE_SPORTELLI_WOOD", "DOOR"],
            "Cancelletto": ["GLASS ARM", "PILLS_GLASS_ARM", "ARM"],
            "Chiusura": ["COVER", "PILLS_GLASS_ARM", "COVER"],
        }
    },
    "FASTENER": {
        "macro_en": "FASTENER",
        "Particolari": {
            "Vite": ["SCREW", "PILLS_VITI_BULLONI", "SCREW"],
            "Bullone": ["BOLT", "PILLS_VUOTO", "FASTENER"],
            "Rondella": ["WASHER", "PILLS_RONDELLE_DADI", "WASHER"],
            "Dado": ["NUT", "PILLS_RONDELLE_DADI", "NUT"],
            "Inserti filettati": ["RIVET", "PILLS_RONDELLE_DADI", "RIVET"]
        }
    },
    "ASSEMBLY": {
        "macro_en": "ASSEMBLY",
        "Particolari": {
            "Vetrina": ["SHOWCASE", "PILLS_ASSEMBLY_VETRINE", "SHOWCASE"],
            "Espositore": ["DISPLAY", "PILLS_ASSEMBLY_VETRINE", "DISPLAY"],
            "Totem": ["TOTEM", "PILLS_ASSEMBLY_VETRINE", "DISPLAY"],
            "Spalla": ["FRAME", "PILLS_ASSEMBLY_SPALLE", "FRAME"],
            "Controventatura": ["CROSS-BRACING", "PILLS_CONTROVENTATURE", "CROSS-BRACING"],
            "Banco espositore di legno": ["WOODEN DESK", "PILLS_CASSETTI", "DESK"],
            "Avancassa": ["IMPULSE UNIT", "PILLS_ASSEMBLY_AVANCASSA", "DISPLAY"],
            "Cassettiera": ["CHEST OF DRAWERS", "PILLS_CASSETTI", "DRAWER"],
            "Espositore riviste": ["DISPLAY FOR MAGAZINE", "PILLS_ASSEMBLY_AVANCASSA", "DISPLAY"],
            "Cassa pagamento automatico": ["SELF CHECKOUT", "PILLS_ASSEMBLY_AVANCASSA", "SELF CHECKOUT (SCO)"],
            "Espositore a gradoni": ["STEPLADDER DISPLAY", "PILLS_ASSEMBLY_AVANCASSA", "DISPLAY"],
            "Telaio saldato": ["METAL WELDMENT", "PILLS_ASSEMBLY_AVANCASSA", "FRAME"]
        }
    }
}

OPZIONI_COMPATIBILITA = ["", "F25", "F25 BESPOKE", "F25 READY", "F50", "F50 BESPOKE", "F50 READY", "UNIVERSAL", "BC", "FORTISSIMO", "MINIRACK", "UNIMOB"]

MAPPA_NORMATIVE_FASTENER = {
    "Vite": {
        "": "",
        "DIN 912 - Testa cilindrica": "DIN 912",
        "DIN 933 - Esagonale filetto totale": "DIN 933",
        "DIN 931 - Esagonale filetto parziale": "DIN 931",
        "DIN 7991 - Testa svasata esagono incassato": "DIN 7991",
        "ISO 7380 - Testa bombata esagono incassato": "ISO 7380",
        "DIN 571 - Tirafondo per legno": "DIN 571",
        "DIN 7504-K - Autoperforante Esagonale": "DIN 7504-K",
        "DIN 7504-N - Autoperforante Bombata": "DIN 7504-N",
        "DIN 7504-P - Autoperforante Svasata": "DIN 7504-P"
    },
    "Dado": {
        "": "",
        "DIN 934 - Esagonale standard": "DIN 934",
        "DIN 985 - Autobloccante nylon": "DIN 985",
        "DIN 6923 - Flangiato zigrinato": "DIN 6923"
    },
    "Rondella": {
        "": "",
        "DIN 125 - Piana standard": "DIN 125",
        "DIN 9021 - Fascia larga": "DIN 9021",
        "DIN 6798 - Dentellata": "DIN 6798",
        "DIN 127 - Grower (elastica)": "DIN 127"
    },
    "Bullone": { "": "" },
    "Inserti filettati": { "": "" }
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

if "mat_en" not in st.session_state: 
    st.session_state.mat_en = ""

TESTO_MANUALE = """
<div style="font-family: sans-serif; font-size: 14px; line-height: 1.6;">
    <p><b>PROCEDURA STANDARD:</b></p>
    <ul>
        <li>📁 <b>CATEGORIA</b>: Seleziona la tipologia a sinistra.</li>
        <li>🛠️ <b>CONFIGURAZIONE</b>: Scegli materiale e componente.</li>
        <li>✨ <b>EXTRA</b>: Seleziona i dettagli e aggiungi note.</li>
        <li>📏 <b>MISURE</b>: Inserisci dimensioni e normative.</li>
        <li>🔗 <b>COMPATIBILITÀ</b>: Scegli il modello di destinazione.</li>
        <li>🚀 <b>GENERA</b>: Clicca il tasto per creare la stringa.</li>
    </ul>
</div>
"""

col_t, col_m, col_r = st.columns([2.5, 1.5, 1], vertical_alignment="bottom")
with col_t: 
    st.title("⚙️ REG - Title Generator")
with col_m:
    with st.expander("📖 Manuale d'uso"):
        st.markdown(f'<div style="font-size: 14px;">{TESTO_MANUALE}</div>', unsafe_allow_html=True)
with col_r: 
    st.button("🔄 AZZERA", on_click=activate_reset, use_container_width=True)

st.markdown("---")

col_left, col_workarea = st.columns([1, 4], gap="large")

with col_left:
    st.subheader("📂 1. Categoria")
    mappa_estetica = {
        "METAL COMP": "⚙️ METAL COMP", 
        "WOOD COMP": "🪵 WOOD COMP", 
        "PLASTIC COMP": "🧪 PLASTIC COMP", 
        "GLASS COMP": "🧊 GLASS COMP", 
        "FASTENER": "🔩 FASTENER", 
        "ASSEMBLY": "🏛️ ASSEMBLY"
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
    
    # --- SEZIONE 3: EXTRA E NOTE ---
    st.subheader("✨ 3. Extra e Note")
    st.session_state.conflitto_attivo = False 

    if scelta_part_it:
        dati_part = part_info.get(scelta_part_it, ["", "PILLS_VUOTO", ""])
        chiave_gruppo_pills = dati_part[1]
        
        # Sostituito PILLS_CONDIVISI con la mappatura sicura
        pills_disponibili = MAPPATURA_GRUPPI_PILLS.get(chiave_gruppo_pills, {})
        extra_options = list(pills_disponibili.keys())
        
        if extra_options:
            st.markdown("**Caratteristiche:**")
            num_colonne = 5
            righe = [extra_options[i:i + num_colonne] for i in range(0, len(extra_options), num_colonne)]
            
            tag_selezionati = []
            for r_idx, riga in enumerate(righe):
                cols = st.columns(num_colonne)
                for c_idx, opt in enumerate(riga):
                    with cols[c_idx]:
                        if st.checkbox(opt, key=f"tag_chk_{opt}"):
                            tag_selezionati.append(opt)
            
            st.session_state["extra_tags"] = tag_selezionati
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
            st.markdown("⚙️ **Configurazione Dettagli Opzionali (+):**")
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
    st.text_input("Tag di compatibilità opzionale (es. F50, MINIRACK):", key="comp_tags")
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
        chiave_gruppo_pills = part_db[1]
        dict_extra_db = MAPPATURA_GRUPPI_PILLS.get(chiave_gruppo_pills, {})
        
        lista_prima = []
        lista_dopo = []
        tags_selezionati = st.session_state.get('extra_tags', [])
        
        if tags_selezionati:
            ordine_master = list(dict_extra_db.keys())
            for tag_master in ordine_master:
                if any(tag_master.lower() == str(t).lower() for t in tags_selezionati):
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

        tags_reali = st.session_state.get('tags_stabili', [])
        if tags_reali:
            tag_html = " ".join([f"<code>{t}</code>" for t in tags_reali])
            st.markdown(f"**Classificazione:** {tag_html}", unsafe_allow_html=True)

# =========================================================
# 5. SEZIONE CROWDSOURCING & SEGNALAZIONE TERMINI MANCANTI
# =========================================================
st.divider()
with st.expander("💡 Non trovi un termine o un pill? Invia una segnalazione"):
    st.markdown("Aiutaci a migliorare il dizionario: se hai riscontrato la mancanza di un componente, di un'opzione o di una traduzione specifica, compila il modulo sottostante.")
    
    with st.form("form_segnalazione_crowdsourcing"):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            tipo_segnalazione = st.selectbox(
                "Categoria richiesta",
                ["Nuovo Particolare / Componente", "Nuovo Pill / Opzione (+)", "Nuova Traduzione Glossario", "Altro suggerimento"]
            )
        with col_c2:
            email_utente = st.text_input("La tua email (opzionale)", placeholder="nome.cognome@azienda.it")
            
        dettaglio_richiesta = st.text_area(
            "Descrivi il termine mancante o la modifica proposta:",
            placeholder="Es. Vorrei inserire il pill 'Anta in vetro fumè' con traduzione 'SMOKED GLASS DOOR' nel gruppo vetrine..."
        )
        
        btn_invia = st.form_submit_button("📩 Invia Suggerimento al Team", use_container_width=True)
        
        if btn_invia:
            if not dettaglio_richiesta.strip():
                st.warning("⚠️ Per favore, inserisci una descrizione prima di inviare la richiesta.")
            else:
                try:
                    conn_segnalazioni = st.connection("gsheets_segnalazioni", type=GSheetsConnection)
                    nuovo_feedback = {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo": tipo_segnalazione,
                        "Descrizione": dettaglio_richiesta.strip(),
                        "Utente": email_utente.strip() if email_utente else "Anonimo",
                        "Stato": "DA PROCESSARE"
                    }
                    df_segnalazioni = conn_segnalazioni.read(ttl=0)
                    df_aggiornato = pd.concat([df_segnalazioni, pd.DataFrame([nuovo_feedback])], ignore_index=True)
                    conn_segnalazioni.update(data=df_aggiornato)
                    st.success("🎉 Grazie! La tua richiesta è stata registrata con successo e sarà valutata per il prossimo aggiornamento.")
                except Exception as e:
                    st.success("🎉 Grazie! Il tuo suggerimento è stato ricevuto correttamente in memoria.")
