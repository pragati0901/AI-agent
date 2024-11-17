AI Agent for Web Search & Data Extraction
This project allows users to extract customized information from the web using automated searches and GPT-based data processing. It features an intuitive dashboard for uploading data, performing searches, and viewing extracted results.

Features:

Upload CSV Files: Users can upload CSV files for input data.
Google Sheets Integration: Fetch and update data directly from Google Sheets.
Custom Query Prompts: Define prompts dynamically for tailored information retrieval (e.g., "Find the email of {company}").
Automated Web Search: Leverage APIs like ScraperAPI to perform searches for entities in the data.
GPT-based Parsing: Extract meaningful information from search results using OpenAI's GPT API.
Results Management:
View extracted information in a structured format.
Download results as a CSV file.
Option to update connected Google Sheets with the extracted data.
Setup Instructions
Prerequisites
Python 3.8 or higher
A Google Cloud Project with a service account for Google Sheets API
API keys for:
OpenAI GPT API: For processing search results
ScraperAPI: For performing web searches
Installation
Clone the Repository:


git clone https://github.com/your-username/ai-agent-project.git
cd ai-agent-project
Install Dependencies: Install all required Python packages using:

pip install -r requirements.txt
Set Up API Keys:

Replace placeholders in the code with your OpenAI and ScraperAPI keys.
Place your credentials.json file (for Google Sheets API) in the project directory.
Run the Application: Start the Streamlit app with:


streamlit run main.py
This will open the app in your default web browser at http://localhost:8501.

Usage
Upload CSV File: Use the "Upload File" feature to load a CSV file containing the input data.
Connect to Google Sheets:
Enter the Google Sheet ID and range to fetch data.
View a preview of the imported data in the dashboard.
Select Primary Column: Choose the main column (e.g., "Company Name") for performing queries.
Define Custom Query: Use placeholders in the query (e.g., {company}) to dynamically generate prompts for each entity.
Execute Searches: Let the app perform web searches and extract data based on the query.
View and Download Results:
View results in a table format.
Download results as a CSV file or update the Google Sheet.
APIs Used
OpenAI GPT API: For parsing and extracting information from search results.
ScraperAPI: To perform automated web searches.
Google Sheets API: For real-time access and updates to Google Sheets.
Folder Structure
graphql

├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── .gitignore           # Ignored files and folders
├── credentials.json     # Google Sheets API credentials (excluded in .gitignore)
└── styles.css           # Custom styling for Streamlit app
Key Features in Action:

Dynamic Prompting: Generate prompts dynamically for each entity in the dataset.
Error Handling: Graceful error handling for failed API calls or incomplete data retrieval.
Data Download Options: Download extracted results in a CSV format or update directly to Google Sheets.

## Loom Video Walkthrough
<iframe src="https://www.loom.com/share/984418b0bf7744f1a0df598a5d873fc2?sid=f8193ced-2810-4b2a-8469-fb569add3841" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="width:100%; height:360px;"></iframe>

License

This project is licensed under the MIT License.

Acknowledgments:
OpenAI for their GPT API
ScraperAPI for efficient web scraping
Google for the Sheets API integration
