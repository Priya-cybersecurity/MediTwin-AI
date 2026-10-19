
import random
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# MediTwin AI — educational Digital Twin prototype
# All telemetry and security events are simulated.
# ---------------------------------------------------------

st.set_page_config(
    page_title="MediTwin AI | Equipment Digital Twin",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }
    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #10243a, #174b63);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 { color: white; margin-bottom: .35rem; }
    .hero p { color: #d8eaf1; margin-bottom: .2rem; }
    .small-note { color: #64748b; font-size: .88rem; }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.25);
        padding: 14px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🏥 MediTwin AI</h1>
        <p>Privacy-aware healthcare equipment Digital Twin</p>
        <p>Local educational prototype · Simulated equipment telemetry</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "DEMO ONLY — All readings, alerts, confidence scores, and security "
    "events are simulated. This is not a medical device, diagnostic tool, "
    "or validated failure-prediction system. Never use it for clinical "
    "decisions or actual equipment safety decisions."
)


# ---------------------- Session state --------------------

defaults = {
    "history": [],
    "current_reading": None,
    "trend_history": [],
    "maintenance_log": [],
    "security_log": [],
    "reading_counter": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


DEVICES = [
    "Ventilator V-101",
    "Infusion Pump P-204",
    "Patient Monitor M-310",
]

SCENARIOS = [
    "Normal operation",
    "Abnormal equipment condition",
]


# ---------------------- Simulation -----------------------

def generate_reading(device, scenario, local_processing):
    """Generate fictional equipment telemetry for demonstration."""

    if scenario == "Normal operation":
        temperature = round(random.uniform(30, 39), 1)
        vibration = round(random.uniform(0.1, 1.2), 2)
        usage = random.randint(100, 900)
        confidence = round(random.uniform(94, 100), 1)
    else:
        temperature = round(random.uniform(44, 60), 1)
        vibration = round(random.uniform(2.2, 5.0), 2)
        usage = random.randint(900, 1800)
        confidence = round(random.uniform(65, 88), 1)

    if device == "Patient Monitor M-310":
        metric_label = "Signal quality (%)"
        metric_value = (
            round(random.uniform(92, 100), 1)
            if scenario == "Normal operation"
            else round(random.uniform(45, 75), 1)
        )
    else:
        metric_label = "Sensor confidence (%)"
        metric_value = confidence

    # These are illustrative demo rules, not validated thresholds.
    anomaly = (
        temperature >= 45
        or vibration >= 2.0
        or metric_value < 80
    )

    if temperature >= 52 or vibration >= 3.8:
        priority = "HIGH"
    elif anomaly:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    if priority == "HIGH":
        recommendation = (
            "Demo flag: review the simulated event with qualified "
            "biomedical engineering staff. Follow approved procedures."
        )
    elif priority == "MEDIUM":
        recommendation = (
            "Demo flag: review the illustrative readings and "
            "maintenance log."
        )
    else:
        recommendation = (
            "Demo status only: routine monitoring scenario selected. "
            "This does not establish actual equipment safety."
        )

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device": device,
        "scenario": scenario,
        "temperature_c": temperature,
        "vibration_mm_s": vibration,
        "usage_demo_units": usage,
        "metric_label": metric_label,
        "metric_value": metric_value,
        "priority": priority,
        "anomaly": anomaly,
        "processing": (
            "Local/edge simulation"
            if local_processing
            else "Central/cloud-style simulation"
        ),
        "recommendation": recommendation,
    }


def add_trend_point(reading):
    """Add a generated reading to the consistent session trend."""

    st.session_state.trend_history.append({
        "Time": reading["timestamp"],
        "Temperature (°C)": reading["temperature_c"],
        "Vibration (mm/s)": reading["vibration_mm_s"],
        "Device": reading["device"],
        "Priority": reading["priority"],
    })

    # Keep the latest 100 readings in this session.
    st.session_state.trend_history = (
        st.session_state.trend_history[-100:]
    )


# ---------------------- Sidebar -------------------------

st.sidebar.title("⚙️ Simulation controls")

device = st.sidebar.selectbox(
    "Virtual equipment",
    DEVICES,
)

scenario = st.sidebar.radio(
    "Illustrative scenario",
    SCENARIOS,
)

local_processing = st.sidebar.toggle(
    "Simulate local/edge processing",
    value=True,
)

show_security = st.sidebar.toggle(
    "Display a simulated security event",
    value=False,
)

st.sidebar.caption(
    "Controls affect fictional demo data only. "
    "No medical equipment is connected."
)

signature = (device, scenario, local_processing)

if (
    st.session_state.current_reading is None
    or st.session_state.get("reading_signature") != signature
):
    reading = generate_reading(
        device, scenario, local_processing
    )
    st.session_state.current_reading = reading
    st.session_state.reading_signature = signature
    add_trend_point(reading)


# ---------------------- Header controls -----------------

left, right = st.columns([3, 1])

with left:
    st.subheader("Equipment monitoring workspace")
    st.caption(
        "Current virtual-device snapshot — not real-time medical telemetry."
    )

with right:
    if st.button(
        "🔄 Generate new reading",
        type="primary",
        use_container_width=True,
    ):
        reading = generate_reading(
            device, scenario, local_processing
        )
        st.session_state.current_reading = reading
        st.session_state.reading_signature = signature
        st.session_state.reading_counter += 1
        add_trend_point(reading)
        st.rerun()

reading = st.session_state.current_reading


# ---------------------- Navigation ----------------------

overview_tab, trends_tab, maintenance_tab, privacy_tab = st.tabs([
    "🏠 Overview",
    "📈 Trends & History",
    "🛠️ Maintenance",
    "🔒 Privacy & Security",
])


# ====================== OVERVIEW =========================

with overview_tab:
    st.subheader("Virtual equipment snapshot")

    a, b, c, d = st.columns(4)

    a.metric("Virtual device", reading["device"])
    b.metric(
        "Simulated temperature",
        f'{reading["temperature_c"]:.1f} °C',
    )
    c.metric(
        "Simulated vibration",
        f'{reading["vibration_mm_s"]:.2f} mm/s',
    )
    d.metric(
        "Illustrative priority",
        reading["priority"],
    )

    st.subheader("Digital Twin status")

    if reading["priority"] == "HIGH":
        st.error("HIGH — simulated equipment-condition flag")
    elif reading["priority"] == "MEDIUM":
        st.warning("MEDIUM — simulated equipment-condition flag")
    else:
        st.success("LOW — selected demo scenario has no high-priority flag")

    x, y = st.columns(2)

    with x:
        st.write(
            f'**{reading["metric_label"]}:** '
            f'{reading["metric_value"]:.1f}'
        )
        st.write(
            f'**Processing mode:** {reading["processing"]}'
        )
        st.write(
            f'**Demo usage counter:** '
            f'{reading["usage_demo_units"]} units'
        )

    with y:
        st.write("**Illustrative next step**")
        st.write(reading["recommendation"])

    st.caption(
        "Priority labels are produced by simple demonstration rules. "
        "They are not validated risk assessments or safety guarantees."
    )

    st.subheader("Recent simulated telemetry")

    if st.session_state.trend_history:
        recent = pd.DataFrame(
            st.session_state.trend_history[-5:]
        )
        st.dataframe(
            recent.iloc[::-1],
            hide_index=True,
            use_container_width=True,
        )

    if st.button("Record current reading in session history"):
        st.session_state.history.append(reading.copy())
        st.success("Reading saved to the current app session.")


# =================== TRENDS & HISTORY ====================

with trends_tab:
    st.subheader("Sensor trends")
    st.caption(
        "Charts use generated demo readings recorded during this session. "
        "They do not represent real equipment measurements."
    )

    if st.session_state.trend_history:
        trend_df = pd.DataFrame(
            st.session_state.trend_history
        )

        temp_chart = px.line(
            trend_df,
            x="Time",
            y="Temperature (°C)",
            color="Device",
            markers=True,
            title="Simulated temperature history",
        )
        temp_chart.update_layout(
            xaxis_title="Recorded session time",
            yaxis_title="Temperature (°C)",
        )
        st.plotly_chart(
            temp_chart,
            use_container_width=True,
        )

        vibration_chart = px.line(
            trend_df,
            x="Time",
            y="Vibration (mm/s)",
            color="Device",
            markers=True,
            title="Simulated vibration history",
        )
        vibration_chart.update_layout(
            xaxis_title="Recorded session time",
            yaxis_title="Vibration (mm/s)",
        )
        st.plotly_chart(
            vibration_chart,
            use_container_width=True,
        )

        st.dataframe(
            trend_df.iloc[::-1],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Generate a simulated reading to begin the trend.")

    if st.session_state.history:
        st.subheader("Manually recorded session readings")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(
            history_df,
            hide_index=True,
            use_container_width=True,
        )

        st.download_button(
            "⬇️ Export recorded readings as CSV",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="meditwin_session_history.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "No readings have been manually recorded yet. "
            "Use the Overview tab to record the current reading."
        )


# ====================== MAINTENANCE ======================

with maintenance_tab:
    st.subheader("Illustrative maintenance workspace")

    st.write(
        "The following labels are generated from demo rules only. "
        "They do not determine whether real equipment is safe to use."
    )

    m1, m2, m3 = st.columns(3)

    m1.metric("Current demo priority", reading["priority"])
    m2.metric("Session readings", len(st.session_state.history))
    m3.metric(
        "Generated trend points",
        len(st.session_state.trend_history),
    )

    st.markdown("**Current illustrative observation**")
    st.write(reading["recommendation"])

    maintenance_note = st.text_input(
        "Maintenance note",
        placeholder="Example: Demo inspection reviewed",
        key="maintenance_note",
    )

    if st.button("Add simulated maintenance log entry"):
        if maintenance_note.strip():
            st.session_state.maintenance_log.append({
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "device": device,
                "note": maintenance_note.strip(),
                "record_type": "SIMULATED / EDUCATIONAL",
            })
            st.success("Demo maintenance note added to this session.")
        else:
            st.warning("Enter a note first.")

    if st.session_state.maintenance_log:
        st.subheader("Session maintenance log")
        maintenance_df = pd.DataFrame(
            st.session_state.maintenance_log
        )
        st.dataframe(
            maintenance_df,
            hide_index=True,
            use_container_width=True,
        )

        st.download_button(
            "⬇️ Export maintenance log",
            data=maintenance_df.to_csv(index=False).encode("utf-8"),
            file_name="meditwin_maintenance_log.csv",
            mime="text/csv",
        )
    else:
        st.info("No maintenance notes have been added this session.")


# =================== PRIVACY & SECURITY ==================

with privacy_tab:
    st.subheader("Privacy and security demonstration")

    st.info(
        "This prototype generates fictional telemetry. It does not "
        "connect to medical devices, inspect network traffic, or "
        "collect patient identifiers."
    )

    st.markdown("**Processing mode**")
    st.write(reading["processing"])

    st.markdown("**Storage behavior**")
    st.write(
        "Session data is held in Streamlit session state while the "
        "session remains active. It is not a durable database. "
        "CSV files are created only when you explicitly export data."
    )

    st.markdown("**Simulated security-event panel**")

    if show_security:
        event = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "event": "SIMULATED unusual access attempt",
            "status": "Fictional demonstration event",
        }

        if (
            not st.session_state.security_log
            or st.session_state.security_log[-1]["event"]
            != event["event"]
        ):
            st.session_state.security_log.append(event)

        st.error(
            "SIMULATED EVENT: unusual access attempt. "
            "No real access attempt or network activity was detected."
        )
    else:
        st.success("No simulated security event currently selected.")

    if st.session_state.security_log:
        security_df = pd.DataFrame(
            st.session_state.security_log
        )
        st.dataframe(
            security_df,
            hide_index=True,
            use_container_width=True,
        )

        st.download_button(
            "⬇️ Export simulated security events",
            data=security_df.to_csv(index=False).encode("utf-8"),
            file_name="meditwin_demo_security_events.csv",
            mime="text/csv",
        )

    st.caption(
        "A visual security demonstration is not a substitute for "
        "authentication, authorization, encryption, or security auditing."
    )


# ======================== LIMITATIONS ====================

with st.expander("Prototype limitations and future work"):
    st.markdown(
        """
        - All equipment readings and security events are simulated.
        - No actual ventilator, infusion pump, or patient monitor is connected.
        - Patient Monitor signal quality is illustrative telemetry, not a
          patient's vital signs.
        - Thresholds are simple demo rules, not clinically validated limits.
        - No machine-learning model has been trained or validated here.
        - Session state is not durable storage and may be lost when the
          session resets.
        - CSV exports are user-initiated and may contain session data.
        - Future engineering work could include authentication, role-based
          access, encrypted communications, validated equipment datasets,
          device interoperability, and independent safety review.
        """
    )

st.divider()
st.caption(
    "MediTwin AI · Educational prototype · Simulated data only"
)



# ---------- AI Anomaly Detection and Maintenance ----------

from maintenance_ai import train_model, analyse_equipment
if "ai_maintenance_history" not in st.session_state:
    st.session_state.ai_maintenance_history = []

st.divider()
st.header("🤖 AI Equipment Health Analysis")

st.caption("Educational prototype using simulated equipment readings.")

@st.cache_resource
def get_ai_model():
    return train_model()

ai_model = get_ai_model()

col1, col2, col3 = st.columns(3)

with col1:
    ai_temperature = st.slider(
        "AI Temperature (°C)", 20.0, 60.0, 37.0, 0.5
    )

with col2:
    ai_vibration = st.slider(
        "AI Vibration (simulated units)", 0.0, 8.0, 2.0, 0.1
    )

with col3:
    ai_usage = st.number_input(
        "AI Usage Hours", min_value=0, max_value=100000, value=1000
    )

if st.button("Analyse Equipment Health"):
    result = analyse_equipment(
        ai_model,
        ai_temperature,
        ai_vibration,
        ai_usage
    )


    priority = str(result.get("Priority", result.get("priority", "LOW"))).upper()

    if priority == "HIGH":
        st.error("🚨 HIGH PRIORITY ALERT: Equipment needs urgent maintenance review!")
    elif priority == "MEDIUM":
        st.warning("⚠️ MEDIUM PRIORITY: Schedule equipment maintenance.")
    else:
        st.success("✅ LOW PRIORITY: No immediate maintenance action indicated by this demo.")


    st.divider()
    st.subheader("📊 Latest Equipment Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌡️ Temperature", f"{ai_temperature} °C")

    with col2:
        st.metric("📳 Vibration", f"{ai_vibration}")

    with col3:
        st.metric("⏱️ Usage Hours", f"{ai_usage}")

    with col4:
        st.metric("🛠️ Priority", priority)

    if priority == "HIGH":
        st.error("🚨 Equipment status: Maintenance review required")
    elif priority == "MEDIUM":
        st.warning("⚠️ Equipment status: Maintenance recommended")
    else:
        st.success("✅ Equipment status: Low priority")




    st.session_state.ai_maintenance_history.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Temperature": ai_temperature,
        "Vibration": ai_vibration,
        "Usage Hours": ai_usage,
        "Anomaly": result["anomaly"],
        "Priority": result["priority"],
        "Recommendation": result["recommendation"]
    })

    if result["anomaly"]:
        st.warning("Unusual sensor pattern detected.")
    else:
        st.success("No unusual pattern detected by the AI model.")

    st.metric("Maintenance Priority", result["priority"])
    st.write("**Recommended action:**", result["recommendation"])
    st.caption(f"Model anomaly score: {result['anomaly_score']}")

    st.info(
        "Simulation only. This result is not a validated failure prediction. "
        "Qualified biomedical staff must assess actual equipment."
    )

    st.divider()
