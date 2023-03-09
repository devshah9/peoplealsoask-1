import json
import os
import time
import re

import requests
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from requests import request
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from webdriver_manager.chrome import ChromeDriverManager

pixaBayList = []
pexelsList = []
unSplashList = []
googleImagesList = []
searchVideoList = []


def apiCaller(url, headers):
    return json.loads(request("GET", url, headers=headers, data={}).text)


def apiPixaBayCom(keyWord):
    global pixaBayList
    pixaBayList = []
    try:
        apiUrl = f"https://pixabay.com/api/?key={os.environ.get('PIXABAY_KEY')}&min_width=640&image_type=photo&q={keyWord}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36",
        }
        apiResponse = apiCaller(apiUrl, headers)
        if 'hist' in apiResponse and len(apiResponse['hits']) > 1:
            pixaBayList.append(apiResponse['hits'][0].get('largeImageURL', ''))
            pixaBayList.append(apiResponse['hits'][1].get('largeImageURL', ''))
    except Exception as e:
        print(e)


def apiPexelsCom(keyWord):
    global pexelsList
    pexelsList = []
    try:
        apiUrl = f"https://api.pexels.com/v1/search?query={keyWord}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36",
            'Authorization': os.environ.get('PEXELS_KEY')
        }
        apiResponse = apiCaller(apiUrl, headers)
        if 'photos' in apiResponse and len(apiResponse['photos']) > 1:
            pexelsList.append(apiResponse['photos'][0]['src']['large'])
            pexelsList.append(apiResponse['photos'][1]['src']['large'])
    except Exception as e:
        print(e)


def apiUnSplashCom(keyWord):
    global unSplashList
    unSplashList = []
    try:
        apiUrl = f"https://api.unsplash.com/search/photos/?query={keyWord}&client_id={os.environ.get('UNSPLASH_KEY')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36",
        }
        apiResponse = apiCaller(apiUrl, headers)
        if 'results' in apiResponse and len(apiResponse['results']) > 1:
            unSplashList.append(apiResponse['results'][0]['urls']['regular'])
            unSplashList.append(apiResponse['results'][1]['urls']['regular'])
    except Exception as e:
        print(e)


