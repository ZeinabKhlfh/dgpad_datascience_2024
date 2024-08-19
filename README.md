Web Article Scraper

# Overview
The Web Article Scraper is a Python-based tool designed to automatically fetch and store articles from a specified website's sitemap. 
It systematically navigates through sitemap URLs, extracts article links, and retrieves comprehensive information about each article, including metadata and content. 
The collected data is then organized and saved in JSON format for easy access and analysis.

#Features
1) Automated Sitemap Navigation: Parses the main sitemap to retrieve all available sitemap links and subsequently all article links within them.
2) Detailed Article Extraction: For each article link, it extracts metadata such as headline, tags, publication date, author, and the full text content.
3) Structured Data Storage: Saves the extracted articles in a structured JSON format, organized by publication year and month.
4) Error Handling: Includes exception handling to manage and log errors during the fetching and parsing processes.

#Prerequisites 
Before running the Web Article Scraper, ensure that you have the following installed on your system:
  Python 3.7 or higher
  pip (Python package installer)

#Installation
Follow these steps to set up the environment and install the necessary dependencies:
1) Clone the Repository
   git clone https://github.com/yourusername/web-article-scraper.git
cd web-article-scraper

2) Create a Virtual Environment (Optional but Recommended)
   python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3) Install Dependencies
Install the required Python packages using pip:
pip install -r requirements.txt
  requirements.txt:
requests
beautifulsoup4
lxml
dataclasses; python_version < '3.7'
Usage
To run the Web Article Scraper, execute the following command in your terminal:
python scraper.py

#Configuration
The scraper comes with default settings, but you can adjust the following parameters as needed:
max_articles: The maximum number of articles to fetch. Default is set to 10,000.
max_articles = 10000
index_url: The URL of the main sitemap index. By default, it is set to https://www.almayadeen.net/sitemaps/all.xml.

#Output 
The scraped articles are saved in JSON format within the web_articles directory in the project's root folder. 
The files are named based on the publication year and month of the articles they contain, following this pattern:
web_articles/web_articles_<year>_<month>.json
web_articles/web_articles_2024_08.json
Each JSON file contains a list of articles with the following structure:
[
    {
        "link": "https://example.com/article-link",
        "article_id": "12345",
        "headline": "Article Headline",
        "tags": ["tag1", "tag2"],
        "image_link": "https://example.com/image.jpg",
        "duration": "5 min read",
        "text_length": 1500,
        "language": "en",
        "date_published": "2023-08-19T12:00:00Z",
        "date_modified": "2023-08-19T13:00:00Z",
        "summary": "This is a summary of the article.",
        "writer": "Author Name",
        "categories": ["Category1", "Category2"],
        "body_text": "Full article text..."
    },
    ...
]
#Logging and Error Handling
The scraper includes basic logging to the console to inform you about its progress, including:
1) Current sitemap being processed.
2) Number of article links retrieved from each sitemap.
3) Success or failure of individual article fetch operations.
   Errors encountered during the fetching and parsing processes are caught and printed to the console without stopping the execution of the script.
    This ensures that one failed operation does not halt the entire scraping process.

  #Extending and Customizing
   You can extend and customize the scraper to fit specific needs:
1) Supporting Additional Metadata: Modify the ArticleFetcher class to extract more metadata fields as required.
2) Changing Output Format: Adjust the save_articles function to save data in different formats such as CSV or XML.
3) Implementing Advanced Logging: Integrate Python's logging module to create detailed logs and possibly log files.
4) Adding Proxy Support: Modify the fetch_web_content function to route requests through proxies for enhanced anonymity or to bypass restrictions.

#Limitations
1) Website Structure Dependency: The scraper relies on the specific HTML and sitemap structure of https://www.almayadeen.net.
    Changes to the website's structure may require corresponding updates to the scraper.
2) Network Reliability: The scraping process depends on network stability. Network issues can lead to failed requests.
3) Legal Considerations: Ensure compliance with the website's terms of service and robots.txt file when scraping data.

#License
This project is licensed under the MIT License.

#Author
Zeinab Hasan Khalifee
  Email: zeinabkhalifee789@gmail.com
  GITHUB: https://github.com/ZeinabKhlfh
  
   



