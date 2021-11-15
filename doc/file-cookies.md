# 从文件输入cookies

## 注意事项

该方法属于实验性功能，目前没有大量的使用反馈，建议仅在自动获取cookies失败时，再去尝试这种方案。

## 工作原理

程序在发现当前路径下有`cookies.txt`文件时，不会尝试启动浏览器，而是直接从文件中读取cookies用于用户登录

## 使用方法

1. 打开你的浏览器，什么浏览器都可以，打开链接`https://www.bigfun.cn/tools/gt/`
2. 点击`bilibili账号登录`完成登录
3. 打开`浏览器开发调试工具`，常见的方法有`右键->检查/inspect`或者`F12`，如果都不行请搜索`浏览器名+开发调试工具`
4. 点击`控制台`或`console`选项卡
5. 在光标内输入`document.cookie`，回车
6. 在下载好的可执行文件`KnightReport-win.exe`或`KnightReport-mac`同路径下，创建文本文件`cookies.txt`
7. 将第5步得到的结果复制到`cookies.txt`，保存
8. 正常双击启动`KnightReport-win.exe`或`KnightReport-mac`

## 场景演示

一般情况下，进行1-5步之后，你能得到类似这样的结果

```
> document.cookie
<·'fingerprint=4f452ffbb7hf5byu6993fc1adbf9df93; b_nut=9636342652; sid=ruyemt40; UM_distinctid=17b3fc5fa72b82-05d8125731163a-4343363-fa000-1127f83fc7b5f3; DedeUserID=1044228; DedeUserID__ckMd5=04e2541cb090de43; user-info=4281958; _csrf=5lWE650HJNscrc049hQUxBBZ; CNZZDATA1275376637=6313191361-1657828504-%7181C6369463; bili_jct=cbed0d842debf557a9b913228d134167; session-api=ofiqb6066nfsp5dcpr61rnkrp0'
```

这种情况下，可以拷贝

```
'fingerprint=4f452ffbb7hf5byu6993fc1adbf9df93; b_nut=9636342652; sid=ruyemt40; UM_distinctid=17b3fc5fa72b82-05d8125731163a-4343363-fa000-1127f83fc7b5f3; DedeUserID=1044228; DedeUserID__ckMd5=04e2541cb090de43; user-info=4281958; _csrf=5lWE650HJNscrc049hQUxBBZ; CNZZDATA1275376637=6313191361-1657828504-%7181C6369463; bili_jct=cbed0d842debf557a9b913228d134167; session-api=ofiqb6066nfsp5dcpr61rnkrp0'
```

到文件cookies.txt，双击启动`KnightReport-win.exe`。

如果此时没有尝试启动浏览器，打开日志`KnightReport.log`，显示

```
当前路径下发现cookies.txt，尝试从文件中获得cookies
```

说明cookies已经从文件输入。