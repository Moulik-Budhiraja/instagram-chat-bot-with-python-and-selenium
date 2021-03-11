from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pickle
import random
import json

## VARIABLES ##

run = True
login_info = {}
chat_functions = {
    'test': {'loop': 0, 'send': 'test'}, 'mimic': {'loop': 0, 'send': ''}, 'spam': {'loop': 0, 'send': ''} 
}  # STRUCTURE: function:{loop:times to loop, 'send': what to type}

personal_commands = {}

## LOAD SAVED VARIABLES ##

# LOAD LOGIN INFO

try:
    with open('login info.json') as login_file:
        login_info = json.load(login_file)

except:
    login_info['username'] = input('Enter Username: ')
    login_info['password'] = input('Enter Password: ')

    with open('login info.json', 'w') as login_file:
        json.dump(login_info, login_file)

# LOAD CUSTOM COMMANDS

try:
    with open('commands.json') as command_file:
        personal_commands = json.load(command_file)

except:
    pass



## FUNCTIONS ##

# GENERAL FUNCTIONS

def reload_page():
    driver.refresh()
    try:
        person = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[@class="-qQT3 rOtsg"]'))
        )
    except:
        driver.quit()

    person.click()


def perform_commands():
    for value in chat_functions.values(): # DEFAULT COMMANDS
        if value['loop'] > 0:
            type_msg(value['send'])
            send_msg()
            value['loop'] -= 1
    time.sleep(0.1)

    for value in personal_commands.values(): # CUSTOM COMMANDS
        if value['loop'] > 0:
            type_msg(value['send'])
            send_msg()
            value['loop'] -= 1
    time.sleep(0.1)

def add_command(name, output):
    if personal_commands.get(name, False) == False:
        personal_commands[name] = {'loop': 0, 'send':output}
        type_msg('Command added')
        send_msg()

        with open('commands.json', 'w') as command_file:
            json.dump(personal_commands, command_file)
    else:
        type_msg('Command name already in use')
        send_msg()


# SEND FUNCTIONS

def type_msg(tx):
    search_bar = driver.find_element_by_xpath('//textarea')
    search_bar.send_keys(tx)


def new_line():
    search_bar = driver.find_element_by_xpath('//textarea')
    search_bar.send_keys(Keys.SHIFT, Keys.RETURN)


def send_msg():
    search_bar = driver.find_element_by_xpath('//textarea')
    search_bar.send_keys(Keys.RETURN)


# RETRIEVE FUNCTIONS

def get_messages():
    msgss = driver.find_elements_by_xpath(
        '//div[@class="VUU41"]/div[@class="                     Igw0E  Xf6Yq         eGOV_     ybXk5    _4EzTm                                                                                                              "]')

    msgs = []
    for i in msgss:
        msgs.append(i.text)
    return msgs


def is_command(msg):
    if msg != '' and msg[0] == '!':
        return msg[1:]
    return False


## INITIALIZATION AND LAUNCH ##
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://www.instagram.com/accounts/login/?next=/direct/inbox/')


## LOGIN ##

try:  # TRY LOADING COOKIES
    with open('cookies.pkl', 'rb') as cookie_file:
        cookies = pickle.load(cookie_file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        try:
            dismiss_noti = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='mt3GC']/button[2]"))
            )
        except:
            driver.quit()

        dismiss_noti.click()

        try:
            person = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@class="-qQT3 rOtsg"]'))
            )
        except:
            driver.quit()

        person.click()

except:  # LOGIN WITHOUT COOKIES
    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
    except:
        driver.quit()

    username.send_keys(login_info.get('username'))

    try:
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
    except:
        driver.quit()

    password.send_keys(login_info.get('password'))
    password.send_keys(Keys.RETURN)

    try:
        dismiss_login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="cmbtv"]'))
        )
    except:
        driver.quit()

    dismiss_login.click()

    try:
        dismiss_noti = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='mt3GC']/button[2]"))
        )
    except:
        driver.quit()

    dismiss_noti.click()

    try:
        person = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[@class="-qQT3 rOtsg"]'))
        )
    except:
        driver.quit()

    person.click()

    with open('cookies.pkl', 'wb') as cookie_file:  # SAVE COOKIES
        pickle.dump(driver.get_cookies(), cookie_file)

## MAIN LOOP ##

type_msg('Active')
send_msg()

while run:
    try:
        latest_msg = get_messages()[-1]
    except:
        latest_msg = ''

    try:
        if len(get_messages()) > 25:
            reload_page()
            print('reloaded')
    except:
        pass

    if is_command(latest_msg) == 'stop':
        for command in chat_functions.values():
            command['loop'] = 0

    elif is_command(latest_msg) == 'test':
        chat_functions['test']['loop'] = 1

    elif is_command(latest_msg) == 'who was in paris':
        chat_functions['who was in paris']['loop'] = 1

    elif is_command(latest_msg) != False and is_command(latest_msg)[:5] == 'mimic':
        chat_functions['mimic']['loop'] = 1
        chat_functions["mimic"]['send'] = latest_msg[7:].strip('(').strip(')')

    elif is_command(latest_msg) != False and is_command(latest_msg)[:4] == 'spam':
        try:
            chat_functions['mimic']['loop'] = int(latest_msg[6:].strip('(').strip(')').split(',')[1])
            chat_functions['mimic']['send'] = latest_msg[6:].strip('(').strip(')').split(',')[0]
        except:
            type_msg('Invalid Syntax')
            send_msg()

    elif is_command(latest_msg) != False and is_command(latest_msg)[:3] == 'add':
        command_name = latest_msg[5:].strip('(').strip(')').split(',')[0]
        output = latest_msg[5:].strip('(').strip(')').split(',')[1]
        
        add_command(command_name, output)

    for i in personal_commands:
        if is_command(latest_msg) == i:
            personal_commands[i]['loop'] = 1
    

    
        
    perform_commands()
