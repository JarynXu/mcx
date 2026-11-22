# MCPTT 位置配置、位置请求和报告：参与功能与终端各做什么？

在 3GPP TS 24.379 V16.14.0 的这条 Stage 3 流程中，参与 MCPTT 功能（PF）可以给终端下发规则，也可以单独要一份位置报告。**下发规则和索要报告都用 SIP MESSAGE，由消息体里的 `Configuration` 或 `Request` 区分；终端上报时发送的是带 `Report` 的 SIP 请求。** 这是 PF 与 MCPTT 终端间的信令，不是向 LMS 订阅另一个用户的位置。[§13.1–13.2.4，印刷页 460–461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=461)；[§13.3.1，印刷页 462](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)。

## 什么时机下发配置？怎样认出是一份配置还是一次请求？

PF 需要终端位置时，§13.1 把配置放在**MCPTT 业务授权成功**之后。§13.2.2 允许 PF 发配置，并未规定每次 IMS REGISTER 成功都下发配置，也没规定授权成功后多少秒发出。若 PF 确实需要终端报告位置，§13.2.3 要求另按位置请求程序生成并发送 SIP MESSAGE。两种 MESSAGE 各自有以下内容：[§13.1、§13.2.2–3，印刷页 460–461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=461)。

- Request-URI 是与 MCPTT 客户端身份对应的 URI。`Accept-Contact` 使用 `g.3gpp.icsi-ref`，值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`，带 `require` 和 `explicit`。同一个服务值也写入 `P-Asserted-Service`。
- `application/vnd.3gpp.mcptt-info+xml` 的 `<mcptt-request-uri>` 元素写目标用户的 MCPTT ID。另一个 MIME body 是 `application/vnd.3gpp.mcptt-location-info+xml`，在 `<location-info>` 根元素中分别放 `<Configuration>` 或 `<Request>`。
- **配置**在规定了 `TriggerId` 的触发条件子元素填写该属性，并把 PF 自己的公共服务标识（PSI）写进 `P-Asserted-Identity`（PAI）。位置请求条款没有列这项 PAI 要求，不能反过来解读为请求必须不带 PAI，也不从配置条款给它加上必带条件。

## PF 转发 SIP 请求时，何时必须删除整个位置体？

先分清包的来路。PF 按 §13.2.2 或 §13.2.3 下发配置或索要报告时，自己生成一条 SIP MESSAGE。§13.2.5 处理的是 **PF 收到的 SIP 请求**，不限于 MESSAGE。先查入向请求，再找同一 PF 对应的出向请求；只看出向包，分不出源发、转发和入向本来就没有位置体这几种情况。

**先核对身份，两条满足一条即可。**

- **看 P-Asserted-Identity（PAI）：**它标识了一个公共用户身份，该身份不与本 PF 服务的任何 MCPTT 用户关联。缺少 PAI 不能当作满足这一条。
- **看请求里的 MCPTT ID：**找到 Content-Type 为 `application/vnd.3gpp.mcptt-info+xml` 的 MIME 体，其中 `<mcptt-request-URI>` 所含的 MCPTT ID 标识本 PF 服务的用户。这里保留 §13.2.5 的拼写，不把它当作源发条款中小写元素名的别名。即使 PAI 关联的是本 PF 服务的用户，这一条也可成立；反过来，第一条成立便不要求第二条也成立。

**再查同一个入向请求，以下三项缺一不可：**

1. `Accept-Contact` 含 `g.3gpp.mcptt`。
2. `Accept-Contact` 含 `g.3gpp.icsi-ref`，值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`。核对这两个特征，不按物理头行数判定；本条也没有另列 `require`、`explicit` 或 `P-Asserted-Service`。
3. `application/vnd.3gpp.mcptt-location-info+xml` MIME 体含 `<Request>` 或 `<Configuration>`。

身份和报文条件都满足时，**PF 必须从出向 SIP 请求中删除整个位置 MIME 体**，不是只删其中的 XML 元素，也不是拒绝整个请求。条款没有给出 SIP 响应码，没保证其余内容原样送到终端。要判断终端是否保存配置或响应请求，须查终端实际收到的 MESSAGE。[TS 24.379 V16.14.0 §13.2.5，印刷页 461–462](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=462)。

例如，PAI 对应本 PF 服务的用户，但上述 MCPTT info 体内的 ID 也指向本 PF 服务的用户。两项特征齐全，位置体含 `Configuration`，便要在转发时删掉该体。其余不变，若位置体只有 `Report`，就不满足本条；若完整入向包确实缺少其中一个特征，也不能用本条要求删除。条件不满足不等于必须保留。抓包不全或只见终端没收到配置，更不能证明 PF 执行过删除或拒绝。

