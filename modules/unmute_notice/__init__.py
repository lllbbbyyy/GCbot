from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

# 插件信息
__name__ = "unmute_notice"
__description__ = "解除禁言的提示"
__author__ = "da-qing-wa"
__usage__ = "自动触发"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


# last_msg = {}  # 用于维护每个群最后一句话

# 解除禁言
@channel.use(ListenerSchema(listening_events=[MemberUnmuteEvent]))
async def unmute_notice(app: GraiaMiraiApplication, group: Group, member: Member = "target"):
    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(" 放出来了，下次不要再犯噢！")]))
    # last_msg[group.name] = MessageChain.create([Plain("@"), Plain(member.name), Plain(" 放出来了，下次不要再犯噢！")]).asDisplay()
