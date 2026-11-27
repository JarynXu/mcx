# MCVideo、MCData 业务配置：哪些校验会报 409？

先分清报错对象：XCAP 请求目标里的 AUID、XUI，还是业务配置文档里的组织域名、参数块、重复项或 MCData 文件可用时间。只看到 HTTP 409，不能分辨触发了哪项。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3），MCVideo §9.4.2.6、MCData §10.4.2.6。AUID 见各自 §.2，Schema 见 §.3，组织域见 §.7；MCData 文件可用时间见 §10.4.2.7 在网项 5、6。

## 请求 URI 的应用用法和 XUI，比的是两个条件

先确认正在查 MCVideo 还是 MCData 业务配置，不凭可能填错的 AUID 来选业务。两节都检查 `Request-URI` 中的文档 URI 或节点 URI：

| 检查项 | 何时命中 | 带 `phrase` 时建议写 |
| --- | --- | --- |
| AUID（应用用法标识） | URI 中的 AUID 不等于该业务 §.2 的值。MCVideo 是 `org.3gpp.mcvideo.service-config`；MCData 是 `org.3gpp.mcdata.service-config` | `invalid application id used` |
| XUI | URI 中的 XUI 值与这份业务配置文档 URI 的 XUI 值不匹配 | `invalid XUI` |

命中其中一条，配置管理服务器（CMS）须返回 HTTP 409（Conflict），含 XCAP `<constraint-failure>`。`phrase` 可以不带。XUI 这一条比较的是两处 URI 的对应值，不是整条 URI，也不是把请求里的 XUI 和 XML 正文、SIP 身份或 AUID 比较。§9.4.2.9、§10.4.2.9 的示例把业务配置文档放在 `global` 下；不能从是否有组织子目录、文件名或该示例推一个 XUI 值，也不按这几句裁定 URI 没有可确认 XUI 时应怎样比较。正确的 AUID 或 XUI 不代替另一项，也不等于获准。

## 组织域名：语法错误和未知是两项检查

查文档中 `<service-configuration-params>` 的 `domain` 属性。两处 §.7 说它存放任务关键组织的域名；不是从 `Request-URI` 的主机名取值，也不从 `global` 下的目录名补值。两份 Schema 都把这个属性声明为必填的 `xs:anyURI`。通过该类型检查不能代替 §.6 的域名检查。

| 已核到正文的 `domain` | CMS 必须返回 | 带 `phrase` 时建议写 |
| --- | --- | --- |
| 未包含语法正确的域名 | HTTP 409（Conflict），含 XCAP `<constraint-failure>` | `syntactically incorrect domain name` |
| 包含未知域名 | HTTP 409（Conflict），含 XCAP `<constraint-failure>` | `unknown domain name` |

语法正确的域名仍可能是未知的。两句未规定验证算法、如何判断域名已知、去哪里查或先查哪项；看见 DNS 失败不足以确认正文域名属于这条的未知情形。缺整个 `domain` 属性与看到属性值不合要求是不同证据，参照 Schema 的必填声明，不能先给缺属性指定上表某个 `phrase`。多项约束可同时不符，不能凭一个响应反推出唯一原因或其他检查已经通过。

## 少了参数块，还是配错了块的组合？

两类文档的根元素都是 `<service-configuration-info>`。在它下面找 `<service-configuration-params>`，再看参数块下的 `<common>`、`<on-network>`、`<off-network>`。

| 两节各自明写的失败条件 | CMS 必须返回 | 带 `phrase` 时建议写 |
| --- | --- | --- |
| 根下没有 `<service-configuration-params>`；或者参数块有了，三类业务范围元素都没有 | HTTP 409（Conflict），含 XCAP `<constraint-failure>` | `mandatory element is missing` |
| 三类业务范围元素的组合不符合下面七种之一 | HTTP 409（Conflict），含 XCAP `<constraint-failure>` | `semantic error` |

七种组合是：单独一类（三种），任意两类且各一个（三种），三类各一个（一种）。单独一个 `<off-network>` 或只放 `<on-network>` 和 `<off-network>` 各一个，都符合这项组合要求；重复同一种不符合。七种只数这三类具名元素，不等于可调换子元素顺序，也不排除 Schema 声明的扩展。

