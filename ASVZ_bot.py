from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import sys

class ASVZ_bot:

    def __init__(self , goal_day , goal_time , eth_username, eth_password, delay=2 , max_load_delay=5 , button_wait=180 ):
        self.goal_day = goal_day
        self.goal_time = goal_time
        self.start_time = goal_time +":00" # start to look for button (should be same as goal time)
        self.delay = delay
        self.max_load_delay = max_load_delay
        self.button_wait = button_wait

        # eth login information
        self.eth_username = eth_username
        self.eth_password = eth_password

        # set up driver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        PATH = '/usr/bin/chromedriver'
        #PATH = "/Users/jan-philippvonbassewitz/bot_automation/chromedriver"
        self.driver = webdriver.Chrome(PATH, options=chrome_options)
        print("Bot is initialized!")


    def find_section_in_sections_with_element(self, sections_class, sub_element_class, search_for,max_load_delay):
        try:
            sections = WebDriverWait(self.driver, max_load_delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME,sections_class)))
            for section in sections:
                sub_element = section.find_element_by_class_name(sub_element_class)
                if (sub_element.text == search_for):
                    return section
        except:
            print("Something went wrong with method find_section_in_sections_with_element!")
            self.driver.quit()


    def quickly_press_button_with_CLASS_NAME(self,btn_CLASS_NAME,max_load_delay):
        try:
            button = WebDriverWait(self.driver, max_load_delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, btn_CLASS_NAME)))
            button.click()
        except TimeoutException:
            print ("Page didn'load or took to long when trying to press button!")
            self.driver.quit()


    def quickly_press_button_with_ID(self,btn_ID,max_load_delay):
        try:
            button = WebDriverWait(self.driver, max_load_delay).until(
                EC.presence_of_element_located((By.ID, btn_ID)))
            button.click()
        except TimeoutException:
            print ("Page didn'load or took to long when trying to press button!")
            self.driver.quit()


    def is_earlier_then(self,time1, time2):
        if int(time1[0:2]) < int(time2[0:1]):
            return True
        else:
            if int(time1[0:2]) > int(time2[0:2]):
                return False

        if int(time1[3:5]) < int(time2[3:5]):
            return True
        else:
            if int(time1[3:5]) > int(time2[3:5]):
                return False

        if int(time1[6:8]) < int(time2[6:8]):
            return True
        else:
            if int(time1[6:8]) > int(time2[6:8]):
                return False
        return False


    def reserve(self):

        # go to Serientrackingtool and login -> wait till site is loaded
        self.driver.get('https://www.asvz.ch/426-sportfahrplan?f[0]=facility:45598&f[1]=sport:122920')
        time.sleep(self.delay)


        # Find section for the day that I want to reserve
        goal_day_section = self.find_section_in_sections_with_element('teaser-list-calendar__day', 'day.text-tiny', self.goal_day,self.max_load_delay)
        # Find section in goal_day_section for the time I want to reserve
        time_slots_info = goal_day_section.find_elements_by_class_name("btn-hover-parent")
        goal_time_section = 0
        for time_slot_info in time_slots_info:
            time_slot = time_slot_info.find_element_by_class_name("offer__time")
            if( time_slot.text[0:5] == self.goal_time ):
                goal_time_section = time_slot_info


        # move to login page for specific time and day
        link = goal_time_section.find_element_by_class_name("offer.flex.link").get_attribute("href")
        self.driver.get(link)


        # move to site where you choose login method
        self.quickly_press_button_with_CLASS_NAME('btn.btn-default.ng-star-inserted',self.max_load_delay)


        # move to switch ai login site
        self.quickly_press_button_with_CLASS_NAME('btn.btn-warning.btn-block',self.max_load_delay)


        # choose eth on switch ai login site
        self.quickly_press_button_with_ID('userIdPSelection_iddicon',self.max_load_delay)
        universities = self.driver.find_elements_by_class_name('idd_listItem.idd_listItem_Nested')
        for university in universities:
            if( 'eth' in university.get_attribute('data')):
                university.click()
                break


        # login at eth shibboleth
        try:
            username_field = WebDriverWait(self.driver, self.max_load_delay).until(EC.presence_of_element_located((By.ID, 'username')))
            username_field.send_keys(self.eth_username)
        except TimeoutException:
            print ("Something went wrong when doing login with eth account!")
            self.driver.quit()
            return 0
        self.driver.find_element_by_id('password').send_keys(self.eth_password)
        self.driver.find_element_by_class_name('btn').click()


        print("Waiting for: " + time.strftime("%H:%M:%S", time.localtime())[0:5] +" == "+ self.start_time[0:5])
        while True:
            if time.strftime("%H:%M:%S", time.localtime())[0:5] == self.start_time[0:5]:
                break
        print("Start looking for button when time: " + time.strftime("%H:%M:%S", time.localtime()))


        try:
            print("Looking for button ...")
            reserve_button = WebDriverWait(self.driver, self.button_wait).until(EC.presence_of_element_located((By.ID, 'btnRegister')))
            reserve_button.click()
        except TimeoutException:
            print("It seems like the timeslot at " + self.goal_time + " on " + self.goal_day +
                  " has been booked out already or is impossible to book, because bot couldn't find button.")
            self.driver.quit()
            return 0


        print("Clicked the button for Fitness timeslot at " + self.goal_time + " on " + self.goal_day)
        time.sleep(120)
        self.driver.quit()
        return 0







