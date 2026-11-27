# MCVideo、MCData 业务配置：缺哪一项会报 409？

查完整的业务配置文档。MCVideo 和 MCData 都要求有参数块，块内至少有一类业务范围配置。MCData 还规定：缺文件的默认可用时间会报错，缺最长可用时间不会设置这个上限。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3），MCVideo §9.4.2.6、MCData §10.4.2.6；Schema 见两节各自的 §.3，MCData 文件可用时间的语义见 §10.4.2.7 在网项 5、6。

## 少了参数块，还是配错了块的组合？

两类文档的根元素都是 `<service-configuration-info>`。在它下面找 `<service-configuration-params>`，再看参数块下的 `<common>`、`<on-network>`、`<off-network>`。

| 两节各自明写的失败条件 | CMS 必须返回 | 带 `phrase` 时建议写 |
| --- | --- | --- |
| 根下没有 `<service-configuration-params>`；或者参数块有了，三类业务范围元素都没有 | HTTP 409（Conflict），含 XCAP `<constraint-failure>` | `mandatory element is missing` |
| 三类业务范围元素的组合不符合下面七种之一 | HTTP 409（Conflict），含 XCAP `<constraint-failure>` | `semantic error` |

七种组合是：单独一类（三种），任意两类且各一个（三种），三类各一个（一种）。单独一个 `<off-network>` 或只放 `<on-network>` 和 `<off-network>` 各一个，都符合这项组合要求；重复同一种不符合。七种只数这三类具名元素，不等于可调换子元素顺序，也不排除 Schema 声明的扩展。

文档还须符合各自的 XML Schema。§9.4.2.3 和 §10.4.2.3 给参数块声明 `minOccurs="0"`，三个业务范围元素也声明 `minOccurs="0" maxOccurs="unbounded"`。不能只看这些声明就略过 §.6 对缺项和组合的检查；符合七种之一也不等于 Schema、其他业务约束或本次请求已经通过。

错误码和错误元素是要求，`phrase` 不必带；表中的字符串是在带它时的建议。空参数块也不符合七种组合，重复元素另有同节的拒绝规则，条款未在这些句子里规定重叠时先查哪项、报哪句建议。另有 URI 标识等失败也可返回同一 409 和错误元素。只有 409、截取的 XML 或一个局部节点请求，不能据此认定整份文档到底少了什么。

## MCData：默认可用时间和最长可用时间分开看

§10.4.2.7 在网项 5、6 把两个字段放在 `<file-availability>` 下：

| MCData 字段 | 字段的作用 | §10.4.2.6 对缺项的规定 |
| --- | --- | --- |
| `<default-file-availability>` | 始发客户端没有请求明确时长时，文件可供从服务器下载的默认时长 | CMS 须返回 HTTP 409，含 XCAP `<constraint-failure>`；若带 `phrase`，建议 `default file availability not provided` |
| `<max-file-availability>` | 文件可供下载的最长时长 | 省略时不施加文件可用时长上限；不免除默认字段要求，也不表示文件会永久保留 |

§10.4.2.6 对默认项缺失的句子没有另列触发条件。字段位置按 §10.4.2.3 的 Schema 和 §10.4.2.7 在网项 5、6。§10.4.2.1 在网项 1(e)、1(f) 则把两项列在 `<tx-and-rx-control>` 下；这里保留两处写法，不把综述当成另一条合规路径。单独一个离网块只符合上面的七种组合之一，不能据此宣布整份配置通过，也不把默认文件时长写成离网字段。MCVideo §9.4.2.6 没有这两条 MCData 文件规则。

文件名、AUID、组织地址与访问规则见[组织业务配置文档](mcvideo-mcdata-org-service-config-documents.md)。要区分整文档写入与节点更新，见[CMC 配置 PUT](cmc-config-document-put.md)。广播挂起字段的[具名时长校验](ad-hoc-broadcast-hang-time.md)另查，不能用上面的结构条款代替各字段的校验。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-mcdata-service-config-validation.json)
