import selenium.webdriver
import selenium.webdriver.support.ui as ui

dr = selenium.webdriver.Chrome()
dr.get('localhost:5000\login')
dr.implicitly_wait(10)
dr.find_element_by_id("user_id").send_keys("tomasyorke@hotmail.com")
dr.find_element_by_class_name("auth-button--user").click()
dr.find_element_by_id("password").send_keys("denada11")
dr.find_element_by_class_name("auth-button--password").click()

print(dr.get_cookies())