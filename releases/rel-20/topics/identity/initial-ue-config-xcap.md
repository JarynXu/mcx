# MCS 终端初始配置：默认模板在哪，终端用哪个 XCAP URI？

**取共同的 MCS UE 初始配置文档，XCAP 地址用设备 ID。**专配和默认模板对应的终端 URI 相同。没有专配时，配置管理服务器（CMS）用管理员的主模板生成该终端的初始配置文档；终端不改用主模板的文件名。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§§7.2.1.0–7.2.1.1、7.2.2.1–7.2.2.3、7.2.2.7。这里讲文档属于谁、URI 怎么定位。下载时点另查[主系统在线配置](primary-ue-online-configuration.md)。

## 管理员的模板不占用终端的 URI

主初始配置模板在 MCS 管理员的用户目录。不含设备筛选元素时，默认模板叫 `DEFAULT-MCPTT-INITIAL-UE.xml`，适用范围是该任务关键组织的 MCS 终端。为特定设备配置时，标准用终端的实例 ID 对照配置文档里的筛选条件。例如文档列出 `Instance-ID-URN` 时，这一条件按实例 ID 相等来判断。模板名带 `MCPTT` 是历史命名，不能据此把共同初始档限于 MCPTT。（§7.2.1.0、§7.2.2.7）

管理员未提供这台终端的专用初始配置文档时，CMS 须从主模板生成该终端的文档，在生成的文档中设置该客户端的 UE ID。具体文档放在 `users` 树中该设备对应的目录，文件名对应设备 ID。§7.2.1.1 没说收到取档失败就改取主模板，也没规定多份专用文档都匹配时的选择顺序。

## 看 AUID 和两个路径位置，不要只看 `mcptt`

| 要读的文档 | 规范给的 URI 模板 | `users` 下的身份 / 最后一段 |
| --- | --- | --- |
| 共同的 MCS UE 初始配置（§7.2.1.1） | `CMSXCAPROOTURI/org.3gpp.mcptt.ue-init-config/users/sip:MCSUEID/MCSUEID` | 设备 ID / 同一设备 ID |
| MCPTT 业务 UE 配置（§§8.2.1、8.2.1A） | `CMSXCAPROOTURI/org.3gpp.mcptt.ue-config/users/sip:MCPTTID/MCSUEID` | 已认证用户的 MCPTT ID / 对应的设备 ID |
| [MCPTT 用户配置档](mcptt-user-profile-xcap-validation.md)（§§8.3.1、8.3.1A，对照） | `CMSXCAPROOTURI/org.3gpp.mcptt.user-profile/users/sip:MCPTTID/mcptt-user-profile-INDEX.xml` | 已认证用户的 MCPTT ID / 按档案索引的文件名 |

前两行的最后一段按原文是设备 ID，没有固定的 `.xml` 后缀。

例如，同一 CMS 下，两名用户分别用同一台设备完成认证，也都获准在这台设备使用 MCPTT。查询业务 UE 配置时，两条 URI 的 MCPTT ID 不同，末段的设备 ID 相同。查询共同初始配置时，URI 不因换用户而变。路径写对不等于授权通过。

## 看不到筛选字段时，先分清文档和管理对象

§7.2.1.1 讲的是 CMS 生成具体的 **初始配置文档**，并在其中设置设备 ID。§7.2.1.0 讲的是另一个产物：与 CMS 共置的设备管理服务器用初始配置文档作模板，生成配置给终端的 **TS 24.483 初始配置管理对象（MO）**。

§7.2.2.7 的范围判断以承担筛选的初始配置文档为准。文档有 `mcptt-UE-id` 时，**文档和对应的 MO 都只适用于该项标识的 MCS UE**。文档无此项时，文档和对应的 MO 都适用于该域的所有 MCS UE。筛选项可见于上传给 CMS 或管理员下载的初始配置文档，但这两种范围下，配置给终端的 MO 都不带此项。只看到 MO 缺这个字段，不能判断它适用哪些设备，也不能说明 CMS 没按设备选档或生成文档。

生成段把元素写作 `<MCPTT-UE-id>`；§7.2.2.1 的结构、§7.2.2.3 的 Schema 和 §7.2.2.7 的语义使用 `<mcptt-UE-id>`。Schema 将它声明为复杂类型；不要把生成段的文字说明当成 XML 序列化示例。本文未核 TS 24.483 的目标正文。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](initial-ue-config-xcap.json)
