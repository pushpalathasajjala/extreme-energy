import streamlit as st
import pandas as pd
import altair as alt

# Load Data
df = pd.read_excel("forecast_results_2024_2029.xlsx")

st.set_page_config(page_title="Forecast Dashboard", layout="wide")

st.title("📊 Forecast Dashboard (2024–2029)")

# ----------------- SIDEBAR FILTERS -----------------
with st.sidebar:
    st.header("🔍 Filters")

    category_filter = st.multiselect("Select Category", df["Category"].unique())
    country_filter  = st.multiselect("Select Country", df["Country"].unique())
    year_filter     = st.multiselect("Select Year", df["Year"].unique())

# ----------------- APPLY FILTERS -----------------
filtered_df = df[
    ((df["Category"].isin(category_filter)) if category_filter else True) &
    ((df["Country"].isin(country_filter))  if country_filter else True) &
    ((df["Year"].isin(year_filter))        if year_filter else True)
]

st.subheader("📄 Filtered Dataset")
st.dataframe(filtered_df, use_container_width=True)

# ----------------- LINE CHART: FORECAST TREND -----------------
st.subheader("📈 Forecast Trend Over Years")

line_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x="Year:O",
    y="Predicted:Q",
    color="Category:N",
    tooltip=["Category", "Country", "Year", "Predicted"]
).interactive()

st.altair_chart(line_chart, use_container_width=True)

# ----------------- BAR CHART: GROWTH -----------------
st.subheader("📊 Growth by Year")

bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Year:O",
    y="Growth:Q",
    color="Country:N",
    tooltip=["Category", "Country", "Year", "Growth"]
).interactive()

st.altair_chart(bar_chart, use_container_width=True)

# ----------------- DATA DOWNLOAD OPTION -----------------
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="forecast_filtered_data.csv",
    mime="text/csv"
)

st.success("Dashboard Loaded Successfully") 

