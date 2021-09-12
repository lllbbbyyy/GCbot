# Bullshit_Generator

用于产生一篇以用户输入文本为主题的狗屁不通的文章

参考配置文件config.json中的配置内容：

```json
{
    "allow_use": true,
    "key_word":"Bullshit",
    "text_length":200,
    "content_start_pos":8,
    "black_list":[939474354,761222195]
}
```

对于策略的说明：

字符串`allow_use`表示是否启用狗屁不通文章生成器
字符串`key_word`表示触发该插件的关键词
数字`text_length`表示生成文章的大概长度，程序在达到200字之后会自动停止生成
数字`content_start_pos`表示开始截取文章标题的位置，该数字随着`key_word`的改变而改变
列表`black_list`表示不使用的群，防止在重要的群当中掩埋掉重要消息

该插件可以使用help语句来显示用法，语句为`Bullshit -help`