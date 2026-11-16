# 跨服务商组文档转发

适用：Release 19，TS 24.481 V19.3.0；GMS 收到按组 ID 寻址的 HTTP 请求，且该 ID 属于另一 MCS 服务商。

组 ID 路由数据库映射到对方的 XCAP root URI 及文档访问 public service identity（§6.2.5.2，p14）。

GMS 用该映射替换 Request-URI 的 XCAP root；缺少 X-3GPP-Asserted-Identity 时，按 TS 24.482 确定发送者身份后补入；存在 Authorization 时删除，再转发（§6.2.5.3，p14）。

这是指定条件下的转发规则，不得原样转发 Authorization 头。身份如何认证、路由缺失如何报错及 TLS 细节不在本页覆盖范围；不能据此信任任意外来身份头或跳过授权。

[结构化条件](forwarding.json) · [来源](../../sources.json) · [组文档授权](document-access.md)
