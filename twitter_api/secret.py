import pandas as pd

# LOGIN = ''
# PASSWORD = ''
# NAME = ''
# PHONE_NUMBER = ''

TWITTER_URL = 'https://twitter.com/login'


follow_path = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/span/span'
acsept_cookies = '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[1]/div/span/span'
first_retwit_path = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[2]/span/span/span'
second_retwit_path = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/span'
like_path = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[2]/span/span/span'

user_agents = list(pd.read_csv('dependents/user_agents.csv')['User_Agent'])

# IPv4 ПРОКСИ
PROXY_HOST = ''
PROXY_PORT = ''
PROXY_USER = ''
PROXY_PASS = ''




dis_login = 'mansur.agliev.87@mail.ru'
dis_password = '5cool55cool5M'




manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"76.0.0"
}
"""


background_js_part = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
); """ 
