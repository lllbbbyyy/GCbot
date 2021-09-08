from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

# 插件信息
__name__ = "kick_group_member"
__description__ = "踢掉群名片格式不对的人"
__author__ = "da-qing-wa"
__usage__ = "在群内发送 开踢 即可触发"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


# last_msg = {}  # 用于维护每个群最后一句话

major_lst = ["计科", "软工", "测绘", "通信", "信安", "大数据", "微电子", "信01", "信02", "信03", "信04", "信05", "信06", "信07",
             "信08", "信09", "信10", "信11", "信12", "信13", "信14", "信15", "信16", "信17", "信18", "信19", "信20", "信21",
             "计拔"]
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
