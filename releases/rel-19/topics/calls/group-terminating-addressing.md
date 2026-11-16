# 组呼终接参与功能：服务设置、身份绑定与下行寻址

TS24.379 V19.4.0，普通非优先预安排组呼；终接参与功能收到面向自己的初始SIP INVITE。

排除emergency-ind=true、imminentperil-ind=true及任何Priv-Answer-Mode头；不覆盖远程监听、重组扩展。

## 资源不足可以拒绝

适用条件：因资源不足而无法处理请求，或存在拥塞风险。

T-PF可拒绝为500；可附Retry-After。若选择拒绝，则不得继续后续步骤；不是所有请求必须500。

依据：§10.1.1.3.2 step1。

## 缺少会议焦点标签

适用条件：执行到Contact检查，且收到的Contact不含isfocus媒体特征标签。

必须403，Warning代码104；停止后续步骤。

依据：§10.1.1.3.2 step2。

## 未收到客户端服务设置

适用条件：执行到客户端服务设置检查，且尚未按§7.3.3或§7.3.4从被邀请MCPTT客户端收到application/poc-settings+xml中的Answer-Mode Indication。

必须480，Warning代码146；停止后续步骤。不是仅检查当前INVITE是否含Answer-Mode头。

依据：§10.1.1.3.2 step3。

## 以被邀 MCPTT ID 查绑定

适用条件：前述检查未拒绝请求。

必须以收到的mcptt-info正文mcptt-request-uri中的MCPTT ID检索其与公共用户身份的绑定；若无绑定，必须404并停止。本步骤未列Warning141，也未显式列到期判断，不能从主叫程序移植。

依据：§10.1.1.3.2 steps4–5。

## 下行指向公共用户身份

适用条件：选择自动按需§6.3.2.2.5.2或手动按需§6.3.2.2.6.2。

生成面向客户端的初始INVITE；Request-URI使用被邀MCPTT ID关联的公共用户身份，PAI使用T-PF公共服务身份。

依据：§6.3.2.2.5.2 steps3–6;6.3.2.2.6.2 steps1–3,7。

## 保留客户端选择约束

适用条件：按§6.3.2.2.3生成面向终接客户端的初始INVITE，且来件存在Accept-Contact或Reject-Contact。

必须保留这些头及其特征值和参数；规则引用RFC3841。这不是本文已验证的fork算法。

依据：§6.3.2.2.3 step1。

## 映射会话身份，不推导部署粘性

适用条件：按§6.3.2.2.3生成面向终接客户端的初始INVITE。

Contact必须含映射至来件Contact中MCPTT session identity的会话身份，并保留其余URI参数；还含g.3gpp.mcptt、MCPTT ICSI及isfocus。映射不等于直接照抄同一URI，更不规定物理节点黏性。

依据：§6.3.2.2.3 step4。

## 证据边界

- 完整SIP fork/多分支失败合并未由这些条款定义；24.229依赖未核。
- 未核24.380媒体实施，不能将响应等同全组建立或话权授予。
- 显式Answer-Mode入口选择不从10.1.1.3.2无头条件反推。
- 6.3.2.2.6.3以reINVITE调用初始INVITE生成条款，保留原交叉引用，不改写成新dialog。

## 按需继续

- [group-terminating-mode](group-terminating-mode.md)
- [group-terminating-responses](group-terminating-responses.md)
- [group-acknowledged-start](group-acknowledged-start.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页288、119、121、122、117；仅本版本。
