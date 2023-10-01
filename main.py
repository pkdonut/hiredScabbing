# program to automate the application process for scab work
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from faker import Faker
import time
import random
import requests
import string
from DataDecleration import EMAIL_DATA


# web = webdriver.Chrome()
# web.get('https://hiredinstaffing.com/submit-resume/')
fake = Faker()


def gen_email(name):
    full_name = name
    random_int = random.randint(99, 9999)
    email_num = str(random_int)
    email_choices = [float(line[2]) for line in EMAIL_DATA]
    email = full_name.lower() + email_num + "@" + random.choices(EMAIL_DATA, email_choices)[0][1]
    return email


def start_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)

    return driver


def gen_phone_number():
    number = fake.phone_number()
    while number == 0:
        number = fake.phone_number()
    else:

        return number


def create_fake_identity():
    fake_identity = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone_number": gen_phone_number(),
        "email": ''
    }

    fake_identity.update({"email": gen_email(fake_identity.get('first_name') + fake_identity.get('last_name'))})
    return fake_identity


def fill_out_form(driver, identity):

    # First Name
    driver.find_element(By.XPATH, '//*[@id="input_118129_1_3"]').send_keys(identity.get('first_name'))

    # Last Name
    driver.find_element(By.XPATH, '//*[@id="input_118129_1_6"]').send_keys(identity.get('last_name'))

    # Phone Number
    driver.find_element(By.XPATH, '//*[@id="input_118129_2"]').send_keys(identity.get('phone_number'))

    # Email
    driver.find_element(By.XPATH, '//*[@id="input_118129_3"]').send_keys(identity.get('email'))


def bypass_security_check(driver):
    num1 = int(driver.find_element(By.XPATH, '//*[@id="field_118129_6"]/div/span[1]').text)
    num2 = int(driver.find_element(By.XPATH, '//*[@id="field_118129_6"]/div/span[2]').text)
    sc_value = num1 + num2
    sc_entry = driver.find_element(By.XPATH, '//*[@id="field_118129_6"]/div/input[1]')
    sc_entry.send_keys(sc_value)


def send_application_count():
    requests.post('https://us-east4-trackingapi-398123.cloudfunctions.net/Add-Data-Count')


def main():
    url = 'https://hiredinstaffing.com/submit-resume/'
    identity = create_fake_identity()
    driver = start_driver(url)
    driver.get(url)

    print("Filling Out Application")
    fill_out_form(driver, identity)
    time.sleep(3)

    print("Bypassing security check")
    bypass_security_check(driver)
    time.sleep(3)
    print("Security check passed")

    print("Submitting Form")
    submit_button = driver.find_element(By.XPATH, '//*[@id="gform_submit_button_118129"]')
    submit_button.click()
    time.sleep(3)
    send_application_count()
    print("Form Submitted")

# Uncomment the following statement at your own peril
# while True:


main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
