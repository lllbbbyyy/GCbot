# guess模块
用于猜测首字母缩写的含义，调用了**requests**库

### 在 config.json 中设置首字母缩写接口信息与权限设置：

    {
        "allow_use": true,
        "cloud_api": {
            "api": "https://lab.magiconch.com/api/nbnhhsh/guess",
            "str_key": "text"
        },
        "black_list": [642362943],
        "key_word": "guess ",
        "substr_start_pos": 6
    }

其中：

`allow_use` 表示是否允许使用该功能。

`cloud_api` 负责存储云接口信息。

其中，`api` 表示接口地址，`str_key` 表示传入参数键。使用 **POST** 请求完成查询。

`black_list` 表示禁用该功能的群。

`key_word` 表示触发关键词，暂定为`guess `

`substr_start_pos` 表示从所收到消息的哪个位置开始截取，其值随`key_word`而改变。

若所guess的首字母缩写有效，则以类似

> yyds可能是
> 
> 永远滴神
> 
> 音乐大师
> 
> 以一当十
> 
> 阴阳大师
> 
> 永远单身
> 
> 游刃有余(日语)
> 
> 硬硬的说
> 
> 永远都是

的形式呈现结果，若搜索结果无效，则提示`找不到噢,试试别的叭！`
