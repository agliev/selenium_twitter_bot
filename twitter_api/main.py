from source_update import Twitter 
from source_update import Premint, Connect2Proxy
import pandas as pd
from time import sleep
import random
from os import listdir


import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    




def main():

        premint_urls = pd.read_excel('dependents/Premint_urls.xlsx')     
        premint_urls = premint_urls[(premint_urls['Done']==0) & (premint_urls['Discord_operations']==0)]
        premint_urls = premint_urls.sample(frac=1)[:3]

        
        # Реристрация на полученные Premint-ы
        for row in premint_urls.iterrows():
                _, values = row

                premint_url = values[0]
                follow_list = values[1].split(',')
                
                
                accounts_df = pd.read_excel('dependents/cred_df.xlsx').sample(frac=1)

                for row in accounts_df.iterrows():    
                    
                    try:
                        _, credentials = row

                        tw_login, tw_password, tw_mail = credentials[:3]
                        tw_phone = credentials[4]
                        
                        proxy_host, proxy_port, proxy_user, proxy_password = credentials[5:9]
                        user_agent = credentials[9]

                        
                        proxy_connector = Connect2Proxy( proxy_host,
                                                        proxy_port,
                                                        proxy_user,
                                                        proxy_password,
                                                        user_agent)

                        twitter_bot = Twitter(tw_login, tw_password, tw_mail, tw_phone, premint_url)
                        
                        premint_bot = Premint(premint_url, tw_login)
                        

                        if f'twitter_{twitter_bot.tw_login}_cookies' in listdir('cookies/twitter_cookies'):
                            browser = proxy_connector.get_undetected_chromedriver()
                        else:
                            # Получим cookie файлы при необходимости
                            browser = twitter_bot.get_cookies(proxy_connector)


                        # Twitter авторизация
                        browser.get('https://twitter.com')
                        browser = twitter_bot.authorise(browser=browser)
                        sleep(8+random.random())

                        
                        # Авторизуемся на Premint.xyz через Twitter
                        twitter_auth_complete, browser = premint_bot.authorise(browser)
                        sleep(5+random.random())

                        # Подпишемся на приведенные Twitter аккаунты
                        browser = twitter_bot.follow(browser, follow_list)
                        sleep(4+random.random())

                    # Авторизуемся в Twitter и попробуем лайкнуть & репостнуть твит
                        like_retweet_complete, browser = twitter_bot.like_and_retwit(browser)
                        sleep(1+2*random.random())

                        if like_retweet_complete==False:

                            # Авторизуемся в Twitter и попробуем лайкнуть & репостнуть твит снова 
                            _, browser = twitter_bot.like_and_retwit(browser)
                            sleep(1+2*random.random())
                        
                
                        # Зарегистрируемся на раздачу на Alphabot.app 
                        premint_bot.premint_register(browser, twitter_auth_complete)
                        
                        # Ожидание между аккаунтами для одного преминта
                        sleep(30+30*random.random())

                    except:
                         print(f'Error occured - when {twitter_bot.tw_login} registring {premint_bot.premint_url}')
                
                # Ожидание между сменой преминтов
                sleep(60 + 300*random.random())
            

if __name__ == '__main__':
    main()


    