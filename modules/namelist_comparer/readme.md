# namelist_comparer

```python
# 插件信息
__name__ = "cmp_namelist"
__description__ = "比较现有群成员和名单信息"
__author__ = "hxb"
__usage__ = "输入 对照名单"
```

比较群成员和班级名单，找出“未加群同学”和“未在名单的同学”，并在聊天框输出



#### `config.json` ——本插件的配置文档

```json
`{`

 `"filename": "namelist_demo.xls",`

 `"sheet": 0,`

 `"ask": [`

  `"bot cmp_namelist",`

  `"对照名单"`

 `],`

 `"major": ["计科", "信安", "大数据", "软工", "自动化", "光电", "计拔", "测绘", "微电子", "通信"],`

 `"class_num": 31`

`}`
```

`filename 班级成员名单`

用自己高程班名单放到此目录下，并修改`config.json`中`filename`与文件名对应（现有的`namelist_demo.xls`为2021三班名单）

`sheet` 默认为0，对应`Sheet1`

`ask` 触发语句

`major和class_num` 专业和班级号



#### `registers.json` ——简单的权限管理

将自己的QQ号添加到admin下面





【对于群名片不合规的成员，不进行统计，请先保证群成员名片已符合要求】











