# 互通组呼晚加入：归属成功与话权状态

适用版本：TS23.283 V19.5.0，Release 19，Stage 2。

正在进行互通组呼；双方已知组配置，IWF 已配置组及用户身份映射；参与侧成功完成组归属。

## 参与侧成功完成组归属

触发正在进行的互通组呼晚加入；适用于包括紧急、迫近危险和广播在内的组呼类型。 [§10.3.3.7.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 MCPTT 系统；LMR 用户加入

首名 LMR 用户适用两种 IWF 归属方式；后续用户仅在 IWF 逐个透传成员归属时触发此流程。MCPTT server 向 IWF 发组呼请求，IWF 响应后加入，并接收已占用或空闲话权状态。 [§10.3.3.7.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 LMR 系统；MCPTT 用户加入

流程适用于首名及后续 MCPTT 用户。IWF 向 MCPTT server 发组呼请求，后者为新用户建立呼叫并响应；IWF 提供话权状态，经 server 转交新用户。 [§10.3.3.7.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

LMR 定义组的晚加入在 §10.3.3.7.3 step 4 还有媒体条件：指定 E2EE 时两侧须同 codec；未指定时可不同，不同 codec 需 IWF 转码。[加密转码专门流程](encrypted-transcoding.md)不能作为忽略此分支条件的通用许可。

话权已占用/空闲通知描述当前状态，不表示向新加入用户授予话权。成功归属是晚加入的触发条件，不是所有呼叫建立步骤已完成的证明。

## 边界与相关问题

本页只核验 TS23.283 的互通段；TS23.379 基础呼叫过程、LMR 内部信令及完整失败状态机未核验。

[组配置](group-configuration.md) · [组呼请求字段](group-call-request.md) · [互通范围](scope.md) · [结构化知识](late-entry.json)

Chat 的显式 join、隐式归属及回覆盖另见 [chat 加入](chat-entry.md)，不要从这里省略其独立前提。

需核对归属本身时见 [归属表示方式](affiliation-representation.md)。
