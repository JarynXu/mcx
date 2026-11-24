# 谁能配置哪些内容源向某个 MCX 用户发送内容？

**调度员或获授权用户**须能配置哪些内容源可以向某个 **MCX 用户**发送内容。业务须提供这项配置能力。比如，配置者可以选定事件现场附近的视频摄像头作为内容源。摄像头是例子，不是对源类型的限定。配置者、内容发送者和目标用户是三个角色。[TS 22.280 V16.8.0 §5.5.1 R-5.5.1-001，印刷页 16](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=17)。

配置好某个源，不代表它已开始发送，也不代表目标用户收到了内容。本项未规定默认许可、授权发放者或传送方式。接收对象若是**业务组**，读[组通信的内容源配置](common-group-transmission-and-setup.md)；若要判断哪个用户能发起在网无话权控制私通信、能与谁通信，读[在网私通信授权](onnetwork-no-floor-private-authorization.md)。这两项不替代本页对内容源的配置。

这是 Release 16 的 Stage 1 要求，出自[在网和离网共用的第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。按 §5.5.1 本行判断：规范性[表 A.1（MCPTT），印刷页 63](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=64)写 NA，[表 B.1（MCVideo），印刷页 74](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=75)和[表 C.1（MCData），印刷页 85](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=86)列出 R-5.5.1-001。本项适用于 MCVideo 和 MCData；NA 不能读成禁止 MCPTT 提供类似能力。
