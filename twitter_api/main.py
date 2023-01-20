from secret import LOGIN, NAME, PASSWORD, PHONE_NUMBER
from source import TwitterBot


import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def main():
    
    bot = TwitterBot(LOGIN, NAME, PASSWORD, PHONE_NUMBER, headless=False)
    bot.like_and_retwit(follow=False)

if __name__ == '__main__':
    main()