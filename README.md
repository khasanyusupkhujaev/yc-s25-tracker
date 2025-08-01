# YC S25 Companies Tracker

A Streamlit app that tracks and displays startups from the **Y Combinator Summer 2025 (S25) batch**.  
The app collects official YC data, enriches company profiles with LinkedIn information, and provides an interactive dashboard for exploration.

---

## Features

- **Official YC Directory Integration**  
  Fetches the full list of S25 companies via the YC OSS API.

- **LinkedIn Enrichment**  
  Uses Google search results (via Serper.dev API) to find LinkedIn company pages.  
  Flags companies that explicitly mention **“YC S25”** in their LinkedIn title or description — including those *not listed* on the official YC directory.

- **Interactive Dashboard**  
  Powered by [Streamlit](https://streamlit.io) with:
  - Search by company name  
  - Filter for companies mentioning YC S25  
  - Metrics: total companies & YC S25 mentions  
  - Clickable links to websites, YC pages, and LinkedIn profiles  

- **Data Deduplication**  
  Ensures no duplicate companies are displayed.

---

## Tech Stack

- [Python 3](https://www.python.org/)  
- [Requests](https://docs.python-requests.org/) — fetch YC data & search results  
- [Pandas](https://pandas.pydata.org/) — data handling  
- [Streamlit](https://streamlit.io/) — dashboard framework  
- [Serper.dev API](https://serper.dev/) — Google search API  

---

## Project Structure

yc_scraper.py # Step 1: Scrape YC OSS API (S25 batch)
linkedin_finder.py # Step 2: Enrich with LinkedIn mentions
app.py # Step 3: Streamlit dashboard
yc_s25_companies.csv # Output of yc_scraper.py
yc_s25_companies_enriched.csv # Output of linkedin_finder.py
README.md

This project is deployed on Streamlit Community Cloud.
You can access the live version here:
https://ycs25scraper.streamlit.app/

