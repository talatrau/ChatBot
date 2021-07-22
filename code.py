import random
import csv
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver

def init_webdriver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    return webdriver.Chrome(executable_path='chromedriver.exe', options=options)


def clean_data(text: str, ignore=""):
    text = text.strip('"')
    text = text.replace('\n', ' ')
    return text.replace(ignore, '')


def save_data(label: str, browser: WebDriver, writer) -> None:
    try:
        title = browser.find_element_by_xpath("/html/body/section[4]/div/div[2]/h1")
        title = clean_data(title.text)

        description = browser.find_element_by_xpath("/html/body/section[4]/div/div[2]/p")
        try:
            span = browser.find_element_by_xpath("/html/body/section[4]/div/div[2]/p/span")
            span = span.text
        except:
            span = ""
        finally:
            description = clean_data(description.text, span)

        contents = browser.find_elements_by_class_name("Normal")
        contents = ''.join(content.text for content in contents[:-1])
        contents = clean_data(contents)

        data = [title, description, contents, label]
        writer.writerow(data)
    except:
        raise ValueError('No description or content')


def crawl_data(link: str, label: str, browser: WebDriver, writer) -> None:
    browser.get(link)
    sleep(random.randint(1, 3))
    index = 0

    for _ in range(500):
        try:
            index += 1
            xpath = '//*[@id="automation_TV0"]/div[2]/article[{}]/p/a'.format(index)
            news = browser.find_element_by_xpath(xpath)
            news.click()
            sleep(random.randint(1, 3))
            save_data(label, browser, writer)
            browser.back()
            sleep(random.randint(1,3))
        except ValueError:
            browser.back()
            sleep(random.randint(1,3))
        except Exception:
            print(index)
            next = browser.find_element_by_xpath('/html/body/div[3]/div/div/div/a[5]')
            next.click()
            index = 0
            sleep(random.randint(1,3))

    browser.close()


with open('data2.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Description", "Content", "Label"])

    browser = init_webdriver()
    crawl_data("https://vnexpress.net/phap-luat-p20", "phapluat", browser, writer)

    sleep(10)

    browser = init_webdriver()
    crawl_data("https://vnexpress.net/khoa-hoc-p2", "khoahoc", browser, writer)