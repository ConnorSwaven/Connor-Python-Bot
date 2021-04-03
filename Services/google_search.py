from googlesearch import search
from bs4 import BeautifulSoup
import requests
import string
from youtubesearchpython import VideosSearch

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