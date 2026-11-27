# IWF 私呼振铃与结束：两个用户 ID 分别指谁？

**主叫和被叫的 ID 一样，消息不一定一样。** IWF 振铃与结束请求都必带两个 ID；结束应答只列一个必带 ID，指**应答方**。先认这条消息的类型，再看字段。不要按网元发送方向换掉主叫、被叫，也不要把结束应答读成建呼成功或媒体已停。

这里读 **TS 23.283 V19.5.0，Rel‑19 Stage 2**，只看 **IWF↔MCPTT server 之间的 IWF‑1**。下列三表各列两个方向。M 为必带，O 为可选。查规范或已识别的一条消息，不需要先找到对应的前一条或后一条。[§10.4.1.1，印刷页 89（PDF 第 90 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=90)。

| 已识别的信息流 | 看哪些字段 |
| --- | --- |
| **IWF ringing（表 10.4.1.4-1）** | 主叫 MCPTT ID M，被叫 MCPTT ID M。Ringing indication O，指给主叫的指示；不据此识别收报网元或认定主叫听到回铃。 |
| **IWF call end request（表 10.4.1.5-1）** | 主叫 MCPTT ID M，被叫 MCPTT ID M，分别指原私呼的双方，不是释放发起者和响应者的配对。Additional application specific data O；NOTE 写 LMR 系统使用该项时可以携带。以 GSM‑R 的 UUI 为例，不是规定只能用 UUI 或使用 GSM‑R 就要带。 |
| **IWF call end response（表 10.4.1.6-1）** | 只列应答方的 MCPTT ID M，不固定为原主叫或被叫。不列另一个用户 ID、Result、SDP answer 或应用附加数据。 |

[振铃与结束请求表，印刷页 91（PDF 第 92 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=92)；[结束应答表，印刷页 92（PDF 第 93 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=93)。

**振铃看正在等待哪一方接受。** 在 §10.4.3.1 的 MCPTT 主叫分支，7 是 IWF→server，8 是 server→主叫 MCPTT 客户端的另一条振铃；在 §10.4.3.2 的 LMR 主叫分支，7 是 MCPTT 被叫客户端→server，8 才是 server→IWF 的振铃。这两支各只有 IWF‑1 的振铃那一腿使用 .4 表。某条出站记录不证明下一端收到，更不证明已接听或媒体建立。表的可选指示缺项，也不把已识别的 IWF ringing 改成其他消息。[§10.4.3.1/.2 步骤 7–11，印刷页 97、99（PDF 第 98、100 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=98)。

**看见附加数据或收到应答，先分建呼与释放。** 建呼的 IWF private call response（表 .3-1）也列可选的 Additional application specific data，并有必带的 Result 和选定媒体参数的 SDP answer。不能据名字或这项数据把它认成结束请求，也不能把建呼的 Result 结构套给结束应答。另一方面，非广播组呼释放请求有 server 发起时省略发起成员 ID 的规则（表 10.3.2.12-1）；它不适用于这里的私呼结束请求，后者仍分别列主叫和被叫 ID 为 M。[私呼应答表，印刷页 91（PDF 第 92 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=92)；[组呼释放请求表，印刷页 38（PDF 第 39 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=39)。

**匹配的结束应答有作用，但只证明本腿的确认。** 已建互通私呼由 MCPTT 客户端发起结束，§10.4.4.1 第 4 步是 IWF 给 server 的确认；由 server 发起时，§10.4.4.2 第 4 步分别有 IWF 和客户端的确认，不能合并。由 LMR 发起时，§10.4.4.3 第 5 步是 MCPTT 客户端向 server 确认，第 6 步才是 server 向 IWF 的确认。读哪条核哪条；把请求和应答关联到一次操作，才需要对应呼叫、端点和事务证据。实际发出确认、另一端收到它、终端提示和资源释放要分开看。IWF 或 server 的传输身份不自动给出表 .6-1 的应答方用户 ID。[§10.4.4.1–.3 的确认，印刷页 100–102（PDF 第 101–103 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=101)。

问[手动私呼怎么接受](private-manual.md)、[已建私呼怎么释放](private-release.md)或[自动私呼如何看建立应答](private-automatic.md)，按对应程序读。这里不定义终端这一腿的线级编码、SIP 状态码、UUI 格式或收到应用数据后的处理。
