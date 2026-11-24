# 在网迫近危险组通信：为谁请求提高优先级，组状态从何时算起？

**优先级请求面向谁？** MCX 业务须能为本次迫近危险组通信的所有参与者请求提高优先级。仅归属该组而未参与本次通信的人不在本项请求范围内。条文不要求每次都发出请求，也不保证获准或实际提高优先级。 [R-6.8.8.3-001，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**业务须知道谁发起了通信？** MCX 业务须掌握哪些已归属该 MCX 业务组的成员发起了这次迫近危险组通信；发起者可以是一人或多人。不能用全体参与者或全体已归属成员的名单代替对发起者的识别。本项没有规定记录格式、信令字段或保存时长。 例如，甲和乙都已归属该组，也都参加这次通信，但只有甲发起。优先级请求的对象包括甲、乙；识别发起成员时，只应把甲算作发起者。[R-6.8.8.3-002，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**建呼失败或通话结束，组状态就清除了吗？** 从首次请求迫近危险组通信之时起，MCX 业务须为该组维持“迫近危险进行中”状态，直至该状态被取消。起点不以建呼成功为条件。建呼被拒、建立失败或一通通信结束，本身都不能证明该组的状态已取消。本项没有指定谁来取消或采用什么程序。 例如，日志只显示首次请求后建呼失败，没有组状态取消的证据；不能用这条失败记录判定组状态已经清除。[R-6.8.8.3-003，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

编者注将迫近危险组通信与 MCX 紧急组通信能否归为一类留作进一步研究（FFS）。不能据此套用紧急组通信的优先级、抢占规则或紧急状态。 见[§6.8.8.3 编者注，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。若问题说的是紧急组通信，见[在网紧急组通信](onnetwork-emergency-group-communication.md)。

适用范围见 [TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)。规范性表 [A.1（MCPTT），印刷页 68](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=69)、[B.1（MCVideo），印刷页 79](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=80)、[C.1（MCData），印刷页 90](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=91) 都列出 §6.8.8.3 的三项要求。

查具体业务时，按问题选读 Stage 2 的 [MCVideo 发起迫近危险组呼](../mcvideo/imminent-peril-group-call-commencement.md)、[MCVideo 升级与取消](../mcvideo/imminent-peril-upgrade-cancel.md)或 [MCData 组短数据与文件分发](../mcdata/group-imminent-peril-sds-fd.md)。若要判读 MCPTT 取消请求的回包，见 [Stage 3 的 MCPTT 取消流程](onnetwork-imminent-peril-cancellation.md)。
