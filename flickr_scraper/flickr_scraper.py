import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# declares the starting url and a list that will be used by later operations.

url = 'https://www.flickr.com'

url_list = []

# asks the user for what they would like to search for and how many images they would like to download.

search_request = input("What would you like to search for on Flickr?: ")

while True:
    try:
        how_many = int(input('How many images would you like to download?: '))
            
    except:
        print("Please enter an integer.")

    else:
        break

# declares the load strategy for the webdriver.

chrome_path = "C:\\Users\\Sephi\\Anaconda3\\chromedriver.exe"

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
  
driver = webdriver.Chrome(desired_capabilities=caps, executable_path=chrome_path)

# opens a chrome window, enters the search request in the search field and clicks on the search icon.

driver.get(url)

search_field = driver.find_element_by_id('search-field')
search_button = driver.find_element_by_class_name('search-icon-button')

search_field.send_keys(search_request)
search_button.click()

# holds the webdriver back as it tends to fail if the page does not load fast enough.

time.sleep(3)

# parses the page, grabbing partial urls for all images on the page and then completes them with the starting url variable.  Then creates a list for them.

page = driver.page_source

soup = BeautifulSoup(page, "html.parser")

url_part_two = soup.findAll("a", class_="overlay")

images = [url + i['href'] for i in url_part_two[0:how_many]]

# opens each compleated url and grabbs the source url for each image, completing with https://.

print('\n')

for i in images:

    list_length = str(len(images))

    index = str(images.index(i)+1)

    print(f'Gathering file {index} of {list_length}...')

    driver.get(i)

    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    true_link = soup.select('img', class_='main-photo')[2]['src'][2:]

    url_list.append('https://' + true_link)

driver.close()

print('\nDone.\n')

# writes each file to the specified folder preserving the file type and giving a semi-random name.

for i in url_list:

    list_length = str(len(url_list))

    index = str(url_list.index(i)+1)

    print(f"Writing file {index} of {list_length}...")

    file = str(i)
    data = requests.get(i).content

    with open('C:\\Users\\Sephi\\Desktop\\Python\\Web Scraing\\flickr_scraper\\downloaded_files\\' + file[40:], 'wb') as f:
        f.write(data)

print('\nDone.\n')
print('Process Complete!\n')