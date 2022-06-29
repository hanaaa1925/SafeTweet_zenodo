from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.by import By
import pybase64


# 继承自unittest.TestCase


class testCase3(unittest.TestCase):
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

    def test_post(self):
        email = "q@q.com"
        password = "q"
        driver = self.driver
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div[1]/a[1]/strong').click()
        driver.find_element(By.ID, 'input-2').click()
        driver.find_element(By.ID, 'input-2').send_keys(email)
        driver.find_element(By.ID, 'input-3').click()
        driver.find_element(By.ID, 'input-3').send_keys(password)
        driver.find_element(By.ID, 'submit').click()
        time.sleep(1)
        logout = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div[1]/a[1]').text

        self.assertEqual("Logout", logout, msg="fail")

        content = "Good"
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(content)
        time.sleep(1)
        driver.find_element(By.ID, 'post').click()
        time.sleep(3)

        first = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[1]/p').text
        self.assertEqual(content, first, msg="fail")

        content_anony = "anonymous"
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(content_anony)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[1]/div[2]/img').click()
        time.sleep(1)
        driver.find_element(By.ID, 'post').click()
        time.sleep(3)


        content_en = "encrypt"
        content_base64 = pybase64.b64encode(content_en.encode())
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(content_en)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[1]/div[4]/img').click()
        time.sleep(1)
        driver.find_element(By.ID, 'post').click()
        time.sleep(3)

        first_en = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[1]/p').text
        self.assertEqual(content_base64, first_en, msg="fail")


    # 入口
    if __name__ == "__main__":
        unittest.main(verbosity=0)
