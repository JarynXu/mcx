# MCData本地位置报告配置：许可、替换更新与触发边界

## 适用范围

- 固定TS24.282 V19.7.0，在网直接MCData ID列表的位置报告配置；目标配置由当前PF管理。排除功能别名、跨PF转送、完整测量/地理围栏/自适应算法。
- 请求客户端、PF和接收客户端按各自实际事件及claim条件处理；不将许可通过、收到200或目标已应用配置作为全页共同前提。
- 本页核配置生命周期有限责任，不将Stage1/2订阅取消或触发覆盖规则移作Stage3报文与停报算法。

## 配置许可、请求200与逐目标下发是三层判断

**条件：** 请求客户端分支以获授权用户要替换或修改一个或多个目标配置为入口；PF分支独立以实际收到配置替换/修改MESSAGE为入口，不预设请求许可或身份绑定已通过。正常后续以前序未停止为条件；逐目标分支限由当前PF管理配置的直接MCData ID。

请求客户端向服务自己的PF公共服务身份发送MESSAGE，用resource-lists的entry.uri列出目标MCData ID，并携location-info内的Configuration；P-Preferred-Service和带require/explicit的Accept-Contact使用MCData ICSI，可带P-Preferred-Identity。PF依次处理资源/拥塞、从PAI公共用户身份确定请求者ID及有效绑定、目标列表正文、配置修改许可。资源风险可500并可附Retry-After；无绑定或过期以404/141停止；无resource-lists正文以403/244停止；无配置请求许可以403/246停止。通过后先发送200，再逐目标处理。缺TriggerId时，为同一criterion在各目标分配相同值，各不同criterion用不同值。本地目标未授权向请求者分享位置时静默停止该目标；授权成功才调用§17.2.2下发配置。

**规范强度：** 请求构造、明确拒绝、200与逐目标处理为SHALL；客户端P-Preferred-Identity、资源500及Retry-After分别为MAY。

- 246是配置更改许可，§17.2.3.2的245是位置查询许可，不能互换。配置许可和逐目标分享许可如何判定均未在这里给出算法。
- 200在逐目标许可和下发之前，不能证明所有目标同意、已接收或已应用，也不能证明取得位置；该段没有给出批量回滚或逐目标完成回执算法。
- 本地§17.2.2A step7c字面检查位置分享许可；跨PF §17.2.2B step4i写替换/修改配置许可。本页不将两者统一，也不展开跨PF分支。

