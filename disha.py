from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import Select
import ast
import json

base_url="https://www.pmgdisha.in/app/login"
driver=webdriver.Chrome(executable_path="C:/Users/Welcome/PycharmProjects/Webautomation/drivers/chromedriver.exe")
driver.maximize_window()
driver.get(base_url)
driver.find_element_by_id("inputEmail").send_keys("UTJH00025613650")
driver.find_element_by_id("lgpass1").send_keys("Pravesh@9793")

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Login']"))).click()
    sleep(5)
    base_url = "https://www.pmgdisha.in/app/trainingCenter/studentsummary"
    driver.get(base_url)
except:
    print("page is already loggen in.")
    driver.quit()
    exit()



select = Select(driver.find_element_by_id('pageSize'))
# select by value
select.select_by_value('50')
sleep(5)
html = driver.page_source
soup = BeautifulSoup(html)
table = soup.find('table', id='studentsummary')
df = pd.read_html(str(table))[0]

totolcurnum = driver.find_element_by_class_name('currPage')
totolpagenum = driver.find_element_by_class_name('totalPage')

print(totolcurnum.text)
print(totolpagenum.text)
df.to_excel("TEst.xls")

#json
studjson = driver.find_element_by_id('studentsJson').get_attribute("value")
print(studjson)
# data = studjson.strip('\"')
import json
data = json.loads(studjson)
cnt = 0
for element in data:
    for key, value in element.items():
        print("{}: {}".format(key, value))
    cnt = cnt +1
print(cnt)

train = pd.DataFrame.from_dict(data, orient='columns')
train.reset_index(level=0, inplace=True)
train.to_excel("Extract2.xls")

# getting password and username

driver.find_element_by_xpath("//*[@id='tbodyid']/tr[1]/td[6]/a[2]").click()
WebDriverWait(driver, 10).until(EC.alert_is_present())
driver.switch_to.alert.accept()
html = driver.execute_script("return document.documentElement.outerHTML")
#switch to modal

wait = WebDriverWait(driver, 15)
try:
    wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
except Exception as e:
    pass


# user_pwd = soup.find('div', class_ ="modal-content")
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='stdactivate']/div/div/div[3]/label[1]")))
    print("found " + element.text)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='stdactivate']/div/div/div[3]/label[2]")))
    print("found " + element.text)
finally:
    ele1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='stdactivate']/div/div/div[4]/button")))
    ele1.click()


# logout and close
# element = driver.find_element_by_tag_name("a")
# element.click()
# driver.quit()




