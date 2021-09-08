# recall_detector
撤回检测，并适当进行提示或禁言。

配置文件 config.json 中存储该模块所需的规则等信息：

    {
        "default_strategy": {
            "ignore_members": [
                2000
            ],
            "should_warn": true,
            "should_mute": true,
            "warning_words": [
                "不要撤回啊..",
                "don't recall your message.."
            ],
            "should_count": true,
            "should_warn_with_count": true,
            "mute_time_sec": 360
        },

        "group_enabled": {
            "100000": {
                "should_use_default_strategy": false,

                "strategy": {
                    "ignore_members": [
                
                    ],
                    "should_warn": true,
                    "should_mute": true,
                    "warning_words": [
                        "不要在这个群里撤回啊..",
                    ],
                    "should_count": true,
                    "should_warn_with_count": true,
                    "mute_time_sec": 5
                }
            },
            
            "762572821": {
                "should_use_default_strategy": true
            }
        }
    }

`default_strategy` 存储默认处理方式。

应将需要启用本插件的群号作为键值添加到 `group_enabled` 中，内容为一个 **json_object** ，记录策略等信息。如果 `should_use_default_strategy` 内容为 true，则当该群出现撤回情况时，加载默认策略。

user_record.json 负责记录用户复读次数。可以不创建。

    {
        "2000": {
            "100000": 1,
            "100001": 2,
            ...
        },
        "2001": {
            ...
        }
    }

其中，`2000` 为用户的**QQ号**，`100000` 为**群号**。