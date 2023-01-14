from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pickle
from secrets import follow_path, acsept_cookies, first_retwit_path, second_retwit_path, like_path 
from secrets import BROWSER_PATH


options = webdriver.ChromeOptions()

# changing user-agent
# options.add_argument(f"user-agent={UserAgent(browsers=['chrome']).random}")
options.add_argument(f"user-agent=qwerty")

options.add_argument('--incognito')

# make it human
options.add_argument("--disable-blink-features=AutomationControlled")

# executing without browser opening
# options.add_argument("--headless")

# for Networks list parsing
options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}) 


class TwitterBot():

    def __init__(self,login:str, name:str, password:str, phone_number:str):

        self.login = login
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.bot = Chrome(BROWSER_PATH,options=options)
    


    def get_cookies(self) -> Chrome:

        browser = self.bot
        
        # Открываем сайт авторизации    
        browser.get('https://twitter.com/login')
        print("Passing through authentication...")

        # Вводим логин 
        login_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input' 
        WebDriverWait(browser, 10*random.random()+5).until(expected_conditions.visibility_of_element_located((By.XPATH, login_xpath)))

        browser.find_element(By.XPATH, login_xpath).clear()
        browser.find_element(By.XPATH, login_xpath).send_keys(self.login)
        browser.find_element(By.XPATH, login_xpath).send_keys(Keys.ENTER)
        

        # Вводим имя пользователя   
        try:
            name_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input' 
            WebDriverWait(browser, 2*random.random()+1).until(expected_conditions.visibility_of_element_located((By.XPATH, name_xpath)))

            browser.find_element(By.XPATH,name_xpath).clear()
            browser.find_element(By.XPATH,name_xpath).send_keys(self.name)
            browser.find_element(By.XPATH,name_xpath).send_keys(Keys.ENTER)
            
        except:
            pass   

        # Вводим пароль 
        pass_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input' 
        WebDriverWait(browser, 5*random.random()+2).until(expected_conditions.visibility_of_element_located((By.XPATH, pass_xpath)))

        browser.find_element(By.XPATH,pass_xpath).clear()
        browser.find_element(By.XPATH,pass_xpath).send_keys(self.password)
        browser.find_element(By.XPATH,pass_xpath).send_keys(Keys.ENTER)
        

        # На случай проверки телефона 
        try: 
            phone_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input' 
            WebDriverWait(browser, 4*random.random()+3).until(expected_conditions.visibility_of_element_located((By.XPATH, phone_xpath)))

            browser.find_element(By.XPATH,phone_xpath).clear()
            browser.find_element(By.XPATH,phone_xpath).send_keys(self.phone_number)
            browser.find_element(By.XPATH,phone_xpath).send_keys(Keys.ENTER)
            print('authentication complete!')

        except:
            print('authentication complete!')

        # cookies
        pickle.dump(browser.get_cookies(), open(f"Downloads/twitter_api/cookies/{self.login}_cookies", "wb"))
        print("🍪Cookies received!🍪")

        browser.close()
        browser.quit()





    def follow(self, url:str):
        
        browser = self.bot
        browser.get(url)
        sleep(5*random.random()+2)

        for cookie in pickle.load(open(f"Downloads/twitter_api/cookies/{self.login}_cookies", "rb")):
            browser.add_cookie(cookie)

        sleep(5*random.random()+2)
        browser.refresh()
        sleep(10*random.random()+2)

        # Избавимся от уведомления об использовании cookie
        WebDriverWait(browser, 10*random.random()).until(expected_conditions.visibility_of_element_located((By.XPATH, follow_path)))
        browser.find_element(By.XPATH,acsept_cookies).click()
        
        # Кликнем - Подписаться
        WebDriverWait(browser, 15*random.random()).until(expected_conditions.visibility_of_element_located((By.XPATH, follow_path)))
        browser.find_element(By.XPATH,follow_path).click()

        sleep(20)
        browser.close()
        browser.quit()

    def like_and_retwit():
        pass

