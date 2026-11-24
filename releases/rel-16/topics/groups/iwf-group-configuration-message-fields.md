# IWF 组配置：四类消息各带哪些信息，Result 说明什么？

TS 23.283 V16.8.0 这八张 Stage 2 信息流表都把 `MC service group ID` 标为 M（必带）。其余信息要看消息类型和各表注释。字段内容不决定实际报文走哪条协议。

## Information：取配置的请求和响应

请求表只有必带的组 ID。响应也必带组 ID，另有两项在 `Status` 列标 O：

- 请求能满足时，注 1 要求带 `MC service group provisioning information`。
- 请求不能满足时，注 2 要求带 `Result`，说明不能提供配置的原因。

O 不能盖过这两条必带条件。注释只写各自条件下必须出现哪一项，没有禁止另一项在这个条件下出现。这里的 `Result` 是失败原因，不是接收方已保存的回报。[表 10.2.1.8-1，印刷页 22](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=23)；[表 10.2.1.9-1，印刷页 23](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=24)。

## Provision：提供配置的请求和响应

请求除组 ID 外，还必须带 `MCPTT group configuration information`。响应除组 ID 外，还必须带 `Result`，报告**接收、修改和存储**组配置的成功或失败。仅知道这个字段存在，不能判断它报告了成功还是失败。[表 10.2.1.10-1 与表 10.2.1.11-1，印刷页 23](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=24)。

不要只凭图中的 provision 字样套表。已收录的 [§10.2.3.5](iwf-defined-group-configuration-pull.md) 写的是 MC 系统缺配置后向 IWF 取，IWF 返回所请求的配置。图中用了 provision 标签，编号正文仍未让 MC GMS 回报收存；不能据此认定用了表 10.2.1.11-1 的响应或确认了哪一侧的保存。

## Subscribe：请求哪些业务，响应确认哪次请求

请求必带组 ID；`MC services requested` 标 O。如果带该项，业务是 MCPTT、MCData，或两者。表没有为省略该项规定默认业务，也没有列 MCVideo。响应必带组 ID 与 `Result`，后者只报告**订阅请求**成功或失败。[表 10.2.1.12-1，印刷页 23](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=24)；[表 10.2.1.13-1，印刷页 24](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=25)。

## Notify：引用和密钥材料至少有一项

请求必带组 ID。`MC service group information reference` 指向已存的组相关信息，`Group related key material` 是供该组使用的密钥材料。两项各标 O，表注要求**至少一项出现**：

- 有组 ID，没有信息引用，但带组相关密钥材料：满足这两项的存在条件。
- 有组 ID，只带引用而不带密钥材料：也满足；两项都有不违反该条件。
- 只有组 ID、两项都没有：不满足该条件。

这是字段存在条件，不足以证明整条请求有效、密钥已安装或更新已经送达。响应必带组 ID 与 `Result`；这里的结果只报告**通知请求**成功或失败。[表 10.2.1.14-1 与表 10.2.1.15-1，印刷页 24](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=25)。

要判断谁提供、谁补取以及各自的前提，查 [MC 与 IWF 的提供和补取流程](iwf-group-configuration-transfer.md)；若是 MC GMS 向 IWF 补取，查上面的 §10.2.3.5。要判断订阅和通知走哪一侧，按组主系统查 [MC 定义组](mc-group-configuration-subscription.md) 或适用的 [LMR 定义组](lmr-group-configuration-subscription.md) 流程。字段在表中的要求不代证某次收件、入库、终端交付、归属或线上编码。
