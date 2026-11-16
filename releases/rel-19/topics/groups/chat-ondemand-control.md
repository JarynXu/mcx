# 控制侧 chat 建立与加入：组文档、有效归属、容量和成功响应

限 TS24.379 V19.4.0 在网按需 chat；目标是 GMS 维护的普通 MCPTT 组，不是 TGI、不是基于预配置组的重组，也未被 regroup。

收到 §10.1.2.4.1.1 所述给负责该组 CF 的 INVITE。incoming 用户 ID 取 mcptt-calling-user-id，组 ID 取 mcptt-request-uri，client ID 取 mcptt-client-id。

请求不携带 emergency、imminent-peril、alert 或 Resource-Priority；控制侧该组当前 in-progress emergency 和 in-progress imminent-peril 均为 false。仅排除请求优先标志不足以排除 steps14–15。

为避开本版未归属分支的 eligible 异常，可执行主链限定该 user/client 已按 §6.3.6 通过 CF 归属检查；不把组成员资格或 O-PF affiliating 状态当作这个前提。

各后续成功分支须所有此前适用检查均未拒绝或停止。

## 资源与媒体特征检查

适用条件：CF 收到本主题范围 INVITE，进入 §10.1.2.4.1.1。

资源不足或拥塞风险时 CF 可返回 500，可附 Retry-After，选择拒绝后停止。若 Accept-Contact 缺 g.3gpp.mcptt，或缺包含 MCPTT ICSI 的 g.3gpp.icsi-ref，或 Contact 带 isfocus，必须 403 并停止。请求 Contact 的 isfocus 拒绝条件与成功响应 Contact 需要 isfocus 的条件方向不同。

依据：§10.1.2.4.1.1 steps1–2。

## 组文档的初始处理

适用条件：CF 已通过前序检查；目标组的文档由 GMS 维护，执行 step4(a) 调用的 §6.3.5.2。

尚未订阅该组文档时先订阅 xcap-diff；订阅 404 对应 404/Warning113，其他 4xx/5xx/6xx 对应其最终响应加 Warning114。对取得或已缓存的普通非重组组文档，on-network-disabled 只要存在就 403/115；list-service/list 缺该用户 entry 则 403/116。on-network-invite-members=true 但请求 session-type 不是 prearranged 时为 404/117；该值 false 而 session-type 不是 chat 时为 404/118。调用返回最终失败后，chat 父流程 step4(d) 停止。

依据：§10.1.2.4.1.1 step4(a,d);6.3.5.2 steps1–5。

## 预配置专用组与有效归属

适用条件：GMS 组文档初始处理未停止，CF 继续 step4(b)；并解释本页采用的已归属前提。

list-service 中 preconfigured-group-use-only=true 时，CF 返回 403/Warning167 并停止，即使客户端没有先阻止仍会有服务器检查。正常继续所用的已归属前提是 §6.3.6 依次找到匹配组 entry、该用户 entry、本次 client ID，且该用户 entry 的 expiration 尚未到达；成员 entry 不能代替该 user/client/有效期判定。

依据：§10.1.2.4.1.1 step4(b),step6 opening;6.3.6。

## 新建会话及媒体检查

适用条件：本主题 CF 已归属前提成立，前序检查未拒绝；处理 step10，并在 chat session 尚未 ongoing 时进入 step11。

媒体参数不可接受或未提供 MCPTT speech codec 时，CF 返回 488 并停止。会话尚未 ongoing 时创建 chat session 并分配 MCPTT session identity；step11(a) 对按 §6.3.3.5 处理 TNG3 使用 MAY。普通非重组 step11 不调用预安排组呼的 TNG1 required/minimum 应答门槛，不据此生成对所有归属成员的普通邀请清单。

依据：§10.1.2.4.1.1 steps10–11(a)。

## 已有会话的容量门槛

适用条件：chat group session 已 ongoing，且 on-network-max-participant-count 已达到；此前适用检查未拒绝。

若本地策略认为来话用户优先级高于某个既有用户，CF 可以按 §10.1.1.4.4.3 移除一个参与者并跳过下一拒绝步；否则返回 486/Warning122。该例外是 MAY，不是优先级较高就必须踢人，也不是资源上限可以无条件越过。

依据：§10.1.2.4.1.1 step12;Note5。

## 控制侧响应与媒体处理顺序

适用条件：本主题普通状态、已归属、非重组路径的全部前序适用检查通过，进入 steps16–25；未执行优先升级 §6.3.3.1.8。

