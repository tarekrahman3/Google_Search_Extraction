csv_import_file = input(':')
csv_import_file = 'import1.csv'
	
from requests_html import HTMLSession
from lxml import html
import random
import time
import csv
import os

def dict_csv_read(csv_import_file):
	try:
		os.system('mkdir "Response Archive"')
	except:
		pass
	rows_dict = []
	with open(csv_import_file) as csv_file:
		reader = csv.DictReader(csv_file)
		for row in reader:
			rows_dict.append(row)
	return rows_dict

def send_get_request(each_keyword_link, Index_No):
	A = (
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
	)
	session = HTMLSession()
	session.cookies.clear()
	USER_AGENT = A[random.randrange(len(A))]
	headers = {"user-agent" : USER_AGENT}
	response = session.get(each_keyword_link, headers=headers)
	with open(f"./Response Archive/{Index_No} - {str(index+1)} - response.txt", "w") as f:
			f.write(response.text)
	session.close()
	return response

def error_429_handle():
	session.close()
	time.sleep(40)
	start_request_session()
	
def recommended_result_parse(response):
	name = response.html.xpath('//h3[1]/text()')[0]
	address = response.html.xpath('//span[@class="BNeawe tAd8D AP7Wnd"]/text()')
	website = response.html.xpath('//a[contains(@href,"geocode=")]//following-sibling::a/@href')
	check_operating_status = response.html.xpath('//*[contains(text(), "Permanently closed")]/text()')
	map_source = response.html.xpath('//a[contains(@href,"&geocode=")]/@href')
	info_dict = {'name':name, 'address':address, 'website':website, 'map_source': map_source, 'operatng staus':check_operating_status}
	return info_dict
	
def parse_list_result(response):
	l={}
	try:
		header = response.html.xpath('//div[@class="yuRUbf"]/a/h3/text()')
		href = response.html.xpath('//div[@class="yuRUbf"]/a/@href')
		header_index = 1
		
		for header_index in range(len(header)):
			header_column_name = f"Search Result {header_index} Header" 
			header_column_content = header[header_index-1]
			url_column_name = f"Search Result {header_index} URL"
			url_column_content = href[header_index-1]
			a = {header_column_name:header_column_content,
			url_column_name:url_column_content}
			l.update(a)
	except:
		header_column_name = f"Search Result 0 Header" 
		url_column_name = f"Search Result 0 URL"
		a = {header_column_name:'',
			url_column_name:''}
		l.update(a)
	return l
def write_csv(dict_array):
	fields = list(dict_array[0].keys())
	with open(f"Cloud G export at {time.ctime()}.csv", 'w') as csvfile: 
		writer = csv.DictWriter(csvfile, fieldnames = fields)
		writer.writeheader()
		writer.writerows(dict_array)

if __name__ == "__main__":
	dict_array = []
	csv_rows = dict_csv_read(csv_import_file) 
	index = 0
	for index in range(len(csv_rows)):
		info_dict = {
		'Index No.': csv_rows[index]['Index No.'],
		'generated link': csv_rows[index]['generated_keyword_urls']}
		time.sleep(random.randint(3, 6))
		response = send_get_request(csv_rows[index]['generated_keyword_urls'], csv_rows[index]['Index No.'])
		#response.html.render()
		# Parse the featured result if available
		try:
			recommended_result = recommended_result_parse(response)
			list_result = parse_list_result(response)
		finally:
			info_dict.update(recommended_result)
			info_dict.update(list_result)
		print(info_dict)
		dict_array.append(info_dict)
	write_csv(dict_array)










			
