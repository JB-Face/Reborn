<!--
 * @Descripttion: 
 * @version: 
 * @Author: JBFace
 * @Date: 2022-05-11 23:30:22
 * @LastEditors: JBFace
 * @LastEditTime: 2022-05-11 23:40:53
-->
# 一个模仿ugs写的git gui

初衷在于美术同学不怎么会用 git，而现在的gitgui过于复杂。所以这个工具只有以下几个功能

1. 拉取确定分支的内容
2.可视化提交记录并可以更新到提交
3.更新完成或者用户自己可以打开设定好的入口文件
4.几个便捷功能和icon支持

# 使用场景
一个工具、软件、库等内容，由维护者托管到git的某个分支
使用者需要较多较为及时的更新，以用来使用、测试等

此时，可以使用这个软件，再配置ssh或者登录服务器的前置配置下，直接修改setting下的 json文件完成设置。
维护者可以直接发送json文件给使用者，然后更新之即可使用

维护者可以再更新后自动 或者 手动打开入口文件。可以是exe、python、甚至一个 书签、一个readme

# setting 配置说明

```
{
    "url":"git@github.com:JB-Face/javascript30day.git",# 托管地址
    "path":".\\test2",# 本地路径
    "workspace":"te22222",# 工作区名字
    "branch":"main",# 分支
    "callback":"123.bat"# 入口

}
```

a.json的icon 为 a.png


# 开发计划

- 支持拉取最新的readerme 作为公告
- 尝试支持p4v
- 多线程处理qt去除黑框框
- 添加 issus 入口
- 可视化 可文字化复制传输的 配置

1242
