# explicit_detector
用于检测文本中是否存在敏感词，在检测到敏感词后@该用户，并做出提醒。

### 在 config.json 中设置脏话词库信息：

    {
        "should_use_local_exp_list": false,
	    "local_exp_list_dir": "/exp_list.json",
        "cloud_api": {
            "api": "https://www.yourserver.com/yourloc/api/yourapi.php",
            "str_key": "str"
        }
    }

其中：

`should_use_local_exp_list` 表示是否使用本地脏话词库。

`local_exp_list_dir` 表示如果使用本地词库，词库的文件地址位置。（假设为 **/exp_list.json**）

`cloud_api` 负责存储云接口信息。

其中，`api` 表示接口地址，`str_key` 表示传入参数键。使用 **Get** 请求完成查询。返回值以 **1** 和 **0** 表示是否检测到脏话。

## 模块依赖于两个json文件，存储相关信息。

### exp_list.json 负责存储敏感词列表：

    {
        "data": [
            "脏话1",
            "脏话2",
            ...
        ]
    }

### warning_words_list.json 负责存储检测到敏感词后，提醒用户的语句：

    [
        "不许说脏话",
        "说脏话不好",
        ...
    ]

当检测到某条**群消息**中存在 `exp_list.json` 中的内容时，会发送一条提示消息。该消息先@该成员，然后从 `warning_words_list.json` 中随机抽取一条发送。