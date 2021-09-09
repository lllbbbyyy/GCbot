"""
Sayu::Modules::RecallDetector
小坚果撤回检测模块
By GTY
"""

import json
import os
import random

from graia.application import Member
from graia.application.event.mirai import GroupRecallEvent
from graia.application.message.elements.internal import At
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication

# 插件信息
__name__ = "recall_detector"
__description__ = "检测群消息撤回，并给予处理。"
__author__ = "GTY"
__usage__ = "群消息主动检测"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}
# 打开配置文件
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

user_record = dict()
try:
    with open(current_path + '/user_record.json', 'r', encoding='utf-8') as f:
        user_record = json.load(f)
except FileNotFoundError:
    pass


def save_user_record():
    with open(current_path + '/user_record.json', 'w', encoding='utf-8') as f:
        json.dump(user_record, f)


@channel.use(ListenerSchema(listening_events=[GroupRecallEvent]))
async def recall_detector(app: GraiaMiraiApplication, group: Group, member: Member):
    print(f'Sayu::RecallDetector: recall detected: {group.name}, {member.name}')
    if str(group.id) in config_info['group_enabled'].keys():
        # 已在该群启用撤回检测
        print(f'Sayu::RecallDetector: enabled')
        strategy = config_info['default_strategy']  # 先加载默认策略
        if not config_info['group_enabled'][str(group.id)]['should_use_default_strategy']:
            strategy = config_info['group_enabled'][str(group.id)]['strategy']  # 加载特有的策略
        if int(member.id) in strategy['ignore_members']:
            # 忽略该用户
            return
        if strategy['should_count']:
            # 需要统计复读次数

            if not str(member.id) in user_record.keys():
                # 该用户无”前科“
                print(f'Sayu::RecallDetector: {member.id} added to keys')
                obj = dict()
                user_record[str(member.id)] = obj

            print(f'Sayu::RecallDetector::Debug: rec = {user_record}')

            if not str(group.id) in user_record[str(member.id)].keys():
                # 未在该群撤回过
                user_record[str(member.id)][str(group.id)] = 0

            user_record[str(member.id)][str(group.id)] += 1  # 记录本次复读

            save_user_record()

        if strategy['should_mute']:
            # 应该禁言
            await app.mute(group, member, strategy['mute_time_sec'])

        if strategy['should_warn']:
            msg = [
                At(member.id),
                Plain(' '),
                Plain(random.choice(strategy['warning_words']))
            ]

            if strategy['should_warn_with_count']:
                msg.append(Plain(f'这是你在本群第{user_record[str(member.id)][str(group.id)]}次撤回消息..'))

            await app.sendGroupMessage(group, MessageChain.create(msg))
