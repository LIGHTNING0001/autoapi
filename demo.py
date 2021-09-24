
from apiauto import execute_apis, get_cookie

url = 'http://192.168.13.41:8080/woniusales/user/login'
data = {'username': 'admin', 'password': 'admin123', 'verifycode': '000'}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}


execute_apis('接口测试用例.xls', cookies=get_cookie(url, data, headers))