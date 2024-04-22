from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options

import pymongo 
from pymongo import MongoClient 
import sys

sys.stdout.reconfigure(encoding='utf-8')
search = input("Search Product :")
amazon_Data_collection=[]

options = Options()

unique_comments = set()
unique_data_collection = []
options.add_argument("--disable-notifications")
# options.add_argument('--headless')
driver = webdriver.Chrome(
    service=Service(executable_path=r"C:\Users\sagen\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"),
    options=options  # Fix the typo here
)

url="https://www.amazon.in/"
driver.get(url)





driver.implicitly_wait(30)
inputeTag = driver.find_element(By.NAME, 'field-keywords')  # Find the search box

inputeTag.send_keys(search + Keys.RETURN)

driver.implicitly_wait(10)
FirstProduct = driver.find_element(By.CLASS_NAME,'s-product-image-container')
FirstProduct.click()

time.sleep(15)

driver.switch_to.window(driver.window_handles[1]) 


time.sleep(25)
try:
    my_element = driver.find_element(By.XPATH,"//a[text()='See more reviews']")
    my_element.click()
except:
    print("next page not exite")
wait = WebDriverWait(driver,30)
for i in range(10):
    if len(unique_comments)>101:
        break
    comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"review-text")))
    ratings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'review-rating')))



    

    for rating,comment in zip(ratings,comments):
        try:
            amazon_Data_collection.append({"comments":comment.text,"rating":rating.get_attribute('textContent')})
        except Exception as e:
            print("An error occurred:", "")


    
    for item in amazon_Data_collection:
        comment = item.get('comments')
        if comment not in unique_comments:
            unique_data_collection.append(item)
            unique_comments.add(comment)
            # print("Find comments :"+ str(len(unique_comments)))

    
    try :
        n = driver.find_element(By.XPATH,"//a[text()='Next page']")
        n.click()
    except:
        print("next page not found ")
        break
    
    time.sleep(10)

time.sleep(10)



amazon_Data_collection = unique_data_collection
client =MongoClient('mongodb://localhost:27017')
db=client['Amazondatabase']
collection=db[search]


collection.insert_many(amazon_Data_collection)

client.close()
print("data insert succesfully")





time.sleep(120)
driver.close()