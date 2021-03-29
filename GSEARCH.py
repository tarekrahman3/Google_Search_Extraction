from requests_html import HTMLSession
from lxml import html
import pandas as pd
import random
import time

A = (
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
)
col0 = []
col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []

def test_no_result(response):
		try:
			test = response.html.xpath("//div[@class='card-section']/p").text
			import re
			if re.match('(?:did not match any documents)'):
				return print('no result')
		except:
			pass
		
		
def load_import_csv():
	df = pd.read_csv('imports.csv', header=0)
	google_search_urls = df.links.to_list()
	return google_search_urls

def start_request_session():
	session = HTMLSession()
	session.cookies.clear()
	return session	

def set_UA_headers_and_send_request(link, session):
	USER_AGENT = A[random.randrange(len(A))]
	headers = {"user-agent" : USER_AGENT}
	response = session.get(link, headers=headers)#, proxies=proxies)
	return response

def error_429_handle():
	time.sleep(120)
	session.cookies.clear()
	session.exit()
	session = HTMLSession()
	return session
	
def scrape(response, google_search_urls, each_link, index_num):	
	urls = response.html.xpath('//div[@class="yuRUbf"]/a/@href')
	titles = response.html.xpath('//div[@class="yuRUbf"]/a/h3')
	try:
		result_1_url = urls[0]
	except:
		result_1_url = 'None'
	try:
		result_2_url = urls[1]
	except:
		result_2_url = ''
	try:
		result_3_url = urls[2]
	except:
		result_3_url = ''
	try:
		result_1_title = titles[0].text
	except:
		result_1_title = 'None'
	try:
		result_2_title = titles[1].text
	except:
		result_2_title = ''
	try:
		result_3_title = titles[2].text
	except:
		result_3_title = ''
	col0.append(google_search_urls[each_link])
	col1.append(result_1_url)
	col2.append(result_2_url)
	col3.append(result_3_url)
	col4.append(result_1_title)
	col5.append(result_2_title)
	col6.append(result_3_title)
	print(f"{index_num} ^ [{result_1_title}]")

def sleep():
	time.sleep(10)

def create_dataframe():
	data = {'generated_urls': col0,
	'result_1_url':col1,
	'result_1_title':col4,
	'result_2_url':col2,
	'result_2_title':col5,
	'result_3_url':col3,
	'result_3_title':col6
	}
	df = pd.DataFrame(data, columns = ['generated_urls', 'result_1_url', 'result_1_title', 'result_2_url', 'result_2_title', 'result_3_url', 'result_3_title'])
	print(df)
	return df
	
def export_to_csv(df):
	df.to_csv('google_xport.csv')
