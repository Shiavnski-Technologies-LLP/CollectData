from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo 
from pymongo import MongoClient 
import random
import time
import sys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')
search = input("search :  ")
options = Options()
options.add_argument("--disable-notifications")
# options.add_argument('--headless')
driver = webdriver.Chrome(
    service=Service(executable_path=r"C:\Users\sagen\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"),
    options=options  # Fix the typo here
)

fb_Data = []
name = "osamboyz9685721212@gmail.com"
password = "Shivam@1212"

unique_comments = set()
url = "https://www.facebook.com/"
driver.get(url)
time.sleep(random.randint(5, 10))

wait = WebDriverWait(driver, 60)


n = wait.until(EC.presence_of_element_located((By.NAME, "email")))
n.send_keys(name)

# Find the password input   
p = wait.until(EC.presence_of_element_located((By.NAME, "pass")))
p.send_keys(password + Keys.RETURN)
time.sleep(2)


s = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
s.send_keys(search + Keys.RETURN)
page=wait.until(EC.presence_of_element_located((By.LINK_TEXT,"Pages")))
page.click()
time.sleep(random.randint(5, 10))
first_post = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[role='presentation']")))
first_post.click()
time.sleep(random.randint(5, 10))
driver.execute_script("window.scrollBy(0, 400);")
time.sleep(random.randint(5, 10))
#c_comment = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Leave a comment']")))

c_comment = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Leave a comment']")))
c_comment.click()
time.sleep(random.randint(5, 10))
try:
    mostrelevent = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Most relevant']")))
    mostrelevent.click()
except:
    print("Not able to click most Relevent")
time.sleep(random.randint(5, 10))
try:
    allcomments = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Show all comments, including potential spam. The most relevant comments will appear first.']")))
    allcomments.click()
except:
    print("Not able to click all comments ")

time.sleep(random.randint(5, 10))

driver.execute_script("window.scrollBy(0, 100);")
i=0
while True:
    i=i+1
    if len(unique_comments) >= 100 or i>11:
            break

    

    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(random.randint(15, 20))
    comments = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x1lliihq.xjkvuk6.x1iorvi4")))
    for comment in comments:
            try:
                fb_Data.append({"comments":comment.text})
                print("comments " + str(len(fb_Data)))
            except Exception as e:
                print("An error occurred:", "")
   
    for comment_dict in fb_Data:
        comment_text = comment_dict.get("comments")
        if comment_text:
            unique_comments.add(comment_text)

    try:
        more = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='View more comments']")))
        more.click()
        time.sleep(random.randint(15, 20))
    except:
        print("View more comments button not found.")

    

unique_comments_list = list(unique_comments)
client = MongoClient('mongodb://localhost:27017')
db=client['FaceBookdatabase']
collection = db[search]


for i, comment in enumerate(unique_comments_list):
    try:
        collection.insert_one({"comments": comment})
        print(f"Inserted comment {i + 1} into the database")
    except pymongo.errors.DuplicateKeyError:
        print(f"Comment {i + 1} is already in the database")
    except Exception as e:
        print(f"An error occurred while inserting comment {i + 1} into the database:", e)

print("data insert succesfully")
client.close()
cancle = driver.find_element(By.XPATH, "//div[@aria-label='Close']")
cancle.click()
time.sleep(random.randint(5, 10))
profile = driver.find_element(By.CSS_SELECTOR, ".x1rg5ohu.x1n2onr6.x3ajldb.x1ja2u2z")
profile.click()
time.sleep(random.randint(7, 13))
log = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Log out']")))
log.click()
time.sleep(random.randint(7, 13))
print("Log out succesfull")
time.sleep(100000)
driver.quit()
