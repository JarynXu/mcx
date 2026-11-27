# 配置 HTTP GET：怎么分辨取整份、取元素和取属性？

先看实际请求的 Request-URI 指向哪一层，再核发送方。**整份文档的 CMS 收端条款明确写 CMC 和 MCS 服务器；元素和属性的收端条款写的是 CMC。**后两项也有 MCS 服务器的发送程序，不能因为收端没点名就判它不得发送，也不能把整份文档的收端规则照搬过去。

依据：3GPP TS 24.484 V20.1.0，Release 20，Stage 3，§6.3.3、§6.3.8、§6.3.11。CMC 是配置管理客户端，CMS 是配置管理服务器。下表的 GC 是供发送角色遵循的通用客户端程序，不是另一个必须先发 GET 的节点。

| 要取的范围 | GC 如何选目标，CMC 如何构造 | CMS 处理实际入站请求 |
| --- | --- | --- |
| 整份 XML 文档（§6.3.3） | GC 发 HTTP GET，引 RFC 4825 的 “Retrieve a Document”。CMC 遵循该 GC 程序，原文写 Request-URI 设为按 TS 24.483 配置的 CMSXCAPRootURI，并带相应用法的 auid（§6.3.3.2.1/.2）。 | §6.3.3.3 要求支持来自 CMC 或 MCS 服务器的文档 GET；实际 Request-URI 标识 XML 文档，auid 对应该应用用法。 |
| 文档中的 XML 元素（§6.3.8） | GC 的 GET URI 引用待取元素。CMC 遵循该 GC 程序，以配置的 CMSXCAPRootURI 为相对路径的根，带相应用法的 auid（§6.3.8.2.1/.2）。 | §6.3.8.3 要求支持来自 CMC 的元素 GET；实际 Request-URI 标识 XML 元素，并带相应用法的 auid。 |
| 文档中的 XML 属性（§6.3.11） | GC 的 GET URI 引用待取属性。CMC 遵循该 GC 程序，也用配置的 CMSXCAPRootURI 作相对路径的根，带相应用法的 auid（§6.3.11.2.1/.2）。 | §6.3.11.3 要求支持来自 CMC 的属性 GET；实际 Request-URI 标识 XML 属性，并带 auid。这里明引第 7 章的相应用法。 |

三项 CMS 处理都指向 RFC 4825 的 “GET Handling”。只看到 GET、根地址或 auid，不足以区分目标。整份文档 GC 小节写 “document to be updated”，但该小节要求 GET，并指向取文；不能据这个短语判成 PUT 或更新。表中的根是按 TS 24.483 配置的 CMSXCAPRootURI；不把根与 auid 当作完整 URI，也不在这里补通用选择器语法。

## 业务服务器发出的 GET 单独核

- **取整份，经 CSC-5。**§6.3.3.2.3 要求 MCS 服务器走整份文档的 GC 程序，按配置让 Request-URI 标识 XML 文档，带相应用法的 auid。条文本身没有把先收到 SIP NOTIFY 设为通用前提；[组织业务配置更新](mcs-server-service-config.md)才有该场景的通知与取文关系。
- **取元素或属性。**§6.3.8.2.3、§6.3.11.2.3 首句分别要求 MCS 服务器执行元素、属性的 GC 程序。后句都写 Request-URI 按配置 “identify the XML document” 并带相应 auid；元素分支的原文主语是 “MCPTT sserver”，属性分支是 “MCS sserver”。保留这两处原文差异，不能据后句改判为只取整份，也不据此补节点选择器或把整份取文的 CSC-5 字样套到这两个小节。实查时，把发送侧按各自 §.2.3 核；两条 CMS 收端的文字只列 CMC，不据这处未列判 MCS 服务器请求一定获准、被禁止或会怎样响应。

§5.1、§5.2、§5.3 分别把上述 CMC 发送、CMS 处理和 MCS 服务器发送列为应支持的程序。这不是已实施证明，也不说明某个文档应用天然可读。区别于[配置 DELETE](cmc-config-delete-target.md)，§5.1 下这三项 GET 是必支持，三项 CMC DELETE 是可支持。

## 抓到请求，不等于收到正文或读到了库

CMC 的[首个 NOTIFY 与取文](cmc-subscription-notify-fetch.md)有自己的通知和响应证据。这里只能用实际 GET 及 CMS 的入站材料核请求范围；要确认客户端取到内容，还要查同一请求的实际返回与内容，不从此处补固定状态码、缓存行为或应用结果。

[在线 CMS 的用户档维护](online-cms-user-profile-database.md) §4.4 另说：为向 UE 下发 MCS 用户档或支持 UE 更新它，在线 CMS 按所引 TS 29.283 取用户库中的该档。某笔 HTTP GET 本身不能证明 CMS 实际读过该库，也不能把这个后端步骤推广到所有文档、元素或属性。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](cmc-mcs-config-get-target.json)
