import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from seleniumwire import webdriver as seleniumwire_webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import random
import pickle
import zipfile
from secret import follow_path, acsept_cookies, second_retwit_path
from secret import manifest_json, background_js_part
from secret import user_agents


class Twitter():

    def __init__( self,
                  tw_login:str,
                  tw_password:str,
                  tw_mail:str, 
                  tw_phone:str,
                  premint_url:str):

        self.tw_login = tw_login
        self.tw_password = tw_password
        self.tw_mail = tw_mail
        self.tw_phone = tw_phone
        self.premint_url = premint_url
    
    def authorise(self,
                  browser:webdriver,
                  first_time_auth:bool=False):

        '''Авторизация в Twitter c использованием cookie'''
        
        if first_time_auth:

            browser.get('https://twitter.com/')
            sleep(1.5+random.random())
        
        for cookie in pickle.load(open(f"cookies/twitter_cookies/twitter_{self.tw_login}_cookies", "rb")):
            browser.add_cookie(cookie)

        sleep(2*random.random()+1)
        browser.refresh()
        sleep(3*random.random()+1)
        
        return browser
    

    def like(self, items:list):
    
        '''Лайк поста через найденную заранее кнопку - items[2]'''

        try:
            # Лайкнем пост
            items[2].click() 
            sleep(random.random())
            print('Like complete')

            sleep(2*random.random())
                        
        except:
            print("Like error!")


    def repost(self, browser:webdriver, items:list):

        '''Репост через найденную заранее кнопку - items[1]'''

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

    def get_cookies(self, browser:webdriver):

        "Получение cookie файлов через авторизацию логином и паролем"

        # Открываем сайт авторизации    
        browser.get('https://twitter.com/login')
        print("Passing through authentication...")
        

        # Вводим логин 
        login_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input' 
        sleep(5+random.random())

        browser.find_element(By.XPATH, login_xpath).clear()
        browser.find_element(By.XPATH, login_xpath).send_keys(self.tw_login)
        browser.find_element(By.XPATH, login_xpath).send_keys(Keys.ENTER)
        

        # Вводим пароль 
        pass_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input' 
        sleep(1.5+random.random())

        browser.find_element(By.XPATH,pass_xpath).clear()
        browser.find_element(By.XPATH,pass_xpath).send_keys(self.tw_password)
        sleep(random.random())

        browser.find_element(By.XPATH,pass_xpath).send_keys(Keys.ENTER)
        sleep(3+random.random())

        # На случай проверки телефона 
        try: 
            phone_xpath = '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'

            browser.find_element(By.XPATH, phone_xpath).clear()
            browser.find_element(By.XPATH, phone_xpath).send_keys(self.tw_phone)
            sleep(random.random())

            browser.find_element(By.XPATH, phone_xpath).send_keys(Keys.ENTER)
            sleep(3+random.random())
        except:
            pass

        try:
            # На случай проверки почты
            browser.find_element(By.CLASS_NAME,'r-30o5oe').send_keys(self.tw_mail)
            sleep(random.random())

            browser.find_element(By.CLASS_NAME,'r-30o5oe').send_keys(Keys.ENTER)
            sleep(5+random.random())
        except:
            pass

        print('authentication complete!')

        # cookies
        sleep(4+random.random())
        pickle.dump(browser.get_cookies(), open(f"cookies/twitter_cookies/twitter_{self.tw_login}_cookies", "wb")) 
        print("🍪 Twitter Cookies received!🍪")

        return browser


    def follow(self, browser:webdriver, follow_list=[]):

        '''Подписка на указанный список Twitter аккаунтов'''
        
        browser.get('https://twitter.com/'+follow_list[0])
        sleep(3+random.random())

        try:
            browser.find_elements(By.CLASS_NAME,'css-18t94o4')[4].click()
            sleep(1)
        except:
            pass

        browser = self.authorise(browser)

        for channel_name in follow_list:
            
            try:

                browser.get('https://twitter.com/'+channel_name)
                sleep(5+random.random())

                browser.find_element(By.XPATH, follow_path).click()
                sleep(1+random.random())
                            
                print(f'{channel_name} follow complete')

            except:
                
                sleep(10+3*random.random())

                try:
                    browser.get('https://twitter.com/'+channel_name)
                    sleep(5+random.random())

                    if channel_name=='bonglo_eth':

                        browser.find_elements(By.CLASS_NAME, 'css-18t94o4')[2].click()
                    else:
                        pass

                    browser.find_element(By.XPATH, follow_path).click()
                    sleep(1+random.random())
                                
                    print(f'{channel_name} follow complete')
                
                except:
                    print(f'{channel_name} follow failed')

        return browser



    def like_and_retwit(self, browser:webdriver):
            
            
            browser.get(self.premint_url)
            sleep(10+random.random())

            try:
                tweet_link = browser.find_element(By.LINK_TEXT, 'this tweet').get_attribute('href')
                sleep(random.random())
                print(f'tweet url - {tweet_link}')
            except:
                pass
            
            
            
            try:

                try:


                    browser.get(tweet_link)
                    sleep(5+random.random())

                    try:
                        # Избавимся от уведомления об уведомлениях
                        closing_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div'
                        browser.find_element(By.XPATH, closing_xpath).click()

                    except:
                        pass

                    sleep(2+3*random.random())


                    browser = self.authorise(browser)
                    sleep(5+2*random.random())




                    try:
                            # Избавимся от уведомления об использовании cookie
                            browser.find_element(By.XPATH, acsept_cookies).click()
                    except:
                            pass  

    
                        
                    # Проверим, возможно пост небольшой и иконки почти видны
                    try: 
                        
                        
                            browser.execute_script(f"window.scrollTo({random.randint(0, 29)},{102+random.randint(30, 35)})")
                            sleep(5+random.random())

                            items = browser.find_elements(By.CLASS_NAME, "r-1srniue")
                            print('Items found')

                            self.repost(browser=browser, items=items) 
                            self.like(items)

                            like_retwit_complete = True
                            sleep(2.4+random.random())

                            channel_name = self.premint_url.split('/')[-2]
                            print(f'Like & Retweet completed for {channel_name}')

                            return like_retwit_complete, browser

                    except:
                        
                        try:
                            browser.execute_script(f"window.scrollTo({random.randint(0, 29)},{302+random.randint(30, 35)})")
                            sleep(5+random.random())

                            items = browser.find_elements(By.CLASS_NAME, "r-1srniue")
                            print('Items found')

                            self.repost(browser=browser, items=items) 
                            self.like(items)

                            like_retwit_complete = True
                            sleep(2.4+random.random())

                            channel_name = self.premint_url.split('/')[-2]
                            print(f'Like & Retweet completed for {channel_name}')

                            return like_retwit_complete, browser
                                            
                            
                            
                        
                        except:

                            try:
                                # Промотаем до появления иконок
                                print('Scrolling down')

                                browser.execute_script(f"window.scrollTo({random.randint(0, 29)},{402+random.randint(380, 401)})")
                                sleep(3+random.random())

                                
                                items = browser.find_elements(By.CLASS_NAME, "r-1srniue")
                                print('Items found')

                                self.repost(browser=browser, items=items) 
                                self.like(items)

                                
                                like_retwit_complete = True
                                sleep(2.4+random.random())

                                channel_name = self.premint_url.split('/')[-2]
                                print(f'Like & Retweet completed for {channel_name}')

                                return like_retwit_complete, browser
                        
                            except:

                                channel_name = self.premint_url.split('/')[-2]
                                print(f'Like & Retweet failed for {channel_name}')  

                                like_retwit_complete = False
                                sleep(2.4+random.random())

                                return like_retwit_complete, browser
                                            


                    
                except:
                    channel_name = self.premint_url.split('/')[-2]
                    print(f'Like & Retweet failed for {channel_name}') 

                    like_retwit_complete = False
                    sleep(2.4+random.random())

                    return like_retwit_complete, browser
            
            except:

                like_retwit_complete = True

                print(f'{self.premint_url} already registred for {self.tw_login}!')
                sleep(2.4+random.random())

                return like_retwit_complete, browser
    




