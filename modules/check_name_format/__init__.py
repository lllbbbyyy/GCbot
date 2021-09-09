import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Member, At, Plain, MessageChain, GraiaMiraiApplication
from graia.application.group import MemberPerm

import re

# 插件信息
__name__ = "check_name_format"
__description__ = "检查群名片"
__author__ = "mqj"
__usage__ = "在群内接收配置文件中的口令后@出群名片格式不对的成员"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}

current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)


def check_name_format_inner_get_reg_ex(strategy):
    # 判断是否匹配的正则表达式
    reg_ex = '^' + strategy['stu-years'] + '5[0-9]{4}\-(信(01'
    # 班号（感觉有点笨）
    for num in range(2, strategy['class-num'] + 1):
        reg_ex = reg_ex + '|'
        if num < 10:
            reg_ex = reg_ex + '0'
        reg_ex = reg_ex + str(num)
    # 专业
    reg_ex = reg_ex + ')'
    for major in strategy['major-list']:
        reg_ex = reg_ex + '|' + major
    # 姓名
    reg_ex = reg_ex + ")\-[\u4E00-\u9FFF"
    for ch in strategy['special-ch']:    # 姓名中可能包含的特殊字符
        reg_ex = reg_ex + ch
    reg_ex = reg_ex + "]+$"
    return reg_ex


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def check_name_format(app: GraiaMiraiApplication, message: MessageChain,
                            group: Group, member: Member):
    if str(group.id) in config_info['groups-enabled'].keys():
        # 判断群组权限
        strategy = config_info['default-strategy']
        if not config_info['groups-enabled'][str(group.id)]['use-default-strategy']:
            strategy = config_info['groups-enabled'][str(group.id)]['strategy']
        if message.asDisplay() == strategy['ask']:
            # 判断群员权限
            if strategy['permission'] == 'All' or\
              (strategy['permission'] == 'Owner-Admin' and member.permission != MemberPerm.Member) or\
              (strategy['permission'] == 'Owner' and member.permission == MemberPerm.Owner):
                reg_ex = check_name_format_inner_get_reg_ex(strategy)
                msg = [Plain(strategy['top-prompt'])]
                msg.append(Plain("\n"))
                memlist = await app.memberList(group)
                for mem in memlist:
                    # 白名单检查
                    if mem.id in strategy['white-list']:
                        continue
                    if not re.match(reg_ex, mem.name):
                        if strategy['should-at']:
                            msg.append(At(mem.id))
                        else:
                            msg.append(Plain(mem.name))
                        msg.append(Plain("\n"))
                msg.append(Plain(strategy['bottom-prompt']))
                await app.sendGroupMessage(group, MessageChain.create(msg))
