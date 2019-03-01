import pymysql
import datetime


class DataAccess():
    def __init__(self, host='10.19.3.35', user='root', password='123456', db='detect', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.conn = None
        self.cursor = None

    def open_conn(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port,
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def select_(self, sql):
        try:
            self.open_conn()
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            raise e
        finally:
            self.conn.close()
            self.cursor.close()

    def update_(self, sql):
        try:
            self.open_conn()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.conn.close()
            self.cursor.close()

    def select_version(self):
        # import functools
        # s = functools.partial(self.select, sql='SELECT VERSION()')
        # return s()[0]
        return self.select(sql='SELECT VERSION()')[0][0]

    def insert_action(self, sql):
        self.update_(sql)


# 记录检测到异常物体的时间日期
class detectTime(DataAccess):
    def __init__(self):
        super(detectTime, self).__init__()

    def insert(self, img):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into time(dtime, img) values('%s', '%s')" % (current_time, img)
        result = self.insert_action(sql)
        return result

if __name__ == "__main__":

    da=DataAccess()
    a=da.select_("select * from time")
    print(a)
