import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="PGA Bachelor Party Leaderboard", layout="wide")
st_autorefresh(interval=60 * 1000, key="refresh")

st.title("🏌️ PGA Championship + Bachelor Party Leaderboard")

tab1, tab2 = st.tabs(["📊 PGA Leaderboard", "💸 Bachelor Party Standings"])

# ---------------- TAB 1: PGA LEADERBOARD ---------------- #
with tab1:
    st.subheader("Live PGA Top 10")
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard"
        r = requests.get(url)
        data = r.json()

        players = data["events"][0]["competitions"][0]["athletes"]
        leaderboard = []

        for player in players:
            name = player["athlete"]["displayName"]
            score = player["score"]
            position = player["status"]["position"]["displayName"]
            thru = player["status"].get("thru", "-")
            leaderboard.append((position, name, score, thru))

        df = pd.DataFrame(leaderboard, columns=["Position", "Player", "Score", "Thru"])
        df["Score"] = df["Score"].astype(int)
        df = df.sort_values(by="Score")
        st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error("Error loading PGA data. Try refreshing.")
        st.exception(e)

# ---------------- TAB 2: BACHELOR PARTY STANDINGS ---------------- #
with tab2:
    st.subheader("Bachelor Party Winnings 💸 (Top 10 Payouts Only)")

    payouts = {
        "1": 198,
        "2": 143,
        "3": 119,
        "4": 95,
        "5": 79,
        "6": 63,
        "7": 48,
        "8": 32,
        "9": 16,
        "10": 8
    }

    teams = {
        "James Trimble": ["Scottie Scheffler", "Jordan Spieth", "Shane Lowry", "Si Woo Kim", "Sergio Garcia", "Tom Kim", "Matt Fitzpatrick", "Samuel Stevens"],
        "Jack Rushin": ["Rory McIlroy", "Viktor Hovland", "Sepp Straka", "Keegan Bradley", "Sam Burns", "Denny McCarthy", "Brian Harman", "Thorbjorn Olesen"],
        "Jimmy Mangan": ["Bryson DeChambeau", "Brooks Koepka", "Russell Henley", "Maverick McNealy", "Dustin Johnson", "Max Homa", "David Puig", "Adam Scott"],
        "John Funkhouser": ["Jon Rahm", "Hideki Matsuyama", "Corey Conners", "Robert MacIntyre", "Will Zalatoris", "J.J. Spaun", "Michael Kim", "Harris English"],
        "Joseph Bauer": ["Xander Schauffele", "Patrick Cantlay", "Jason Day", "Tony Finau", "Keith Mitchell", "Aaron Rai", "Andrew Novak", "Alex Smalley"],
        "Rich Wehman": ["Justin Thomas", "Tommy Fleetwood", "Wyndham Clark", "Daniel Berger", "Cameron Smith", "Davis Thompson", "Thomas Detry", "Mackenzie Hughes"],
        "Jack Byrne": ["Collin Morikawa", "Tyrrell Hatton", "Sungjae Im", "Justin Rose", "Akshay Bhatia", "Taylor Pendrith", "Stephan Jaeger", "Rasmus Hojgaard"],
        "Matthew Bauer": ["Ludvig Åberg", "Joaquin Niemann", "Patrick Reed", "Min Woo Lee", "Dean Burmester", "Byeong Hun An", "Ryan Fox", "Rickie Fowler"],
    }

    # Get all players from leaderboard
    url = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard"
    try:
        r = requests.get(url)
        data = r.json()
        players = data["events"][0]["competitions"][0]["athletes"]

        player_results = {}
        for player in players:
            name = player["athlete"]["displayName"]
            pos = player["status"]["position"]["displayName"]
            player_results[name] = pos

        summary = []

        for friend, golfers in teams.items():
            total = 0
            for golfer in golfers:
                pos = player_results.get(golfer, "—")
                winnings = payouts.get(pos, 0)
                summary.append({
                    "Friend": friend,
                    "Golfer": golfer,
                    "Position": pos,
                    "Winnings": f"${winnings}"
                })
                total += winnings
            summary.append({
                "Friend": friend,
                "Golfer": "Total",
                "Position": "",
                "Winnings": f"${total}"
            })

        df_summary = pd.DataFrame(summary)
        df_summary["Winnings ($)"] = df_summary["Winnings"].apply(lambda x: int(x.replace("$", "")) if "$" in x else 0)

        leaderboard = df_summary[df_summary["Golfer"] == "Total"].sort_values(by="Winnings ($)", ascending=False)
        st.markdown("### 💰 Leaderboard")
        st.dataframe(leaderboard[["Friend", "Winnings"]], use_container_width=True)

        st.markdown("### 🏌️ Player Breakdown")
        st.dataframe(df_summary[df_summary["Golfer"] != "Total"][["Friend", "Golfer", "Position", "Winnings"]], use_container_width=True)

    except Exception as e:
        st.error("Error loading Bachelor Party leaderboard.")
        st.exception(e)
