
## Team and Institution

**College:** Adhiyamaan College of Engineering  
**Department:** Computer Science and Engineering (Cybersecurity)  
**Programme:** B.E. CSE (Cybersecurity)

### Team Members

| Name | Role |
|---|---|
| Priyadharshini S | Team Lead |
| Madhanraj S | Team Member |


### College / Incubator Information

**Institution:** Adhiyamaan College of Engineering  
**Programme:** B.E. CSE (Cybersecurity)  
**Incubator Affiliation:** Not applicable — the project is being developed independently by the student team for the Hack-A-Throne hackathon.


### Project

**Project Name:** MediTwin AI

# MediTwin AI

**Privacy-aware Healthcare Equipment Digital Twin — beginner hackathon prototype**

MediTwin AI demonstrates how a hospital could visualize simulated medical-equipment telemetry, flag unusual equipment patterns, prioritize maintenance review, and record an audit-style session history.

> **Safety note:** This is an educational prototype using synthetic data. It is not a medical device, diagnostic system, clinically validated predictive-maintenance model, or real-time hospital monitoring system. Do not use it for clinical decisions.

## Problem

Hospitals rely on different medical devices and monitoring systems. Fragmented equipment information can make it difficult to demonstrate unified condition monitoring, maintenance prioritization, privacy-conscious processing, and decision support.

## Proposed solution

A single interactive dashboard that:
- Represents three example device types.
- Generates normal and abnormal simulated telemetry.
- Flags illustrative anomalies using transparent thresholds.
- Recommends human-reviewed maintenance actions.
- Demonstrates local/edge versus cloud-style processing modes.
- Displays simulated security events and a session audit trail.
- Exports session history as CSV.

## Technology stack

| Tool | Role |
|---|---|
| Python | App logic and simulation |
| Streamlit | Interactive web dashboard |
| Pandas | Tabular readings and session history |
| Plotly | Trend charts |
| SQLite | Planned future extension; not used in this starter version |
| GitHub | Version control and project documentation |

## Run locally

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment (recommended).

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Demo steps

1. Select a device in the sidebar.
2. Choose **Normal operation** and observe the indicators.
3. Choose **Abnormal equipment condition** to see a higher maintenance priority.
4. Switch between local/edge and cloud-style simulation.
5. Enable the simulated security event.
6. Add readings to session history and export the CSV.

## How the prototype maps to the research gap

- **Integrated framework:** device simulation, anomaly rules, maintenance recommendations, and dashboard in one app.
- **Privacy:** generated data only; no real patient information.
- **Edge–cloud intelligence:** demonstrates two processing modes conceptually; it does not connect to actual edge/cloud infrastructure.
- **Predictive maintenance:** demonstrates condition-based anomaly flags and priority recommendations; it does not forecast a real failure.
- **Autonomous decision support:** provides rule-based suggestions for human review; it does not control medical equipment.
- **Heterogeneous environments:** configurable profiles for several device categories.

## Results

The prototype should display generated readings, flag abnormal scenarios, show trend charts, and let the user export session history. Record your own screenshots and actual test outcomes after running it; do not claim unperformed tests.

## Repository structure

```text
MediTwin_AI/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations and future work

- Add authenticated roles and stronger access control.
- Add encrypted storage and secure communications.
- Connect to validated, de-identified equipment datasets.
- Evaluate anomaly detection against labeled data.
- Add real edge-device and cloud integration.
- Complete medical-device safety, privacy, and clinical validation before any real-world use.

## Suggested GitHub description

Privacy-aware healthcare equipment Digital Twin prototype with simulated telemetry, anomaly alerts, maintenance decision support, and edge–cloud workflow demonstration.
