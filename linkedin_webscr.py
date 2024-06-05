# Import Packages
from selenium import webdriver
import time
import pandas as pd
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

# Use this URL and change city or role accordingly
url1 = 'https://www.linkedin.com/jobs/search?keywords=Marketing%20Data%20Analyst&location=Berlin%2C%20Berlin%2C%20Germany&geoId=106967730&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

# Specify the path to chromedriver
chrome_driver_path = r'C:\\Users\\ankit\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

# Set up the web driver and get the URL
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)
driver.get(url1)

# Find number of job listings
y = driver.find_elements(By.CLASS_NAME, 'results-context-header__job-count')[0].text
print(y)

n = pd.to_numeric(y.replace(',', ''))
print(n)

# Loop to scroll through all jobs and click on see more jobs button for infinite scrolling
i = 2
while i <= int((n+200)/25)+1: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i += 1
    
    try:
        send = driver.find_element(By.XPATH, "//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", send)   
        time.sleep(3)
    except:
        pass
        time.sleep(5)

# Create empty lists for company name, job title, and location
companyname = []
titlename = []
locationname = []

# Find and append company names, titles, and locations to the lists
try:
    for i in range(n):
        company = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')[i].text
        companyname.append(company)
        title = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')[i].text
        titlename.append(title)
        location = driver.find_elements(By.CLASS_NAME, 'job-search-card__location')[i].text
        locationname.append(location)
except IndexError:
    print("no")

# Create dataframes for company name, title, and location
companyfinal = pd.DataFrame(companyname, columns=["company"])
titlefinal = pd.DataFrame(titlename, columns=["title"])
locationfinal = pd.DataFrame(locationname, columns=["location"])

# Join the lists
x = companyfinal.join(titlefinal).join(locationfinal)
print(x)

# Save file in your directory
x.to_csv('linkedin.csv')

# Find job links and append them to a list
jobList = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')
hrefList = [e.get_attribute('href') for e in jobList]

print(hrefList)

linklist = pd.DataFrame(hrefList, columns=["joblinks"])
linklist.to_csv('linkedinlinks.csv')

# Close the driver
driver.close()
