
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE
st.set_page_config(
    page_title="India Unemployment Analytics",
    page_icon="📊",
    layout="wide"
)

# UI
st.markdown("""
<style>
.main {
    background-color: #F5F7FA;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

h1, h2, h3 {
    color: #1F2937;
}
</style>
""", unsafe_allow_html=True)

# LOAD DATA
df = pd.read_csv("Unemployment in India.csv")

df.columns = df.columns.str.strip()

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

rate = "Estimated Unemployment Rate (%)"
employed = "Estimated Employed"
labour = "Estimated Labour Participation Rate (%)"

# HEADER
st.title("📊 India Unemployment Analytics")
st.caption("Interactive Data Analytics Dashboard | India")

st.divider()

# SIDEBAR
st.sidebar.header("🔎 Dashboard Filters")

# Region
regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

filtered = df[df["Region"].isin(selected_regions)].copy()

# Area
areas = sorted(filtered["Area"].dropna().unique())

selected_areas = st.sidebar.multiselect(
    "Select Area",
    areas,
    default=areas
)

filtered = filtered[
    filtered["Area"].isin(selected_areas)
].copy()

# Date
min_date = filtered["Date"].min().date()
max_date = filtered["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:

    start_date, end_date = date_range

    filtered = filtered[
        (filtered["Date"].dt.date >= start_date) &
        (filtered["Date"].dt.date <= end_date)
    ].copy()

# KPI CARDS
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Unemployment",
    f"{filtered[rate].mean():.2f}%"
)

c2.metric(
    "Highest Unemployment",
    f"{filtered[rate].max():.2f}%"
)

c3.metric(
    "Labour Participation",
    f"{filtered[labour].mean():.2f}%"
)

c4.metric(
    "Total Records",
    f"{len(filtered):,}"
)

st.divider()

# CHARTS
col1, col2 = st.columns(2)

with col1:

    region_avg = (
        filtered.groupby("Region")[rate]
        .mean()
        .reset_index()
        .sort_values(rate, ascending=False)
    )

    fig1 = px.bar(
        region_avg,
        x="Region",
        y=rate,
        title="Average Unemployment by Region"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    trend = (
        filtered.groupby("Date")[rate]
        .mean()
        .reset_index()
        .sort_values("Date")
    )

    fig2 = px.line(
        trend,
        x="Date",
        y=rate,
        markers=True,
        title="Unemployment Trend Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

# EMPLOYMENT
st.subheader("👥 Employment Overview")

employment = (
    filtered.groupby("Date")[employed]
    .mean()
    .reset_index()
)

fig3 = px.area(
    employment,
    x="Date",
    y=employed,
    title="Estimated Employment Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# DATA TABLE
st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered,
    use_container_width=True,
    height=400
)

# DOWNLOAD
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Data",
    csv,
    "unemployment_filtered.csv",
    "text/csv"
)