## 终端什么时候等 minimumReportInterval，什么时候直接走请求分支？

终端的两条接收程序先看**本机实际收到的 SIP MESSAGE**：`Accept-Contact` 是否含 MCPTT 的 `g.3gpp.icsi-ref` 值，`Content-Type` 是否为 `application/vnd.3gpp.mcptt-location-info+xml`，位置体的 `<location-info>` 内是否有对应元素。发端的字段要求不自动变成接收分支未列的检查项。[§13.3.2–3，印刷页 462–463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)。

| 终端本机真正遇到的事件 | 终端动作 |
| --- | --- |
| 收到匹配的 `Configuration` | 保存配置、设置触发条件、启动 `minimumReportInterval`。附录列有可选的 `LocationConfigurationReceived` 触发条件；收到配置本身不表示每次立即上报。 |
| 已配置的事件触发，且 `minimumReportInterval` 正在运行 | 等计时器到期。到期时仍有报告触发条件为真，才按报告程序发送。不能把一度触发、到期时已不成立的条件当成到期时仍成立。 |
| 收到匹配的显式 `Request` | 按报告程序发送报告，并重置 `minimumReportInterval`。本分支未列“先等正在运行的计时器到期”，也未承诺端到端的秒数。 |

§13.3.4.1 没有另写事件触发但计时器未运行的处理，也未规定事件触发与显式请求同时到达时的先后。不要据此补定时器分支或调度策略。[§13.3.2–13.3.4.1，印刷页 462–463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)；[附录 F.3.3，印刷页 566、568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)。

## 第二份位置配置会保留哪些旧项？

先核对本机实收的 SIP MESSAGE 是否命中上节 `Configuration` 入口：`Accept-Contact` 中是 MCPTT ICSI，`Content-Type` 是 `application/vnd.3gpp.mcptt-location-info+xml`，对应 MIME 体的 `<location-info>` 内是 `<Configuration>`。在有效配置里查看 `Configuration` 的 XML 属性 `ConfigScope`，不要从 SIP 头里找它。以下比较同一终端已有位置上报配置时，两种明确写出的值。[§13.3.2，印刷页 462](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)；[F.3.2，印刷页 559](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)；[F.3.3，印刷页 564](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=565)。

- **`Full` 替换整份旧的位置上报配置。** 新的有效全量配置不带某个旧的可选项，该项就不再沿用。要移除旧配置元素，须用 `Full`。这不等于清除其他业务的设置，也不表示可用任意空的 `Configuration` 清空配置。
- **`Update` 在旧配置上追加。** 没列进新包的旧项不因缺席而删除。若之前没有配置，这两处条款没有为缺失字段给出初始值。它们也没有规定追加内容与已有内容冲突时怎样合并。

`TriggerId` 标识一条触发条件；这里没有规定用它关联配置版本或更新条目。PF 源发报文中的目标 MCPTT ID 对应该用户，也不决定配置范围。不要从相同或不同的 ID 推断某一项已覆盖、已删除，或终端另存了一套配置。`Request` 是要报告，`Report` 是报告，都不按此处的 `ConfigScope` 改配置。XSD 列出 `Full` 和 `Update`，属性声明没有写 `use="required"` 或默认值；语义条款也没给缺省行为。仅凭缺少属性、值不认识或消息体异常，不能选用某个范围、推定保留旧配置，或指定 SIP 响应码。[§13.2.2，印刷页 460–461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=461)；[F.3.2，印刷页 559](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)；[F.3.3，印刷页 564](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=565)。

命中接收分支后，终端须保存配置内容、设置触发条件、启动 `minimumReportInterval`。这里写的是启动，没规定第二份配置来到时怎样处理已经在跑的计时器，也没规定此前已触发的事件怎样处理。这不能推出每份配置都立即上报；可选的 `LocationConfigurationReceived` 仍按上节的触发入口判断。PF 出包只证明发出；终端实收合格报文只能确定该走哪条分支。要确认某项实际保留或移除，核对终端处理记录和变更前后的有效配置、触发设置，不用 SIP 2xx 代替本地状态。[§13.3.2、§13.3.4.1，印刷页 462–463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)；[F.3.3，印刷页 566](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)。

## 普通和紧急时怎样匹配位置触发条件？

