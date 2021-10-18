import undetected_chromedriver.v2 as uc
import time
import simpleaudio
from selenium.webdriver.common.keys import Keys
import pandas as pd

wave_obj = simpleaudio.WaveObject.from_wave_file("bell.wav")


driver = uc.Chrome()

def dict_csv_read():
	return pd.read_csv('imports.csv').links.tolist()

def scrape(url, index, dict_array):
	driver.get(url+'&hl=en')
	time.sleep(2)
	if "captcha" in (driver.page_source):
		play_obj = wave_obj.play()
		play_obj.wait_done()
		input("Press any key to continue")
	try:
		permanently_closed = driver.find_element_by_xpath('//h2[text()="Complementary results"]/following-sibling::div//span[text()="Permanently closed"]').text
	except:
		permanently_closed = None
	try:
		name = driver.find_element_by_xpath('//h2[text()="Complementary results"]/following-sibling::div//h2/span').text
	except:
		name = None
	try:
		address = driver.find_element_by_xpath('//h2[text()="Complementary results"]/following-sibling::div//a[text()="Address"]/../following-sibling::span').text
	except:
		address = None
	try:
		website = driver.find_element_by_xpath('//h2[text()="Complementary results"]/following-sibling::div//a/div[text()="Website"]/..').get_attribute('href')
	except:
		website = None
	try:
		phone =  driver.find_element_by_xpath('//h2[text()="Complementary results"]/following-sibling::div//span[contains(@aria-label,"Call")]').text
	except:
		phone =  None
	try:
		title = driver.find_element_by_xpath('//h3').text
	except:
		title = None
	try:
		description = driver.find_element_by_xpath('//h3/ancestor::div/following-sibling::div[2]').text
	except:
		description = None
	try:
		first_result_url = driver.find_element_by_xpath('//h3/ancestor::a').get_attribute('href')
	except:
		first_result_url = None
	data = {'source':url,
	'name':name,
	'address':address,
	'website':website,
	'phone':phone,
	'permanently_closed':permanently_closed,
	'1st_result_title': title,
	'1st_result_description': description,
	'1st_result_url': first_result_url
	}
	print(f"{index} | {data['name']} | {data['website']} | {data['phone']}")
	dict_array.append(data)

google_search_urls = dict_csv_read()
dict_array = []
try:
	for index, url in enumerate(google_search_urls):
			time.sleep(5)
			scrape(url, index, dict_array)#scrape_1st_result()
finally:
	pd.DataFrame(dict_array).to_csv('export.csv', index = False)
driver.quit()
