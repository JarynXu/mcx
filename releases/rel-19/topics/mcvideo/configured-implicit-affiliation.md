# 配置隐式归属：空配置、无新增、N2及owner结果

TS24.281 V19.3.0在网MCVideo的serving/PF隐式归属helper与配置入口。每条claim独立继承本主题common_conditions和自己的conditions，不继承前条成功；所需serving用户/client记录及已有service authorization按各入口成立。

本页不展开跨系统迁移/gateway、NCF、重组、功能别名/地理规则、第三方强制或协商归属、完整紧急/迫近危险状态机、GMS/IMS/RFC事务或媒体控制实现。业务触发类型可按第8章概览辨认，具体已闭合普通业务链接到既有on-demand有TC chat页，不把概览当全部优先业务实现。

service authorization、显式PUBLISH兴趣集合、业务请求隐式候选、profile配置归属和媒体implicit transmission request是不同入口。不用MCData/MCPTT或其它版本补省略项。

## 授权和profile配置入口

适用条件：服务授权PUBLISH按7.3.3成功，或settings-only PUBLISH按7.3.4通过保护、现有未过期绑定及RFC处理；server进入200后的active-profile处理，或其他已授权调用进入8.2.2.2.15。

7.3.3与7.3.4在选定/取得active profile后，若OnNetwork/ImplicitAffiliations含至少一个携带MCVideo group ID的entry，则须调用8.2.2.2.15。helper以已成功service authorization为入口，识别served用户和请求mcvideo-client-id，未缓存profile则下载。helper内若ImplicitAffiliations缺失或其中没有携带组ID的entry，就跳过余下步骤；这不是把现有归属清空。

- 两个PUBLISH主条的200已先发送，不证明后续配置归属成功；具体注册/绑定/设置寿命见既有第7章主题，不重复实现。
- 8.2.2.2.15用“received for service authorisation”标识请求/身份，而7.3.4 settings-only也明确调用它；保留调用与helper措辞差别，不虚构本次settings-only必须重新带access token或重新认证。
- 缺配置/无entry是helper内部保护出口；不改写为主条在缺配置时也必须调用helper。没有证据表明删掉该配置就自动对已有组去归属。

依据：§7.3.3 steps9–13;7.3.4 steps9–13;8.2.2.2.15 steps1–4，印刷页 161、162、163、194。

## 保留旧组与无新增提前退出

适用条件：8.2.2.2.15已通过非空配置条件并定位served用户/client；其既有组记录列表可读取。

PF复制该client全部旧组记录。对profile中每个组，仅当原列表无此组或原条目已过期时加入new entry，状态affiliating，期限current time+candidate expiration interval。若此步没有加入任何new entry，须丢弃candidate并跳过剩余步骤，因此不会在这次调用继续N2缩减、存储替换或owner转交。既有但从profile移除的组在复制步骤仍被保留，本流程不是显式PUBLISH式的完整兴趣集合替换。

- 无新项出口不等于所有配置组都已成功归属：未过期affiliating、deaffiliating或deaffiliated条目也不满足此new条件。不得把调用成功/返回等同配置全部生效。
- candidate expiration interval仍未在helper定义；先复制再新增过期同组条目的歧义与业务helper相同，不擅自修成替换。只说本步骤保留旧组，不排除随后N2策略改变最终candidate。

依据：§8.2.2.2.15 steps5–8，印刷页 194、195。

## 配置N2与业务单目标规则不同

适用条件：8.2.2.2.15 step8确实新增了至少一个组，未走无新项出口，进入step9。

PF按同用户各client的不同group ID计数，纳入当前candidate及其他client中affiliating/affiliated且未过期条目；超过profile Common/MaxAffiliationsN2时，按服务商策略将candidate组缩减至N2。随后step10用candidate替换本client的stored list。本配置helper没有.12那条“特定业务目标因N2不能加入则丢弃candidate”的单目标失败段，也没有自行返回486/102的步骤。

- 这不是承诺每个配置组都能加入，也不说明策略必定优先新配置组。若N2缩减改变新增组集合，step8无新项检查并未在step9后再写一次，不自行补第二次保护出口。
- 用户各client的合并计数不等于在本步骤无条件修改其它client存储；策略落实、默认N2和并发配置变化未闭合。
- 486/102是具体业务调用者在相应失败条件下的响应，不能因为两个helper都用N2就搬到已经回200的service settings流程。

