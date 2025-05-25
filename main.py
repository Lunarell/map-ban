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

if seite == "📥 Match-Erfassung":
    st.title("📥 Match-Erfassung")
    datum = st.date_input("Datum")
    liga = st.text_input("Liga")
    phase = st.selectbox("Phase", ["Playday", "Playoffs", "Runden"])
    team1 = st.text_input("Team 1")
    team2 = st.text_input("Team 2")
    match_format = st.selectbox("Match Format", ["Bo1", "Bo3", "Bo5"])

    # Matchlink optional
    faceit_link = st.text_input("Matchlink (optional)")

    # --- Map-Bans & Picks ---
    st.subheader("🗺️ Map-Bans & Picks")
    ban_pick_data = []
    if match_format == "Bo1":
        for i in range(8):
            col1, col2 = st.columns(2)
            with col1:
                who = st.selectbox(f"Ban {i+1} von", [team1, team2], key=f"bo1banwho{i}")
            with col2:
                mapname = st.selectbox(f"Map (Ban {i+1})", maps, key=f"bo1banmap{i}")
            ban_pick_data.append((who, "Ban", mapname))
        pick_team = st.selectbox("Wer pickt die Map?", [team1, team2])
        picked_map = st.selectbox("Welche Map wird gespielt?", maps)
        ban_pick_data.append((pick_team, "Pick", picked_map))
        # Startseiten optional
        atk_start = st.selectbox("Start als Attacker (optional)", ["", team1, team2])
        def_start = st.selectbox("Start als Defender (optional)", ["", team1, team2])
    elif match_format == "Bo3":
        for i in range(4):
            who = st.selectbox(f"Ban {i+1} von", [team1, team2], key=f"bo3banwho{i}")
            mapname = st.selectbox(f"Map (Ban {i+1})", maps, key=f"bo3banmap{i}")
            ban_pick_data.append((who, "Ban", mapname))
        for i in range(2):
            who = st.selectbox(f"Pick {i+1} von", [team1, team2], key=f"bo3pickwho{i}")
            mapname = st.selectbox(f"Map (Pick {i+1})", maps, key=f"bo3pickmap{i}")
            ban_pick_data.append((who, "Pick", mapname))
        for i in range(2):
            who = st.selectbox(f"Ban {i+5} von", [team1, team2], key=f"bo3banwho2_{i}")
            mapname = st.selectbox(f"Map (Ban {i+5})", maps, key=f"bo3banmap2_{i}")
            ban_pick_data.append((who, "Ban", mapname))
        who = st.selectbox("Letzter Pick von?", [team1, team2])
        mapname = st.selectbox("Letzter Pick Map", maps)
        ban_pick_data.append((who, "Pick", mapname))
    elif match_format == "Bo5":
        for i in range(2):
            who = st.selectbox(f"Ban {i+1} von", [team1, team2], key=f"bo5banwho{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5banmap{i}")
            ban_pick_data.append((who, "Ban", mapname))
        for i in range(2):
            who = st.selectbox(f"Pick {i+1} von", [team1, team2], key=f"bo5pickwho{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5pickmap{i}")
            ban_pick_data.append((who, "Pick", mapname))
        for i in range(2):
            who = st.selectbox(f"Ban {i+3} von", [team1, team2], key=f"bo5banwho2_{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5banmap2_{i}")
            ban_pick_data.append((who, "Ban", mapname))
        for i in range(3):
            who = st.selectbox(f"Pick {i+3} von", [team1, team2], key=f"bo5pickwho2_{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5pickmap2_{i}")
            ban_pick_data.append((who, "Pick", mapname))

    # --- Operatorenbans je Map ---
    st.subheader("🚫 Operator-Bans pro Map")
    played_maps = [entry[2] for entry in ban_pick_data if entry[1] == "Pick"]
    operator_data = []
    for m in played_maps:
        st.markdown(f"#### Map: {m}")
        for team in [team1, team2]:
            atk_bans = st.multiselect(f"{team} - Attacker Bans auf {m}", attack_ops, key=f"{team}_{m}_att")
            def_bans = st.multiselect(f"{team} - Defender Bans auf {m}", defense_ops, key=f"{team}_{m}_def")
            operator_data.append((m, team, ",".join(atk_bans), ",".join(def_bans)))

    if st.button("📁 Speichern"):
        entry = {
            "Datum": datum,
            "Liga": liga,
            "Phase": phase,
            "Team1": team1,
            "Team2": team2,
            "Matchformat": match_format,
            "Matchlink": faceit_link,
            "BanPick": ban_pick_data,
            "OperatorBans": operator_data
        }
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            df = pd.DataFrame(columns=["Datum", "Liga", "Phase", "Team1", "Team2", "Matchformat", "Matchlink", "BanPick", "OperatorBans"])
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(data_path, index=False)
        st.success("Matchdaten gespeichert.")

elif seite == "📊 Auswertung":
    st.title("📊 Match-Auswertung")
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df["BanPick"] = df["BanPick"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
        df["OperatorBans"] = df["OperatorBans"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

        team_filter = st.selectbox("Team auswählen (optional)", ["Alle Teams"] + sorted(set(df["Team1"]).union(set(df["Team2"]))))

        if team_filter != "Alle Teams":
            df = df[(df["Team1"] == team_filter) | (df["Team2"] == team_filter)]

        # Operatorban-Analyse
        st.subheader("🔍 Operator-Ban Analyse")
        ban_counts = {}
        for row in df["OperatorBans"]:
            for m, team, atk, dfn in row:
                for op in atk.split(","):
                    if op:
                        ban_counts[op] = ban_counts.get(op, 0) + 1
                for op in dfn.split(","):
                    if op:
                        ban_counts[op] = ban_counts.get(op, 0) + 1
        if ban_counts:
            sorted_bans = sorted(ban_counts.items(), key=lambda x: x[1], reverse=True)
            st.write(pd.DataFrame(sorted_bans, columns=["Operator", "Bans"]))

        st.subheader("📄 Gesamtdaten")
        st.dataframe(df)
    else:
        st.warning("Noch keine Matchdaten vorhanden.")
