import DB
import datetime
import config


m_rate = DB.sqlexc("SELECT exp(sum(log(rate))) from {}.detail".format(config.database))
m_pl = DB.sqlexc("SELECT sum(lp) from {}.detail".format(config.database))
m_count = DB.sqlexc("SELECT count(*) from {}.detail".format(config.database))
DB.sqlexc("insert into {}.mth_detail (date,rate,profit_loss,count) value ({},{},{},{},{})"
        .format(config.database,
                "{}/{}".format(datetime.datetime.now().year,datetime.datetime.now().month),
                m_rate[0][0],m_pl[0][0],m_count[0][0]))
DB.sqlexc("DELETE FROM {}.detail".format(config.database))

"""

    달 정산 코드
    한 달 동안의 거래내역들을 정리하고 계산하여
    데이터베이스에 넣고 한 달 동안의 거래내역들을 삭제한다.
    
"""