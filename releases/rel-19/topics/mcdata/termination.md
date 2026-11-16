# MCData 在网终止：预告、原因与补充信息

适用：Rel19，TS22.282 V19.0.0，Stage1 在网要求。

服务可预告终止，也可不预告就终止；原因字段本身也是可选的（§6.2.3 R-007–009）。收到预告后，UE 须向用户呈现预告及其中已有的原因；实际终止通知的用户呈现则为可选能力，若呈现也包括其中已有的原因（R-010/010a）。

服务可在终止预告中请求更多信息。UE 必须响应，但响应不一定带剩余数据量，该字段为可选（R-011/012/012a及注2）。因此，不能把“有义务响应”解释成“必能报告精确剩余字节数”。

## 使用边界

仅覆盖 Stage1 通知义务；不列举完整终止条件，不规定请求编码、响应超时或延长是否获准。

[transmission-options.md](transmission-options.md) · [delivery-evidence.md](delivery-evidence.md) · [来源](https://www.etsi.org/deliver/etsi_ts/122200_122299/122282/19.00.00_60/ts_122282v190000p.pdf)，印刷页16。

Stage 1 要求之后用本版 Stage 3 核预告、查询、计时与结果的具体承载。 [session-release-extension](session-release-extension.md)。

Stage1概览之后按HTTP分支核Stage3条件。 [http-fd-release-extension](http-fd-release-extension.md)。