依据：§8.2.2.2.15 steps9–10;8.2.2.2.12 steps8–11，印刷页 193、195。

## 向owner转交与条件p-id

适用条件：8.2.2.2.15确实新增过组、完成必要N2处理并替换本client列表，进入step11。

对profile配置中仍在candidate且状态affiliating的每个group ID，PF调用8.2.2.2.6向owner发送该served用户的归属请求；step11并非只筛选“本次新增”条目。此时8.2.2.2.6生成current p-id，对同用户该组未过期、affiliating且affiliating p-id未设置的记录赋此值，owner PUBLISH的presence使用该current p-id。配置helper的new-entry步骤本身只列状态/期限，没有从client显式presence拷贝p-id。

- 若step8根本无新项，先前出口已阻止来到step11；不能单凭存在旧affiliating条目就声称每次settings PUBLISH都会再次转交。
- 已设置的affiliating p-id不会被.6的“not set”条件覆盖；不能保证所有旧/新条目的p-id自动统一。profile触发与client显式PUBLISH的两层p-id差别只按实际赋值步骤描述。
- owner PUBLISH字段、全部live client列表、路由发现与失败清理复用已核显式归属serving主题中的公共helper，但此处有独立配置入口，不把该主题的显式client commons机械套入。

依据：§8.2.2.2.15 step11;8.2.2.2.6 steps7–10，印刷页 185、186、195。

## 结果沿owner状态观察判断

适用条件：配置过程已按8.2.2.2.15调用.6并发出owner PUBLISH；若需要获知实际owner结果，使用.7的owner状态确定及client .1.3状态观察入口。

配置流程在step11调用的是owner PUBLISH helper，不是业务候选helper .12；本入口未调用.13，不以service PUBLISH的200宣告这些组完成。向owner的PUBLISH若F到期或收到3xx/4xx/5xx/6xx，适用.6本用户各client同组记录的清理，而非.14只删业务新增条目。若通过owner状态观察收到符合.7条件的NOTIFY，则按该过程更新本地pending状态；client可依8.2.1.3订阅获知成功归属的组。

- .15没有明确在step11前自动建立owner订阅或保证client已经订阅；不补完整触发编排。NOTE2是client can subscribe，不把显式client“要知道本次变更结果则先订阅”的入口原封不动变成配置调用的前置。
- .7正向确认只对匹配user/client且本地未过期affiliating记录，NOTIFY需有expires；负向pending还依赖匹配p-id。这些详细条件及半寿命/续期缺口见owner-confirmation主题，不缩写为任意NOTIFY均成功。
- owner必须另过其组存在/成员与PIDF检查；profile列出组不豁免这些条件，也不等于组呼建立、conference加入或媒体发送许可。

依据：§8.2.2.2.15 step11 and NOTE2;8.2.2.2.6 response handling;8.2.2.2.7;8.2.2.2.13，印刷页 186、187、188、193、195。

## 证据边界

- 限第7章已授权/有效绑定入口与第8章配置helper。空配置不是显式清空请求，无新增不是全部成功；外部profile模型与默认未核。

## 按需继续

- [service-authorization](service-authorization.md)
- [service-settings-validity](service-settings-validity.md)
- [implicit-affiliation-lifecycle](implicit-affiliation-lifecycle.md)
- [explicit-affiliation-owner-confirmation](explicit-affiliation-owner-confirmation.md)
- [explicit-affiliation-request](explicit-affiliation-request.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

## 原文差异与未闭合依赖

- 8.1的service authorization/settings PUBLISH引用7.3.2，与实际7.3.3/7.3.4调用位置不同。8.2.2.2.15以已完成service authorisation及该request标识输入，7.3.4 settings-only仍显式调用；不改源。
- 8.2.2.2.11 step1存储引用9.2.2.2.2，且查user记录后失败项写group entry；PF该helper未列owner6.3.6的expiry检查。
- .12/.15都先复制旧列表，再对缺失或已过期组加入new entry；candidate expiration interval来源和旧过期同组记录移除未明写，不推唯一键实现。
- 未过期deaffiliating/deaffiliated条目不满足.12/.15新建条件，业务completion/cancellation以added entry为对象；不填状态转换缺口。
- owner .6/.7公共helper的错引、两层p-id保留、selected expiration/续期缺口沿用显式稿已核边界，不从配置入口静默修复。
