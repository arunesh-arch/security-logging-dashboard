
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Security Monitoring Center",
    page_icon="🛡️",
    layout="wide"
)

# Initialize application data
if "logs" not in st.session_state:
    st.session_state.logs = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

st.title("🛡️ Security Logging & Alerting Center")
st.caption("SOC Dashboard | Simulated Security Monitoring System")

# Sidebar controls
st.sidebar.header("Monitoring Configuration")

logging_enabled = st.sidebar.toggle(
    "Enable Security Logging", True
)

alerting_enabled = st.sidebar.toggle(
    "Enable Security Alerting", True
)

incomplete_logging = st.sidebar.toggle(
    "Simulate Incomplete Logs", False
)

st.sidebar.info(
    "This application generates simulated security events. "
    "It does not interact with real accounts or systems."
)

# Main controls
st.subheader("Security Event Simulator")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚨 Simulate 5 Failed Logins", use_container_width=True,
                 width="stretch"):
        st.session_state.attempts += 5

        for i in range(5):
            event = {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Event": "Failed Login",
                "Username": "admin",
                "Source IP": (
                    "Not recorded"
                    if incomplete_logging
                    else "192.0.2.10"
                ),
                "Status": "Failed"
            }

            if logging_enabled:
                st.session_state.logs.append(event)

        if logging_enabled and alerting_enabled:
            alert = {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Alert": "Multiple Failed Login Attempts",
                "Severity": "HIGH",
                "Details": "5 failed login attempts detected"
            }
            st.session_state.alerts.append(alert)

with col2:
    if st.button("🔄 Reset Simulation", use_container_width=True,
                 width="stretch"):
        st.session_state.logs = []
        st.session_state.alerts = []
        st.session_state.attempts = 0
        st.rerun()

# Metrics
st.divider()
st.subheader("Security Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Attempts", st.session_state.attempts)
m2.metric("Events Logged", len(st.session_state.logs))
m3.metric("Alerts Generated", len(st.session_state.alerts))

status = "ACTIVE" if logging_enabled else "FAILED"
m4.metric("Logging Status", status)

# Alert section
st.divider()
st.subheader("🚨 Security Alerts")

if st.session_state.alerts:
    for alert in reversed(st.session_state.alerts):
        st.error(
            f"⚠️ {alert['Alert']} | "
            f"{alert['Severity']} | {alert['Time']}"
        )
else:
    st.success("No security alerts generated.")

# Logs section
st.divider()
st.subheader("📋 Security Event Logs")

if st.session_state.logs:
    st.dataframe(
        list(reversed(st.session_state.logs)),
        use_container_width=True,
        width="stretch",
        hide_index=True
    )
else:
    st.warning("No security events recorded.")

# Explanation
st.divider()
st.subheader("🔍 Monitoring Analysis")

if not logging_enabled:
    st.error(
        "LOGGING FAILURE: Security events are not being recorded. "
        "Investigators may have no evidence to review."
    )

elif not alerting_enabled:
    st.warning(
        "ALERTING FAILURE: Events are recorded, but suspicious "
        "activity is not generating alerts."
    )

elif incomplete_logging:
    st.warning(
        "INCOMPLETE LOGGING: Source IP information is missing. "
        "Investigating the source of suspicious activity becomes harder."
    )

else:
    st.success(
        "Monitoring is operational. Security events are recorded "
        "and alerts are generated for simulated suspicious activity."
    )
