import sys

import requests

import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Taobao:
    # 开始抢购时间
    # rush_buying_time = 1696555680000
    rush_buying_time = 1696558080000

    def __init__(self):
        self.options = self.set_options()
        self.driver = self.get_driver()

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
        # 隐性等待最多60s，60秒不返回则报错，隐性适用于全局。
        driver.implicitly_wait(60)
        return driver

    def login_taobao(self):
        print(f'开始时间: ========={datetime.now()}')
        # 先进行登录处理。
        driver = self.driver
        driver.get("https://world.taobao.com")
        # 获取当前窗口句柄
        original_window = driver.current_window_handle
        webdriver_wait = WebDriverWait(driver, 20, 0.1)
        print(f'----------original_window: {original_window}')
        # 先查看点击登录按钮是否存在
        try:
            login_button = webdriver_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'user-login-button')))
            login_button.click()
        except Exception:
            print('========未找到登录按钮========')
            driver.quit()
        # 获取所有窗口的句柄列表
        all_window_handles = driver.window_handles
        print(f'----------login_all_window_handles: {all_window_handles}')
        # 切换到新窗口的句柄
        driver.switch_to.window(all_window_handles[-1])

        # 查看当前的页面窗口。
        now_window = driver.current_window_handle
        print(f'----------login_active_window: {now_window}')

        # 查看iframe窗口是否存在存在则进行切换
        try:
            webdriver_wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, 'reg-iframe')))
        except Exception:
            print('========未找到iframe页面========')
            driver.quit()
        # 点击扫码登录
        try:
            qrcode_element = webdriver_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'icon-qrcode')))
            qrcode_element.click()
            self.driver = driver
            print('=========扫码登录成功============')
            print(f'login_taobao耗费时间: ========={datetime.now()}')
        except Exception:
            print('========未找到登录按钮============')
            driver.quit()

    def enter_cart(self):
        # 进入到购物车界面
        driver = self.driver
        webdriver_wait = WebDriverWait(driver, 20, 0.1)
        # 点击购物车
        try:
            cart_element = webdriver_wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="J_MiniCart"]/div[1]/a')))
            cart_element.click()
        except Exception:
            print('========未找到登录按钮============')
            driver.quit()

        # 获取所有窗口的句柄列表
        all_window_handles = driver.window_handles
        print(f'----------cart_all_window_handles: {all_window_handles}')
        # 切换到新窗口的句柄
        driver.switch_to.window(all_window_handles[-1])
        # 查看当前的页面窗口。
        now_window = driver.current_window_handle
        print(f'----------cart_active_window: {now_window}')
        self.driver = driver
        print(f'enter_cart耗费时间: ========={datetime.now()}')

    def submit_cart(self):
        # 选择购物车
        driver = self.driver
        webdriver_wait = WebDriverWait(driver, 20, 0.1)
        # 获取所有窗口的句柄列表
        print('============选择商品============')
        try:
            checkbox_element = webdriver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_SelectAll1"]')))
            checkbox_element.click()
        except Exception:
            print(f'========未选中商品============')
            driver.quit()

    def get_taobao_time(self):
        # 获取淘宝的时间
        r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                          headers={
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
        x = eval(r1.text)
        timeNum = int(x['data']['t'])
        return timeNum

    def submit_order(self):
        taobao_time = self.get_taobao_time()
        # 结账方法。
        while True:
            print(f'现在的时间为: =========={datetime.fromtimestamp(taobao_time / 1000)}')
            if taobao_time > self.rush_buying_time:
                print(f'淘宝秒杀时间为: =========={datetime.fromtimestamp(self.get_taobao_time() / 1000)}')
                driver = self.driver
                # 点击结算按钮
                try:
                    while True:
                        settlement = driver.find_element(By.LINK_TEXT, "结 算")
                        if settlement:
                            print(f'点击提交: ========={datetime.fromtimestamp(self.get_taobao_time() / 1000)}')
                            settlement.click()
                            print(f'已提交: ========={datetime.fromtimestamp(self.get_taobao_time() / 1000)}')
                            break
                except Exception:
                    print(f'========结算按钮未显示============')
                    driver.quit()
                    break

                # 点击结账按钮。
                try:
                    while True:
                        submit_order = driver.find_element(By.LINK_TEXT, "提交订单")
                        if submit_order:
                            print(f'开始结账: ========={datetime.fromtimestamp(self.get_taobao_time() / 1000)}')
                            submit_order.click()
                            print(f'已结账: ========={datetime.fromtimestamp(self.get_taobao_time() / 1000)}')
                            print(f'结账电脑系统时间为: =========={datetime.now()}')
                        break
                    driver.quit()
                    break
                except Exception:
                    print(f'========抢购失败============')
                    driver.quit()
                    break

            taobao_time = self.get_taobao_time()

    def main(self):
        # self.user_info()
        self.login_taobao()
        self.enter_cart()
        self.submit_cart()
        self.submit_order()


if __name__ == '__main__':
    taobao = Taobao()
    taobao.main()
