from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

# 插件信息
__name__ = "mute_revoker"
__description__ = "禁言撤回者"
__author__ = "da-qing-wa"
__usage__ = "自动触发x"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


# last_msg = {}  # 用于维护每个群最后一句话

# 禁言撤回者
@channel.use(ListenerSchema(listening_events=[GroupRecallEvent]))
async def mute_revoker(app: GraiaMiraiApplication, event: GroupRecallEvent):
    await app.sendGroupMessage(event.group, MessageChain.create([At(event.operator.id), Plain(" 不要撤回噢!")]))
    # last_msg[event.group.name] = MessageChain.create([Plain("@"), Plain(event.operator.name), Plain(" 不要撤回噢!")]).asDisplay()
    if event.operator.permission == event.operator.permission.Member:
        await app.mute(event.group, event.operator, 1 * 10)