def googleImages(keyword):
    global googleImagesList
    googleImagesList = []

    # Use the requests library to fetch the HTML of the Google Images search page
    url = "https://www.google.com/search?q={}&source=lnms&tbm=isch".format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    proxies = {"http": os.environ['PROXY_IP'], "https": os.environ['PROXY_IP']}
    response = requests.get(url, headers=headers, proxies=proxies)

    soup = BeautifulSoup(response.text, 'lxml')

    all_script_tags = soup.select("script")

    # https://regex101.com/r/eteSIT/1
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)
    
    # https://regex101.com/r/VPz7f2/1
    matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

    removed_matched_google_images_thumbnails = re.sub(
            r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    googleImagesList = [
            bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]


    img_tags = soup.find_all('img')
    img_urls = [img.get('data-src', None) for img in img_tags]
    print(url)

    # Print the URLs of the images
    for url in list(filter(None, img_urls)):
        googleImagesList.append(url)


def listMakerofSerp(driver):
    try:
        soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
        results = soup.find_all('div', {'class': 'g'})
        outputs = []
        for result in results:
            title_element = result.find("h3")
            link_element = result.find("a")
            if title_element and link_element:
                outputs.append({'title': title_element.text, 'url': link_element.get('href', "")})

        return outputs
    except Exception as e:
        print(e)
        return []


def get_video_results(key_word, driver):
    driver.get(f'https://www.youtube.com/results?search_query={key_word}')
    time.sleep(2)
    cnt = 5
    while cnt > 0:
        driver.execute_script(
            "var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        cnt -= 1
    youtube_data = []

    try:
        for result in driver.find_elements(By.CSS_SELECTOR, '.text-wrapper.style-scope.ytd-video-renderer'):
            title = result.find_element(By.CSS_SELECTOR, '.title-and-badge.style-scope.ytd-video-renderer').text
            link = result.find_element(By.CSS_SELECTOR,
                                       '.title-and-badge.style-scope.ytd-video-renderer a').get_attribute(
                'href')
            youtube_data.append({'title': title, 'url': link, })

        driver.quit()
        return youtube_data
    except Exception as e:
        driver.quit()
        print(e)
        return []


def listMakerofRelated(driver):
    relatedList = []
    for i in driver.find_elements(By.XPATH, """//div[@class="s75CSd OhScic AB4Wff"]"""):
        relatedList.append(i.text)
    return relatedList


def listMakerofPaa(driver, numOfTimes):
    uniqueList = []
    scrapDataPaa = []
    try:
        while True:
            if not driver.find_elements(By.XPATH, """//div[@jsname="F79BRe"]"""):
                break
            for data in driver.find_elements(By.XPATH, """//div[@jsname="F79BRe"]"""):
                if data.get_attribute("data-q") not in uniqueList:
                    if len(uniqueList) == int(numOfTimes):
                        return scrapDataPaa
                    answer = answerScraper(data.get_attribute("innerHTML"))
                    uniqueList.append(data.get_attribute("data-q"))
                    dataDict = {'que': data.get_attribute("data-q"), 'ans': answer}
                    scrapDataPaa.append(dataDict)
                    data.click()
                    time.sleep(2)
        return scrapDataPaa
    except Exception as e:
        print(e)
        return scrapDataPaa


def answerScraper(answerHtml):
    answerStr = ''
    soup = BeautifulSoup(answerHtml, 'html.parser')
    if soup.find('span', class_='hgKElc'):
        span = soup.find('span', class_='hgKElc')
        for string in span.strings:
            answerStr += string
    elif soup.find('ol', class_='X5LH0c'):
        ol = soup.find('ol', class_='X5LH0c')
        for string in ol.strings:
            answerStr += string
    elif soup.find('ul', class_='i8Z77e'):
        ul = soup.find('ul', class_='i8Z77e')
        for string in ul.strings:
            answerStr += string
    elif soup.find('div', class_='iKJnec'):
        div = soup.find('div', class_='iKJnec')
        for string in div.strings:
            answerStr += string
    elif soup.find('span', class_='XdBtEc'):
        span = soup.find('span', class_='XdBtEc')
        for string in span.strings:
            answerStr += string
    return answerStr


def mainScraper(keyWordList, numOfTimes, relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord,
                youTubeKeyWord, paaKeyWord, serpKeyWord):
    allScrapDataList = []
    for i in keyWordList:
        scrapDataDict = scraper(i, numOfTimes, relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord,
                                googleKeyWord, youTubeKeyWord, paaKeyWord, serpKeyWord)
        allScrapDataList.append(scrapDataDict)
    return allScrapDataList


def scraper(key_word, numOfTimes, relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord,
            youTubeKeyWord, paaKeyWord, serpKeyWord):
    key_word = key_word.replace(" ", "+")
    scrapDataDict = {'google_images_videos': {
        'google_images_urls': [],
        'youtube_urls': [],
    }, 'pixabay_images': [],
        'pexels_images': [],
        'unsplash_images': [],
        'g_questions_answers': {'g_que_ans': []},
        'related_searches': []

    }
    if pixaBayKeyWord:
        apiPixaBayCom(key_word)
        scrapDataDict['pixabay_images'] = pixaBayList
    if pexelKeyWord:
        apiPexelsCom(key_word)
        scrapDataDict['pexels_images'] = pexelsList
    if unSplashKeyWord:
        apiUnSplashCom(key_word)
        scrapDataDict['unsplash_images'] = unSplashList
    if googleKeyWord:
        googleImages(key_word)
        scrapDataDict['google_images_videos']['google_images_urls'] = googleImagesList

    if paaKeyWord or relatedKeyWord or serpKeyWord or youTubeKeyWord:  # Will only use proxy If paaKeyWord or relatedKeyWord
        try:
            display = Display(visible=False, size=(800, 600))
            display.start()
            options = Options()
            options.add_argument('--no-sandbox')
            options.headless = True
            proxyIpPort = os.environ['PROXY_IP']
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = proxyIpPort
            proxy.ssl_proxy = proxyIpPort
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['acceptInsecureCerts'] = True

            proxy.add_to_capabilities(capabilities)

            driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=options,
                desired_capabilities=capabilities
            )
            url = f"https://www.google.com/search?q={key_word}&gl=us"
            driver.get(url)

            time.sleep(2)

            # Accept Cookies part (it opens in incognito).
            if len(list(driver.find_elements(By.CLASS_NAME, "tHlp8d"))) == 5:
                list(driver.find_elements(By.CLASS_NAME, "tHlp8d"))[3].click()

            if paaKeyWord:
                scrapDataDict['g_questions_answers']['g_que_ans'] = listMakerofPaa(driver, numOfTimes)

            if relatedKeyWord:
                scrapDataDict['related_searches'] = listMakerofRelated(driver)

            # Check SERP Part
            if serpKeyWord:
                scrapDataDict['google_search_results'] = listMakerofSerp(driver)

            if youTubeKeyWord:
                videos = get_video_results(key_word,
                                           driver=webdriver.Chrome(ChromeDriverManager().install(),
                                                                   options=options,
                                                                   desired_capabilities=capabilities))
                scrapDataDict['google_images_videos']['youtube_urls'] = videos

        except Exception as e:
            print(e)

    return scrapDataDict
