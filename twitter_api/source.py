from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pickle
from secret import follow_path, acsept_cookies, first_retwit_path, second_retwit_path, like_path 
from secret import BROWSER_PATH


options = webdriver.ChromeOptions()

# changing user-agent
# options.add_argument(f"user-agent={UserAgent(browsers=['chrome']).random}")
options.add_argument(f"user-agent=asdfg")

options.add_argument('--incognito')

# make it human
options.add_argument("--disable-blink-features=AutomationControlled")

# for Networks list parsing
options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}) 


class TwitterBot():

    def __init__(self,login:str, name:str, password:str, phone_number:str,headless:bool=False):
        
        ''' First four parametres is needed for authorisation to get or update cookies for
            twitter account.
            
            Headless parametr is responsible for adding headless mode to the options of webdriwer.
            With it there will be no poping up browser windows and code will be faster in general
        '''

        self.login = login
        self.name = name
        self.password = password
        self.phone_number = phone_number
        
        if headless: # Добавление аргумента для работы без открытия браузерного окна

            # executing without browser opening
            options.add_argument("--headless")

        else:
            pass

        self.bot = Chrome(BROWSER_PATH,options=options)

    


    def get_cookies(self):
        
        ''' Authorise in Twitter for getting cookies of this account.
            This cookie-files will be used in another operation to make them faster
            Cookie-files will be saved in /cookie folder, named like {account_login}_cookes
        '''

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
        pickle.dump(browser.get_cookies(), open(f"C:/Users/Mans/Downloads/twitter_api/cookies/{self.login}_cookies", "wb")) 
        print("🍪Cookies received!🍪")

        browser.close()
        browser.quit()





    def follow(self, url:str):
        
        ''' It could follow to the given twitter account
            using taken cookies.
        '''
        browser = self.bot
        browser.get(url)
        sleep(random.random()+2)

        for cookie in pickle.load(open(f"C:/Users/Mans/Downloads/twitter_api/cookies/{self.login}_cookies", "rb")):
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




    def like_and_retwit(self, follow:bool=False):
        
        ''' This method can be used to solve all the competition tasks given on Premint.com by Kaoryu Tamago.
            It could like and retwit twitter post which is actual for competition now. To do this it doesn't need 
            any other parameters or any user intervensions - all needed data code will receice on 'premint.xyz/kaoryu-tamago/' website. 
            
            It also could  follow to the twitter account of competiotion creator if it's nessecary. follow parametr is responcible for this.       
        '''
        
        browser = self.bot
        browser.get('https://www.premint.xyz/kaoryu-tamago/')
        sleep(2+random.random())

        tweet_link = browser.find_element(By.LINK_TEXT, 'this tweet').get_attribute('href')
        
        
        channel_link_items = browser.find_elements(By.CLASS_NAME, 'c-base-1')
        channel_link = channel_link_items[2].get_attribute('href')

        browser.get(channel_link)
        sleep(3*random.random())

        for cookie in pickle.load(open(f"C:/Users/Mans/Downloads/twitter_api/cookies/{self.login}_cookies", "rb")):
            browser.add_cookie(cookie)
        sleep(3*random.random())

        browser.refresh()
        sleep(2+random.random())

        if follow:

            try:
                WebDriverWait(browser, 15*random.random()).until(expected_conditions.visibility_of_element_located((By.XPATH, follow_path)))
                browser.find_element(By.XPATH, follow_path).click()
                sleep(random.random())
                
                print('Follow complete')

            except:
                print('Follow items not found!')     
        
        else:
            print("Following isn't nessesary")

        browser.get(tweet_link)
        sleep(3+random.random())

        # Избавимся от уведомления об использовании cookie
        WebDriverWait(browser, 10*random.random()).until(expected_conditions.visibility_of_element_located((By.XPATH, acsept_cookies)))
        browser.find_element(By.XPATH,acsept_cookies).click()
        
        
        browser.execute_script(f"window.scrollTo({random.randint(0, 29)},{502+random.randint(305, 467)})")
        sleep(3+5*random.random())

        try:
            items = browser.find_elements(By.CLASS_NAME, "r-1srniue")
            print('Items found')

            try:
                # Ретвитнем пост
                items[1].click() 
                sleep(random.random())

                # Подтвердим ретвит
                WebDriverWait(browser, 5).until(expected_conditions.visibility_of_element_located((By.XPATH, second_retwit_path)))
                browser.find_element(By.XPATH,second_retwit_path).click()
                print('Retwit complete')

                sleep(2*random.random())
                
            except:
                print("Retwit error!")   

            try:
                # Лайкнем пост
                items[2].click() 
                sleep(random.random())
                print('Like complete')

                sleep(2*random.random())
                
            except:
                print("Like error!")
        
        except:
            print('Items not found!')
        
        # Завершив подготовку - авторизуемся в конкурсе 
        browser.get('https://www.premint.xyz/kaoryu-tamago/')
        sleep(10+random.random())
        
        try:
            # Попытка регистрации
            button_items = browser.find_elements(By.CLASS_NAME,'btn')
            button_items[5].click()

            sleep(10 + 5*random.random())
            print('Premint.xyz authorisation complete')

        except:
            print("Let's authorise by Twiter")
            # Необходимо авторизоваться через Twitter
            try:
                # Входим на страницу авторизации
                browser.get('https://www.premint.xyz/login/?next=/kaoryu-tamago/')
                sleep(5 + 5*random.random())
                
                # Выбираем авторизацию черех Twitter
                browser.find_elements(By.CLASS_NAME,'fa-twitter').click()
                sleep(5+random.random())

                # Новая попытка регистрации
                browser.get('https://www.premint.xyz/kaoryu-tamago/')
                sleep(6+random.random())

                button_items = browser.find_elements(By.CLASS_NAME,'btn')
                button_items[5].click()

                sleep(10 + 5*random.random())
                print('Premint.xyz authorisation complete')
            
            except:
                print("Premint.xyz not authorised!")

        sleep(15+random.random())
        browser.close()
        browser.quit()



