# MCPTT MBMS 的 SIP MESSAGE 返回 403：查通告方向，还是查上报者绑定？

先看**哪一端收到 MESSAGE**，再检查实际携带的 XML 正文。承载通告与终端的监听、暂停报告都可以使用 `application/vnd.3gpp.mcptt-mbms-usage-info+xml`。MIME 类型相同，不代表可以向同一端发送同一种内容。在正常回报路径上，终端从通告取 PF 的 MBMS 公共业务身份（MBMS PSI）；终端发监听或暂停报告时，把这项身份放在 `Request-URI`，在另一份 `mcptt-info` 正文的 `mcptt-request-uri` 中写自己的 MCPTT ID。[TS 24.379 V16.14.0，§14.3.2，印 470–471](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)；[§14.3.3.2，印 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474)及[印 474](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=475)。

## 参与功能 PF 收到的是通告，还是有身份问题的上报？

§14.2.4 针对 PF 收到带上述 MBMS usage 正文的 SIP MESSAGE。**以下任一条件成立，PF 须回 SIP 403：**

| 完整来件及 PF 的绑定记录 | 按这条规范怎样判 |
| --- | --- |
| `P-Asserted-Identity` 指出的公共用户身份未关联到任何由这个 PF 服务的 MCPTT 用户。 | 满足第一项。不要求另有 mcptt-info 正文，也不要求 usage 正文含通告、监听或暂停状态。 |
| MBMS usage 正文有一个或多个 `announcement`，同时 `mcptt-info` 正文的 `mcptt-request-uri` 指出这个 PF 服务的 MCPTT 用户。 | 满足第二项。有服务对象也不能把这条消息作为有效的终端报告；不要求第一项同时成立。 |

所以，截到一笔 PF 回的 403，不能只凭状态码断言用户未注册、绑定查不到，或通告发反了。若只截到 `announcement`，没拿到另一份正文，也不能说已经证实第二项。终端收到符合 §14.3.2 的承载通告，走的是另一套程序，不能把 PF 的 403 倒用到终端。[§14.2.4、§14.3.2，印 470](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)。

## 同一个 PF 服务甲和乙，两边名字都查得到，报告就能接收吗？

**仍要核对那一对身份是否绑定。** 正常报告用 `mbms-listening-status` 或 `mbms-suspension-status`；其 `mcptt-info` 正文须给出这个 PF 服务的 MCPTT ID。§14.2.3 要求 PF 查这次来件里 `P-Asserted-Identity` 的公共用户身份是否绑定到**正文中的这个 MCPTT ID**。例如，头指向甲，正文写乙，两人都由这个 PF 服务，且两者没有这项绑定。若这一笔不含通告，不能套 §14.2.4 的两项条件断言必须回 403；也不能按 §14.2.3 的绑定通过分支处理乙的状态。§14.2.3 的绑定检查没有为这一种失败单列 SIP 状态码。[§14.2.3，印 468–469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)及[印 469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=470)；[§14.2.4，印 470](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)。

排查时把三项分开记录：**这段 MESSAGE 寻址的 PF**（看 `Request-URI`，再核实际收件记录）、**谁在上报**（PF 收到的 `P-Asserted-Identity`）、**上报指向谁**（`mcptt-request-uri`）。§4.2 的配置假定中，MBMS PSI 与服务该用户的 PF PSI 是同一 URI；这不是头部用户身份和正文身份可以互换的理由。查完路由与身份也不能拿 SIP 响应代替终端实际监听或承载切换的证据。[§4.2，印 33](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[§6.3.1.3，印 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=79)；[§14.2.3，印 468–469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)。

已有正常监听报告，需复核中继切换前后的承载／报告链路，查[锚定会话的接入转移](anchored-session-transfer.md)。若收件方确是终端，查[如何处理通告和撤告](mcptt-mbms-announcement-sdp.md)。若要确认无线暂停、恢复及客户端该不该上报，查[MBMS 暂停上报](mbms-suspension-reporting.md)。
