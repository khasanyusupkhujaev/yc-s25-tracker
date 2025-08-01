import requests
import pandas as pd

url = "https://yc-oss.github.io/api/batches/summer-2025.json"
try:
    response = requests.get(url)
    response.raise_for_status()
    companies = response.json()
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

# Load into DataFrame
df = pd.DataFrame(companies)

# Rename columns to match task requirements
df = df.rename(columns={
    "name": "company_name",
    "one_liner": "description",
    "website": "website"
})

# Add YC profile link
if "slug" in df.columns:
    df["yc_page"] = "https://www.ycombinator.com/companies/" + df["slug"]
else:
    df["yc_page"] = ""

# Save to CSV
df.to_csv("yc_s25_companies.csv", index=False)
print(f"Saved {len(df)} companies to yc_s25_companies.csv")