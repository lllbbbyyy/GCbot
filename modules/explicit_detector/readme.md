# explicit_detector
用于检测文本中是否存在敏感词，在检测到敏感词后@该用户，并做出提醒。

模块依赖于两个json文件，存储相关信息。

exp_list.json 负责存储敏感词列表：

    {
        "data": [
            "脏话1",
            "脏话2",
            ...
        ]
    }

warning_words_list.json 负责存储检测到敏感词后，提醒用户的语句：

    [
        "不许说脏话",
        "说脏话不好",
        ...
    ]

当检测到某条**群消息**中存在 `exp_list.json` 中的内容时，会发送一条提示消息。该消息先@该成员，然后从 `warning_words_list.json` 中随机抽取一条发送。