st.subheader("Maintenance History")

if st.session_state.ai_maintenance_history:
    history_df = pd.DataFrame(
        st.session_state.ai_maintenance_history
    )

    st.dataframe(history_df, use_container_width=True)

    csv_data = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Maintenance History (CSV)",
        data=csv_data,
        file_name="meditwin_maintenance_history.csv",
        mime="text/csv"
    )
else:
    st.info("Run an equipment analysis to create maintenance history.")

   
st.divider()
st.subheader("Maintenance Priority Overview")

if st.session_state.ai_maintenance_history:
    priority_df = pd.DataFrame(
        st.session_state.ai_maintenance_history
    )

    priority_counts = (
        priority_df["Priority"]
        .value_counts()
        .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
        .rename_axis("Priority")
        .reset_index(name="Count")
    )

    priority_chart = px.bar(
        priority_counts,
        x="Priority",
        y="Count",
        title="Analysis Results by Maintenance Priority",
        text="Count"
    )

    st.plotly_chart(priority_chart, use_container_width=True)
else:
    st.info("Run an equipment analysis to display the chart.")


# MULTIPLE SIMULATED EQUIPMENT MONITORING


# EQUIPMENT HEALTH TREND CHARTS

st.divider()
st.header("📈 Equipment Health Trends")
st.caption(
    "Trends are based on equipment analyses recorded "
    "during this app session."
)

