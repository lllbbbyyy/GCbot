# check_name_format

用于检测高程群群名片

参考配置文件config.json中的配置内容：

```json
{
    "default-strategy" :
    {
        "ask" : "检查群名片",
        "top-prompt" : "请修改群名片:",
        "bottom-prompt" : "",
        "white-list" : [278787983],
        "stu-years" : "(17|18|19|20|21)",
        "class-num" : 21,
        "major-list" : ["计拔", "计科", "软工", "信安", "大数据", "通信", "微电子", "测绘"],
        "special-ch" : ["·"],
        "permission" : "Owner-Admin",
        "should-at" : true
    },
    
    "groups-enabled" :
    {
        "642362943" :
        {
            "use-default-strategy" : true
        },
        "123456789" :
        {
            "use-default-strategy" : false,
            "strategy" :
            {
                "ask" : "test",
                "top-prompt" : "测试用，不@人",
                "bottom-prompt" : "",
                "white-list" : [278787983],
                "stu-years" : "(17|18|19|20|21)",
                "class-num" : 21,
                "major-list" : ["计拔", "计科", "软工", "信安", "大数据", "通信", "微电子", "测绘"],
                "special-ch" : ["·"],
                "permission" : "All",
                "should-at" : false
            }
        }
    }
}
```

`default-strategy`记录默认处理方式

应将需要启用本插件的群号作为键值添加到`group-enabled`中，内容为一个 json_object ，记录策略等信息。如果 `use-default-strategy`内容为 true，则在该群加载默认策略。

对于策略的说明：

字符串`ask`表示检测的询问语句
字符串`top-prompt`表示机器人发出的消息的头部提示信息
字符串`bottom-prompt`表示机器人发出的消息的底部提示信息
列表`white-list`表示白名单人员的qq号，机器人不对其进行检查
字符串`stu-years`表示群内合法学号的开头两位，格式为"(xx|..|xx)"，方便偷懒
数`class-num`表示本届信息类班级个数
字符串`major-list`表示转专业补课同学都来自哪些专业
列表`special-ch`表示学生姓名中可能包含的特殊符号
字符串`permission`表示触发该插件功能所需要的权限，有三种：`Owner`, `Owner-Admin`, `All`
`should-at`表示发出信息时是否@群名片不正确的成员

当在**群聊**中出现`ask`语句时，机器人回复信息格式如下:

top-prompt

@stu1

@stu2

...

bot-prompt