# 组呼何时结束：按组类型区分T4、TNG3与人员条件

TS24.379 V19.4.0 §6.3.8.1及§6.3.3.5；控制功能的组呼释放策略。各条保留组类型，不照搬私呼或把所有计时器当同一超时。

## T4与参与人数适用的组不同

适用条件：控制功能判断组呼释放。

预安排、广播或adhoc组呼收到媒体层T4 inactivity到期指示时须释放；只剩一名或无人参与的释放条件适用于预安排、广播或chat组呼。两组类型列表不同，不能互换，也不能把本节写成服务器自行按静音时长判断。

依据：§6.3.8.1 条件1–2。

## 人员离开和affiliation不足

适用条件：控制功能判断组呼释放。

预安排或adhoc组呼发起者离开且本地策略要求时须释放；adhoc中特定一名或多名用户离开且本地策略要求时亦须释放。最少affiliated成员不足也触发释放，但原文明示该项不适用于adhoc；TNG3到期是另一释放条件。

依据：§6.3.8.1 条件3–6。

## TNG3由组文档启动

适用条件：收到发起组会话INVITE，且已分配会话identity。

在未进入启动TNG2的例外时，组文档有on-network-maximum-duration才按其值启动TNG3；缺失则不启动；启动TNG2时不启动TNG3。注释说明预安排组必须配置、chat可选，但不据此给缺失配置编造默认时长。最后客户端离开时停表；到期按BYE程序释放。

依据：§6.3.3.5.1。

## 合并和拆分切换各组计时器

适用条件：活动组呼合并为临时组，或临时组拆回独立组。

合并时停止各原活动组TNG3，临时组控制功能启动其TNG3；拆分时停止临时组TNG3，各独立组控制功能启动各自TNG3。不把该动作补成继承剩余秒数的规则。

依据：§6.3.3.5.1。

## 紧急组呼TNG2与TNG3切换

适用条件：控制功能处理组呼的紧急计时器切换。

启动TNG2时不启动TNG3。TNG3运行中的组呼升级为紧急时，停TNG3并按服务配置emergency-call/group-time-limit启动TNG2；TNG2运行期间取消紧急时，停TNG2并按组文档maximum-duration启动TNG3。TNG2到期后也启动TNG3；不据此把TNG2到期直接等同整个组呼已结束。

依据：§6.3.3.5.2。

## 证据边界

- T4及媒体行为依赖TS24.380；TNG2到期的其他紧急状态处理、数值范围、组文档验证及计时竞态未在本页展开。
- 不为缺失配置、重启与合并拆分补剩余时长继承算法；TNG1是建立确认等待，非本页时长计时器。

## 按需继续

- [server-release-chain](server-release-chain.md)
- [../groups/temporary-group-lifecycle](../groups/temporary-group-lifecycle.md)
- [../interworking/group-call-release](../interworking/group-call-release.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页153、164；仅本版本。

- [建立时的 TNG1 不同于存续时长](group-acknowledged-start.md)