文档还须符合各自的 XML Schema。§9.4.2.3 和 §10.4.2.3 给参数块声明 `minOccurs="0"`，三个业务范围元素也声明 `minOccurs="0" maxOccurs="unbounded"`。不能只看这些声明就略过 §.6 对缺项和组合的检查；符合七种之一也不等于 Schema、其他业务约束或本次请求已经通过。

错误码和错误元素是要求，`phrase` 不必带；表中的字符串是在带它时的建议。空参数块也不符合七种组合，重复元素另见[未知项与重复项](#未知项与重复项)的拒绝规则，条款未在这些句子里规定重叠时先查哪项、报哪句建议。上面的 URI 标识和组织域名检查也会用同样的状态码与错误元素。只有 409、截取的 XML 或一个局部节点请求，不能据此认定整份文档到底少了什么。

## 未知项与重复项

§9.4.2.6、§10.4.2.6 各列两条。先分清已确认的是未知，还是重复：

| 文档中的情况 | 条款写的处理 |
| --- | --- |
| 未知的元素或属性 | 原文称业务配置服务器（service configuration server）忽略未知项。没有说要删掉它、写回文档，或接受整个请求 |
| CMS 收到重复的元素或属性 | 配置管理服务器须返回 HTTP 409（Conflict），含 XCAP `<constraint-failure>`；若带 `phrase`，建议 `duplicate attribute or element received` |

**忽略未知项不免除 Schema 校验。** 例如，两种文档的 §.3 都在根类型和参数类型中另有允许其他命名空间元素的 `xs:any` 和允许任意命名空间属性的 `xs:anyAttribute` 声明，均写 `processContents="lax"`。这是这些位置的 Schema 声明，不是说任意未知项都能通过。§.6 注 1 的文字写 `##any` 并分别提到 `mcvideo-info`、`mcdata-info`；不要用注中的写法替换这两个类型在 §.3 的声明。未知项也不能充当必需的参数块或三类业务范围元素。

**CMS 收到重复项时，不能用自动保留一份代替条款要求的响应。** 两句没定义怎样识别未知或重复，不能只看同名就定性。例如 §.3 中功能别名列表的 `<functional-alias-entry>` 声明可出现多次；不因此认为同一业务条目可重复。若确定重复的 `<common>` 等元素也让参数块不合七种，重复约束和组合约束分别命中。两节未规定同时不符时先报哪条或如何选 `phrase`，也不规定遇到重复的未知项时先忽略还是先查重复。这里保留两条原文的服务器称谓，不据此判它们是否同一个进程。

## MCData：默认可用时间和最长可用时间分开看

§10.4.2.7 在网项 5、6 把两个字段放在 `<file-availability>` 下：

| MCData 字段 | 字段的作用 | §10.4.2.6 对缺项的规定 |
| --- | --- | --- |
| `<default-file-availability>` | 始发客户端没有请求明确时长时，文件可供从服务器下载的默认时长 | CMS 须返回 HTTP 409，含 XCAP `<constraint-failure>`；若带 `phrase`，建议 `default file availability not provided` |
| `<max-file-availability>` | 文件可供下载的最长时长 | 省略时不施加文件可用时长上限；不免除默认字段要求，也不表示文件会永久保留 |

§10.4.2.6 对默认项缺失的句子没有另列触发条件。字段位置按 §10.4.2.3 的 Schema 和 §10.4.2.7 在网项 5、6。§10.4.2.1 在网项 1(e)、1(f) 则把两项列在 `<tx-and-rx-control>` 下；这里保留两处写法，不把综述当成另一条合规路径。单独一个离网块只符合上面的七种组合之一，不能据此宣布整份配置通过，也不把默认文件时长写成离网字段。MCVideo §9.4.2.6 没有这两条 MCData 文件规则。

文件名、AUID、组织地址与访问规则见[组织业务配置文档](mcvideo-mcdata-org-service-config-documents.md)。要区分整文档写入与节点更新，见[CMC 配置 PUT](cmc-config-document-put.md)。广播挂起字段的[具名时长校验](ad-hoc-broadcast-hang-time.md)另查，不能用上面的结构条款代替各字段的校验。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-mcdata-service-config-validation.json)
