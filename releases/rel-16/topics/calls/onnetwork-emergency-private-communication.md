# 在网紧急私通信：优先于哪些通信，正在进行的私通信能否转为紧急？

适用于在网的 MCVideo、MCData。[TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)限定在网场景；规范性表 [B.1（MCVideo），印刷页 79](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=80) 和 [C.1（MCData），印刷页 90](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=91) 都列出 §6.8.8.2 的四项要求。[A.1（MCPTT），印刷页 68](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=69) 在本节标为 NA。不能由表 A.1 的 NA 推断其他规范没有 MCPTT 紧急私呼。

**与其他私通信比，谁优先？** MCX 业务须确保紧急私通信相对于所有其他私通信享有最高优先级。不能把私通信之间的比较推广为在全部 MCX 通信中优先级最高。 [R-6.8.8.2-001，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**谁能替谁请求提高优先级？** MCX 业务须能为一次紧急私通信的参与者请求提高优先级。条文不要求每次实际发出请求，也不保证请求获准或参与者的优先级已经提高。 [R-6.8.8.2-002，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**私通信已经开始，还能转为紧急吗？** MCX 业务须能把正在进行的私通信转为紧急私通信。仅能另建一通紧急私通信，不足以满足这项转换要求。条文没有规定自动转换、触发条件、由谁发起或使用哪种信令。 [R-6.8.8.2-003，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**哪些通信不在抢占规则内？** 紧急私通信（包括其内容和信令）相对于其他类型的 MCX 业务通信须享有抢占优先权，但系统通信、MCX 紧急组通信和其他 MCX 紧急私通信除外。列为例外不能证明对方反过来享有抢占优先权，也不能证明双方同级。享有抢占优先权不等于某次通信实际被中断。例如，紧急视频私呼遇到紧急组通信，不能用本条裁定哪一方抢占另一方。[R-6.8.8.2-004，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

若问题是传输或呈现时怎样比较一般私通信，见[私通信的相对优先级](onnetwork-private-communication-priority.md)。若是一通紧急组通信到来，而接收用户正在私通信，见[紧急组通信的通知和接通](onnetwork-emergency-group-communication.md)。

查具体升级流程时，按业务选读 Stage 2 的 [MCVideo 私呼](../mcvideo/private-emergency-upgrade.md)、[MCData 一对一短数据](../mcdata/one-to-one-sds-emergency-upgrade.md)或[一对一文件分发](../mcdata/one-to-one-fd-emergency-upgrade.md)。若要解释 MCPTT 按需私呼升级的实际信令，另见 [MCPTT Stage 3 的应答与告警](emergency-private-upgrade.md)；其依据不是本节。
