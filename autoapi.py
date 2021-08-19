# -*- encoding: utf-8 -*-

__author__ = 'lishanjie'

import json
import xlrd
import requests


def get_cookie(url, headers, data):
    """
    获取cookie
    :param url: 接口地址
    :param headers: 请求头部信息
    :param data: 根据具体登录接口 构造 data 参数， 以字典方式保存
    :return: 返回cookie
    """
    try:
        resp = requests.post(url=url, data=data, headers=headers)
        return resp.cookies
    except requests.exceptions.RequestException as e:
        print('获取 cookie 失败')


def read_excel(file):
    """
    读取Excel表 获取工作表
    :param file: 文件对象
    :return: 包含工作表的列表
    """
    try:
        xl = xlrd.open_workbook(file)
        tables = xl.sheets()
        return tables
    except Exception as e:
        print('Error: ', e)
        print(f'读取{file}', file)


def get_testcases(tables):
    """
    获取全部测试用例数据
    :param tables: 包含工作表的列表
    :return: 测试用例列表
    """
    res = []
    for table in tables:
        for i in range(1, table.nrows):     # 从表的第一个测试用例开始获取
            tmp = []
            '''
            tmp[1] : 测试用例的编号
            tmp[2] : api 地址
            tmp[3] : 请求的参数
            tmp[4] : 请求头部
            tmp[5] : 请求方法
            tmp[6] : 预期结果 
            '''
            tmp.append(int(table.cell_value(i, 0)))  # 用例编号
            tmp.append(table.cell_value(i, 4))  # url
            # key=value&key1=value1 格式转换
            tmp.append(convert_urlpara_to_dict(table.cell_value(i, 5)))     # param
            tmp.append(convert_headers_to_dict(table.cell_value(i, 6)))     # headers
            tmp.append(table.cell_value(i, 7))  # method
            tmp.append(table.cell_value(i, 8))  # 预期结果
            res.append(tmp)
    return res


def get_testcase(tables, index_table, start, stop):
    """"
    从 table[index_table] 获取 start 到 stop 的测试用例
    :param tables: 包含工作表的列表
    :param index_table: 工作表的索引
    :param start: 开始执行用例的编号
    :param stop: 结束执行用例的编号
    :return:
    """
    res = []
    try:
        table = tables[index_table]
        for i in range(start, stop):
            tmp = []
            tmp.append(int(table.cell_value(i, 0)))  # 用例编号
            tmp.append(table.cell_value(i, 4))  # url
            tmp.append(convert_urlpara_to_dict(table.cell_value(i, 5)))  # param
            # tmp.append(json.loads(table.cell_value(i, 5)))  # param
            tmp.append(convert_headers_to_dict(table.cell_value(i, 6)))  # headers
            tmp.append(table.cell_value(i, 7))  # method
            tmp.append(table.cell_value(i, 8))  # 预期结果
            res.append(tmp)
        return res
    except Exception as e:
        print('Error: ', e)


def convert_urlpara_to_dict(param_data):
    """ 转换url 参数
    :param param_data:
    :return:
    """
    lines = param_data.split('&')
    result = {}
    for line in lines:
        tmp = line.strip().split('=', 1)
        if len(tmp) > 1:
            try:
                result[tmp[0]] = tmp[1]
            except IndexError as e:
                print('IndexError: ', e)
    return result


def convert_headers_to_dict(headers_data):
    """ 转换 头部信息
    :param headers_data:
    :return:
    """
    lines = headers_data.strip().splitlines()
    result = {}
    for line in lines:
        line.strip()
        tmp = line.split(':', 1)
        if len(tmp) > 1:
            try:
                result[tmp[0].strip()] = tmp[1].strip()
            except IndexError as e:
                print('IndexError: ', e)
    return result


def send_request(cases, cookies):
    """
    执行测试用例
    :param cases:
    :param cookies:
    """
    count = len(cases)  # 总共的测试用例
    casepass = 0    # 通过的测试用例数
    casefail = 0    # 失败的测试用例数
    for case in cases:

        print(f'\033[1;32m 正在执行：测试用例{case[0]}', end='\t \033[0m')

        if str(case[4]).lower() == 'get':
            result = requests.get(url=case[1], data=case[2], headers=case[3], cookies=cookies, timeout=8)
            try:
                assert result.text == case[5]
            except AssertionError as e:
                print('expect: ', case[5])
                print('result: ', result.text)
                print('\033[1;31m Error \033[0m', e, end='  ')
                print('\033[1;31m测试用例未通过\033[0m')
                casefail += 1
                continue
        elif str(case[4]).lower() == 'post':
            result = requests.post(url=case[1], data=case[2], headers=case[3], cookies=cookies, timeout=8)
            try:
                assert result.text == case[5]
            except AssertionError as e:
                print('expect: ', case[5])
                print('result: ', result.text)
                print('\033[1;31m Error \033[0m', e, end='  ')
                print('\033[1;31m测试用例未通过\033[0m')
                casefail += 1
                continue

        print(f'\033[1;32m =========>  测试用例{case[0]}通过\033[0m')
        casepass += 1

    print(f'共执行测试用例: {count}, 通过：{casepass}, 未通过： {casefail}')


def get_table_row(tables, index):
    """ 获取行数 """
    return tables[index].nrows


def get_tables_len(tables):
    """ 获取工作表的数量 """
    return len(tables)


def execute_apis(file, *, cookies):
    """
    执行全部用例
    :param file: 要执行的接口文档
    :param cookies: cookie
    """
    tables = read_excel(file)
    cases = get_testcases(tables)
    send_request(cases, cookies)


def execute_api(*, file, cookies, index_table=0, start, stop):
    """
    选择部分测试用例执行
    :param file: 要执行的接口文档
    :param cookies: cookie
    :param index_table: sheet工作表的索引，从0开始
    :param start:  开始执行的excel表的行标
    :param stop:  结束执行的行标 不包括 0
    """

    tables = read_excel(file)

    if index_table >= get_tables_len(tables):
        print('不存在此工作表')
        return

    if start >= 1:
        if stop > get_table_row(tables, index_table):
            print('结束行标大于实际行数')
            return
    else:
        print('开始行标应大于0')
        return

    cases = get_testcase(tables, index_table, start, stop)
    send_request(cases, cookies)


if __name__ == '__main__':
    pass

# 问题：
# 设置请求超时
# 边界检查


