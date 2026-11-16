# 服务器释放私呼：触发、REFER确认与BYE

TS24.379 V19.4.0的选定私呼服务器释放链；结合§11.1.4.1，无话权私呼仅由客户端发起结束，不把服务器触发规则无限外推。

## 私呼释放触发条件

适用条件：控制功能适用私呼会话释放策略。

收到媒体层T4 inactivity到期指示、会话时长超过私呼最大时长、会话只剩一名或没有参与者，任一条件成立须释放。此处不规定T4值或最长时长配置值；不能用群组TNG3替代。

依据：§6.3.8.2；11.1.4.1。

## 控制侧发送BYE

适用条件：控制功能需移除私呼参与者。

发送BYE前与媒体层交互，收到该BYE的200后再进行关联媒体资源释放；不将组呼TNG3特例并入私呼。

依据：§6.3.3.1.5；6.3.3.2.4。

## 控制侧收到BYE

适用条件：控制功能收到私呼BYE。

先媒体处理并回200，再检查会话释放策略；需释放其他参与者时按发送BYE程序处理，并复制已有mcptt-info；不将adhoc授权特例并入私呼。

依据：§6.3.3.1.5；6.3.3.2.4。

## 按需客户端BYE经参与功能转送

适用条件：参与功能收到按需私呼客户端的BYE。

媒体处理后生成面向控制功能的新BYE，目标取收到的会话identity，PAI为参与功能PSI，复制已有mcptt-info。收到下游200后回客户端200并处理媒体释放。

依据：§6.3.2.1.6；11.1.3.2.1.1。

## REFER的200早于下游释放

适用条件：客户端预建立会话REFER的Refer-To含method=BYE。

参与功能先从PAI查身份绑定，无绑定返回403+Warning141并停止。通过后先回REFER的200，再向Refer-To目标发BYE，PAI为参与功能PSI并复制已有mcptt-info；收到BYE的200后处理媒体释放。因此REFER200不能证明下游BYE及全部释放已完成。

依据：§6.3.2.1.7；11.1.3.2.1.2。

## 不建立隐式订阅的条件

适用条件：参与功能收到客户端Refer-To含method=BYE的REFER，已找到PAI公共用户身份与MCPTT ID的绑定，且请求同时含Refer-Sub=false及Supported=norefersub。

不建立隐式订阅。响应声明Supported=norefersub。响应回Refer-Sub=false只以请求该字段为false为条件，不要求同时具备Supported；两字段联合条件用于不建立隐式订阅，不能仅凭BYE方法推断无订阅。

依据：§6.3.2.1.7。

## 证据边界

- TS24.380媒体行为、T4值、最大时长数值、SIP/REFER完整事务及边界竞态未核验。
- §6.3.2.1.6响应段角色称terminating，与所在originating章节不一致，保留该文字疑义。

## 按需继续

- [release-signalling](release-signalling.md)
- [without-floor-control](without-floor-control.md)
- [first-to-answer-selection](first-to-answer-selection.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页109、110、131、149、164、464、465；仅本版本。
