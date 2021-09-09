import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

import re

# 插件信息
__name__ = "kick_group_member"
__description__ = "踢掉群名片格式不对的人"
__author__ = "da-qing-wa"
__usage__ = "在群内发送 开踢 即可触发"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def kick_group_member(app: GraiaMiraiApplication, group: Group,
                            message: MessageChain, member: Member):
    if message.asDisplay() == '开踢' \
            and (member.permission == member.permission.Administrator
                 or member.permission == member.permission.Owner):
        mylst = await app.memberList(group)
        for stu in mylst:
            if stu.name in config_info['white_lst']:
                continue
            else:
                if not re.match(config_info['match_strategy'], stu.name):
                    await app.sendGroupMessage(group, MessageChain.create([At(stu.id), Plain(" 被踢出")]))
                    if stu.permission == stu.permission.Member:
                        await app.kick(group, stu)