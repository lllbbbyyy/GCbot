import json
import os

from graia.application.message.elements.internal import At
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, Member, GroupMessage, Plain, MessageChain, GraiaMiraiApplication
from graia.application.group import MemberPerm

import re

# 插件信息
__name__ = "self_mute"
__description__ = "自助禁言"
__author__ = "MoonKuun"
__usage__ = "在群内发送配置文件中的触发指令和禁言时间"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

current_path = os.path.dirname(__file__)

config_info = {}
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def self_mute(app: GraiaMiraiApplication, message: MessageChain,
                    group: Group, member: Member):
    if str(group.id) in config_info['groups-enabled'].keys():
        strategy = config_info['default-strategy']
        if not config_info['groups-enabled'][str(group.id)]['use-default-strategy']:
            strategy = config_info['groups-enabled'][str(group.id)]['strategy']
        
        reg_exr = '^' + strategy['ask'] + ' *?(\d+|\d+\.\d+) *?(d|天|h|min|s|小时|分钟|秒)$'
        match_list = re.findall(reg_exr, message.asDisplay())
        if not len(match_list) == 0:
            #判断群成员权限
            if member.permission == MemberPerm.Member:
                #判断机器人权限
                if group.accountPerm == MemberPerm.Owner or group.accountPerm == MemberPerm.Administrator:
                    #计算禁言时长
                    time_str = match_list[0][0]
                    time_unit = match_list[0][1]
                    second = 0
                    if time_unit == 'd' or time_unit == '天':
                        second = int(float(time_str) * 24 * 60 * 60)
                    elif time_unit == 'h' or time_unit == '小时':
                        second = int(float(time_str) * 60 * 60)
                    elif time_unit == 'min' or time_unit == '分钟':
                        second = int(float(time_str) * 60)
                    elif time_unit == 's' or time_unit == '秒':
                        second = int(float(time_str))
                    
                    #禁言时间超上限取上限
                    if second > strategy['time-range']:
                        second = strategy['time-range']
                        await app.mute(group, member.id, second)
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(' ' + strategy['over-range-message'])]))
                    else:
                        await app.mute(group, member.id, second)
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(' ' + strategy['success-message'])]))
                else:
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(' ' + strategy['bot-no-permission-message'])]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(' ' + strategy['target-not-member-message'])]))
