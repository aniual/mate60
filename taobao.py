import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Taobao:

    def __init__(self):
        self.options = self.set_options()
        self.driver = self.get_driver()

    def set_options(self):
        # 创建并配置Selenium选项
        options = Options()
        options.add_argument('--disable-gpu')  # 禁用GPU加速
        options.add_argument('--disable-client-side-phishing-detectio')  # 禁用客户端网络钓鱼检测
        # 最大化打开窗口
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        # enable-automation窗口不显示自动化测试操作
        # disable-popup-blocking'禁用弹出窗口阻止
        options.add_experimental_option("excludeSwitches",
                                        ['enable-automation', 'disable-popup-blocking'])
        # 保持窗口打开。
        options.add_experimental_option('detach', True)
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
        return options

    def get_driver(self):
        # 获取全局的driver
        driver = webdriver.Chrome(options=self.options)
        # 隐性等待最多10s，10秒不返回则报错，隐性适用于全局。
        driver.implicitly_wait(10)
        return driver

    def login_taobao(self):
        # 先进行登录处理。
        driver = self.driver
        driver.get("https://world.taobao.com")
        # 获取当前窗口句柄
        original_window = driver.current_window_handle
        webdriver_wait = WebDriverWait(driver, 10, 0.1)
        print(f'original_window: {original_window}')
        # 先查看点击登录按钮是否存在
        login_element = webdriver_wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'user-login-text')))
        if not login_element:
            print(f'未找到登录按钮')
            return
        # 点击登录按钮
        driver.find_element(By.CLASS_NAME, 'user-login-text').click()
        # 获取所有窗口的句柄列表
        all_window_handles = driver.window_handles
        print(f'all_window_handles: {all_window_handles}')
        # 切换到新窗口的句柄
        driver.switch_to.window(all_window_handles[-1])

        # 查看当前的页面窗口。
        now_window = driver.current_window_handle
        print(f'now_window: {now_window}')

        # 查看iframe窗口是否存在
        iframe_element = webdriver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'reg-iframe')))
        if not iframe_element:
            print('未找到iframe元素')
            return
        # 获取到iframe元素
        iframe = driver.find_element(By.CLASS_NAME, 'reg-iframe')
        # 跳转到ifame元素
        driver.switch_to.frame(iframe)
        # 点击扫码登录
        driver.find_element(By.CLASS_NAME, 'icon-qrcode').click()
        print('=========扫码登录成功============')
        self.driver = driver

    # def user_info(self):
    #     # 点击进入到用户的窗口。
    #     driver = self.driver
    #     webdriver_wait = WebDriverWait(driver, 10, 0.1)
    #     user_info_element = webdriver_wait.until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[4]/div[2]/div[1]/a[1]')))
    #     if not user_info_element:
    #         print('元素不存在')
    #         return
    #     driver.find_element(By.XPATH, '//*[@id="root"]/div[3]/div[4]/div[2]/div[1]/a[1]').click()
    #     # 获取所有窗口的句柄列表
    #     all_window_handles = driver.window_handles
    #     print(f'all_window_handles: {all_window_handles}')
    #     # 切换到新窗口的句柄
    #     driver.switch_to.window(all_window_handles[-1])
    #
    #     # 查看当前的页面窗口。
    #     now_window = driver.current_window_handle
    #     print(f'now_window: {now_window}')
    #     self.driver = driver

    def enter_cart(self):
        # 进入到购物车界面
        driver = self.driver
        webdriver_wait = WebDriverWait(driver, 10, 0.1)
        cart_element = webdriver_wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="J_MiniCart"]/div[1]/a')))
        if not cart_element:
            print('购物车没找到')
            return
        driver.find_element(By.XPATH, '//*[@id="J_MiniCart"]/div[1]/a').click()
        # 获取所有窗口的句柄列表
        all_window_handles = driver.window_handles
        print(f'enter_cart_all_window_handles: {all_window_handles}')
        # 切换到新窗口的句柄
        driver.switch_to.window(all_window_handles[-1])
        # 查看当前的页面窗口。
        now_window = driver.current_window_handle
        print(f'now_window: {now_window}')
        self.driver = driver

    def submit_cart(self):
        # 选择购物车
        driver = self.driver
        webdriver_wait = WebDriverWait(driver, 10, 0.1)
        # 获取所有窗口的句柄列表
        all_window_handles = driver.window_handles
        print(f'submit_cart_all_window_handles: {all_window_handles}')
        print('============选择商品============')
        try:
            webdriver_wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="J_SelectAll1"]')))
            time.sleep(0.05)
            driver.find_element(By.XPATH, '//*[@id="J_SelectAll1"]').click()
        except Exception:
            print(f'************没有找到全选按钮***************')
            return False

    def submit_order(self):
        # 结账
        driver = self.driver
        webdriver_wait = WebDriverWait(driver, 10, 0.1)
        print('=========点击结算===============')
        try:
            webdriver_wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="J_Go"]')))
            time.sleep(0.11)
            driver.find_element(By.XPATH, '//*[@id="J_Go"]').click()
        except:
            print('**********没有找到结算按钮***********')
            return False
        try:
            print(f'start_time========={datetime.now()}')
            WebDriverWait(driver, 20, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="submitOrderPC_1"]/div/a[2]')))
            time.sleep(0.01)
            driver.find_element(By.XPATH, '//*[@id="submitOrderPC_1"]/div/a[2]').click()
            check_bill = driver.find_element(By.XPATH, '//*[@id="submitOrderPC_1"]/div/a[2]').text
            while not check_bill:
                print('**********结算按钮没有出来等待处理***********')
                has_bill = driver.find_element(By.XPATH, '//*[@id="submitOrderPC_1"]/div/a[2]').text
                if has_bill:
                    driver.find_element(By.XPATH, '//*[@id="submitOrderPC_1"]/div/a[2]').click()
                    break
        except:
            print(f'**********没有找到付款按钮: {datetime.now()}***********')
            return False

    def main(self):
        self.login_taobao()
        # self.user_info()
        self.enter_cart()
        self.submit_cart()
        end_msctime = 1696471680000
        print(f'开始抢购时间为========={datetime.fromtimestamp(end_msctime / 1000)}')
        start_msctime = int(round(time.time() * 1000))
        while start_msctime < end_msctime:
            now_msctime = int(round(time.time() * 1000))
            print(f'现在的时间是=========={datetime.fromtimestamp(now_msctime / 1000)}')
            start_msctime = now_msctime
        self.submit_order()


if __name__ == '__main__':
    taobao = Taobao()
    taobao.main()
