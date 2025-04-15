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

# 清真Halal-廠商後台
# 更新公司資訊成功


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

# 登入'廠商'後台
@pytest.fixture(scope="function")
def login_manufactor(driver):
    driver.get('https://halal-dev.intersense.cloud/halal-manufactor')
    unified_number = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="account"]'))
    assert unified_number is not None, "找不到：unified_number"
    unified_number.send_keys('88888888')
    password = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/div[2]/div/input'))
    assert password is not None, "找不到：password"
    password.send_keys('Test1234')
    login = wait_for_element_clickable(driver, (By.XPATH, '//*[@id="root"]/div/div[2]/div/form/button'))
    assert login is not None, "找不到：login"
    login.click()
    WebDriverWait(driver, 10).until(EC.url_changes('https://halal-dev.intersense.cloud/halal-association/account-management/employee'))
    return driver

# 新增申請案件成功
def test_add_new_application_case_successfully(driver,login_manufactor):
    
    driver = login_manufactor
    # 確保載入'我的案件'頁面
    WebDriverWait(driver, 10).until(EC.url_to_be("https://halal-dev.intersense.cloud/halal-manufactor/case-management"))
    time.sleep(1)

    # 我的案件頁面-新增申請案件
    add_case = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"新增申請案件")]'))
    assert add_case is not None, "找不到：add_case"
    add_case.click()
    # 選擇'飲料食品'類別
    drink_and_food = wait_for_element_clickable(driver, (By.XPATH, '//div[@class="radio-button_container__ZHR0B"]//div[1]'))
    assert drink_and_food is not None, "找不到：drink_and_food"
    drink_and_food.click()
    time.sleep(0.5)
    check_button = wait_for_element_clickable(driver, (By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button'))
    assert check_button is not None, "找不到：check_button"
    check_button.click()
    time.sleep(0.5)
    check_alert = wait_for_element_clickable(driver, (By.XPATH, '/html/body/div[3]/div/div[6]/button[1]'))
    assert check_alert is not None, "找不到：check_alert"
    check_alert.click()

    # 基本資料tag
    # 滾動頁面至底部-填入聯絡人資訊
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(0.5)

    # 填入聯絡人資訊
    name = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='name']"))
    assert name is not None, "找不到：name"
    name.send_keys('harry',random_name)
    companyTel = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='companyTel']"))
    assert companyTel is not None, "找不到：companyTel"
    companyTel.send_keys('(02)22223333')
    extensionNumber = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='extensionNumber']"))
    assert extensionNumber is not None, "找不到：extensionNumber"
    extensionNumber.send_keys('1234')
    phone = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='phone']"))
    assert phone is not None, "找不到：phone"
    phone.send_keys('0987654321')
    email = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='email']"))
    assert email is not None, "找不到：email"
    email.send_keys('harry@intersense.com.tw')
    saleCountries = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='saleCountries']"))
    assert saleCountries is not None, "找不到：saleCountries"
    saleCountries.send_keys('台灣')
    # 下一步
    next_step = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'下一步')]"))
    assert next_step is not None, "找不到：next_step"
    next_step.click()
    time.sleep(1)

    # 工廠資訊tag
    # 工廠資訊-新增工廠
    for i in range(1):  # 新增 3 筆工廠
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        factory_no = f'{current_time}{i:02d}'
        factory_name = f'櫻特森工廠_{current_time}_{i}'
        # 工廠資訊tag
        add_factory = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"新增工廠")]'))
        assert add_factory is not None, "找不到：add_factory"
        add_factory.click()
        factoryNo = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='factoryNo']"))
        assert factoryNo is not None, "找不到：factoryNo"
        factoryNo.send_keys(factory_no)
        factoryName = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='factoryName']"))
        assert factoryName is not None, "找不到：factoryName"
        factoryName.send_keys(factory_name)
        factoryAddress = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='factoryAddress']"))
        assert factoryAddress is not None, "找不到：factoryAddress"
        factoryAddress.send_keys('台北市大安區仁愛路四段123號')
        factoryTel = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='factoryTel']"))
        assert factoryTel is not None, "找不到：factoryTel"
        factoryTel.send_keys('(02)12345678')
        factoryURL = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='factoryWebsite']"))
        assert factoryURL is not None, "找不到：factoryURL"
        factoryURL.send_keys('https://www.intersense.com.tw')
        # 代工廠
        foundry_checkbox = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='foundry']"))
        assert foundry_checkbox is not None, "找不到：foundry_checkbox"
        foundry_checkbox.click()
        # 生產設備
        production_equipment = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='equipment']"))
        assert production_equipment is not None, "找不到：production_equipment"
        production_equipment.click()
        attachment_description = wait_for_element_clickable(driver, (By.XPATH, "//textarea[@id='equipmentDescription']"))
        assert attachment_description is not None, "找不到：attachment_description"
        attachment_description.send_keys('「製程選擇」（Process Selection）是指決定商品或服務系統化生產的方式...')

        # 滾動頁面至底部
        def scroll_down(driver, pixels=500):
            driver.execute_script(f"window.scrollBy(0, {pixels});")
        scroll_down(driver, pixels=1600)
        time.sleep(0.5)

        shipping_method = wait_for_element_clickable(driver, (By.XPATH, "//textarea[@id='transportation']"))
        assert shipping_method is not None, "找不到：shipping_method"
        shipping_method.send_keys('中轉倉是從進來的卡車上卸下物料...')
        def upload_file(filetype_text, file_path):
            driver.find_element(By.CLASS_NAME, "css-dk3iff-control").click()
            time.sleep(0.5)
            for el in driver.find_elements(By.XPATH, f"//div[text()='{filetype_text}']"):
                if el.is_displayed():
                    el.click()
                    break
            upload_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'attachments'))
            )
            upload_input.send_keys(file_path)
            file_type_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[text()='{filetype_text}']"))
            )
            assert file_type_text.text == filetype_text, f"列表中找不到『{filetype_text}』"
        # 上傳五個文件
        upload_file('產品製程圖', 'assets/test.pdf')
        upload_file('工廠登記核准相關文件', 'assets/dog1.jpg')
        upload_file('工廠平面配置圖', 'assets/dog2.jpg')
        upload_file('生產設備 清潔/消毒 之作業 方式/程序(含清潔劑、消毒劑)', 'assets/dog3.jpg')
        upload_file('其它(檔名請清楚描述檔案用途)', 'assets/dog4.jpg')
        add_button = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/div[2]/button"))
        assert add_button is not None, "找不到：add_button"
        add_button.click()
        time.sleep(0.5)

        # 滾動頁面至頂部
        def scroll_to_top(driver):
            driver.execute_script("window.scrollTo(0, 0);")
        scroll_to_top(driver)
        time.sleep(0.5)


    # 滾動頁面至底部
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(0.5)

    next_step = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'下一步')]"))
    assert next_step is not None, "找不到：next_step"
    next_step.click()
    time.sleep(1)

    # 滾動頁面至頂部
    def scroll_to_top(driver):
        driver.execute_script("window.scrollTo(0, 0);")
    scroll_to_top(driver)
    time.sleep(0.5)


    # 申請產品tag
    # 產品分類清單-新增分類
    category_names = []
    for i in range(3):
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        name_cn = f'{current_time}_CN_{i}'
        name_en = f'{current_time}_EN_{i}'

        category_names.append(name_cn)

        add_category = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'新增分類')]"))
        assert add_category is not None, "找不到：add_category"
        add_category.click()
        categoryCN = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='productTypeName']"))
        assert categoryCN is not None, "找不到：categoryCN"
        categoryCN.send_keys(name_cn)
        categoryEN = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='productTypeNameEn']"))
        assert categoryEN is not None, "找不到：categoryEN"
        categoryEN.send_keys(name_en)
        add_button = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/button"))
        assert add_button is not None, "找不到：add_button"
        add_button.click()

    # 滾動頁面至底部
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(0.5)

    # 申請產品清單-新增產品
    # 產品分類清單-新增分類-使用迴圈新增3筆
    for i in range(3): 
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        name_cn = f'產品名稱中文_{current_time}_{i}'
        name_en = f'product_name_en_{current_time}_{i}'
        category_to_select = category_names[i]  # <-- 用對應的分類名稱

        add_product = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'新增產品')]"))
        assert add_product is not None, "找不到：add_product"
        add_product.click()
        nameCN = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='productName']"))
        assert nameCN is not None, "找不到：nameCN"
        nameCN.send_keys(name_cn)
        nameEN = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='productNameEn']"))
        assert nameEN is not None, "找不到：nameEN"
        nameEN.send_keys(name_en)
        productType = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div"))
        assert productType is not None, "找不到：productType"
        productType.click()
        time.sleep(0.5)
        for el in driver.find_elements(By.XPATH, f"//div[text()='{category_to_select}']"):
            if el.is_displayed():
                el.click()
                break
        
        # 含藥化妝品核取方塊
        medicated_cosmetics_checkbox = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='isContainsCosmetic']"))
        assert medicated_cosmetics_checkbox is not None, "找不到：medicated_cosmetics_checkbox"
        medicated_cosmetics_checkbox.click()
        # 衛生署許可證-上傳檔案(PDF)
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'healthLicense'))
        )
        upload_input.send_keys('assets/test.pdf')
        # 驗證顯示'檢視檔案'
        file_link = wait_for_element_clickable(driver, (By.XPATH, "//a[contains(text(),'檢視檔案')]"))
        assert "檢視檔案" in file_link.text, "欄位文字顯示錯誤，應為『檢視檔案』"

        # 工廠名稱下拉式選單 - 展開下拉
        factory_dropdown = wait_for_element_clickable(driver, (
            By.XPATH, "//div[contains(@class,'css-dk3iff-control')]//div[contains(text(),'請選擇工廠')]"
        ))
        assert factory_dropdown is not None, "找不到：factory_dropdown"
        factory_dropdown.click()
        time.sleep(0.5)
        # 選擇特定工廠名稱，例如『櫻特森工廠』
        factory_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'-option')]"))
        )
        assert len(factory_options) > 0, "找不到任何下拉選項"
        factory_options[0].click()

        # 製程圖
        # 製程圖下拉選單 - 展開下拉
        process_drawing_dropdown = wait_for_element_clickable(driver, (
            By.XPATH, "//div[contains(@class,'css-dk3iff-control')]//div[contains(text(),'請選擇製程圖')]"
        ))
        assert process_drawing_dropdown is not None, "找不到：process_drawing_dropdown"
        process_drawing_dropdown.click()
        time.sleep(0.5)

        # 點選下拉選單中的第一個選項
        process_drawing_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'-option')]"))
        )
        assert len(process_drawing_options) > 0, "找不到任何製程圖選項"
        process_drawing_options[0].click()

        bind_picture = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'綁定圖片')]"))
        assert bind_picture is not None, "找不到：bind_picture"
        bind_picture.click()

        # 等待表格中的文字出現
        factory_text_cell = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'product-modal_table')]//td[contains(text(),'櫻特森')]"))
        )
        assert "櫻特森工廠" in factory_text_cell.text, "表格內找不到『櫻特森工廠』字樣"


        # 中文規格
        packageSpec_CN = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='packageSpec']"))
        assert packageSpec_CN is not None, "找不到：packageSpec_CN"
        packageSpec_CN.send_keys('產品規格中文')

        # 英文規格
        packageSpec_EN = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='packageSpecEn']"))
        assert packageSpec_EN is not None, "找不到：packageSpec_EN"
        packageSpec_EN.send_keys('Product specification in English')

        # 等待並定位到隱藏的 file input 元素
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//label[normalize-space(text())='規格圖片']/following-sibling::div//input[@type='file']"
            ))
        )
        upload_input.send_keys("assets/dog1.jpg")


        # 等待表格中的「產品規格中文」出現
        # spec_text_cell = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'product-modal_table')]//th[contains(text(),'產品規格中文')]"))
        # )
        # assert "產品規格中文" in spec_text_cell.text, "表格內找不到『產品規格中文』字樣"


        # 選擇原料
        select_raw_material = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div[2]/div[4]/div[1]/div/button"))
        assert select_raw_material is not None, "找不到：select_raw_material"
        select_raw_material.click()
        # 新增原料
        add_raw_material = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[1]/div/button"))
        assert add_raw_material is not None, "找不到：add_raw_material"
        add_raw_material.click()
        time.sleep(1)


        name_cn = f'原料中文_{i}'
        name_en = f'raw_en_{i}'
        nickname_val = f'nickname_{i}'
        manufacturer_val = f'製造商_{i}'
        origin_val = f'產地_{i}'
        supplier_val = f'供應商_{i}'

        # 輸入欄位資料
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='name']")).send_keys(name_cn)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='nameEn']")).send_keys(name_en)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='nickName']")).send_keys(nickname_val)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='manufacturer']")).send_keys(manufacturer_val)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='origin']")).send_keys(origin_val)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='supplier']")).send_keys(supplier_val)
        # 滾動並點擊「新增」按鈕
        add_btn_target = driver.find_element(By.XPATH, "//*[@id='target-element']/div[3]/div[2]/button")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", add_btn_target)
        time.sleep(1)
        add_button = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='target-element']/div[3]/div[2]/button"))
        assert add_button is not None, "找不到：add_button"
        add_button.click()
        # 點擊「確定」Alert
        check_alert = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"確定")]'))
        assert check_alert is not None, "找不到：check_alert"
        check_alert.click()
        time.sleep(0.5)
        # 滾動回「新增原料」按鈕（準備選取）
        select_raw_material_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div[1]/div/button")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", select_raw_material_button)

        # 勾選核取方塊（index從1開始）
        checkbox_xpath = f"(//input[@id='select'])[{i+1}]"
        select_raw_material = wait_for_element_clickable(driver, (By.XPATH, checkbox_xpath))
        assert select_raw_material is not None, f"找不到：select_raw_material 第{i+1}項"
        select_raw_material.click()
        # 點選「選取」按鈕
        select_btn_target = driver.find_element(By.XPATH, "//button[contains(text(),'選取')]")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", select_btn_target)
        time.sleep(1)
        select_button = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'選取')]"))
        assert select_button is not None, "找不到：select_button"
        select_button.click()
        time.sleep(1)  # 等下一輪開窗完成


        add_button = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div[2]/div[5]/div[2]/button"))
        assert add_button is not None, "找不到：add_button"
        add_button.click()
        check_alert = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"確定")]'))
        assert check_alert is not None, "找不到：check_alert"
        check_alert.click()
        time.sleep(1)  # 稍微等待避免時間太近

    next_step = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'下一步')]"))
    assert next_step is not None, "找不到：next_step"
    next_step.click()
    time.sleep(1)

    # 不申請產品tag
    # 不申請產品清單-新增產品
    for i in range(3):  # 新增 3 筆產品
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        name_cn = f'產品名稱中文_{timestamp}_{i}'
        name_en = f'product_name_en_{timestamp}_{i}'
        add_product = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='root']/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/button"))
        assert add_product is not None, "找不到：add_product"
        add_product.click()
        nameCN = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='productName']"))
        assert nameCN is not None, "找不到：nameCN"
        nameCN.send_keys(name_cn)
        nameEN = wait_for_element_clickable(driver, (By.XPATH, "//input[@id='productNameEn']"))
        assert nameEN is not None, "找不到：nameEN"
        nameEN.send_keys(name_en)
        # 共線核取方塊
        collinear_checkbox = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='usingSameLine']"))
        assert collinear_checkbox is not None, "找不到：collinear_checkbox"
        collinear_checkbox.click()
        add_button = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/div[2]/button"))
        assert add_button is not None, "找不到：add_button"
        add_button.click()
        time.sleep(0.5)
        check_alert = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"確定")]'))
        assert check_alert is not None, "找不到：check_alert"
        check_alert.click()
        time.sleep(1)  # 等待彈窗處理完畢再進下一輪

    # 滾動頁面至底部
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(1)

    next_step = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'下一步')]"))
    assert next_step is not None, "找不到：next_step"
    next_step.click()
    time.sleep(1)


    # 原料資訊tag
    # 滾動頁面至頂部
    def scroll_to_top(driver):
        driver.execute_script("window.scrollTo(0, 0);")
    scroll_to_top(driver)
    time.sleep(0.5)

    # 新增原料
    for i in range(1):
        name_cn = f'edit_{i}'
        name_en = f'edit_{i}'
        nickname_val = f'edit_{i}'
        manufacturer_val = f'edit_{i}'
        origin_val = f'edit_{i}'
        supplier_val = f'edit_{i}'
        # 點擊新增原料（第一層）
        add_raw_material = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='root']/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/button"))
        assert add_raw_material is not None, "找不到：add_raw_material"
        add_raw_material.click()
        time.sleep(1)
        # 點擊新增原料（第二層彈窗內）
        add_raw_material2 = wait_for_element_clickable(driver, (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/button"))
        assert add_raw_material2 is not None, "找不到：add_raw_material2"
        add_raw_material2.click()
        time.sleep(1)
        # 輸入欄位資料
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='name']")).send_keys(name_cn)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='nameEn']")).send_keys(name_en)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='nickName']")).send_keys(nickname_val)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='manufacturer']")).send_keys(manufacturer_val)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='origin']")).send_keys(origin_val)
        wait_for_element_clickable(driver, (By.XPATH, "//input[@id='supplier']")).send_keys(supplier_val)
        # 滾動並點擊「新增」按鈕
        add_btn_target = driver.find_element(By.XPATH, "//*[@id='target-element']/div[3]/div[2]/button")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", add_btn_target)
        time.sleep(1)
        add_button = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='target-element']/div[3]/div[2]/button"))
        assert add_button is not None, "找不到：add_button"
        add_button.click()
        # 點擊「確定」Alert
        check_alert = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"確定")]'))
        assert check_alert is not None, "找不到：check_alert"
        check_alert.click()
        time.sleep(0.5)
        # 滾動回「新增原料」按鈕（準備選取）
        select_raw_material_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div/button")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", select_raw_material_button)
        time.sleep(1)
        # 勾選核取方塊（index從1開始）
        checkbox_xpath = f"(//input[@id='select'])[{i+4}]"
        select_raw_material = wait_for_element_clickable(driver, (By.XPATH, checkbox_xpath))
        assert select_raw_material is not None, f"找不到：select_raw_material 第{i+4}項"
        select_raw_material.click()
        # 點選「選取」按鈕
        select_btn_target = driver.find_element(By.XPATH, "//button[contains(text(),'選取')]")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", select_btn_target)
        time.sleep(1)
        select_button = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'選取')]"))
        assert select_button is not None, "找不到：select_button"
        select_button.click()
        time.sleep(1)  # 等下一輪開窗完成

    # 滾動頁面至底部
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(1.5)
    next_step = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'下一步')]"))
    assert next_step is not None, "找不到：next_step"
    next_step.click()
    time.sleep(1)
    
    # 其他附件tag
    for i in range(3):  # 要上傳 3 筆檔案
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_desc = f'test_file_{timestamp}_{i}'
        file_path = f'assets/dog{i+1}.jpg'  # dog1.jpg ~ dog3.jpg
        # 輸入檔案說明
        file_name = wait_for_element_clickable(driver, (By.XPATH, "//input[@placeholder='請輸入檔案說明']"))
        assert file_name is not None, "找不到：file_name"
        file_name.clear()  # 清除舊內容（以防 UI 沒自動清掉）
        file_name.send_keys(file_desc)
        # 上傳檔案
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.input_container__KIk1u input[type="file"]'))
        )
        upload_input.send_keys(file_path)
        time.sleep(1)  # 給點時間讓檔案上傳完成
    # 滾動頁面至底部
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(0.5)
    next_step = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'下一步')]"))
    assert next_step is not None, "找不到：next_step"
    next_step.click()
    time.sleep(1)
    
    # 文審費tag
    # 滾動頁面至底部
    def scroll_down(driver, pixels=500):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, pixels=1600)
    time.sleep(0.5)
    # 付款帳號末五碼
    account_number = wait_for_element_clickable(driver, (By.XPATH, "//*[@id='paidCode']"))
    assert account_number is not None, "找不到：account_number"
    account_number.send_keys('12345')
    # 付款日期
    # 點開日期選擇器
    payment_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='請選擇日期']"))
    )
    payment_input.click()
    # 點選「今天」的日期（根據特殊 class）
    today_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".react-datepicker__day--today"))
    )
    today_btn.click()
    # 匯款單據-上傳檔案
    upload_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "paidFile"))
    )
    upload_input.send_keys("assets/dog1.jpg")
    # # 彈窗確認
    check_alert = wait_for_element_clickable(driver, (By.XPATH, '//button[contains(text(),"確定")]'))
    assert check_alert is not None, "找不到：check_alert"
    check_alert.click()
    # # 送出申請
    send_application = wait_for_element_clickable(driver, (By.XPATH, "//button[contains(text(),'送出申請')]"))
    assert send_application is not None, "找不到：send_application"
    send_application.click()
    # # 審核提醒彈窗-確認送出
    send_check = wait_for_element_clickable(driver, (By.XPATH, '/html/body/div[2]/div/div[6]/button[1]'))
    assert send_check is not None, "找不到：send_check"
    send_check.click()
    # # 強制等待避免彈窗太快關閉
    time.sleep(3)
    # # 等待 h2 標題出現並驗證文字為申請成功
    swal_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "swal2-title"))
    )
    assert swal_title.text.strip() == "申請成功", f"彈窗標題錯誤，實際為: {swal_title.text}"
    print("#測試案例 協會送出訂單成功")