class Discord():

    def __init__(self,
                 dis_login:str,
                 dis_password:str):

        self.dis_login = dis_login
        self.dis_password = dis_password


    def discord_authorise(self,
                          browser:webdriver):

        browser.get('https://discord.com/login')
        sleep(2+random.random())

        
        browser.find_elements(By.CLASS_NAME,'inputDefault-Ciwd-S')[0].send_keys(self.dis_login)
        sleep(1.5+random.random())    

        browser.find_elements(By.CLASS_NAME,'inputDefault-Ciwd-S')[1].send_keys(self.dis_password)
        sleep(0.5+random.random())
        
        browser.find_elements(By.CLASS_NAME,'inputDefault-Ciwd-S')[1].send_keys(Keys.ENTER)
        sleep(0.5+random.random())
        print('authentication complete!')

        return browser


class Premint():

    def __init__(self,
                 premint_url:str,
                 tw_login:str):

        self.premint_url = premint_url
        self.tw_login = tw_login



    def authorise(self, browser:webdriver):
    
        # Регистрируемся в Premint при помощи Twitter аккаунта 
        channel_name = self.premint_url.split("www.premint.xyz/")[1]

        try: 
                
            browser.get(f'https://www.premint.xyz/login/?next=/{channel_name}')
            sleep(6+3*random.random())

                                    
            # Кликнем авторизоваться через Twitter 
            browser.find_element(By.PARTIAL_LINK_TEXT, 'Twitter').click()
            sleep(1.6+2*random.random())

            twitter_auth_complete = True
            print('Twitter connected')


        except:
            twitter_auth_complete = False
            print('Could not find "Login with Twitter" button!')

        return twitter_auth_complete, browser

    

    def premint_register(self, browser:webdriver, twitter_auth_complete:bool, discord_connect:bool=False):    

            # Завершив подготовку - авторизуемся в конкурсе 
            browser.get(self.premint_url)
            sleep(10+3*random.random())                          
        
            print("Let's authorise by Twiter")

        
            if twitter_auth_complete:
                
                # post Twitter and Discord authorisation Premint.com registration
                browser.get(self.premint_url)
                sleep(2+random.random()) 

                print('Starting connecting Discord to Rremint')

                if discord_connect:
                    try:
                        dis_connect_link = browser.find_elements(By.CLASS_NAME, 'btn-circle')[1].get_attribute('href')
                        print(dis_connect_link)

                        browser.get(dis_connect_link)
                        sleep(4+3*random.random())

                        print('lets activate second button')
                        browser.find_elements(By.CLASS_NAME, 'button-f2h6uQ')[1].click()
                        sleep(2+random.random())
                    except:
                        print('Discord connecting failed!')
                

                
                try:
                    browser.execute_script(f"window.scrollTo({random.randint(202, 231)},{random.randint(602, 631)})")
                    sleep(1+random.random())
                                
                    browser.find_element(By.ID,'register-submit').click()
                    sleep(2+random.random())

                    print(f'Premint.xyz/{channel_name} registration complete') 
                except:
                    print('Button was not active!')

            else:
                print('Registration failed on Twitter connecting stage!')

            sleep(3+random.random())
            browser.execute_script(f"window.scrollTo({random.randint(2, 31)},{random.randint(35, 64)})")
            sleep(1+random.random())

            channel_name = self.premint_url.split('/')[-2]
            browser.save_screenshot(f'screenshots/work_results/{self.tw_login}_{channel_name}_screen.png')
            sleep(1+random.random())


            browser.close()
            browser.quit()
            


