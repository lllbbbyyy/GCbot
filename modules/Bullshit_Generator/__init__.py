import random
import json
import os
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Member, At, Plain, MessageChain, GraiaMiraiApplication
from graia.application.group import MemberPerm

# 插件信息
__name__ = "Bullshit_Generator"
__description__ = "狗屁不通文章生成器"
__author__ = "SZY"
__usage__ = "在群内根据用户输入的标题，生成对应的狗屁不通的文章"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

Have_data=True

config_info = {}

current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

try:
    with open(current_path + '/data.json', 'r', encoding='utf-8') as test:
        data = json.load(test)
except FileNotFoundError:
    print('未找到词库文件，请检查词库文件之后重新运行插件')
    Have_data=False
    

def generator(title, length=800):
    """
    :param title: 文章标题
    :param length: 生成正文的长度
    :return: 返回正文内容
    """
    body = ""
    while len(body) < length:
        num = random.randint(0, 100)
        if num < 10:
            body += "\r\n"
        elif num < 20:
            body += random.choice(data["famous"]) \
                .replace('a', random.choice(data["before"])) \
                .replace('b', random.choice(data['after']))
        else:
            body += random.choice(data["bosh"])
        body = body.replace("x", title)
    return body

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def text_generator(app: GraiaMiraiApplication, group: Group,
                        message: MessageChain, member: Member):
               
    if message.asDisplay()=="Bullshit -help":
        help="格式:\nBullshit+文章标题\neg:Bullshit 红红火火恍恍惚惚"
        await app.sendGroupMessage(group,MessageChain.create([Plain(help)]))

    elif message.asDisplay().startswith(config_info['key_word']) and group not in config_info['black_list'] and config_info['allow_use']:
        if Have_data:
            msg=""
            title=message.asDisplay()[config_info['content_start_pos']:]
            if config_info['text_length']:
                msg=generator(title,config_info['text_length'])
            else:
                msg=generator(title)
            await app.sendGroupMessage(group, MessageChain.create([Plain(msg)]))
        else:
            print('Bullshit_Generator:无词库文件，请检查词库文件之后重试')
   