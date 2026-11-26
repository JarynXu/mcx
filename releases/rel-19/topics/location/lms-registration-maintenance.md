# LMS 注册续期与注销：哪次更新赶在到期前？

**看 LMS 是否在当前 `expTime` 前收到对同一注册的成功 PUT。** 终端提前发出，不等于服务器提前收到；应答在到期后才到终端，也不等于服务器收晚了。若 LMS 在截止前没有收到成功更新，规范要求把该 LMC 视为隐式注销，并移除对应注册资源。实际 DELETE 成功是另一条路径。

这里读 **TS 24.283 V19.3.0，Rel‑19，Stage 3，LMS_Reporting** 的个别 LMC 注册。查标准不用抓包；判断线上一笔事务，先对上**该 LMS 的同一个注册资源、LMC、HTTP 方法与对应应答**。创建时的实际 `201 Location` 可用来定位；`registrationId` 不是 LMC 实例标识，也不是 `locationConfigUri`、`locationRequestUri` 或订阅 ID。判一笔已识别的 PUT/DELETE，不要求同一份抓包也有创建 201。[§§6.2.2.2.2、6.2.2.3.2、6.2.2.4.2，印刷页 18–20](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=19)。

## PUT：替换已有注册，不只改一个时间

LMC 向个别注册资源发 PUT，正文用一份完整的 `LMCRegistration` 替换原属性，不是送 `expTime` 一项、PATCH 或新建请求。数据类型要求：`expTime`、实例字段（表和 A.2 拼为 `mclocClientID`）、`locationConfigUri`、`locationRequestUri`；`pei`、`supi` 可选。两个回调地址是**注册属性**，都不是 PUT 应发去的资源。

PUT 和 DELETE 的 LMC 都按正文带适用的全部 Bearer 访问令牌；实例字段、注册 ID、回调地址或只建立 TLS，不能代替认证与授权。**PUT 先查资源是否存在**：不存在返回 404；存在才验证所有令牌，用令牌派生的 MC service IDs 识别发送者。任一令牌验证失败回 401 并停止；成功则更新注册并关联 LMS 授权的 MC service IDs。若只知道匹配的 401，不凭状态码给出具体失败令牌或未满足的条件；404 也不能独自说明是自然过期、显式删除还是找错资源。[§6.2.2.3.2，印刷页 18–19](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=19)；[§7.1.6.2.2，印刷页 43](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=44)；[§7.1.9，印刷页 60](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=61)。

| 属于这笔 PUT 的实际 LMS 应答 | 能确认什么 |
| --- | --- |
| **200 + `LMCRegistration`** | 成功更新。正文描述 LMS 返回更新后的到期时间；实际收到的 `expTime` 覆盖 LMC 维护的原值。不能用请求中期望的日期盖掉服务端返回值。 |
| **204 No Content** | 也表示成功替换，没有应答正文或从正文返回的 `expTime`。要跟踪此次提交的到期值，回看这笔已接受的完整 PUT；没有请求的值或另有后续变化时，不从 204 猜日期、延长量或固定续期间隔。 |

[表 7.1.3.3.3.1-2、-3，印刷页 36](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=37)；[A.2 个别注册 PUT，印刷页 75–76](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=76)。更新成功不等于后来一直有效，也不表示配置已下发或位置报告已被 LMS 接受。

## 到期线：别用终端接应答的时钟代替 LMS 收请求

1. **找准截止时间。** 用该注册当时生效的 `expTime`。初建时 LMS 可返回比终端原请求更早的到期时间；后续 200 带的更新值会盖掉旧值。不是固定注册时长，也不用另一台 LMC 的时间。
2. **分清发送、收到、成功。** 条款要求 LMC 在到期前发送，并以 LMS 在到期前**收到成功的更新请求**决定是否隐式注销。例：旧截止 10:00；若核实 LMS 09:59 收到这笔，之后确认该笔处理成功，即使 LMC 10:01 才收到匹配结果，这笔也仍是及时收到的更新。反过来，09:59 的出站、错误应答、代理码、另一注册的成功，或只有终端收应答时间，都不够。条款没有把 LMS 发回 200/204 或 LMC 收到应答的时间定成截止。
3. **证据不全就不判定。** 证实到期前 LMS 没收到成功更新，才据这条规则判隐式注销及移除对应资源；缺少一段日志不等于该更新不存在。晚到的单次请求不能补成在原截止前的更新，也不能证明此前没有其他更新。若已确认该资源过期移除且晚到 PUT 实际查无，按不存在的 404 分支读。条款没有给迟到容忍、过期复活、并发覆盖、到期同刻调度或自动重建规则。观察到不合上述条件的成功码，要先核新的截止值、资源身份、服务器收件和状态。

[§6.2.2.2.2 及 §6.2.2.3.2，印刷页 18–19](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=19)。

## DELETE：获准后才查资源，找到才确认注销

LMC 对同一个别注册资源发 DELETE。LMS **先核身份和注销权限**。在获准分支，查无返回 404；查有则注销这条注册、删除其资源，再回 204。表和 A.2 都没有为此 DELETE 定义请求体，不复用 PUT 的 `LMCRegistration`。印刷页 37 的链接表标题提到 200，不另定义删除成功码；应答表与 A.2 的成功都是 204。A.2 通用错误列表有 401、403；本处程序未给身份/权限不通过指定唯一状态码，不照搬 PUT 或位置订阅。

**匹配的 LMS DELETE 204 确认这笔注销成功。** 仅出站、到期后无日志、404 或另一个操作的 204 都不能证明此次删除。LMS 已发与 LMC 已收也不同。它不证明订阅、IMS 注册、其他设备或后续重建状态，不能推断旧配置回调是否已排空或数据是否物理抹除。[§6.2.2.4.2，印刷页 19–20](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=20)；[表 7.1.3.3.3.2-2、-3，印刷页 37](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=38)；[A.2 删除，印刷页 76](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=77)。

## 本版的写法差别

- **URI、名字和载荷：**§7.1.3.3.2 印作 `{apiRoot}/lms-reporting//<apiVersion>/registrations/{registrationId}`；A.2 在 `{apiRoot}/lms-reporting/v1` 下列 `/registrations/{registrationId}`。正文写实例字段 `mclocClientId`，表/A.2 写 `mclocClientID`。PUT 的校验步骤虽出现 `RegistrationRequest` 字样，仍在本次 PUT 内。A.2 的 PUT 载荷说明误说 subscription，但路径、方法描述与 schema 是个别 **LMC 注册**、`LMCRegistration`，不改作 `/subscriptions`。不因此造 URI 别名、路径回退或 GET 检查。[§7.1.3.3.2，印刷页 35](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=36)；[A.2，印刷页 73、75、77–78](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)。
- **307/308 不是完成：**正文两张资源应答表列 307/308 + `Location`，说 alternative LMS；§7.1.10 的规则限同一 LMS 的另一服务实例。A.2 在 DELETE 逐项列了 307/308，PUT 未逐项列出。保留差别，不规定双写法兼容，也不凭重定向决定及时续期、授权注销或自动重试。[印刷页 36–38、60、75–76](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=37)。
- **读取边界：**[A.1，印刷页 73](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)只给 API 信息元素及方法的编码冲突优先规则；OpenAPI 未表达的程序及条件也适用。

问创建或配置到达，读[注册与配置回调](lms-registration-configuration.md)；问 `LMS_Information` 的个别位置订阅，读[位置订阅](lms-subscription-notification.md)；要判断位置已提交给 LMS，读[位置上报](lms-location-report-publish.md)。它们的同名状态码不能替这笔注册维护取证。
