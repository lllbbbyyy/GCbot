import json
import os
import difflib

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
__name__ = "mute_for_repeat"
__description__ = "禁言复读者"
__author__ = "胡孝博"
__usage__ = "禁言复读者--默认为开启状态"

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

msg_list = {"926594031": []}


def string_similar(s1, s2, s3):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio() * difflib.SequenceMatcher(None, s2, s3).quick_ratio()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def mute_for_repeat(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    if config_info["switch"]:
        msg = message.asDisplay()

        if msg == "[表情]":
            return

        if msg_list.get(str(group.id)) == None:
            msg_list[str(group.id)] = []

        msg_list[str(group.id)].append(msg)

        # 判断标准 两句完全一样 / 连着三句相似度高于75
        if len(msg_list[str(group.id)]) > 1 and msg_list[str(group.id)][-2] == msg_list[str(group.id)][-1] \
                or len(msg_list[str(group.id)]) > 2 and string_similar(msg_list[str(group.id)][-3],
                                                                       msg_list[str(group.id)][-2],
                                                                       msg_list[str(group.id)][-1]) > 0.75:

            msc = MessageChain.create([])
            msc.plus(MessageChain.create([At(member.id), Plain(" 不要复读嗷!\n")]))
            #print("6666")
            current_path = os.path.dirname(__file__)
            with open(current_path + '/repeater.json', 'r', encoding='utf-8') as f:
                repeater_info = json.load(f)

            if repeater_info.get(str(group.id)) == None:
                repeater_info[str(group.id)] = []
            repeater_info[str(group.id)].append(member.id)

            cnt = repeater_info[str(group.id)].count(int(member.id))

            if cnt == 1:
                msc.plus(MessageChain.create([Plain("这是你首次复读 下次注意啦")]))
            else:
                msc.plus(MessageChain.create([Plain("这是你在本群第%d次复读 将被禁言%d小时" % (cnt, (8 * (cnt - 1))))]))

            with open(current_path + '/repeater.json', 'w', encoding='utf-8') as fp:
                fp.write(json.dumps(repeater_info, sort_keys=True, indent=4, separators=(',', ': ')))

            await app.sendGroupMessage(group, msc)
            msg_list[str(group.id)].append(msc.to_string())
            if group.accountPerm == MemberPerm.Administrator and member.permission == MemberPerm.Member:
                await app.mute(group, member, (8 * (cnt - 1)) * 3600)


