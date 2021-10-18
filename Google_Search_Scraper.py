import undetected_chromedriver.v2 as uc
import time
import simpleaudio
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

wave_obj = simpleaudio.WaveObject.from_wave_file("bell.wav")
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
	return permanently_closed, name, address, phone, website

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


def first_search_result(driver):
	results = driver.find_elements(By.XPATH, '//div[@class]/div[@class="g"]')
	try:
		first_result_title = results[0].find_element_by_xpath('.//h3').text
	except:
		first_result_title = None
	try:
		first_result_description = results[0].find_element_by_xpath('.//*[@style="-webkit-line-clamp:2"]').text
	except:
		first_result_description = None
	try:
		first_result_url = results[0].find_element_by_xpath('.//a[@href and @data-ved]').get_attribute('href')
	except:
		first_result_url = None
	return first_result_title, first_result_description, first_result_url

def scrape(url, index, dict_array):
	driver.get(url+'&hl=en')
	time.sleep(2)
	if "captcha" in (driver.page_source):
		play_obj = wave_obj.play()
		play_obj.wait_done()
		input("Press any key to continue")
	permanently_closed, name, address, phone, website = complimentary_result(driver)
	first_result_title, first_result_description, first_result_url = first_search_result(driver)
	socials = social_accounts(driver)
	data = {
		'source':url,
		'complimentary_result_name':name,
		'complimentary_result_address':address,
		'complimentary_result_website':website,
		'complimentary_result_phone':phone,
		'permanently_closed':permanently_closed,
		'socials':socials,
		'1st_result_title': first_result_title,
		'1st_result_description': first_result_description,
		'1st_result_url': first_result_url
		}
	print(f"{index} | {data['complimentary_result_name']} | {data['complimentary_result_website']} | {data['complimentary_result_phone']} | {data['socials']}")
	dict_array.append(data)

google_search_urls = dict_csv_read()
dict_array = []
try:
	for index, url in enumerate(google_search_urls):
			time.sleep(1)
			scrape(url, index, dict_array)
except Exception as e:
	print(e)
finally:
	pd.DataFrame(dict_array).to_csv('export.csv', index = False)
driver.quit()
