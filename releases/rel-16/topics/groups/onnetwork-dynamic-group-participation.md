# 在网动态组参与：谁能按条件自动归属或选定组？

**自动归属和自动选定是两项动作。** 每项动作又分两条要求：业务须让用户具备自动处理的能力，业务自己也须能替用户自动处理。依据是 3GPP TS 22.280 V16.8.0（Release 16）的在网动态组参与（Dynamic Group Participation）Stage 1 要求。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)；[§6.6.5.2，印刷页 37（PDF 第 38 页）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。

| 动作 | 业务须使 MCX 用户能够做什么 | MCX 业务自身须能做什么 |
| --- | --- | --- |
| 自动归属（affiliation） | 使用户能够按一个条件或多个条件的组合，自动归属到一个或多个 MCX 业务组。[R-6.6.5.2-001，印刷页 37](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。 | 业务自身须能按一个条件或多个条件的组合，为该用户自动建立对一个或多个 MCX 业务组的归属。[R-6.6.5.2-002，印刷页 37](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。 |
| 自动选定（selection） | 使用户能够按一个条件或多个条件的组合，自动选择自己的选定 MCX 业务组（Selected MCX Service Group）。[R-6.6.5.2-003，印刷页 37](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。 | 业务自身须能按一个条件或多个条件的组合，为该用户自动选择其选定 MCX 业务组。[R-6.6.5.2-004，印刷页 37](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。 |

表内四项都是业务**必须具备的能力**，不以已有操作、已经发生条件变化或观察到结果为前提。“让用户能够”不是必须提供某种开关；“业务为用户”也不是条文规定了授权委托步骤。只知道某一条能力存在，不证明另外三条已经实现。

例如，只知道甲能够按位置自动选定巡检组，(1) 不能据此认定业务自己能替甲选定，(2) 不能推定甲归属了巡检组或撤销了旧组归属。条款没有把选定和归属设成彼此的前置步骤，不规定条件怎样组合、规则优先级、显式信令或此次结果。地理区域、功能别名等是同页附注的条件示例，不是必选条件。

**适用业务：** 表 A.1（MCPTT）、B.1（MCVideo）、C.1（MCData）均在 §6.6.5.2 要求行列出 -001 至 -004。本页不收录 -005 至 -007，不凭这四条推断撤销归属、组成员资格或入呼。[表 A.1，印刷页 67](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=68)；[表 B.1，印刷页 78](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=79)；[表 C.1，印刷页 89](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=90)。

若问[用户重组怎样维护临时组成员与配置归属](onnetwork-user-regroup-membership.md)、[终端自动归属两类广播组](onnetwork-affiliation-and-revocation.md)或[获授权用户变更他人的归属组或选定组](onnetwork-remote-group-change.md)，按对应的 Stage 1 条款判断。若问具体的 [MCPTT 客户端归属规则](client-rules-affiliation.md)或[组地理区域通知](group-geographic-area-notification.md)，按各自的 Stage 3 条件查证，不把其中的规则判法、消息或结果套给此处四项业务能力。
