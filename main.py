import random
import time
import os
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import argparse


PATH = './assets/chromedriver.exe'

TARGET_URL_1 = 'https://pedantic-lumiere.67-23-238-111.plesk.page/'

DICT_TABS = {
            'news': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/news-page',
            'sports': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/sports-page',
            'tech': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/tech-page',
            'lifestyle': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/lifestyle-page',
            'finance': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/finance-page',
            'video': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/video-page',
            'authors': 'https://pedantic-lumiere.67-23-238-111.plesk.page/index.php/authors'
            }

EXTERNAL_LINKS = {
    'twilio': 'https://www.twilio.com/',
    'github': 'https://github.com/',
    'codepen': 'https://codepen.io/',
    'codeforces': 'https://codeforces.com/',
    'hackkerrank': 'https://www.hackerrank.com/'
}

MIN_SLEEP_TIME = 5
MAX_SLEEP_TIME = 10

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

def open_url(driver):
    '''
    Open a url -> Clicks -> Scrolls down -> Presses Tab -> Scrolls up ->
    Presses Tab -> Scrolls down -> Closes the browser

    Tab can also be used to invoke data traffic for a website
    '''

    time.sleep(MIN_SLEEP_TIME)

    driver.find_element_by_xpath("//body").click()
    driver.find_element_by_xpath("//body").click()

    press_tab(driver)
    scroll_down(driver)

    press_tab(driver)
    scroll_up(driver)

    scroll_down(driver)

    time.sleep(sleep_time()*2)

def open_tab(driver, url):
    driver.get(url)
    time.sleep(5)


def run(driver):
    driver.get(TARGET_URL_1)
    open_url(driver)

    total_visit = random.randint(2, 5)
    pages = random.choices(list(DICT_TABS.values()), k=total_visit)
    # print(pages)
    for page in pages:
        open_tab(driver, page)
        open_url(driver)
    #     print('Done')
    driver.execute_script(f'''window.open("{random.choice(list(EXTERNAL_LINKS.values()))}", "_blank");''')


def bot_visit(user_agent):
    '''
    configure the webdriver
    '''

    opts = webdriver.ChromeOptions()
    opts.add_argument(f"user-agent={user_agent}")
    # opts.add_argument('--headless')
    opts.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=opts)
    driver.maximize_window()

    run(driver)
    time.sleep(sleep_time()*2)
    driver.quit()

def get_user_agent(k):
    with open('./assets/user-agents.txt') as user_agents:
        user_agent = user_agents.readlines()
        return random.choices(user_agent, k=k)

def get_user_agent_phone(k):
    with open('./assets/user-agents-phone.txt') as user_agents:
        user_agent = user_agents.readlines()
        return random.choices(user_agent, k=k)

def get_user_agent_tab(k):
    with open('./assets/user-agents-tab.txt') as user_agents:
        user_agent = user_agents.readlines()
        return random.choices(user_agent, k=k)

def get_args():
    parser = argparse.ArgumentParser(description='Bot visits websites')
    parser.add_argument('--num_concurrent', help='Number of browsers working in parallel', type=int)
    parser.add_argument('--num_agent', help='Total number of user-agents to be used', type=int)
    return parser.parse_args()

def shot_counter(num):
    file_desktop = 'assets/file_desktop.txt'
    file_tab = 'assets/file_tab.txt'

    if not os.access(file_desktop, os.F_OK):
        with open(file_desktop, 'w') as desk_f:
            desk_f.writelines('0\n')

    if not os.access(file_tab, os.F_OK):
        with open(file_tab, 'w') as tab_f:
            tab_f.writelines('0\n')

    desk_f = open(file_desktop, 'r')
    desk_counter = int(desk_f.readline())
    desk_f.close()

    tab_f = open(file_tab, 'r')
    tab_counter = int(tab_f.readline())
    print(f'{tab_counter=} {desk_counter=}')
    tab_f.close()

    with open(file_desktop, 'w') as desk_f:

        new_desk = (desk_counter+num) % 20
        hit_desk = (desk_counter+num) // 20
        desk_f.write(str(new_desk))

    with open(file_tab, 'w') as tab_f:

        new_tab = (tab_counter+num) % 50
        hit_tab = (tab_counter+num) // 50
        tab_f.write(str(new_tab))

    return hit_desk, hit_tab


if __name__ == '__main__':
    args = get_args()
    total = args.num_agent
    user_ag_phone = get_user_agent_phone(total)
    num_desk, num_tab = shot_counter(total)
    user_ag_desk = get_user_agent(num_desk)
    user_ag_tab = get_user_agent_tab(num_tab)
    user_agents = user_ag_phone + user_ag_desk + user_ag_tab

    with ThreadPoolExecutor(max_workers=args.num_concurrent) as executor:
        executor.map(bot_visit, user_agents)
