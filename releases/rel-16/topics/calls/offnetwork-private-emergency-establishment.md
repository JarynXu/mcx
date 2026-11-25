# 离网 MCPTT 紧急私呼初建：什么时候标紧急，谁启动 TFP8？

第一条 `PRIVATE CALL SETUP REQUEST` 可以标紧急，也可以请求手动接听。发出这条请求、被叫记下紧急类型、某一端进入紧急通话状态，是三件事。以下只看 TS 24.379 V16.14.0（Release 16，Stage 3）的离网一对一紧急私呼初建。每端的基本呼叫控制 P 与呼叫类型控制 Q 并行，分别以本端的状态和事件判断。[§§11.2.3.1–.3，印 436–437](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=437)。

## 主叫如何选紧急类型和接听模式？

**类型看 Q0。** 本端用户要求发起呼叫，若关联的已存紧急状态为 `true`，且用户配置档的 `Common/PrivateCall/EmergencyCall/Authorised` 为 `true`，终端须保存紧急私呼类型和对应的 ProSe 逐包优先级。若该紧急状态为 `false`，用户明确要求发起紧急私呼且有同一项授权，才命中第二条紧急分支。这里读取的是 §12.2.2.2 [按 MCPTT 组保存的告警状态机](offnetwork-mcptt-group-emergency-alert.md)所关联的状态，不是这场私呼的 Q2。引用的条款没有规定多组时怎样选取或合并状态，也没有为紧急授权不满足的请求规定一律降为普通私呼。[§11.2.3.4.2，印 437](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=438)；[§12.2.2.2，印 457](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=458)。

**模式看 P0/P1 的发起分支。** 本端还须满足 `Common/PrivateCall/Authorised=true`。用户请求自动且 `AutoCommence=true` 才选择自动；否则 `ManualCommence=true` 时选择手动。两个模式条件都未命中，本项不给默认值。终端为本次新呼叫生成并保存 Call identifier，请求里的 Commencement mode 取已选模式，Call type 取类型控制保存的值。发出请求后启动 TFP1，在 P2 等待应答。这一步没有规定启动 TFP8。与此相对，[已有普通私呼升为紧急](offnetwork-private-emergency-upgrade.md)要求本端原在 Q1，复用这通呼叫的标识，填自动模式并在发起分支进入 Q2。只看报文名、紧急类型或自动模式，无法区分这两种程序。[§11.2.2.4.2.1 第 1、4–5、9、10–14 项，印 423–424](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=424)；[§11.2.3.4.5.1 入口和第 6(a)、6(d)、12 项，印 438](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=439)。

## 被叫标记紧急后，什么时候才算本端进入 Q2？

空闲被叫在 Q0 收到 SETUP REQUEST，若 Call type 是 `EMERGENCY PRIVATE CALL`，须保存紧急类型和对应的 ProSe 逐包优先级。接听仍看基本呼叫控制：若被叫在 P0/P1，收到手动模式请求且 Call identifier 不同于已存值，须发 `PRIVATE CALL RINGING`，启动等待用户应答的 TFP2，进入 P5。紧急类型本身不把手动改成自动，也不触发 Q2 或 TFP8。[§11.2.3.4.3–.4，印 437–438](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=438)；[§11.2.2.4.4.1，印 429](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=430)。

- **P 层何时进 P4？** 主叫在 P2 实收回应本次 SETUP REQUEST、且 Call identifier 相同的 `PRIVATE CALL ACCEPT`，须发 `PRIVATE CALL ACCEPT ACK` 并按基本流程进入 P4。被叫在 P5 实收该 ACK 或来自主叫的 RTP，也按本端基本流程进入 P4。被叫发 ACCEPT 时仍按相应接听分支处于 P5，不能用发出 ACCEPT 代替后续收件。[§11.2.2.4.2.8，印 425–426](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=426)；[§11.2.2.4.3.2、.3.4，印 427–429](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=428)；[§11.2.2.4.4.3、.4.5，印 430–432](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=431)。
- **Q 层何时启动 TFP8？** 本端仍在 Q0，已存类型为紧急，且实收这通呼叫的 ACCEPT 或 ACCEPT ACK，须启动隐式降级计时器 TFP8 并进入 Q2。该条按本端收件判断，不规定 P 和 Q 在同一事件上的调度顺序。ACCEPT ACK 的消息定义只确认收到 ACCEPT；本端发出 ACK 不证明对端收到，也不证明对端 Q2、TFP8 或媒体呈现。[§11.2.3.4.4，印 438](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=439)；[§15.1.11.1，印 482](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=483)。

例如，乙已发 ACCEPT，之后只查到乙实际收到甲的 RTP，没有乙收到 ACCEPT ACK 的证据。RTP 足以命中乙的 P5 进入 P4 的基本流程；Q0 的 §11.2.3.4.4 没有列 RTP 这个入口。不要把 P4 写成乙的 TFP8 已启动，也不要从抓包没看到 ACK 断言乙一定没收到。查乙本机的入站消息和类型状态记录。

普通私呼另查[手动接听](offnetwork-private-manual-client.md)和[自动接听](offnetwork-private-auto-client.md)。已在 Q2 的终端遇到 TFP8 到期，查[离网紧急私呼降级](offnetwork-private-emergency-downgrade.md)。这里不推导实际优先级数值、底层是否按该优先级传送、端到端保护参数或对端是否听到语音。
