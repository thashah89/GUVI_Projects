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
import pymysql

# Database Connection and Setup
def setup_database():
    try:
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='ShahulSqL2024')
        cursor = mydb.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS redbus")
        cursor.execute("USE redbus")
        cursor.execute("DROP TABLE IF EXISTS bus_routes")
        cursor.execute("CREATE TABLE IF NOT EXISTS bus_routes ("
                       "id INT AUTO_INCREMENT PRIMARY KEY, "
                       "state VARCHAR(50), "
                       "bus_route_name TEXT, "
                       "bus_route_link TEXT, "
                       "bus_name TEXT, "
                       "bus_type TEXT, "
                       "departing_time TIME, "
                       "duration TEXT, "
                       "reaching_time TIME, "
                       "star_rating FLOAT, "
                       "price DECIMAL(10, 2), "
                       "seat_availability INT)")
        return create_engine("mysql+pymysql://root:ShahulSqL2024@127.0.0.1/redbus")
    except pymysql.Error as e:
        print(f"Database Error: {e}")
        exit()

# Web Scraping Functions
def is_at_end_of_page(driver):
    "Check if the webpage is scrolled to the bottom."
    scroll_position = driver.execute_script("return window.scrollY;")
    page_height = driver.execute_script("return document.documentElement.scrollHeight;")
    viewport_height = driver.execute_script("return window.innerHeight;")
    return scroll_position + viewport_height >= page_height

def scroll_page(driver):
    "Scrolls the page to the bottom."
    while not is_at_end_of_page(driver):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

def extract_route_data(driver, state, route_name, route_link):
    "Extracts data for a single route."
    driver.get(route_link)
    time.sleep(10)
    try:
        # Handle cases where buses are not found
        if len(driver.find_elements(By.XPATH, "//h3[text()='Oops! No buses found.']")) > 0:
            driver.find_element(By.XPATH, "//*[@id='fixer']/div/div/div[1]/span[@class='next']").click()
            time.sleep(5)

        # Expand all bus listings
        expand_buttons = driver.find_elements(By.XPATH, "//*[@class='button']")
        for btn in reversed(expand_buttons):
            btn.click()
            time.sleep(3)

        scroll_page(driver)

        # Extract bus data
        bus_elements = driver.find_elements(By.XPATH, "//*[@class='row-sec clearfix']")
        route_data = []
        for bus in bus_elements:
            
            try:
                # Try to find the star rating element
                star_rating_element = bus.find_element(By.XPATH, ".//*[@class='column-six p-right-10 w-10 fl']")
                star_rating_text = star_rating_element.text.strip()
                if star_rating_text:
                    star_rating = star_rating_text.split()[0].replace('New', '0')  # Process rating
                else:
                    star_rating = 0
            except Exception as e:
                print(f"Star rating not found or invalid: {e}")

            
            route_data.append({
                "state": state,
                "bus_route_name": route_name,
                "bus_route_link": route_link,
                "bus_name": bus.find_element(By.XPATH, ".//*[@class='travels lh-24 f-bold d-color']").text,
                "bus_type": bus.find_element(By.XPATH, ".//*[@class='bus-type f-12 m-top-16 l-color evBus']").text,
                "departing_time": bus.find_element(By.XPATH, ".//*[@class='dp-time f-19 d-color f-bold']").text,
                "duration": bus.find_element(By.XPATH, ".//*[@class='dur l-color lh-24']").text,
                "reaching_time": bus.find_element(By.XPATH, ".//*[@class='bp-time f-19 d-color disp-Inline']").text,
                "star_rating": star_rating,
                "price": bus.find_element(By.XPATH, ".//div[contains(@class, 'fare d-block')]//span").text,
                "seat_availability": bus.find_element(By.XPATH, ".//*[contains(@class, 'column-eight w-15 fl')]/div[1]").text.split(' ')[0]
            })
        return route_data
    except Exception as e:
        print(f"Error extracting data for {route_name}: {e}")
        return []

def scrape_state_data(driver, state, state_url):
    "Scrapes all routes for a given state."
    actions = ActionChains(driver)
    driver.get(state_url)
    route_name, route_link, route_data = [], [], []
    
    # identifying the number of pages found in each web page
    no_of_pages = len(driver.find_elements(By.CLASS_NAME, 'DC_117_pageTabs '))

    # looping through the pages
    for n in range(1,no_of_pages+1):
        actions.move_to_element(driver.find_element(By.XPATH, "//*[@id='root']/div/div[4]/div[12]/div[text()='" + str(n) + "']")).click()
        actions.perform()
        routes = driver.find_elements(By.XPATH, "//a[@class='route']")
        
        # looping through the selenium object to extract data into the list
        for route in routes:
            route_name.append(route.text)
            route_link.append(route.get_attribute('href'))
    
    for r_name, r_link in zip(route_name,route_link):
        route_data.extend(extract_route_data(driver, state, r_name, r_link))
    return route_data

# Main Execution
def main():
    engine = setup_database()
    driver = webdriver.Chrome()
    driver.maximize_window()

    transport_states = ['Andhra Pradesh','Kerala','Telangana','Karnataka','Rajasthan','South Bengal','Haryana','Assam','Uttar Pradesh','West Bengal','Chandigarh','Punjab']
    transport_urls = [
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

    for state, url in zip(transport_states, transport_urls):
        print(f"Scraping data for {state}...")
        state_data = scrape_state_data(driver, state, url)
        if state_data:
            df = pd.DataFrame(state_data)
            df.to_sql('bus_routes',engine , if_exists='append', index=False)
            df.to_csv(f"{state}.csv", index=False)
            print(f"{state} data scraped and saved successfully.")

    driver.quit()
    print("Scraping completed!")

if __name__ == "__main__":
    main()
