# 功能别名私呼：解析、300与重新邀请

TS24.379 V19.4.0，在网按需、带话权控制private/first-to-answer；不包含转接、转发别名流程。

## 区分目标别名与主叫别名

适用条件：按功能别名发起私呼。

目标别名置于resource-lists，call-to-functional-alias-ind=true。不要把它与描述主叫的functional-alias-URI混淆。

依据：§11.1.1.2.1.1 步骤9、14c。

## 查询已激活者

适用条件：业务流程需要解析功能别名。

向别名所属控制功能PSI发SUBSCRIBE，消息体携带目标别名以查询成功激活者，Expires=0。需要持续通知时，注释允许4294967295；PSI发现算法未规定。

依据：§9A.2.2.2.8。

## 普通私呼先选一个用户

适用条件：控制功能处理private，call-to-functional-alias-ind=true，且此前检查未终止流程。

解析无ID时403+Warning145并停止；否则选一个ID，生成300并停止其余步骤。选择由实现决定；300消息体mcptt-request-uri给选中ID，Contact给会话identity。

依据：§11.1.1.4.2 步骤8a。

## 客户端重新邀请

适用条件：普通private按功能别名发起，客户端收到对应控制功能选定目标的300。

使用300消息体mcptt-request-uri中的选中ID（不是Contact会话identity）构造新initial INVITE的resource-lists，移除call-to-functional-alias-ind，以called-functional-alias-URI保留原目标别名。这是继续发起，不能把300当作接听成功或授权豁免。

依据：§11.1.1.2.1.1 收到300分支。

## FTA不套普通私呼单选链

适用条件：控制功能处理first-to-answer，且call-to-functional-alias-ind=true。

解析无ID同样403+145；有ID则将原资源列表的别名URI记录为called-functional-alias-URI，并邀请解析出的ID(s)，不是先按普通private发送300。

依据：§11.1.1.4.2 步骤12。

## 证据边界

- 别名激活并发、完整SUBSCRIBE事务与解析后的密钥处理未在本页完整核验。
- 300段MIME名缺+xml、FTA步骤12b称private request，保留文本异常，不由此生成完整报文模板。

## 按需继续

- [originating-authorization](originating-authorization.md)
- [first-to-answer-selection](first-to-answer-selection.md)
- [../identity/functional-alias](../identity/functional-alias.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页251、252、415、417、421、455、456；仅本版本。
