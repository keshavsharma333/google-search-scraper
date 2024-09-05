# Google Search Scraper

A Python-based web scraper that uses Selenium and BeautifulSoup to scrape data from Google search results.

## Features

- Scrapes data such as names, phone numbers, addresses, and websites.
- Supports optional email scraping using `requests_html`.
- Saves data to a CSV file.

## Requirements

- Python 3.x
- Chrome browser
- `pip` (Python package installer)

## Setup

1. **Clone the repository:**

   git clone https://github.com/keshavsharma333/google-search-scraper.git
   cd google-search-scraper

2. **Install dependencies:**

   pip install -r requirements.txt

3. **Run the script:**

   python run.py

## Usage

- Enter the filename where the scraped data will be saved when prompted.
- Choose whether to scrape email addresses by entering 'y' or 'n'.
- Enter the search term when prompted.
- The script will scrape the data and save it to the specified CSV file.

Note
The script uses webdriver_manager to automatically manage the ChromeDriver, so you do not need to manually download or set up the driver.

Contributing
Feel free to fork this repository and submit pull requests.

Disclaimer
This script is intended for educational purposes only. When using it, please ensure that you comply with Google's Terms of Service and respect their robots.txt file. The use of this script for scraping Google search results should be done responsibly and without violating any of Google's policies.

License
This project is licensed under the MIT License.
