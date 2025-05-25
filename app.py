import streamlit as st
import pandas as pd
import altair as alt

# Load data from local CSV files in the 'data' folder
@st.cache_data
def load_data():
    benin = pd.read_csv('data/benin_clean.csv')
    sierra_leone = pd.read_csv('data/sierra_leone_clean.csv')
    togo = pd.read_csv('data/togo_clean.csv')

    # Add a Country column to each dataframe
    benin['Country'] = 'Benin'
    sierra_leone['Country'] = 'Sierra Leone'
    togo['Country'] = 'Togo'

    # Combine all dataframes into one
    df = pd.concat([benin, sierra_leone, togo], ignore_index=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
countries = st.sidebar.multiselect(
    "Choose Countries", 
    options=df["Country"].unique(), 
    default=df["Country"].unique()
)
metric = st.sidebar.selectbox(
    "Select Metric for Boxplot", 
    options=["GHI", "DNI", "DHI"]
)
sample_size = st.sidebar.slider(
    "Sample Size for Charts", 100, min(3000, len(df)), 1000
)

# Main title and description
st.markdown("## ☀️ Solar Insight Dashboard")
st.markdown("Explore solar radiation and climate metrics across selected West African countries.")

# Summary statistics table
st.markdown("### 📊 Summary Table")

summary = df[df["Country"].isin(countries)].groupby("Country").agg({
    "GHI": ["mean", "std", "median"],
    "DNI": ["mean", "std", "median"],
    "DHI": ["mean", "std", "median"]
}).round(2)

summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
summary.reset_index(inplace=True)

st.dataframe(summary, use_container_width=True)

# Boxplot chart
st.markdown(f"### 📦 Distribution of {metric} by Country")

box_data = df[df["Country"].isin(countries)]

# If sample size is larger than data, just use all rows
if sample_size < len(box_data):
    box_data = box_data.sample(sample_size, random_state=42)

box_chart = alt.Chart(box_data).mark_boxplot(extent='min-max').encode(
    x=alt.X('Country:N', title="Country"),
    y=alt.Y(f'{metric}:Q', title=metric),
    color='Country:N'
).properties(
    width=700,
    height=400
)

st.altair_chart(box_chart, use_container_width=True)
