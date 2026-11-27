# CMC 用 HTTP PUT 写整份配置：怎么区分创建、更新和改节点？

**创建和更新整份配置都用 HTTP PUT。**两条程序都要求配置管理客户端（CMC）准备对应应用用法的 XML 并发送。仅凭 PUT、文档级 Request-URI 和 XML 正文，不足以区分本次是创建还是更新。查所执行的程序和业务场景，不把创建写成 POST，也不把准备 XML 当作服务器已新建文档。

依据：3GPP TS 24.484 V20.1.0，Release 20，Stage 3，§6.3.2、§6.3.4。

| 要做什么 | CMC 发什么 | CMS 要支持什么 |
| --- | --- | --- |
| 创建配置文档（§6.3.2） | §6.3.2.1 写的是管理员创建配置的场景，指向 TS 23.280。CMC 按 §6.3.2.2 创建相应用法的 XML 文档并发送。原文把 PUT 的 Request-URI 写为设到按 TS 24.483 配置的 CMSXCAPRootURI，并带第 7 章相应用法的 auid。 | §6.3.2.3 要求支持接收应用用法的 XML 文档：这次 PUT 的 Request-URI 标识 XML 文档，并带第 7 章相应用法的 auid。 |
| 更新配置文档（§6.3.4） | CMC 同样要准备相应用法的整份 XML 并发送。§6.3.4.2 同样写配置的 CMSXCAPRootURI 及相应用法的 auid，这次没有明引第 7 章。 | §6.3.4.3 要求支持接收 XML 文档：这次 PUT 的 Request-URI 标识 XML 文档，并带相应用法的 auid，这次也没有明引第 7 章。 |

两条 CMC 程序都指向 RFC 4825 的 “Create or Replace a Document”，两条 CMS 程序都指向 “PUT Handling”。这里没有单列 GC 步骤。 更新段也用 “create an XML document” 描述 CMC 生成要发送的正文，不是说 CMS 在更新时新建文档。章号有没有写出来，不是决定某个应用能不能写的依据。两条收端文字也没有另列发送方名录，不能从 §6.3.3 的 GET 规则搬来 MCS 服务器的写权限，或从管理员场景倒推本次发送者已认证。

**两个角色的支持要求不同。**§5.1 要求 CMC 支持创建；支持更新是可选项。CMC 选用更新程序时，仍须按 §6.3.4.2 处理。§5.2 要求 CMS 支持创建和更新的两条接收程序。有没有实现某项请求能力，与某一笔是否写成，分开判断。

## 实际 URI 指向节点时，另查节点程序

- **元素：**§6.3.6.2.1 的 GC 通用客户端程序用 PUT 引用元素；CMC 按 §6.3.6.2.2 执行该程序，以配置的 CMSXCAPRootURI 为相对路径的根、带相应 auid。§6.3.6.3 要求 CMS 支持处理实际收到的 CMC HTTP PUT：这笔请求的 Request-URI 标识 XML 元素，auid 也要对应相应用法。仅凭 CMC 发端记录或只看到入站 URI 里的元素，不能证明收端条件齐备。入站元素对但 auid 不匹配，不满足本条条件。
- **属性：**§6.3.9.2.1 的动作和引用都说创建或替换属性，但 GC 句的 URI 对象原写为 “element”。CMC 依 §6.3.9.2.2 执行该 GC 程序，以配置的根作相对路径的根、带相应 auid。§6.3.9.3 要求 CMS 支持处理实际收到的 CMC HTTP PUT：这笔请求的 Request-URI 标识 XML 属性，且 auid 对应第 7 章所述的相应用法。保留两处用词差异，不从 GC 的这处文字把属性规则改成元素规则，也不据此补选择器语法。

整份文档的条文写法不能替代节点寻址，也不能把根和 auid 当作完整地址。GET、DELETE 各有原有的[取回对象](cmc-mcs-config-get-target.md)和[删除对象](cmc-config-delete-target.md)入口。

## 有 XML 不等于通过校验、写成功或已存库

本页的两条整文档程序没有给通用 Content-Type 或固定成功状态码，也没有定义所有应用用法的写入校验。应用用法确定后，按对象分别查[默认用户档引用](default-profile-reference-xcap.md)、[在网初始档的 TLS 组合](initial-ue-tls-tunnel-validation.md)或 [MCPTT 用户档写入校验](mcptt-user-profile-xcap-validation.md)。不能拿某一对象的约束去验所有 PUT。抓到发送、CMS 实收或知道 CMS 要支持它，都不能证明本次已经写成。

[在线 CMS 的用户档维护](online-cms-user-profile-database.md) §4.4 另有后端条件：MCS 用户档文档**已由 MCS UE 创建或更新**，在线 CMS 才按这里所引 TS 29.283 流程将其作为用户档存入 MC 业务用户数据库。只抓到一笔配置 PUT，不能证明这个条件已发生，更不能证明存库已完成。管理员创建配置的场景不能替代 §4.4 的这一条件。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](cmc-config-document-put.json)
