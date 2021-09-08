from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, Face
from graia.application.entry import Friend, Group, Member, FriendMessage, GroupMessage, GroupRecallEvent, \
    MemberMuteEvent, At, MemberUnmuteEvent

# 插件信息
__name__ = "certain_reply"
__description__ = "一些特定的回复"
__author__ = "da-qing-wa"
__usage__ = "在群内发送对应关键词"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


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
        #last_msg[group.name] = str
