from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import json
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pickle
from secrets import LOGIN, NAME, PASSWORD, PHONE_NUMBER
from secrets import follow_path, acsept_cookies, first_retwit_path, second_retwit_path, like_path 
from source import TwitterBot


import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


bot = TwitterBot(LOGIN, NAME, PASSWORD, PHONE_NUMBER)

# bot.authorise()

bot.follow('https://twitter.com/KaoryuTamago')