**先核对终端生效的配置和事件发生时的上报状态。** `TriggeringCriteria` 列出非紧急上报的触发条件，`EmergencyTriggeringCriteria` 列出紧急上报的条件。它们回答“什么事件使终端上报”。所请求的内容另看可选的 `NonEmergencyLocationInformation` 和 `EmergencyLocationInformation`。例如，同一终端两套条件都配置了进入同一 ECGI（小区标识），但各自的 `TriggerId` 不同。本机上报状态已知且不变时，实际进入该小区便按当时那套条件核对此次触发对应的 ID。不能只根据紧急呼叫的出现时间或报告标签推定状态已切换。这里不规定状态切换时点，或如何处理切换前已经触发的条件。[F.3.3，印刷页 564、566](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=565)（[紧急条件](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)）。

**周期触发和最短间隔分开看。** 两套条件都可配置 `PeriodicReport`，值以秒为单位，用来产生周期触发。各自的位置内容块如果存在，必须包含 `minimumIntervalLength`。这个值以秒为单位，表示两次报告间的最短等待时间；XSD 将其定义为正整数。它不产生触发，也不把 `PeriodicReport` 变成保证发包的间隔。已配置的事件触发且 `minimumReportInterval` 正在运行时，按 §13.3.4.1 等待；到期仍有任一触发条件为真才进入报告程序。这里不从紧急标签推出免等或最短间隔为零，不补正在运行的计时器重算规则。LMS 的 Stage 2 表另有规则，不能移用。[§13.3.4.1，印刷页 463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=464)；[F.3.2，印刷页 562](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=563)；[F.3.3，印刷页 564、566、568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=565)（[非紧急周期](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)、[紧急周期](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)）。

**`ReportType` 说明发送时的情形。** `Emergency` 和 `NonEmergency` 不指出是哪一条条件触发。要查触发，把报告里实际携带的 `TriggerId` 与终端生效配置和本机事件记录对应起来。到期时“仍有任一条件为真”决定这一分支要不要发，不表示报告列出的每个已触发条件在到期时都仍为真。只看到标签或终端发包，也不证明 PF 已实收、核准或使用；没抓到报告不能判为终端已停止上报。[F.3.2，印刷页 559](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)；[F.3.3，印刷页 568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)；[§13.3.4.1–2，印刷页 463–464](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=464)。

§6.2.9.1(1) 处理按已收到的配置为指定触发在 SIP 请求中附上位置时，要求按 §13.3.4.2 填位置并跳过该辅助程序的余下步骤。别把[独立紧急告警请求](../calls/standalone-group-alert-client.md)中缺少紧急位置配置时的坐标规则套到所有 `Emergency` 报告。[§6.2.9.1，印刷页 76–77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=77)

固定版有一处 XML 差异：F.3.3 要求在 `anyExt` 中包含必备的 `EmergencyTriggeringCriteria`，并称它未在 schema 声明；F.3.2 又为它列出全局声明，且把 `Configuration` 的 `anyExt` 声明为可选。可用上文判断条件的角色，不用这处差异指定终端必收的报文结构。[F.3.2，印刷页 559、563](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)（[全局声明](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=564)）；[F.3.3，印刷页 566](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)。

<a id="geographic-crossing"></a>
## 终端换了小区，算进入地理围栏吗？

假设终端从小区甲切到小区乙，切换前后以及途中都在同一多边形内。**这次换小区不是进入该多边形。** 若生效配置要求“小区发生变化”或“进入小区乙”，这次事件可命中相应的 `CellChange` 条件。`TravelledDistance` 另按配置的米数判断；只知道小区变了，不能推出已经走够距离。后来终端从多边形外跨到里面，即使一直使用小区乙，也可命中**进入这个多边形**的条件；从里面出去才是退出。停在区域内的一次坐标读数不能区分“刚进入”和“始终在内”。

判一份报告时，先找当时生效的普通或紧急触发配置。在 `GeographicalAreaChange` 下，`AnyAreaChange` 表示任一地理区域变化，不能据此指定某个区域及方向。特定进入和特定退出各有自己的条件和必填的唯一字符串属性 `TriggerId`。用报告中实际列出的触发 ID 查生效配置；若命中的是特定进入或退出，再核对**该项的方向和区域**，不能按报告标签、某个角点或当前经纬度猜原因。核对触发并不等于看到了出包：若最短间隔计时器仍在运行，须等到期，届时仍有上报条件为真才走事件报告程序；报告可以随别的 SIP 请求发送。报告记录的是终端认定已触发的条件，不是对真实轨迹的独立测量。[TS 24.379 V16.14.0，F.3.3，普通条件，印刷页 564–566](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=565)；[紧急条件和报告，页 566–568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)；[§13.3.4.1–2，页 463–464](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=464)。

