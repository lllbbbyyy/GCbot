import json
import os

from graia.application.event.mirai import GroupRecallEvent
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application.entry import Group, GroupMessage, Plain, MessageChain, GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, At, Image
from graia.application.group import Group, Member, MemberPerm
from graia.template import Template

from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication
from graia.application.event.mirai import GroupRecallEvent
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.exceptions import AccountMuted, UnknownTarget
from graia.application.message.elements.internal import MessageChain, Plain, Image, FlashImage, Xml, Json, Voice

# 插件信息
__name__ = "mute_for_recall"
__description__ = "禁言撤回消息者"
__author__ = "胡孝博"
__usage__ = "禁言撤回消息者--默认为开启状态"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    config_info = json.load(f)

root = os.path.join(os.getcwd(), "registers.json")
with open(root, encoding='utf-8') as fp:
    register_list = json.load(fp)


@channel.use(ListenerSchema(listening_events=[GroupRecallEvent]))
async def mute_for_recall(app: GraiaMiraiApplication, events: GroupRecallEvent, group: Group, member: Member):
    if config_info["switch"]:
        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(" 群消息不许撤回嗷~下次注意哈")]))
        if group.accountPerm == MemberPerm.Administrator and member.permission == MemberPerm.Member:
            await app.mute(group, member, 60)
