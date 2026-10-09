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
# Import del nostro modulo dati centralizzato
from database import *
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
# 1. CONFIGURAZIONE PAGINA E CREDENZIALI DI ACCREDITAMENTO
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
# 2. INTERFACCIA UTENTE (Layout & Logica)
# =========================================================

if "mat_en" not in st.session_state: 
    st.session_state.mat_en = ""

# --- HEADER RISTRUTTURATO (Suggerimenti a SX, Titolo al CENTRO, Reset a DX) ---
col_s, col_t, col_r = st.columns([1.5, 2.5, 1], vertical_alignment="bottom")

with col_s:
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
                        st.error(f"⚠️ Errore di registrazione: {e}")

with col_t: 
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
    st.subheader("🛠️️ 2. Configurazione Base")
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
    # =========================================================
# --- SEZIONE 3: EXTRA E NOTE (LAYOUT AFFIANCATO) ---
# =========================================================
    st.subheader("✨ 3. Extra e Note")
    st.session_state.conflitto_attivo = False 

    if scelta_part_it:
        dizionario_corrente_pills = MAPPA_PILLS_CATEGORIA.get(macro_it, {})
        extra_options = list(dizionario_corrente_pills.keys())
        
        if extra_options:
            # Dividiamo l'area in due colonne: a sinistra la ricerca pillole, a destra le opzioni (+) se attive
            col_ricerca_pills, col_config_plus = st.columns([1.8, 1.2], gap="medium")
            
            with col_ricerca_pills:
                st.markdown(f"**Caratteristiche ({macro_it}):**")
                tag_selezionati = st.multiselect(
                    "Caratteristiche specifiche:",
                    options=sorted(extra_options),
                    key="extra_tags",
                    label_visibility="collapsed",
                    placeholder=f"Cerca caratteristiche per {macro_it}..."
                )
            
            # Verifichiamo se ci sono pillole con (+) attive nello stato
            tags_attuali = st.session_state.get("extra_tags", [])
            pills_con_plus = [t for t in tags_attuali if t.endswith("(+)")]
            
            with col_config_plus:
                if pills_con_plus:
                    with st.container(border=True):
                        st.markdown("⚙ **Dettagli Opzionali (+):**")
                        for pill_p in pills_con_plus:
                            sub_dict = SUB_OPTIONS_CONFIG.get(pill_p, {})
                            if sub_dict:
                                opzioni_chiavi = list(sub_dict.keys())
                                st.markdown(f"*{pill_p}*")
                                # Pulsanti a pillola orizzontali puliti, senza tendine
                                st.pills(
                                    f"Variante {pill_p}",
                                    options=opzioni_chiavi,
                                    key=f"sub_{pill_p}",
                                    label_visibility="collapsed"
                                )
                            elif pill_p in EXTRA_CON_INPUT_MANUALE:
                                st.text_input(
                                    f"Valore per *{pill_p}*:",
                                    key=f"manual_{pill_p}"
                                )
                else:
                    # Suggerimento visivo pulito quando non ci sono (+) attivi
                    st.markdown("<p style='color: gray; font-size: 0.85rem; padding-top: 25px;'>💡 Seleziona un'opzione con (+) per configurare i dettagli a lato.</p>", unsafe_allow_html=True)
            
            # Logica di controllo conflitti
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
    if not testo: 
        return ""
    
    glossario_locale = {
        "mensola": "BRACKET", "mensole": "BRACKETS", "gondola": "GONDOLA",
        "spalla": "FRAME", "innesto": "COUPLING", "montante": "UPRIGHT", 
        "losanga": "LOSANGA", "rivestimento": "BACK PANEL", "cancelletto": "GATE", 
        "vasca": "TANK", "con ruote": "WITH WHEELS", "senza ruote": "WITHOUT WHEELS", 
        "rinforzato": "REINFORCED", "verniciato": "PAINTED", "zincato": "GALVANIZED", 
        "superiore": "UPPER", "trasparente": "TRANSPARENT"
    }
    
    testo_elaborato = str(testo).lower().strip()
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
    if 'scelta_part_it' in locals() and scelta_part_it:
        part_db = DATABASE.get(macro_it, {}).get("Particolari", {}).get(scelta_part_it, ["", "PILLS_VUOTO", ""])
        part_en = str(part_db[0]).upper()
        
        # --- FIX: Usa il dizionario pills specifico della categoria attiva ---
        dict_extra_db = MAPPA_PILLS_CATEGORIA.get(macro_it, PILLS_METAL_COMP)
        
        lista_prima = []
        lista_dopo = []
        tags_selezionati = st.session_state.get('extra_tags', [])
        
        if tags_selezionati:
            for tag_master in tags_selezionati:
                if tag_master in SUB_OPTIONS_CONFIG:
                    chiave_sub = st.session_state.get(f"sub_{tag_master}", "")
                    traduzione = str(SUB_OPTIONS_CONFIG[tag_master].get(chiave_sub, chiave_sub)).upper()
                elif tag_master in EXTRA_CON_INPUT_MANUALE:
                    traduzione = str(st.session_state.get(f"manual_{tag_master}", "")).upper()
                else:
                    traduzione = str(dict_extra_db.get(tag_master, tag_master)).upper()
                
                if traduzione in TERMINI_ANTICIPATI:
                    lista_prima.append(traduzione)
                else:
                    lista_dopo.append(traduzione)

        dim_list = []
        L = str(st.session_state.get("dim_l", "") or "").strip()
        P = str(st.session_state.get("dim_p", "") or "").strip()
        H = str(st.session_state.get("dim_h", "") or "").strip()
        D = str(st.session_state.get("dim_dia", "") or "").strip()

        if L: dim_list.append(f"L{L.upper()}")
        if P: dim_list.append(f"P{P.upper()}")
        if H: dim_list.append(f"H{H.upper()}")
        if D:
            prefix_d = "M" if (macro_it == "FASTENER" and not D.upper().startswith("M")) else "Ø"
            dim_list.append(f"{prefix_d}{D.upper()}")
        
        dim_str = " ".join(dim_list)
        norma_sel = st.session_state.get("norm_select", "")
        norma_str = MAPPA_NORMATIVE_FASTENER.get(scelta_part_it, {}).get(norma_sel, "")

        note_it = str(st.session_state.get("extra_text", "") or "").strip()
        note_en = traduci_note(note_it)

        if "ASSEMBLY" in macro_it.upper():
            prefix_base = "ASSEMBLED" if st.session_state.get("check_assembled") else ""
        else:
            prefix_base = str(st.session_state.get("mat_en", "") or "").upper()

        elementi_prefisso = [prefix_base] + lista_prima
        prefisso_lista = [str(p).strip().upper() for p in elementi_prefisso if p and str(p).strip()]
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
            
        raw_comp_tag = st.session_state.get("comp_tags")
        comp_tag = str(raw_comp_tag).strip().upper() if raw_comp_tag else ""
        
        if comp_tag and comp_tag != "NONE":
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
    """Aggiorna la stringa stabile quando l'utente modifica manualmente il testo."""
    if 'input_manuale' in st.session_state:
        st.session_state['stringa_stabile'] = st.session_state['input_manuale'].upper()

