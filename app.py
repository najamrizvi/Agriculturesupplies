import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="Agricultural Analytics Dashboard",
    page_icon="🌾",
    layout="wide"
)

# --------------------------------
# GLOBAL BACKGROUND & THEME STYLING
# --------------------------------
st.markdown("""
<style>
/* Full app background */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
}

/* Main content container */
.block-container {
    padding-top: 1.5rem;
}

/* Header styling */
.dashboard-header {
    background: linear-gradient(90deg, #020617, #1e293b);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
}

/* Title text */
.dashboard-title {
    color: #f8fafc;
    font-size: 40px;
    font-weight: 700;
}

/* Subtitle text */
.dashboard-subtitle {
    color: #cbd5f5;
    font-size: 18px;
}

/* Section headers */
.section-header {
    color: #e5e7eb;
    font-size: 26px;
    font-weight: 600;
    margin-top: 30px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background-color: #020617;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.35);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Load Data
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sorghum_annual_supply_disappearance.csv")

    df["year"] = df["marketing_year"].str[:4].astype(int)

    for col in df.columns:
        if col not in ["marketing_year", "period"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# --------------------------------
# Sidebar Filters
# --------------------------------
st.sidebar.title("🔎 Dashboard Filters")

year_range = st.sidebar.slider(
    "Select Marketing Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

numeric_columns = df.select_dtypes(include="number").columns.tolist()
metric = st.sidebar.selectbox("Select Metric", numeric_columns, index=1)

filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# --------------------------------
# DASHBOARD HEADER
# --------------------------------
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">🌾 Agricultural Supply & Utilization Dashboard</div>
    <div class="dashboard-subtitle">
        Interactive visualization of production, trade, and stock trends across marketing years
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# KPIs
# --------------------------------
st.markdown('<div class="section-header">📌 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="kpi-card kpi-average">', unsafe_allow_html=True)
    st.metric("Average Value", f"{filtered_df[metric].mean():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kpi-card kpi-maximum">', unsafe_allow_html=True)
    st.metric("Maximum Value", f"{filtered_df[metric].max():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="kpi-card kpi-minimum">', unsafe_allow_html=True)
    st.metric("Minimum Value", f"{filtered_df[metric].min():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# Trend Analysis
# --------------------------------
st.markdown('<div class="section-header">📈 Trend Analysis</div>', unsafe_allow_html=True)

line_fig = px.line(
    filtered_df,
    x="year",
    y=metric,
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(line_fig, use_container_width=True)

# --------------------------------
# Distribution Analysis
# --------------------------------
st.markdown('<div class="section-header">📊 Distribution Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Histogram")
    hist_fig = px.histogram(
        filtered_df,
        x=metric,
        nbins=30,
        template="plotly_dark"
    )
    st.plotly_chart(hist_fig, use_container_width=True)

with col2:
    st.subheader("Box Plot")
    box_fig = px.box(
        filtered_df,
        y=metric,
        template="plotly_dark"
    )
    st.plotly_chart(box_fig, use_container_width=True)

# --------------------------------
# Composition Analysis
# --------------------------------
st.markdown('<div class="section-header">🥧 Composition Analysis (Latest Year)</div>', unsafe_allow_html=True)

latest_year = filtered_df["year"].max()
latest_data = filtered_df[filtered_df["year"] == latest_year]

pie_cols = ["production", "imports", "exports", "ending_stocks"]

pie_data = latest_data[pie_cols].T.reset_index()
pie_data.columns = ["Category", "Value"]

pie_fig = px.pie(
    pie_data,
    names="Category",
    values="Value",
    hole=0.4,
    template="plotly_dark"
)

st.plotly_chart(pie_fig, use_container_width=True)

# --------------------------------
# Data Table
# --------------------------------
st.markdown('<div class="section-header">📄 Data Preview</div>', unsafe_allow_html=True)

with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
