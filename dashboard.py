import streamlit as st
import pandas as pd
import base64
import requests

from emi_calculator import calculate_emi
from emi_schedule import generate_schedule

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="EMI Dashboard", layout="wide")

# -------------------- BACKGROUND VIDEO --------------------
def add_bg_video(video_file):
    try:
        with open(video_file, "rb") as video:
            video_bytes = video.read()
            encoded = base64.b64encode(video_bytes).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background: none;
        }}

        video {{
            position: fixed;
            top: 0;
            left: 0;
            min-width: 100%;
            min-height: 100%;
            z-index: -1;
            object-fit: cover;
        }}
        </style>

        <video autoplay muted loop>
            <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
        </video>
        """, unsafe_allow_html=True)

    except:
        st.warning("⚠️ Background video not loaded")

add_bg_video("background.mp4")

# -------------------- UI STYLING --------------------
st.markdown("""
<style>

/* TITLE GLASS */
.title-container {
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.title-text {
    font-size: 48px;
    font-weight: bold;
    color: white;
    text-shadow: 2px 2px 12px rgba(0,0,0,0.9);
}

/* GLASS BOX */
.glass-box {
    background: rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}

/* HEADINGS BLACK */
h2, h3 {
    color: black !important;
}

/* METRIC LABEL */
[data-testid="stMetricLabel"] {
    color: black !important;
    font-weight: 600;
}

/* METRIC VALUE */
[data-testid="stMetricValue"] {
    color: black !important;
    font-size: 30px;
    font-weight: bold;
}

/* METRIC BOX */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.4);
    padding: 10px;
    border-radius: 10px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

/* TABLE */
[data-testid="stDataFrame"] {
    background-color: rgba(0,0,0,0.6);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("""
<div class="title-container">
    <div class="title-text">💰 EMI Calculator & Tracking System</div>
</div>
""", unsafe_allow_html=True)

# -------------------- INPUTS --------------------
col1, col2, col3 = st.columns(3)

with col1:
    principal = st.number_input("💵 Loan Amount (₹)", min_value=0.0, value=20000.0)

with col2:
    rate = st.number_input("📊 Interest Rate (%)", min_value=0.0, value=9.0)

with col3:
    tenure = st.number_input("📅 Tenure (months)", min_value=1, value=24)

# -------------------- CALCULATE --------------------
if st.button("🚀 Calculate EMI"):

    if principal <= 0 or rate <= 0:
        st.error("❌ Please enter valid values")
    else:

        emi = calculate_emi(principal, rate, tenure)
        df = generate_schedule(principal, rate, tenure, emi)

        total_payment = emi * tenure
        total_interest = total_payment - principal

        # EMI SUMMARY
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("## 💸 EMI Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Monthly EMI", f"₹ {emi:,.2f}")
        c2.metric("Total Interest", f"₹ {total_interest:,.2f}")
        c3.metric("Total Payment", f"₹ {total_payment:,.2f}")

        st.markdown('</div>', unsafe_allow_html=True)

        # INSIGHTS
        st.markdown("## 🧠 Insights")

        if total_interest > principal * 0.5:
            st.warning("⚠️ High interest burden! Consider reducing tenure.")
        else:
            st.success("✅ Loan looks manageable.")

        if tenure > 60:
            st.info("💡 Tip: Shorter tenure reduces total interest significantly.")

        # EMI SCHEDULE
        st.markdown("## 📋 EMI Schedule")
        st.dataframe(df, use_container_width=True)

        # CHARTS
        st.markdown("## 📈 Interest vs Principal")
        st.line_chart(df[["Interest", "Principal"]])

        st.markdown("## 📉 Remaining Balance")
        st.line_chart(df["Balance"])

        # PIE
        st.markdown("## 🥧 Payment Distribution")
        fig = df[["Interest", "Principal"]].sum().plot.pie(autopct='%1.1f%%').figure
        st.pyplot(fig)

        # DOWNLOAD
        st.download_button(
            "📥 Download EMI Report",
            df.to_csv(index=False),
            "emi_report.csv",
            "text/csv"
        )

        st.toast(f"EMI calculated: ₹ {emi:,.2f}")

# -------------------- LOAN HISTORY --------------------
if st.button("📜 View Loan History"):
    try:
        res = requests.get("http://127.0.0.1:5000/loans")
        st.write(res.json())
    except:
        st.error("❌ Backend not running")