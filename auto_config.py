#-*- coding:utf-8 -*-
import pyupbit
import config 
import DB
import time


access_key = config.access_key
secret_key = config.secret_key
upbit = pyupbit.Upbit(access_key, secret_key)

# 지갑 정보 가져오기
def getwallet():
    lists = upbit.get_balances()
    filtered_lists = [item for item in lists if item['avg_buy_price'] != '0' and float(item['balance']) > 0.5]
    if(len(filtered_lists) == 0):
        return 0
    price = sum(float(cash['balance']) for cash in filtered_lists)
    return price

#지갑 원화 가져오기
def getKRW():
    KRW = round(upbit.get_balance("KRW"),0)
    return KRW

# 현재가 가져오기
def getcurrentPrice(ticker):
    current_price = pyupbit.get_current_price("KRW-"+ticker)
    return current_price

# 주문 정보 가져오기
def getorderlist(ticker):
    detail_wait = upbit.get_order("KRW-"+ticker)
    return detail_wait

# <변동성 돌파 전략>
"""

    변동성이 큰 시장에서 사용하는 전략으로
    상승기점을 돌파하면 매수신호, 하락기점을 돌파하면 매도신호 등을 보내는 전략.

"""
def Trading(ticker):
    df = pyupbit.get_ohlcv(ticker="KRW-"+ticker,interval="day",count=2)
    Range = df.iloc[0]['high'] - df.iloc[0]['low']
    BP = Range*0.5 + df.iloc[1]['open']
    return BP

def Trading_coin(ticker,BP):
    current_price = pyupbit.get_current_price(ticker="KRW-"+ticker)
    if BP > current_price:
        return True
    else:
        return False
    
def havingCoin(ticker):
    try:
        mount = upbit.get_balance("KRW-"+ticker)
        price = upbit.get_avg_buy_price("KRW-"+ticker)
        total = round(mount*price,0)
        if total > 5000 :
            return True
        else :
            return False
    except Exception as e:
        print(e)

# 변동장 함수 <MACD 전략>
"""

    횡보시장에서 사용하는 전략
    이동평균수렴확산 전략

"""
def rising_coin(ticker):
    df = pyupbit.get_ohlcv(ticker)

    new_df = df ['close']
    MOV = df['close'].rolling (window=20, min_periods=1).mean()#. iloc [-1]
    ShortEMA = df.close.ewm(span=12, adjust=False).mean()
    LongEMA = df.close.ewm (span=26, adjust=False).mean()
    MACD = LongEMA - ShortEMA
    signal = MACD.ewm(span = 9, adjust = False).mean()
    EMA = df['close'].ewm(span=100, adjust = False).mean()

    price = pyupbit.get_current_price(ticker)
        
    # 1. MACD가 Sigmal선보다 위쪽 #2. MACD 값은 하향이 아닌 상승 #3. 현재 가상 화폐의 가격은 100일 EMA선보다 위쪽 #4. 20일 이동평균보다도 높다 #5. 현재의 가상 화계 가격은 이전의 가격보다 높다
    if (MACD[-1] > signal[-1]) and (MACD[-1] > MACD[-2]) and (price > EMA[-1]) and (price > MOV[-1]) and (price > new_df[-2]):
        return True
    else:
        return False

def sell_coin():
    avg_price = upbit.get_avg_buy_price("KRW-BTC")
    coin = upbit.get_balance("KRW-BTC")
    current_price = round(pyupbit.get_current_price("KRW-BTC"), 0)
    upbit.sell_market_order("KRW-BTC", coin)  # 시장가 매도
    rate = round(current_price/avg_price,3)
    print("매도완료")
    buy_price = (avg_price*coin) * 0.9995
    sell_price = (current_price * coin) * 0.9995  # 매도 총가 = (매도가 * 종목수량) * 수수료 빼기
    profit = (round(buy_price - sell_price, 0) * -1)  # 수익 = (매수 총가 - 매도 총가) 반올림 후 -1 곱하기
    DB.sqlexc("INSERT INTO {}.detail (coin,buy,sell,rate,lp) VALUES ('BTC',{},{},{},{})"
                .format(config.database,buy_price,sell_price,rate,profit))
    time.sleep(100)
    return False

# <횡보장 전략 ADR 매수>
def coin_ADR(ticker):
    df = pyupbit.get_ohlcv("KRW-"+ticker,interval="minute30",count=12)
    new_df = df['high'] - df['low']
    ADR = new_df.mean()
    J = True if ADR > 78000 else False # T이면 변동성, F이면 횡보
    df2 = pyupbit.get_ohlcv("KRW-"+ticker,count=100)
    MA = df2.close.rolling(window=5, min_periods=1).mean()
    S = True if (pyupbit.get_current_price("KRW-"+ticker) >= MA.iloc[-1]) else False
    return J,S
