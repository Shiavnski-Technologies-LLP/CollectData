from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo 
from pymongo import MongoClient 
import random
import time
import pymongo
import sys
from selenium.common.exceptions import StaleElementReferenceException


sys.stdout.reconfigure(encoding='utf-8')


username=input("username  : ")
password=input("password : ")
search=input("Search : ")
no_of_comments=int(input("How many comments you wants : "))

driver= webdriver.Chrome()


             
twitter_Data=[]

unique_comments = set()
url="https://twitter.com/home"
driver.get(url)
time.sleep(random.uniform(2,5))

driver.implicitly_wait(20)
InputUsername = driver.find_element(By.NAME, 'text')  # Find the username
InputUsername.send_keys(username + Keys.RETURN)
time.sleep(random.uniform(2,5))

InputPassword= driver.find_element(By.NAME, 'password')  # Find the password box
InputPassword.send_keys(password + Keys.RETURN)
time.sleep(random.uniform(5,8))
time.sleep(10)
SearchElement= driver.find_element(By.CLASS_NAME, 'r-30o5oe')  # Find the search box
SearchElement.send_keys(search + Keys.RETURN)


time.sleep(random.uniform(5,8))
people=driver.find_element(By.LINK_TEXT,"People")
people.click()
time.sleep(random.uniform(3,7))
f=driver.find_element(By.CLASS_NAME,'r-18kxxzh')
f.click()
time.sleep(random.randint(5, 10))

# driver.fullscreen_window()


firstpost=driver.find_element(By.CSS_SELECTOR,".css-1rynq56.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim")

#firstpost=driver.find_element(By.XPATH,"//div[@data-testid='tweetText']/span")

firstpost.click()
wait = WebDriverWait(driver,120)

while True:
    try:
        if len(unique_comments)>=no_of_comments:
            break
        time.sleep(random.randint(15, 25))
        comments=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".css-1rynq56.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim")))
        
        time.sleep(2)
        for comment in comments:
            try:
                twitter_Data.append({"comments":comment.text})
                
                
            except StaleElementReferenceException:
                # print("Stale element encountered. Trying again...")
                continue
            except Exception as e:
                print("An error occurred:", e)
        for comment_dict in twitter_Data:
            comment_text = comment_dict.get("comments")
            if comment_text:
                unique_comments.add(comment_text)
                # print("Find comment " + str(len(unique_comments)))
        try :
            show_more=driver.find_element(By.XPATH, "Show more replies")
          
        except:
            prev_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(15, 25))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break

        
    except Exception as e:
                print("An error occurred:", e)







unique_comments_list = list(unique_comments)

client =MongoClient('mongodb://localhost:27017')
db=client['Twitterdatabase']
collection=db[search]


for i, comment in enumerate(unique_comments_list):
    try:
        collection.insert_one({"comments": comment})
        
  
    except Exception as e:
        print(f"An error occurred while inserting comment {i + 1} into the database:", e)

client.close()
# print(unique_comments_list)



time.sleep(random.uniform(3,7))

account=driver.find_element(By.XPATH,"//div[@aria-label='Account menu']")
account.click()
time.sleep(4)

alog_out=driver.find_element(By.XPATH, "//a[@href='/logout']")
alog_out.click()
time.sleep(random.uniform(3,7))
log_out = driver.find_element(By.XPATH, "//*[@role='button']")


log_out.click()
time.sleep(random.uniform(3,7))

print(str(len(unique_comments))+"comments  insert succesfully")

time.sleep(10000)

driver.quit()