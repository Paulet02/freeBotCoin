from selenium.webdriver.common.action_chains import ActionChains #to simulate the mouse movement and enable the play without captcha button
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import numpy.random as npr
import pyotp
import re
from selenium.webdriver.chrome.options import Options
import os
import telegram
from telegram.ext import Updater, CommandHandler
import yaml
import pickle

class Telegram_agent:
    token = None
    chat_id = None
    bot = None
    updater = None
    def __init__(self, file_config_path):
        #load_yaml
        try:
            with open(file_config_path, 'r') as config:
                bot_data = yaml.safe_load(config)
            print(bot_data)
        except Exception as e:
            print("Esto es un error", e)
        self.token = str(bot_data['id'])+":"+str(bot_data['key'])
        self.chat_id = bot_data['chat_id']
        self.bot = telegram.Bot(token=self.token)
        self.updater = Updater(self.token, use_context=True)
        #updater.dispatcher.add_handler(CommandHandler("now", send_max))
        # Start the Bot
        #self.updater.start_polling()


    def send_message(self, message, chat_id=None):
        if chat_id:
            self.bot.sendMessage(chat_id=chat_id, text=message)
        else:
            for id in self.chat_id:
                print(id)
                self.bot.sendMessage(chat_id=id, text=message)
			


    def send_image(self, image_path, chat_id):
        self.bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'))


    def send_hola(self):
        message = "hola"
        for id in self.chat_id:
            self.bot.sendMessage(chat_id=id, text=message)



data = {"email":"snowman.informer.19@gmail.com", "pass":"FreebitcoinSnowman2", "key2fa":"DWHL3F25MIYIVEKH", "ip":"188.6.197.119", "port":"39364"}

'''def time_remaining(driver):#a??adir funcionalidad de equivocarse
    try:
        element = driver.find_element(By.XPATH, '//div[@id="time_remaining"][@class="hasCountdown"]/span[@class="countdown_row countdown_show2"]/span[@class="countdown_section"][text()="Minutes"]/span[@class="countdown_amount"]')
        time_remaining = int(element.text)*60
        element = driver.find_element(By.XPATH, '//div[@id="time_remaining"][@class="hasCountdown"]/span[@class="countdown_row countdown_show2"]/span[@class="countdown_section"][text()="Seconds"]/span[@class="countdown_amount"]')
        time_remaining = time_remaining + int(element.text)
    except:
        time_remaining = 0
    return time_remaining'''
    
#Keys.BACKSPACE to delete character before the cursor
#Keys.DELETE to delete character after the cursor
def key_writting_simulation(element, string):#to test
    try:
        element.clear()#clean it
        last_character = ""
        for c in string:
            if npr.rand()>0.9:
                time.sleep(0.4*npr.rand())
                element.send_keys(Keys.BACKSPACE)
                time.sleep(0.15*npr.rand())#simulate human delay
                element.send_keys(last_character)
                element.send_keys(c)
            else:
                element.send_keys(c)#write a character
                time.sleep(0.15*npr.rand())#simulate human delay
            last_character = c
    except:
        pass

def wait_until_complete(driver):
    while(driver.execute_script("return document.readyState") != 'complete'):
        time.sleep(0.5)
    return driver
    
    
global dir_path
global image_path
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "screenshot.png")
cookies_path = os.path.join(dir_path, "cookies.pkl")
   
   
time_remaining = 0

def wait_seconds(seconds):
    global time_remaining
    time_remaining = seconds
    while time_remaining > 0:
        time.sleep(1)
        time_remaining = time_remaining - 1
    
t_agent = Telegram_agent(os.path.join(dir_path, "token.yaml"))

send_price = lambda update, context: t_agent.send_message("El ultimo precio ha sido:")
t_agent.updater.dispatcher.add_handler(CommandHandler("last_price", send_price))

send_time = lambda update, context: t_agent.send_message(str(time_remaining)+" seconds left")
t_agent.updater.dispatcher.add_handler(CommandHandler("time", send_time))

def send_last(update, context):
    if os.path.isfile(image_path):
        t_agent.send_image(image_path, t_agent.chat_id[0])
    else:
        t_agent.send_message("No image")

