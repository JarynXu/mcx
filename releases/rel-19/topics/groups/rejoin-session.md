# 重新加入预安排组呼：使用已有会话身份

TS24.379 V19.4.0 Stage3，在网普通预安排组呼的rejoin；不展开紧急、迫近危险、远程发起和重组特例。

本页解释已有会话身份的寻址与准入；并非新建组呼或显式affiliation注册流程。

## 按需重入使用初始INVITE

适用条件：用户要求重入进行中会话，或客户端因回到覆盖触发重入，且使用按需会话。

客户端复用§10.1.1.2.1.1的起呼过程，但Request-URI改为要重入的MCPTT session identity URI；发的是initial INVITE，不是原对话中的re-INVITE。如何检测回到覆盖在本规范范围外。

依据：§10.1.1.2.4.1。

## 预建立路径使用REFER中的会话目标

适用条件：用户要求在预建立会话内重新加入进行中的MCPTT呼叫，或因回到覆盖触发。

客户端按§10.1.1.2.2.1生成REFER；Refer-To指向要重入的MCPTT session identity URI，其URI headers部分按该条携Content-Type及body参数，mcptt-info中的session-type=prearranged。不是将业务组ID不加区别地替代已有会话身份；完整URI编码依赖原条款。

依据：§10.1.1.2.4.2。

## 参与功能映射到上游会话身份

适用条件：参与功能收到相应prearranged重入INVITE或预建立REFER。

参与功能复用各自起呼程序，发往控制功能的INVITE Request-URI使用映射后的会话身份：按需取来话Request-URI中的身份，预建立取REFER的Refer-To中的身份。映射不等于把原URI逐字转发，也不定义集群节点粘性。

依据：§10.1.1.3.5.1;10.1.1.3.5.2。

## 已有身份仍须通过授权和归属

适用条件：控制功能处理Request-URI指向会话身份的重入INVITE。

资源不足或拥塞可回500（可附Retry-After）；会话不存在回404；媒体参数不可接受或没有MCPTT speech codec回488；Accept-Contact缺MCPTT特征或正确MCPTT ICSI回403。按§6.3.5.3判断加入许可，未授权403+121；按§6.3.6检查该用户在本客户端对会话所属组的归属，未归属403+120。加入许可不能由发起许可或持有组密钥替代。原文在归属检查前调用§6.3.3.2.2初始INVITE处理，不自行改写内部副作用顺序。

依据：§10.1.1.4.5.1 steps1–8。

## 满员时的本地策略与拒绝

适用条件：前序重入检查未拒绝，且已达到on-network-max-participant-count。

若本地策略判新用户优先级高于现有用户，控制功能可以按§10.1.1.4.4.3移除一名参与者并跳过满员拒绝；否则回486+122。策略可考虑user-priority、participant-type等信息，但不是强制抢占，也没有固定排序算法。收到Resource-Priority时还可按24.229施加优先处理。

依据：§10.1.1.4.5.1 steps9–10。

## 完成媒体处理后答复并通知订阅者

适用条件：重入准入通过，未被满员等条件拒绝。

控制功能构造200及SDP answer；完成规定媒体处理之后发送200，再生成加入通知并向订阅conference event package的客户端发送NOTIFY。这是加入既有会话，不是重新等待所有组成员确认的建组流程。

依据：§10.1.1.4.5.1 steps11–16。

## 证据边界

- 参与功能与客户端的起呼复用涉及其他条款，本页不提供完整SIP/SDP模板、重传与失败回滚。
- §10.1.1.3.5.1/.5.2引用起呼步骤编号分别为10/16；保留本版引用，不凭该编号改写目的会话映射语义。
- 多节点会话映射存储、检测恢复覆盖、原会话身份的持久保存策略、完整媒体/话权过程未由这些条款定义。
- 只覆盖已有会话身份rejoin。直接以组ID请求加入活跃会话的§10.1.1.4.2 step15为另一个入口，不能默认等同。

## 按需继续

- [prearranged-origination](prearranged-origination.md)
- [join-authorization](join-authorization.md)
- [prearranged-admission](prearranged-admission.md)
- [../calls/group-acknowledged-start](../calls/group-acknowledged-start.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页278、289、303、304；仅本版本。

- [组ID入口及服务器邀请](active-call-entry.md)

- [conference-state](conference-state.md)
