# MCData 预建立共享资源：SIP 支持、Rx 绑定与完成证据

## 适用范围

- 固定 TS24.282 V19.7.0 与 TS29.214 V19.3.0，均为 Release19 Stage3；两版并列不表示已验证组合互通。
- MCData 用途仅普通在网、media standalone SDS/SDS session 的客户端—PF预建立会话；注册、服务设置和逐请求准入仍适用，不扩展FD/IPCONN。
- Rx 结论仅本文所列 AF/PCRF、IP-CAN 与 PCC/PCEF/BBERF 语境；不展开29.214 Annex E的5GS适配，也不转成N5/PCF/UPF契约。
- SIP-core与PF直接Rx是不同路径；只在明确主体下使用相应结论。P-CSCF Annex A规则不能不加条件套给直接Rx的PF。
- 未核TS24.229、29.212、29.213、29.229和23.228的固定版依赖；不从共享键、响应或接口调用推定承载实现、独立媒体资源、业务连通或逐消息交付。

## 先区分两条共享路径

MCData PF 可经 SIP core 使用共享，也可直接经 Rx 控制 PCC。TS24.282 §18.1/.2（印刷页418、419）要求预建立会话使用共享；即使共享受支持，允许客户端使用仍是 MAY。SIP-core支持可由第三方 REGISTER 的 message/sip 中 Resource-Share=supported 识别，registration-token用来识别注册UE。注册成功不替代服务设置、共享支持或逐请求准入。

§18.3.2.2（印刷页421）的 SIP-core 分支还核对 MCData ID 与注册UE的绑定，以及 INVITE Feature-Caps 中的UE标识。共享不支持、所列绑定缺失或PF不支持预建立时，403/226拒绝并停止。直接Rx路径不能作为省略该拒绝条件的依据。完整准入和预建立200的范围见[既有准入主题](../mcdata/pre-established-session-admission.md)。下列Rx条件也不能用SIP注册成功代替。

## SIP共享应答是逐流规则，不是单一成功标志

适用主体：参与MCData PF。

适用条件：已通过§18.3.2.2此前准入；SIP core支持resource sharing，PF生成预建立INVITE200。

Resource-Share answer使用media-sharing，origin为session-initiator，并带timestamp及rules；每个媒体流一条规则，顺序与SDP m-line一致，每条包括new-sharing-key与对应流的directionality。

规范强度：shall，受SIP-core支持条件限定。

- 24.229定义具体header语法和转换；不能仅据这些字段实现完整Resource-Share解析器，也不能将new-sharing-key字面直接当成29.214数字AVP。
- 不反向推导直接Rx路径必须发送相同SIP头。

依据：TS 24.282 V19.7.0 §18.3.2.2 step9d，印刷页421。

## Rx共享支持需要本会话的特性交集

适用主体：Rx AF与PCRF。

适用条件：使用Rx的Supported-Features协商；拟使用resource-sharing扩展。

首请求声明客户端特性，首应答给出双方共同特性；后续命令遵守该集合，未声明支持的特性不得用于命令构造。Feature-List-ID 1的bit11 ResShare表示跨多个AF会话共享资源，属于可选特性。

规范强度：协商约束shall/shall not；ResShare实现可选。

- Resource-Share=supported是MCData所见SIP-core信号，不是已核的Rx逐跳特性协商记录；不以SIP注册成功替代ResShare支持。
- 29.229的发现/错误处理依赖未核，不构造完整协商失败算法。

依据：TS 29.214 V19.3.0 §5.4.1；Table 5.4.1.1 ResShare，印刷页65、66、67、68。

## UE注册绑定不替代Rx的IP-CAN会话绑定

适用主体：AF与PCRF。

适用条件：PCRF收到初始AAR；AF提供适用于到UE之流的会话信息。

AF须提供完整UE IP地址，PCRF按29.213执行session binding；私网情况下可补Called-Station-Id中的PDN信息及IP-Domain-Id。绑定失败回AAA并给IP-CAN_SESSION_NOT_AVAILABLE。

规范强度：地址及绑定shall；补充信息may。

- 重复私网地址可能使单独IP不足；29.214 NOTE7明确非IMS AF取得UE私网地址及不保留原私网地址协议的支持缺口。
- MCData ID与registration-token标识UE的绑定另由24.282准入处理；不发明该token到IP-CAN/AVP的映射。
- 29.213完整绑定算法未核。

依据：TS 29.214 V19.3.0 §4.4.1 session binding;NOTEs6–7，印刷页18。

依据：TS 24.282 V19.7.0 §18.2；18.3.2.2 steps4–5，印刷页419、421。

## 共享键区分方向和同一用户的媒体组件关系

适用主体：Rx AF。

适用条件：同一用户、跨AF会话的媒体组件；相应方向需要适用或不适用资源共享。

Sharing-Key-DL与Sharing-Key-UL分别标识下行和上行共享关系。同方向需共享的组件使用相同键值，不共享的组件使用不同值；AF可在Media-Component-Description中提供键来表达共享关系。

规范强度：同/异值规则shall；发送共享指示may。

- 键不是MCData业务session identity，也不是媒体内容、MSRP连接或独立承载已建立的证明。
- 不提供键分配算法、全网唯一范围、资源容量计算或承载合并实现；不把resource sharing与ARP priority sharing混同。

