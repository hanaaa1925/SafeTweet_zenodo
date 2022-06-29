from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.by import By


# 继承自unittest.TestCase


class testCase4(unittest.TestCase):
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

    def test_check(self):
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

        safe_content = "Good"
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(safe_content)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[1]/div[5]/img').click()
        time.sleep(10)
        alert1 = driver.switch_to.alert
        alertcontent1 = alert1.text
        alert1.accept()
        self.assertEqual("Safe!", alertcontent1, msg="fail")

        driver.find_element(By.ID, 'textcontent').clear()

        anon_content = "Bad boss"
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(anon_content)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[1]/div[5]/img').click()
        time.sleep(10)
        alert2 = driver.switch_to.alert
        alertcontent2 = alert2.text
        alert2.accept()
        self.assertEqual("You have sensitive message, please anonymous.", alertcontent2, msg="fail")

        driver.find_element(By.ID, 'textcontent').clear()

        en_content = "Bad boss David"
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(en_content)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[1]/div[5]/img').click()
        time.sleep(10)
        alert3 = driver.switch_to.alert
        alertcontent3 = alert3.text
        alert3.accept()
        self.assertEqual("You may leak 'name' information. Please encryption.", alertcontent3, msg="fail")

        driver.find_element(By.ID, 'textcontent').clear()

        en_content2 = "I earn $2000 every month"
        driver.find_element(By.ID, 'textcontent').click()
        driver.find_element(By.ID, 'textcontent').send_keys(en_content2)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[1]/div[5]/img').click()
        time.sleep(10)
        alert4 = driver.switch_to.alert
        alertcontent4 = alert4.text
        alert4.accept()
        self.assertEqual("You may leak 'money' information.  Please encryption.", alertcontent4, msg="fail")


    # 入口
    if __name__ == "__main__":
        unittest.main(verbosity=0)
