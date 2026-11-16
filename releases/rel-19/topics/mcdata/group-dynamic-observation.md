# MCData group dynamic：独立组观察，不是归属或会话参加证明

限 TS24.282 V19.7.0 §8.2.7 的客户端 group dynamic 观察及必要接收/通知条款；不展开跨域转发、其他用户代理或完整动态组配置。

下列服务器分支按 §8.3.3.9 所列入口描述。本版 per-group filter 和调用者身份条件存在文字不一致，必须保留，不把业务判断写成已验证可执行报文。

## 动态组观察的独立入口

适用条件：客户端希望获得某个组的当前及后续动态资料，或只获取一次当前资料。

§8.2.7 的初始 SUBSCRIBE 仍发给服务用户的 originating PF，但 mcdata-request-uri 填目标组 ID，另附 MCData ICSI、PIDF Accept 及指向组 ID 的 per-group simple-filter 请求。当前加后续资料用 Expires=4294967295，仅取当前用 0；对话内续订和退订分别用 4294967295 和 0，并保留 PIDF Accept。这一入口与 §8.2.3 以用户 ID 为目标、按客户端过滤归属状态的入口不同。§8.2.1 要求变更前启动的是归属状态确定，并未把 group dynamic 订阅列为此前置。

- 只就这些已读条款说明前置关系，不据此断言所有 MCData 功能永远无需 group dynamic 数据。
- 这里的订阅不构成创建/修改组、发起归属变更或加入 SDS session；各操作仍有各自入口。
- 此 claim 保留原文对 per-group filter 的要求，其具体编码缺口见同页后续 claim，不自行用 per-client 语法替换。

依据：§8.2.1;8.2.3 initial SUBSCRIBE;8.2.7，印刷页 158、159、160、162。

## 动态资料的授权与结果

适用条件：到达控制目标组的 CF，且按 §8.3.3.9 入口及其待澄清 filter/身份条件解释请求。

该过程从 mcdata-request-uri 取目标组 ID、从 mcdata-calling-user-id 取 handled 用户 ID。Expires 缺失或非零低于 4294967295 时返回 423/Min-Expires 并停止；组在 GMS 中不存在，或该用户无权订阅该组动态资料时，分别返回 403 并停止。通过后发送 SUBSCRIBE 200，订阅期间由 §8.3.3.10 发 per-group dynamic PIDF 通知，并要求 affiliation 带 expires。客户端在收到满足 §8.2.7 条件的 NOTIFY 后确定组动态资料；200 本身不是资料内容，也不是用户已归属或会话已参加的证明。

- Min-Expires 值为 4294967295；未核 GMS 查询、组资料授权策略或 RFC6665 订阅恢复。
- 这里不能只用“请求了目标组”替代 handled 用户的动态数据订阅授权；也不能把此授权当成 SDS 发送许可。
- §8.3.3.10 指向 §8.4.1，但本页不从 per-group affiliation 结构自行外推出完整动态数据字典。

依据：§8.3.3.9 steps1–6 and final paragraph;8.3.3.10;8.2.7 NOTIFY paragraph，印刷页 162、185、186。

## 过滤与调用者身份的编码缺口

适用条件：需要把 §8.2.7 的业务要求转换成 interoperable 的 group dynamic 请求/通知编码。

本版 §8.2.7 要求按 §8.4.2 构造 per-group filter，但 §8.4.2 实际只列 per-client 和 per-user 限制，两种 include 都按 tuple.id 选择，分别代入客户端 ID 或用户 ID。§8.3.3.9 的入口又要求 filter 中的组 ID 与 mcdata-calling-user-id 相同，随后却把该字段识别为 handled 用户；前面的转发过程也将该字段填写为 originating 用户 ID。这些不是已经核实的同一身份关系，不能静默把用户字段换成组字段、或自行拼一个 per-group XPath 后宣称编码闭合。

- 业务意图、独立授权及通知结果可以分段说明；本页不声称 group dynamic 的完整 filter/schema 已验证通过。
- 8.4.1 的正文介绍 per-user/per-group affiliation，未在本页核到另列的完整 group dynamic 编码说明，不据字段名称补数据模型。
- 保留原文关系待澄清，既不把这一不一致扩为整个 MCData 归属不可用，也不把它藏在泛泛的“外部依赖待核”中。

依据：§8.2.7 initial SUBSCRIBE step7;8.3.3.8 forwarding step4c(B);8.3.3.9 opening5 and steps1,2;8.4.2.1/.2，印刷页 162、184、185、188、189。

## 证据边界

- 本主题不构造完整转发链和可执行 filter；原文编码与身份关系缺口直接限制实现结论。

## 按需继续

- [explicit-affiliation-observation](explicit-affiliation-observation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

- §8.2.7 step7;8.3.3.9 opening5;8.4.2：group dynamic 调用 per-group filter，但被调用条款只给 per-client/per-user filter。 不替换 ID 或借用 MCPTT 配方补造过滤器。
- §8.3.3.8 forwarding step4c(B);8.3.3.9 opening5,steps1,2：owner 入口要求组 ID 与 calling-user-id 一致，转发及后续识别则把 calling-user-id 作为用户 ID。 分别保留组目标与用户授权的业务含义，不声称已证实入口能按这一字面关系闭合。
- §8.2.7 NOTIFY paragraph;8.3.3.10;8.4.1.1/.2：group dynamic 通知引用8.4.1；该条款介绍与语法实际是 per-user/per-group affiliation。 只报告已有调用和 expires 要求，不扩为完整动态组数据模型。
- §8.3.3.8 opening2 and step1 versus step4c：转发接收段的 mcdata-info MIME 名称省略 +xml，而新生成的请求使用 application/vnd.3gpp.mcdata-info+xml。 本页只取明确的调用者/组字段语义，不把未修复的入口写成已通过完整报文验证。
