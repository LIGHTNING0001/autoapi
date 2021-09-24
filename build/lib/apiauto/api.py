# -*- coding: utf-8 -*-
from apiauto.autoapi import execute_api_xls, execute_apis_xls, get_cookie_inner


def execute_api(file, cookies, index_table, start, stop):
    return execute_api_xls(file, cookies, index_table, start, stop)


def execute_apis(file, cookies):
    return execute_apis_xls(file, cookies)


def get_cookie(url, headers, data):
    return get_cookie_inner(url, headers, data)