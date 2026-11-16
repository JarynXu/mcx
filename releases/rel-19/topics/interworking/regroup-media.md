# 重组后的 LMR 加密与编解码兼容

适用：Rel19，TS23.283 V19.5.0，Stage2 MC/LMR 互通。仅下列结论已对照原文。

只要参与重组的一个 LMR 组要求 LMR 端到端加密，MCPTT 临时组就宜优先采用 LMR 语音编解码。若某个成员不支持 LMR 加密或优选的 LMR 编解码，使用该加密的语音呼叫会对该成员失败（§10.2.2.6）。这不是对全组必然失败的判断，也不说明可以自动降级绕过加密要求。

## 边界与后续读取

该规范将 MC 系统如何判定临时组需要 LMR 加密或编解码排除在范围外（§10.2.2.6 注1、2）；本页不提供协商或转码实现。

[regroup-boundaries.md](regroup-boundaries.md) · [group-call-request.md](group-call-request.md) · [来源](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)，印刷页29。
