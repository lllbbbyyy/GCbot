# c++ Compiler 模块
用于在线编译c++代码，支持有标准输入输出及错误提示，使用在线编api：**https://wandbox.org/api/compile.json**

### 在 config.json 中设置接口信息、权限设置、在线编译器选项、输入 c++ help时、c++ eg的提示语、群号黑名单、关键词信息

    {
    "allow_use": true,
    "url" : "https://wandbox.org/api/compile.json",
    "black_list": [],
    "key_word": ["c++","c++ help","c++ eg"],
    "help_tip":"\n用g++12标准进行编译并显示输出结果\n---------\n使用格式：\nc++\nxxxx(待编译程序)\n// StdInput xxxx\n---------\n(如有输入，在程序中间或尾部加上注释，在StdInput后给出\n关键词：StdInput)\n发送c++ eg查看例子",
    "c++_eg":"\nc++\n#include<iostream>\nusing namespace std;\n int main(){\n    int yxx=0;\n    for(int i=0;i<2;i++){\n       cin>>yxx;\n        cout<<yxx<<endl;\n    }\n    return 0;\n}\n// StdInput 43 37",
    "data_options": "warning,gnu++1y",
    "data_compiler": "gcc-head",
    "data_compiler-option-raw": "-Dx=hogefuga\n-O3",
    "data_Content-Type": "application/json"
}

其中：

`allow_use` 表示是否允许使用该功能。

`url` 负责存储云接口信息。

`black_list` 表示禁用该功能的群。

`key_word` 表示触发关键词，

其中，`c++ help `用于提示触发规则，包括格式及输入输出，`c++ eg`用于触发消息例子，以供参考

`data_xxx`为编译器选项

## 注意
因为输入为正则表达式`r"//\s?StdInput\s?([\w\s]+)\n?"`,故建议在代码注释中避免例如 `// Stdinput xxx`

## 触发格式类似于
>c++
>
>xxxxxx 
>
>// StdInput xx xx

若所c++ 功能有效触发，则以类似

>@xxx
>
>编译成功，输出为
>
>xxxxx

如果编译错误，则输出为：

>@xxx
>
>编译错啦，仔细检查哦
>
>xxxxx（错误信息）

如果发送消息行数较多，采取截取20行，避免刷屏;如果行数过多或死循环导致在线编译错误，无任何输出