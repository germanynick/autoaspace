from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os, json, string, random

def create(driver: webdriver, cfg_signup_link: str):
    wait = WebDriverWait(driver, 30)

    # Go to signup link
    driver.get(cfg_signup_link)

    # Generate random email/password
    email = f"a{''.join(random.sample(string.ascii_lowercase + string.digits, 10))}@outlook.com"
    password = ''.join(random.sample(string.ascii_letters, 8))
    
    print(f"Account creation started | {email}")

    # Enter email
    wait.until(EC.visibility_of_element_located((By.ID, "MemberName"))).send_keys(email)
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    # Enter password
    wait.until(EC.visibility_of_element_located((By.ID, "PasswordInput"))).send_keys(password)
    # Uncheck promotion checkbox
    wait.until(EC.visibility_of_element_located((By.ID, "iOptinEmail"))).click()
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "BirthDateCountryAccrualInputPane")))
    # Select country
    Select(driver.find_element(By.ID, "Country")).select_by_value("US")
    # Select birthday month
    Select(driver.find_element(By.ID, "BirthMonth")).select_by_value("1")
    # Select birthday day
    Select(driver.find_element(By.ID, "BirthDay")).select_by_value("1")
    # Select birthday year
    driver.find_element(By.ID, "BirthYear").send_keys("2000")
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    # Ask the user to manually complete the captcha
    wait.until(EC.visibility_of_element_located((By.ID, "enforcementFrame"))).click()
    print(f"Captcha completion required | {email}")

    WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))

    # Save credentials to file
    with open("accounts.txt", "a") as f:
        f.write(f"{email}:{password}\n")

    return email

def run(amount: int, drive_type: str, signup_link: str):
    try:
        cfg_signup_link = signup_link.lower()
        cfg_webdriver = drive_type.lower()

        

        if "firefox" in cfg_webdriver or "gecko" in cfg_webdriver:
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        elif "chrome" in cfg_webdriver:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        emails = [create(driver, cfg_signup_link=cfg_signup_link) for _ in range(amount)]
        
        return f"Creating {amount} accounts with {cfg_webdriver} webdriver\n {emails.join(', ')}"
    except Exception as e:
        print(e)
        return e

    
