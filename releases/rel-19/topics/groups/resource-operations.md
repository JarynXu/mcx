# 组文档操作：先选资源层级，再选 HTTP 方法

适用：Rel19，TS24.481 V19.3.0，Stage3，§6.3.3–12。HTTP 方法相同，不代表操作范围相同；Request-URI 必须定位本次操作的对象。

| 目标 | 读取 | 创建/替换或更新 | 删除 |
|---|---|---|---|
| 整份组文档 | GET，§6.3.3 | PUT更新，§6.3.4；新建另见[建组](creation.md) | DELETE，§6.3.5 |
| XML元素 | GET，§6.3.8 | PUT创建/替换，§6.3.6 | DELETE，§6.3.7 |
| XML属性 | GET，§6.3.11 | PUT创建/替换，§6.3.9 | DELETE，§6.3.10 |
| namespace bindings | GET，§6.3.12 | 本流程不提供 | 本流程不提供 |

namespace selector 不得用于 PUT 或 DELETE（[RFC4825 §7.10](https://www.rfc-editor.org/rfc/rfc4825.html#section-7.10)）；这限制的是该 selector 的操作，不等于禁止一切会改变文档 namespace 声明的编辑。

整文档读取明确供 GMC 与 MCS server 使用；这些修改和细粒度流程描述的是 GMC，不能自动扩展主体权限。更新文档须按 §7.2.1 的 application usage 构造 XML。

实现时必须继续满足所引 RFC4825 的 selector、MIME和服务器处理约束。本页没有核完完整组文档 schema、MIME及所有寻址规则，不提供可执行请求模板。知道 URI 或选对方法，也不意味着已获[读取权限](document-access.md)。并发修改先读 [ETag与412](conditional-update.md)，持续跟踪变化则读[订阅资源与SIP地址](change-subscription.md)。

[TS24.481 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)，印刷页16–20。

需要构造地址时读 [XCAP 寻址](xcap-addressing.md)；需要判断请求正文、替换范围或 409 时读 [写入校验](xcap-write-validation.md)。
