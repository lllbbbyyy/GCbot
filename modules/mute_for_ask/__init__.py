import json
import os
import random

from graia.application.group import MemberPerm, Member
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.literature import Literature
from graia.application.message.parser.signature import FullMatch
from graia.application.message.elements.internal import Plain, At, Image
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.message.parser.literature import Literature

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication
from graia.application.message.elements.internal import MessageChain, Plain, AtAll, At

# 插件信息
__name__ = "mute_for_ask"
__description__ = "随机给禁言套餐"
__author__ = "胡孝博"
__usage__ = "在群内发送指令：我要禁言套餐"

current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


@channel.use(ListenerSchema(listening_events=[GroupMessage], inline_dispatchers=[Kanata([FullMatch('我要禁言套餐')])]))
async def mute_for_ask(app: GraiaMiraiApplication, message: MessageChain,
                      group: Group,member: Member):
    if config_info["switch"]:
        if member.permission == MemberPerm.Member:
            ret =random.randint(60/2, 60*60)
            if group.accountPerm == MemberPerm.Administrator:
                await app.mute(group, member, ret)
            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(" 恭喜你获得%d分钟禁言套餐"% (ret/60+1))]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(" ???")]))

    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain("本功能暂已关闭")]))
        #await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile(os.path.dirname(__file__) + '/' + "qiuguanli.jpg")]))
