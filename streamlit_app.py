# streamlit_app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Business Value Architect Jobs", layout="wide")
st.title("💼 Real-Time Business Value Architect Job Tracker")

# User filters
location = st.text_input("Location (optional):", "")

# Build query
role = "Business Value Architect"
query = role.replace(" ", "+")
base_url = f"https://www.indeed.com/jobs?q={query}&l={location}"

# Scraper
def scrape_indeed_jobs(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    jobs = []
    for div in soup.find_all(name="div", attrs={"class": "job_seen_beacon"}):
        title = div.find("h2").text.strip() if div.find("h2") else "N/A"
        company = div.find("span", class_="companyName").text.strip() if div.find("span", class_="companyName") else "N/A"
        location = div.find("div", class_="companyLocation").text.strip() if div.find("div", class_="companyLocation") else "N/A"
        link = div.find("a", href=True)
        job_url = f"https://www.indeed.com{link['href']}" if link else ""

        jobs.append({
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Link": job_url
        })

    return pd.DataFrame(jobs)

# Run
with st.spinner("Fetching jobs from Indeed..."):
    jobs_df = scrape_indeed_jobs(base_url)

if not jobs_df.empty:
    st.success(f"Found {len(jobs_df)} jobs")
    st.dataframe(jobs_df, use_container_width=True)
else:
    st.warning("No jobs found. Try changing location or retry later.")
