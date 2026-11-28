# MCData 在网 ad hoc 组数据通信：支持开关、人数与时长

先看业务配置里有没有 `on-network/anyExt/adhoc-group-data-comn`。已确认整块缺失时，标准把它解释为 MCData 系统不支持在网 ad hoc 组数据通信。块存在时，查里面的支持开关和允许人数；两个时长各管一件事，一个管同一次通信内相邻发送之间可静默多久，一个管整次通信可持续多久。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§10.4.2.1/.3/.6/.7。这里查在网 MCData 业务档，不沿用 [MCPTT、MCVideo 的 ad hoc 组呼字段](ad-hoc-broadcast-hang-time.md)。

### 配置块可选，开关和人数是块内必需字段

§10.4.2.1 在网项 4(g) 在 `anyExt` 下列出可选的 `adhoc-group-data-comn` 及四个子项。§10.4.2.3 的 `on-networkType` 声明可选 `anyExt`，其类型有 `##any`、`lax` 的通配声明；`adhoc-group-data-comn` 另有全局元素声明，类型是 `adhoc-group-comnType`。它不是 `on-network` 的具名直接子项。

| 子项，按 Schema 声明顺序 | 类型与出现约束 | §10.4.2.7 在网用途 |
| --- | --- | --- |
| `allow-adhoc-group-data-comn-support` | 必需，`xs:boolean`，本声明无 `default` 或 `fixed` | 项 20：指示在网 ad hoc 组数据通信支持是启用还是禁用。指向 TS 24.483 §11.2.19 `AllowAdhocGroupComn`。 |
| `max-no-participants` | 必需，`xs:positiveInteger`，本声明无 `default` 或 `fixed` | 项 21：允许的参与者人数。指向 TS 24.483 §11.2.20 `MaxNoParticipants`。 |
| `hang-time` | 可选，`xs:duration`，无 `default` 或 `fixed` | 项 22、注 3：同一次数据通信内，两次连续 MCData 传输之间可配置的最长静默。指向 TS 24.483 §11.2.21 `HangTime`。 |
| `max-duration-of-data-comn` | 可选，`xs:duration`，无 `default` 或 `fixed` | 项 23：整次在网 ad hoc 组数据通信允许的最长时长。指向 TS 24.483 §11.2.22 `MaxDurationOfComn`。 |

人数填 `0` 不满足 `xs:positiveInteger`，不表示人数不限。字段给的是允许人数，不是某次实际参与人数。本处不规定如何清点参与者、超额时拒绝谁或该字段专用的 409 诊断。两个时长分别可省略；从缺少一个时长不能推出沿用另一个、自动填零或没有时限。时长定义不说明计时何时开始或复位、何时停止通信。TS 24.483 的四项仅作原文定位。

### 正文默认 true 不能补缺失的块或必需子项

§10.4.2.6 的文字给**支持开关**默认值 `true`，表示启用。§10.4.2.3 对这个布尔子项却没有写入 XSD 默认值，并且要求块内出现该子项。块存在而开关缺失时，不能用正文默认值说它已满足这个 Schema 约束；也不能把缺开关说成缺整块。已经明确写入 `false` 时，字段指示禁用，不把它改读为默认 `true`。

§10.4.2.6 另规定整块缺失指示系统不支持。不从默认值创建块，也不把节选里没看到当成完整配置确定缺项。已配置启用不等于一次组通信已建立。

### 两项时长有自己的格式和数值检查

§10.4.2.6 后一份具名时长清单是 `hang-time` 和 `max-duration-of-data-comn`，不是[共用配置的暂存等待与周期公告](mcdata-common-tx-rx-duration-config.md)。本段要求按秒表示：表示式原写 `PT<h>H<m>M<n>S`，其中 `<n>` 是有效秒值；格式校验句另写 `PT <n>S`。本段注 5 举例 300 ms 可表示为 `PT0.3S`，说明秒可用小数，不证明某个 CMS 会接受，也不由示例决定小时、分钟或空格如何解析。

| 条文触发条件 | CMS 必须返回 | 带 `phrase` 时建议用 |
| --- | --- | --- |
| 两项之一的值不符合原文所写的 `PT <n>S` 结构 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `invalid format for duration` |
| 收到无效的 `<n>` 值 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `invalid value for duration` |

只知 409 不能判定是哪一条。原文不在这里列出有效 `<n>` 的数值范围，也没规定条件重叠时先处理哪条。确认缺少一个可选时长，不等于收到了一个格式错误或空的值。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcdata-on-network-adhoc-group-data-config.json)
