#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 21:02:29 2019

@author: kenkuo
"""

#from bs4 import BeautifulSoup
#import requests
#import re
#
#base_url = "http://www.hung-ya.com/cgi-bin/bbs/"
#url = "http://www.hung-ya.com/cgi-bin/bbs/postlist.pl?board=4_people"
#
#html = requests.get(url).text
#soup = BeautifulSoup(html, 'lxml')
#img_href = soup.find_all('td', {"align":"left","class": "B2"})
#
#import os
#
#os.makedirs('./img/', exist_ok=True)
#
#for href in img_href:
##    print(href.a['href'])
#    r=requests.get(base_url+str(href.a['href']))
##    print(r.text)
#    img_soup = BeautifulSoup(r.text, 'html.parser')
#    imgs =img_soup.find_all('img')
#    for img in imgs:
#        url = img['src']
##        print(url)
#        if re.match('.+jpg$',img['src'])!=None:
#            rr = requests.get(url, stream=True)
#            image_name = url.split('/')[-1]
#            with open('./img/%s' % image_name, 'wb') as f:
#                for chunk in rr.iter_content(chunk_size=128):
#                    f.write(chunk)
#            print('Saved %s' % image_name)

from selenium import webdriver
import time
#This is a test~~
#This is a test2~~
driver = webdriver.Chrome()
driver.get("https://www.google.com")
#driver.find_element_by_name('q').send_keys('inty youtube')
#driver.find_element_by_link_text('Gmail').click()
#elements=driver.find_elements_by_tag_name('a')
#for element in elements:
#    print(element.text)

driver.find_element_by_css_selector('')
#time.sleep(2)
driver.quit()

#driver.find_element_by_id("email").send_keys('')
#driver.find_element_by_id("pass").send_keys('')
#driver.find_element_by_id("loginbutton").click()