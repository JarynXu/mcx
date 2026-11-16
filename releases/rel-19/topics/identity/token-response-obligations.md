# 令牌响应字段：两个 Rel19 规范版本不能静默合并

比较 TS24.482 V19.0.0 与 TS33.180 V19.4.0 的选定条款。此处记录证据差异，不为部署选择规范优先级。

## 协议文本要求成功响应包含三类 token

适用条件：收到相应 Token Request，验证有效并生成成功响应。

TS24.482 V19.0.0 要求包含 ID、access、refresh token。§6.3.1 另包含 MC service ID，§6.3.3 的伙伴响应原文写 MCPTT ID。不能将后者默改成所有服务的统一字段。

依据：§6.3.1; 6.3.3。

## 安全规范表格保留可选字段

适用条件：以 TS33.180 V19.4.0 的对应响应表为依据。

两个表格均将 access token 列为 REQUIRED，将 ID 与 refresh token 列为 OPTIONAL；B.4.2.5 开头又描述返回三类 token。不得只选一句改写成整个 Rel19 的统一必选规则。

依据：§B.4.2.5 表B.4.2.5-1; B.7.5 表B.7.5-1。

## 先定位同一业务步骤，再保留未消解义务

适用条件：需要把两个规范的响应规则组合使用。

首次认证码响应与伙伴 JWT bearer 响应分别对应上述两组表格，不是把首次认证误比成刷新。协议进一步收紧字段是可能解释，但所核条款未明确给出消解说明。home 签发 security token 的 §6.3.2 是另一阶段，不能用其字段替换伙伴成功响应。

依据：§6.2.1; 6.2.3; 6.3.1; 6.3.3。

## 证据边界

- 未比较后续规范版本或变更请求；不能宣布此差异已在后续版本修复。
- 未核完整 OIDC/RFC；不提供猜测的兼容回退、缺字段容错或错误码。
- 24.482 §6.2.3 写 RFC7253 [19]，而参考文献 [19] 是 RFC7523；§6.3.1 将302对象写成 request method，并用 authorization_code 称呼返回码。这些文字不能直接生成线协议字段。

## 按需继续

- [native-authentication](native-authentication.md)
- [partner-token-exchange](partner-token-exchange.md)
- [http-sender-identity](http-sender-identity.md)

[TS24.482 V19.0.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124482/19.00.00_60/ts_124482v190000p.pdf)，印刷页9–13；[TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页132、136、138。
