# check_name_format

用于检测高程群群名片

参考配置文件config.json中的配置内容：

```json
{
    "ask" : "检查群名片",
    "top-prompt" : "请修改群名片:",
    "bottom-prompt" : "",
    "white-list" : [278787983],
    "stu-years" : "(17|18|19|20|21)",
    "class-num" : 21,
    "major-list" : ["计拔", "计科", "软工", "信安", "大数据", "通信", "微电子", "测绘"]
}
```

字符串`ask`表示检测的询问语句
字符串`top-prompt`表示机器人发出的消息的头部提示信息
字符串`bottom-prompt`表示机器人发出的消息的底部提示信息
列表`white-list`表示白名单人员的qq号，机器人不对其进行检查
字符串`stu-years`表示群内合法学号的开头两位，格式为"(xx|..|xx)"，方便偷懒
字符串`class-num`表示本届信息类班级个数
字符串`major-list`表示转专业补课同学都来自哪些专业

当在**群聊**中出现`ask`语句时，机器人回复信息格式如下:

top-prompt

@stu1

@stu2

...

bot-prompt