class Connect2Proxy():

    def __init__(self,
                 proxy_host:str,
                 proxy_port:str,
                 proxy_user:str,
                 proxy_password:str,   
                 user_agent:str):
        
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_password = proxy_password
        self.user_agent = user_agent



    def get_undetected_chromedriver(self):
                     
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--user-agent={self.user_agent}')
        
        plugin_file = 'dependents/proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)

                background_js = background_js_part % (self.proxy_host, self.proxy_port, self.proxy_user, self.proxy_password)
                zp.writestr('background.js', background_js)
            
        chrome_options.add_extension(plugin_file)
        
    
        

        s = Service(
            executable_path='chromedriver.exe'
        )
        driver = webdriver.Chrome(
            service=s,
            options=chrome_options
        )

        return driver


    def get_seleniumwire_https(self):

        options = {
        'proxy': {
            'http': f'http://{self.proxy_user}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
            'https': f'http://{self.proxy_user}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
            'no_proxy': 'localhost,83.242.179.142' }
        }

        browser = seleniumwire_webdriver.Chrome(seleniumwire_options=options)

        return browser

    def get_undetected_seleniumwire_https(self):

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument(f'--user-agent={self.user_agent}')

        options = {
                'proxy': {
                        'http': f'https://{self.proxy_user}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                        'https': f'https://{self.proxy_user}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                        'no_proxy': 'localhost,83.242.179.142'
                    }, 
                'user_agent': self.user_agent
                }

        browser = uc.Chrome(
            options=chrome_options,
            seleniumwire_options=options
        )
        
        return browser

    def get_undetected_seleniumwire_socks(self):

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument(f'--user-agent={self.user_agent}')

        options = {
                'proxy': {
                        'http': f'socks5://{self.proxy_user}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                        'https': f'socks5://{self.proxy_user}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                        'no_proxy': 'localhost,83.242.179.142'
                    }, 
                'user_agent': self.user_agent
                }

        browser = uc.Chrome(
            options=chrome_options,
            seleniumwire_options=options
        )
        
        return browser