**依据：**
- [TS24.282 V19.7.0 §17.3.2.2;17.2.2A](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 409,410,416；规范依据。
- [TS24.282 V19.7.0 §17.2.3.2 step5](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 411,412；comparison-only：245查询许可。
- [TS24.282 V19.7.0 §17.2.2B step4](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 410,411；comparison-only：跨PF授权措辞，不扩展本页路径。

## 目标收到配置后按Full或Update存储，删除不能靠省略

**条件：** PF下发分支以§17.2.2A本地目标分享许可通过后调用§17.2.2为条件；接收客户端分支独立以实际收到MESSAGE且Accept-Contact含MCData ICSI、Content-Type为application/vnd.3gpp.mcdata-location-info+xml、对应正文location-info内含Configuration为入口。

PF将Request-URI设为服务授权中对应目标MCData ID的公共用户身份，info正文mcdata-request-uri标识目标，location正文携所需Configuration。出站Accept-Contact带MCData ICSI及require/explicit，PAI为PF公共服务身份，P-Asserted-Service为MCData ICSI；可在mcdata-calling-user-id中带配置请求者。触发项已有且有效的TriggerId保留，否则在定义该属性的位置生成唯一值。PF发送并为该客户端存储配置。接收端按ConfigScope替换或修改已存内容、存储配置、据此设置触发并启动minimumReportInterval。D.4规定Full替换先前配置，Update是在先前配置上追加；删除配置元素需要Full，不能把Update中省略旧元素解释为删除。

**规范强度：** 在本页实际调用条件下，下发必需构造、发送/存储与接收处理为SHALL；附带mcdata-calling-user-id为MAY。§17.2.2一般配置能力的MAY不取消调用后的步骤义务。

- ConfigScope的schema枚举为Full/Update，没有声明默认值；不能把缺失自动当Full或Update。只需存储最新配置的NOTE不取消Update追加语义。
- §17.2.5另规定正文剥离：PAI公共身份不关联本PF服务用户，或请求含mcdata-info正文且mcdata-request-URI指向本PF服务用户；在此OR条件下，还须同时含g.3gpp.mcdata的Accept-Contact、MCData ICSI的Accept-Contact，以及含Request或Configuration的位置正文，PF发送请求时移除位置正文。第二OR原文没有not，本页不补否定，也不泛化为所有本地配置都被剥离。
- §17.2.2的目标字段写mcdata-request-uri，§17.2.5写mcdata-request-URI；此处保留大小写差异，不输出自行修复的可执行XML。PF存储或发送不等于目标已应用。服务授权的公共身份与请求者身份、PF公共服务身份各有用途。

**依据：**
- [TS24.282 V19.7.0 §17.2.2;17.2.2A step7c;17.3.2.1](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 408,409,410,415,416；规范依据。
- [TS24.282 V19.7.0 §D.4.2 tConfigurationType;D.4.3 Configuration/ConfigScope](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 596,604；字段取值、缺省边界与替换/追加语义。
- [TS24.282 V19.7.0 §17.2.5](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 415；完整异常守卫与正文剥离，保留字面差异。

## 周期与配置收到触发可选，删周期项不等于全局停报

**条件：** 配置字段按实际存在的块解释：NonEmergencyLocationInformation与EmergencyLocationInformation各自可选；TriggeringCriteria为非紧急触发配置。客户端接收、触发发生、timer到期及显式位置Request是不同事件，不要求一次同时发生。这里只展开PeriodicReport和LocationConfigurationReceived及其共用报告入口，不展开紧急、地理围栏或自适应算法。

D.4的两个LocationInformation块若存在，其minimumIntervalLength为必需的正整数，语义单位为秒、约束报告间最短等待时间。PeriodicReport是可选的秒间隔触发项，并需唯一TriggerId；McdataSignallingEvent中的LocationConfigurationReceived也是可选触发项，需唯一TriggerId。配置收到本身先导致存储、设置触发和启动timer，不是无条件立即报告。§17.3.4.1在触发发生时检查minimumReportInterval是否运行，运行则等待；timer到期且任一触发仍真时才按§17.3.4.2报告。该条对实际收到显式位置Request另列报告入口，不以周期触发仍真为前提。删除周期配置需按Full语义处理，但不因此关闭其他触发或显式Request入口。

**规范强度：** 所述接收处理、到期仍真时报告及显式Request报告为SHALL；D.4的可选项是字段可选性，不是把存在时的必需TriggerId或触发义务降为MAY。

- PeriodicReport的schema内容是integer，不是布尔开关；LocationConfigurationReceived为带TriggerId的空内容类型，不是true/false字段。不能以显式false或周期0自行编码停报；缺失某项也不能忽略Update仍保留先前配置。ConfigScope和所核周期字段没有提供默认秒数。
- 流程使用minimumReportInterval timer/time，D.4字段名为minimumIntervalLength。本页分别说明最短间隔与timer守卫，不补缺块时默认值、两个状态块的选值算法或不存在的精确调度保证。
- §17.3.4.2区分借用其他原因发送的SIP请求与独立MESSAGE；独立报告回程取配置MESSAGE的PAI，而非直接用原配置请求者身份。报告发送还涉及触发标识、重置与许可，按需Request/Report的条件化说明见相关页；配置成功不能替代这些条件或证明位置新鲜。
- 相关helper §6.2.5.1 step1写application/vnd.3gpp.location-info+xml，§17.3.4.2及该helper自身配置引用使用application/vnd.3gpp.mcdata-location-info+xml；helper有需协调文本的编辑说明。本页保留差异，不把两段拼成已经验证的互操作算法。D.4 schema与语义也不在这里扩成完整可执行位置配置。

**依据：**
- [TS24.282 V19.7.0 §17.3.2.1;17.3.4.1–17.3.4.2](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 415,416,417,418；规范依据。
- [TS24.282 V19.7.0 §D.4.2 tConfigurationType/TriggeringCriteriaType/tEmptyTypeAttribute/tIntegerAttributeType/tSignallingEventType/tRequestedLocationType](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 596,597,598,601；实际字段类型、必需项与未声明默认值。
- [TS24.282 V19.7.0 §D.4.3 Configuration;NonEmergencyLocationInformation;EmergencyLocationInformation;TriggeringCriteria f,h](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 604,605,606,607；Full删除、秒单位与两种可选触发。
- [TS24.282 V19.7.0 §6.2.5.1 including editor note](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 61,62；依赖/比较：报告helper及MIME差异，不扩紧急算法。
- [TS24.282 V19.7.0 §17.3.3.1;17.2.4.1](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 414,416；comparison-only：显式Request及报告许可独立入口。

## 使用边界与关联

- 本页不提供全局停止位置报告命令、所有目标应用完成证明或经自行修复的XML。安全、基础SIP事务与外部配置策略仍是依赖。
- [本地按需位置请求](local-location-request.md)：仅在该页同PF、直接ID及各角色事件条件下，查看Request/Report关联、路由与新鲜度边界；不是配置收到后的无条件后续。
