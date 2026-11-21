# 离网话权排队：私呼看双方 SDP，组呼看哪一位发出的请求？

看到 `mc_queueing`，先看它来自**私呼的哪一份 SDP**，还是**组呼的单向通告**。它表示支持话权请求排队，不表示有人已经排进队列；固定版语法写的是裸参数 `mc_queueing`，不是 `mc_queueing=1`。[TS 24.380 V16.9.0，§§12.1.2.2–.3，印 225–226](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=226)

## 私呼：主叫带了排队参数，被叫没有带，能算协商成功吗？

不能。离网 MCPTT 私呼的 `PRIVATE CALL SETUP REQUEST` 带 SDP offer，`PRIVATE CALL ACCEPT` 带 SDP answer。支持排队的主叫须在 offer 带 `mc_queueing`；被叫接受呼叫、收到带它的 offer，而且自己也支持排队时，须在 answer 带它。要确认双方在**这通私呼**选择了该能力，要对上这对完整 offer/answer 中的参数。只抓到 offer，尚不知道被叫如何回答；只知道被叫发了 `PRIVATE CALL ACCEPT`，也不能代替检查 answer。若完整 answer 没带该参数，不能登记已协商排队；这不等于该私呼被拒，也不能单凭缺参判定被叫终端为何没填。[§§14.6.1–.2，印 240–241](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=241)

## 组呼：发起者通告可排队，为什么乙按键还是收到拒绝？

通过 `GROUP CALL ANNOUNCEMENT` 或 `GROUP CALL BROADCAST` 发起组呼时，不能像离网私呼那样协商本次通话的能力。在普通离网组呼中，支持排队的发起者仍须在 SDP offer 带 `mc_queueing`。这说明发起侧支持，不是所有对端的回答。在使用排队的组呼里，规范的注说明参加者在各自 `Floor Request` 的 `Floor Indicator` 表明支持，字段表将 **F=1** 定义为支持排队。乙没有发出相应请求，或只抓到他人请求，不能用发起者的 SDP 代填乙的 F 位。[§§14.6.1–.2，印 241](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=242)；[§8.2.3.15 表 8.2.3.15-2，印 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=157)。

**再查乙这一次的请求，以及当时这组的配置。** 在普通离网组呼中，当前持有者有发言许可并负责仲裁。对已判为非抢占的请求，若组配置 `OffNetwork/QueueUsage=true` 却收到乙的 F=0 或缺 `Floor Indicator`，持有者须回 `Floor Deny` 原因 #1：另一终端已有许可。发起者通告支持，不能补这个请求所缺的字段。即使乙发来 F=1，也可能因队列满收到原因 #7；这不是私呼式协商失败。若看到 `Floor Queue Position Info`，还要核对乙终端是否按对应身份接受它，才能说乙本地已经进入排队。字段差异、组配置关闭时的行为和全部响应见[离网持有者仲裁和队列字段](offnetwork-floor-participant.md)。这一组配置分支不套到离网私呼或广播。[§§7.2.3.5.1、7.2.3.5.4，印 128–129](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=129)；[§7.2.3.5.4，印 129](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=130)；[§7.2.3.6.3，印 133–134](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=134)。

若乙的请求实际具有抢占优先级，查[离网话权请求如何判抢占](offnetwork-floor-preemption.md)。要复核私呼的接听握手而不是排队参数，查[离网自动私呼的建立](offnetwork-private-auto-client.md)。
