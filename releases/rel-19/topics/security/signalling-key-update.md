# 信令密钥更新：初始CSK、替换和组播退回单播

TS33.180 V19.4.0 §9.2；MC客户端和MCX服务器信令保护，不是媒体PCK/GMK分发。

## 客户端先生成并上传CSK

适用条件：客户端已从KMS取得用户专属密钥材料，初次连接MC服务器。

客户端随机生成128位CSK并按CSK upload封装，通过用于MC用户授权的初始REGISTER或PUBLISH发往服务器PSI。服务器提取CSK后才能解密该消息中用相应机制保护的用户信息。此密钥建立不替代access token校验。

依据：§9.2.1.2；9.2.1.3。

## 更新按服务器关联替换

适用条件：服务器决定更新CSK，客户端成功收到key download中的新CSK。

服务器可因撤销、到期等原因在任意时点决定更新，并通过key download分发。客户端从CSK-ID最高4位识别密钥类型，丢弃与该MC Server FQDN关联的旧CSK，并使用新CSK发送上行信令。不能将这一替换解释为删除所有服务器的密钥。

依据：§9.2.1.4。

## 组播保护有独立密钥和回退条件

适用条件：服务器需要受保护的MBMS组播信令。

MuSiK通过key download下发；可采用覆盖普通组播信令的MuSiKAll（不含bearer announcement），也可在需要组相关信令且组配置要求密码保护时下发MuSiKGRP。服务器可以为隐私需求单独分配，不要求每建立一个新承载都重新分配。若客户端拒绝MuSiK，服务器向该客户端分发信令时只能使用单播承载。

依据：§9.2.2。

## 证据边界

- CSK upload、key download的完整MIKEY报文、服务授权失败映射和服务器重启恢复未覆盖。
- 拒绝MuSiK的单播回退是信令规则，不能扩展成所有媒体也自动回退。

## 按需继续

- [kms-provisioning](kms-provisioning.md)
- [group-media-control](group-media-control.md)
- [ue-key-lifecycle](ue-key-lifecycle.md)
- [../identity/service-authorization](../identity/service-authorization.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页97、98、99；仅本版本。

## 停用不等于物理删除

§9.2.1.2规定CSK使用至需要新CSK、SIP会话拆除、用户退出或其他指示。停止使用与UE材料保存分别判断，不能因密钥仍在存储中就继续使用。

- [MCData的CSK下载验证与替换入口](../mcdata/csk-key-download-validation.md)
