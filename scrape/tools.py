
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup


def get_soup(url, post_data=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    try:
        if post_data:
            resp = requests.post(url, headers=headers, data=post_data)
        else:
            resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'lxml')
            if soup:
                return soup
    except:
        print('get soup failed.')

    return None


def get_chrome(url, driver=r'c:\webdriver\chromedriver', hide=False):
    try:
        options = None
        # 設定是否隱藏
        if hide:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
        chrome = webdriver.Chrome(driver, options=options)
        # 設定最大等待秒數
        chrome.implicitly_wait(10)
        chrome.get(url)
        return chrome
    except Exception as e:
        print(e)

    return None


def getSoupWithChrome(url, path='c:/webdriver/chromedriver', hide=False):
    option = webdriver.ChromeOptions()
    if hide:
        option.add_argument('--headless')

    try:
        chrome = webdriver.Chrome(path, options=option)
        chrome.implicitly_wait(10)
        chrome.get(url)
    except:
        return 'get webdriver error.'

    soup = None
    if chrome != None:
        soup = BeautifulSoup(chrome.page_source, 'lxml')
        chrome.quit()
    return soup


def getSoup(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    if resp.status_code == 200:
        return BeautifulSoup(resp.text, 'lxml')

    return None


def getWebDriver(url, option=None, wait=10):

    if option != None:
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')

    try:
        chrome = webdriver.Chrome(r'c:\webdriver\chromedriver', options=option)
        chrome.implicitly_wait(wait)
        chrome.get(url)

        return chrome
    except:
        return None


def getYoutubeData(url, key):
    xpath = r'/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input'

    chrome = getWebDriver(url)

    if chrome != None:
        youtube_input = chrome.find_element_by_xpath(xpath)
        youtube_input.clear()
        youtube_input.send_keys(key+'\n')

        time.sleep(3)

        soup = BeautifulSoup(chrome.page_source, 'lxml')

        links = soup.find_all(id="video-title")

        datas = []

        for link in links:
            if link != None:
                try:
                    print(link.text.strip())
                    print(url+link.get('href'))
                    datas.append([link.text.strip(), url+link.get('href')])
                except Exception as e:
                    print(e)

        chrome.quit()

        return datas


if __name__ == '__main__':
    #url = 'https://www.youtube.com'
    #print(getYoutubeData(url, '周杰倫'))
    pass
    URL = 'https://www.yahoo.com.tw/'
    print(getSoup(URL))
    # sendEmail('iiiplay001@gmail.com',"test1","test2");
