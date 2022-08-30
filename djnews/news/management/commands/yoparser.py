import sys
import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_docker_url = "http://chrome:4444"

# load user-agents from json
path = os.getcwd()
file_path = os.path.join(path, "user-agents.json")
if os.path.exists(file_path):
    file = open("user-agents.json")
    agents = json.load(file)
    file.close()
else:
    sys.stdout.write(f"\nNo user-agents.json file found in {path} \n")
    sys.exit()

# TODO: The following code could be rewritten into one (Class)
# TODO: add logger instead of sys.stdout.write

# declare webdriver options
options = Options()
userAgent = random.choice(agents)
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-infobars")
options.add_argument(f"User-Agent={userAgent}")
# configure chrome browser to not load images and javascript
options.add_argument("--disable-blink-features=AutomationControlled")

sys.stdout.write(f"\nUsing User-Agent: "
                 f"\n{userAgent} \n")


def parse_news_links_yandex(type: str) -> dict:
    parsed = {}
    if type == 'docker':
        driver = webdriver.Remote(chrome_docker_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.get("https://market.yandex.ru/partners/news")
    time.sleep(random.SystemRandom().uniform(0.5, 1.2))
    for count, news in enumerate(
            driver.find_elements(By.CLASS_NAME,
                                 "link_theme_normal")):
        if count < 10:
            link = news.get_attribute("href")
            if link != '':
                parsed.update({count: link})
    driver.quit()
    return parsed


def parse_news_links_ozon(type: str) -> dict:
    parsed = {}
    if type == 'docker':
        driver = webdriver.Remote(chrome_docker_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    start = 0
    while len(parsed) < 10:
        limit = 10 - len(parsed)
        driver.get(f"https://seller.ozon.ru/content-api/news/?_limit={limit}&_start={start}")
        time.sleep(random.SystemRandom().uniform(0.5, 1.2))
        content = driver.find_element(By.TAG_NAME, 'pre').text
        parsed_json = json.loads(content)
        time.sleep(random.SystemRandom().uniform(0.5, 1.2))
        for count, news in enumerate(parsed_json):
            ready_tags = [d["name"] for d in news["theme"]]
            ready_tags.append('ozon')
            post = {'title': news["title"],
                    'link': "https://seller.ozon.ru/news/{}/".
                            format(news["slug"]),
                    'slug': news["slug"],
                    'date': news["date"],
                    'tags': ready_tags}
            parsed.update({news["title"]: post})
        start += len(parsed_json)
    driver.quit()
    return parsed


def parse_single_article_link_yandex(article_url: str, type: str) -> dict:
    tags = []
    if type == 'docker':
        driver = webdriver.Remote(chrome_docker_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.get(article_url)
    time.sleep(random.SystemRandom().uniform(0.5, 1.2))
    WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.CLASS_NAME,
                                        "news-info__post-body")))
    post_title = driver.find_element(By.CLASS_NAME,
                                     "news-info__title").text
    post_date = driver.find_element(By.CLASS_NAME,
                                    "news-info__published-date")\
        .get_attribute("datetime")
    post_body = driver.find_element(By.CLASS_NAME,
                                    "news-info__post-body").text.replace("\n", " ")
    for count, tag in enumerate(driver.find_elements(By.CLASS_NAME,
                                                     "news-info__tag")):
        tags.append(tag.text.strip("#"))
    tags.append('yandex')
    driver.quit()
    return {'title': post_title,
            'date': post_date,
            'body': post_body,
            'tags': tags}


def parse_single_article_link_ozon(url: str, type: str) -> dict:
    if type == 'docker':
        driver = webdriver.Remote(chrome_docker_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(random.SystemRandom().uniform(0.5, 1.2))
    post_body = driver.find_element(By.CLASS_NAME, "new-section").text.replace("\n", " ")
    driver.quit()
    return {'body': post_body}
