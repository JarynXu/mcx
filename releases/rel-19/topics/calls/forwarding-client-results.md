# 转发结果与映射授权为何不能等同接通

在网私呼转发 MESSAGE 到达原主叫后的会话路径选择、按需重呼、结果 MESSAGE 与映射授权衔接。预建立分支只覆盖明确已核的入口和转发专用字段，不宣称完整 REFER/SIP/媒体实现。

forwarded-calling-client是原主叫；forwarded-by-client是请求转发的原被叫；forwarded-to-client是新目标。

## 结果MESSAGE可在180之后生成

适用条件：所调用重呼程序已经收到 SIP 180 或 SIP final response。

生成结果 SIP MESSAGE：resource-lists/entry@uri 取收到的 forwarded-by-mcptt-id；mcptt-Params/mcptt-called-party-id 为新目标 forwarded-to-client 的 MCPTT ID；anyExt/response-type=forwarding-private-call-response；按发起程序是否成功填 forwarding-call-outcome=success 或 fail。Request-URI 按原文设为服务 forwarded-by-client 的 participating function PSI，并发送。

依据：§11.1.9.2.2 after steps 1–4。

## 原被叫接收业务结果

适用条件：原转发请求方收到 forwarding private call response 的 SIP MESSAGE。

从 forwarding-call-outcome 判断转发请求成功/失败，生成并发送 SIP 200；SHOULD 向用户显示结果。

依据：§11.1.9.2.1 response handling。

## 交付转发MESSAGE时缓存映射

适用条件：PF向原主叫交付转发request的MESSAGE。

终接侧按mcptt-request-uri取得绑定；转发request分支原文从mcptt-called-party-id取目标并缓存二者映射，并发请求需多份映射。字段衔接未闭合，见证据边界。

依据：§11.1.9.3.2 steps 2–5; 11.1.1.3.1.1 step 11d。

## 后续INVITE校验映射

适用条件：O-PF收到call-forwarding-ind=true的private INVITE。

没有forwarded user与target的缓存映射时，返回403+Warning173并停止。有缓存仍不替代一般私呼授权。

依据：§11.1.9.3.2 steps 2–5; 11.1.1.3.1.1 step 11d。

## 手动转发的两层许可

适用条件：手动转发请求及其 originating PF 请求处理，非笼统涵盖全部自动转发。

手动输入转发只适用于 manual commencement。客户端 allow-call-fwd-manual-any 缺失/false 时 SHOULD 告知未授权并 SHALL 停止。O-PF 从 PAI 映射用户，缺失/过期 404+141；当 request-type=forward-private-call-request 且 allow-call-forward-manual-input 缺失/false 时 403+173 并停止。

依据：§11.1.9.2.1 step 1; 11.1.9.3.1 steps 2–4。

## 请求事务失败

适用条件：转发请求方收到此前请求MESSAGE的4xx/5xx/6xx。

应告知用户请求失败并退出流程，不以先收到业务结果MESSAGE为前提。

依据：§11.1.9.2.1，p507。

## 证据边界

- 触发条件不是只能收到 200，也不能把 180 直接定义为新被叫已接听。
- 原文此处未给 success 的额外充要判据，不自行定义 180=success 或规定每个后续响应都重新发一次结果。
- Request-URI 原文指 forwarded-by-client 的 PF，不静默改成发送客户端自身 PF。
- 请求事务 2xx、业务结果 MESSAGE 及新目标呼叫建立是不同结果；链接已有 forwarding-message-routing。
- 字段衔接未闭合：控制功能 request 分支写 forwarding-target-id，客户端也读 forwarding-target-id，但映射缓存条款读 mcptt-called-party-id；不得静默统一字段。
- 已查 6.3.2.2.11 和其 MIME 复制依赖 6.3.2.2.9（p125–126），只规定复制而未发现补该字段的转换。
- 映射有效期、消费/删除以及所有并发匹配规则未核，不制造一次性令牌或长期授权语义。
- 有缓存不是全部私呼授权成功，通用权限仍链接 originating-authorization。
- 客户端和服务器使用的配置字段名确实不同，不互相替换；TS24.484 全部配置定义未核。
- O-PF 权限条件是 request-type，不擅自添加仅 forwarding-reason=manual-input 才检查的限制。

## 按需继续

- [forwarding-client-reorigination](forwarding-client-reorigination.md)
- [forwarding-message-routing](forwarding-message-routing.md)
- [originating-authorization](originating-authorization.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页437、506、507、508、509、510；仅本版本。
