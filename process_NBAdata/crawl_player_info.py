import requests as req
#from bs4 import BeautifulSoup as bs
from selenium import webdriver
import os
from time import sleep
from contextlib import closing
import sys

def read_names():
	names = [];
	with open("players_name.txt", "r") as f:
		for line in f.readlines():
			line = line[:-1]
			names.append(line)

	return names

# def write_urls(urls):
# 	with open("player_pic_urls.txt", "w") as f:
# 		for each_url in urls:
# 			f.writelines(each_url)

def get_pic_url(browser, player_name):
	
	e_search = browser.find_element_by_name("q")
	e_search.send_keys(player_name)

	e_button_search = browser.find_element_by_name("btnG")
	e_button_search.click()
	sleep(2)

	e_pics = browser.find_elements_by_css_selector("img.rg_ic.rg_i")
	e_pics[0].click()

	sleep(2)

	e_view_button = browser.find_element_by_link_text("View image")
	e_view_button.click()

	sleep(10)
	
	browser.switch_to_window(browser.window_handles[1])
	pic_url = browser.current_url

	browser.close()
	browser.switch_to_window(browser.window_handles[0])
	browser.back()
	sleep(60)

	return pic_url

# def urls_for_all_players():
# 	chrome_driver = "/usr/bin/chromedriver"
# 	os.environ["webdriver.chrome.driver"]  = chrome_driver
# 	browser = webdriver.Chrome(chrome_driver)
# 	browser.get("http://image.google.com")
# 	sleep(1)

# 	player_list = read_names()

# 	urls = []
# 	# names = ["kobe bryant", "Yao Ming", "steve nash", "anthony davis"]
# 	# for name in names:
# 	# 	urls.append(get_pic_url(browser, name))
# 	# print(urls)
# 	for each in player_list:
# 		search_name = each + " NBA"
# 		urls.append(get_pic_url(browser, search_name) + "@" + each)

# 	return urls

# def get_image(urls):
# 	userAgent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# 	for each in urls:
# 		rec = each.spilt("@")
# 		url = rec[0]
# 		name = rec[1]
# 		with closing(req.get(url, headers=userAgent, stream=True)) as rep:
# 			fn = name + ".jpg"
# 			with open("".join(["player_pics/",fn]), "wb") as f:
# 				for chunk in rep.iter_content(1024):
# 					f.write(chunk) 

# def main():
# 	urls = urls_for_all_players()
# 	write_urls(urls)
# 	get_image(urls)
# 	print("done")

#this code is more efficient than main()
def main1():
	#searchbase = " :espn"
	searchbase = " :espn 350 × 254 nba"
	#searchbase = " nba"
	#searchbase = " :nba.com"

	player_list = read_names()
	download_pic(player_list, 0, searchbase)



def download_pic(namelist, start, url_suffix):
	userAgent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	chrome_driver = "/usr/bin/chromedriver"
	os.environ["webdriver.chrome.driver"]  = chrome_driver
	browser = webdriver.Chrome(chrome_driver)
	browser.get("http://image.google.com")
	sleep(1)

	s = start
	e = 25

	player_list = namelist[start : start + e]
	if(player_list == []):
		sys.exit(0)

	print(player_list)
	
	try:
		i = 0
		while(s < start + e):
			player_name = player_list[i]
			s += 1
			i += 1
			search_name = player_name + url_suffix
			print(search_name)
			fn = player_name + ".png"
			fnn = "".join(["player_pics/",fn])
			
			url = get_pic_url(browser, search_name)
			
			with closing(req.get(url, headers=userAgent, stream=True)) as rep:
				with open(fnn, "wb") as f:
					for chunk in rep.iter_content(512):
						f.write(chunk)

		browser.quit()
		print(s)
		sleep(60)
		download_pic(namelist, s, url_suffix)
	except:
		browser.quit()
		download_pic(namelist, s, url_suffix)
	

if __name__ == "__main__":
	main1()
	#download_pic()
	#read_names()
	
