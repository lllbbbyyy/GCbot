import json
import os
from io import StringIO
import xlrd

from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, At, Image
from graia.application.group import Group, Member, MemberPerm
from graia.template import Template

# 插件信息
__name__ = "namelist_comparer"
__description__ = "比较现有群成员和名单信息"
__author__ = "hxb"
__usage__ = "输入 对照名单"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

# 读取白名单（目前暂时放在了同目录下）
register_list = {}
# root = os.path.join(os.getcwd(), "registers.json")
with open(current_path + '/registers.json', encoding='utf-8') as fp:
    register_list = json.load(fp)


class_list = config_info["major"]
for i in range(1, config_info["class_max"]):
    to_ins = ""
    if len(str(i)) == 1:
        to_ins = "信0" + str(i)
    else:
        to_ins = "信" + str(i)
    class_list.append(to_ins)


def name_match(name):
    if name == "" or name.count("-") != 2:
        return False
    else:
        tmp = name.split("-")
        if len(tmp[0]) != 7 or (tmp[1] not in class_list):
            return False
        return True


@channel.use(ListenerSchema(listening_events=[GroupMessage], inline_dispatchers=[Kanata([FullMatch('对照名单')])]))
async def namelist_comparer(app: GraiaMiraiApplication, message: MessageChain,
                       group: Group, member: Member):
    msg = message.asDisplay()
    if msg in config_info["ask"] and member.id in register_list["admin"]:
        list_info, list_len = read_namelist()

        memlist = await app.memberList(group)
        ret = []

        for mem in memlist:
            if mem.permission != MemberPerm.Member:
                continue
            # 不处理name_format错误的成员
            if not name_match(mem.name):
                continue

            tmp = mem.name.split("-")
            ret.append([tmp[0], tmp[2]])

        not_in_namelist = []
        not_in_group = []
        for it in list_info:
            if it not in ret:
                not_in_group.append(it)

        for it in ret:
            if it not in list_info:
                not_in_namelist.append(it)

        # print到内存中
        s = StringIO()
        print("未加群：%d人" % len(not_in_group), file=s)
        print(not_in_group, file=s)
        print("不在名单中：%d人" % len(not_in_namelist), file=s)
        print(not_in_namelist, file=s)

        await app.sendGroupMessage(group, MessageChain.create([Plain(s.getvalue())]))


# 读取excel名单
filename = config_info["filename"]
sh = config_info["sheet"]


def read_namelist():
    data = xlrd.open_workbook(current_path + '/namelist_demo.xls')
    table = data.sheet_by_index(sh)

    ret = []
    nrows = table.nrows
    for j in range(7, nrows):
        ret.append(table.row_values(j, start_colx=0, end_colx=None)[1:3])

    for it in ret:
        if it[1].find("·") != -1:
            it[1] = it[1][:it[1].find("·")]
    return ret, len(ret)
