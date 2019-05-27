<h1 align="center">Panda Sandbox</h1>


<div align="center">这是一个基于 Cuckoo 开源版本的沙箱的修订版本, 该版本完全为了适配国内软件环境所打造</div>

#### 设计特性

- 将收录和兼容 Cuckoo 社区中的所有行为签名和检测手段。
- 采用新的方式重构任务调度和沙箱调度，提高整体的运行效率。
- 将集成开源情报，并将集成小型开源情报库在内，构建信誉体系。
- 合并 Cuckoo 开源插件中的 android、linux、macos 平台检测。
- 重构 Cuckoo 文件报告的展示效果，计划支持在 Web 界面制作虚拟机。
- 将采用全新的设计方式实现多节点的支持，实现高效的集群能力。


#### TODO清单:
 * [x] 创建新的项目并创建第一次提交
 * [x] 迁移官方最新的 agent 脚本过来
 * [ ] 构建基本任务调度框架结构(celery)
 * [ ] 构建基本的虚拟机调用程序(VMWare Fusion Pro base on MacOS)