t_agent.updater.dispatcher.add_handler(CommandHandler("last_screenshot", send_last))



def login(driver):
    if data['key2fa']:
        second_factor = True
        totp = pyotp.TOTP(data['key2fa'])
        
        
    element = WebDriverWait(driver, 30, poll_frequency=1).until(expected_conditions.element_to_be_clickable((By.XPATH, '//li[@class="login_menu_button"]/a[text()="LOGIN"]')))#find the login tab
    element.click()#click on it
    
    driver.get_screenshot_as_file(image_path)
    t_agent.send_image(image_path, t_agent.chat_id[0])
    
    
    #finding the username input element
    element = driver.find_element(By.XPATH, '//input[@id="login_form_btc_address"][@name="btc_address"]')
    element.clear()#clean it
    key_writting_simulation(element, data['email'])#ElementNotInteractableException: Message: Element is not visible

    # pop up 
    try:#class pushpad_deny_button
        wait = WebDriverWait(driver, 3, poll_frequency=1)
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="pushpad_deny_button"]'))) 
        ActionChains(driver).move_to_element(element).perform() 
        element.click()#click on it
    except:
        print("No hay pop up")
    
    
    #finding the password input element
    element = driver.find_element(By.XPATH, '//input[@id="login_form_password"][@name="password"]')
    element.clear()#clean it
    key_writting_simulation(element, data['pass'])
    
    try:#class pushpad_deny_button
        wait = WebDriverWait(driver, 3, poll_frequency=1)
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="pushpad_deny_button"]'))) 
        ActionChains(driver).move_to_element(element).perform() 
        element.click()#click on it
    except:
        print("No hay pop up")
    
    #finding the 2fa input element if enable
    if second_factor:
        element = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="login_form_2fa"][@name="2fa_code"]')))
        element.clear()
        key_writting_simulation(element, totp.now())
    
    try:#class pushpad_deny_button
        wait = WebDriverWait(driver)
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="pushpad_deny_button"]'))) 
        ActionChains(driver).move_to_element(element).perform() 
        element.click()#click on it
    except:
        print("No hay pop up")
    
    #finding the login button
    element = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@id="login_button"][@class="new_button_style profile_page_button_style center"][text()="LOGIN!"]')))
    ActionChains(driver).move_to_element(element).perform()#MoveTargetOutOfBoundsException if scroll  or click the login button
    element.click()#click on it
    try:
        element.click()
    except Exception as e:
        print(e)
    time.sleep(2)
    driver.get_screenshot_as_file(image_path)
    t_agent.send_image(image_path, t_agent.chat_id[0])
    
    return driver

def setup():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    return driver
        

def store_cookies(driver):
    pickle.dump( driver.get_cookies() , open(cookies_path,"wb"))
    
