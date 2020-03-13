import time
import pymysql

def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")



def get_conn():
    # :return:连接，游标
    # 建立连接
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="123456",
                           db="epidemic",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果默认以元组显示
    return conn,cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql,*args):
    # 封装通用查询，返回查询结果
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res


def get_centerA_data():
    # 获取centerA实时数据
    # 取时间戳最新的那组数据
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]


def get_centerB_data():
    # 获取map各省实时数据
    # 取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
    "where update_time=(select update_time from details " \
    "order by update_time desc limit 1) " \
    "group by province"
    res = query(sql)
    return res


def get_left_data():
    # 全国累计数据折线图
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


if __name__ == "__main__":
    print(get_left_data())