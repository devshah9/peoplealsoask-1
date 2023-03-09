import json
import os
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from requests import request
import http.client



conn = http.client.HTTPSConnection("api.scrapingant.com")


scrapDataDict= {}



pixaBayList = []
pexelsList = []
unSplashList = []
googleImagesList = []
searchVideoList = []

def parse_search_results(query):
    """parse search results from google search page"""
    
    url = f"https://www.google.com/search?hl=en&q={quote(query)}"
    url = str(quote(url)).replace('/', '%2F')


    conn.request("GET", f"/v2/general?url={url}&x-api-key=8a4f454e6520437fbc48feaf1aa04bdd&browser=false")

    

    res = conn.getresponse()
    data = res.read()
    
    soup = BeautifulSoup(data.decode("utf-8"), "html.parser")


    results = []
    for i in soup.find_all('div',{'class': 'g'}):
        title = i.find('h3', {'class': 'LC20lb MBeuO DKV0Md'})
        url = i.find('a')['href']
        if title is not None:
            results.append({'title':title, 'url':url})
    return results


def scrape_video_search(query: str, page=1, country="US"):
    try:
        """scrape image results for a given keyword"""
        url = f'https://www.youtube.com/results?search_query={query}'
        
        url = str(quote(url)).replace('/', '%2F')

    
        conn.request("GET", f"/v2/general?url={url}&x-api-key=8a4f454e6520437fbc48feaf1aa04bdd&browser=false")

    

        res = conn.getresponse()
        data = res.read()
    
        soup = BeautifulSoup(data.decode("utf-8"), "html.parser")




    
        results = soup.select("script")
        
        for div in results:
            if str(div.text).startswith('var ytInitialData'):
                youtube_urls = []
                json_object = json.loads(str(div.text)[20:-1])
                new_list = json_object['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
                for i in new_list:
                    if 'videoRenderer' in i:
                        title = i['videoRenderer']['title']['runs'][0]['text']
                        url_id = i['videoRenderer']['videoId']
                        url = 'https://www.youtube.com/watch?v=' + url_id
                        youtube_urls.append({'title':title, 'url':url})
        print(youtube_urls)
        return youtube_urls
    except Exception as e:
        print(e)
        return youtube_urls

def parse_people_also_ask(query):

    url = f"https://www.google.com/search?hl=en&q={quote(query)}"
    url = str(quote(url)).replace('/', '%2F')

    conn.request("GET", f"/v2/general?url={url}&x-api-key=8a4f454e6520437fbc48feaf1aa04bdd&browser=false")

    res = conn.getresponse()
    data = res.read()

    new_list = []
    soup = BeautifulSoup(data.decode("utf-8"), "html.parser")
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    for i in soup.select(".related-question-pair span"):

        new_list.append({'que': i.get_text(strip=True), 'ans': ''})
    return new_list

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
        if 'hits' in apiResponse and len(apiResponse['hits']) > 1:
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


def googleImages(query):
    global googleImagesList
    googleImagesList = []

    url = f"https://www.google.com/search?hl=en&q={query}&source=lnms&tbm=isch"
    url = str(quote(url)).replace('/', '%2F')

    
    conn.request("GET", f"/v2/general?url={url}&x-api-key=8a4f454e6520437fbc48feaf1aa04bdd&browser=false")

    

    res = conn.getresponse()
    data = res.read()
    
    soup = BeautifulSoup(data.decode("utf-8"), "lxml")
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
    
    # Print the URLs of the images
    for url in list(filter(None, img_urls)):
        googleImagesList.append(url)
    



def parse_related_search(query):


    url = f"https://www.google.com/search?hl=en&q={quote(query)}"
    url = str(quote(url)).replace('/', '%2F')


    conn.request("GET", f"/v2/general?url={url}&x-api-key=8a4f454e6520437fbc48feaf1aa04bdd&browser=false")

    

    res = conn.getresponse()
    data = res.read()
    
    soup = BeautifulSoup(data.decode("utf-8"), "html.parser")

    with open("output.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    results = []
    related_search = soup.find('div', {'class': 'y6Uyqe'})
    a = related_search.find_all('a')
    for i in a:
        print(i.text)
        results.append(i.text)
    return results

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
    query = key_word
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
        scrapDataDict['pixabay_images'] = pixaBayList[:10]
    if pexelKeyWord:
        apiPexelsCom(key_word)
        scrapDataDict['pexels_images'] = pexelsList[:10]
    if unSplashKeyWord:
        apiUnSplashCom(key_word)
        scrapDataDict['unsplash_images'] = unSplashList[:10]
    if googleKeyWord:
        googleImages(query)
        scrapDataDict['google_images_videos']['google_images_urls'] = googleImagesList[:10]


    if paaKeyWord:
        scrapDataDict['g_questions_answers']['g_que_ans'] = parse_people_also_ask(query)[:numOfTimes]
            
    if relatedKeyWord:
        scrapDataDict['related_searches'] = parse_related_search(query)[:10]

    if serpKeyWord:
        scrapDataDict['google_search_results'] = parse_search_results(query)[:10]

    if youTubeKeyWord:
        videos = scrape_video_search(query)
        scrapDataDict['google_images_videos']['youtube_urls'] = videos


    print('asdjfpoadsfoi')    
    return scrapDataDict

