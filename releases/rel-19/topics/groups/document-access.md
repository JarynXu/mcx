# 组文档寻址与成员表权限

Release 19；TS 24.481 V19.3.0。所列规则已对照[规范原文](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf#page=65)核对，不代表完整授权实现已验证。

## 按组 ID 访问不会增加权限

按组 ID 寻址的文档沿用其关联 users-tree 文档的管理授权；全局路径不是公开访问许可。依据：§7.2.12.2，正文第 65 页。

## 成员身份不自动允许读取全表

在“组成员读取成员表”这一授权分支，还须匹配文档中的 rule：conditions 为真或缺省，且 actions 含 on-network-allow-getting-member-list。依据：§7.2.12.1，正文第 64 页。

该成员分支不是全部授权规则，其他读取与写入分支如下。本文不提供完整权限算法、身份认证或XCAP实现。

## 其他读取分支

组成员可读list-service及非list后代；自己的entry及后代另有身份匹配分支，匹配entry URI、mcvideo-mcvideo-id URI或mcdata-mcdata-id URI之一。获授权MCS服务器列表中的身份可读整份文档。不要把读取本人entry等同读取全体成员。

依据：§7.2.12.1。

## 所有者仍受明确禁止规则约束

适用范围：本人XUI用户树，或另一XUI用户树且提供方政策允许。

创建、读取、修改、删除权限仍受本条其他禁止规则约束：既有组文档的on-network-temporary不能创建、删除或修改；含on-network-regrouped的组文档不能删除。授权GMS可在既有文档创建和删除on-network-regrouped元素。所有者并非无条件管理员。

依据：§7.2.12.1。

## 两个地址不是两个独立副本

byGroupID文档与users树的关联文档内容相同并随其创建；经byGroupID修改或删除会作用于关联文档，不能把它视为可独立清理的缓存副本。此条未给出并发或分布式事务保证。

依据：§7.2.11.2。

成员表规则的actions元素存在条件不能脱离§7.2.8的布尔语义：false表示不允许。本页不提供完整OMA求值器。

相关：[不取成员表](memberlist-free-retrieval.md)、[临时组生命周期](temporary-group-lifecycle.md)、[GKTP](gktp-access.md)、[跨域转发](forwarding.md)。

进一步核对：[代理和拥有方授权](subscription-proxy.md)、[未知扩展处理](unknown-extensions.md)。
