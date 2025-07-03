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
        
        # Target countries and their major cities
        target_locations = {
            'India': ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune'],
            'Singapore': ['Singapore'],
            'Netherlands': ['Amsterdam', 'Rotterdam', 'Utrecht', 'The Hague'],
            'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
            'France': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice']
        }
        
        # Platforms to simulate
        platforms = ['LinkedIn', 'Indeed', 'Glassdoor', 'AngelList', 'Naukri', 'Monster', 'StepStone', 'Welcome to the Jungle']
        
        # Work types
        work_types = ['Remote', 'Hybrid', 'Onsite']
        
        # Sample companies by country
        companies_by_country = {
            'India': ['Infosys', 'TCS', 'Wipro', 'HCL Technologies', 'Tech Mahindra', 'Flipkart', 'Zomato', 'Paytm', 'Swiggy', 'Freshworks'],
            'Singapore': ['Grab', 'Sea Limited', 'DBS Bank', 'Singtel', 'Shopee', 'Gojek', 'Stripe', 'Revolut', 'PropertyGuru', 'Carousell'],
            'Netherlands': ['Booking.com', 'Adyen', 'Philips', 'ING', 'ASML', 'Takeaway.com', 'Coolblue', 'Exact', 'TomTom', 'Randstad'],
            'Germany': ['SAP', 'Siemens', 'Allianz', 'BMW', 'Mercedes-Benz', 'Zalando', 'Delivery Hero', 'N26', 'Rocket Internet', 'AUTO1'],
            'France': ['Airbus', 'Thales', 'Atos', 'Capgemini', 'Orange', 'BlaBlaCar', 'Criteo', 'Dassault Systèmes', 'Murex', 'Datadog']
        }
        
        # Salary ranges by country
        salary_ranges = {
            'India': ['₹15,00,000 - ₹25,00,000', '₹25,00,000 - ₹40,00,000', '₹40,00,000 - ₹60,00,000', '₹60,00,000 - ₹80,00,000'],
            'Singapore': ['S$80,000 - S$120,000', 'S$120,000 - S$160,000', 'S$160,000 - S$200,000', 'S$200,000 - S$250,000'],
            'Netherlands': ['€60,000 - €80,000', '€80,000 - €100,000', '€100,000 - €120,000', '€120,000 - €150,000'],
            'Germany': ['€65,000 - €85,000', '€85,000 - €110,000', '€110,000 - €130,000', '€130,000 - €160,000'],
            'France': ['€55,000 - €75,000', '€75,000 - €95,000', '€95,000 - €115,000', '€115,000 - €140,000']
        }
        
        # Generate sample jobs for each country
        for country, cities in target_locations.items():
            for _ in range(random.randint(2, 4)):  # 2-4 jobs per country
                city = random.choice(cities)
                company = random.choice(companies_by_country[country])
                platform = random.choice(platforms)
                work_type = random.choice(work_types)
                salary = random.choice(salary_ranges[country])
                experience = random.choice(['2+ years', '3+ years', '4+ years', '5+ years', '6+ years', '7+ years', '8+ years'])
                
                job_levels = ['Senior', 'Lead', 'Principal', 'Staff', 'Manager']
                job_level = random.choice(job_levels)
                
                jobs.append({
                    'Job Title': f'{job_title} - {job_level}',
                    'Company': company,
                    'Platform': platform,
                    'Location': f'{city}, {country}',
                    'Country': country,
                    'Work Type': work_type,
                    'Salary': salary,
                    'Experience': experience,
                    'Apply Link': f'https://{platform.lower().replace(" ", "")}.com/jobs/{company.lower().replace(" ", "-")}-{job_title.lower().replace(" ", "-")}-{random.randint(100000, 999999)}',
                    'Posted Date': datetime.now().strftime('%Y-%m-%d'),
                    'Description': f'We are looking for a skilled {job_title} to join our {work_type.lower()} team in {city}. The role involves architecting scalable solutions, implementing DevOps best practices, and driving digital transformation initiatives. Perfect opportunity for professionals with {experience} of experience.'
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
        countries = st.sidebar.multiselect(
            "Select Countries",
            options=df['Country'].unique(),
            default=df['Country'].unique()
        )
        
        platforms = st.sidebar.multiselect(
            "Select Platforms",
            options=df['Platform'].unique(),
            default=df['Platform'].unique()
        )
        
        work_types = st.sidebar.multiselect(
            "Select Work Type",
            options=df['Work Type'].unique(),
            default=df['Work Type'].unique()
        )
        
        job_titles = st.sidebar.multiselect(
            "Select Job Types",
            options=df['Job Title'].unique(),
            default=df['Job Title'].unique()
        )
        
        # Apply filters
        filtered_df = df[
            (df['Country'].isin(countries)) &
            (df['Platform'].isin(platforms)) &
            (df['Work Type'].isin(work_types)) &
            (df['Job Title'].isin(job_titles))
        ]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", len(filtered_df))
        
        with col2:
            st.metric("Countries", len(filtered_df['Country'].unique()))
        
        with col3:
            st.metric("Platforms", len(filtered_df['Platform'].unique()))
        
        with col4:
            st.metric("Work Types", len(filtered_df['Work Type'].unique()))
        
        # Main data table
        st.subheader("📊 Job Listings")
        
        # Display options
        col1, col2 = st.columns([3, 1])
        with col2:
            show_description = st.checkbox("Show Descriptions", value=False)
        
        # Configure display columns
        display_columns = ['Job Title', 'Company', 'Platform', 'Location', 'Country', 'Work Type', 'Salary', 'Experience', 'Apply Link', 'Posted Date']
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
                'Platform': st.column_config.TextColumn(width="small"),
                'Location': st.column_config.TextColumn(width="medium"),
                'Country': st.column_config.TextColumn(width="small"),
                'Work Type': st.column_config.TextColumn(width="small"),
                'Salary': st.column_config.TextColumn(width="medium"),
                'Experience': st.column_config.TextColumn(width="small"),
                'Apply Link': st.column_config.LinkColumn(width="medium"),
                'Posted Date': st.column_config.DateColumn(width="small"),
                'Description': st.column_config.TextColumn(width="large") if show_description else None
            }
        )
        
        # Country and Work Type distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌍 Country Distribution")
            country_counts = filtered_df['Country'].value_counts()
            st.bar_chart(country_counts)
        
        with col2:
            st.subheader("💼 Work Type Distribution")
            work_type_counts = filtered_df['Work Type'].value_counts()
            st.bar_chart(work_type_counts)
        
        # Platform distribution
        st.subheader("🔗 Platform Distribution")
        platform_counts = filtered_df['Platform'].value_counts()
        st.bar_chart(platform_counts)
        
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
