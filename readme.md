# 坎公骑冠剑——超级骑士报表

* 想知道自己总共出了多少刀？
* 想知道自己是哪天忘记了出刀？
* 想看看是哪个群友天天在抢将军？
* 会长想鲨人却不知道该鲨谁？

为了解决bigfun接口缺乏统计功能的问题，特推出开箱即用的会战报表系统！

只需要双击一下，就可以生成详细的会战报表，方便大家详细了解自己的总出刀数、对各个boss出刀数、缺刀日期等数据。

[TOC]

## 准备工作

* 依赖Windows系统和Edge浏览器（macOS/Linux上的Edge理论上也行，但咱懒得测试了）
* 如果需要从源码运行，除上述需求以外，需要准备`Python`环境并安装`browser-cookies3`包
* 如果需要从源码打包，除上述需求以外，还需要安装`pyinstaller`包

## 如何运行

有三种方法可以使用到本程序功能：

### 直接运行

从release中下载可执行文件`KnightReport.exe`，双击运行

### 从源码运行

执行以下命令

```
mkdir tmp
cd tmp
python ../src/main.py
```

### 从源码打包

下载源码后，运行`build.ps1`进行打包，可执行文件将会在当前目录下的`tmp/dist/KnightReport.exe`

## 使用方法

1. 程序会启动bigfun的登录界面，如果是未登录状态，点击**bilibili账号登录**开始正常登录流程
2. 确认登陆完成后，**可以关闭网页**，等待程序结束
3. 如果已经是登陆状态，**可以直接关闭网页**

日志将会生成在当前目录下的`KnightReport.log`

错误信息将会生成在当前目录下的`KnightReport.err`

会战报表将会生成在当前目录下的`report.csv`

## 数据描述

报表中有以下数据：

| 题头           | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| uid            | 玩家uid                                                      |
| 玩家           | 玩家用户名                                                   |
| 出刀           | 本次会战期间玩家总出刀次数                                   |
| 伤害           | 本次会战期间玩家总造成伤害                                   |
| XXX出刀        | 本次会战期间玩家对XXX（boss名）出刀次数                      |
| XXX伤害        | 本次会战期间玩家对XXX（boss名）造成伤害                      |
| YYYY-MM-DD漏刀 | 玩家在YYYY-MM-DD（日期）漏刀次数（-1为本日只出了2刀，-2为本日只出了一刀，-3为本日未出刀，无漏刀不显示） |

## 使用到的接口

为方便二次开发，特提供可用的WEB API

定义在`constants.py`中：

```python
# 用于人工介入的用户登录
# web API for user login
LoginURL = 'https://www.bigfun.cn/tools/gt/'

# 用于读取公会成员数据和会战日期区间
# web API for guild status
GuildStatusURL = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log-filter%2Fa"

# 用于读取每日会战数据（需要日期参数）
# web API for combat status(need argument date)
DateStatusURL = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report%2Fa&date={:s}"
```

## 平台测试

已经在以下平台上测试通过

| program         | version        |
| --------------- | -------------- |
| Windows         | 10(19042.1110) |
| Python          | 3.9.4          |
| browser-cookies | 0.12.1         |
| pyinstaller     | 4.5.1          |

## 特别鸣谢

[bigfun](https://www.bigfun.cn/)的[坎公百宝袋](https://www.bigfun.cn/tools/gt/)提供了全部API支持

[browser-cookies](https://github.com/borisbabic/browser_cookie3)提供了获得本地浏览器cookies的方案



