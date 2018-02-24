import re
import requests
from bs4 import BeautifulSoup

youtube_url = "https://www.youtube.com/watch?v=%s"

def check(text):
	try:
		url = get_url_string(text) 
		
		if not url or not get_url(text):
			return False
		return True
	except:
		return False

def get_url_string(text):
	url = text.split("/download")
	
	if len(url) < 2:
		url = text.split("/d")

	return url[1].strip()

def check_url_re(url):
	regex = re.compile('^(?:http|ftp)s?://', re.IGNORECASE)
	return regex.match(url)

def is_short_url(url):
	regex = re.compile('https?:\/\/youtu.be\/(.+)')
	return regex.match(url)

def get_url(text):
	url = get_url_string(text)
	
	if not check_url_re(url):
		return None
	
	return url

def get_vId(url):
	short_url = is_short_url(url)

	if short_url:
		return short_url.group().split("/")[-1]

	regex = r"\?v=(.+)"
	matches = re.finditer(regex, url)
	
	for matchNum, match in enumerate(matches):
		return match.group()[3:]

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu	

def search_songs(query):
	result = {}
	html_content = requests.get("https://www.youtube.com/results?search_query=%s" % query)
	soup = BeautifulSoup(html_content.text, 'html.parser')
	res = soup.find_all('a', href = re.compile(r'/watch\?v=(.+)'))
	for i in res:
		url = i.get('href').strip().replace("/watch?v=", "")
		title = i.get("title")
		if title and not check_url_re(title):
			result[url] = {
				"url": url,
				"title": title
			}

	return list(result.values())[:5]


def get_query(text):
	try:	
		return text.split("/s")[1].strip()
	except:
		return False

