import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication

# 插件信息
__name__ = "check_alive"
__description__ = "检查机器人是否存活"
__author__ = "llbbyy"
__usage__ = "在群内发送配置文件中给定的口令"

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
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def check_alive(app: GraiaMiraiApplication, message: MessageChain,
                      group: Group):

    if message.asDisplay() == config_info['ask']:
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(config_info['ans'])]))