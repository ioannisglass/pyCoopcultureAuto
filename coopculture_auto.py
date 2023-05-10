from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

strDate = input('Input date (mm-dd-yyyy) \n')
objDate = datetime.strptime(strDate, '%m-%d-%Y').date()
strDate = objDate.strftime("%d/%m/%Y")

strTime = input('Input time (hh:mm) \n')
objTime = datetime.strptime(strTime, '%H:%M')
strTime = objTime.strftime("%H:%M")

strQuantity = input('Input quantity \n')
nQuantity = int(strQuantity)
strTicketType = input('Input ticket type \n')
strCheckFrequency = input('Input Availability Check Frequency \n')
nCheckFrequency = int(strCheckFrequency)
strDateTimeToStart = input('Input date-time to start availability-check (mm-dd-yyyy hh:mm) \n')
strDateTimeToStop = input('Input date-time to stop availability-check (mm-dd-yyyy hh:mm) \n')

captcah_err_list = [
    'ERROR_ZERO_CAPTCHA_FILESIZE',
    'ERROR_WRONG_USER_KEY',
    'ERROR_KEY_DOES_NOT_EXIST',
    'ERROR_ZERO_BALANCE',
    'ERROR_PAGEURL',
    'ERROR_NO_SLOT_AVAILABLE',
    'ERROR_TOO_BIG_CAPTCHA_FILESIZE',
    'ERROR_WRONG_FILE_EXTENSION',
    'ERROR_IMAGE_TYPE_NOT_SUPPORTED',
    'CAPCHA_NOT_READY'
]

strUrl = 'https://ecm.coopculture.it/index.php?option=com_snapp&view=event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79E95CA-090E-FDA8-2364-017448FF0FA0&lang=it'

# check time, time is match, run selenium
objTimeToStart = datetime.strptime(strDateTimeToStart, '%m-%d-%Y %H:%M')
objTimeToStop = datetime.strptime(strDateTimeToStop, '%m-%d-%Y %H:%M')
while True:
    objCurrentTime = datetime.now()
    if objCurrentTime >= objTimeToStop:
        print("Time is over.")
        exit()
    elif objCurrentTime >= objTimeToStart:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        chrome_options.add_argument('start-maximized')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
        stealth(
            chrome_driver,
            user_agent='',
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=False
        )
        chrome_driver.maximize_window()
        chrome_driver.get(strUrl)
        
        # check availability of day
        # available_dates = chrome_driver.find_elements(By.XPATH, "//td[@class='calendar-day  text-center' and @style='background: #eee']")
        # available_dates = chrome_driver.find_elements(By.XPATH, "//div[@class='day-number available active']")
        xpath_day = "//div[@class='day-number available active' and @data-date='" + strDate + "']"
        try:
            elem_available = WebDriverWait(chrome_driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_day)))
            # elem_available = chrome_driver.find_element(By.XPATH, xpath_day)
            # elem_available.click()
            chrome_driver.execute_script("arguments[0].click();", elem_available)
        except NoSuchElementException as e:
            #btn_next_month = chrome_driver.find_element(By.XPATH, "//div[@class='next changemonth glyphicon glyphicon-chevron-right']")
            # btn_next_month.click()
            btn_next_month = WebDriverWait(chrome_driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='next changemonth glyphicon glyphicon-chevron-right']")))
            chrome_driver.execute_script("arguments[0].click();", btn_next_month)
            try:
                # elem_available = chrome_driver.find_element(By.XPATH, xpath_day)
                elem_available = WebDriverWait(chrome_driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_day)))
                # elem_available.click()
                chrome_driver.execute_script("arguments[0].click();", elem_available)
            except NoSuchElementException as e:
                time.sleep(nCheckFrequency)
                continue
        
        # check availability of time
        bTimeAvailable = False
        while True:
            WebDriverWait(chrome_driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='perf_row even row-height2 text-center']")))
            elems_time = chrome_driver.find_elements(By.XPATH, "//div[@class='perf_row even row-height2 text-center']")
            elems_odd_time = chrome_driver.find_elements(By.XPATH, "//div[@class='perf_row odd row-height2 text-center']")
            elems_time += elems_odd_time
        
            if elems_time != None and len(elems_time) > 0:
                for elem_time in elems_time:
                    strLineTime = elem_time.find_elements(By.XPATH, ".//div")[0].text
                    if strTime in strLineTime:
                        btnAvailable = elem_time.find_element(By.XPATH, ".//button")
                        strTemp = btnAvailable.text
                        strTemp = strTemp[strTemp.find('(') + 1 : strTemp.find(')')]
                        nAvailableCount = int(strTemp.strip())
                        if nQuantity > nAvailableCount:
                            nQuantity = nAvailableCount
                        bTimeAvailable = True
                        # btnAvailable.click()
                        chrome_driver.execute_script("arguments[0].click();", btnAvailable)
                        break
                if bTimeAvailable == True:
                    break
                
                try:
                    btnNextPage = chrome_driver.find_element(By.XPATH, "//a[@class='page-link next']")
                    # hover = ActionChains(chrome_driver).move_to_element(btnNextPage)
                    # hover.perform()
                    # btnNextPage.click()
                    chrome_driver.execute_script("arguments[0].click();", btnNextPage)
                except NoSuchElementException as e:
                    break    
            else:
               break
        if bTimeAvailable == False:
            time.sleep(nCheckFrequency)
            
        input_quantity = WebDriverWait(chrome_driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='quantitytoadd form-control']")))
        input_quantity = chrome_driver.find_elements(By.XPATH, "//input[@class='quantitytoadd form-control']")[0]
        # input_quantity.send_keys(Keys.BACKSPACE)
        input_quantity.send_keys(nQuantity)
        btnAddCart = chrome_driver.find_element(By.XPATH, "//button[@class='btn btn-primary addtocart']")
        # btnAddCart.click()
        chrome_driver.execute_script("arguments[0].click();", btnAddCart)
        break
    else:
        time.sleep(60)

temp = input("Add to cart success. After check out, press any key to exit.\n")