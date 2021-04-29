from selenium import webdriver
# pip3 install selenium
import time
import simpleaudio
wave_obj = simpleaudio.WaveObject.from_wave_file("bell.wav")
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
from selenium_stealth import stealth
# pip3 install selenium-stealth
options = Options()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument("user-agent=DN")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('user-data-dir="/home/tarek/Selenium_Projects/Project_LinkedIn/user_dir"')
driver = webdriver.Chrome(options=options, executable_path='/home/tarek/MY_PROJECTS/Selenium_Projects/webdrivers/chromedriver')
stealth(driver,
languages=["en-US", "en"],
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Google SwiftShader",# Intel Iris OpenGL Engine
fix_hairline=True,
)

def dict_csv_read():
	google_search_urls = []
	with open('imports.csv') as csv_file:
		reader = csv.DictReader(csv_file, delimiter=",")
		for row in reader:
			google_search_urls.append(row['links'])
	return google_search_urls

def scrape():
	driver.get(i)
	try:
		name = driver.find_element_by_xpath('//h3[1]').text
	except:
		name = ''
	try:
		address = driver.find_element_by_xpath("//span[contains(text(),'Address')]/ancestor::span/following-sibling::span/span").text
	except:
		address = ''
	try:
		website = driver.find_element_by_xpath("//div[@id='main']/div[3]//a[contains(@href,'https://maps.google.com/maps?')]//following-sibling::a").get_attribute('href')
	except:
		website = ''
	try:
		phone =  driver.find_element_by_xpath("//span[contains(text(),'Phone')]/ancestor::span/following-sibling::span/span").text
	except:
		phone =  ''
	data = {'source':i,
	'name':name,
	'address':address,
	'website':website,
	'phone':phone}
	print(data)
	dict_array.append(data)
	return dict_array

def scrape_1st_result():
	indx = (google_search_urls.index(i))+1
	'''if indx%15==0:
		driver.delete_all_cookies()
		print("\n\n****COOKIES CLEARED******\n\n")
	else:
		pass'''
	driver.get(i)
	if "robot" in (driver.page_source):
		play_obj = wave_obj.play()
		play_obj.wait_done()
		input("Press any key to continue")
	else:
		pass
	try:
		title = driver.find_element_by_xpath('//h3').text
	except:
		title = ''
	try:
		description= driver.find_element_by_xpath('//h3/ancestor::div/following-sibling::div[2]').text
	except:
		description=''
	try:
		url = driver.find_element_by_xpath('//h3/ancestor::a').get_attribute('href')
	except:
		url = ''
	data = {'source':i,
	'title':title,
	'description':description,
	'url':url}
	print(f"{indx} - {data}")
	dict_array.append(data)
	return dict_array
google_search_urls = dict_csv_read()
dict_array=[]
try:
	for i in google_search_urls:
			time.sleep(5)
			scrape_1st_result()
finally:
	fields = ['source', 'title', 'description', 'url']
	with open('Selenium_GSEARCH_export.csv', 'w') as csvfile: 
		writer = csv.DictWriter(csvfile, fieldnames = fields)
		writer.writeheader()
		writer.writerows(dict_array)
driver.quit()
