# CMC 的 HTTP DELETE：删整份配置、一个元素，还是一个属性？

看这次请求的 `Request-URI` 实际指向什么。三种操作都用 HTTP DELETE，也都要用目标对应的应用用法标识 `auid`。只看到方法、XCAP 根或 `auid`，还不能判断要删哪一层。

依据：3GPP TS 24.484 V20.1.0，Release 20，Stage 3，§6.3.5（文档）、§6.3.7（元素）、§6.3.10（属性）。

| 目标 | 发出请求 | CMS 的处理范围 |
| --- | --- | --- |
| 整份 XML 文档 | CMC 按 §6.3.5.2 发 DELETE。原文把 Request-URI 写成采用按 TS 24.483 配置的 `CMSXCAPRootURI`，并带上要删文档对应的 `auid`；操作指向 RFC 4825 的 “Delete a Document”。本节没有单列 GC 步骤。 | CMS 须支持处理来自 CMC、实际 Request-URI 以相应用法的 `auid` 标识 XML 文档的请求（§6.3.5.3）。 |
| 文档内的一个 XML 元素 | 一般客户端（GC）程序要求 Request-URI 指向元素（§6.3.7.2.1，“Delete an Element”）。CMC 执行该 GC 程序，以配置的 `CMSXCAPRootURI` 为相对路径的根，带上对应的 `auid`（§6.3.7.2.2）。 | CMS 须支持处理来自 CMC、实际 Request-URI 标识该 XML 元素并带相应 `auid` 的请求（§6.3.7.3）。 |
| 文档内的一个 XML 属性 | GC 程序要求 Request-URI 指向属性（§6.3.10.2.1，“Delete an Attribute”）。CMC 执行该 GC 程序，也以配置的 `CMSXCAPRootURI` 为相对路径的根，带上对应的 `auid`（§6.3.10.2.2）。 | CMS 须支持处理来自 CMC、实际 Request-URI 标识该 XML 属性并带相应 `auid` 的请求。这一收端条款明确指向第 7 章的相应用法（§6.3.10.3）。 |

GC 是 CMC 在元素、属性两项中遵循的一般客户端程序，不是先由 GC 发一条、再由 CMC 发一条。三条 CMS 收端规则都指向 RFC 4825 的 “DELETE Handling”。核对范围时保留上表的 URI 写法差异，不把整文档的“采用根和 `auid`”当作完整地址或独立可用的删除目标。这里未展开 RFC 4825 的选择器语法或 TS 24.483 的根地址配置。

**支持程序和这次删除成功是两件事。**§5.1 把三项 CMC 删除程序列在 `may` 下；CMC 选用相应程序时，要遵循该程序的 `shall`。§5.2 把三项 CMS 处理列在 `shall` 下。抓到发端请求可核它要求删的对象；要核 CMS 收端条件，应看 CMS 实际收到的请求。仅凭发送、收到或必须支持，不能断定删除已经完成。这几节未在本处给定本次响应码、重复请求的结果或后续联动；不要拿 GET、PUT 或订阅流程替这一笔 DELETE 下结论。

**查用户库要换条款。**[在线 CMS 的用户档维护](online-cms-user-profile-database.md) §4.4 说的是 MCS UE 请求删除 MCS 用户档时，在线 CMS 用 TS 29.283 所指程序从 MC 业务用户数据库删除用户档。不能把某笔配置 DELETE 直接当作库中删除已发生的证据，也不能由此指定哪个前端 URI 必然触发库操作，或外推到删除其他资源或触发版本、通知联动。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](cmc-config-delete-target.json)
