# pip install discord.py 후 진행
import discord
from discord.ext import commands
import auto_config
import embed
import traceback
import DB
import config
import auto_config

"""
    discord basic setting
    디스코드 기본 설정
    command_prefix : None -> 명령어로 시작할 접두사 지정
    activity : None -> ~ 하는 중 같은 활동 없애기
    help_command : None -> 기본 도움말 명령어 제거
"""
intents = discord.Intents.default()
intents.message_content = True # 서버에서 명령어 인식 여부 (default = false)
bot_activity = discord.Game(name='돈 세기')
bot = commands.Bot(command_prefix='!', intents=intents, activity=None, help_command=None) # 명령어의 시작이 ! ex) !안녕 


@bot.event 
async def on_ready():
    print (f'{bot.user.name}이 연결 되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=bot_activity)
"""
    Bot connecting events
    봇 연결 이벤트

    change_presence : 상태 변경 메소드 함수
    
    status : [online, offline, idle, dnd, invisible]
    -> 온라인, 오프라인, 자리비움, 다른 용무중, 오프라인 표시

"""

# !안녕 명령어 정의
# @bot.command()
# async def 안녕(ctx):
#     await ctx.send("안녕!")

"""
    봇 커맨드 테스트 코드
"""

@bot.command(aliases=['자산'])
async def 지갑(ctx):
    try:
        wallet = auto_config.getwallet()
        KRW = auto_config.getKRW()
        await ctx.send("{} 님의 매수자산은 : {} 원, 원화자산은 : {} 원 입니다.".format(ctx.author.nick,wallet,KRW))
    except Exception as e:
        print(e)

    """
        업비트 API로부터 자산을 가져와 표시해준다.
        
        ctx.author.nick : 명령어를 작성한 사람의 닉네임
        ctx.send() : 봇이 메시지로 출력
        ctx.message.delete() : 명령어 내역을 채팅에서 삭제

    """

@bot.command(aliases=['도움말'])
async def help(ctx):
    msg = await ctx.send(embed=embed.helpEmbed)
    await msg.delete(delay=10)

    """
        도움말 명령어

        aliases : 같은 동작을 하는 명령어 추가 -> !help == !도움말
        embed : 임베드 메시지로 이미지, 이모지, 제목, 필드, 바닥글 등을 추가하여 메시지를 보낼 수 있다.

    """

# @bot.command()
# async def 코인(ctx):
#     msg = await ctx.send(embed=embed.coinEmbed)
#     await msg.add_reaction("<:Bitcoin:1128215499461906474>")
#     await msg.add_reaction("<:Etherum:1128216018137915472>")
#     await msg.add_reaction("<:XRP:1128216590375206985>")

    """
        코인 종목을 설정할 수 있는 명령어

        .add_reaction() : 반응을 추가할 수 있는 메소드 함수
        -> 이모지 id는 "\이모지"를 채팅에 입력하여 확인

    """
    
@bot.command()
async def 현재가(ctx, ticker):
    coin_dict = {"비트코인":"BTC","이더리움":"ETH","리플":"XRP"}
    if( ticker not in coin_dict):
        await ctx.send("확인할 수 없는 종목입니다.")
        return
    current_price = auto_config.getcurrentPrice(ticker=coin_dict[ticker])
    await ctx.send("{} 원 입니다.".format(current_price))

    """
        입력한 코인의 현재가를 가져온다.
    """

# @bot.command()
# async def 주문(ctx,ticker):
#     coin_dict = {"비트코인":"BTC","이더리움":"ETH","리플":"XRP"}
#     if(ticker not in coin_dict.keys):
#         await ctx.send("현재 코인은 {} 만 가능합니다.".format(coin_dict.keys))
#     wait = auto_config.getorderlist(coin_dict[ticker])
#     if(len(wait)==0):
#         await ctx.send("주문내역이 없습니다.")
#         return
#     detailEmbed = discord.Embed(title="주문상황",description="주문대기중 상황을 알려준다.",color=0xF5A9A9)
#     detailEmbed.add_field(name="주문 대기중",value=wait,inline=False)
#     await ctx.send(embed=detailEmbed)
# @주문.error
# async def 주문에러(ctx,error):
#     await ctx.send("코인을 입력해주세요")

    """
        입력한 코인의 주문 상황을 가져온다.
        주문 대기 중 내역을 보여준다.
    """

@bot.command()
async def 매수(ctx):
    try:
        krw = auto_config.upbit.get_balance("KRW")
        if krw * 0.9995 < 5000 :
            await ctx.send("원화가 부족합니다. 최소주문금액을 확인해주세요.")
        auto_config.upbit.buy_market_order("KRW-BTC",krw*0.9995)
        avg_price = auto_config.upbit.get_avg_buy_price("KRW-BTC")
        await ctx.send("평균 매수가 {} 원 으로 매수 완료.".format(avg_price))
    except Exception as e:
        print(e)
    pass

@bot.command()
async def 매도(ctx):
    try:
        if auto_config.upbit.get_balance("KRW-BTC") * round(auto_config.pyupbit.get_current_price("KRW-BTC"), 0) > 5000 :
            auto_config.sell_coin()
            await ctx.send("매도 하였습니다.")
        else:
            await ctx.send("매수한 코인이 없습니다.")
    except Exception as e:
        print(e)
        await ctx.send(e)

    """
    
        현재 매수한 코인을 매도한다.
    
    """

@bot.command()
async def 매수가(ctx):
    if auto_config.upbit.get_balance("KRW-BTC") * round(auto_config.pyupbit.get_current_price("KRW-BTC"), 0) > 5000 :
        await ctx.send("현재 평균매수가는 {} 원 이고, 총 매수가는 {} 원 입니다.".format(
            auto_config.upbit.get_avg_buy_price("KRW-BTC"),
            round(
            auto_config.upbit.get_balance("KRW-BTC")*auto_config.upbit.get_avg_buy_price("KRW-BTC"),0)
        ))
    pass

    """
    
        현재 매수한 코인의 매수가를 보여준다.
    
    """

@bot.command()
async def 수익(ctx):
    if auto_config.upbit.get_balance("KRW-BTC") * round(auto_config.pyupbit.get_current_price("KRW-BTC"), 0) > 5000 :
        await ctx.send("현재 비트코인 수익은 {} % 입니다.".format(round((auto_config.pyupbit.get_current_price("KRW-BTC")/auto_config.upbit.get_avg_buy_price("KRW-BTC")-1)*100,3)))
    else:
        await ctx.send("매수한 코인이 없습니다.")
    
    """
    
        현재 매수한 코인의 수익률을 보여준다.
    
    """

@bot.command()
async def 수익률(ctx):
    mth_rate = DB.sqlexc("SELECT exp(sum(log(rate))) from {}.{}".format(config.database,config.mth_table))
    if mth_rate is None:
        mth_rate = 0
    count = DB.sqlexc("SELECT count(*) from {}.{}".format(config.database,config.mth_table))
    await ctx.send("{} 개월 간 수익률 은 {} % 입니다.".format(count[0][0],mth_rate[0][0]))

    """

        DB에서 한 달 단위의 수익률을 가져와 총 수익률을 계산해 출력한다.
        
    """

@bot.command()
async def 정산(ctx):
    rate = DB.sqlexc("SELECT exp(sum(log(rate))) as avr from {}.{}".format(config.database,config.detail_table))
    mth_rate = DB.sqlexc("SELECT exp(sum(log(rate))) as avr from {}.{}".format(config.database,config.mth_table))
    pl  = DB.sqlexc("SELECT sum(pl) as pl from {}.{}".format(config.database,config.detail_table))
    mth_pl = DB.sqlexc("SELECT sum(profit_loss) as pl from {}.{}".format(config.database,config.mth_table))
    mth_count = DB.sqlexc("SELECT sum(count) from {}.{}".format(config.database,config.mth_table))
    count = DB.sqlexc("SELECT count(*) from {}.{}".format(config.database,config.detail_table))
    receiptEmbed = discord.Embed(title="정산 결과")
    receiptEmbed.add_field(name="거래 횟수",value="{} 번".format(count+mth_count))
    receiptEmbed.add_field(name="수익률",value="{} %".format(rate[0][0]*mth_rate[0][0]),inline=False)
    receiptEmbed.add_field(name="손익",value="{} 원".format(pl[0][0]+mth_pl[0][0]))
    await ctx.send(embed=receiptEmbed)

    """

        DB에서 현재까지의 거래내역들을 정산한다.

    """

@bot.command()
async def 오늘장(ctx):
    is_bull = auto_config.rising_coin("KRW-BTC")
    await ctx.send("현재 BTC 는 {} 중 입니다.".format("상승" if is_bull else "하락"))

    """

        BTC(비트코인)이 현재 상승/하락 인지 알려준다.
    
    """

@bot.command(aliases=['adr','변동장'])
async def ADR(ctx):
    J,S = auto_config.coin_ADR('BTC')
    rise = "변동" if J else "횡보"
    await ctx.send("지금 {} 추세 입니다.".format(rise))

@bot.event
async def on_command_error(ctx,error):
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    err = [line.rstrip() for line in tb]
    errstr = '\n'.join(err)
    if isinstance(error, commands.CommandError):
        msg = await ctx.send('잘못된 명령어입니다.')
        await ctx.message.delete()
        await msg.delete(delay=2)
    else:
        print(errstr)

    """
        커맨드 오입력에 따른 이벤트
        명령어에 없는 입력을 할 경우 실행
    """

# @bot.event
# async def on_reaction_add(reaction,user):
#     coin = ""
#     if user.bot == 1: #봇이면 패스
#         return None
#     if str(reaction.emoji) == "<:Bitcoin:1128215499461906474>":
#         await reaction.clear()
#         msg = await reaction.message.channel.send("비트코인으로 설정 합니다.")
#         coin = "비트코인"
#         type = "BTC"
#         await reaction.message.delete(delay=2)
#     if str(reaction.emoji) == "<:Etherum:1128216018137915472>":
#         await reaction.clear()
#         msg = await reaction.message.channel.send("이더리움으로 설정 합니다.")
#         coin = "이더리움"
#         type = "ETH"
#         await reaction.message.delete(delay=2)
#     if str(reaction.emoji) == "<:XRP:1128216590375206985>":
#         await reaction.clear()
#         msg = await reaction.message.channel.send("리플로 설정 합니다.")
#         coin = "리플"
#         type = "XRP"
#         await reaction.message.delete(delay=2)
#     await msg.delete(delay=3)
#     await reaction.message.channel.send("현재 코인 : "+coin)

    """
        이모지 반응에 대한 이벤트
        각 이모지를 선택 시 선택한 코인으로 설정시킨다.
    """

# bot에 대한 token 고유값
bot.run(config.token_id)