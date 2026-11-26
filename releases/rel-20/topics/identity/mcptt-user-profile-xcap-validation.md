# MCPTT 用户配置档：按哪条 XCAP 路径找档，遇到 409 查什么？

**用已认证的 MCPTT ID 找用户目录，用 `user-profile-index` 找档。**同一用户可以有多份档。写入收到 HTTP 409 时，先区分正文里的 XUI 是否与文档 URI 一致、文件名是否按索引命名、目录里是否已有另一份预选档。这几项都可能返回 `constraint-failure`，仅凭状态码和该错误元素不能分因。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3。这里是已建立用户身份语境下的 MCPTT **用户配置档**，不是[主系统认证前默认档](primary-ue-online-configuration.md)，也不是迁入伙伴系统时用来发现 IdMS 的步骤。

## 文档路径里的用户与档案，是两个键

§8.3.1 把 MCPTT 用户配置档组织在该用户的 XDM 目录里；这里的 XCAP 用户指已认证用户的 **MCPTT ID**。§8.3.1A 给出客户端访问其中一份档的 URI 模板：

```text
CMSXCAPROOTURI/org.3gpp.mcptt.user-profile/users/sip:MCPTTID/mcptt-user-profile-INDEX.xml
```

- `org.3gpp.mcptt.user-profile` 是该应用的 AUID。相同 MCPTT ID 下，`INDEX` 对应配置档根元素的 `user-profile-index` 属性；§8.3.2.8 给索引 9 的文件名 `mcptt-user-profile-9.xml`，不把这一位填成用户名或 `ProfileName`。（§8.3.1A、§8.3.2.2、§8.3.2.7–.8）
- 根元素 `mcptt-user-profile` 必须有 `XUI-URI` 和 `user-profile-index`；Schema 类型分别为 `xs:anyURI` 和 `xs:unsignedByte`。`ProfileName` 是可选的档案名称元素；§8.3.1 和 §8.3.2.7 用它描述配置档的名字。不要把这个 XML 元素当成客户端 URI 模板里的 `INDEX`。（§8.3.2.1 项 1、4、6；§8.3.2.3、§8.3.2.7）

## 409 要看哪一项没有满足

| 线索 | 按本版条款判断 |
| --- | --- |
| **XUI 不符** | 正文根元素的 `XUI-URI` 必须与 **Document URI 的 XUI 值**一致；比的不是整条文档 URI，也不是配置档索引。两者不符时，XDMS 返回 HTTP 409 和 `constraint-failure`。若响应含 `phrase` 属性，建议用 `Wrong User Profile URI`。（§8.3.2.6） |
| **文件名不符** | 按索引命名，格式为 `mcptt-user-profile-<profile-index>.xml`；与客户端 URI 模板和索引 9 的示例一致。文件名不符时，XDMS 返回 HTTP 409 和 `constraint-failure`。若响应含 `phrase`，建议写明这个命名格式。本条没有规定怎样处理其他文件名或哪项校验先做。（§8.3.2.6、§8.3.1A、§8.3.2.8） |
| **同一目录两份都要预选** | 若同一用户已经有一份档含 `Pre-selected-indication`，再给另一份档加上它，XDMS 返回 HTTP 409 和 `constraint-failure`。若带 `phrase`，建议文字要指出**已有预选档的名称**，不是第二份档的名称。该段称名称元素为 `Profile-Name`；结构和 Schema 写的是 `ProfileName`，不要因此多建一个 XML 元素。（§8.3.2.6；§8.3.2.1、§8.3.2.3） |

`phrase` 只是可选的诊断属性；缺少它不排除上述任一分支。实际核查时，对照该次请求的 URI、XML 和同一用户的目录；§8.3.2.6 还列有其他约束，不能只从 409 选定上述原因。

## 没有预选元素，结果看用户目录有几份档

- **只有一份。**`Pre-selected-indication` 可省略；省略时，该唯一档仍默认预选。
- **多于一份。**正文规定只一份带 `Pre-selected-indication`。一份档没带这个元素，不表示它默认预选，也不推出终端会挑第一份。该元素是空类型；看是否出现，不读取真假值。

§8.3.2.6 和 §8.3.2.7 给出上述规则；它们没规定发现多份档但没有预选时的专用报错，也不规定怎样原子切换预选项。配置档被指定预选，不等于某台终端已经选用它。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-xcap-validation.json)
