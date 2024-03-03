from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from chromedriver_py import binary_path
from fake_useragent import UserAgent
useragent = UserAgent()
cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"]
all_job_titles = []
all_company_names = []
all_salaries = []
for city in cities:

    url = f'https://in.indeed.com/jobs?q=&l={city}'
    c_options = webdriver.ChromeOptions()
    c_options.add_argument(f"user-agent={useragent}")
    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=svc,options=c_options)
    driver.get(url)
    time.sleep(5)
    try:
        container_element = driver.find_element(By.CLASS_NAME, 'google-Only-Modal-Upper-Row')
        close_button = container_element.find_element(By.TAG_NAME, 'button')
        close_button.click()
    except:
        pass
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    job_title_spans = soup.find_all('span', id=lambda x: x and x.startswith('jobTitle-'))
    job_titles = [span.text for span in job_title_spans]
    all_job_titles.extend(job_titles)

    company_name_spans = soup.find_all('span', {'data-testid': 'company-name'})
    company_names = [span.text for span in company_name_spans]
    all_company_names.extend(company_names)

    salary_div_classes = soup.find_all('div', attrs={'data-testid': 'attribute_snippet_testid'})
    salaries = [sal.text.strip() for sal in salary_div_classes]
    all_salaries.extend(salaries)

    driver.quit()

# Write data to CSV file
with open('dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Job Title', 'Company Name', 'Salary'])
    writer.writerows(zip(all_job_titles, all_company_names, all_salaries))