from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

# 插件信息
__name__ = "guess"
__description__ = "猜测首字母缩写的含义"
__author__ = "da-qing-wa"
__usage__ = "在群内发送guess xxx"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


import requests


url = "https://lab.magiconch.com/api/nbnhhsh/guess"
data = {}


# guess
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def guess(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith("guess") and group.id != 642362943:
        data["text"] = message.asDisplay()[6:]
        resp = requests.post(url=url, data=data)
        json = resp.json()
        str = ""
        if not json:
            str += "找不到噢,试试别的叭！"
        elif "trans" not in json[0]:
            if not json[0]["inputting"]:
                str += "找不到噢,试试别的叭！"
            else:
                str += message.asDisplay()[6:] + "可能是" + "\n" + json[0]["inputting"][0]
        else:
            str += message.asDisplay()[6:] + "可能是"
            for i in json[0]["trans"]:
                str += '\n' + i
        await app.sendGroupMessage(group, MessageChain.create([Plain(str)]))
        # last_msg[group.name] = str


# @channel.use(ListenerSchema(listening_events=[GroupMessage]))
# async def chat(app: GraiaMiraiApplication, message: MessageChain, group: Group):
#     url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg="
#     if message.asDisplay().startswith("chat"):
#         url += message.asDisplay()[5:]
#         res = requests.get(url)
#         resp = res.json()["content"]
#         await app.sendGroupMessage(group, MessageChain.create([Plain(resp)]))

