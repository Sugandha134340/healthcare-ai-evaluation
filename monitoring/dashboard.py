import streamlit as st

st.set_page_config(page_title="Healthcare AI Evaluation", layout="wide")
st.title("Healthcare AI Evaluation Dashboard")
st.info("Dashboard scaffold. Benchmark results will be loaded here after the evaluation pipeline is implemented.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Task Completion", "—")
c2.metric("Tool Accuracy", "—")
c3.metric("Hallucination Rate", "—")
c4.metric("p95 Latency", "—")

st.subheader("Quality Drift")
st.warning("No benchmark has been executed yet.")