risultato_container = st.container()

if st.session_state.get('stringa_stabile'):
    with risultato_container:
        st.markdown("---")
        col_titolo, col_opt = st.columns([4, 1])
        
        with col_titolo:
            st.subheader("📋 Risultato Finale")
        
        # Toggle per la modifica manuale
        modifica_attiva = col_opt.toggle("✏️ Modifica", key="toggle_manual_edit")

        # Inizializzazione e sincronizzazione sicura dello stato manuale
        current_stable = st.session_state.get('stringa_stabile', '')
        if "input_manuale" not in st.session_state or st.session_state.get("last_synced_string") != current_stable:
            st.session_state["input_manuale"] = current_stable
            st.session_state["last_synced_string"] = current_stable

        if modifica_attiva:
            st.text_input(
                "Modifica manuale stringa:", 
                key="input_manuale",
                on_change=sincronizza_modifica,
                label_visibility="collapsed"
            )
        else:
            st.code(current_stable, language=None)

        # Monitoraggio lunghezza stringa
        lunghezza = len(current_stable)
        perc = min(lunghezza / 100, 1.0)
        
        if lunghezza > 100:
            st.error(f"⚠️ LIMITE CRITICO: {lunghezza}/100 caratteri (Supera lo standard consentito)")
        elif lunghezza >= 90:
            st.warning(f"🟡 ATTENZIONE: {lunghezza}/100 caratteri (Vicino al limite massimo)")
        else:
            st.markdown(f"<p style='color: #00cc66; font-size: 0.8rem; margin-bottom: -10px;'>✅ Lunghezza ottimale: {lunghezza}/100 caratteri</p>", unsafe_allow_html=True)
        
        st.progress(perc)
