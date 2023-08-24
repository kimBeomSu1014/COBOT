import discord

"""
    임베드 메시지 구성시

    discord.Embed() :
        title : 제목 [str] , 
        description : 설명 [str] ,
        color : 색깔 [int](16진수) ,
        url : 링크 [str]
    
    .add_field():
        name : 필드 이름 [str] ,
        value : 내용 [str] ,
        inline : 줄바꿈 [boolean] ,
    
"""

helpEmbed = discord.Embed(title="도움말",color=0xFF0080)
helpEmbed.add_field(name="!help",value="명령어 도움말", inline=False)
helpEmbed.add_field(name="!지갑,!자산",value="현재 지갑 잔고를 알려준다.",inline=False)
helpEmbed.add_field(name="!현재가",value="구매한 코인의 현재가를 알려준다.",inline=False)
helpEmbed.add_field(name="!매수가",value="구매한 코인의 평균 매수가를 알려준다.",inline=False)
helpEmbed.add_field(name="!수익",value="구매한 코인의 수익을 알려준다.",inline=False)
helpEmbed.add_field(name="!정산",value="현재까지의 거래내역을 정산하여 알려준다.",inline=False)
helpEmbed.add_field(name="!오늘장",value="비트코인의 상승세/하락세 를 알려준다.",inline=False)
helpEmbed.add_field(name="!ADR,!adr,!변동장",value="비트코인의 변동/횡보 를 알려준다.",inline=False)
# helpEmbed.add_field(name="!코인",value="코인의 종목을 설정한다.",inline=False)


"""
    도움말 임베드 메시지 구성
"""

coinEmbed = discord.Embed(title="코인 설정하기",description="거래하고 싶은 코인으로 변경해 보아요", color=0xD8F781)
coinEmbed.add_field(name="<:Bitcoin:1128215499461906474>",value="비트코인")
coinEmbed.add_field(name="<:Etherum:1128216018137915472>",value="이더리움")
coinEmbed.add_field(name="<:XRP:1128216590375206985>",value="리플")

"""
    코인 설정 임베드 메시지 구성
"""
