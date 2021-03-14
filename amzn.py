from selenium import webdriver
base_url="https://www.amazon.in"
# declare and initialize driver variable
driver=webdriver.Chrome(executable_path="C:/Users/Welcome/PycharmProjects/Webautomation/drivers/chromedriver.exe")
# browser should be loaded in maximized window
driver.maximize_window()
# driver should wait implicitly for a given duration, for the element under consideration to load.
# to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
driver.implicitly_wait(10) #10 is in seconds
# to load a given URL in browser window
driver.get(base_url)
# test whether correct URL/ Web Site has been loaded or not
assert "Amazon" in driver.title
# to close the browser
driver.close()