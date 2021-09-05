import asyncio
import os
import json

from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

from graia.broadcast import Broadcast

from graia.application.entry import GraiaMiraiApplication, Session

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))

configs = {}
# 配置文件名一定是config.json
# 配置文件格式为：
# {
#     "host":str形式的主机，例："http://localhost:8080",
#     "auth-key":str形式的认证串,
#     "bot-qq":num形式的qq号
# }
current_path = os.path.dirname(__file__)
with open(current_path + '/config.json', 'r', encoding='utf-8') as f:
    configs = json.load(f)

app = GraiaMiraiApplication(broadcast=bcc,
                            connect_info=Session(host=configs["host"],
                                                 authKey=configs["auth-key"],
                                                 account=configs["bot-qq"],
                                                 websocket=True))

ignore = ["__init__.py", "__pycache__"]

with saya.module_context():
    for module in os.listdir("modules"):
        if module in ignore:
            continue
        try:
            if os.path.isdir(module):
                saya.require(f"modules.{module}")
            else:
                saya.require(f"modules.{module.split('.')[0]}")
        except ModuleNotFoundError:
            pass

app.launch_blocking()

try:
    loop.run_forever()
except KeyboardInterrupt:
    exit()