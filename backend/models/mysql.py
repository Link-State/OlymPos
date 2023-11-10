import sys
import os
import pymysql
import re

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


# table = string
# cols, conds = list or tuple
def get(table="", cols=[], conds=[]) :

    sql = f"""
    SELECT {", ".join(cols)}
    FROM {table}
    WHERE {" and ".join(conds)};"""

    print(sql)

    result = execute(sql, True)

    # 반환타입 : list(dict())
    return result

# 추가, 수정, 제거, 삭제, 검색 단위로 함수 생성
def add(table, cols, values) :
    sql = f"""INSERT INTO {table} ({", ".join(cols)})
    VALUES({", ".join(values)});"""

    execute(sql)

    conds = []
    for i in range(len(cols)) :
        if type(values[i]) == type(str()) and (values[i].upper() == "NULL" or values[i].upper() == "NOT NULL") :
            conds.append(f"""{cols[i]} is {values[i]}""")
        else :
            conds.append(f"""{cols[i]} = '{values[i]}'""")

    # 테이블의 정보 받아옴
    result = execute(f"""SHOW INDEX FROM {table}""", True)

    # PK만 필터링
    pks = [dic["Column_name"] for dic in result]
    
    # 생성된 레코드의 기본키 받아오기
    result = get(table, pks, conds)

    if len(result) != 1 :
        return dict()
    
    return result[0]

# table = string
# values, conds = list or tuple
def modify(table, values, conds) :

    sql = f"""
    UPDATE {table}
    SET {", ".join(values)}
    WHERE {" and ".join(conds)};
    """

    execute(sql)

    # 수정이 적용 됐으면 true
    return

# table = string
# conds = list or tuple
def delete(table, conds) :
    sql = f"""
    DELETE FROM {table}
    WHERE {" and ".join(conds)};
    """

    execute(sql)

    # 삭제가 됐으면 true
    return
