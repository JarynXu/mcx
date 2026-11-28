# MCData 共用收发时长：暂存等待与周期公告

两项都在 `common/tx-and-rx-control`，计的事情不同。它们是 TS 24.484 V20.1.0（Release 20，Stage 3）的 MCData 共用业务配置。这里的 `common` 是在网和离网共用的配置范围，不表示某次通信已经启动计时器。

| 想查什么 | 字段 | §10.4.2.7 共用项 |
| --- | --- | --- |
| 暂存的数据在等待交付给接收用户时，可等待多久 | `time-temp-data-waiting` | 项 1：暂存待交付数据的等待时限。对应 TS 24.483 [4] §11.2.7 的 `TimeTempDataWaiting`。 |
| 包含近期受邀且可用的数据组通信列表的周期公告，用哪一个计时器 | `time-periodic-announcement` | 项 2：该周期公告的计时器。对应 TS 24.483 [4] §11.2.8 的 `TimePeriodicAnnouncement`。 |

一个是数据等交付的时限，一个是公告的计时器。公告里列的是**数据组通信**，不是受邀用户或待交付数据。以上两项不规定何时开始、复位或重启计时，不规定超时后清理或再次尝试，也不证明公告已发送或接收。TS 24.483 在这里只作定位。

### 结构正文只列一项，Schema 声明两项

§10.4.2.1 的共用项 1(a) 在可选 `tx-and-rx-control` 下只列 `time-temp-data-waiting`，没有列 `time-periodic-announcement`。后者仍见 §10.4.2.3 的 `common-tx-and-rx-controlType` 和 §10.4.2.7 共用项 2。不能从 §.1 没列就判第二项不允许，也不将共用项 1(a) 读成等待字段必填。

§10.4.2.3 把 `tx-and-rx-control` 设为 `common` 的直接可选子块。在它的类型中，两项依次为 `time-temp-data-waiting`、`time-periodic-announcement`，各为 `xs:duration`，均 `minOccurs="0"`，没有 `default` 或 `fixed`。按这两个声明，留其中一项、不留另一项，不因为这个省略就违反出现次数。缺项不补零、默认时长或“无限等待”；只看节选也不能判缺项。这个共用块不同于[在网同名块的四个字节上限](mcdata-on-network-tx-rx-byte-limits.md)。

### 格式不符和秒值无效要分开

§10.4.2.6 点名这两个共用字段，要求按秒表示。表示式原写 `PT<h>H<m>M<n>S`，其中 `<n>` 为有效秒值，可用十进制小数。格式校验句另用字面 `PT <n>S`。两处照原字面定位，不能据此指定空格、小时或分钟写法会被哪种解析器接受，也不把其他时长段的例子套进来。

| 条文触发条件 | CMS 响应 | 如果带 `phrase`，建议用 |
| --- | --- | --- |
| 这两项之一的值不符合原文所写的 `PT <n>S` 结构 | 必须返回 HTTP 409（Conflict），包含 XCAP `constraint-failure` | `invalid format for duration` |
| 收到无效的 `<n>` 值 | 必须返回 HTTP 409（Conflict），包含 XCAP `constraint-failure` | `invalid value for duration` |

两条都没有在这里列出有效 `<n>` 的数值范围，也没有规定条件重叠时先处理哪条。只知 409，不能区分这两种原因。不能因为叶可省略，就把已出现的空值或错误值当作没有该叶。若问题是[其他文档校验或文件可用时长](mcvideo-mcdata-service-config-validation.md)，另查相应条件。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcdata-common-tx-rx-duration-config.json)
