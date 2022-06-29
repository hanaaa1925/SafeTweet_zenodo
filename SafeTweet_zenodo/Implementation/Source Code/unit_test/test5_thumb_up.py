from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.by import By


# 继承自unittest.TestCase


class testCase5(unittest.TestCase):
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

    def test_thumb_up(self):
        email = "w@w.com"
        password = "w"
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

        number_before = driver.find_element(By.XPATH,
                                            '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[2]/div[1]/span').text
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[2]/div[1]/img').click()
        time.sleep(2)
        number_after = driver.find_element(By.XPATH,
                                            '//*[@id="app"]/div/div[2]/div/div/ul[2]/li[1]/div[2]/div[1]/span').text
        self.assertEqual(int(number_before)+1, int(number_after), msg="fail")


    # 入口
    if __name__ == "__main__":
        unittest.main(verbosity=0)
