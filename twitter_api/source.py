import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import random
import pickle
import zipfile
from secret import follow_path, acsept_cookies, second_retwit_path
from secret import manifest_json, background_js
from secret import BROWSER_PATH
from secret import user_agents


def get_chromedriver(use_proxy=False, user_agent=None):
        chrome_options = webdriver.ChromeOptions()

        if use_proxy:
            plugin_file = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)
                zp.writestr('background.js', background_js)
            
            chrome_options.add_extension(plugin_file)
        
        if user_agent:
            chrome_options.add_argument(f'--user-agent={user_agent}')

        s = Service(
            executable_path=BROWSER_PATH
        )
        driver = webdriver.Chrome(
            service=s,
            options=chrome_options
        )

        return driver





class TwitterBot():

    def __init__(self,login:str, name:str, password:str, phone_number:str, use_proxy=False, user_agent=None):

        self.login = login
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.bot = get_chromedriver(use_proxy=use_proxy, user_agent=user_agent)

    def get_cookies(self):

        browser = self.bot
        
        # Открываем сайт авторизации    
        browser.get('https://twitter.com/login')
        print("Passing through authentication...")
        

        # Вводим логин 
        login_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input' 
        sleep(5+random.random())

        browser.find_element(By.XPATH, login_xpath).clear()
        browser.find_element(By.XPATH, login_xpath).send_keys(self.login)
        browser.find_element(By.XPATH, login_xpath).send_keys(Keys.ENTER)
        

        # Вводим имя пользователя   
        try:
            name_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input' 
            sleep(2+random.random())

            browser.find_element(By.XPATH,name_xpath).clear()
            browser.find_element(By.XPATH,name_xpath).send_keys(self.name)
            browser.find_element(By.XPATH,name_xpath).send_keys(Keys.ENTER)
            
        except:
            pass   

        # Вводим пароль 
        pass_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input' 
        sleep(3+random.random())

        browser.find_element(By.XPATH,pass_xpath).clear()
        browser.find_element(By.XPATH,pass_xpath).send_keys(self.password)
        browser.find_element(By.XPATH,pass_xpath).send_keys(Keys.ENTER)
        

        # На случай проверки телефона 
        try: 
            phone_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input' 
            sleep(2+random.random())

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
        
        browser = self.bot
        browser.get(url)
        sleep(5+random.random())

        for cookie in pickle.load(open(f"C:/Users/Mans/Downloads/twitter_api/cookies/{self.login}_cookies", "rb")):
            browser.add_cookie(cookie)

        sleep(5*random.random()+2)
        browser.refresh()
        sleep(10*random.random()+2)

        # Избавимся от уведомления об использовании cookie
        browser.find_element(By.XPATH,acsept_cookies).click()
        sleep(2+random.random())

        # Кликнем - Подписаться
        browser.find_element(By.XPATH,follow_path).click()

        return browser




    def like_and_retwit(self, premint_url:str, follow:bool=False, mult_follow:bool=False, follow_list=[]):
        
        browser = self.bot
        # browser.get('https://2ip.ru/')
        # sleep(1+random.random())

        browser.get(premint_url)
        sleep(5+random.random())

        tweet_link = browser.find_element(By.LINK_TEXT, 'this tweet').get_attribute('href')
        
        
        channel_link_items = browser.find_elements(By.CLASS_NAME, 'c-base-1')
        channel_link = channel_link_items[3].get_attribute('href')

        browser.get(channel_link)
        sleep(3+3*random.random())

        for cookie in pickle.load(open(f"C:/Users/Mans/Downloads/twitter_api/cookies/{self.login}_cookies", "rb")):
            browser.add_cookie(cookie)
        sleep(3*random.random())

        browser.refresh()
        sleep(6+2*random.random())

        if follow:
            
            if mult_follow:
                
                for channel_name in follow_list:
                    browser.get('https://twitter.com/'+channel_name)
                    sleep(4+random.random())

                    browser.find_element(By.XPATH, follow_path).click()
                    sleep(1+random.random())
                    
                    print(f'{channel_name} follow complete')



            else:
                try:
                    browser.find_element(By.XPATH, follow_path).click()
                    sleep(1+random.random())
                    
                    print('Follow complete')

                except:
                    print('Follow items not found!')   

            
        
        else:
            print("Following isn't nessesary")

        browser.get(tweet_link)
        sleep(6+random.random())

        try:
            # Избавимся от уведомления об использовании cookie
            browser.find_element(By.XPATH,acsept_cookies).click()
        except:
            pass    
        
        browser.execute_script(f"window.scrollTo({random.randint(0, 29)},{352+random.randint(305, 353)})")
        sleep(3+random.random())

        try:
            items = browser.find_elements(By.CLASS_NAME, "r-1srniue")
            print('Items found')

            try:
                # Ретвитнем пост
                items[1].click() 
                sleep(2+random.random())

                # Подтвердим ретвит
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
        
        sleep(3)
        return browser

    

    def premit_register(self, premint_url:str, browser):    

            # Завершив подготовку - авторизуемся в конкурсе 
            browser.get(premint_url)
            sleep(5*random.random()+5)                          
        
            print("Let's authorise by Twiter")

            # Регистрируемся в Premint при помощи Twitter аккаунта 
            try: 
                channel_name = premint_url.split("www.premint.xyz/")[1]
                browser.get(f'https://www.premint.xyz/login/?next=/{channel_name}')
                sleep(5+random.random())

            
                print('Starting Premint authorisation')
                        
                # Кликнем авторизоваться через Twitter 
                browser.find_element(By.PARTIAL_LINK_TEXT, 'Twitter').click()
                sleep(10*random.random()+2)

                auth_window_opened = True

            except:
                auth_window_opened = False
                print('Could not find "Login with Twitter" button!')

                    
            if auth_window_opened:

                    try:
                        sleep(7+random.random())
                            
                        try:
                            # Кликнем войти
                            browser.find_element(By.CLASS_NAME, 'submit').click()
                            sleep(2+random.random())

                            # Введем логин и пароль от Твиттер акканунта

                            try:
                                # Login
                                browser.find_element(By.CLASS_NAME, 'r-30o5oe').send_keys(self.login)
                                sleep(2*random.random())
                                browser.find_element(By.CLASS_NAME, 'r-30o5oe').send_keys(Keys.ENTER)
                                sleep(5)
                                print('Login complete')

                                # Password
                                browser.find_element(By.NAME, 'password').send_keys(self.password)
                                sleep(2*random.random())

                                browser.find_element(By.NAME, 'password').send_keys(Keys.ENTER)    
                                sleep(2*random.random())
                                print('Password complete')

                                print('Premint authorisation complete')

                                twitter_auth_complete = True

                            except:
                                print('Last Twitter login Error!')
                                twitter_auth_complete = False
                                
                            
                        except:
                            twitter_auth_complete = False

                            # post Twitter authorisation Premint.com registration
                            sleep(3+random.random())

                            browser.execute_script(f"window.scrollTo({random.randint(102, 131)},{random.randint(502, 531)})")
                            sleep(4+random.random())
                                            
                            browser.find_element(By.ID,'register-submit').click()
                            sleep(10 + 5*random.random())

                            print(f'Premint.xyz/{channel_name} registration complete') 

                    except:
                        twitter_auth_complete = False
                        print('Could not send Login and Password for Twitter authorisation!')

            if twitter_auth_complete:
                
                # post Twitter authorisation Premint.com registration
                sleep(3+random.random())

                browser.execute_script(f"window.scrollTo({random.randint(102, 131)},{random.randint(502, 531)})")
                sleep(3+random.random())
                            
                browser.find_element(By.ID,'register-submit').click()
                sleep(10 + 5*random.random())

                print(f'Premint.xyz/{channel_name} registration complete') 

            else:
                pass

            sleep(10)
            browser.close()
            browser.quit()

    
