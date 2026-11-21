# MBMS 话权 MuSiK：默认下载点名一个组，哪些组的密钥会变？

终端已有 A、B 两组的单独 MuSiK，C 组一直用默认密钥。参与 MCPTT 功能（PF）这次发来一笔**默认下载**，只在里面列 A。终端先解除 A 的单独密钥关联，然后按照默认下载处理 **A 和 C**。B 仍有有效的单独关联，不受这笔默认下载影响。默认下载里的名单是**取消哪些单独关联**的名单，不是“只给这些组更新默认项”的名单。[TS 24.379 V16.14.0，Rel-16 Stage 3，§14.2.2.5，印 468](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)；[§14.3.4，印 474–475](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=476)。

## 先看下载类型，再看名单

这里的 MuSiK 是 PF 打算在多媒体广播多播业务（MBMS）下行保护**话权控制信令**所用的密钥，不是给语音 RTP 解密的密钥。PF 对每台相应 MCPTT 客户端按 MuSiK 分别发 SIP MESSAGE。默认值可以共用，显式下载只针对使用指定组的客户端。查 MCPTT MBMS 用途正文（`application/vnd.3gpp.mcptt-mbms-usage-info+xml`）里的下载元素与 `group`：

| 下载元素 | `group` 名单 | 这台客户端处理哪些组 |
| --- | --- | --- |
| `mbms-explicitMuSiK-download` | 至少一个 | 只处理列出的组。其余组不受这笔下载影响。 |
| `mbms-defaultMuSiK-download` | 没有 `group` | 只处理这台客户端支持且没有有效单独关联的组，不清除已有的有效单独关联。 |
| `mbms-defaultMuSiK-download` | 有一个或多个 `group` | 先解除所列组的有效单独关联，再处理这台客户端支持且没有有效单独关联的所有组，包含没列出的这类组。 |

查故障时，用这台客户端处理前的有效关联来算影响范围，不能套用另一台终端保存的名单。[§14.2.2.5 第 5 项，印 468](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)；[§14.3.4 入口及范围处理第 1–3 项，印 474–475](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=476)。

## 200 确认的是哪一次下载？

客户端把消息认作语法正确、有效且无错误的默认或单独 MuSiK 下载，才对这条 MESSAGE 回 200。收到的 MIKEY 负载标识确为 MuSiK-ID 时，客户端以为自己服务的 PF 公共服务身份为依据核对发起者，验证消息并读取 Status；按 Status 对每个受影响组标记安全功能不用，或更新其 MuSiK 与 MuSiK-ID。**200 不能区分是设置了密钥还是处理了停用。** 在这条鉴权分支中，身份不符合、消息认证失败或缺少 Status 会导致 488 和以 136 开头的 Warning 文本。Warning 的 136 不是 SIP 状态码。没有 MIKEY 负载或 key identifier 不是 MuSiK-ID，不能套用这里的缺 Status 拒绝，也不能直接记为停用或装钥。[§14.3.4，印 475–476](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=476)；[200 条件，印 476](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=477)。

## 终端还报 listening，为什么话权要改单播？

PF **实际收到这台客户端对本笔下载 MESSAGE 的 200**，才认定本次下载成功。未收到这个 200 时，PF 须对**这台客户端**、**这份 MuSiK 原本要保护的组**使用单播话权信令。另一台终端的 200 或这台终端的 MBMS 监听报告都不替代下载响应。客户端日志显示已回 200，不能单凭它认定 PF 收到了；同样，没找到 PF 的日志不等于已证实它没收到。[§14.2.2.5 末段，印 468](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)。

该回退不要求把整个组的语音 RTP 改单播，也不证明 PF 实际发出了单播包、客户端已经收到，或它不支持 MuSiK。要核每类下行包走哪条路，查[PF 的 MBMS 话权和 RTP 分流](mbms-pf-floor-routing.md)；要核 MBMS 监听或暂停报告本身是否被 PF 接受，查[MBMS 监听状态报告的拒绝条件](../bearers/mcptt-mbms-status-message-rejection.md)；若查的是目标组并非临时组组成组的在网组呼，且已确定要核单播保护，读[客户端与 PF、PF 与 CF 的话权保护，以及 PF／CF 是否解密 RTP 负载](on-network-unicast-media-protection.md)。
