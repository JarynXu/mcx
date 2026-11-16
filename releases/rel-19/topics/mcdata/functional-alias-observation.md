# 功能别名观察：变更前订阅与当前状态查询

限TS24.282V19.7.0 MCData客户端功能别名状态确定过程；观察自己、其他用户或某个别名的目标含义不可互换。

这里只核客户端发起方式和必要观察边界，不因能够构造SUBSCRIBE就宣称已获准观察任意其他用户，也不展开跨服务器授权。

## 变更前启动状态观察

适用条件：客户端希望得知某MCData用户的功能别名状态变更是否成功或被拒。

§22.2.1.1要求在启动该用户的状态变更过程之前，先发起该用户的状态确定过程。这样变更意图和状态观察有独立通路；不能只发PUBLISH并把其事务结果当作最后的激活/停用结果。原文规定的是先发起，不额外规定必须等到某个特定SUBSCRIBE响应后才允许PUBLISH。

- 这个先后要求带有获得变更成功/拒绝信息的目的条件，不改写成所有只读查询都必须伴随PUBLISH。
- 仅发起订阅并不证明订阅已获准或持续存在；发送失败和竞态恢复仍依赖未展开的SIP事件规范。

依据：§22.2.1.1;22.2.1.3 opening and NOTIFY handling，印刷页 476、478、479。

## 按用户或按别名选择查询目标

适用条件：客户端发起初始SUBSCRIBE查询当前或后续别名状态。

Request-URI指向服务本用户的originating PF公共服务身份，并携MCData服务标识。按用户查激活别名时，mcdata-request-uri取目标MCData ID，request-type为functional-alias-status-determination；按某个别名查已激活它的用户时，mcdata-request-uri取该功能别名，request-type为fa-user-status-determination。两者虽然共用presence订阅和application/pidf+xml接收类型，却不是把用户ID和别名ID放进同一含义的字段后随意互换。

- 正文step2A把request-type放在mcdata-Params的anyExt中，step2放在mcdata-Params中；保留两分支的编码位置差别，不提供统一XML模板。
- 本批结果解释以per-user状态通知为主，未完整核per-functional-alias解析、服务器发现或跨域查询流程。
- 客户端正文使用Events header字面，服务端入口使用Event；见原文差异，不据此生成改写后的报文。

依据：§22.2.1.3 initial SUBSCRIBE steps1,2,2A,3,6,7，印刷页 478。

## 查询、持续观察与取消订阅

适用条件：区分初始SUBSCRIBE与同一dialog内的重新订阅/取消订阅。

初始SUBSCRIBE若要当前状态和后续通知，Expires取4294967295；若只取当前状态，Expires取0。重新订阅和取消则使用in-dialog SUBSCRIBE：继续观察请求4294967295，取消请求0，并继续携presence事件标识与application/pidf+xml的Accept。因而Expires=0在初始请求中是当前状态fetch，在既有dialog内是取消订阅，不能只看数值判断业务动作。

- 4294967295是本节要求填写的请求值，不证明订阅永久不失效；实际SIP事件生命周期、响应与刷新算法依赖24.229/RFC6665，未展开。
- SUBSCRIBE的Expires不等于PUBLISH的控制意图，也不等于NOTIFY中单个别名的expires时间。

依据：§22.2.1.3 initial SUBSCRIBE steps4–7;in-dialog SUBSCRIBE steps1–4，印刷页 478、479。

## 证据边界

- 未展开对其他用户的权限判定、订阅失败恢复、跨域路由和完整presence事件实现。

## 按需继续

- [functional-alias-change-request](functional-alias-change-request.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

- §22.2.1.3 initial steps6/in-dialog step3;22.2.2.2.4 opening4：客户端段写Events header，服务端入口写Event header。 保留字面差异并引用presence事件意图，不无声修订客户端拼写，不据本批生成完整报文。

- [后续服务器条件与证据](functional-alias-owner-observation.md)

- [功能别名目标的解析与路由边界](sds-functional-alias-resolution.md)
