import requests
import warnings
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
from tqdm import tqdm
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

def display_banner():
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
 __     __                                                     __                         
/  |   /  |                                                   /  |                        
$$ |   $$ | ______    ______    ______   __    __  _______   _$$ |_     ______    ______  
$$ |   $$ |/      \  /      \  /      \ /  \  /  |/       \ / $$   |   /      \  /      \ 
$$  \ /$$//$$$$$$  |/$$$$$$  |/$$$$$$  |$$  \/$$/ $$$$$$$  |$$$$$$/   /$$$$$$  |/$$$$$$  |
 $$  /$$/ $$    $$ |$$ |  $$/ $$ |  $$ | $$  $$<  $$ |  $$ |  $$ | __ $$    $$ |$$ |  $$/ 
  $$ $$/  $$$$$$$$/ $$ |      $$ |__$$ | /$$$$  \ $$ |  $$ |  $$ |/  |$$$$$$$$/ $$ |      
   $$$/   $$       |$$ |      $$    $$/ /$$/ $$  |$$ |  $$ |  $$  $$/ $$       |$$ |      
    $/     $$$$$$$/ $$/       $$$$$$$/  $$/   $$/ $$/   $$/    $$$$/   $$$$$$$/ $$/       
                              $$ |                                                        
                              $$ |                                                        
                              $$/                                                         """)))
    print("")

def select_proxy_server(proxy_servers):
    print(Colors.orange, Center.XCenter("╔════════════════════════════════════════════════════════════════════════════╗"))
    print(Colorate.Vertical(Colors.green_to_blue,"  "))
    for i in range(1, len(proxy_servers) + 1):
        print(Colors.cyan, Center.XCenter(f"Server {i}: {proxy_servers[i]}"))
    print(" ")
    print(Colors.red, Center.XCenter("The only available Proxy is currently Proxy-1")
    print(Colors.orange, Center.XCenter("╚════════════════════════════════════════════════════════════════════════════╝"))

    while True:
        try:
            proxy_choice = int(input(Colorate.Vertical(Colors.cyan_to_blue, "Choose the Proxy (1-5): >>")))
            if proxy_choice in proxy_servers:
                return proxy_servers[proxy_choice]
            else:
                print(Fore.RED + "This number is not available!")
        except ValueError:
            print(Fore.RED + "Enter a Number.")

def get_twitch_username():
    print(Colorate.Vertical(Colors.green_to_blue, "\n\n"))
    print(Colors.orange, Center.XCenter("╔════════════════════════════════════════════════════════════════════════════╗"))
    print(Colors.cyan, Center.XCenter("Streamer (e.g. Verpxnter)"))
    print(Colors.orange, Center.XCenter("╚════════════════════════════════════════════════════════════════════════════╝"))
    return input(Colorate.Vertical(Colors.cyan_to_blue, "Enter Streamer >> "))

def get_viewer_count():
    print(Colorate.Vertical(Colors.green_to_blue, "\n\n"))
    print(Colors.orange, Center.XCenter("╔════════════════════════════════════════════════════════════════════════════╗"))
    print(Colors.cyan, Center.XCenter("Viewers to be added"))
    print(Colors.orange, Center.XCenter("╚════════════════════════════════════════════════════════════════════════════╝"))

    while True:
        try:
            return int(input(Colorate.Vertical(Colors.cyan_to_blue, "Viewer Count >> ")))
        except ValueError:
            print(Fore.RED + "Enter an Number. And keep in mind, a higher amount of Views needs more time!")

def setup_driver():
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-de15v-shm-usage')
    chrome_options.binary_location = chrome_path

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_cookies(driver, cookies_file='cookies.pkl'):
    try:
        with open(cookies_file, 'rb') as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(Fore.GREEN + "Cookies loaded successfully.")
    except (FileNotFoundError, pickle.PickleError) as e:
        print(Fore.RED + "No Cookies were found..")

def save_cookies(driver, cookies_file='cookies.pkl'):
    cookies = driver.get_cookies()
    with open(cookies_file, 'wb') as f:
        pickle.dump(cookies, f)
    print(Fore.GREEN + "Cookies were saved.")

def main():
    display_banner()

    # Proxy URLs
    proxy_servers = {
        1: "https://www.blockaway.net",
        # ------ #
        # At the moment, Proxy Server *1 is the only one operational. (Cause of the cookies)
        # ------ #
        2: "https://www.croxy.network",
        3: "https://www.croxy.org",
        4: "https://www.youtubeunblocked.live",
        5: "https://www.croxyproxy.net",
    }

    proxy_url = select_proxy_server(proxy_servers)
    twitch_username = get_twitch_username()
    proxy_count = get_viewer_count()

    driver = setup_driver()

    try:
        driver.get(proxy_url)
        # time.sleep(5)
        load_cookies(driver)
        # save_cookies(driver)

        for i in tqdm(range(proxy_count), desc="Loading Tabs"):
            if i != 0:
                driver.switch_to.new_window('tab')
            driver.get(proxy_url)

            text_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'url'))
            )

            text_box.click()
            text_box.send_keys(f'https://www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.ENTER)

        print(Colors.orange, Center.XCenter("╔════════════════════════════════════════════════════════════════════════════╗"))
        print(Colors.cyan, Center.XCenter("Die Viewer wurden hinzugefügt und erscheinen bald."))
        print(Colors.orange, Center.XCenter("╚════════════════════════════════════════════════════════════════════════════╝"))

        while True:
            print(Fore.LIGHTYELLOW_EX + "Refreshing in 15 Seconds...")
            time.sleep(15)
            Windows = driver.window_handles
            # print("Length Windows-Array:", len(Windows))
            # print("Windows: ", Windows)
            for window in tqdm(Windows, desc="Refreshing"):
                driver.switch_to.window(window)
                driver.refresh()

        # input(Colorate.Vertical(Colors.cyan_to_blue, "Press any key to stop..."))

    except Exception as e:
        print(Fore.RED + f"Fehler: {e}")

if __name__ == '__main__':
    main()


##############
# Copyright © 2024 Verpxnter. All rights reserved.
# Unauthorized copying or distribution of this script, in any form or by any means, is strictly prohibited.
##############
