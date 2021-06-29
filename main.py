import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import argparse


PATH = './assets/chromedriver.exe'

TARGET_URL_1 = 'https://www.twilio.com/'
TARGET_URL_2 = 'https://datafull.com.br/'

MIN_SLEEP_TIME = 1
MAX_SLEEP_TIME = 2

def sleep_time():
    return random.uniform(MIN_SLEEP_TIME, MAX_SLEEP_TIME)

def scroll_down(driver):
    y = 1000
    for timer in range(0, 20):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(0.5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(sleep_time())

def scroll_up(driver):
    y = 15000
    for timer in range(0, 11):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y -= 1000
        time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")

    time.sleep(sleep_time())

def press_tab(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//body'))).send_keys(Keys.TAB)

def open_url(driver, url):
    '''
    Open a url -> Clicks -> Scrolls down -> Presses Tab -> Scrolls up ->
    Presses Tab -> Scrolls down -> Closes the browser

    Tab can also be used to invoke data traffic for a website
    '''

    driver.get(url)

    time.sleep(2)

    driver.find_element_by_xpath("//body").click()
    driver.find_element_by_xpath("//body").click()

    press_tab(driver)
    scroll_down(driver)

    press_tab(driver)
    scroll_up(driver)

    scroll_down(driver)

    time.sleep(sleep_time()*2)


def bot_visit(user_agent):
    '''
    configure the webdriver
    '''

    opts = webdriver.ChromeOptions()
    opts.add_argument(f"user-agent={user_agent}")
    opts.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=opts)

    open_url(driver, TARGET_URL_1)
    open_url(driver, TARGET_URL_2)

    driver.quit()

def get_user_agent(k):
    with open('./assets/user-agents.txt') as user_agents:
        user_agent = user_agents.readlines()
        return random.choices(user_agent, k=k)

def get_args():
    parser = argparse.ArgumentParser(description='Bot visits websites')
    parser.add_argument('--num_concurrent', help='Number of browsers working in parallel', type=int)
    parser.add_argument('--num_agent', help='Total number of user-agents to be used', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    user_agents = get_user_agent(args.num_agent)
    with ThreadPoolExecutor(max_workers=args.num_concurrent) as executor:
        executor.map(bot_visit, user_agents)
