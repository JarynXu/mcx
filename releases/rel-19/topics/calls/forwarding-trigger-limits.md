# 私呼转发何时触发，何时因限次拒绝

TS24.379 V19.4.0，终接参与功能处理私呼INVITE；先前检查未终止。本页沿已核转发分支，不包含迁移转发全貌。

## 即时转发

适用条件：allow-call-forwarding=true、call-forwarding-on=true、call-forwarding-condition=immediate。

若forwarding-immediate-list存在且达到max-immediate-forwardings，返回403+Warning174并停止；否则对原INVITE回480+175，另生成reason=immediate的转发MESSAGE。此480不能等同于后续新呼叫已经失败。

依据：§11.1.1.3.2 步骤4。

## 无绑定时无需先等TNP1

适用条件：目标MCPTT ID无公共身份绑定；允许且开启转发；条件为no-answer。

forwarding-other-list含至少一entry时403+174并停止；否则480+175并生成reason=no-answer的转发MESSAGE。无绑定未被特殊分支处理才404，不能把这里与MESSAGE接收端无绑定混为一谈。

依据：§11.1.1.3.2 步骤5–7。

## 已有邀请的未答超时

适用条件：私呼邀请；允许且开启转发；条件为no-answer。

发INVITE前启动TNP1；到期前收到200则停表并转送。到期先检查forwarding-other-list限次：含至少一entry则403+174并停止，未超限才CANCEL、480+175及转发MESSAGE。不能写成到期无条件CANCEL。

依据：§6.3.2.5。

## 证据边界

- TNP1数值及全部失败竞态尚未核验，不给统一超时秒数或重试保证。
- 本页触发MESSAGE不代表重呼成功；后续字段与路由见关联主题。

## 按需继续

- [forwarding-message-routing](forwarding-message-routing.md)
- [terminating-authorization](terminating-authorization.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页128、449、450；仅本版本。
