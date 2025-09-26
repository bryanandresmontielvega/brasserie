#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 13:11:27 2025

@author: bryanandresmontielvega
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fooi verdelen (formulier)", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://dynamic-media-cdn.tripadvisor.com/media/photo-o/06/f9/7a/2b/brasserie-keyzer.jpg?w=900&h=500&s=1');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Styling: alles in witte boxen ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f2f5f8;
    }
    .white-box {
        background: #ffffff;
        padding: 15px 18px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        color: #000000;
        font-weight: 600;
    }
    .form-row {
        background: #ffffff;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .form-row .name {
        color: #000000;
        font-weight: 700;
        font-size: 16px;
    }
    .result-box {
        background: #ffffff;
        padding: 12px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .result-box .naam {
        color: #000000;
        font-weight: 700;
    }
    .result-box .bedrag {
        color: #000000;
        font-weight: 700;
        float: right;
    }
    .stNumberInput > label {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Title in box ---
st.markdown("<div class='white-box' style='font-size:22px'>💰 Fooi verdeling Keyzer</div>", unsafe_allow_html=True)

# --- Werknemers ---
werknemers = {
    "Sander": 0,
    "River Vis": 0,
    "Chantal Blaauw": 0,
    "Ferry Schoppen": 0,
    "Elsa Goetmaker": 0, 
    "Majd Salloum":0,
    "Gabriel":0,
    
    "Bryan Montiel Vega":0,
    "Anabelle de la pierre":0,
    "Floor":0,
    "Demi":0,
    "Thalisa":0,
    "Emilie":0,
    "Mervi":0,
    "Viktor":0,
    "Boyd":0,
    "Josef":0,
    "Francesco":0,
    "Marcello":0,
    
}


# --- Formulier ---
with st.form("fooiform"):
    st.markdown("<div class='white-box'>Vul per persoon de gewerkte uren in (per week)</div>", unsafe_allow_html=True)

    for naam in werknemers.keys():
        col_left, col_right = st.columns([3, 1])
        with col_left:
            st.markdown(f"<div class='form-row'><div class='name'>{naam}</div></div>", unsafe_allow_html=True)
        with col_right:
            st.number_input("", min_value=0.0, step=0.25, value=0.0, key=f"hours_{naam}")

    st.markdown("<div class='white-box'>Totale fooi (€)</div>", unsafe_allow_html=True)
    totale_fooi = st.number_input("", min_value=0.0, step=0.5, value=0.0, key="totale_fooi")

    submitted = st.form_submit_button("Bereken fooi")

# --- Resultaten ---
if submitted:
    uren_dict = {naam: float(st.session_state.get(f"hours_{naam}", 0.0)) for naam in werknemers.keys()}
    totaal_uren = sum(uren_dict.values())

    if totaal_uren <= 0:
        st.markdown("<div class='white-box'>⚠️ Vul minimaal één uur in (totaal uren moet > 0 zijn).</div>", unsafe_allow_html=True)
    elif totale_fooi <= 0:
        st.markdown("<div class='white-box'>⚠️ Vul het totale fooi in (moet meer dan 0 zijn).</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='white-box' style='font-size:18px'>Verdeling fooi</div>", unsafe_allow_html=True)
        resultaten = []
        for naam, uren in uren_dict.items():
            aandeel = (uren / totaal_uren) * totale_fooi if uren > 0 else 0.0
            resultaten.append({"Naam": naam, "Uren": uren, "Fooi": round(aandeel, 2)})
            st.markdown(
                f"<div class='result-box'><span class='naam'>{naam}</span>"
                f"<span class='bedrag'>€ {aandeel:,.2f}</span>"
                f"<div style='clear:both'></div>"
                f"<div style='color:#6c757d; font-size:12px'>{uren} uur</div></div>",
                unsafe_allow_html=True,
            )
        # Dataframe + download
        df = pd.DataFrame(resultaten)
        st.markdown("<div class='white-box'>Samenvatting</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv_bytes, "fooiverdeling.csv", "text/csv")

