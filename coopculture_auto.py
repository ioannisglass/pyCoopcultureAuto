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
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pyautogui
import random
user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible MSIE 9.0 Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.1 WOW64 Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.0 Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.1 Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 10.0 Windows NT 6.1 WOW64 Trident/6.0)',
    'Mozilla/5.0 (compatible MSIE 10.0 Windows NT 6.1 Trident/6.0)',
    'Mozilla/4.0 (compatible MSIE 8.0 Windows NT 5.1 Trident/4.0 .NET CLR 2.0.50727 .NET CLR 3.0.4506.2152 .NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (compatible U ABrowse 0.6 Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 OPR/36.0.2130.32',
    'Opera/9.80 (Windows NT 6.1 WOW64) Presto/2.12.388 Version/12.18',
    'Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Opera/9.80 (Windows NT 5.1 WOW64) Presto/2.12.388 Version/12.17'
]
def enter_proxy_auth(proxy_username, proxy_password):
    time.sleep(1)
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    pyautogui.press('enter')

pyautogui.FAILSAFE = False

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
        
        proxy_file = open("proxies.txt", "r")
        proxy_list = proxy_file.readlines()
        proxy_line = random.choice(proxy_list)
        proxy = proxy_line
        if proxy_line.find('\n') != -1:
            proxy = proxy_line[:proxy_line.find('\n')]
        proxy = proxy.strip()
        proxy_ip = proxy.split(":")[0]
        proxy_port = proxy.split(":")[1]
        # proxy_user = proxy.split(":")[2]
        # proxy_password = proxy.split(":")[3]
        proxy = Proxy()
        proxy.proxyType = ProxyType.MANUAL
        proxy.autodetect = False
        proxy_string = proxy_ip + ":" + proxy_port
        proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = proxy_string
        # proxy.socksPassword = proxy_password
        # proxy.socksUsername = proxy_user
        chrome_options.Proxy = proxy
        
        chrome_options.add_argument('--proxy-server={}'.format(proxy_string))
        user_agent = random.choice(user_agent_list)
        chrome_options.add_argument("--user-agent=" + user_agent)
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
        stealth(
            chrome_driver,
            user_agent=user_agent,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=False
        )
        chrome_driver.maximize_window()
        try:
            chrome_driver.get(strUrl)
        except Exception as ex:
            print(ex)
            continue
        
        # enter_proxy_auth(proxy_user, proxy_password)
        
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