import GSEARCH

google_search_urls = GSEARCH.load_import_csv()
session = GSEARCH.start_request_session()

for each_link in range(3, 22):
	index_num = google_search_urls.index(google_search_urls[each_link])
	link = google_search_urls[each_link]
	response = GSEARCH.set_UA_headers_and_send_request(link, session)
	if response.status_code == 429:
		response = GSEARCH.error_429_handle()
	else:
		pass
	GSEARCH.scrape(response, google_search_urls, each_link, index_num)
	GSEARCH.sleep()
GSEARCH.create_dataframe()
GSEARCH.export_to_csv(df)

