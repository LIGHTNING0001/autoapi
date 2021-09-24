import os
import pymysql


class ConnTools:

    def __init__(self):
        self.conn = self.__create_conn()

    def updata(self, sql):
        """
        更新数据库表
        :return: 更新成功返回True, 更新失败返回False
        """
        cursor = self.conn.cursor()
        res = cursor.execute(sql)
        self.conn.commit()
        cursor.close()
        if res >= 1:
            return True
        else:
            return False

    def query(self, sql, num=1):
        cursor = self.conn.cursor()
        n = cursor.execute(sql)
        if num > 1:
            res = cursor.fetchmany(n)
        elif num == 1:
            res = cursor.fetchone()
        else:
            res = cursor.fetchall()
        cursor.close()
        return res

    def __create_conn(self):
        """
        创建连接对象
        """
        data = self.__read_db()
        conn = pymysql.connect(
            host=data['host'],
            user=data['user'],
            password=data['password'],
            database=data['database'],
            port=int(data['port'])
        )
        return conn

    def __read_db(self):
        """
        读取数据库配置文件
        配置文件 默认从项目根目录下查找  文件名：db.properties
        返回字典的形式
        """
        li, res = [], {}
        with open(os.getcwd() + '/db.properties', encoding='utf-8') as f:
            li = f.readlines()
        for i in li:
            tmp = i.strip().split('=')
            res[tmp[0]] = tmp[-1]
        return res

    def close(self):
        self.conn.close()

