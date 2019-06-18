<h1 align="center">Welcome to Panda-Sandbox(钟馗沙箱)</h1>
<p align="center">
  <img src="https://img.shields.io/badge/version-v0.1-blue.svg?cacheSeconds=2592000" />
  <img src="https://img.shields.io/badge/language-python3-blue.svg?cacheSeconds=2592000" />
  <img src="https://img.shields.io/badge/platform-macos-blue.svg?cacheSeconds=2592000" />
  <a href="http://www.gnu.org/licenses/gpl-3.0.html">
    <img alt="License: GPL" src="https://img.shields.io/badge/License-GPL-yellow.svg" target="_blank" />
  </a>
</p>

### 🏠 [个人小栈](https://ryuchen.github.io/)

  > 未来更新的说明会刊登在这里，并且会不定时分享部分内容和心得

### 📎 项目说明:
  > 目前Github社区中的开源沙箱系统，相较活跃的是 [cuckoosandbox](http://www.cuckoosandbox.org/)，但是这个项目在过去的一年中变得更新较为缓慢，后续也未见其进行卓越性的改进，逐渐走向闭源。
  > 鉴于此，这个项目将初期集成和兼容 cuckoo 的 [monitor](https://github.com/cuckoosandbox/monitor) 和 [community](https://github.com/cuckoosandbox/community)。
  > 这是一个基于已经初见成熟的 cuckoo 开源版本的沙箱的修订版本，但将进行彻底的重新构建，后续该版本将彻底重构，能够完全适配国内软件环境。


### 🔥 设计特性:

- 将收录和兼容 cuckoo 社区中的所有行为签名和检测手段。
- 采用新的方式重构任务调度和沙箱调度，提高整体的运行效率。
- 将集成开源情报，并将集成小型开源情报库在内，构建信誉体系。
- 合并 cuckoo 开源插件中的 android、linux、macos 平台检测。
- 重构 cuckoo 文件报告的展示效果，计划支持在 Web 界面制作虚拟机。
- 将采用全新的设计方式实现多节点的支持，实现高效的集群能力。
- 提供检测手段的算子化界面操作，支持在界面自定义文件检测流程和通过的检测手段。


### 👌 待办清单：
 * [x] 创建新的项目并创建第一次提交
 * [x] 迁移官方最新的 agent 脚本过来, 并将其改写为 Python3 的版本
 * [x] 测试改写后的 agent 脚本，使其功能可用
 * [x] 完成基本测试的 VMware Fusion Pro base on MacOS 的基本调用测试
 * [x] 构建 Readme.md
 
    * [x] 完成 Readme.md 文档的初步框架构建
    
 * [ ] 迁移官方 Guest.py 脚本过来，并将其改写为 Python3 的版本
 * [ ] 构建基本任务调度框架结构(celery)
 * [ ] 构建基本的虚拟机调用程序(VMWare Fusion Pro base on MacOS)
 
### 📖 安装说明:

```python

```

### 👤 作者介绍:

Ryuchen ( 陈 浩 )

* Github: [https://github.com/Ryuchen](https://github.com/Ryuchen)
* Email: [chenhaom1993@hotmail.com](chenhaom1993@hotmail.com)
* QQ: 455480366
* 微信: Chen_laws

Nameplace ( 虚位以待 )

### 🤝 贡献源码:

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/Ryuchen/Panda-Sandbox/issues).

### ⭐ 渴望支持: 

Give a ⭐️ if this project helped you!
Please buy me a coffee!

| **微信**                         | **支付宝**                           |
| ------------------------------- | ----------------------------------- |
|<p align="center"><img src="https://github.com/Ryuchen/Panda-Sandbox/tree/master/sponsor/wechat.svg" alt="wechat" width="100"/></p>|<p align="center"><img src="https://github.com/Ryuchen/Panda-Sandbox/tree/master/sponsor/alipay.svg" alt="alipay" width="100"/></p>|
| ------------------------------- | ----------------------------------- |

### 📝 开源协议:

Copyright © 2019 [Ryuchen](https://github.com/Ryuchen).<br />
This project is [GPL](http://www.gnu.org/licenses/gpl-3.0.html) licensed.
请谨遵开源协议，谢谢使用！

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_