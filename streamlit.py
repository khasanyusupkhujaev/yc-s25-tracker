import streamlit as st
import pandas as pd

st.set_page_config(page_title="YC S25 Companies Tracker", layout="wide")

st.title("🚀 YC S25 Companies Tracker")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("yc_s25_companies_enriched.csv", encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv("yc_s25_companies_enriched.csv", encoding="latin1")

df = load_data()

st.sidebar.header("Filters")
only_yc_s25 = st.sidebar.checkbox("Show only companies mentioning YC S25", value=False)

if only_yc_s25:
    df = df[df["Mentions YC S25"] == True]

search_query = st.sidebar.text_input("Search by company name")
if search_query:
    df = df[df["YC Company"].str.contains(search_query, case=False, na=False)]

st.subheader("Summary")
col1, col2 = st.columns(2)
col1.metric("Total Companies", len(df))
col2.metric("YC S25 Mentions", int(df["Mentions YC S25"].sum()))

st.subheader("Company Directory")

def make_clickable(link, text):
    if pd.isna(link) or link == "":
        return ""
    return f'<a href="{link}" target="_blank">{text}</a>'

df_display = df.copy()

df_display["Website"] = df_display.apply(
    lambda x: make_clickable(x.get("Website",""), "Website"), axis=1)
df_display["YC Page"] = df_display.apply(
    lambda x: make_clickable(x.get("YC Page",""), "YC Page"), axis=1)
df_display["LinkedIn Page"] = df_display.apply(
    lambda x: make_clickable(x.get("LinkedIn Page",""), "LinkedIn"), axis=1)

columns_to_show = [
    "YC Company",
    "Website",
    "Description (YC)",
    "YC Page",          
    "LinkedIn Page",
    "Mentions YC S25"
]

df_display = df_display[columns_to_show]

st.write(
    df_display.to_html(escape=False, index=False),
    unsafe_allow_html=True
)
