# CF 的 INVITE 临时应答：PAI 和 Contact 分别标识什么？

控制 MCPTT 功能（CF）**对收到的 SIP INVITE 发送非 100 临时应答时**，须生成该应答，并在 `P-Asserted-Identity`（PAI）中带上 CF 自己的公共业务标识（PSI）。`Contact` 放的是 MCPTT 会话标识。两处字段回答不同的问题：一个标识控制功能，另一个标识会话。[TS 24.379 V16.14.0 §6.3.3.2.3.1，印刷页 120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=121)

这份 `Contact` 还须带三项标记：

- `g.3gpp.mcptt`
- `g.3gpp.icsi-ref`，值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`
- `isfocus`

这条规定不适用于 `100 Trying`，也没有要求每个 INVITE 都发送一份非 100 临时应答。它只说明 CF 发出的这一腿临时应答，不说明终端在另一腿实际收到了什么。

即使抓到这份 `Contact`，也不能把这条临时应答记成 INVITE 的最终接受，或由此认定已重入、已归属、已获话权。要查最终应答和 ACK，应读[重入 INVITE 的最终应答与 ACK](rejoin-late-entry.md)，不要用这里的临时应答代替本腿的最终应答。若查聊天组纠正优先级时 183、PRACK 和最终应答各说明什么，读[聊天组建立、加入与优先级纠正中的应答](chat-establish-join.md)。
