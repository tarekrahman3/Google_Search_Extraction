import GSEARCH
google_search_urls = GSEARCH.dict_csv_read()
session = GSEARCH.start_request_session()
dict_array = []
sleep_time = int(input('interval period (in second): '))
try:
	for i in google_search_urls:
		index_num = google_search_urls.index(i)
		link = i
		response = GSEARCH.set_UA_headers_and_send_request(i, session)
		if response.status_code == 429:
			response = GSEARCH.error_429_handle(session)
		else:
			pass
		info = GSEARCH.scrape_all_result(response, google_search_urls, i, index_num)
		#info = GSEARCH.scrape_first_three_result(response, google_search_urls, each_link, index_num)
		dict_array.append(info)
		GSEARCH.sleep(sleep_time)
finally:
	GSEARCH.write_csv(dict_array)
