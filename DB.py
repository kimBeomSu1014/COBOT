import pymysql
import config

def sqlexc(sql):
    conn = pymysql.connect(host=config.host_IP, user = config.user_name, password = config.user_password, db = config.database)
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()
    result = curs.fetchall()
    curs.close()
    conn.close()
    return result

"""

    DB에 참조하여 sql문을 통해 접근할 수 있는 함수

"""