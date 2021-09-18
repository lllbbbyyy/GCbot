# self_mute模块

用于群成员自主进行禁言。

### 参考配置文件config.json中的配置内容：

    {
        "default-strategy" :
        {
            "ask" : "我要禁言",
            "success-message" : "已禁言",
            "bot-no-permission-message" : "我没有禁言权限。",
            "target-not-member-message" : "你无法被我禁言。",
            "over-range-message" : "禁言时间过长，已禁言30天。"
        },
        "groups-enabled" :
        {
            "642362943" :
            {
                "use-default-strategy" : true
            },
            "748798035" :
            {
                "use-default-strategy" : false,
                "strategy" :
                {
                    "ask" : "我要自裁",
                    "success-message" : "满足你！",
                    "bot-no-permission-message" : "等我有了管理再来治你！",
                    "target-not-member-message" : "呜呜呜，我帮不了你。",
                    "over-range-message" : "这么久我怕世界把你忘了，满足你30天吧！"
                }
            }
        }
    }

### 关于策略的说明：

`default-strategy`记录默认处理策略

`group-enabled`记录启用该模块的群号

字符串`use-default-strategy`表示是否启用默认处理策略

字符串`ask`表示触发此模块的关键词

字符串`success-message`表示禁言成功时的提示消息

字符串`bot-no-permission-message`表示机器人无禁言权限时的提示消息

字符串`target-not-member-message`表示希望被禁言者为管理员或群主时的提示消息

字符串`over-range-message`表示禁言时间过长的提示消息

### 群内触发格式

> 字符串`ask` + `禁言时间`