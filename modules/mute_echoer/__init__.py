from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

# 插件信息
__name__ = "mute_echoer"
__description__ = "禁言复读者"
__author__ = "da-qing-wa"
__usage__ = "自动触发"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


last_msg = {}  # 用于维护每个群最后一句话

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
            last_msg[group.name] = MessageChain.create([Plain("@"), Plain(member.name), Plain(" 不要复读噢!")]).asDisplay()
            if member.permission == member.permission.Member:
                await app.mute(group, member, 1 * 10)
        else:
            last_msg[group.name] = msg
    else:
        last_msg[group.name] = msg

