import sys, os
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from semantic_engine import load_data, answer_structured, group_metric, monthly_revenue, kpi

st.set_page_config(page_title="MetricMind", page_icon="🤖", layout="wide")
st.title("🤖 MetricMind")
st.caption("Governed Agentic BI — local portfolio MVP")

df = load_data(ROOT / "data" / "sales.csv")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Revenue", f"₹{kpi(df,'revenue'):,.0f}")
c2.metric("Profit", f"₹{kpi(df,'profit'):,.0f}")
c3.metric("Margin", f"{kpi(df,'margin'):.1%}")
c4.metric("Orders", f"{kpi(df,'orders'):,}")

st.divider()
question = st.text_input("Ask a business question", placeholder="e.g. Which region has the highest revenue?")
if st.button("Analyze") and question:
    result = answer_structured(question, df)
    st.subheader("Answer")
    st.write(result["answer"])
    if result["type"] == "table":
        st.dataframe(pd.DataFrame(result["data"]), use_container_width=True)
        if "Country" in result["data"][0]:
            fig = px.bar(pd.DataFrame(result["data"]), x="Country", y="revenue", title="Top Countries by Revenue")
        elif "Region" in result["data"][0]:
            fig = px.bar(pd.DataFrame(result["data"]), x="Region", y="revenue", title="Revenue by Region")
        else:
            fig = px.bar(pd.DataFrame(result["data"]), x="Product", y="revenue", title="Top Products by Revenue")
        st.plotly_chart(fig, use_container_width=True)
    elif result["type"] == "monthly":
        m = pd.DataFrame(result["data"])
        fig = px.line(m, x="Month", y="Revenue", markers=True, title="Monthly Revenue")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Quick business views")
left,right = st.columns(2)
with left:
    st.plotly_chart(px.bar(group_metric(df,"Region","revenue"), x="Region", y="revenue", title="Revenue by Region"), use_container_width=True)
with right:
    st.plotly_chart(px.bar(group_metric(df,"Product","profit").head(8), x="Product", y="profit", title="Profit by Product"), use_container_width=True)

st.info("Architecture: User → Agent/Question Router → Governed Semantic Layer → Data → Insight. This MVP uses a local governed semantic engine; an LLM and Cube/dbt can be connected in the next production-hardening step.")
