import pandas as pd

STATE_FILE = "data/clean/conversation_state.csv"
OUTPUT_FILE = "data/clean/conversation_metrics.csv"


def generate_metrics():
    try:
        df = pd.read_csv(STATE_FILE)
    except FileNotFoundError:
        print(" conversation_state.csv not found")
        return

    if df.empty:
        print(" conversation_state.csv is empty")
        return

    metrics = {}

    # 1️⃣ Outcome metrics
    metrics["completed_count"] = (df["current_state"] == "completed").sum()
    metrics["engaged_count"] = (df["current_state"] == "engaged").sum()
    metrics["closed_count"] = (df["current_state"] == "closed").sum()

    # 2️⃣ Retry metrics
    metrics["avg_retry_count"] = round(df["retry_count"].mean(), 2)
    metrics["max_retry_reached_count"] = (df["retry_count"] >= 3).sum()

    # 3️⃣ State distribution
    state_counts = df["current_state"].value_counts()
    for state, count in state_counts.items():
        metrics[f"state_{state}_count"] = int(count)

    # 4️⃣ Stop reasons
    metrics["stopped_by_completion"] = (df["current_state"] == "completed").sum()
    metrics["stopped_by_max_retries"] = (df["current_state"] == "closed").sum()

    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(OUTPUT_FILE, index=False)

    print(" Metrics generated successfully 🚀")
    print(metrics_df)


if __name__ == "__main__":
    generate_metrics()
