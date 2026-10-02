import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configurazione della pagina admin
st.set_page_config(page_title="Pannello Admin - REG 2.0", page_icon="🛠️", layout="wide")

st.title("🛠️ Pannello Amministrazione - Gestione Segnalazioni")
st.markdown("---")

# Gestione dello stato di autenticazione admin
if "admin_autenticato" not in st.session_state:
    st.session_state.admin_autenticato = False

# Se non autenticato, mostriamo il box di login centrato
if not st.session_state.admin_autenticato:
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

# --- AREA ADMIN AUTENTICATA ---
col_info, col_logout = st.columns([4, 1])
with col_info:
    st.success("🔓 Accesso amministrativo autorizzato.")
with col_logout:
    if st.button("🔒 Logout Admin", use_container_width=True):
        st.session_state.admin_autenticato = False
        st.rerun()

st.markdown("---")

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
