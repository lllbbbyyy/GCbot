# GCbot
高级语言程序设计课程用机器人



## 说明

该项目主要负责构建QQ机器人，从而帮忙完成同济大学高级语言程序设计课程群的管理工作，仅供学习用途。

该项目基于QQ机器人库[`mirai`](https://github.com/mamoe/mirai)以及配套的python sdk库[`graia`](https://github.com/GraiaProject/Application)开发。



## 涉及到的相关项目

- [`mirai`](https://github.com/mamoe/mirai):一个在全平台下运行，提供 QQ Android 协议支持的高效率机器人库
- [`mirai-console`](https://github.com/mamoe/mirai-console):一个基于mirai开发的插件式可扩展开发平台
- [`mirai-api-http`]():提供与mirai交互方式的mirai-console插件
- [`graia-application`](https://github.com/GraiaProject/Application):提供python sdk以便进行机器人开发
- [`mirai-console-loader`](https://github.com/iTXTech/mirai-console-loader):模块化、轻量级且支持完全自定义的mirai加载器
- [`saya_plugins_collection`](https://github.com/SAGIRI-kawaii/saya_plugins_collection):一个Graia-Saya的插件仓库



## 安装与配置

环境的配置请参考`docs/环境基本配置.md`



## 贡献说明

**注意你的所有文件都应该使用UTF-8编码**

本项目使用Saya插件化的方法进行组织，即将自己完成的功能封装为一个插件，供main函数调用使用，插件将会统一存放在`modules`文件夹下，以供`main.py`调用

插件可以是单独的文件形式，亦可是包的形式（多文件情况下）

整个项目的结构与相关插件的实现方法可以参考[`saya_plugins_collection`](https://github.com/SAGIRI-kawaii/saya_plugins_collection)

目前插件库中给出了一个check_alive插件的实现过程，以供参考

注意给出的插件最好应当给予相应的`readme.md`文件，以说明插件的功能与用法，因此基本上推荐以文件夹（包）的形式给出

注意你的插件不应该对其他插件造成影响，并且应该注意**python模块被调用时的相对路径文件**

如果你觉得某些功能很有泛用性，可以提炼出相应的模块放置在`utils`文件夹下

请通过提交Pr的形式进行贡献



## 其他说明

### config.json文件说明

注意根目录下的`config.json`文件是被添加在`.gitignore`文件中，不会被上传的，因此下载本项目后应该首先自行新建该文件，并且进行相关配置后才可运行

`config.json`文件需与`main.py`文件同级

`config.json`文件的结构与配置说明如下：

```json
{
	"host":str形式的主机，例："http://localhost:8080",
	"auth-key":str形式的认证串,
	"bot-qq":num形式的qq号
}
```



## 开源许可证

我们使用 [`GNU GPLv3`](https://choosealicense.com/licenses/gpl-3.0/) 作为本项目的开源许可证

