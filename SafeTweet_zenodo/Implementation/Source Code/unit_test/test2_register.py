from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.by import By


# 继承自unittest.TestCase


class testCase2(unittest.TestCase):
    # 测试固件 (默认运行)
    def setUp(self):  # self为类的实例
        self.driver = webdriver.Chrome('./chromedriver')
        self.url = "http://localhost:8080/"
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(1)

    # 测试固件
    def tearDown(self):
        self.driver.quit()

    def test_register(self):
        email = 'o@o.com'
        name = 'o'
        password = 'o'
        company = 'o'

        driver = self.driver
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/a[2]').click()
        driver.find_element(By.XPATH, '//*[@id="input-1"]').click()
        driver.find_element(By.ID, 'input-1').send_keys(email)
        driver.find_element(By.ID, 'input-2').click()
        driver.find_element(By.ID, 'input-2').send_keys(name)
        driver.find_element(By.ID, 'input-3').click()
        driver.find_element(By.ID, 'input-3').send_keys(password)
        driver.find_element(By.ID, 'input-4').click()
        driver.find_element(By.ID, 'input-4').send_keys(company)
        time.sleep(1)
        driver.find_element(By.ID, 'input-5').click()
        time.sleep(1)

        login = driver.find_element(By.XPATH, '//*[@id="login"]').text

        self.assertEqual("Login", login, msg="fail")




    # 入口
    if __name__ == "__main__":
        unittest.main(verbosity=0)
