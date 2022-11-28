import requests
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from colorama import Fore
import os
from os.path import exists
from datetime import date

today = date.today()
date = today.strftime("%d%m%Y")

globalCount = 0
globalCountAll = 0

def checker(url, driver):
    try:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        r = requests.get(url=url, headers=headers, allow_redirects=False)
        if r.status_code == 200 and "404" not in r.text:
            if not exists(date):
                os.mkdir(date)
            img_name = url.replace("https://", "")
            if "www." in img_name:
                img_name = img_name.replace("www.", "")
            separator = '.'
            update_img_name = img_name.split(separator, 1)[0]
            driver.get(url)
            driver.save_screenshot(date + "/" + update_img_name + ".png")
            print(Fore.MAGENTA + "[+] " + url + Fore.CYAN + " ScreenShot name : " + date + "/" + update_img_name)
            return True
        else:
            print(Fore.YELLOW + "[-] " + url)
            return False
    except requests.exceptions.RequestException as e:
        return False


def jsonDecode(name, driver):
    countAll = 0
    count = 0
    with open('url.json', encoding="utf8") as f:
        data = json.load(f)
        for i in data:
            countAll = countAll + 1
            url = i['url'].replace("{}", name)
            if checker(url, driver):
                count = count + 1
    return countAll, count


if __name__ == '__main__':
    op = Options()
    op.add_argument("--headless")
    op.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=op)
    pseudo = None
    while True:
        pseudo = input("Identifiant :")
        if pseudo:
            break
    thisCountAll, thisCount = jsonDecode(pseudo, driver)

    print(Fore.WHITE + "\nSite tested : " + str(thisCountAll))
    print(Fore.WHITE + "\nResult : " + Fore.MAGENTA + str(thisCount))
