# 主叫参与功能：身份绑定、私呼权限与控制功能路由

仅 TS24.379 V19.4.0 §11.1.1.3.1.1 的在网按需、带话权控制的 private/first-to-answer INVITE。以下为选定主干，不含完整转接、功能别名或紧急策略。

## 由PAI找用户，再找控制服务

适用条件：已进入 originating participating 流程。

从P-Asserted-Identity的公共用户身份取得MCPTT ID。绑定不存在或过期：404+Warning141；找不到该用户对应私呼或first-to-answer控制功能：404+Warning142。控制PSI的发现算法与跨域出口网关选择不由此节规定。

依据：§11.1.1.3.1.1 步骤3–7。

## 业务权限不是注册成功的同义词

适用条件：检查请求资源和用户配置。

缺resource-lists，或普通私呼的resource-lists中一个list包含多个entry，返回403+145。allow-private-call缺失或false返回403+107。普通私呼收到Answer-Mode: Auto/Manual而相应allow-automatic/manual-commencement缺失或false，分别403+125/126。未转接、未转发、非功能别名的普通私呼，若非空PrivateCall名单不匹配且未允许名单外呼叫，则403+144。

依据：§11.1.1.3.1.1 步骤8–11e。

## 强制自动接听有独立主叫许可

适用条件：普通私呼包含模式头。

Priv-Answer-Mode=Auto只有allow-force-auto-answer为true才传出，否则403+143；收到Priv-Answer-Mode=Manual不向外包含该特权头。未输出特权Auto时，按本节复制已有普通Answer-Mode。此处仅按需INVITE，不套用预建立REFER规则。

依据：§11.1.1.3.1.1 步骤18。

## 路由身份与业务用户身份分开传递

适用条件：前置检查通过，继续发送。

Request-URI设为控制功能PSI，消息体mcptt-calling-user-id设为主叫MCPTT ID。回传200时保留收到的P-Answer-State，并映射MCPTT session identity；因此上游200的应答状态仍需读，不能仅凭状态码证明被叫已接听。

依据：§11.1.1.3.1.1 步骤16–17及200响应处理。

## 证据边界

- 各拒绝条款有各自前提，不是无条件按错误码推断唯一根因。
- TS24.484配置全貌、RFC身份信任规则和完整24.229尚未核；不提供可部署的PAI信任策略。
- 本节步骤18d对步骤17的引用与邻近步骤编号不一致；不据此发明额外行为。

## 按需继续

- [terminating-authorization](terminating-authorization.md)
- [control-routing-results](control-routing-results.md)
- [commencement-selection](commencement-selection.md)
- [../identity/service-authorization](../identity/service-authorization.md)

[ETSI 官方 TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页436、437、438、439、440、441；仅本版本。
