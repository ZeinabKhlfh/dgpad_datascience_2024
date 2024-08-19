from dataclasses import dataclass, field
from typing import List
import requests
from bs4 import BeautifulSoup
import json

@dataclass
class ArticleData:
    """Data class to represent the structure of an article's metadata and content."""
    url: str
    post_id: str
    title: str
    keywords: List[str]
    thumbnail: str
    publication_date: str
    last_updated: str
    author: str
    article_text: str
    additional_metadata: dict = field(default_factory=dict)

class SitemapParser:
    """Class to handle parsing the sitemap and extracting article URLs."""

    def __init__(self, main_sitemap_url):
        """Initialize the parser with the main sitemap URL."""
        self.main_sitemap_url = main_sitemap_url

    def get_nested_sitemap_urls(self):
        """Retrieve the URLs of all nested sitemaps from the main sitemap."""
        try:
            # Send a GET request to the main sitemap URL
            response = requests.get(self.main_sitemap_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the XML response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'xml')
            
            # Extract and return all sitemap URLs
            return [sitemap.find('loc').text for sitemap in soup.find_all('sitemap')]
        except requests.RequestException as e:
            # Print error message if the request fails
            print(f"Failed to retrieve sitemap URLs: {e}")
            return []

    def get_article_urls(self, sitemap_url, max_articles):
        """Extract article URLs from a given sitemap URL, with an optional limit."""
        try:
            # Send a GET request to the sitemap URL
            response = requests.get(sitemap_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the XML response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'xml')
            
            # Extract and return the article URLs, limited by max_articles if provided
            urls = [url.find('loc').text for url in soup.find_all('url')]
            return urls[:max_articles] if max_articles > 0 else urls
        except requests.RequestException as e:
            # Print error message if the request fails
            print(f"Failed to retrieve article URLs from {sitemap_url}: {e}")
            return []

class ArticleScraper:
    """Class to handle scraping individual articles for metadata and content."""

    def fetch_article_data(self, article_url):
        """Scrape metadata and content from a given article URL."""
        try:
            # Send a GET request to the article URL
            response = requests.get(article_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the HTML response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the script tag containing metadata
            script_tag = soup.find('script', {'id': 'tawsiyat-metadata', 'type': 'text/tawsiyat'})
            metadata = json.loads(script_tag.string.strip()) if script_tag else {}
            
            # Find the section containing the article content
            section = soup.find('section', class_='news-section read-section light_bg pd-top-0 light_bg')
            paragraphs = [p.get_text(strip=True) for p in section.find_all('p')] if section else []
            
            # Print progress to the console
            print(f"Scraped {article_url}")
            
            # Return the extracted data as an ArticleData object
            return ArticleData(
                url=article_url,
                post_id=metadata.get('postid', ''),
                title=metadata.get('title', ''),
                keywords=metadata.get('keywords', '').split(','),
                thumbnail=metadata.get('thumbnail', ''),
                publication_date=metadata.get('published_time', ''),
                last_updated=metadata.get('last_updated', ''),
                author=metadata.get('author', ''),
                article_text=' '.join(paragraphs),
                additional_metadata=metadata
            )
        except Exception as e:
            # Print error message if scraping fails
            print(f"Failed to scrape {article_url}: {e}")
            return None

class FileUtility:
    """Utility class to handle saving data to JSON files."""

    def save_to_file(self, data, filename):
        """Save the given data to a file in JSON format."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            # Print error message if saving fails
            print(f"Failed to save data to {filename}: {e}")

def main(max_articles=200):
    """Main function to coordinate sitemap parsing, article scraping, and file saving."""
    
    # URL of the main sitemap
    main_sitemap_url = 'https://www.almayadeen.net/sitemaps/all.xml'
    
    # Instantiate the necessary classes
    parser = SitemapParser(main_sitemap_url)
    scraper = ArticleScraper()
    file_util = FileUtility()

    # Get all nested sitemap URLs from the main sitemap
    nested_sitemaps = parser.get_nested_sitemap_urls()
    total_scraped = 0

    # Loop through each sitemap URL and scrape articles
    for sitemap_url in nested_sitemaps:
        if max_articles == 0 or total_scraped < max_articles:
            # Calculate remaining articles to scrape if a limit is set
            remaining_articles = max_articles - total_scraped if max_articles > 0 else 0
            
            # Get article URLs from the current sitemap
            article_urls = parser.get_article_urls(sitemap_url, remaining_articles)
            
            # Scrape data from each article
            articles_data = [scraper.fetch_article_data(url) for url in article_urls if url]
            
            # Save scraped data to a JSON file
            file_util.save_to_file([data.__dict__ for data in articles_data if data], f'articles_data_{total_scraped}.json')
            
            # Update the total number of scraped articles
            total_scraped += len(article_urls)
        else:
            break

if __name__ == "__main__":
    main(50)  # Adjust this number as needed or set to 0 to scrape all articles