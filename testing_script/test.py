from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Set the options for the headless browser
options = Options()
options.add_argument("-headless") 
today = datetime.date.today()
current_day = today.day
driver = webdriver.Firefox(options=options)
#user defined variables
from_data_enter = 21
to_data_enter = 21
working_hour = 8

#Open the browser and go to the system
logging.info("Opening the login page.")
driver.get('https://timesheep.orz.ewalker.com.hk/loginpage')
#login to timesheet
logging.info("Logging in.")
username = driver.find_element(By.ID, ":r0:")
password = driver.find_element(By.ID, ":r1:")
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'LOGIN')]")
username.send_keys("")
password.send_keys("")
login_button.click()
#Wait for the page to load
logging.info("Waiting for redirection to home page.")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Time Sheet')]")))
#Click on the timesheet button
logging.info("Clicking the timesheet button.")
timesheet_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Time Sheet')]")
timesheet_button.click()
#Wait for the page to load
logging.info("Waiting for the timesheet page to load.")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Welcome Man Shun Anson Li to Timesheet')]")))
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Timesheet Loaded')]")))
#Enter ther from date
logging.info("Entering the from date.")
from_open = driver.find_element(By.ID, ":r0:")
from_open.click()
from_data = driver.find_element(By.XPATH, f"//button[contains(text(), '{from_data_enter}')]")
from_data.click()
from_data_confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
from_data_confirm.click()
#Wait for the page to load
if from_data_enter != current_day:
    logging.info("Waiting for the timesheet page to load after entering the from date.")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Timesheet Loaded')]")))
    #Enter the to date
    logging.info("Entering the to date.")
    to_open = driver.find_element(By.ID, ":r2:")
    to_open.click()
    to_data = driver.find_element(By.XPATH, f"//button[contains(text(), '{to_data_enter}')]")
    to_data.click()
    to_data_confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
    to_data_confirm.click()
#Enter the working hour
logging.info("Entering the working hour.")
working_hour_input = driver.find_element(By.ID, ":r4:")
working_hour_input.clear()
working_hour_input.send_keys(working_hour)
#Select the task
logging.info("Selecting the task.")
task = driver.find_element(By.ID, "taskprogressselect")
task.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Execution')]")))
task_select = driver.find_element(By.XPATH, "//li[contains(text(), 'Execution')]")
task_select.click()
#Select the allocation time
logging.info("Selecting the allocation time.")
WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiPopover-root")))
allocation_time_element = driver.find_element(By.XPATH, f"//span[@data-index='{working_hour}']")
allocation_time_element.click()
#$Save the timesheet
logging.info("Saving the timesheet.")
save = driver.find_element(By.XPATH, "//button[contains(text(), 'SAVE')]")
save.click()
#Wait for the form to submit
logging.info("Waiting for the timesheet to be updated.")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Timesheet Updated')]")))
logging.info("Closing the browser.")
driver.quit()
