from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain, At
from graia.application.entry import Friend, Group, Member, BotOnlineEvent

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEYDYHZYISn",  # 填入 authKey
        account=1234567,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    ))


@bcc.receiver("GroupMessage")
async def friend_message_listener(app: GraiaMiraiApplication, group: Group,
                                  message: MessageChain, member: Member):
    if message.asDisplay() == '还活着':

        await app.sendGroupMessage(group, MessageChain.create([Plain("死了")]))


app.launch_blocking()
