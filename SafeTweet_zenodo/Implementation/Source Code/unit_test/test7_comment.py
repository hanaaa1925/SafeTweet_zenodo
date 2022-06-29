from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.by import By


# 继承自unittest.TestCase


class testCase7(unittest.TestCase):
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

    def test_comment(self):
        email = "q@q.com"
        password = "q"
        driver = self.driver
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div[1]/a[1]/strong').click()
        driver.find_element(By.ID, 'input-2').click()
        driver.find_element(By.ID, 'input-2').send_keys(email)
        driver.find_element(By.ID, 'input-3').click()
        driver.find_element(By.ID, 'input-3').send_keys(password)
        driver.find_element(By.ID, 'submit').click()
        time.sleep(3)
        logout = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div[1]/a[1]').text

        self.assertEqual("Logout", logout, msg="fail")

        comment = "Wonderful!"
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[2]/div[2]/img').click()
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[3]/div/form/div[1]/textarea').click()
        time.sleep(1)
        driver.find_element(By.XPATH,
                            '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[3]/div/form/div[1]/textarea').send_keys(comment)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[3]/div/form/div[2]/button').click()
        time.sleep(1)
        firstcomment = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[3]/div/ul/li/div/p/span').text

        self.assertEqual(comment, firstcomment, msg="fail")



    # 入口
    if __name__ == "__main__":
        unittest.main(verbosity=0)
