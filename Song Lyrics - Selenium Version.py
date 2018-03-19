#! python3
# Selenium Song Lyric Web Script.py - Grabs queried song lyrics from https://www.azlyrics.com/ using selenium
# and prints it out and puts it into a text file.

# Note: This script performs similar to Google's "I'm feeling lucky" button. It only returns the top search result.


import os, sys, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# #Creates file to store lyrics in if it does not already exist
os.makedirs('Lyrics', exist_ok = True)

print("Enter the song name you would like to find lyrics for.")
query = input()

#Load webdriver and go to site
driver = webdriver.Firefox()
driver.get('https://azlyrics.com/')


#Input search query into site
search_bar = driver.find_element_by_xpath("//input[@id = 'q']")
search_bar.send_keys(query)
search_bar.send_keys(Keys.RETURN)


#Create function to check if xpath exists
def check_element_exist(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#Create variables for page elements
with_album_artist = "//div[@class = 'panel'][3]//td/a"
with_albums = "//div[@class = 'panel'][2]//td/a"
without_albums = "//tr[2]//td//a"

#Depending on the page layout, click a certain link
wait = WebDriverWait(driver, 8)
try:
    wait.until(EC.presence_of_element_located((By.XPATH, with_album_artist)))
    driver.find_element_by_xpath(with_album_artist).click()
except:
    if check_element_exist(with_albums) == True:
        driver.find_element_by_xpath(with_albums).click()
    elif check_element_exist(without_albums) == True:
        driver.find_element_by_xpath(without_albums).click()
    else:
        print("Sorry, we could not find any results for that search. Please modify your search terms.")
        driver.quit()
        sys.exit()

#Find lyrics on the page and print the result
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
wait.until(EC.presence_of_element_located((By.XPATH, '//div[2]/div[5]')))
lyrics = driver.find_element_by_xpath("//div[2]/div[5]").text
title = driver.title
print(lyrics)
print("\n Returned lyrics for " + title)

#Creates file to write to which is located in lyrics folder
file = open('Lyrics/' + title + '.txt', 'w', encoding = 'utf-8')
file.write(str(lyrics))
file.close()
