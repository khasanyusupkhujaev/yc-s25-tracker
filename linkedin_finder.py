import requests
import pandas as pd
import time

API_KEY = "0e1e5a7afda00fa6b640dd67c0913929c1686d1b"
SEARCH_URL = "https://google.serper.dev/search"

df = pd.read_csv("yc_s25_companies.csv")
enriched = []

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

for idx, row in df.iterrows():
    company_name = row["company_name"]
    # Add "+ YC" to prioritize YC mentions in results
    query = f'site:linkedin.com/company "{company_name}" + YC'

    try:
        response = requests.post(SEARCH_URL, headers=headers, json={"q": query})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Search error for {company_name}: {e}")
        continue

    linkedin_link = ""
    linkedin_snippet = ""
    yc_s25_flag = False

    for result in data.get("organic", []):
        if "linkedin.com/company" in result.get("link", ""):
            linkedin_link = result.get("link", "")
            linkedin_snippet = result.get("snippet", "")
            title = result.get("title", "")
            if "YC S25" in (title + linkedin_snippet).upper():
                yc_s25_flag = True
            break  # only take the first relevant result

    enriched.append({
        "YC Company": company_name,
        "Website": row.get("website"),
        "Description (YC)": row.get("description") or row.get("long_description"),
        "YC Page": row.get("yc_page"),
        "LinkedIn Page": linkedin_link,
        "LinkedIn Snippet": linkedin_snippet,
        "Mentions YC S25": yc_s25_flag
    })

    print(f"[{idx+1}/{len(df)}] {company_name} -> YC S25: {yc_s25_flag}")
    time.sleep(2)  # prevent hitting API rate limits

# Save results
pd.DataFrame(enriched).to_csv("yc_s25_companies_enriched2.csv", index=False)
print("Enrichment completed and saved to yc_s25_companies_enriched.csv")



# import requests
# import pandas as pd
# import time

# API_KEY = "0e1e5a7afda00fa6b640dd67c0913929c1686d1b"
# SEARCH_URL = "https://google.serper.dev/search"

# headers = {
#     "X-API-KEY": API_KEY,
#     "Content-Type": "application/json"
# }

# all_companies = []

# # Paginate through multiple Google result pages
# for page in range(0, 5):  # adjust number of pages
#     print(f"Scraping page {page+1}...")
#     query = 'site:linkedin.com/company "YC S25"'
    
#     response = requests.post(
#         SEARCH_URL, headers=headers,
#         json={"q": query, "num": 20, "start": page * 20}
#     )
    
#     data = response.json()
#     results = data.get("organic", [])
    
#     if not results:
#         print("No more results, stopping.")
#         break
    
#     for result in results:
#         if "linkedin.com/company" in result.get("link", ""):
#             all_companies.append({
#                 "Company (LinkedIn)": result.get("title", "").replace(" | LinkedIn", ""),
#                 "LinkedIn Page": result.get("link", ""),
#                 "LinkedIn Snippet": result.get("snippet", ""),
#                 "Mentions YC S25": "YC S25" in (result.get("title","") + result.get("snippet","")).upper()
#             })
    
#     time.sleep(3)  # to avoid API rate limiting

# # Convert to DataFrame
# df_linkedin = pd.DataFrame(all_companies)

# # Remove duplicates
# df_linkedin.drop_duplicates(subset=["LinkedIn Page"], inplace=True)

# # Merge with YC CSV
# df_yc = pd.read_csv("yc_s25_companies.csv")
# df_merged = df_linkedin.merge(
#     df_yc,
#     left_on="Company (LinkedIn)", 
#     right_on="company_name",
#     how="left",
#     suffixes=("_linkedin", "_yc")
# )

# # Save both discovered and enriched YC companies
# df_merged.to_csv("yc_s25_linkedin_discovery.csv", index=False)
# print(f"Saved {len(df_merged)} companies to yc_s25_linkedin_discovery.csv")
