# MCPTT 功能别名：怎样申请启用或停用，怎样知道结果？

例如，用户想启用“值班调度”这个功能别名。客户端用 SIP PUBLISH 提交请求；要知道这次变更成功还是被拒，应先为该用户发起状态订阅，再发 PUBLISH。随后看 SIP NOTIFY 里这个别名的状态。只查了一次当前状态，不能靠那次查询收到以后的变更通知。

依据：[3GPP TS 24.379 V16.14.0，Release 16，Stage 3](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=200)，§9A.2.1.1–3，印刷页 199–201。以下以用户手动申请为例。

## 先选要观察谁、观察多久

可以查询本人或另一名 MCPTT 用户已启用哪些别名。初始 SUBSCRIBE 发给服务于查询者的起始参与 MCPTT 功能：SIP 的 Request-URI 填该功能的公共服务身份，消息体 `mcptt-request-uri` 填**被查询用户**的 MCPTT ID。MCPTT 信息体中的 `request-type` 为 `functional-alias-status-determination`；P-Preferred-Service 指明 MCPTT 业务，订阅的事件包为 `presence`，Accept 包含 `application/pidf+xml`。

初始 SUBSCRIBE 的 Expires 为 0，只取当前状态；为 4294967295，则取当前状态并订阅后续通知。已有订阅时，在同一对话内再发 SUBSCRIBE：用 4294967295 续订，用 0 退订；事件包和 Accept 保持上述取值。（§9A.2.1.3，页 200–201）

## 用户的请求何时发出

**手动停用前先查配置。** 客户端查看用户在网配置档中该别名的 `manual-deactivation-not-allowed-if-location-criteria-met`。如果别名是由位置区域触发启用的，并且该项为 `true`，客户端就不发送这项停用请求。此时可以提示用户，但规范不要求一定显示提示。（§9A.2.1.2，页 200）

对需要发出的请求，同一次 PUBLISH 可以申请启用多个别名，也可以申请停用多个别名。启用时 Expires 为 4294967295，停用时为 0；两种操作不能放在同一次 PUBLISH 中。请求仍发给服务于发起用户的起始参与功能，P-Preferred-Service 指明 MCPTT；MCPTT 信息体的 `mcptt-request-uri` 填该用户的 MCPTT ID。（§9A.2.1.2，页 199–200）

按用户组织的 PIDF 消息体（`application/pidf+xml`）另写目标客户端的 MCPTT 客户端 ID；申请启用时列出该用户为这个 MCPTT ID 请求启用的全部别名。请求中的别名条目不写 `status` 和 `expires` 属性。客户端在根元素 `presence` 下为这次发布填写全局唯一的 `p-id-fa`。如果客户端已收到可以接管某个别名的指示，而且确实打算接管，就把 `take-over` 子元素设为 `true`。（§9A.2.1.2，页 200）

## 收到通知后，怎样认出这次变更

当 NOTIFY 含有符合 §9A.3.1 的按用户组织的功能别名 PIDF 消息体时，客户端逐个读取其中的别名，判断该用户在每个别名上的状态。如果通知的 `presence` 下带有 `p-id-fa`，可以把它与发布时的值对应，找出触发这份通知的 PUBLISH。没有这个字段，客户端仍须逐个判断所列别名的状态，但不能用这个字段关联发布。检测到别名启用或停用后，客户端按 §9.2.1.7 执行基于规则的组归属程序。（§9A.2.1.3，页 201）
