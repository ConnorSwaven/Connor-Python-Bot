from googlesearch import search
from bs4 import BeautifulSoup
import requests
import string
from youtubesearchpython import VideosSearch
import random
import time
import urllib.request
import validators
import os

from googleapiclient.discovery import build

def image_search(query, filtered):

    cxvalue = os.getenv('IMAGECX')
    rightsvalue = 'cc_publicdomain cc_attribute cc_sharealike cc_noncommercial cc_nonderived'
    if filtered == False:
      cxvalue = os.getenv('IMAGECXNOFILTER')
      rightsvalue = ''

    service = build("customsearch", "v1",
               developerKey=os.getenv('GOOGLEAPIKEY'))
    
    res = service.cse().list(
         q=query, #'lectures',
         cx=cxvalue,
         searchType='image',
         rights=rightsvalue,
       ).execute()

    urls = [item['link'] for item in res['items']]
    print(urls)
    return random.choice(urls)


def findImage(array):
  for v in range(10):
      url = random.choice(array)
      if validators.url(url):
        return url
  return "Image cannot be found"

def image_search2(searchTerm, filtered):
  random.seed(time.time())

  urlKeyword = urllib.parse.quote(searchTerm)
  url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
  if filtered: 
    url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=on&tbm=isch'

  # headers is necessary when you send request
  headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}

  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, 'lxml')
  images = []
  for img in soup.findAll('img'):
    images.append(img.get('src'))

  randomurl = findImage(images)
  return randomurl





# Search youtube and respond with first result
def youtube_search(message):
  print(message)
  videosSearch = VideosSearch(message, limit = 2)
  videosResult = videosSearch.result()
  videosResult = videosResult["result"][0]["link"]
  print(videosResult)
  return videosResult

# Get anarray of top 10 links from a search
def get_links(searchQuestion):
  links = []
  for j in search(searchQuestion, tld="co.in", num=10, stop=10, pause=1): 
    links.append(j) 
  return links

# Find if Google has responded within its "box" from search engine
def chatbot_query(searchQuestion):

	question = searchQuestion.replace(' ', '+')
	URL = f"https://google.com/search?q={question}"

	headers = {
	    'User-Agent':
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
	}
	r = requests.get(URL, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')

	result = soup.find('div', class_="sXLaOe") or soup.find('div', class_='Z0LcW XcVN5d') or soup.find(
	    'div', class_='Pb0vac') or soup.find(
	        'div', class_="Z0LcWXcVN5d AZCkJd") or soup.find(
	            'div', class_="Z0LcW XcVN5d AZCkJd") or soup.find(
	                'div', class_="DCiuzf") or soup.find(
	                    'div', class_="gsrt vk_bk dDoNo FzvWSb XcVN5d DjWnwf")
	# print(result.text)
	return result.text
	# 14 June 1946 (age 71)

# Try to scrape website data from search results
def chatbot_query2(query, index=0):
	#fallback = str(english_bot.get_response(query)) # 'Sorry, I cannot think of a reply for that.'
	result = ''

	try:
		search_result_list = list(
		    search(query, tld="co.in", num=10, stop=3, pause=0.8))

		page = requests.get(search_result_list[index])

		soup = BeautifulSoup(page.content, features="lxml")

		article_text = ''
		article = soup.findAll('p')
		for element in article:
			article_text += '\n' + ''.join(element.findAll(text=True))
		article_text = article_text.replace('\n', '')

		first_sentence = article_text.split('.')
		first_sentence = first_sentence[0].split('?')[0]

		chars_without_whitespace = first_sentence.translate(
		    {ord(c): None
		     for c in string.whitespace})

		if len(chars_without_whitespace) > 0:
			result = first_sentence
		else:
			result = ""

		return result
	except Exception as err:
		print(err)
		if len(result) == 0: result = ""
		return result