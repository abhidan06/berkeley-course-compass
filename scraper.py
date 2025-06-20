import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

BASE_URL = "https://guide.berkeley.edu"
COURSES_URL = f"{BASE_URL}/courses/"

response = requests.get(COURSES_URL)
soup = BeautifulSoup(response.text, "html.parser")

course_urls = [BASE_URL + link['href'] for link in soup.select("#atozindex a[href]")]

def parse_course_block(block, department):
    title_tag = block.find('h3', class_='courseblocktitle')
    desc_tag = block.find('p', class_='courseblockdesc')

    if not title_tag or not desc_tag:
        return None
    
    course_code = title_tag.find("span", class_="code").text.replace('\xa0', ' ')
    course_title = title_tag.find("span", class_="title").text
    units = title_tag.find("span", class_="hours").text.split(" ")[0]
    desc_parts = list(desc_tag.find("span", class_="descshow").stripped_strings)
    description = desc_parts[1] if len(desc_parts) > 1 else None 

    return {
        "department": department,
        "course_code": course_code,
        "title": course_title,
        "units": units,
        "description": description
    }

all_courses = []
for url in tqdm(course_urls):
    department = url.split('/')[-2].upper()
    res = requests.get(url)
    s = BeautifulSoup(res.text, 'html.parser')
    blocks = s.find_all('div', class_='courseblock')
    for block in blocks:
        data = parse_course_block(block, department)
        if data:
            all_courses.append(data)

df = pd.DataFrame(all_courses)
df.to_csv("berkeley_courses.csv", index=False)
print(f"Saved {len(df)} courses to berkeley_courses.csv")