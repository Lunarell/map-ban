
# Streamlit-basierte eSports Analyse Web-App (mit CSV-Speicherung)

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import ast

st.set_page_config(page_title="eSports Analyse Tool", layout="wide")

# --- Seitenwahl ---
seite = st.sidebar.radio("Seite wählen", ["📥 Match-Erfassung", "📊 Auswertung"])

# --- CSV Datei Pfad ---
data_path = "match_data.csv"

# --- Listen ---
maps = ["Bank", "Border", "Chalet", "Clubhouse", "Consulate", "Kafe", "Nighthaven", "Oregon", "Skyscraper"]
attack_ops = ["Ace", "Amaru", "Ash", "Blackbeard", "Blitz", "Buck", "Capitao", "Dokkaebi", "Finka", "Flores", "Glaze", "Gridlock", "Hibana", "Iana", "IQ", "Jackal", "Kali", "Lion", "Maverick", "Montagne", "Nokk", "Nomad", "Osa", "Sens", "Sledge", "Thatcher", "Thermite", "Twitch", "Ying", "Zero", "Zofia", "Grim", "Brave", "Fuze", "Ram", "Demos", "Rauora"]
defense_ops = ["Alibi", "Aruni", "Azami", "Bandit", "Castle", "Caveira", "Clash", "Doc", "Echo", "Ela", "Frost", "Goyo", "Jäger", "Kaid", "Kapkan", "Lesion", "Melusi", "Mira", "Mozzie", "Mute", "Orxy", "Pulse", "Rook", "Smoke", "Tachanka", "Thorne", "Thunderbird", "Valkyrie", "Vigil", "Wamai", "Warden", "solis", "Maestro", "Fenrir", "Tubarao", "Skopos"]

# (Kürzung des Codes für bessere Übersicht – vollen Code bei Bedarf einfügen)
