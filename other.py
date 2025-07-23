from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.add_argument("--headless")  # chạy ẩn
driver = webdriver.Chrome(options=options)

def get_conferences_with_selenium(url):
    driver.get(url)
    time.sleep(3)  # đợi trang load xong
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    conferences = []
    rows = soup.select('.listing-content')  # kiểm tra selector này đúng hay chưa

    for row in rows:
        title = row.select_one('.title a')
        date = row.select_one('.date')
        location = row.select_one('.location')
        desc = row.select_one('.details')

        if title and date and location:
            conferences.append({
                'Title': title.text.strip(),
                'Link': "https://www.conferencealerts.com" + title['href'],
                'Date': date.text.strip(),
                'Location': location.text.strip(),
                'Details': desc.text.strip() if desc else ''
            })
    return conferences

def save_to_csv(data, filename='conferences.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Title', 'Date', 'Location', 'Link', 'Details'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    all_data = []
    for i in range(1, 4):
        page_url = f"https://www.conferencealerts.com/topic-listing?topic=Education&page={i}"
        print(f"Crawling page {i}...")
        data = get_conferences_with_selenium(page_url)
        all_data.extend(data)
    save_to_csv(all_data)
    print(f"Đã lưu {len(all_data)} hội thảo vào 'conferences.csv'")
    driver.quit()
