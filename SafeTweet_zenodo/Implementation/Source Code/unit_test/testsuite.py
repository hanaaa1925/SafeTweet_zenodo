import unittest
import test1_login_update, test2_register, test3_post, test4_check, test5_thumb_up, test6_decrypt, test7_comment, test8_search


def createSuite():
    suite = unittest.TestSuite()

    # 1、addTest() 用法
    # 将测试用例加入到测试套件中
    # suite.addTest(test_login_update.testCase1("test_login"))
    # suite.addTest(test001.testCase1("test_baidu2"))
    # suite.addTest(test002.testCase2("test_baidu1"))
    # suite.addTest(test002.testCase2("test_baidu2"))
    # return suite

    # 2、TestLoder用法
    # suite1 = unittest.TestLoader.loadTestsFromTestCase(test001.testCase1)
    # suite2 = unittest.TestLoader.loadTestsFromTestCase(test002.testCase2)
    # suite = unittest.TestSuite([suite1,suite2])
    # return suite

    # 3、discover 用法
    discover = unittest.defaultTestLoader.discover('../unit_test',pattern='test*',top_level_dir=None)
    print(discover)
    return discover


if __name__ == "__main__":
    suite = createSuite()
    # 执行测试
    runner = unittest.TextTestRunner(verbosity=2)  # 是否显示执行结果详细信息
    runner.run(suite)
