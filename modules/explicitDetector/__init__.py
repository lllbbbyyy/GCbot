"""
Sayu::Modules::ExplicitDetector
复读检查模块
By GTY
"""

import json
import os
import random

from graia.application import Member
from graia.application.message.elements.internal import At
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication

# 插件信息
__name__ = "explicit_detector"
__description__ = "脏话检测"
__author__ = "GTY"
__usage__ = "群内产生消息时，主动处理。"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

current_path = os.path.dirname(__file__)


with open(current_path + '/warning_words_list.json', 'r', encoding='utf-8') as f:
    warning_words_list = json.load(f)


def warn_dont_speak_explicitly():
    return random.choice(warning_words_list)


exp_list = list()  # 脏话列表

'''
请将脏话词库以json格式存储于同路径 exp_list.json 文件中
json格式：
{
  "data": [
    "脏话1",
    "脏话2",
    ...
  ]
}
'''

with open(current_path + '/exp_list.json', 'r', encoding='utf-8') as f:
    exp_list = json.load(f)['data']


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def exp_detector(app: GraiaMiraiApplication, group: Group,
                       message: MessageChain, member: Member):
    for w in exp_list:
        if w in message.asDisplay():
            msg_list = [
                At(member.id),
                Plain(' '),
                Plain(warn_dont_speak_explicitly())
            ]
            await app.sendGroupMessage(group, MessageChain.create(msg_list))
