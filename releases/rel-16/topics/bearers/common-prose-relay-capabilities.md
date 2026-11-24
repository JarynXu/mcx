# 终端无法从网络取得服务时，宜尝试哪种 ProSe 中继？离网终端之间又用哪种？

先看中继通向哪里。**UE 到网络中继**给远端终端提供一条去网络的路；**UE 到 UE 中继**服务于终端之间。在 [§5.14，印刷页 26](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=27)，这两种路径对应不同的要求：

| 对象和场景 | 本条要求 |
| --- | --- |
| MCX 业务（R-5.14-001） | 业务须能使用 TS 22.278 [5] 和 TS 22.468 [6] 所定义的 ProSe（邻近服务）中继能力。这两份规范是本条的引用对象，见[§2 的 [5]、[6]，印刷页 9](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=10)。 |
| MCX 终端无法从 3GPP 网络取得服务（R-5.14-002） | 终端**宜尝试**利用附近一个或多个合适的 ProSe UE 到网络中继。原文是 *should attempt*，不是要求接入成功，也没有指定必须选最近的一台。触发条件是无法取得服务，不要求先证明没有无线覆盖。 |
| 离网的 MCX 终端之间（R-5.14-003） | 终端之间**须支持** ProSe UE 到 UE 中继。没有要求每台终端都充当中继，也没有要求每次离网通信都经中继。 |
| 机器人中的 MCX 终端（R-5.14-004） | **业务须提供手段**，让装在机器人中的终端具备 ProSe UE 到网络中继能力。它是能提供中继的一方，不只是借别人的中继入网；具备能力不等于正在转发。 |

“宜尝试利用”和“须搜索”不是同一个动作。[§6.18，印刷页 49](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=50) 另行要求，无法从 3GPP 网络取得服务的终端**须搜索**能服务于该用户已归属业务组的 UE 到网络中继。搜索到了也不能据此认定已经接通。若查这项搜索与网络侧的关系，见[在网覆盖扩展](prose-ue-to-network-coverage-extension.md)。若要区分离网私通信和组通信，分别查 §7.15 的[私通信中继](offnetwork-private-ue-to-ue-relay.md)、[组通信中继](offnetwork-group-ue-to-ue-relay.md)。

判读现场记录还要分清所查的动作：§7.12 讨论[实时收发与中继换路](prose-relay-streaming.md)，§7.13 讨论[切到离网直连](offnetwork-direct-path-switching.md)，§7.14 讨论[离网活动的审计记录](../security/offnetwork-audit-metadata-retrieval.md)。要看具体过程，按组发现某台中继读[Stage 2 中继发现](relay-discovery-by-group.md)；已有 MCPTT 通话改经中继读[会话转移及其协议程序](anchored-session-transfer.md)。这些过程都不是 §5.14 另外指定的实现步骤。

3GPP TS 22.280 V16.8.0（Release 16，Stage 1）[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)涵盖在网和离网。规范性[表 A.1（MCPTT，印刷页 64）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=65)、[表 B.1（MCVideo，印刷页 75）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=76)、[表 C.1（MCData，印刷页 86）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=87)均列出 §5.14 的全部四项要求。
