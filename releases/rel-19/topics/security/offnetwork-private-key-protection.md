# 离网私呼的密钥分发、验证与保护边界

## 适用范围

- 限TS33.180 V19.4.0中普通离网MCPTT/MCVideo两用户私呼的密钥分发与保护；不包括MCData、组呼、first-to-answer、远程监听/查看、视频推拉、网关或跨域扩展。
- 本页说明安全上下文的前提、接收验证和离网媒体/控制材料关系，不替代各业务呼叫状态机、权限配置或媒体建立流程。新建呼叫的分发、收到密钥的验证及持有密钥后的使用各有独立入口。

## 离网私呼仍须先具备身份密钥材料

适用条件：开始普通离网MCPTT或MCVideo私呼的受保护密钥分发；手动或自动开始均在§7.2.3范围。

UE须先通过在网获取或离网配置取得所需个人密钥材料；两端的KMS材料与用户的MC service user ID关联。发现过程是可能已执行的前置步骤，不替代身份密钥配置。发起UE生成PCK，在发给终接UE的Call Setup Request中携带MIKEY-SAKKE I_MESSAGE：PCK封装给终接用户UID，带PCK-ID，并以发起用户UID关联的密钥签名。Call Setup Response仍按MCPTT或MCVideo业务规范返回；密钥分发不能替代业务接受与媒体建立判据。

- 本条不是在网§7.2.2的服务器转发及SDP承载过程，不将那一过程的路由、在线注册或KMS重定向分支直接移入离网建立。
- §7.2.3允许预生成建立消息，也允许附加加密给发起者的SAKKE-to-self分量；它们不是每次呼叫的强制条件，本页不展开多设备取钥。
- KMS实际配置、身份有效期刷新及发现协议未在本页闭合；离网不表示不需要预配置可信材料。

规范强度：§5.2.1个人材料取得为SHALL；§7.2.3按正文描述分发流程，may的发现、预生成与附加分量不得升为必须。

依据：TS33.180 V19.4.0 §5.2.1 private-communication paragraphs;7.2.3 opening and steps0–2，印刷页39, 70, 71。

## 终接端验证签名后才提取PCK

适用条件：终接实体实际收到本页I_MESSAGE，且采用的KMS可接受，按§5.2.2公共密钥提取机制处理。

终接实体从IDRi取发起者URI并转换为UID，用于检验I_MESSAGE签名；仅验证有效后，才用KMS配置的自身UID密钥提取并解密所封装密钥，同时取得密钥标识。公共机制中的UID结合实体URI与时间相关参数，呼叫开始前双方须持有KMS配置的限时身份材料。该机制保护密钥的机密性及载荷的完整性、真实性，不自动隐藏传送的身份。

- 本页未实现UID算法、时间窗口、重放检测、MIKEY解析及验证失败后的业务响应；不能把收到I_MESSAGE本身当成验证成功。
- 可接受KMS是提取入口条件；不从本页推导离网时一定能查询KMS、接受未知证书或完成重定向。身份掩码机制另见源文Annex E.7，本页未展开。

规范强度：公共机制明确以签名有效作为解密提取条件；限时身份材料配置为SHALL，身份可见性边界来自NOTE，不提升为额外隐藏义务。

依据：TS33.180 V19.4.0 §5.2.2 common distribution and extraction paragraphs;7.2.3 step1，印刷页39, 40, 71。

## 离网私呼控制使用PCK上下文，而非在网服务器信令密钥

适用条件：私呼成员已共享并接受PCK及PCK-ID，使用RTP媒体，MC客户端处于离网操作。

§7.4.1以PCK作MIKEY TGK、PCK-ID作CSB-ID、PCK下发的RAND及规定CS-ID派生SRTP master key和master salt，须支持PRF-HMAC-SHA-256；MKI为purpose tag为1的32位PCK-ID。§7.5.1规定RTP媒体采用SRTP完整性及机密性保护。离网时，PCK也用于话权、发送控制与媒体控制的SRTCP：§7.4.1明确其master key、master salt及MKI与SRTP对应材料相同；§9.4.4相应给出私呼KFC=PCK、KFC-ID=PCK-ID。

- 这里相同的是master材料及MKI，不推出SRTP与SRTCP最终会话密钥相同，也不把PCK直接作为媒体会话密钥。CS-ID表、完整SRTP/SRTCP profile及算法实现仍是接口依赖。
- §9.4.4将私呼PCK/组GMK回指§7.3.4，但该条标题是Broadcast group call；保留该回指差异。私呼离网共享master材料的直接依据是§7.4.1，不用组GMK规则补私呼。
- 不将此离网控制规则用于在网逐跳控制，也不据密钥具备推定已获话权、发送许可、自动接受或全部业务控制消息均受同一机制保护。

规范强度：§7.4.1派生输入、MKI及PRF支持和§7.5.1 RTP保护保留SHALL；离网master材料对应及§9.4.4 KFC映射按正文陈述，不改写为整个业务安全已验证。

依据：TS33.180 V19.4.0 §7.4.1;7.5.1 opening;9.4.4;TOC 7.3.4 heading (reference comparison only)，印刷页5, 85, 86, 87, 105。

## 整体边界

仅核明列的安全义务与接口关系，不提供完整密码实现、完整重放/证书策略或所有业务消息的端到端安全验收。

## 相关主题

- [private-key-distribution](private-key-distribution.md)
- [group-media-control](group-media-control.md)
- [ue-key-lifecycle](ue-key-lifecycle.md)
- [kms-provisioning](kms-provisioning.md)
