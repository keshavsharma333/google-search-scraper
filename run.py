# Import necessary libraries
from math import fabs
from selenium import webdriver   
from selenium.webdriver.chrome.service import Service  # Import Service to manage ChromeDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Import By for new Selenium element location strategy
from bs4 import BeautifulSoup  # to parse the HTML code
import time 
import pandas as pd  # to store data in CSV file
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse as urlparse
from requests_html import HTMLSession
import re

# Enter inputs before initializing the browser to avoid interruptions
print("Enter the filename")  # filename to store data
filename = str(input())
isEmail = input("Do you want to get email?(y/n)").lower() == "y"

# Prompt for search term
search_query = input("Enter Your Search Term: ")

# Construct the dynamic Google search URL for local businesses
base_url = "https://www.google.com/search"
params = {
    "q": urlparse.quote_plus(search_query),  # Encode the search query
    "tbm": "lcl",  # Local search for business listings
    "num": "10",  # Number of results per page
    "tbs": "lf:1,lf_ui:9"  # Filter for local search results
}

# Combine base URL with encoded parameters
link = f"{base_url}?{urlparse.urlencode(params)}"

# Initialize HTML session only if needed
session = None
if isEmail:
    session = HTMLSession()

# Set up Chrome options
chrome_options = Options() 
chrome_options.add_argument('--no-sandbox')  
chrome_options.add_argument('--headless')

# Initialize the Chrome WebDriver instance
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

def get_email(url):
    # Function to get emails from a website URL
    if not url or url == "#":
        return []

    # Regex pattern
    pattern = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

    # Send the GET request
    response = session.get(url)

    # Simulate JS running code
    response.html.render()

    # Get body element
    body = response.html.find("body")[0]

    # Extract emails
    emails = re.findall(pattern, body.text)
    return emails

# Initialize variables
record = []
e = []  # Ensure 'e' is initialized here
t1 = time.time()
countt = 0

def Selenium_extractor():
    global countt, e  # Declare 'e' as global to avoid scope issues
    time.sleep(2)
    
    # Updated to use By.CLASS_NAME
    a = browser.find_elements(By.CLASS_NAME, "VkpGBb")
    time.sleep(1)
    for i in range(len(a)):
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        
        # BeautifulSoup for scraping the HTML source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.findAll('div', {"class": "SPZz6b"})
            if Name_Html:
                name = Name_Html[0].text
                name = "".join(name.rsplit('Directions            Saved (0) Saved Save', 1))
                name = "".join(name.rsplit('Website', 1))
                name = "".join(name.rsplit('Saved (0) Saved Save', 1))
                name = "".join(name.rsplit('     Call', 1))
                name = "".join(name.rsplit('     ', 1))
                name = "".join(name.rsplit('Call', 1))
                
                if name not in e:
                    e.append(name)
                    print(name)
                    Phone_Html = soup.findAll('span', {"class": "LrzXr zdqRlf kno-fv"})    
                    phone = Phone_Html[0].text if Phone_Html else "Not available"
                    print(phone)
                    
                    Address_Html = soup.findAll('span', {"class": "LrzXr"})
                    address = Address_Html[0].text if Address_Html else "Not available"
                    
                    email = "[]"
                    try:
                        Website_Html = soup.findAll('div', {"class": "QqG1Sd"})
                        if Website_Html:
                            web = Website_Html[0].findAll('a')
                            website = web[0].get('href') if web else "Not available"
                            if website and website != "#" and isEmail:
                                email = str(list(set(get_email(website))))
                        else:
                            website = "Not available"
                    except:
                        website = "Not available"
                    
                    record.append((name, phone, address, website, email))
                    df = pd.DataFrame(record, columns=['Name', 'Phone number', 'Address', 'Website', 'Email'])
                    df.to_csv(filename + '.csv', index=False, encoding='utf-8')
                    countt += 1
            else:
                print("Name element not found.")
        except Exception as ex:
            print(f"Error processing entry: {ex}")
            continue

    try:
        time.sleep(1)            
        next_button = browser.find_element(By.ID, "pnnext")  # Updated to use By.ID
        next_button.click()
        browser.implicitly_wait(2)
        time.sleep(2)
        Selenium_extractor()
    except Exception as ex:
        print(f"ERROR occurred at clicking next button: {ex}")
        print(f"Total time taken to save {str(countt)} is {str(time.time() - t1)}")
        browser.quit()

# Navigate to the search results page
browser.get(str(link)) 
time.sleep(10)  # Pausing the program for 10 seconds
Selenium_extractor()
