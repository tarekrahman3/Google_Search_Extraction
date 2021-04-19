from requests_html import HTMLSession
from lxml import html
import random
import time
import csv

A = (
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
)

def dict_csv_read():
	google_search_urls = []
	with open('imports.csv') as csv_file:
		reader = csv.DictReader(csv_file, delimiter=",")
		for row in reader:
			google_search_urls.append(row['links'])
	return google_search_urls

def start_request_session():
	session = HTMLSession()
	session.cookies.clear()
	return session	

def set_UA_headers_and_send_request(i, session):
	USER_AGENT = A[random.randrange(len(A))]
	headers = {"user-agent" : USER_AGENT}
	response = session.get(i, headers=headers)
	return response

def error_429_handle(session):
	time.sleep(120)
	session.cookies.clear()
	session.exit()
	session = HTMLSession()
	return session
	
def scrape_first_three_result(response, google_search_urls, i, index_num):	
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
		result_1_title = ''
	try:
		result_2_title = titles[1].text
	except:
		result_2_title = ''
	try:
		result_3_title = titles[2].text
	except:
		result_3_title = ''
	info = {
	'generated_urls':i,
	'result_1_url':result_1_url,
	'result_1_title':result_1_title,
	'result_2_url':result_2_url,
	'result_2_title':result_2_title,
	'result_3_url':result_3_url,
	'result_3_title':result_3_title
	}
	print(f"{index_num} ^ [{result_1_title}]")
	return info

def scrape_all_result(response, google_search_urls, i, index_num):
	print(f"url - {google_search_urls.index(i)}- {i}")
	urls = response.html.xpath('//div[@class="yuRUbf"]/a/@href')
	titles = response.html.xpath('//div[@class="yuRUbf"]/a/h3')
	try:
		result_1_url = urls[0]
	except:
		result_1_url = ''
	try:
		result_2_url = urls[1]
	except:
		result_2_url = ''
	try:
		result_3_url = urls[2]
	except:
		result_3_url = ''
	try:
		result_4_url = urls[3]
	except:
		result_4_url = ''
	try:
		result_5_url = urls[4]
	except:
		result_5_url = ''
	try:
		result_6_url = urls[5]
	except:
		result_6_url = ''
	try:
		result_7_url = urls[6]
	except:
		result_7_url = ''
	try:
		result_8_url = urls[7]
	except:
		result_8_url = ''
	try:
		result_9_url = urls[8]
	except:
		result_9_url = ''
	try:
		result_10_url = urls[9]
	except:
		result_10_url = ''
	try:
		result_1_title = titles[0].text
	except:
		result_1_title = ''
	try:
		result_2_title = titles[1].text
	except:
		result_2_title = ''
	try:
		result_3_title = titles[2].text
	except:
		result_3_title = ''
	try:
		result_4_title = titles[3].text
	except:
		result_4_title = ''
	try:
		result_5_title = titles[4].text
	except:
		result_5_title = ''
	try:
		result_6_title = titles[5].text
	except:
		result_6_title = ''
	try:
		result_7_title = titles[6].text
	except:
		result_7_title = ''
	try:
		result_8_title = titles[7].text
	except:
		result_8_title = ''
	try:
		result_9_title = titles[8].text
	except:
		result_9_title = ''
	try:
		result_10_title = titles[9].text
	except:
		result_10_title = ''
	info = {
	'google_search_url': i,
	'result_1_url': result_1_url,
	'result_2_url': result_2_url,
	'result_3_url': result_3_url,
	'result_1_title': result_1_title,
	'result_2_title': result_2_title,
	'result_3_title': result_3_title,
	'result_4_url': result_4_url,
	'result_5_url': result_5_url,
	'result_6_url': result_6_url,
	'result_7_url': result_7_url,
	'result_8_url': result_8_url,
	'result_9_url': result_9_url,
	'result_10_url': result_10_url,
	'result_4_title': result_4_title,
	'result_5_title': result_5_title,
	'result_6_title': result_6_title,
	'result_7_title': result_7_title,
	'result_8_title': result_8_title,
	'result_9_title': result_9_title,
	'result_10_title': result_10_title
	}
	print(f"{index_num} ^ [{result_1_title}]")
	return info

def sleep(sleep_time):
	time.sleep(sleep_time)

def write_csv(dict_array):
	fields = list(dict_array[0].keys())
	with open('GSEARCH_export.csv', 'w') as csvfile: 
		writer = csv.DictWriter(csvfile, fieldnames = fields)
		writer.writeheader()
		writer.writerows(dict_array)
