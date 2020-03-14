import requests

import pymysql
import time
import json
import traceback  # 追踪异常

def get_tencent_data():
    # 爬虫获取并处理数据
   # 返回历史数据和当日详细数据
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    r = requests.get(url, headers)
    r1= requests.get(url1, headers)
    res = json.loads(r.text)   # json字符串转字典
    res1 = json.loads(r1.text)
    data_all = json.loads(res['data'])
    data_all1 = json.loads(res1['data'])

    history = {}   # 历史记录
    for i in data_all1["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds,"%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d",tup)   #   改变时间格式，不然插入数据库会报错，数据库是datetime类型
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all1["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式，不然插入数据库会报错，数据库是datetime类型
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []  # 当日详细数据
    update_time = data_all["lastUpdateTime"]
    data_country = data_all["areaTree"]   # list25个国家
    data_province = data_country[0]["children"]  # 中国各省
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history,details


def get_conn():
    # :return:连接，游标
    # 建立连接
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="123456",
                           db="epidemic",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn,cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def update_details():
    # 更新detail表:return:
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]   # 0是历史数据字典，1是最新详细数据列表
        conn,cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'  # 对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


def insert_history():
    # 插入历史数据
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0是历史数据字典，1是最新详细数据列表
        print(f"{time.asctime()}开始插入历史数据")
        conn,cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])
        conn.commit()   # 提交事务
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_history():
    # 更新历史数据
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0是历史数据字典，1是最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn,cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()   # 提交事务
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# insert_history()  # 插入历史数据

update_details()




