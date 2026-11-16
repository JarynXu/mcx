# GKTP：资源存在、订阅授权与密钥接收者

TS24.481 V19.3.0 Stage3；GKTP文档承载组密钥传输payload，与普通组配置文档区分。

## 建组时建立关联资源

适用条件：创建users树中定义组ID的组文档。

GMS同时建立关联GKTP文档；GMK生成取决于组文档媒体、话权控制和组播话权控制保护字段的存在、缺省和值。资源存在本身不证明一定存在某种密钥。

依据：§7.7.11。

## XCAP寻址不意味着允许XCAP管理

适用条件：访问GKTP文档。

GKTP文档不得用XCAP管理，可以经SIP获取。SIP获取完整文档或片段使用application/xcap-diff+xml；名称含xcap不改变这个限制。

依据：§7.7.6; 7.7.12。

## 订阅者须符合GKTP自己的授权分支

适用条件：已认证身份订阅GKTPs变化。

授权条件是该身份为关联组成员，或该身份列于授权GMS列表且代表该关联组的一个组成组订阅。不能把普通组文档中其他服务器的授权分支直接搬到GKTP。

依据：§7.7.12。

## 有订阅权不代替载荷接收者和签名检查

适用条件：MCPTT组不是组成组，读取GMK或MKFC的GKTP。

GMK载荷加密给访问用户的MCPTT ID；在网组播话权控制的MKFC载荷可加密给访问用户或访问MCPTT服务器的身份，二者均由GMS签名。这里不把GKTP订阅授权等同密钥解密、验签成功。

依据：§7.7.8。

## 证据边界

- 本页不实现密码算法或完整SIP订阅状态机。
- GMK/MKFC接收者结论限所述非组成MCPTT组分支；重组载荷另有子元素与临时组ID关联。

## 按需继续

- [constituent-subscription](constituent-subscription.md)
- [temporary-group-lifecycle](temporary-group-lifecycle.md)
- [../security/group-key-distribution](../security/group-key-distribution.md)

[ETSI官方TS24.481 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)，印刷页75、76、77；仅本版本。
