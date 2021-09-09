import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain

from graia.application.message.elements.internal import Plain
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, At
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

config_info = {}
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

import requests


data = {}


# guess
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def guess(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith(config_info['key_word']) and group.id not in config_info['black_list'] and config_info['allow_use']:
        data[config_info['cloud_api']['str_key']] = message.asDisplay()[config_info['substr_start_pos']:]
        resp = requests.post(url=config_info['cloud_api']['api'], data=data)
        json = resp.json()
        str = ""
        if not json:
            str += "找不到噢,试试别的叭！"
        elif "trans" not in json[0]:
            if not json[0]["inputting"]:
                str += "找不到噢,试试别的叭！"
            else:
                str += message.asDisplay()[config_info['substr_start_pos']:] + "可能是" + "\n" + json[0]["inputting"][0]
        else:
            str += message.asDisplay()[config_info['substr_start_pos']:] + "可能是"
            for i in json[0]["trans"]:
                str += '\n' + i
        await app.sendGroupMessage(group, MessageChain.create([Plain(str)]))


# @channel.use(ListenerSchema(listening_events=[GroupMessage]))
# async def chat(app: GraiaMiraiApplication, message: MessageChain, group: Group):
#     url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg="
#     if message.asDisplay().startswith("chat"):
#         url += message.asDisplay()[5:]
#         res = requests.get(url)
#         resp = res.json()["content"]
#         await app.sendGroupMessage(group, MessageChain.create([Plain(resp)]))

