import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="PGA Bachelor Party Leaderboard", layout="wide")

# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="refresh")

st.title("🏌️ PGA Championship + Bachelor Party Leaderboard")

tab1, tab2 = st.tabs(["📊 PGA Leaderboard", "💸 Bachelor Party Standings"])

# -------- TAB 1: PGA LEADERBOARD --------
with tab1:
    st.subheader("Live PGA Top 10")

    # Pull from ESPN API
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard"
        r = requests.get(url)
        data = r.json()

        leaderboard = []
        for player in data["leaders"]:
            name = player["athlete"]["displayName"]
            score = player["totalScore"]
            pos = player["currentPosition"]
            thru = player.get("thru", "-")
            leaderboard.append((pos, name, score, thru))

        df = pd.DataFrame(leaderboard, columns=["Position", "Player", "Score", "Thru"])
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error("Error loading PGA data. Try refreshing.")
        st.exception(e)

# -------- TAB 2: BACHELOR PARTY --------
with tab2:
    st.subheader("Bachelor Party Drafted Teams")

    # Sample static table (replace this with dynamic payout logic if needed)
    teams = {
        "James Trimble": ["Scottie Scheffler", "Jordan Spieth", "Shane Lowry"],
        "Jack Rushin": ["Rory McIlroy", "Viktor Hovland", "Sepp Straka"],
        "Jimmy Mangan": ["Bryson DeChambeau", "Brooks Koepka", "Russell Henley"],
        "John Funkhouser": ["Jon Rahm", "Hideki Matsuyama", "Corey Conners"],
        "Joseph Bauer": ["Xander Schauffele", "Patrick Cantlay", "Jason Day"],
        "Rich Wehman": ["Justin Thomas", "Tommy Fleetwood", "Wyndham Clark"],
        "Jack Byrne": ["Collin Morikawa", "Tyrrell Hatton", "Sungjae Im"],
        "Matthew Bauer": ["Ludvig Åberg", "Joaquin Niemann", "Patrick Reed"],
    }

    df2 = pd.DataFrame.from_dict(teams, orient="index").transpose()
    st.dataframe(df2, use_container_width=True)

