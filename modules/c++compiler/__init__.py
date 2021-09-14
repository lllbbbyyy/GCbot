import json
import os
import re

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain

from graia.application.message.elements.internal import Plain
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, At

import requests
# 插件信息
__name__ = "c++_online_compiler"
__description__ = "c++在线编译"
__author__ = "Tinyyu433"
__usage__ = "在群内发送c++ xxxxx"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

def count_and_cut_str_line(str):
    count=0
    new_str=str
    if_out=0
    for i in range(len(str)):
        if str[i]=='\n':
            count+=1
        if count >= 20:
            if_out=1
            new_str=str[:i]
            break
    ret=[if_out,new_str]
    return ret


# c++ help
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def cpp_help(app: GraiaMiraiApplication, message: MessageChain, group: Group,member: Member):
    if message.asDisplay() == config_info['key_word'][1] \
            and group.id not in config_info['black_list'] \
            and config_info['allow_use']:
        str = config_info['help_tip']
    if message.asDisplay() == config_info['key_word'][2] \
            and group.id not in config_info['black_list'] \
            and config_info['allow_use']:
        str = config_info['c++_eg']
    await app.sendGroupMessage(group, MessageChain.create([At(member.id),Plain(str)]))

# c++ compiler
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def cpp_compiler(app: GraiaMiraiApplication, message: MessageChain, group: Group,member: Member):
    if message.asDisplay().startswith(config_info['key_word'][0]) \
        and message.asDisplay()!=config_info['key_word'][1]\
        and message.asDisplay()!=config_info['key_word'][2]\
        and group.id not in config_info['black_list'] \
            and config_info['allow_use']:
        url = config_info["url"]
        data = json.dumps({
        "code":message.asDisplay()[len(config_info['key_word'][0])+1:],
        "stdin":(re.findall(r"//\s?StdInput\s?([\w\s]+)\n?",message.asDisplay())[0]) if re.findall(r"//\s?StdInput\s?([\w\s]+)\n?",message.asDisplay()).__len__()!=0 else '',
        "options": config_info["data_options"],
        "compiler":  config_info["data_compiler"],
        "compiler-option-raw":  config_info["data_compiler-option-raw"],
        })
        headers = {'Content-Type': config_info["data_Content-Type"]}
        r_json = requests.request("POST", url, headers=headers,data = data)
        res=r_json.json()
        if "compiler_error" in res.keys():
            resp=(("编译错啦，仔细检查哦\n"+res["compiler_error"]))
        else:
            resp= "\n编译成功"
            if "program_output" in res.keys():
                ret=count_and_cut_str_line(res["program_output"])
                if ret[0]:
                    resp+="，但是我怀疑你在刷屏啊?!只给你前20行吧\n"
                else:
                    resp += "，输出为：\n"
                resp+=ret[1]
        await app.sendGroupMessage(group, MessageChain.create([At(member.id),Plain(resp)]))

