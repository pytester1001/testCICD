from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pytest , time , os , random

# 清真Halal-協會後台
# 測試案例1-1 協會用戶登入/登出成功

# 設置 Browser 環境
@pytest.fixture
def driver(scope="function"):

    # 設置遠端Selenium Server環境
    driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=webdriver.ChromeOptions()
    )

    # 設置 Chrome 環境
    # options = ChromeOptions()
    # service = ChromeService("/usr/local/bin/chromedriver")
    # driver = webdriver.Chrome(service=service, options=options)

    # 設置 Firefox 環境
    # options = FirefoxOptions()
    # options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
    # service = FirefoxService("/usr/local/bin/geckodriver")
    # driver = webdriver.Firefox(service=service, options=options)

    # 設置 Safari 環境
    # driver = webdriver.Safari()
    # driver.set_window_rect(0, 0, 1200, 800)

    # 無頭測試
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")

    yield driver
    driver.quit()

# 設置元素等待條件
def wait_for_element_clickable(driver, locator, timeout=10, screenshot_name="screenshot"):
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.element_to_be_clickable(locator))
        return element
    except TimeoutException:
        capture_screenshot(driver, screenshot_name)
        return None

# 設置截圖路徑/名稱
def capture_screenshot(driver, filename="screenshot.png"):
    directory = '/Users/harry/Desktop/Project/halal/screenshots'
    if not os.path.exists(directory):
        os.makedirs(directory)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filepath = os.path.join(directory, f"{filename}_{timestamp}.png")
    driver.save_screenshot(filepath)

# 獲取當前時間
current_datetime1 = datetime.now().strftime('%Y%m%d%H%M%S')
random_name = f'{current_datetime1}'

# 登入'協會'後台
@pytest.fixture(scope="function")
def login_association(driver):
    driver.get('https://halal-dev.intersense.cloud/halal-association')
    account = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/div[1]/div/input'))
    assert account is not None, "找不到：account"
    account.send_keys('admin@test.com')
    password = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/div[2]/div/input'))
    assert password is not None, "找不到：password"
    password.send_keys('Test1234')
    login = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/button'))
    assert login is not None, "找不到：login"
    login.click()
    WebDriverWait(driver, 10).until(EC.url_changes('https://halal-dev.intersense.cloud/halal-association/account-management/employee'))
    return driver

# 測試案例1-1 協會用戶登入/登出成功
def test_user_association_login_and_logout_successfully(driver):

    # 驗證登入
    driver.get('https://halal-dev.intersense.cloud/halal-association')
    account = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/div[1]/div/input'))
    assert account is not None, "找不到：account"
    account.send_keys('admin@test.com')
    password = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/div[2]/div/input'))
    assert password is not None, "找不到：password"
    password.send_keys('Test1234')
    login = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/button'))
    assert login is not None, "找不到：login"
    login.click()
    time.sleep(1)
    # 預期網址
    expected_url = "https://halal-dev.intersense.cloud/halal-association/account-management/employee"
    # 驗證當前網址
    assert driver.current_url == expected_url, f"登入後跳轉網址異常 ,預期: {expected_url}，實際: {driver.current_url}"
    print('#測試案例1-1 協會用戶登入成功')

    # 驗證登出
    logout = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/header/div/div'))
    assert logout is not None, "找不到：logout"
    logout.click()
    time.sleep(1)
    # 預期網址
    expected_url = "https://halal-dev.intersense.cloud/halal-association"
    # 驗證當前網址
    assert driver.current_url == expected_url, f"登入後跳轉網址異常 ,預期: {expected_url}，實際: {driver.current_url}"
    print('#測試案例1-1 協會用戶登出成功')
