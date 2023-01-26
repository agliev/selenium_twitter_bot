from secret import LOGIN, NAME, PASSWORD, PHONE_NUMBER
from secret import user_agents
from source import TwitterBot
from random import choice

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

premint_url = 'https://www.premint.xyz/everybody-raffle/'
follow_list = ['everybodysfun','_foreversean' ]

def main(premint_url:str):
    
    bot = TwitterBot(LOGIN, NAME, PASSWORD, PHONE_NUMBER, use_proxy=True, user_agent=choice(user_agents))
    
    # Авторизуемся в Twitter и выполним условия раздачи
    browser = bot.like_and_retwit(premint_url,follow=True, mult_follow=True, follow_list=follow_list)

    # Зарегистрируемся на раздачу на Premint.com 
    bot.premit_register(premint_url,browser)

if __name__ == '__main__':
    main(premint_url)