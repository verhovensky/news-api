import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

# Webdriver config
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen
# configure chrome browser to not load images and javascript
options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs",
                                       {"profile.managed_default_content_settings.images": 2})


# The following two functions could be rewritten into one:
# parse_news_links(url: str, type: str, amount: int) -> dict:
#     parsed = {}
#     types = {'y': {'news_element': ''
#                    'click_btn': '' } }
#     ...
#     while len(parsed) < amount:
#         ...


def parse_news_links_yandex() -> dict:
    parsed = {}
    driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
    driver.get("https://market.yandex.ru/partners/news")
    for count, news in enumerate(
            driver.find_elements(By.CLASS_NAME,
                                 "link_theme_normal")):
        link = news.get_attribute("href")
        if link != '':
            parsed.update({count: link})
    return parsed


def parse_news_links_ozon() -> dict:
    parsed = {}
    driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
    start = 0
    while len(parsed) < 10:
        limit = 10 - len(parsed)
        driver.get(f"https://seller.ozon.ru/content-api/news/?_limit={limit}&_start={start}")
        content = driver.find_element(By.TAG_NAME, 'pre').text
        parsed_json = json.loads(content)
        time.sleep(random.SystemRandom().uniform(0.5, 1.2))
        for count, news in enumerate(parsed_json):
            post = {'title': news["title"],
                    'link': "https://seller.ozon.ru/news/{}/".
                            format(news["slug"]),
                    'date': news["date"],
                    'tags': news["theme"]}
            parsed.update({news["title"]: post})
        start += len(parsed_json)
    return parsed


def parse_single_article_link_yandex(article_url: str) -> dict:
    tags = {}
    driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
    driver.get(article_url)
    WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.CLASS_NAME,
                                        "news-info__post-body")))
    post_title = driver.find_element(By.CLASS_NAME,
                                     "news-info__title").text
    post_date = driver.find_element(By.CLASS_NAME,
                                    "news-info__published-date")\
        .get_attribute("datetime")
    post_body = driver.find_element(By.CLASS_NAME,
                                    "news-info__post-body").text
    for count, tag in enumerate(driver.find_elements(By.CLASS_NAME,
                                                     "news-info__tag")):
        tags.update({count: tag.text})

    return {'title': post_title,
            'date': post_date,
            'body': post_body,
            'tags': tags}


def parse_single_article_slug_ozon(article_slug: str) -> dict:
    article_url = f"https://seller.ozon.ru/news/{article_slug}/"
    driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
    driver.get(article_url)
    content = driver.page_source
    print(content)
    post_body = driver.find_element(By.CLASS_NAME, "new-section").text
    print(post_body)
    return {'body': post_body}


parse_single_article_slug_ozon('fbs-i-realfbs-izmenili-mehaniku-blokirovok')


# https://github.com/MaistrenkoAnton/django-material-admin
