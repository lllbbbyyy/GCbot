import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication, At

# 插件信息
__name__ = "check_name"
__description__ = "检查群成员群名片是否符合 七位数字-专业-姓名"
__author__ = "codejoker-c"
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
#     "ask":"不理不理！"
# }
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def check_name(app: GraiaMiraiApplication, group: Group,
                     message: MessageChain):
    if message.asDisplay() == config_info['ask']:
        lst1 = await app.memberList(group)
        lst2 = []
        lst3 = ['计科', '大数据', '测绘', '软工', '信安', '交通', '信01', '信02', '信03', '信04', '信05', '信06', '信07',
                '信08', '信09', '信10', '信11', '信12', '信13', '信14', '信15', '信16', '信17', '信18', '信19']
        for i in lst1:
            flag = 0  # 标志名片学号是否有问题，1代表有问题
            major = 0  # 标志专业是否有问题，1代表没有问题
            name = i.name
            for ch in name[:7]:
                if ch < '0' or ch > '9':
                    lst2.append(i.id)
                    flag = 1
                    break

            if flag:
                continue

            j = 0
            for ch in name[8:]:
                if ch == '-':
                    break
                j = j+1
            if j > 3:
                lst2.append(i.id)
                continue

            for i in lst3:
                if i == name[8:8+j]:
                    major = 1
                    break
            if major != 1:
                lst2.append(i.id)

        str = MessageChain.create([Plain('')])
        for i in lst2:
            str.plus(MessageChain.create([At(i), Plain('\n')]))

        await app.sendGroupMessage(group, str)
