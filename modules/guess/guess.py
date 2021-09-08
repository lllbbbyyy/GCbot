import os
import json
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent


# 插件信息
__name__ = "guess"
__description__ = "猜测首字母缩写的含义"
__author__ = "da-qing-wa"
__usage__ = "在群内发送guess xxx"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

last_msg = {}  # 用于维护每个群最后一句话


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    str = ""
    flag = 0
    if message.asDisplay() == '小青蛙':
        str += "呱呱呱"
        flag = 1
    elif message.asDisplay() == '蚊子':
        str += "[mirai:face:2]"
        flag = 1
    elif message.asDisplay() == '别骂了' or message.asDisplay() == '爬了':
        str += "[mirai:face:107]"
        flag = 1
    elif message.asDisplay() == '渣哥':
        str += "哪个娃叫我[mirai:face:271]"
        flag = 1
    elif message.asDisplay() == '小坚果很委屈':
        str += "是呢[mirai:face:111]"
        flag = 1
    elif message.asDisplay() == '快睡觉':
        str += "别熬夜啦，跟我一起冬眠叭😪"
        flag = 1
    elif message.asDisplay().startswith('呱'):
        str += "不许抢我台词！呱！"
        flag = 1
    elif message.asDisplay().startswith("孤寡"):
        str += "不许孤寡"
        flag = 1
    if flag:
        await app.sendGroupMessage(group, MessageChain.fromSerializationString(str))
        last_msg[group.name] = str

"""
@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, target: Friend, message: MessageChain):
    if message.asDisplay() == '小青蛙':
        await app.sendFriendMessage(target, MessageChain.create([Plain("呱呱呱")]))
    elif message.asDisplay() == '小青蛙很委屈':
        await app.sendFriendMessage(target, MessageChain.fromSerializationString("[mirai:face:111]"))
"""

major_lst = ["计科", "软工", "测绘", "通信", "信安", "大数据", "微电子", "信01", "信02", "信03", "信04", "信05", "信06", "信07",
             "信08", "信09", "信10", "信11", "信12", "信13", "信14", "信15", "信16", "信17", "信18", "信19", "信20", "信21",
             "计拔"]


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_member_name_corrector_whole(app: GraiaMiraiApplication, group: Group,
                                            message: MessageChain, member: Member):
    if message.asDisplay() == '群名片格式 总' \
            and (member.permission == member.permission.Administrator
                 or member.permission == member.permission.Owner or member.id == 2654676573):
        mystr = MessageChain.create([Plain("")])
        mylst = await app.memberList(group)
        for stu in mylst:
            if stu.name == "沈坚" or stu.name == "陈宇飞" or stu.name == "233" or stu.name == "小坚果" \
                    or stu.name == "RookieBot":
                continue
            elif stu.name.count('-') != 2:
                mystr.plus(MessageChain.create([At(stu.id), Plain("\n")]))
            else:
                str_lst = stu.name.split('-')
                if len(str_lst[0]) != 7:
                    mystr.plus(MessageChain.create([At(stu.id), Plain("\n")]))
                elif str_lst[1] not in major_lst:
                    mystr.plus(MessageChain.create([At(stu.id), Plain("\n")]))
        mystr.plus(MessageChain.create([Plain(" 请尽快修改群名片格式哦!")]))
        await app.sendGroupMessage(group, mystr)
        last_msg[group.name] = mystr.asDisplay()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def kick_group_member(app: GraiaMiraiApplication, group: Group,
                            message: MessageChain, member: Member):
    if message.asDisplay() == '开踢' \
            and (member.permission == member.permission.Administrator
                 or member.permission == member.permission.Owner or member.id == 2654676573):
        mylst = await app.memberList(group)
        for stu in mylst:
            if stu.name == "沈坚" or stu.name == "陈宇飞" or stu.name == "233" or stu.name == "小坚果" \
                    or stu.name == "RookieBot":
                continue
            elif stu.name.count('-') != 2:
                await app.sendGroupMessage(group, MessageChain.create([At(stu.id), Plain(" 被踢出")]))
                if stu.permission == stu.permission.Member:
                    await app.kick(group, stu)
            else:
                str_lst = stu.name.split('-')
                if len(str_lst[0]) != 7:
                    await app.sendGroupMessage(group, MessageChain.create([At(stu.id), Plain(" 被踢出")]))
                    if stu.permission == stu.permission.Member:
                        await app.kick(group, stu)
                elif str_lst[1] not in major_lst:
                    await app.sendGroupMessage(group, MessageChain.create([At(stu.id), Plain(" 被踢出")]))
                    if stu.permission == stu.permission.Member:
                        await app.kick(group, stu)


# 禁言复读者
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def mute_echoer(app: GraiaMiraiApplication, group: Group,
                      message: MessageChain, member: Member):
    tmp = message.asSerializationString()
    msg = ""
    for i in range(len(tmp)):
        if tmp[i] == ']':
            msg = tmp[i + 1:]
            break
    # print(msg)
    if group.name in last_msg:
        if msg == last_msg[group.name]:
            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(" 不要复读噢!")]))
            last_msg[group.name] = MessageChain.create(
                [Plain("@"), Plain(member.name), Plain(" 不要复读噢!")]).asDisplay()
            if member.permission == member.permission.Member:
                await app.mute(group, member, 1 * 10)
        else:
            last_msg[group.name] = msg
    else:
        last_msg[group.name] = msg


# 禁言撤回者
@channel.use(ListenerSchema(listening_events=[GroupRecallEvent]))
async def mute_revoker(app: GraiaMiraiApplication, event: GroupRecallEvent):
    await app.sendGroupMessage(event.group, MessageChain.create([At(event.operator.id), Plain(" 不要撤回噢!")]))
    last_msg[event.group.name] = MessageChain.create(
        [Plain("@"), Plain(event.operator.name), Plain(" 不要撤回噢!")]).asDisplay()
    if event.operator.permission == event.operator.permission.Member:
        await app.mute(event.group, event.operator, 1 * 10)


# 解除禁言
@channel.use(ListenerSchema(listening_events=[MemberUnmuteEvent]))
async def unmute_notice(app: GraiaMiraiApplication, group: Group, member: Member = "target"):
    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(" 放出来了")]))
    last_msg[group.name] = MessageChain.create(
        [Plain("@"), Plain(member.name), Plain(" 放出来了")]).asDisplay()

"""
import requests

TEST_GROUP_LIST = [789651380, 939474354, 481527396, 1087728587]
url = "https://lab.magiconch.com/api/nbnhhsh/guess"
data = {}


# guess
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def guess(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith("guess"):
        #  and group.id in TEST_GROUP_LIST:
        data["text"] = message.asDisplay()[6:]
        resp = requests.post(url=url, data=data)
        json = resp.json()
        str = ""
        if not json:
            str += "找不到噢,试试别的叭！"
        elif "trans" not in json[0]:
            if not json[0]["inputting"]:
                str += "找不到噢,试试别的叭！"
            else:
                str += message.asDisplay()[6:] + "可能是" + "\n" + json[0]["inputting"][0]
        else:
            str += message.asDisplay()[6:] + "可能是"
            for i in json[0]["trans"]:
                str += '\n' + i
        await app.sendGroupMessage(group, MessageChain.create([Plain(str)]))
        last_msg[group.name] = str
"""
"""
# chat
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def chat(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg="
    if message.asDisplay().startswith("chat"):
        url += message.asDisplay()[5:]
        res = requests.get(url)
        resp = res.json()["content"]
        await app.sendGroupMessage(group, MessageChain.create([Plain(resp)]))
"""
