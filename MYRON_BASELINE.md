# myron 基线对照实验

本分支 myron/baseline_test 从 myron/droidspaces_only 的 785e133 创建。
保留同一 locked.xml、r62 源码、工具链、Bazel fast 参数和 AnyKernel3 提交。
不应用 Droidspaces 补丁、不添加 IPC 符号导出、不修改 gki_defconfig。
保留原构建的 check_defconfig disabled 设置，以减少实验变量。
这是 AOSP 候选基线，不是小米原厂源码的复刻。

## 运行

刻意保留 workflow 文件路径：
.github/workflows/myron-droidspaces-only.yml
因此默认分支注册的 Run workflow 可以选择 myron/baseline_test。
此分支运行名称为 Build myron baseline GKI。
产物名称包含 myron-baseline，以免与 Droidspaces 版混淆。
尚未推送；不需要将本分支设为默认分支。

下载产物中的 Image，用同一原厂 boot 备份及重打包工具生成测试镜像。
通过 fastboot boot 临时启动，对比 Wi-Fi、蜂窝、震动和模块列表。
基线不支持 Droidspaces 是预期行为。
若基线同样故障，优先排查 GKI 与原厂模块兼容性；若基线正常，
再逐步引入 Droidspaces 配置与补丁定位。

MYRON_DROIDSPACES.md 是继承的原实验说明；本分支以本文为准。
