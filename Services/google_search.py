from googlesearch import search
from bs4 import BeautifulSoup
import requests
import string
import lxml

def chatbot_query(searchQuestion):

	question = searchQuestion.replace(' ', '+')
	URL = f"https://google.com/search?q={question}"

	headers = {
	    'User-Agent':
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
	}
	r = requests.get(URL, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')

	result = soup.find('div', class_='Z0LcW XcVN5d') or soup.find(
	    'div', class_='Pb0vac') or soup.find(
	        'div', class_="Z0LcWXcVN5d AZCkJd") or soup.find(
	            'div', class_="Z0LcW XcVN5d AZCkJd") or soup.find(
	                'div', class_="DCiuzf") or soup.find(
	                    'div', class_="gsrt vk_bk dDoNo FzvWSb XcVN5d DjWnwf")
	# print(result.text)
	return result.text
	# 14 June 1946 (age 71)

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