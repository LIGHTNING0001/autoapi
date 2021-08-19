
from autoapi import *


class TestAutoAPI():

    def test_get_cookie(self):
        url = 'http://192.168.0.108:8080/woniusales/user/login'
        data = {'username': 'admin', 'password': 'admin123', 'verifycode': '000'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = get_cookie(url, headers, data)
        print(resp)

    def test_read_excel(self):
        file = '接口测试用例.xls'
        result = read_excel(file)
        assert 1 == len(result)


    # def test_woniusales(self):
    #
    #     execute_api(file='接口测试用例.xls',
    #                 cookies=get_cookie(url, headers, data),
    #                 index_table=0,
    #                 start=2,
    #                 stop=3)


# if __name__ == '__main__':
#     execute_api(file='接口测试用例.xls',
#                 cookies=get_cookie(url, headers, data),
#                 index_table=0,
#                 start=2,
#                 stop=5)
