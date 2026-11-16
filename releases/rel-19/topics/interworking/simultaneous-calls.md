# 同一LMR用户的多路互通呼叫

TS23.283 V19.5.0，Release19，Stage2。在网同时互通呼叫场景。

## 在网IWF代表同一LMR用户

IWF可支持该用户的同时多路互通呼叫。代表用户邀请、加入或接受多路呼叫，以及归属多个组，可能使用户处于多路呼叫中；归属多个已有活跃呼叫的组可能带来同时邀请。 [§10.10.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 需要处理同一LMR用户的同时互通呼叫

IWF如何容纳这些同时呼叫不在本规范范围；不能从可支持多呼叫推出必须混音、自动抢占或具体优先级调度。 [§10.10.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

TS23.379§10.8为基础依赖，本页未核验其完整同时会话行为。

[affiliation-representation](affiliation-representation.md) · [late-entry](late-entry.md) · [结构化条件](simultaneous-calls.json)
