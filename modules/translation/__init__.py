import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain

from graia.application.message.elements.internal import Plain
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, At

from googletrans import Translator

# 插件信息
__name__ = "translation"
__description__ = "翻译"
__author__ = "da-qing-wa"
__usage__ = "在群内发送trans to xx xxxxx"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)


translator = Translator(service_urls=[config_info['url']])
# str_min_len是“trans to xx ”的长度，小于该长度时不触发。
str_min_len = len(config_info['key_word'][0]) + config_info['choice_len'] + 1


# trans help
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def trans_help(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay() == config_info['key_word'][1] \
            and group.id not in config_info['black_list'] \
            and config_info['allow_use']:
        str = "trans功能支持翻译成以下语言："
        for choice in config_info['choice']:
            str += "\n" + choice + " - " + config_info['choice'][choice]
        str += "\n格式为 trans to xx hello"
        await app.sendGroupMessage(group, MessageChain.create([Plain(str)]))


# translation
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def trans(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith(config_info['key_word'][0]) \
            and len(message.asDisplay()) > str_min_len \
            and group.id not in config_info['black_list'] \
            and config_info['allow_use']:
        choice = message.asDisplay()[len(config_info['key_word'][0]):len(config_info['key_word'][0]) + config_info['choice_len']]
        str = ""
        # 翻成中文
        if choice == 'ch':
            str += "翻译结果为：\n"
            # +1是因为还要跳过一个空格
            str += translator.translate(message.asDisplay()[len(config_info['key_word'][0]) + config_info['choice_len'] + 1:], dest='zh-CN').text
        # 翻成其他语言
        elif choice in config_info['choice'] \
                and message.asDisplay()[len(config_info['key_word'][0]) + config_info['choice_len']] == ' ':
            str += "翻译结果为：\n"
            # +1是因为还要跳过一个空格
            str += translator.translate(message.asDisplay()[len(config_info['key_word'][0]) + config_info['choice_len'] + 1:], dest=choice).text
        else:
            str += "不支持这种语言噢，换一种试试叭！"
        await app.sendGroupMessage(group, MessageChain.create([Plain(str)]))
