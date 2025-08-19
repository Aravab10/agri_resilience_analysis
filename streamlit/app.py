import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Agri-Resilience Explorer", layout="wide")

st.title("Agri-Resilience Explorer (Starter)")
st.markdown("Visualize cropland change and precipitation deltas at county level.")

data_path = st.text_input("Path to metrics CSV", "../data/processed/metrics.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    county_col = st.selectbox("County column", options=[c for c in df.columns if "NAME" in c or "county" in c.lower()], index=0 if "NAME" in df.columns else 0)
    cols = [c for c in df.columns if c not in (county_col,)]
    metric = st.selectbox("Metric", options=[c for c in cols if df[c].dtype != 'object'])
    st.write(f"Showing metric: **{metric}**")

    fig = px.histogram(df, x=metric)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df[[county_col, metric]].sort_values(metric, ascending=False).head(25))
else:
    st.info("Provide a valid path to the processed metrics CSV to begin.")
