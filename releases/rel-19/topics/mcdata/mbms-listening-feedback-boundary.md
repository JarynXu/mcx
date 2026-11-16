# MBMS监听反馈：触发、对象与证据边界

## 适用范围

- 固定TS24.282 V19.7.0 §19在网MBMS；PF指参与MCData功能，终端为其服务的MCData客户端。不是§19A的5GS MBS，不把两者身份、承载或术语直接等同。
- 本页的使用条件是公告处理、区域可用性及监听报告条件，不替代组归属、业务授权或完整安全准入。公告、监听、映射、数据到达和应用处理分别判断。
- 只核24.282信令责任。TS24.582的MBMS媒体、TS33.180密码过程、RAN服务区/无线条件检测及所引RFC未核，不提供实现算法或精确版本组合互通保证。
- 各条结论继承共同条件且仅按自身角色、状态和触发执行；发生拒绝并要求停止时不得继续。未展开承载创建、MuSiK下载、暂停预警和全部Map/Unmap过程。

## 两条独立的监听报告路径

适用条件：客户端未因公告处理失败而停止；分别判断会话映射触发与通用子信道可用触发。

须报listening的两条独立路径是：收到通用子信道上的Map Group To Bearer，参与所指组会话且尚未报listening；或收到公告、进入通用MBMS可用服务区并具有良好承载无线条件。第二路径不附带第一路径的已参与会话和未重复报告条件。它报告监听状态，不确认业务包、文件或应用内容到达。

- 未核good的测量算法/阈值，不创造迟滞计时或首包门槛。

依据：TS24.282 V19.7.0 §19.3.3.1 first condition set，印刷页 432。

## 不再监听的实际触发

适用条件：分别观察公告取消与无线条件变差；依据19.3.3.1的not-listening分支判断。

须报not-listening的触发是：取消项对应正在进行会话的映射TMGI且尚未报not-listening；或取消公告、当前未参加会话、此前因该公告通用子信道可用而报过listening且尚未报not-listening；或遭遇差的MBMS承载无线条件。不要把未核的暂停预警流程混入这些触发，也不要给无线变差分支自行追加前两支条件。

- 原文取消分支将标识拼为TGMI；本页按同一公告标识语境说明，不提供修正后XML模板。
- 不补退出服务区的独立码值、暂停预警或取消确认算法。

依据：TS24.282 V19.7.0 §19.3.3.1 second condition set，印刷页 432、433。

## 反馈对象与报告范围

适用条件：客户端满足报告触发，准备向PF发送监听或不监听报告。

须用SIP MESSAGE发往公告P-Asserted-Identity所给PF的MBMS服务身份，带版本1及自身MCData ID。listening与not-listening分别标记状态；针对进行中会话子信道时带session-id，针对通用子信道时general-purpose分别为true/false，并携适用承载标识。P-Preferred-Identity仅SHOULD。通用子信道不再监听还隐含此前报listening的进行中会话子信道均不再监听，不代表会话已释放。

- 省略了通用SIP头配方，不能当可运行消息模板。原文适用承载字段写TGMI而公告写TMGI，且g分支编号重复iii；schema未核，不静默纠正。

依据：TS24.282 V19.7.0 §19.3.3.2 listening-report procedure,NOTE2，印刷页 433、434。

## PF验证身份后更新媒体状态

适用条件：PF收到监听状态更新，含mbms-listening-status及mcdata-info中的mcdata-request-uri，且该MCData ID由本PF服务。

PF须验证P-Asserted-Identity的公共用户身份与body中MCData ID绑定。仅绑定成立后，按listening/not-listening以及session-id或general-purpose的条件通知媒体面；not-listening还须调用24.582媒体过程。通用子信道不再监听的隐含会话范围同样适用。这是身份校验后的媒体状态更新，不是数据交付回执或全体组员收齐证明。

- 本分支未把所有绑定失败情况映射为统一403，本页不编造响应。
- 未核24.582对应媒体动作，不据此断言立即切单播或已完成流量迁移。

依据：TS24.282 V19.7.0 §19.2.3 listening-status branch and NOTE1，印刷页 429。

## 证据边界

- 限所列公告与监听链；不建立MBMS端到端交付保证。

## 按需继续

- [MCData 服务授权如何建立绑定：身份来源、并发上限和响应边界](service-authorization-binding.md)
- [MBMS公告与终端监听条件](mbms-announcement-and-listening-conditions.md)

[TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅所列版本和条款。
