# MCPTT 业务配置报 409：查请求目标的 AUID，还是正文的组织域名？

**先确认请求目标是 MCPTT 业务配置文档或其中的节点。**再分别查 `Request-URI` 里的应用用法标识 AUID，以及文档参数块里的组织域名 `domain`。下列三种情况都要求配置管理服务器（CMS）返回 **HTTP 409（Conflict）**，含 XCAP 错误元素 `<constraint-failure>`。只看状态码或错误元素，分不出这次是哪项不符。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.6；业务 AUID 见 §8.4.2.2，参数块和组织域见 §8.4.2.3/.7。

| 检查位置 | 什么条件要求返回 409 | 若响应带 `phrase`，建议用 |
| --- | --- | --- |
| `Request-URI` 中的文档 URI 或节点 URI | 它的 AUID 不等于 `org.3gpp.mcptt.service-config` | `invalid application id used` |
| `<service-configuration-params>` 的 `domain` 属性 | 值不包含语法正确的域名 | `syntactically incorrect domain name` |
| 同一个 `domain` 属性 | 值包含未知域名 | `unknown domain name` |

`phrase` 可以不带。语法正确并不证明域名已知；两项要分别核对，条文没写先查哪项、从哪里查域名是否已知。DNS 失败不足以单独判定后一项，也不能从一个错误短语反推其他检查都通过。

## 请求路径与组织域名各查一处

`domain` 记录任务关键组织的域名。Schema 将其声明为必填的 `xs:anyURI`；符合该类型不代替两项域名检查。**属性没写**与**属性值不符合要求**要分开。缺属性不符合该声明，但不能只凭这两句为它指定某个 `phrase`。如果只看到 XCAP 节点请求的一小段内容，也不能据此判整份文档缺该属性。

业务配置的[组织文档路径](mcs-server-service-config.md)在 `global` 树。不要用 URI 主机名、`global` 下的组织目录或文件名填补正文的 `domain`；也不要从可能有误的 AUID 倒推真正请求的是哪项业务。URI 写对、域名已知，仍不证明访问获准或这次写入成功。（§8.4.2.3/.7/.9）

## XUI 为什么不能照搬 MCVideo、MCData？

[MCVideo、MCData 的业务配置校验](mcvideo-mcdata-service-config-validation.md)在 §9.4.2.6、§10.4.2.6 明写两处 URI 的 XUI 不匹配时的 409。MCPTT **业务配置**的 §8.4.2.6 没有这条对应句，不能将它作为 MCPTT 此处的第四项。这个区别不是 MCPTT 的 XUI 通用豁免；例如 [MCPTT 用户配置档](mcptt-user-profile-xcap-validation.md)的 §8.3.2.6 核对正文根元素的 `XUI-URI` 与文档 URI 的 XUI，不是业务配置里两处 URI 的比对。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-service-target-domain-validation.json)