依据：TS 29.214 V19.3.0 §4.4.1 Sharing-Key paragraph；5.3.37；5.3.38，印刷页16、53。

## Rx应答与实际资源执行分开

适用主体：PCRF。

适用条件：收到携带Sharing-Key的媒体组件信息，进入初始授权正常应答分支。

PCRF可按29.212应用资源共享；须向AF返回AAA，确认应在所需PCC规则下发之前或并行发生。因而不能由AAA单独证明共享承载已执行或每个AF会话拥有独立资源。

规范强度：应用共享may；应答shall；相对下发时序should；证据边界为有限推论。

- 不把should改成强制先后，也不把携带键改成PCRF必定实施共享。
- 29.212/29.213授权、下发及执行结果未核；不从资源授权推出SDS业务成功。

依据：TS 29.214 V19.3.0 §4.4.1 resource sharing and AA-Answer paragraphs，印刷页19、20。

## P-CSCF停止共享不等于销毁AF会话

适用主体：P-CSCF，及相关PCRF。

适用条件：仅IMS/P-CSCF路径；P-CSCF按24.229判断共享可行或需要停止共享。

A.12允许P-CSCF标明跨AF会话共享；新AF会话按媒体组件分配不同共享键，双向共享时同一组件两方向可同值。停止共享的触发在24.229；NOTE2说明停止时提供同一用户其他AF会话未使用的新键值。

规范强度：指示may；逐组件区分shall；双向同值可用；停止说明为NOTE。

- 这不是直接PF Rx路径的完整触发程序，也不是终止会话的STR；不得推导已释放整个共享承载。
- A.12另禁止Emergency Session带共享键，并禁止PCRF对RTCP相关PCC/QoS规则带该键；普通MCData范围不因此获得紧急或RTCP流程覆盖。
- 24.229/23.228依赖缺失，SIP Resource-Share到Rx键转换及停止时机仍未闭合。

依据：TS 29.214 V19.3.0 §A.12 including NOTEs1–2，印刷页90。

## Rx终止只沿对应AF会话及SDF收尾

适用主体：AF与PCRF。

适用条件：AF会话终止；本条限普通终止，不含请求access-network信息、sponsored阈值或RAN-NAS-Cause相关延后应答分支。

已收到初始成功AAA时AF须发STR；否则条文要求先等初始AAA。PCRF收到STR后回STA，随后请求移除相关PCC/QoS规则并更新受影响IP-CAN bearer的授权QoS，以释放对应SDF资源。

规范强度：shall。

- 不从“否则等待”补造初始失败AAA后的完整恢复算法。
- STA不是PCEF/BBERF完成回执；“对应SDF”不能扩为其他AF会话、整UE或整个IP-CAN全部释放。共享场景如何保留其余规则/承载的具体算法属于未核29.212。
- MCData业务leave与销毁预建立SIP会话仍沿既有24.282主题判断；本条不建立任意BYE到STR的一一映射。

依据：TS 29.214 V19.3.0 §4.4.4 opening and ordinary termination paragraphs，印刷页24。

## 原文接口与适用边界

- TS 24.282 V19.7.0 §18.3.2.2 steps4–5，印刷页421：step4写SIP-core支持时核UE绑定，step5拒绝绑定缺失的文字未加同一前提；保留直接Rx路径绑定契约未闭合，不以两路径替代关系删除step5。
- TS 29.214 V19.3.0 §4.4.1 NOTE7，印刷页18：非IMS AF取得原UE私网地址存在明示范围缺口；不假设MCData PF自动拥有该信息。
- TS 29.214 V19.3.0 §A.12;5.3.37/.38，印刷页53、90：A.12新会话逐组件不同值，与同用户跨会话需共享时同值描述属于不同上下文；不裁成全局唯一或任意同值，也不补24.229触发/映射。

## 未覆盖的依赖

- TS24.229的Resource-Share完整语法、共享/停止触发、registration-token生成转发及SIP到Rx映射未核。
- TS29.212的共享实施和剩余资源保留、TS29.213完整session binding、TS29.229特性错误框架及TS23.228 IMS架构未核。
- TS24.582媒体复用和业务/消息资源映射不在本页覆盖范围；这些接口片段不构成可运行的预建立共享实现或精确版本互通验证。

## 按需继续

- 需要区分注册、预建立准入和INVITE200，查[MCData 预建立会话：SDS 范围、共享资源与准入](../mcdata/pre-established-session-admission.md)。
- 需要判断REFER及逐业务建立结果，查[预建立会话上的私聊 SDS：REFER、业务 INVITE 与结果反馈](../mcdata/pre-established-private-sds-use.md)。
- 需要区分业务leave与预建立SIP会话销毁，查[预建立会话的退出：离开 SDS 业务与销毁会话](../mcdata/pre-established-leave-and-release.md)。
- 需要追溯MCData用户、client与IMS身份绑定，查[MCData 服务授权如何建立绑定：身份来源、并发上限和响应边界](../mcdata/service-authorization-binding.md)。
- 遇到Rx暂时拒绝或重试间隔，查[Rx 临时拒绝与重试间隔](rx-retry.md)。

[TS24.282 V19.7.0 官方版](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；[TS29.214 V19.3.0 官方版](https://www.etsi.org/deliver/etsi_ts/129200_129299/129214/19.03.00_60/ts_129214v190300p.pdf)。各结论按所列固定版本与条款适用。
