import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache_data
def load_data():
    countries = ['Benin', 'Togo', 'Sierra Leone']
    data = []
    for country in countries:
        for _ in range(3000):
            data.append({
                'Country': country,
                'GHI': np.random.normal(220, 80),
                'DNI': np.random.normal(150, 100),
                'DHI': np.random.normal(110, 70)
            })
    return pd.DataFrame(data)

df = load_data()

# Sidebar - Filters
st.sidebar.header("🔍 Filter Options")
countries = st.sidebar.multiselect("Choose Countries", df["Country"].unique(), default=["Benin", "Togo", "Sierra Leone"])
metric = st.sidebar.selectbox("Select Metric for Boxplot", ["GHI", "DNI", "DHI"])
sample_size = st.sidebar.slider("Sample Size for Charts", 100, 3000, 1000)

# Main Title
st.markdown("## ☀️ Solar Insight Dashboard")
st.markdown("Explore solar radiation and climate metrics across selected West African countries.")

# Summary Statistics
st.markdown("### 📊 Summary Table")

summary = df[df["Country"].isin(countries)].groupby("Country").agg(
    {
        "GHI": ["mean", "std", "median"],
        "DNI": ["mean", "std", "median"],
        "DHI": ["mean", "std", "median"]
    }
).round(2)

summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
summary.reset_index(inplace=True)

st.dataframe(summary, use_container_width=True)

# Boxplot Chart
st.markdown(f"### 📦 Distribution of {metric} by Country")

box_data = df[df["Country"].isin(countries)].sample(sample_size)

box_chart = alt.Chart(box_data).mark_boxplot(extent='min-max').encode(
    x=alt.X('Country:N', title="Country"),
    y=alt.Y(f'{metric}:Q', title=metric),
    color='Country:N'
).properties(
    width=700,
    height=400
)

st.altair_chart(box_chart, use_container_width=True)