**发送方写 `EnterSpecificArea`，接收方却查 `EnterSpecificAreaType`，差在哪里？** 本版 F.3.3 的语义说明用前一个名字；F.3.2 的 XSD（XML 结构定义）声明的**元素名**是后一个，并非仅在类型名里多了 `Type`。退出在两处都写 `ExitSpecificAreaType`。XSD 把“任意变化、特定进入、特定退出”三个直接子项各列为 0 或 1 次。特定进入与退出共用一套结构：在触发元素上填 `TriggerId`，内含一个必需的 `GeographicalArea`。语义文字却称进入项下的 `GeographicalArea` 可选并带 `TriggerId`；XSD 没在区域定义上声明这个具名属性。另有一处差异：语义将 `GeographicalAreaChange` 列为可选，XSD 的 `TriggeringCriteriaType` 却要求有这个容器。容器必需也不等于终端一定配置了进区触发。不能据此宣称两个进入元素是别名，或规定接收端必须兼容哪种拼写。[F.3.2，普通触发类型，页 559–560](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)、[区域元素及其类型，页 562–563](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=563)；[F.3.3，页 566](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)、[568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)。

| 核对配置中的区域形状 | F.3.2 给出的结构 |
| --- | --- |
| `PolygonArea`（多边形） | 3 至 15 个 `Corner`；每个点先 `longitude`，后 `latitude`。这些是所配置区域的角点，不是报告里终端所在的点。 |
| `EllipsoidArcArea`（椭球弧） | 依次是 `Center`、`Radius`、`OffsetAngle`、`IncludedAngle`。中心点同样先经后纬；半径为非负整数，两种角度字段都是无符号字节。 |

区域定义用的是顺序结构，两个形状子项各可省略、各最多出现一次，不是由 XSD 强制二选一。结构本身不能说明没有形状、或两种形状并存时终端如何判断越界。F.3.3 对形状的几何定义另引 TS 23.032；这里不从字段类型推导半径单位、角度换算、边界点归属或定位误差处理。[F.3.2，页 563](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=564)；[F.3.3，页 566](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)、[568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)。

## Report 发到哪里？怎样证明它是对这次请求的报告？

若终端正因别的理由需要发一个 SIP 请求，就把含 `<Report>` 的位置 MIME body 加进该请求；MBMS 监听报告只是原文举例。若没有另一个要发的请求，终端构造独立 SIP MESSAGE：Request-URI 取自此前**收到的位置配置 MESSAGE** 中 PAI 的 SIP URI，不是取自这次位置请求；Content-Type 是上述位置 MIME，`Accept-Contact` 用不同的 `g.3gpp.mcptt` 特征标签，也带 `require` 和 `explicit`。独立 MESSAGE 的目的地规则需要这份配置里的 URI，条款没有为缺少该 URI 指定后备目的地。两种发送分支都把 `minimumReportInterval` 设为规定时长并启动，重置全部触发条件。在独立 MESSAGE 分支，正文把实际发送列在这些动作之后；不把这一步骤排序套到显式请求程序另列的重置动作上。[§13.3.3–13.3.4.2，印刷页 462–464](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)。

**只有由显式位置请求触发的报告才按该请求回填关联值。** 正文 §13.3.4.2 写 `RequestID` → `ReportID`；附录 F.3.2 的 XSD 把请求属性写作必需的 `RequestId`，把报告属性写作可选的 `ReportID`；F.3.3 的描述写 `RequestId` → `ReportId`。XSD 中的可选性并不抹掉显式请求分支的回填要求。对实际触发的事件，正文把来源属性写成 `Trigger-Id`，报告子元素写成 `TriggerId`；附录用 `TriggerId` 表述其关联属性。报告按已触发条件填对应内容，不以一个触发标识替代这次请求的回填值。这里保留定版中的拼写差异，不定义等价别名或可直接发送的 XML。[§13.3.4.2，印刷页 463–464](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=464)；[附录 F.3.2，印刷页 559](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)；[附录 F.3.3，印刷页 568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)。

PF 实际收到 Content-Type 匹配、位置体的 `<location-info>` 内有 `<Report>` 的 SIP 请求，须按**收到的 MCPTT ID** 核准这份报告。用户获准上报后，PF 按需使用位置信息，并检查以下两种情况：若 PF 判定终端进出紧急告警区，按[紧急告警区通知](../calls/area-alert-notification.md)处理；若 PF 判定终端进出组地理区域，按[组地理区域通知](../groups/group-geographic-area-notification.md)处理。这是 PF 收报后的步骤，与终端先前匹配围栏触发条件不同。这里不指定 MCPTT ID 必在某一字段，也没有给出专用的 SIP 成功或拒绝码。终端发出报告、见到任意 SIP 2xx，或能用回填值配对，都不能单独证明 PF 已核准并使用位置。看到 `Report` 元素也不能直接断定含坐标。[§13.2.4，印刷页 461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=462)。

