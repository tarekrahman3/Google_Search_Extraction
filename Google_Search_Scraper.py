import undetected_chromedriver.v2 as uc
import time
#import simpleaudio
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import urllib.parse

def notify():
	#wave_obj = simpleaudio.WaveObject.from_wave_file("bell.wav")
	#play_obj = wave_obj.play()
	#play_obj.wait_done()
	print('stuck')

driver = uc.Chrome()

def dict_csv_read():
	return pd.read_csv('imports.csv').links.tolist()

def complimentary_result(driver):
	try:
		permanently_closed = driver.find_element_by_xpath('//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//span[text()="Permanently closed"]').text
	except:
		permanently_closed = None
	try:
		name = driver.find_element_by_xpath('//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//h2/span').text
	except:
		name = None
	try:
		realorgtype  = driver.find_element(By.XPATH,'//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//*[@data-attrid="subtitle"]/span').text
	except:
		realorgtype  =  None
	try:
		assumedorgtype=  driver.find_element(By.XPATH,'//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//*[@data-attrid="kc:/local:one line summary"]//span[contains(text(),"organization")]').text
	except:
		assumedorgtype =  None
	try:
		address = driver.find_element_by_xpath('//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//a[text()="Address"]/../following-sibling::span').text
	except:
		address = None
	try:
		website = driver.find_element_by_xpath('//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//a/div[text()="Website"]/..').get_attribute('href')
	except:
		website = None
	try:
		phone =  driver.find_element_by_xpath('//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//span[contains(@aria-label,"Call")]').text
	except:
		phone =  None
	return permanently_closed, name,realorgtype,assumedorgtype, address, phone, website

def social_accounts(driver):
	try:
		social_profiles =  driver.find_element_by_xpath('//h2[text()="Complementary results" or text()="Complementary Results"]/following-sibling::div//*[text()="Profiles"]/following::div[1]')
		try:
			facebook = social_profiles.find_element_by_xpath('.//a[contains(@href,"facebook.com/")]').get_attribute('href')
		except:
			facebook = None
		try:
			instagram = social_profiles.find_element_by_xpath('.//a[contains(@href,"instagram.com/")]').get_attribute('href')
		except:
			instagram = None
		try:
			twitter = social_profiles.find_element_by_xpath('.//a[contains(@href,"twitter.com/")]').get_attribute('href')
		except:
			twitter = None
		try:
			linkedin = social_profiles.find_element_by_xpath('.//a[contains(@href,"linkedin.com/")]').get_attribute('href')
		except:
			linkedin = None
		socials = f"""facebook: {facebook}\ninstagram: {instagram}\ntwitter: {twitter}\nlinkedin: {linkedin}"""
		return socials
	except:
		return None


def search_result(driver,index):
	results = driver.find_elements(By.XPATH, '//div[@class]/div[@class="g"]')
	try:
		result_title = results[index].find_element_by_xpath('.//h3').text
	except:
		result_title = None
	try:
		result_description = results[index].find_element_by_xpath('.//*[@style="-webkit-line-clamp:2"]').text
	except:
		result_description = None
	try:
		result_url = results[index].find_element_by_xpath('.//a[@href and @data-ved]').get_attribute('href')
	except:
		result_url = None
	return result_title, result_description, result_url

def scrape(url, index, dict_array):
	if index%50==0:
		pd.DataFrame(dict_array).to_csv('backup_au_school.csv', index = False)
	driver.get(url+'&hl=en')
	time.sleep(2)
	if "captcha" in (driver.page_source):
		notify()
		epoch = time.perf_counter()
		while True:
			if not "captcha" in (driver.page_source):
				break
			if int(epoch)>30 and (int(time.perf_counter()) - int(epoch))%30==0:
				notify()
	
	permanently_closed, name, realorgtype, assumedorgtype,address, phone, website = complimentary_result(driver)
	first_result_title, first_result_description, first_result_url = search_result(driver,0)
	second_result_title, second_result_description, second_result_url = search_result(driver,1)
	third_result_title, third_result_description, third_result_url = search_result(driver,2)
	fourth_result_title, fourth_result_description, fourth_result_url = search_result(driver,3)
	fifth_result_title, fifth_result_description, fifth_result_url = search_result(driver,4)
	sixth_result_title, sixth_result_description, sixth_result_url = search_result(driver,5)
	seventh_result_title, seventh_result_description, seventh_result_url = search_result(driver,6)
	eighth_result_title, eighth_result_description, eighth_result_url = search_result(driver,7)
	ningth_result_title, ningth_result_description, ningth_result_url = search_result(driver,8)
	tenth_result_title, tenth_result_description, tenth_result_url = search_result(driver,9)
	socials = social_accounts(driver)
	data = {
		'source':url,
		'complimentary_result_name':name,
		'complimentary_result_realorgType':realorgtype,
		'complimentary_result_assumedorgtype':assumedorgtype,
		'complimentary_result_address':address,
		'complimentary_result_website':website,
		'complimentary_result_phone':phone,
		'permanently_closed':permanently_closed,
		'socials':socials,
		'first_result_title': first_result_title,
		'first_result_description': first_result_description,
		'first_result_url': first_result_url,
		'second_result_title': second_result_title,
		'second_result_description': second_result_description,
		'second_result_url': second_result_url,
		'third_result_title': third_result_title,
		'third_result_description': third_result_description,
		'third_result_url': third_result_url,
		'fourth_result_title': fourth_result_title,
		'fourth_result_description': fourth_result_description,
		'fourth_result_url': fourth_result_url,
		'fifth_result_title': fifth_result_title,
		'fifth_result_description': fifth_result_description,
		'fifth_result_url': fifth_result_url,
		'sixth_result_title': sixth_result_title,
		'sixth_result_description': sixth_result_description,
		'sixth_result_url': sixth_result_url,
		'seventh_result_title': seventh_result_title,
		'seventh_result_description': seventh_result_description,
		'seventh_result_url': seventh_result_url,
		'eighth_result_title': eighth_result_title,
		'eighth_result_description': eighth_result_description,
		'eighth_result_url': eighth_result_url,
		'ningth_result_title': ningth_result_title,
		'ningth_result_description': ningth_result_description,
		'ningth_result_url': ningth_result_url,
		'tenth_result_title': tenth_result_title,
		'tenth_result_description': tenth_result_description,
		'tenth_result_url': tenth_result_url
		}
	print(f"{index} | {data['complimentary_result_name']} | {data['complimentary_result_website']} | {data['complimentary_result_assumedorgtype']} | {data['complimentary_result_realorgType']}")
	dict_array.append(data)

google_search_urls = dict_csv_read()
dict_array = []
try:
	for index, search_string in enumerate(google_search_urls):
			time.sleep(1)
			url = 'https://www.google.com/search?q='+urllib.parse.quote(search_string)
			scrape(url, index, dict_array)
except Exception as e:
	print(e)
finally:
	pd.DataFrame(dict_array).to_csv('export.csv', index = False)
driver.quit()