if st.session_state.ai_maintenance_history:
    trend_df = pd.DataFrame(
        st.session_state.ai_maintenance_history
    ).copy()

    # Convert recorded time into a usable date-time format
    trend_df["Time"] = pd.to_datetime(
        trend_df["Time"], errors="coerce"
    )
    trend_df = trend_df.dropna(subset=["Time"])

    # Give each analysis a sequential number
    trend_df = trend_df.reset_index(drop=True)
    trend_df["Analysis"] = range(1, len(trend_df) + 1)

    if not trend_df.empty:
        st.subheader("🌡️ Temperature Trend")

        temperature_chart = px.line(
            trend_df,
            x="Analysis",
            y="Temperature",
            markers=True,
            title="Temperature Across Analyses"
        )
        st.plotly_chart(
            temperature_chart,
            use_container_width=True
        )

        st.subheader("📳 Vibration Trend")

        vibration_chart = px.line(
            trend_df,
            x="Analysis",
            y="Vibration",
            markers=True,
            title="Vibration Across Analyses"
        )
        st.plotly_chart(
            vibration_chart,
            use_container_width=True
        )

        st.subheader("⏱️ Usage Hours Trend")

        usage_chart = px.line(
            trend_df,
            x="Analysis",
            y="Usage Hours",
            markers=True,
            title="Usage Hours Across Analyses"
        )
        st.plotly_chart(
            usage_chart,
            use_container_width=True
        )

        st.subheader("🛠️ Maintenance Priority Trend")

        priority_values = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3
        }

        trend_df["Priority Level"] = (
            trend_df["Priority"]
            .map(priority_values)
        )

        priority_chart = px.line(
            trend_df,
            x="Analysis",
            y="Priority Level",
            markers=True,
            title="Maintenance Priority Across Analyses"
        )

        priority_chart.update_yaxes(
            tickmode="array",
            tickvals=[1, 2, 3],
            ticktext=["LOW", "MEDIUM", "HIGH"]
        )

        st.plotly_chart(
            priority_chart,
            use_container_width=True
        )

    else:
        st.info("No valid equipment analysis times are available.")

