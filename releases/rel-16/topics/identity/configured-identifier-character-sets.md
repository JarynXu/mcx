# MCX 标识符能用哪些语言字符？

配置指定哪些国际语言字符集，MCX 业务就须支持使用这些字符集的标识符。这是 3GPP TS 22.280 V16.8.0（Release 16，Stage 1） 的 [R-5.1.4-001，印刷页 13](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=14)；[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13) 是在网与离网共用的要求。[表 A.1（MCPTT），印刷页 62](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=63)、[表 B.1（MCVideo），印刷页 73](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=74)、[表 C.1（MCData），印刷页 84](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=85) 均在 §5.1.4 行列出本项。

例如，验收问题可以是“配置指定的字符集能否用于标识符”，而不是“界面能否显示多种语言”。本项没有指定 UTF-8、字符数量、大小写规则或配置者，也没有规定每一类标识符都须接受任意文字。

若问 ID 和别名由谁配置、能否临时分配、唯一性怎样要求，见[在网 ID 与别名管理](onnetwork-id-and-alias-management.md)。若问接收端拿到谁的 ID 和别名、怎样呈现，见[在网组通信的发送者标识](onnetwork-group-sender-identification.md)。
