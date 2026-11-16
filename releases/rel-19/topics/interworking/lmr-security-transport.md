# LMR 安全消息：透明载荷与 MCData 承载

TS23.283 V19.5.0，Release 19，Stage 2。

LMR安全信息可在IWF与具备LMR感知能力的MC客户端之间传递，不要求MC服务服务器理解载荷。

## 选择跨MC系统的LMR安全消息承载

端到端消息在业务语义上独立，但3GPP传输仅通过MCData实现；不能据业务独立推断任何MC服务都有同一传输实现。 [§10.12.2.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## MC客户端已注册，用户已认证且获授权使用MC服务服务器

客户端发起时，经MC服务服务器转发给IWF；IWF发起时反向经服务器转给客户端。安全消息内容对MC业务透明，内容和格式不在3GPP范围；转发不等于服务器解释或完成LMR密钥管理。 [§10.12.2.2–3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 构造Non-3GPP security message信息流

发送与目标安全实体对应的两个MC service ID及透明载荷为必需；LMR type一般标为可选，但向MC客户端发送时必需。 [§10.12.1.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

这里只覆盖安全消息运输，不提供LMR密钥格式、端到端密码算法或TS33.180的MC密钥获取流程。

Stage2信息元素不是Stage3编码；与IWF解密转码所需MC密钥管理分开判断。

[加密转码及MC密钥前提](encrypted-transcoding.md) · [互通范围](scope.md) · [结构化条件](lmr-security-transport.json)
