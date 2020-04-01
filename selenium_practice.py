#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:17:12 2020

@author: kenkuo
"""


from selenium import webdriver
import time
driver=webdriver.Chrome('/Users/kenkuo/Downloads/chromedriver')
driver.fullscreen_window()
driver.get('https://www.google.com')
driver.find_element_by_name('q').send_keys('html selenium')
time.sleep(3)

driver.quit()