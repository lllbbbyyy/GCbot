import json
import os

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, At, Image
from graia.application.group import Group, Member, MemberPerm

# 插件信息
__name__ = "check_name"
__description__ = "检查群名片"
__author__ = "hxb"
__usage__ = "群内输入 检查群名片"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

config_info = {}

current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

root = os.path.join(os.getcwd(), "registers.json")
with open(root, encoding='utf-8') as fp:
    register_list = json.load(fp)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def check_name(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    msg = message.asDisplay()
    ifkick = 0
    if msg in config_info["ask"] and member.id in register_list["admin"]:
        if msg == "pupu checkname-kick":
            ifkick = 1
        if ifkick == 1 and group.accountPerm == MemberPerm.Member:
            await app.sendGroupMessage(group, MessageChain.create([Plain("不具有管理权限！")]))
            ifkick = 0

        memlist = await app.memberList(group)
        msc = MessageChain.create([])
        kick_list = []
        cnt = 0  # 群名片有问题的人数

        for mem in memlist:
            if mem.permission != MemberPerm.Member:
                continue
            if not name_match(mem.name):
                if ifkick == 0:
                    msc.plus(MessageChain.create([At(mem.id)]))
                    cnt += 1
                else:
                    kick_list.append(mem)

        if ifkick == 0:
            if cnt < 1:
                await app.sendGroupMessage(group, MessageChain.create([Plain("perfect!")]))
                return
            msc.plus(MessageChain.create([Plain(" 请以上同学尽快改正群名片哦！")]))
            await app.sendGroupMessage(group, msc)
        elif ifkick == 1:
            if len(kick_list) != 0:
                ms = MessageChain.create([])
                for mem in kick_list:
                    if mem == kick_list[0]:
                        ms.plus(MessageChain.create([Plain(mem.name), Plain(","), Plain(mem.id)]))
                    else:
                        ms.plus(MessageChain.create([Plain("\n"), Plain(mem.name), Plain(","), Plain(mem.id)]))
                    await app.kick(group, mem)

                await app.sendGroupMessage(group, ms)
                await app.sendGroupMessage(group, MessageChain.create([Plain("本次完成清理%d人!" % len(kick_list))]))


class_list = ["计科", "信安", "大数据", "软工", "自动化", "光电", "微电子", "计拔", "通信", "测绘"]
for i in range(1, 30):
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
        # print(tmp)
        if len(tmp[0]) != 7 or (tmp[1] not in class_list):
            return False
        return True


'''
        # crawler
        path = 'F:/anaconda3/chromedriver.exe'
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        browser = webdriver.Chrome()

        browser.get("https://qun.qq.com/member.html#gid=" + str(group.id))
        sleep(20)

        all_number_name = browser.find_elements_by_xpath('//*[@class="list"]/tr/td[4]/span[1]')
        all_number_qq = browser.find_elements_by_xpath('//*[@class="list"]/tr/td[5]')

        li = []
        err = []
        print(len(all_number_qq))
        for k in range(len(all_number_qq)):
            li.append([])
            li[k].append(all_number_qq[k].text)
            li[k].append(all_number_name[k].text)
            if int(all_number_qq[k].text) not in register_list["bot"] \
                    and int(all_number_qq[k].text) not in register_list["teacher"]:
                ss = all_number_name[k].text
                if ss == "":
                    err.append(all_number_qq[k].text)
                    continue

                if ss.count("-") != 2:
                    err.append(all_number_qq[k].text)
                    continue

                tmp = ss.split("-")
                if len(tmp[0]) != 7 or (tmp[1] not in class_list):
                    err.append(all_number_qq[k].text)
                    continue

        print(err)
'''
