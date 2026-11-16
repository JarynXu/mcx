# MCData TLV 信令逐段保护：谁解密，何时为下一段重新加密

依据 TS 24.282 V19.7.0 的 6.6，限普通在网单播的 Data signalling 信令面转送链，不把 XML body、Data signalling 和用户 Data 混为同一保护对象。

涉及解密或加密的分支均以该段相应协商或配置的密钥和标识可用为前提；本文不补密钥缺失恢复、协商流程或算法实现。

## 保护对象与启用条件

适用条件：判断信令面 MCData 消息应由哪一层保护，以及能否套用 XML 配置默认。

4.7 把用于通信识别和管理的 Data signalling 与真正用户或应用 Data 分开；6.6.1 把 SDS/FD SIGNALLING PAYLOAD、SDS/FD NOTIFICATION、FD NETWORK NOTIFICATION、COMMUNICATION RELEASE 等列为 Data signalling，而 Data 列为 DATA PAYLOAD。客户端与其 PF 的单播信令保护以协商为条件；PF—CF 信令保护以配置为条件。SIP 中有 XML 保护不能代替这些条件。

- 这里用等表明只列在网相关例项，不把列表删节说成完整枚举；6.6.1 还列离网消息，但其处理不在本主题范围。
- 本段未给出 XML 的配置元素缺失默认规则；不把 6.5 的 true/absent 默认移植到 TLV 协商或配置。
- SDS 经媒体控制面、FD 文件本身的保护另引 TS 24.582，本批未核。

依据：§4.7;6.6.1;6.6.3.1，印刷页 38、131、132、133。

## 客户端CPK文字不能静默更名

适用条件：客户端发送 Data signalling 且已协商该消息保护，或客户端收到已加密的 Data signalling，执行 6.6.3.2 末两段。

本客户端条款要求发送时加密、接收时解密，但密钥文字写 CPK 和 CPK-ID；接收对象还写成 media control。6.6.1 的同类 client—PF 单播关系及 6.6.3.3 的 PF 接收分支却写 CSK 和 CSK-ID。可确定角色有加解密职责，不能据此把 CPK 静默更正为 CSK 或 PCK，或宣称它们确定同义。

- 本条用于提示实现证据缺口，不提供自行修复的密钥映射；名称裁决需要额外规范依据或勘误。

依据：§6.6.3.2 final two paragraphs;6.6.1;6.6.3.3，印刷页 132、133。

## 发送侧参与功能重建出口保护

适用条件：PF 收到来自其服务客户端的已加密 Data signalling 消息，执行 6.6.3.3 的上行信令分支。

PF 使用与该发送客户端协商的 CSK/CSK-ID 解密。随后向 CF 转送时，如果该 PF—CF 段配置了保护，使用该段 SPK/SPK-ID 加密。前一段的密文不是直接作为下一段的保护结果透传。

- 出口保护条件必须单独成立；已加密入站消息不能证明出口保护已配置。
- 本段没有给出出口未配置保护、解密失败或缺少密钥时的完整错误响应或降级算法；不补成一律明文发送或一律拒绝。

依据：§6.6.3.3 second paragraph，印刷页 133。

## 控制功能转向目标参与功能

适用条件：CF 收到来自 PF 的已加密 Data signalling 消息，执行 6.6.3.4 的信令分支。

CF 用与来源 PF 配置的 SPK/SPK-ID 解密。向服务目标客户端的 PF 转送时，若相应 PF—CF 段配置了保护，则用该段 SPK/SPK-ID 加密。不能把来源 PF 的安全关联自动当成目标 PF 的安全关联。

- 不推定不同 PF 的 SPK 必须不同或必须相同，也不补其分发、轮换和选择算法。
- 未配置出口保护或保护处理失败的完整动作未在本分支展开。

依据：§6.6.3.4 second paragraph，印刷页 134。

## 目标参与功能使用自己的客户端段

适用条件：目标 PF 收到来自 CF 的已加密 Data signalling 消息，执行 6.6.3.3 的下行信令分支。

PF 用其与 CF 配置的 SPK/SPK-ID 解密；向目标客户端转送时，如果该 PF—客户端已协商保护，则使用该客户端段的 CSK/CSK-ID。保护是否协商必须针对目标段判断，不能因源客户端曾协商就视为目标客户端也已协商。

- 原句在出口写 using CSK/CSK-ID；本稿不扩成完整重编码步骤，也不以该 PF 文字解决客户端条款的 CPK 名称差异。
- 未协商出口保护或解密失败的具体 SIP 错误码不在本分支给出。

依据：§6.6.3.3 third paragraph;6.6.1，印刷页 132、133。

## 证据边界

- 仅核本版本指定在网信令面职责，不覆盖完整保护协商、密钥准备及失败恢复；不能将XML错误码或配置缺项默认外推到本页。

## 按需继续

- [security-layers](security-layers.md)
- [xml-protection-activation](xml-protection-activation.md)
- [sds-notification-routing](sds-notification-routing.md)
- [sds-disposition-aggregation](sds-disposition-aggregation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 来源中的未解细节

- §6.6.3.2 final two paragraphs versus 6.6.1 and 6.6.3.3，印刷页 132、133：客户端 Data signalling 分支使用 CPK/CPK-ID；同类链的一般说明与 PF 分支使用 CSK/CSK-ID。不自行裁决同义或更正成 PCK。
- §6.6.3.2 final paragraph，印刷页 133：接收 encrypted MCData Data signalling 的动作对象写 media control；保留原文措辞，不扩大成完整媒体控制协议处理。