CF 接受并生成 INVITE 200，附 §6.3.3.2.1 SDP answer；应含 Session-Expires 并按 RFC4028 监督会话，建议省略 refresher，带则为 uac。Require 必须含 timer；Contact 含 g.3gpp.mcptt、MCPTT ICSI 的 g.3gpp.icsi-ref、MCPTT session identity 和 isfocus；Supported 含 tdialog。step24 先与 TS24.380 媒体面交互，step25 才发送 200。这里处理顺序与 O-PF 发 200 后再媒体交互的顺序不同。

依据：§10.1.2.4.1.1 steps16–21,24–25。

## 已有会话加入后的通知

适用条件：CF 已按本普通分支发送 200；该 chat session 在本次请求前已 ongoing，且至少一个参与者订阅 conference 事件。

CF 按 §10.1.3.4.2 向所有持有该 conference 订阅的参与者发送 NOTIFY。条件是已有会话加至少一个订阅者，不是新建 chat 就必须通知全体成员，也不是把所有已归属用户自动加入通知对象。

依据：§10.1.2.4.1.1 step26。

## 证据边界

- §6.3.5.3 有控制侧允许加入既有组会话的一般授权条件；但 §10.1.2.4.1.1 没有像预安排 §10.1.1.4.2 那样显式调用 §6.3.5.3/.4，也没有在此给 403/121、403/119。本页不宣布 chat 豁免通用授权，也不移植预安排的检查位置或失败码。
- 未归属者的 implicit eligibility/执行路径有原文冲突，不能据修正后的布尔式声称完整准入实现。
- 普通非重组范围排除已 regroup 的 403/148 与补发重组 MESSAGE、临时组/预配置重组多 CF 联动及 emergency/imminent-peril/alert 状态机。
- TS24.229、TS24.380、RFC4028 及 SDP helper 仅作为明确引用依赖，未在本页全部核验。
- 不从此 403 分支补出 Warning 码；原文未在这些检查中列该码。
- 元素存在条件不改成值为 true。取得文档、订阅状态和 XCAP 的完整机制复用 TS24.481 主题，不在这里重建。组类型不匹配的失败用于说明类型一致性，不把错误配置当作合法普通 chat。
- 不在本 claim 给未归属者一律判 403/120；其实际 step6 同时含 eligible 与 constituent group 条件，原文异常见本页证据边界。
- 这里仅描述新会话分支。TNG3 配置、停止和到期另见 calls/group-release-timers；不设默认时长，不声称加入已有 chat 必须重置计时器。
- 移除成功、失败及通知条件由已有 participant-removal 主题承担；不把退出动作简化成删除成员资格或归属。
- SHOULD 不写成 SHALL。媒体交互不被本页补成完整加解密、承载、话权或可听见语音的判定。优先分支 SDP 例外交叉引用有错位，不用于本条。
- 订阅权限、有效订阅、NOTIFY 内容与版本合并由既有 conference-state 主题承担；本条不创建订阅。
- §10.1.2.4.1.1 step6（印刷页341、342）：用户按 §6.3.6 尚未归属时，原文进一步写 eligible for implicit affiliation 且 mcptt-calling-group-id 不是 constituent group ID，然后返回 403/Warning120。不是 not eligible。普通来话通常没有该 calling-group-id，缺失元素的布尔求值亦未在这一步另行给出。 保留字面条件和异常，不反转 eligible、不补缺失元素求值；主链限定 CF 已归属。
- §10.1.2.4.1.1 step13（印刷页343）：隐式归属执行回指 eligible in step5，但 step5 是预配置重组存储信息，资格文字实际出现在 step6。 保留交叉引用错误；不将其视为有证据的无条件自动建归属。
- §10.1.2.4.1.1 step17（印刷页344）：SDP answer 例外引用 step13(a)/14(a)，而优先升级调用分别位于 step14(a)/15(a)。 普通范围未执行优先升级，故本页的 SDP answer 结论不依赖修正该引用。

## 按需继续

- [../calls/chat-ondemand-entry](../calls/chat-ondemand-entry.md)
- [../groups/implicit-affiliation-eligibility](../groups/implicit-affiliation-eligibility.md)
- [../groups/join-authorization](../groups/join-authorization.md)
- [../groups/conference-state](../groups/conference-state.md)
- [../calls/group-participant-removal](../calls/group-participant-removal.md)
- [../calls/group-release-timers](../calls/group-release-timers.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页159、160、161、163、164、340、341、342、343、344、345；仅本版本。
