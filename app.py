import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAIError
import os
import time


# Streamlit Page Configuration
st.set_page_config(page_title="AI Agent", layout="wide")

# OpenAI API Key
openai.api_key = "openapi key"
# ScraperAPI Key
scraperapi_key = "sccrsperapi key"
scraperapi_url = "http://api.scraperapi.com/"

# Function to load CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found. Default styles will be applied.")

# Call the CSS loader
load_css("styles.css")

# Title
st.title("AI Agent: Web Search & Data Extraction")

# File Upload Section
uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head())
    # Allow user to select a column for querying
    selected_column = st.selectbox("Select the main column for queries", df.columns)

# Google Sheets Integration
credentials_file = st.file_uploader("Upload your Google Sheets credentials JSON", type=["json"])
sheet_id = st.text_input("Enter Google Sheet ID")
range_name = st.text_input("Enter Data Range (e.g., Sheet1!A1:C100)")

def authenticate_google_sheets(credentials_file):
    creds = Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_google_sheet_data(service, sheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    return pd.DataFrame(values[1:], columns=values[0])  # Assuming first row is the header

if credentials_file and sheet_id and range_name:
    service = authenticate_google_sheets(credentials_file)
    sheet_data = get_google_sheet_data(service, sheet_id, range_name)
    st.write("Google Sheet Data Preview:", sheet_data.head())

# Query Input Section
query_template = st.text_input("Enter your query template", value="Get the email address of {company}")

# Perform Search Using ScraperAPI with Error Handling
def fetch_url_content(url):
    params = {
        'api_key': scraperapi_key,
        'url': url
    }
    try:
        response = requests.get(scraperapi_url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL content: {e}")
        return None

def search_google(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    html_content = fetch_url_content(search_url)
    if html_content:
        return extract_google_results(html_content)
    else:
        return []

def extract_google_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    for item in soup.find_all('div', class_='g'):  # Adjust if the structure changes
        title = item.find('h3')
        link = item.find('a', href=True)
        snippet = item.find('span', class_='aCOpRe')
        if title and link and snippet:
            results.append({
                'title': title.get_text(),
                'url': link['href'],
                'snippet': snippet.get_text()
            })
    return results

# GPT Information Extraction with Error Handling
def extract_information(results, prompt):
    full_prompt = f"{prompt}\nSearch Results: {results}"
    try:
        formatted_results = "\n".join([f"{result['title']} - {result['url']} - {result['snippet']}" for result in results])
        full_prompt = f"{prompt}\nSearch Results:\n{formatted_results}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=full_prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except openai.OpenAIError as e:
        return f"Error extracting information: {e}"

# Processing Uploaded Data or Google Sheets Data
data_source = "uploaded_file" if uploaded_file else "google_sheet" if credentials_file and sheet_id else None

if data_source:
    if data_source == "uploaded_file":
        data = df
    elif data_source == "google_sheet":
        data = sheet_data

    if data is not None:
        query_results = []
        for _, row in data.iterrows():
            entity = row[selected_column]  # Selected column from the dropdown
            query = query_template.format(company=entity)
            search_results = search_google(query)
            extracted_info = extract_information(search_results, query_template)
            query_results.append({
                'Entity': entity,
                'Query': query,
                'Extracted Info': extracted_info
            })

        # Convert to DataFrame
        results_df = pd.DataFrame(query_results)
        st.write("Extracted Results:", results_df)

        # Download Results as CSV
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="extracted_results.csv",
            mime="text/csv"
        )

        # Write Back to Google Sheet (if connected)
        if credentials_file and sheet_id:
            try:
                sheet = service.spreadsheets()
                body = {
                    'values': results_df.values.tolist()
                }
                sheet.values().append(
                    spreadsheetId=sheet_id,
                    range="Sheet1",
                    valueInputOption="RAW",
                    body=body
                ).execute()
                st.success("Results written back to Google Sheet successfully!")
            except Exception as e:
                st.error(f"Error writing back to Google Sheet: {e}")

# Welcome Message
st.markdown("🚀 Welcome to the AI Agent App!")
if st.button("Click to Get Started"):
    st.write("Let's go!")

# Spinner Simulation
with st.spinner('Processing your query...'):
    time.sleep(2)
    st.success('Done!')