def load_cookies(driver):
    cookies = pickle.load(open(cookies_path, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
        
    return driver

def do_macro(data, driver):
    #setting up
    #data -> second_factor ->key2fa
    

    
    
    
    print("Driver created")
    
    #driver = webdriver.Firefox(options = options, executable_path = path_geckodriver, capabilities = set_proxy_firefox(data['ip'], data['port']))

    
    #profile = webdriver.FirefoxProfile()
    #driver = webdriver.Firefox(executable_path = path_geckodriver)
    
    #url2="https://freebitco.in/?op=signup_page"
    #driver.get(url2)#web page url
    #driver = wait_until_complete(driver)
    
    #hacer funcion que dada una cadena de un elemento te de el xpath pj <input name="continue" type="submit" value="Login" />
    #element = driver.find_element(By.XPATH, '//li[@class="login_menu_button"]/a[text()="LOGIN"]')
    time.sleep(2)
    
    
    print("Dentro")
    driver.get_screenshot_as_file(image_path)
    #t_agent.send_image(image_path, t_agent.chat_id[0])
    
    
    #(EC.staleness_of(login))
    
#driver.get('http://stackoverflow.com/')
#wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#h-top-questions')))
#driver.execute_script("window.stop();")
    
    #if #error_too_many_tries(driver)#test too many tries error -> get the minutes
    #print(error_too_many_tries(driver))
    
    time.sleep(1)
    try:
        #in homepage find the free roll button
        wait = WebDriverWait(driver, 30)
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[@class="free_play_link"][text()="FREE BTC"]'))) 
        ActionChains(driver).move_to_element(element).perform() 
        element.click()#click on it
    except Exception as e:
        print(e)
    
    print("Free play link")
    driver.get_screenshot_as_file(image_path)
    #t_agent.send_image(image_path, t_agent.chat_id[0])
    #time.sleep(3)
    
    #close the "no thanks" popup
    try:
        wait = WebDriverWait(driver, 30, poll_frequency=1)
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[text()="NO THANKS"]'))) 
        ActionChains(driver).move_to_element(element).perform() 
        element.click()#click on it
    except Exception as e:
        print(e)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll to bottom
    
    #if hay captcha y no esta la cuenta atras, entonces lo llamas
    #solve_captcha(driver)
    
    #find no captcha roll button
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll to bottom
    #wait = WebDriverWait(driver, 30)
    #element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[@id="play_without_captchas_button"][@class="play_without_captcha_button center"]'))) 
    #ActionChains(driver).move_to_element(element).perform() 
    #element.click()#click on it

    #find roll button
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll to bottom
    wait = WebDriverWait(driver, 30)
    element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="free_play_form_button"][@class="free_play_element new_button_style profile_page_button_style"][@value="ROLL!"]'))) 
    ActionChains(driver).move_to_element(element).perform() 
    element.click()#click on it
    
    time.sleep(3)
    print("Done")
    driver.get_screenshot_as_file(image_path)
    t_agent.send_image(image_path, t_agent.chat_id[0])
    #element = driver.find_element(By.XPATH, '//button[@class="new_button_style red_button_big homepage_play_now_button"][text()="PLAY NOW"]')
    
    #time.sleep(2)
    #time_sleep = time_remaining(driver)
    #t_agent.send_message("Waiting " +str(time_sleep))
    
    #time.sleep(time_sleep)
    #time.sleep(npr.randint(1,10))
    #driver.close()
    
    '''
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll to bottom
    wait = WebDriverWait(driver, 30)
    element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[@id="switch_captchas_button"]'))) 
    ActionChains(driver).move_to_element(element).perform() 
    element.click()#click on it
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll to bottom
    img = driver.find_element_by_xpath('//div[@id="botdetect_free_play_captcha"]/div[@class="captchasnet_captcha_content"]/img')
    src = img.get_attribute('src')

    # download the image
    urllib.request.urlretrieve(src, r'C:/Users/Paulet/Desktop/Box Sync/Business/Apuestas/captcha.png')
    
    '''
    
    

    
data = {"email":"snowman.informer.19@gmail.com", "pass":"FreebitcoinSnowman2", "key2fa":"DWHL3F25MIYIVEKH", "ip":"188.6.197.119", "port":"39364"}


t_agent.send_message("Starting...")
print("Starting...")

t_agent.updater.start_polling()

#driver = setup()

#url = "https://freebitco.in/?op=signup_page"
#driver.get(url)#web page url
#time.sleep(1)

#if os.path.isfile(cookies_path):
#    print("Cookies")
#    url = "https://freebitco.in/?op=signup_page"
#    driver.get(url)#web page url
#    driver = load_cookies(driver)
#    driver.get(url)#web page url
#else:
#    print("logged in")
#    driver = login(driver)

#close pop up

#time.sleep(2)
#driver.get_screenshot_as_file(image_path)
#t_agent.send_image(image_path, t_agent.chat_id[0])


wait_seconds(60*60)
while 1:
    try:
        driver = setup()
        time.sleep(1)
        if os.path.isfile(cookies_path):
            print("Cookies")
            url = "https://freebitco.in/?op=signup_page"
            driver.get(url)#web page url
            driver = load_cookies(driver)
            driver.get(url)#web page url
        else:
            print("logged in")
            driver = login(driver)
        do_macro(data, driver)
        t_agent.send_message("Waiting " +str(60*60)+" seconds")
        wait_seconds(60*60)
    except Exception as e:
        print(e)
        
        t_agent.send_message("Problema en el main")
        t_agent.send_message(str(e))