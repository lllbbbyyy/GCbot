# translation模块
用于词句的翻译，支持多种语言，调用了第三方库**googletrans(注意：版本为4.0.0rc1，如果用默认版本3.0.0会出错)**
，需要挂VPN

### 在 config.json 中设置接口信息、权限设置，及所支持的语言：

    {
      "allow_use": true,
      "url": "translate.google.cn",
      "black_list": [642362943],
      "key_word": ["trans to ","trans help"],
      "choice": {
        "ch":"中文",
        "en":"英语",
        "ja":"日语",
        "ko":"韩语",
        "fr":"法语",
        "de":"德语",
        "ru":"俄语",
        "es":"西班牙语",
        "pt":"葡萄牙语",
        "it":"意大利语",
        "vi":"越南语",
        "id":"印尼语",
        "ar":"阿拉伯语",
        "nl":"荷兰语"
      },
      "choice_len": 2
    }

其中：

`allow_use` 表示是否允许使用该功能。

`url` 负责存储云接口信息。

`black_list` 表示禁用该功能的群。

`key_word` 表示触发关键词，

其中，`trans to `是触发翻译功能的前缀，`trans help`用于提示触发规则

`choice`中是所支持翻译成的所有语言种类。

`choice_len`指所有`choice`的长度都是2

## 触发格式应该类似于 
>trans to en 你好 

若所trans to 功能有效触发，则以类似

> 翻译结果为：
> 
> Hello

的形式呈现结果，若格式错误或所要求的语言不支持，则提示`不支持这种语言噢，换一种试试叭！`
