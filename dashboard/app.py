import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


METRICS_FILE = "data/clean/conversation_metrics.csv"

st.set_page_config(page_title="AI Agentic Dashboard", layout="centered")
st.title("🤖 AI Agentic Conversational Dashboard")
st.write("Agent Performance & Funnel Health")


# Load Metrics
try:
    metrics_df = pd.read_csv(METRICS_FILE)
except FileNotFoundError:
    st.error("❌ conversation_metrics.csv not found")
    st.stop()

if metrics_df.empty:
    st.warning("⚠️ Metrics file is empty. Run metrics generation first.")
    st.stop()

metrics = metrics_df.iloc[0]

# Helper to safely fetch numeric values
def safe_int(val, default=0):
    try:
        if pd.isna(val):
            return default
        return int(val)
    except Exception:
        return default

def safe_float(val, default=0.0):
    try:
        if pd.isna(val):
            return default
        return float(val)
    except Exception:
        return default

# 1️⃣ Outcome Metrics
st.header("📊 Outcome Metrics")

completed = safe_int(metrics.get("completed_count", 0))
engaged = safe_int(metrics.get("engaged_count", 0))
closed = safe_int(metrics.get("closed_count", 0))

c1, c2, c3 = st.columns(3)
c1.metric("Completed", completed)
c2.metric("Engaged", engaged)
c3.metric("Closed", closed)


# 2️⃣ Retry Behaviour
st.header("🔁 Retry Behaviour")

avg_retry = safe_float(metrics.get("avg_retry_count", 0.0))
max_retry_hits = safe_int(metrics.get("max_retry_reached_count", 0))

c4, c5 = st.columns(2)
c4.metric("Average Retries", avg_retry)
c5.metric("Max Retry Hits", max_retry_hits)


# 3️⃣ Funnel State Distribution
st.header("🔀 Funnel State Distribution")

state_cols = [col for col in metrics.index if col.startswith("state_") and col.endswith("_count")]

if not state_cols:
    st.info("ℹ️ No state distribution data available yet.")
else:
    state_names = [c.replace("state_", "").replace("_count", "") for c in state_cols]
    state_values = [safe_int(metrics[c]) for c in state_cols]

    fig, ax = plt.subplots()
    ax.bar(state_names, state_values)
    ax.set_ylabel("Leads")
    ax.set_xlabel("State")
    ax.set_title("Conversation Funnel Distribution")
    st.pyplot(fig)


# 4️⃣ Stop Reasons (Crash-proof Pie)
st.header("🛑 Stop Reasons")

stopped_by_completion = safe_int(metrics.get("stopped_by_completion", 0))
stopped_by_max_retries = safe_int(metrics.get("stopped_by_max_retries", 0))

if stopped_by_completion == 0 and stopped_by_max_retries == 0:
    st.info("ℹ️ No stop events yet to visualize.")
else:
    stop_data = {
        "Completed": stopped_by_completion,
        "Closed (Max Retries)": stopped_by_max_retries
    }

    fig2, ax2 = plt.subplots()
    ax2.pie(
        stop_data.values(),
        labels=stop_data.keys(),
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.axis("equal")
    ax2.set_title("Why the Agent Stops")
    st.pyplot(fig2)

st.success("✅ Dashboard loaded successfully")
