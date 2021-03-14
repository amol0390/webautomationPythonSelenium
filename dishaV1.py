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
from selenium.webdriver.common.action_chains import ActionChains

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
page=1
max_page=1
SN=[]
NAME=[]
RDATE=[]
STATUS=[]
EmailVerified=[]
Train10days = []
StudentoutcomeForm = []
TestCompleted = []

while page<=max_page:

 rows= WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='tbodyid']/tr")))
 for row in rows:
    SN.append(row.find_element_by_xpath('./td[1]').text)
    NAME.append(row.find_element_by_xpath('./td[2]').text)
    RDATE.append(row.find_element_by_xpath('./td[3]').text)
    STATUS.append(row.find_element_by_xpath('./td[4]/i').get_attribute('aria-hidden'))
    EmailVerified.append(row.find_element_by_xpath('./td[5]/span[1]/i').get_attribute('aria-hidden'))
    Train10days.append(row.find_element_by_xpath('./td[5]/span[2]/i').get_attribute('aria-hidden'))
    StudentoutcomeForm.append(row.find_element_by_xpath('./td[5]/span[3]/i').get_attribute('aria-hidden'))
    TestCompleted.append(row.find_element_by_xpath('./td[5]/span[4]/i').get_attribute('aria-hidden'))

 # #move on next page
 element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div/div[3]/div[1]/div[3]/div/div[2]/ul/li[5]/a")))
 driver.execute_script("arguments[0].click();", element)
 page=page+1
 # print('navigate to page: ' + str(page))

df=pd.DataFrame({"SN":SN,"Name":NAME,"RDATE":RDATE,"STATUS":STATUS,"EmailVerified":EmailVerified,
                 "Train10days":Train10days,"StudentoutcomeForm":StudentoutcomeForm,"TestCompleted":TestCompleted,
                 # "UserNames":UserNames,"PWDs":PWDs
                 })
print(df)

# getting password and username
base_url = "https://www.pmgdisha.in/app/trainingCenter/studentsummary"
driver.get(base_url)

UserNames=[]
PWDs=[]
page=1
while page<=max_page:

 rows= WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='tbodyid']/tr")))
 for row in rows:
    # # getting password and username
    # row.find_element_by_xpath("./td[6]/a[2]").click()

    pope_ele = row.find_element_by_xpath("./td[6]/a[2]")
    driver.implicitly_wait(10)
    ActionChains(driver).click(pope_ele).perform()
    try:
        WebDriverWait(driver, 30).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        html = driver.execute_script("return document.documentElement.outerHTML")
    except:
        pass
    # switch to modal
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass

    # user_pwd = soup.find('div', class_ ="modal-content")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='stdactivate']/div/div/div[3]/label[1]")))
        print("found " + element.text)
        UserNames.append(element.text)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='stdactivate']/div/div/div[3]/label[2]")))
        print("found2 " + element.text)
        PWDs.append(element.text)
    # finally:
        ele1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='stdactivate']/div/div/div[4]/button")))
        ele1.click()
    except:
        UserNames.append("")
        PWDs.append("")

  # move on next page
 element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div/div[3]/div[1]/div[3]/div/div[2]/ul/li[5]/a")))
 driver.execute_script("arguments[0].click();", element)
 page=page+1
 print('navigate to page: ' + str(page))
df1=pd.DataFrame({"UserNames":UserNames,"PWDs":PWDs})


print(df1)
df.to_csv('output_IP.csv',index=False)


# logout and close
# element = driver.find_element_by_tag_name("a")
# element.click()
# driver.quit()




