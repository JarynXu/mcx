# 初始配置引用默认用户档：配哪两个值，写入遇到 409 查什么？

**先在 CMS 建好目标档，再在初始配置里引用它。**引用用的是目标用户档的 XUI 和档案索引。两个值都存在还不够，它们得指向同一份档案。只看到 HTTP 409，不能判断是哪项不合要求。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§§4.1.1、7.2.2.1、7.2.2.3、7.2.2.6、7.2.2.7。这里校验的是 **MCS UE 初始配置文档**对默认用户档的引用，[不是校验目标用户档本身](mcptt-user-profile-xcap-validation.md)。

## 可不填；填了就用同一份档的两个值

初始配置文档的 `Default-user-profile` 元素可以省略。使用它时，结构和 Schema 要求这两个属性：

| 初始配置文档里的引用项 | 填什么 |
| --- | --- |
| `User-ID`（`xs:anyURI`） | 要用作默认档的 MCPTT 用户配置档中，`XUI-URI` 属性里的 XUI。不是设备 ID 或档案名。 |
| `user-profile-index`（`xs:unsignedByte`） | 同一目标档的 `user-profile-index` 值。即使只配了一份档，引用元素仍需要这个属性。 |

例如用户 A 只有索引 3，用户 B 有索引 7。填 A 的 XUI 和索引 7，不能借用 B 的档。§4.1.1 和 §7.2.2.6 的注要求先在 CMS 创建至少一份带有两项匹配值的用户配置档。注写目标档的 `XUI-URI`，引用侧仍按结构写 `User-ID`，不是多填一个 `XUI-URI` 属性。

## 三项校验都可能报同一个状态

以下三条各自适用。命中任一条所写的条件，CMS 须回 HTTP **409 Conflict**，带 XCAP `constraint-failure`。若包含 `phrase` 属性，原文建议用下列诊断；`phrase` 不是必填。

| 触发条件 | `phrase` 诊断 |
| --- | --- |
| `User-ID` 的语法不符合所引 RFC 3986 的 URI 规则 | `syntactically incorrect User ID URI` |
| 没有 MCS 用户配置档的 `XUI-URI` 对应该用户标识 | 提示该用户标识没有对应的 MCS 用户配置档，原文以 `No MCS User Profile configuration document exists` 起头。 |
| `user-profile-index` 没有指向该用户的一份 MCPTT 用户档 | 提示这一索引未标识该用户的一份配置档，原文以 `The user profile index does not identify` 起头。 |

没看到 `phrase` 时，核对**实际提交的两个值**和 **CMS 中的目标档**。别把一个 409 当成 URI 错、档案不存在或索引无效的唯一证明。本段没有给出检查顺序或多处不合格时的诊断优先级；其他校验也可能用 409。

## 不把引用、设备文件名和下载时机混在一起

- §7.2.2.10 的 “Resource interdependencies” 段写无资源相互依赖；同版 §7.2.2.6 仍写了上述校验和先建档的注。不要据前一段跳过引用校验，也不据此推导删档、级联更新或自动改选。
- §7.2.2.7 将两个属性分别指向 TS 24.483 §8.2.6 的 `UserID` 和 §8.2.7 的 `UserProfileIndex`；未核目标正文。§4.2.2.1.1 的写法是 MO 中的 `default-user-profile`；[主系统终端下载默认档是否更新](primary-ue-online-configuration.md)是另一件事，不由写入通过决定。
- 这个引用不是[管理员的共同初始配置模板或终端的初始配置 URI](initial-ue-config-xcap.md)，也不能用档案名 `ProfileName` 代替索引。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](default-profile-reference-xcap.json)
