# import packages required
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

# Creating a connection to mysql to import data into database
try:
    mydb = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'ShahulSqL2024'
    )
    print("Connection Established")
    cursor = mydb.cursor()
    cursor.execute("create database if not exists redbus")
    mydb.commit()
    print("Database created successfully")
    cursor.execute("use redbus")
    cursor.execute("drop table if exists bus_routes")

except mysql.connector.Error as e:
    print(f"An error occured {e}")

host = '127.0.0.1'
db = 'redbus'
user = 'root'
pw = 'ShahulSqL2024'

engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")

# inititate browser
driver = webdriver.Chrome()

# initiate action chains
actions = ActionChains(driver)


transport_state = ['Andhra Pradesh','Kerala','Telangana','Karnataka','Rajasthan','South Bengal','Haryana','Assam','Uttar Pradesh','West Bengal','Chandigarh','Punjab']
transport_info = [
    'https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/astc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile',
    'https://www.redbus.in/online-booking/chandigarh-transport-undertaking-ctu',
    'https://www.redbus.in/online-booking/pepsu/?utm_source=rtchometile'
    ]

# scroll pages to the bottom to load all the data
def is_at_end_of_page(driver):
    # Execute JavaScript to get the scroll position, document height, and viewport height
    scroll_position = driver.execute_script("return window.scrollY;")
    page_height = driver.execute_script("return document.documentElement.scrollHeight;")
    viewport_height = driver.execute_script("return window.innerHeight;")
    
    # Check if we've reached the bottom of the page
    return scroll_position + viewport_height >= page_height


for j,k in zip(transport_info,transport_state):
    # opening web page
    driver.get(j);
    driver.maximize_window()
    time.sleep(3)

    # declaring empty list to store values
    route_name = []
    route_link = []
    rte_name = []
    rte_link = []
    bus_name = []
    bus_type = []
    departing_time = []
    duration = []
    reaching_time = []
    star_rating = []
    price = []
    seat_availability = []
    state = []

    # identifying the number of pages found in each web page
    no_of_pages = len(driver.find_elements(By.CLASS_NAME, 'DC_117_pageTabs '))

    # looping through the pages
    for n in range(1,no_of_pages+1):
        actions.move_to_element(driver.find_element(By.XPATH, "//*[@id='root']/div/div[4]/div[12]/div[text()='" + str(n) + "']")).click()
        actions.perform()
        temp_route = driver.find_elements(By.XPATH, "//a[@class='route']")
        
        # looping through the selenium object to extract data into the list
        for i in temp_route:
            rte_name.append(i.text)
            rte_link.append(i.get_dom_attribute('href'))

    # looping through the extracted 
    for r,s in zip(rte_name,rte_link):
        
        driver.get(s);
        time.sleep(10)

        check = len(driver.find_elements(By.XPATH,"//h3[text()='Oops! No buses found.']"))

        if check > 0:
            actions.move_to_element(driver.find_element(By.XPATH,"//*[@id='fixer']/div/div/div[1]/span[@class='next']")).click()
            actions.perform()
            time.sleep(5)

        # identify the number of expandable options within the webpage
        no_of_clicks = driver.find_elements(By.XPATH,"//*[@class='button']")

        clicks = len(no_of_clicks)

        if clicks <= 1:
            for t in no_of_clicks:
                t.click()
                time.sleep(3)
        else:
            clicks = len(no_of_clicks)-1
            for t in range(clicks,-1,-1):
                no_of_clicks[t].click()
                time.sleep(5)

        # Scroll down and check if we are at the end
        while not is_at_end_of_page(driver):
            # Scroll down by sending PAGE_DOWN or by using JavaScript
            driver.find_element('tag name', 'body').send_keys(Keys.PAGE_DOWN)

        list_items = driver.find_elements(By.XPATH, "//*[@class='row-sec clearfix']")

        for a in list_items:
            state.append(k)
            route_name.append(r)
            route_link.append(s)
            bus_name.append(driver.find_element(By.XPATH, "//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[1]/div[1]").text)
            bus_type.append(driver.find_element(By.XPATH, "//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[1]/div[2]").text)
            departing_time.append(driver.find_element(By.XPATH,"//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[2]/div[1]").text)
            duration.append(driver.find_element(By.XPATH,"//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[3]/div").text)
            reaching_time.append(driver.find_element(By.XPATH,"//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[4]/div[1]").text)
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[5]/div[1]/div/span"))
                )
                star_rating.append(element.text)
            except TimeoutException:
                star_rating.append(0)
            price.append(driver.find_element(By.XPATH,"//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[6]/div/div/span").text)
            seat_availability.append((driver.find_element(By.XPATH,"//*[@id='" + a.get_dom_attribute('id') + "']/div/div[1]/div[1]/div[7]/div").text).split(' ')[0])
        
    col_name = ['state','bus_route_name', 'bus_route_link', 'bus_name', 'bus_type', 'departing_time', 'duration', 'reaching_time', 'star_rating', 'price', 'seat_availability']
    df = pd.DataFrame(list(zip(state,route_name,route_link,bus_name,bus_type,departing_time,duration,reaching_time,star_rating,price,seat_availability)),columns=col_name)

    df.to_sql('bus_routes',engine,if_exists='append',index=False)
    df.to_csv(f"{k}.csv",index=False)
    print(f"{k} is successfully extracted")

cursor.execute('Alter table bus_routes add column id int auto_increment primary key')
cursor.execute('Alter table bus_routes modify column departing_time time')
cursor.execute('Alter table bus_routes modify column reaching_time time')
cursor.execute('Alter table bus_routes modify column star_rating float')
cursor.execute('Alter table bus_routes modify column price decimal')
cursor.execute('Alter table bus_routes modify column seat_availability int')

print('Data Extracted Successfully!')

driver.quit()