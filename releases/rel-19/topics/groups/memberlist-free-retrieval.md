# 按需取组文档：默认不取成员表

TS24.481 V19.3.0 Stage3；GMC向GMS读取组文档。

## 默认请求不含成员表的文档

适用条件：MCS用户需要组文档。

GMC默认采用不含成员信息的获取过程；用户需要成员信息时，才转入完整文档读取过程§6.3.3.2.1。这不是声明用户天然拥有读取完整成员表的权限。

依据：§6.3.16.1。

## 使用GMOP POST而非普通GET

适用条件：请求不含成员表的组文档。

GMC向按组ID寻址的组文档XCAP URI发送HTTP POST，body类型为application/vnd.3gpp.GMOP+xml；GMOP的request含get-excluding-memberlist元素。不能仅凭使用XCAP URI就把该操作改为GET。

依据：§6.3.16.2; 7.3.4.2。

## 响应缺少的是list子树

适用条件：GMS收到针对既有组文档、包含规定GMOP请求的POST。

服务器以HTTP 2xx返回指定文档，但不包含group/list-service/list元素；客户端只有在2xx同时带有§7.2.6所定MIME类型body时，才按不含成员表的文档处理。缺少list不能据此判断该组没有成员。

依据：§6.3.16.2–3。

## 证据边界

- 此过程不替代§7.2.12授权；HTTP认证依赖TS24.482，本页不声称已核其报文。
- 未核RFC9110完整POST语义、缓存及错误恢复；不把这一裁剪结果当全量文档进行覆盖写入。

## 按需继续

- [document-access](document-access.md)
- [resource-operations](resource-operations.md)
- [xcap-addressing](xcap-addressing.md)

[ETSI官方TS24.481 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)，印刷页33、34、67；仅本版本。
