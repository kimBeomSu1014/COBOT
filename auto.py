
import config 
import time
import DB
import auto_config


# 매수/매도 조건 변수
cond = auto_config.havingCoin("BTC")
buy_cond = False

# 프로그램 시작
while True:
    try:
        J,S = auto_config.coin_ADR("BTC")
        #is_bull = auto_config.rising_coin("KRW-BTC") # 상승장 판단
        krw = auto_config.upbit.get_balance("KRW")
        if cond is False:
            if J : # 변동성이 있는 장
                # < 변동성 돌파 전략 >
                BP = auto_config.Trading("BTC")
                is_buy = auto_config.Trading_coin("BTC",BP)
                if is_buy and S :
                    if krw * 0.9995 > 5000 : # 최소 주문 금액 5000원 이상인지 판단
                        print("하락장 매수 완료")
                        cond = True
                        buy_cond = True
                        time.sleep(10)
                        continue
                    else :
                        print("최소 주문 금액 부족")
                        time.sleep(3600)
                        continue
            else: # 횡보 시 
                if S and (krw * 0.9995 > 5000):
                    print("상승기세 매수 완료")
                    cond = True
                    buy_cond = True
                    time.sleep(10)
                    continue
                else :
                    time.sleep(10)
                    continue
        else:
            if buy_cond is True:
                buy_result = auto_config.upbit.buy_market_order("KRW-BTC",krw*0.9995)
                buy_cond = False
            avg_price = auto_config.upbit.get_avg_buy_price("KRW-BTC")
            buy_profit = auto_config.pyupbit.get_current_price("KRW-BTC")/avg_price
            if(auto_config.havingCoin("BTC") is False):
                    print("수동 매매 되었습니다.")
                    cond = False
                    continue
            if((S is False) and (buy_profit > 1.015 or buy_profit < 0.95)):
                coin = auto_config.upbit.get_balance("KRW-BTC")
                current_price = round(auto_config.pyupbit.get_current_price("KRW-BTC"), 0)
                if ((current_price * coin) > 5000 and auto_config.havingCoin("BTC")):
                    cond = auto_config.sell_coin()
                    continue
                else:
                    print("최소 매도 수량이 아닙니다.")
                    continue
            
    except Exception as e:
        print(e)
        time.sleep(60)