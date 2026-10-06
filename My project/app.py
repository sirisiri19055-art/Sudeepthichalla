import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Smart Timetable Generator",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #243b6b;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.subject-box {
    background-color: #eef4ff;
    padding: 12px;
    border-radius: 10px;
    margin: 5px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">📚 AI Based Smart Timetable Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Create a personalized and intelligent study timetable based on your subjects, '
    'difficulty and available time.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Timetable Settings")

student_name = st.sidebar.text_input(
    "👤 Student Name",
    placeholder="Enter your name"
)

course = st.sidebar.text_input(
    "🎓 Course / Branch",
    placeholder="Example: B.Tech CSE"
)

days = st.sidebar.multiselect(
    "📅 Select Study Days",
    [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ],
    default=[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
    ]
)

study_hours = st.sidebar.slider(
    "⏰ Study Hours Per Day",
    min_value=1,
    max_value=12,
    value=4
)

session_duration = st.sidebar.selectbox(
    "⏱️ Session Duration",
    [30, 45, 60, 90, 120],
    index=2
)

# =========================================================
# SUBJECT INPUT
# =========================================================

st.header("📖 Enter Your Subjects")

st.write(
    "Add the subjects you want to include in your study timetable."
)

if "subjects" not in st.session_state:
    st.session_state.subjects = []

col1, col2, col3 = st.columns(3)

with col1:
    subject_name = st.text_input(
        "Subject Name",
        placeholder="Example: DBMS"
    )

with col2:
    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

with col3:
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )

if st.button("➕ Add Subject"):

    if subject_name.strip() == "":
        st.warning("Please enter a subject name.")

    else:

        st.session_state.subjects.append({
            "Subject": subject_name,
            "Difficulty": difficulty,
            "Priority": priority
        })

        st.success(f"{subject_name} added successfully!")

# =========================================================
# DISPLAY SUBJECTS
# =========================================================

if st.session_state.subjects:

    st.subheader("📋 Your Subjects")

    subject_df = pd.DataFrame(st.session_state.subjects)

    st.dataframe(
        subject_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑️ Clear All Subjects"):
        st.session_state.subjects = []
        st.rerun()

else:

    st.info(
        "No subjects added yet. Add your subjects using the form above."
    )

# =========================================================
# GENERATE TIMETABLE
# =========================================================

st.divider()

st.header("🤖 Generate Smart Timetable")

if st.button("🚀 Generate My Timetable", use_container_width=True):

    if len(days) == 0:
        st.error("Please select at least one study day.")

    elif len(st.session_state.subjects) == 0:
        st.error("Please add at least one subject.")

    else:

        # -------------------------------------------------
        # SUBJECT WEIGHT CALCULATION
        # -------------------------------------------------

        subjects = []

        for subject in st.session_state.subjects:

            weight = 1

            if subject["Difficulty"] == "Hard":
                weight += 2

            elif subject["Difficulty"] == "Medium":
                weight += 1

            if subject["Priority"] == "High":
                weight += 2

            elif subject["Priority"] == "Medium":
                weight += 1

            for _ in range(weight):
                subjects.append(subject["Subject"])

        # -------------------------------------------------
        # REMOVE DUPLICATES WHILE KEEPING ORDER
        # -------------------------------------------------

        unique_subjects = list(dict.fromkeys(subjects))

        # -------------------------------------------------
        # NUMBER OF SESSIONS
        # -------------------------------------------------

        sessions_per_day = max(
            1,
            int((study_hours * 60) / session_duration)
        )

        total_sessions = sessions_per_day * len(days)

        # -------------------------------------------------
        # CREATE TIMETABLE
        # -------------------------------------------------

        timetable = []

        for i in range(total_sessions):

            day = days[i % len(days)]

            subject = subjects[i % len(subjects)]

            session_number = (i // len(days)) + 1

            start_hour = 6 + (
                (i % sessions_per_day)
                * (session_duration // 60 + 1)
            )

            if start_hour >= 22:
                start_hour = 20

            start_time = f"{start_hour:02d}:00"

            end_minutes = (
                start_hour * 60 + session_duration
            )

            end_hour = end_minutes // 60
            end_minute = end_minutes % 60

            end_time = f"{end_hour:02d}:{end_minute:02d}"

            timetable.append({
                "Day": day,
                "Time": f"{start_time} - {end_time}",
                "Subject": subject,
                "Session": f"Session {session_number}",
                "Activity": "Study + Practice"
            })

        timetable_df = pd.DataFrame(timetable)

        # -------------------------------------------------
        # DISPLAY RESULT
        # -------------------------------------------------

        st.success(
            "🎉 Your personalized smart timetable has been generated!"
        )

        st.subheader("📅 Your Weekly Timetable")

        st.dataframe(
            timetable_df,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # DOWNLOAD BUTTON
        # -------------------------------------------------

        csv = timetable_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Timetable",
            data=csv,
            file_name="smart_timetable.csv",
            mime="text/csv"
        )

        # =================================================
        # ANALYSIS
        # =================================================

        st.divider()

        st.subheader("📊 Timetable Analysis")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📚 Subjects",
                len(st.session_state.subjects)
            )

        with col2:
            st.metric(
                "📅 Study Days",
                len(days)
            )

        with col3:
            st.metric(
                "⏰ Hours / Day",
                study_hours
            )

        with col4:
            st.metric(
                "📝 Sessions",
                len(timetable_df)
            )

        # =================================================
        # SUBJECT DISTRIBUTION
        # =================================================

        st.subheader("📈 Subject Distribution")

        distribution = (
            timetable_df["Subject"]
            .value_counts()
            .reset_index()
        )

        distribution.columns = [
            "Subject",
            "Sessions"
        ]

        st.bar_chart(
            distribution.set_index("Subject")
        )

# =========================================================
# SMART STUDY TIPS
# =========================================================

st.divider()

st.header("💡 Smart Study Recommendations")

recommendations = [
    "Start your day with difficult subjects when your concentration is high.",
    "Take a short break after every study session.",
    "Practice coding regularly instead of studying only theory.",
    "Revise previously studied topics every week.",
    "Keep one session for solving previous question papers.",
    "Avoid studying the same subject continuously for many hours.",
    "Track your progress and update your timetable regularly."
]

for recommendation in recommendations:
    st.write("✅", recommendation)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <h4>🤖 AI Based Smart Timetable Generator</h4>
        <p>Personalized • Smart • Simple • Student Friendly</p>
        <p>Developed using Python & Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)