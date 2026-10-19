import random
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="MediTwin AI", page_icon="🏥", layout="wide")
st.title("🏥 MediTwin AI")
st.caption("Privacy-aware healthcare equipment Digital Twin — educational prototype using simulated data only.")

st.warning("Demo only: all readings are simulated. This is not a medical device, diagnostic tool, or validated failure-prediction system. Never use it to make clinical decisions.")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Simulation controls")
device = st.sidebar.selectbox("Medical equipment", ["Ventilator V-101", "Infusion Pump P-204", "Patient Monitor M-310"])
mode = st.sidebar.radio("Scenario", ["Normal operation", "Abnormal equipment condition"])
local_processing = st.sidebar.toggle("Simulate edge/local processing", value=True)
show_security = st.sidebar.toggle("Show security event", value=False)

if mode == "Normal operation":
    temp = round(random.uniform(30, 39), 1)
    vibration = round(random.uniform(0.1, 1.2), 2)
    usage = random.randint(100, 900)
else:
    temp = round(random.uniform(44, 60), 1)
    vibration = round(random.uniform(2.2, 5.0), 2)
    usage = random.randint(900, 1800)

if device == "Patient Monitor M-310":
    # These are illustrative equipment telemetry values, not patient vital signs.
    metric_label = "Signal quality (%)"
    metric_value = round(random.uniform(92, 100) if mode == "Normal operation" else random.uniform(45, 75), 1)
else:
    metric_label = "Sensor confidence (%)"
    metric_value = round(random.uniform(94, 100) if mode == "Normal operation" else random.uniform(65, 88), 1)

anomaly = temp >= 45 or vibration >= 2.0 or metric_value < 80
priority = "HIGH" if temp >= 52 or vibration >= 3.8 else ("MEDIUM" if anomaly else "LOW")
recommendation = (
    "Escalate to biomedical engineering staff; inspect device according to approved hospital procedures."
    if priority == "HIGH" else
    "Schedule inspection and review recent equipment logs."
    if priority == "MEDIUM" else
    "Continue routine monitoring and scheduled maintenance."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Virtual device", device)
col2.metric("Temperature", f"{temp} °C")
col3.metric("Vibration", f"{vibration} mm/s")
col4.metric("Maintenance priority", priority)

st.subheader("Digital Twin status")
status = "⚠️ Abnormal pattern detected" if anomaly else "✅ Simulated normal operation"
st.markdown(f"### {status}")
st.write(f"**{metric_label}:** {metric_value}")
st.write(f"**Processing mode:** {'Local/edge simulation' if local_processing else 'Central/cloud-style simulation'}")
st.write(f"**Recommended next step:** {recommendation}")

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
record = {"timestamp": now, "device": device, "scenario": mode, "temperature_c": temp,
          "vibration_mm_s": vibration, metric_label: metric_value, "priority": priority,
          "processing": "edge" if local_processing else "cloud"}
if st.button("Add this simulated reading to history"):
    st.session_state.history.append(record)
    st.success("Simulated reading added to this session's history.")

st.subheader("Sensor trend (illustrative)")
trend = pd.DataFrame({
    "Time step": list(range(1, 13)),
    "Temperature (°C)": [round(random.uniform(31, 38), 1) for _ in range(8)] + [temp, temp, temp, temp],
    "Vibration (mm/s)": [round(random.uniform(0.2, 1.1), 2) for _ in range(8)] + [vibration, vibration, vibration, vibration]
})
chart1, chart2 = st.columns(2)
chart1.plotly_chart(px.line(trend, x="Time step", y="Temperature (°C)", title="Simulated temperature trend"), use_container_width=True)
chart2.plotly_chart(px.line(trend, x="Time step", y="Vibration (mm/s)", title="Simulated vibration trend"), use_container_width=True)

st.subheader("Privacy and security")
st.write("The prototype uses generated values and stores history only in the current app session unless you export it.")
if show_security:
    st.error("SIMULATED SECURITY EVENT: unusual access attempt detected. No real network traffic is monitored.")
else:
    st.info("No simulated security event selected.")
st.caption("Privacy design demonstration: no real patient identifiers or clinical records are collected.")

if st.session_state.history:
    st.subheader("Session history / audit trail")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)
    st.download_button("Download session history CSV", history_df.to_csv(index=False), "meditwin_session_history.csv", "text/csv")

with st.expander("Prototype limitations and next steps"):
    st.markdown("""
    - Edge/cloud behavior is simulated; no actual edge device or cloud service is connected.
    - Anomaly flags use transparent demonstration thresholds, not a trained or clinically validated model.
    - The dashboard supports equipment-condition scenarios, not diagnosis or treatment.
    - Future work: authenticated roles, validated datasets, device interoperability, encrypted transport, model evaluation, and safety review.
    """)
