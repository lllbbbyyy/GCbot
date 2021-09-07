"""
Sayu::Modules::RepeatChecker
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
__name__ = "repeat_checker"
__description__ = "复读检测"
__author__ = "GTY"
__usage__ = "群内产生消息时，主动处理。"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}
# 打开配置文件
# 配置文件格式为：
# {
#     "ask":str,
#     "ans":str
# }
current_path = os.path.dirname(__file__)


def warn_dont_repeat():
    msg_list = ["不许复读！", "不要复读！", "别复读啊..."]
    return random.choice(msg_list)


def just_warn_dont_repeat_this_time():
    msg_before_list = ['这次先警告，',
                       '这次就算了',
                       '这次放过你',
                       '这次饶过你',
                       '先饶了你',
                       '既然是初犯，就算了']
    msg_after_list = ['下不为例哈~',
                      '不会有下一次的吧...',
                      '不许有下次！']
    return random.choice(msg_before_list) + '，' + random.choice(msg_after_list)


last_msg = dict()

user_record = dict()

'''
复读存储格式：
{
    "key1" {
        "skey1": num1,
        "skey2": num2,
        ...
    }
}
key1 为用户QQ号
skeyX 为群号
'''

current_path = os.path.dirname(__file__)
with open(current_path + '/userRecord.json', 'r', encoding='utf-8') as f:
    user_record = json.load(f)


def store_user_record():
    with open(current_path + '/userRecord.json', 'w', encoding='utf-8') as f:
        json.dump(user_record, f)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def repeat_checker(app: GraiaMiraiApplication, group: Group,
                         message: MessageChain, member: Member):
    gid = group.id
    uid = member.id

    if not str(gid) in last_msg.keys():
        last_msg[str(gid)] = message.asDisplay()
    else:
        if '[图片]' in message.asDisplay():
            last_msg[str(gid)] = '[图片]'
            return
        if message.asDisplay() == last_msg[str(gid)]:
            rc_this_group = 0
            rc_total = 0
            if str(member.id) in user_record.keys():
                for group_id in user_record[str(member.id)].keys():
                    if int(group_id) == group.id:
                        rc_this_group = user_record[str(member.id)][group_id]
                    rc_total += user_record[str(member.id)][group_id]

            rc_this_group += 1
            rc_total += 1

            if not str(member.id) in user_record.keys():
                empty_dict_obj = dict()
                user_record[str(member.id)] = empty_dict_obj

            user_record[str(member.id)][str(group.id)] = rc_this_group

            store_user_record()

            msg_list = list()
            msg_list.append(At(member.id))
            msg_list.append(Plain(' '))
            msg_list.append(Plain(warn_dont_repeat()))
            msg_list.append(Plain('\n'))

            if rc_this_group == 1:
                msg_list.append(Plain('这是你首次在本群复读。'))
                msg_list.append(Plain(just_warn_dont_repeat_this_time()))
            else:
                msg_list.append(Plain(f'你在本群复读了{rc_this_group}次，'
                                      f'在高程群共复读{rc_total}次，'
                                      f'当禁言{pow(8, rc_this_group)}秒...'))
                await app.mute(group, member, pow(8, rc_this_group))
                await app.sendGroupMessage(group, MessageChain.create(msg_list))
        else:
            last_msg[str(gid)] = message.asDisplay()
