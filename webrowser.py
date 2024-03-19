from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from functions import takeCommand, get_website_url_from_command
import time
import bs4

service = Service("./chromedriver_win32/chromedriver.exe")
options = webdriver.ChromeOptions()


def set_user_agent():
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/94.0.4606.81 Safari/537.36")


def execute_search(search_keyword, search_box=None):
    for char in search_keyword:
        search_box.send_keys(char)
        time.sleep(0.1)
    search_box.submit()


def search_on_site():
    site_url = "https://www.google.com"
    search_keyword = ""
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(site_url)
        try:
            # 等待搜索框加载完成
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            execute_search(search_keyword, search_box)  # 修正此处的参数传递
            while True:
                command = input("指令: ")
                if command == "close the window":
                    break
            results = driver.find_elements(By.XPATH, '//div/h3/a')
            summaries = []
            for result in results:
                result.click()
                # 打开新标签页
                main_window = driver.current_window_handle
                handles = driver.window_handles
                print(handles)
                driver.switch_to.window(handles[-1])
                source = driver.page_source
                soup = bs4.BeautifulSoup(source, 'lxml')
                content = soup.find('body')
                summary = openai()
                summaries.append(summary)
                scroll_pause_time = 0.5
                screen_height = driver.execute_script("return window.screen.height;")
                i = 0
                while True:
                    driver.execute_script("window.scrollTo(0,{screen_height}*{i}*{0.75});")
                    i += 1
                    time.sleep(scroll_pause_time)
                driver.close()
                driver.switch_to.window(main_window)
            driver.quit()
        except NoSuchElementException:
            print("找不到搜索框元素")
            return None
        except TimeoutException:
            print("页面加载超时")
            return None


if __name__ == '__main__':
    while True:
        # print("Listening...")
        # query = takeCommand()
        search_on_site()
