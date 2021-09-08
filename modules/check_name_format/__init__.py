import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, At, Plain, MessageChain, GraiaMiraiApplication

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


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def check_name_format(app: GraiaMiraiApplication, message: MessageChain,
                            group: Group):
    msg = [Plain(config_info['top-prompt'])]
    msg.append(Plain("\n"))

    if message.asDisplay() == config_info['ask']:
        # 判断是否匹配的正则表达式
        reg_ex = '^' + config_info['stu-years'] + '5[0-9][0-9][0-9][0-9]\-(信(01'
        # 班号（感觉有点笨）
        for num in range(2, config_info['class-num'] + 1):
            reg_ex = reg_ex + '|'
            if num < 10:
                reg_ex = reg_ex + '0'
            reg_ex = reg_ex + str(num)
        # 专业
        reg_ex = reg_ex + ')'
        for major in config_info['major-list']:
            reg_ex = reg_ex + '|' + major
        reg_ex = reg_ex + ")\-[\u4E00-\u9FA5]+$"

        memlist = await app.memberList(group)
        for mem in memlist:
            ignore = 0
            # 白名单检查
            for white_id in config_info['white-list']:
                if mem.id == white_id:
                    ignore = 1
            if ignore:
                continue

            if not re.match(reg_ex, mem.name):
                msg.append(At(mem.id))
                msg.append(Plain("\n"))
        msg.append(Plain(config_info['bottom-prompt']))
        await app.sendGroupMessage(group, MessageChain.create(msg))