else:
    st.info(
        "Run Analyse Equipment Health to generate "
        "your first health trend charts."
    )

st.divider()
st.header("🏥 Equipment Fleet Monitor")
st.caption("Demo only: all equipment readings are simulated.")

fleet_data = [
    {
        "Equipment ID": "DEV-001",
        "Equipment": "Ventilator",
        "Temperature": 37.5,
        "Vibration": 2.0,
        "Usage Hours": 1200
    },
    {
        "Equipment ID": "DEV-002",
        "Equipment": "Infusion Pump",
        "Temperature": 46.0,
        "Vibration": 2.0,
        "Usage Hours": 1800
    },
    {
        "Equipment ID": "DEV-003",
        "Equipment": "Patient Monitor",
        "Temperature": 42.0,
        "Vibration": 2.0,
        "Usage Hours": 2200
    },
    {
        "Equipment ID": "DEV-004",
        "Equipment": "Suction Unit",
        "Temperature": 36.8,
        "Vibration": 2.0,
        "Usage Hours": 900
    }
]

fleet_df = pd.DataFrame(fleet_data)


def fleet_priority(row):
    temp = row["Temperature"]
    vibration = row["Vibration"]
    hours = row["Usage Hours"]

    if temp >= 45 or vibration >= 4.5:
        return "HIGH"
    elif (
        temp >= 41
        or vibration >= 3.5
        or hours >= 4000
    ):
        return "MEDIUM"
    else:
        return "LOW"


fleet_df["Priority"] = fleet_df.apply(
    fleet_priority, axis=1
)

st.subheader("Equipment Overview")

high_count = (fleet_df["Priority"] == "HIGH").sum()
medium_count = (fleet_df["Priority"] == "MEDIUM").sum()
low_count = (fleet_df["Priority"] == "LOW").sum()

col1, col2, col3 = st.columns(3)

col1.metric("🚨 High Priority", int(high_count))
col2.metric("⚠️ Medium Priority", int(medium_count))
col3.metric("✅ Low Priority", int(low_count))

st.subheader("Individual Equipment Status")
st.dataframe(
    fleet_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("Fleet Maintenance Priority Chart")

priority_counts = (
    fleet_df["Priority"]
    .value_counts()
    .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
)

st.bar_chart(priority_counts)

st.info(
    "These are illustrative, rule-based priorities using "
    "simulated readings. They are separate from the AI "
    "analysis of your individual equipment inputs."
)
