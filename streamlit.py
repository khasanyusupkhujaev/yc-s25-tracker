import streamlit as st
import pandas as pd

st.set_page_config(page_title="YC S25 Companies Tracker", layout="wide")

st.title("🚀 YC S25 Companies Tracker")

from datetime import datetime

def format_unix_timestamp(ts):
    try:
        ts = float(ts)
        if pd.notna(ts) and ts > 0:
            return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
    except:
        return "N/A"
    return "N/A"

@st.cache_data
def load_data():
    try:
        enriched = pd.read_csv("yc_s25_companies_enriched.csv", encoding="utf-8")
    except UnicodeDecodeError:
        enriched = pd.read_csv("yc_s25_companies_enriched.csv", encoding="latin1")
    try:
        yc_data = pd.read_csv("yc_s25_companies.csv", encoding="utf-8")
    except UnicodeDecodeError:
        yc_data = pd.read_csv("yc_s25_companies.csv", encoding="latin1")

    df = pd.merge(enriched, yc_data, how="left", left_on="YC Company", right_on="company_name")
    return df

df = load_data()

company_param = st.query_params.get("company", None)

if company_param:
    # DETAIL PAGE
    st.sidebar.markdown("[⬅ Back to Directory](?)")
    company_data = df[df["YC Company"] == company_param].iloc[0]

    if pd.notna(company_data.get("small_logo_thumb_url")):
        st.image(company_data["small_logo_thumb_url"], width=120)

    st.header(f"📌 {company_data['YC Company']}")

    col1, col2 = st.columns(2)
    with col1:
        if pd.notna(company_data.get("Website")):
            st.markdown(f"[🌐 Website]({company_data['Website']})", unsafe_allow_html=True)
        if pd.notna(company_data.get("yc_page")):
            st.markdown(f"[🏢 YC Page]({company_data['yc_page']})", unsafe_allow_html=True)
    with col2:
        if pd.notna(company_data.get("LinkedIn Page")) and company_data["LinkedIn Page"]:
            st.markdown(f"[💼 LinkedIn]({company_data['LinkedIn Page']})", unsafe_allow_html=True)

    st.info(f"**Mentions YC S25:** {'✅ Yes' if company_data['Mentions YC S25'] else '❌ No'}")

    st.subheader("📖 Company Details")
    details = {
        "🌍 Location": company_data.get("all_locations", "N/A"),
        "📝 Short Description": company_data.get("Description (YC)", "N/A"),
        "📜 Long Description": company_data.get("long_description", "N/A"),
        "👥 Team Size": company_data.get("team_size", "N/A"),
        "🏭 Industry": company_data.get("industry", "N/A"),
        "🚀 Launched At": format_unix_timestamp(company_data.get("launched_at")),
        "🏷️ Tags": company_data.get("tags", "N/A"),
        "🌎 Regions": company_data.get("regions", "N/A"),
        "📈 Stage": company_data.get("stage", "N/A"),
        "🔗 YC Profile URL": company_data.get("yc_page", "N/A"),
    }

    for key, value in details.items():
        st.write(f"**{key}:** {value}")

else:
    st.sidebar.header("Filters")
    only_yc_s25 = st.sidebar.checkbox("Show only companies mentioning YC S25", value=False)
    search_query = st.sidebar.text_input("Search by company name")

    df_display = df.copy()

    if only_yc_s25:
        df_display = df_display[df_display["Mentions YC S25"] == True]

    if search_query:
        df_display = df_display[df_display["YC Company"].str.contains(search_query, case=False, na=False)]

    st.subheader("Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Companies", len(df_display))
    col2.metric("YC S25 Mentions", int(df_display["Mentions YC S25"].sum()))

    def make_clickable(link, text):
        if pd.isna(link) or link == "":
            return ""
        return f'<a href="{link}" target="_blank">{text}</a>'

    df_display["Website"] = df_display.apply(
        lambda x: make_clickable(x.get("Website",""), "Website"), axis=1)
    df_display["YC Page"] = df_display.apply(
        lambda x: make_clickable(x.get("yc_page",""), "YC Page"), axis=1)
    df_display["LinkedIn Page"] = df_display.apply(
        lambda x: make_clickable(x.get("LinkedIn Page",""), "LinkedIn"), axis=1)

    df_display["More Information"] = df_display["YC Company"].apply(
        lambda name: f'<a href="?company={name}">ℹ️ More Info</a>'
    )

    columns_to_show = [
        "YC Company",
        "Website",
        "Description (YC)",
        "yc_page",
        "LinkedIn Page",
        "Mentions YC S25",
        "More Information"
    ]
    df_display = df_display[columns_to_show]

    st.subheader("Company Directory")
    st.write(
        df_display.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
