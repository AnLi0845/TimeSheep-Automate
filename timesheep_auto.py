import argparse
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from tqdm.rich import tqdm
from rich.logging import RichHandler

def automate_timesheet(username, password, from_data_enter, to_data_enter, working_hour):
    # Set up logging with RichHandler
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])

    # Set up Firefox options for headless mode
    options = Options()
    options.add_argument("-headless")

    # Get today's date and extract the current day
    today = datetime.date.today()
    current_day = today.day

    # Initialize the WebDriver with headless mode
    driver = webdriver.Firefox(options=options)

    # Define the steps for the progress bar
    steps = [
        "Opening the login page",
        "Logging in",
        "Waiting for redirection to home page",
        "Clicking the timesheet button",
        "Waiting for the timesheet page to load",
        "Entering the from date",
        "Waiting for the timesheet page after entering the from date",
        "Entering the to date",
        "Entering the working hour",
        "Selecting the task",
        "Selecting the allocation time",
        "Saving the timesheet",
        "Waiting for the timesheet to be updated",
        "Closing the browser"
    ]

    with tqdm(total=len(steps), desc="Progress", leave=True) as progress_bar:
        try:
            logging.info("Opening the login page.")
            driver.get('https://timesheep.orz.ewalker.com.hk/loginpage')
            progress_bar.update(1)

            logging.info("Logging in.")
            username_field = driver.find_element(By.ID, ":r0:")
            password_field = driver.find_element(By.ID, ":r1:")
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'LOGIN')]")
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            progress_bar.update(1)

            logging.info("Waiting for redirection to home page.")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Time Sheet')]")))
            progress_bar.update(1)

            logging.info("Clicking the timesheet button.")
            timesheet_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Time Sheet')]")
            timesheet_button.click()
            progress_bar.update(1)

            logging.info("Waiting for the timesheet page to load.")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Timesheet Loaded')]")))
            progress_bar.update(1)

            logging.info("Entering the from date.")
            from_open = driver.find_element(By.ID, ":r0:")
            from_open.click()
            from_data = driver.find_element(By.XPATH, f"//button[contains(text(), '{from_data_enter}')]")
            from_data.click()
            from_data_confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
            from_data_confirm.click()
            progress_bar.update(1)

            if from_data_enter != current_day:
                logging.info("Waiting for the timesheet page to load after entering the from date.")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Timesheet Loaded')]")))
                progress_bar.update(1)

                logging.info("Entering the to date.")
                to_open = driver.find_element(By.ID, ":r2:")
                to_open.click()
                to_data = driver.find_element(By.XPATH, f"//button[contains(text(), '{to_data_enter}')]")
                to_data.click()
                to_data_confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
                to_data_confirm.click()
                progress_bar.update(1)
            else:
                progress_bar.update(2)
                logging.info("Skipping the to date as it is the current day.")

            logging.info("Entering the working hour.")
            working_hour_input = driver.find_element(By.ID, ":r4:")
            working_hour_input.clear()
            working_hour_input.send_keys(working_hour)
            progress_bar.update(1)

            logging.info("Selecting the task.")
            task_element = driver.find_element(By.ID, "taskprogressselect")
            task_element.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Execution')]")))
            task_select = driver.find_element(By.XPATH, "//li[contains(text(), 'Execution')]")
            task_select.click()
            progress_bar.update(1)

            logging.info("Selecting the allocation time.")
            WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiPopover-root")))
            allocation_time_element = driver.find_element(By.XPATH, f"//span[@data-index='{working_hour}']")
            allocation_time_element.click()
            progress_bar.update(1)

            logging.info("Saving the timesheet.")
            save = driver.find_element(By.XPATH, "//button[contains(text(), 'SAVE')]")
            save.click()
            progress_bar.update(1)

            logging.info("Waiting for the timesheet to be updated.")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Timesheet Updated')]")))
            progress_bar.update(1)

        finally:
            logging.info("Closing the browser.")
            driver.quit()
            progress_bar.update(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate timesheet entry.")
    parser.add_argument("username", help="Username for login")
    parser.add_argument("password", help="Password for login")
    parser.add_argument("--from_data_enter", type=int, default=21, help="From date")
    parser.add_argument("--to_data_enter", type=int, default=21, help="To date")
    parser.add_argument("--working_hour", type=int, default=8, help="Working hours")

    args = parser.parse_args()

    automate_timesheet(args.username, args.password, args.from_data_enter, args.to_data_enter, args.working_hour)
