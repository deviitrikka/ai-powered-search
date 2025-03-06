from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_linkedin_jobs(query: str):
    """Scrapes LinkedIn job listings based on the given query."""
    
    # Set up Selenium WebDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Construct LinkedIn job search URL
    base_url = "https://www.linkedin.com/jobs/search?keywords="
    search_url = f"{base_url}{query.replace(' ', '+')}"
    driver.get(search_url)

    # Wait for page to load
    time.sleep(5)

    # Extract job listings
    job_listings = []
    jobs = driver.find_elements(By.CLASS_NAME, "jobs-search__results-list")

    for job in jobs:
        job_cards = job.find_elements(By.TAG_NAME, "li")
        for card in job_cards:
            try:
                title = card.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = card.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                job_link = card.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")
                posted_time = card.find_element(By.TAG_NAME, "time").text.strip() if card.find_elements(By.TAG_NAME, "time") else "N/A"
                
                if title and company and location and job_link:
                    job_listings.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "job_link": job_link,
                        "posted_time": posted_time
                    })
            except Exception as e:
                print(f"Error extracting job details: {e}")

    # Close the driver
    driver.quit()
    print (job_listings)
    return job_listings
