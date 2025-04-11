import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="IPL 2025 Report App", layout="centered")

# Load IPL schedule
schedule_df = pd.read_csv("ipl_schedule.csv", parse_dates=["DATE"])

# Initialize report storage
REPORT_FILE = "ipl_reports.csv"
try:
    reports_df = pd.read_csv(REPORT_FILE)
except FileNotFoundError:
    reports_df = pd.DataFrame(columns=["date", "time", "team1", "team2", "who_hit_six", "who_won"])
    reports_df.to_csv(REPORT_FILE, index=False)

# Function to get today's matches
def get_match(date, time=None):
    date = pd.to_datetime(date).date()
    if time:
        filtered = schedule_df[(schedule_df["DATE"].dt.date == date) & (schedule_df["TIME"] == time)]
    else:
        filtered = schedule_df[schedule_df["DATE"].dt.date == date]
    return filtered.iloc[0] if not filtered.empty else None

# Apply basic custom style
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
    }
    .big-match {
        font-size: 25px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
        .big-matchs {
        font-size: 25px;
        font-weight: bold;
        color: #69fa7a;
        margin-bottom: 10px;
    }
    .highlight {
        background-color: #69fa7a;
        padding: 10px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Page navigation
page = st.sidebar.radio("📂 Choose a page", ["Add Report", "View Report"])

# Page 1: Add Report
if page == "Add Report":
    st.header("📋 Add IPL Match Report")

    today = datetime.date.today()
    date_input = st.date_input("Select match date", value=today)
    is_weekend = date_input.weekday() in [5, 6]  # Sat=5, Sun=6

    time_input = None
    if is_weekend:
        time_display = {
    "3:30 PM": "15:30",
    "7:30 PM": "19:30"
}
        selected_display = st.selectbox("Select match time", list(time_display.keys()))
        time_input = time_display[selected_display]


    # Get teams based on schedule
    match = get_match(date_input, time_input)
    if match is not None:
        team1 = match["TEAM 1"]
        team2 = match["TEAM 2"]

        st.markdown(f'<div class="big-match">{team1} 🆚 {team2}</div>', unsafe_allow_html=True)
        who_hit_six = st.selectbox("6️⃣ Who hit a six in the first 2 overs?", ["Neither", team1, team2, "Both"])
        who_won = st.selectbox("🏆 Who won the match?", [team1, team2])


       
        if st.button("📤 Submit Report"):
            new_report = {
                "date": date_input,
                "time": time_input if time_input else "",
                "team1": team1,
                "team2": team2,
                "who_hit_six": who_hit_six,
                "who_won": who_won
            }
            reports_df = reports_df.append(new_report, ignore_index=True)
            reports_df.to_csv(REPORT_FILE, index=False)
            st.success("✅ Report submitted successfully!")
    else:
        st.warning("⚠️ No match scheduled on this date/time.")

# Page 2: View Report
else:
    st.header("📅 View Match Report")

    date_input = st.date_input("Select date to view match")

    is_weekend = date_input.weekday() in [5, 6]
    time_input = None
    if is_weekend:
        time_input = st.selectbox("Select match time", ["15:30", "19:30"])

    if st.button("🔍 Get Report"):
        filtered = reports_df[reports_df["date"] == str(date_input)]
        if is_weekend:
            filtered = filtered[filtered["time"] == time_input]

        if not filtered.empty:
            match = filtered.iloc[0]
            st.markdown(f'<div class="big-match">{match["team1"]} 🆚 {match["team2"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="big-matchs"><strong style="color: white;">🏆 Winner:</strong> {match["who_won"]}</div>',unsafe_allow_html=True)

            st.markdown(f'<div class="big-matchs"><strong style="color: white;">💥 Six in first 2 overs:</strong> {match["who_hit_six"]}</div>',unsafe_allow_html=True)

        else:
            st.warning("⚠️ No report found for this date and time.")

