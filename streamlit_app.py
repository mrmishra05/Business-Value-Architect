import requests
import pandas as pd
import time
from datetime import datetime
import streamlit as st
import threading
import json
import re
from bs4 import BeautifulSoup
import random
from urllib.parse import urlencode, quote_plus

class JobScraper:
    def __init__(self):
        self.job_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def extract_salary(self, salary_text):
        """Extract salary range from text"""
        if not salary_text:
            return "Not specified"
        
        # Common salary patterns
        patterns = [
            r'[\$£€][\d,]+(?:\s*-\s*[\$£€][\d,]+)?(?:\s*(?:per year|annually|pa|k|K))?',
            r'[\d,]+\s*-\s*[\d,]+\s*(?:USD|GBP|EUR|INR|k|K)',
            r'[\d,]+\s*(?:USD|GBP|EUR|INR|k|K)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, salary_text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return "Not specified"
    
    def extract_experience(self, job_description):
        """Extract experience requirements from job description"""
        if not job_description:
            return "Not specified"
        
        # Experience patterns
        patterns = [
            r'(\d+)\s*(?:-\s*\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+\s*(?:years?|yrs?)',
            r'minimum\s*(\d+)\s*(?:years?|yrs?)',
            r'at least\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return f"{match.group(1)}+ years"
        
        # Check for entry level keywords
        entry_keywords = ['entry level', 'junior', 'graduate', 'trainee', 'intern']
        for keyword in entry_keywords:
            if keyword in job_description.lower():
                return "Entry level"
        
        return "Not specified"
    
    def scrape_jobs_api(self, job_title, location=""):
        """Scrape jobs using multiple APIs and sources"""
        jobs = []
        
        # Simulate API calls with sample data (replace with actual API calls)
        sample_jobs = [
            {
                'title': f'{job_title} - Senior',
                'company': 'TechCorp Solutions',
                'location': 'San Francisco, CA, USA',
                'region': 'North America',
                'salary': '$120,000 - $150,000',
                'experience': '5+ years',
                'description': 'Leading cloud infrastructure and DevOps practices...',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': f'{job_title} - Mid-Level',
                'company': 'Global Tech Ltd',
                'location': 'London, UK',
                'region': 'Europe',
                'salary': '£70,000 - £85,000',
                'experience': '3+ years',
                'description': 'Architecting business solutions and driving digital transformation...',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': f'{job_title} - Lead',
                'company': 'Innovation Hub',
                'location': 'Sydney, Australia',
                'region': 'Asia-Pacific',
                'salary': 'AUD 140,000 - AUD 160,000',
                'experience': '7+ years',
                'description': 'Leading DevOps transformation and cloud migration projects...',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': f'{job_title} - Senior',
                'company': 'Tech Innovators',
                'location': 'Toronto, Canada',
                'region': 'North America',
                'salary': 'CAD 110,000 - CAD 130,000',
                'experience': '4+ years',
                'description': 'Driving business value through technology architecture...',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': f'{job_title} - Principal',
                'company': 'Digital Solutions AG',
                'location': 'Zurich, Switzerland',
                'region': 'Europe',
                'salary': 'CHF 150,000 - CHF 180,000',
                'experience': '8+ years',
                'description': 'Leading enterprise architecture and DevOps strategy...',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': f'{job_title} - Senior',
                'company': 'Tech Bangalore',
                'location': 'Bangalore, India',
                'region': 'Asia',
                'salary': '₹25,00,000 - ₹35,00,000',
                'experience': '6+ years',
                'description': 'Architecting scalable solutions and managing DevOps pipelines...',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        # Add some randomization to simulate real-time updates
        selected_jobs = random.sample(sample_jobs, random.randint(3, len(sample_jobs)))
        
        for job in selected_jobs:
            jobs.append({
                'Job Title': job['title'],
                'Company': job['company'],
                'Location': job['location'],
                'Region': job['region'],
                'Salary': job['salary'],
                'Experience': job['experience'],
                'Posted Date': job['posted_date'],
                'Description': job['description'][:200] + "..." if len(job['description']) > 200 else job['description']
            })
        
        return jobs
    
    def fetch_all_jobs(self):
        """Fetch jobs for both roles"""
        all_jobs = []
        
        # Fetch Business Value Architect jobs
        bva_jobs = self.scrape_jobs_api("Business Value Architect")
        all_jobs.extend(bva_jobs)
        
        # Fetch DevOps jobs
        devops_jobs = self.scrape_jobs_api("DevOps Engineer")
        all_jobs.extend(devops_jobs)
        
        return all_jobs

def main():
    st.set_page_config(
        page_title="Job Monitoring Dashboard",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🚀 Real-Time Job Monitoring Dashboard")
    st.markdown("### Business Value Architect & DevOps Roles")
    
    # Initialize session state
    if 'job_data' not in st.session_state:
        st.session_state.job_data = []
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto Refresh", value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto_refresh
    
    # Refresh interval
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 30)
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.session_state.job_data = []
        st.rerun()
    
    # Filter options
    st.sidebar.header("Filters")
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Fetch jobs if data is empty or auto-refresh is enabled
    if not st.session_state.job_data or (auto_refresh and 
        (datetime.now() - st.session_state.last_update).seconds > refresh_interval):
        
        with st.spinner("🔍 Fetching latest job postings..."):
            st.session_state.job_data = scraper.fetch_all_jobs()
            st.session_state.last_update = datetime.now()
    
    # Display last update time
    st.sidebar.info(f"Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    # Convert to DataFrame
    if st.session_state.job_data:
        df = pd.DataFrame(st.session_state.job_data)
        
        # Sidebar filters
        regions = st.sidebar.multiselect(
            "Select Regions",
            options=df['Region'].unique(),
            default=df['Region'].unique()
        )
        
        job_titles = st.sidebar.multiselect(
            "Select Job Types",
            options=df['Job Title'].unique(),
            default=df['Job Title'].unique()
        )
        
        # Apply filters
        filtered_df = df[
            (df['Region'].isin(regions)) &
            (df['Job Title'].isin(job_titles))
        ]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", len(filtered_df))
        
        with col2:
            st.metric("Regions", len(filtered_df['Region'].unique()))
        
        with col3:
            st.metric("Companies", len(filtered_df['Company'].unique()))
        
        with col4:
            st.metric("Latest Update", f"{(datetime.now() - st.session_state.last_update).seconds}s ago")
        
        # Main data table
        st.subheader("📊 Job Listings")
        
        # Display options
        col1, col2 = st.columns([3, 1])
        with col2:
            show_description = st.checkbox("Show Descriptions", value=False)
        
        # Configure display columns
        display_columns = ['Job Title', 'Company', 'Location', 'Region', 'Salary', 'Experience', 'Posted Date']
        if show_description:
            display_columns.append('Description')
        
        # Display the table
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                'Job Title': st.column_config.TextColumn(width="medium"),
                'Company': st.column_config.TextColumn(width="medium"),
                'Location': st.column_config.TextColumn(width="medium"),
                'Region': st.column_config.TextColumn(width="small"),
                'Salary': st.column_config.TextColumn(width="medium"),
                'Experience': st.column_config.TextColumn(width="small"),
                'Posted Date': st.column_config.DateColumn(width="small"),
                'Description': st.column_config.TextColumn(width="large") if show_description else None
            }
        )
        
        # Regional distribution chart
        st.subheader("📍 Regional Distribution")
        region_counts = filtered_df['Region'].value_counts()
        st.bar_chart(region_counts)
        
        # Export functionality
        st.subheader("📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"job_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = filtered_df.to_json(orient='records', indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"job_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
    else:
        st.info("🔄 Loading job data...")
        st.empty()
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
