import sys
import os
import pymysql

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import API

def execute(SQL, fetch=False) :

    result = True

    # host를 127.0.0.1로 바꿔도 작동이 될까?
    connection = pymysql.connect(
        host=API.host,
        user=API.mysql_username,
        password=API.mysql_pwd,
        database=API.database,
        port=API.mysql_port,
        use_unicode=True,
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute(SQL)

    if fetch :
        result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result

def executes(SQLs=[], fetchs=[]) :
    return


# 추가, 수정, 제거, 삭제 단위로 함수 생성
def add() :
    return

def modify() :
    return

def remove() :
    return

def delete() :
    return