<a id="report-location-content"></a>
## 收到位置报告却读不到经纬度，包里到底有什么？

先看 `Report/CurrentLocation`。**报告必须有这个容器，但一般的报告不一定有坐标。** 完整位置体里只有服务小区、没有坐标，和连 `CurrentLocation` 都没有，是两种情况：

| 在完整的 `Report` 中看哪里 | 怎样判读 |
| --- | --- |
| `Report` 自身 | XSD 要求一个 `CurrentLocation` 和属性 `ReportType`（`Emergency` 或 `NonEmergency`）。`TriggerId` 可为零到多个；报告与显式请求的关联另按上节核对。 |
| `CurrentLocation` 的子项 | 服务小区 `CurrentServingEcgi`、邻区 `NeighbouringEcgi`、MBMS 服务区 `MbmsSaId`、MBSFN 区 `MbsfnArea`、坐标 `CurrentCoordinate` 均可选。这五项里只有邻区可重复。服务小区标识不是经纬度。 |
| `CurrentCoordinate` | 若出现，XSD 要求依次有 `longitude`、`latitude`。只有经度而没有纬度，不等同于合法省略整个可选坐标。 |

这张表只判断报告结构。§13.3.4.2 要求填入与实际触发条件对应的位置项，不能用“坐标可选”证明具体终端报齐了该报的内容。另一个入口是[独立组紧急告警](../calls/standalone-group-alert-client.md)：在 §6.2.9.1 第 2 项的告警分支中，若终端先前没有通过 §13.3.2 收到含 `EmergencyLocationInformation` 的配置，就必须带 `CurrentCoordinate`。不能只凭 `ReportType=Emergency` 就套用这条告警规则。[F.3.2，印刷页 559](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)、[562–563](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=563)；[F.3.3，印刷页 568–569](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)；[§13.3.4.2，印刷页 463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=464)；[§6.2.9.1，印刷页 76–77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=77)。

**坐标节点在，不等于坐标明文在。** F.3.3 把保护标记 `type` 放在四类无线位置项各自的元素上；对坐标则分别放在 `longitude` 和 `latitude` 上，不在外层 `CurrentCoordinate` 或 `CurrentLocation` 上。F.3.2 的属性声明未把 `type` 标为必填；实际报告仍要按 F.3.3 对应的保护条件核对取值。

- **无需保密保护时**，相应的 `type` 为 `Normal`。服务小区和邻区的明文值在 `Ecgi`，MBMS 服务区在 `SaId`，MBSFN 区在 `MbsfnAreaId`。经纬度各自的明文子元素在 F.3.2 的 XSD 拼作 `threebytes`，F.3.3 正文写作 `three-bytes`。这是同一版本的拼写差异，不把两者注册成等价 XML 名称，也不把编码值直接读作十进制度数。
- **需要保密保护时**，相应的 `type` 为 `Encrypted`，上述每个已包含的无线位置项或坐标分量各自带 `xenc:EncryptedData`（这里的 `xenc` 代表命名空间 `http://www.w3.org/2001/04/xmlenc#`），其中有 `CipherData/CipherValue`。`Type` 属性、`EncryptionMethod` 和 `KeyInfo` 是可选信息；不能仅因其中一项缺失就认定没有密文。

例如，两条坐标轴都在，各自都有上述密文结构：这份包报告了受保护的坐标分量，**不是终端没报坐标**。观察者不能从这段密文读出明文经纬度，也不能据此还原发送方实际使用的配置，或断言 PF 已解密、已按 MCPTT ID 核准报告，或已取得终端的真实位置。若抓到的只是片段，更不能凭没看见某个节点判定完整报告缺项。[F.3.2，印刷页 562–563](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=563)；[F.3.3，印刷页 569](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=570)；[§13.2.4，印刷页 461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=462)。

若问的是 [LMS 如何在 Stage 2 配置事件上报](event-reporting-configuration.md)或[其他用户怎样订阅位置](user-subscription.md)，按 LMS 的角色读相应主题。若在排查 IMS 接入之后哪项 MC 业务获授权，见[共享 SIP 注册与业务授权](../identity/shared-sip-registration.md)。此处的 PSI 是位置配置 SIP MESSAGE 的 `P-Asserted-Identity` 所带的参与 MCPTT 功能标识，不是 LMS 有 SIP PSI 或 SIP SUBSCRIBE 的证据。
