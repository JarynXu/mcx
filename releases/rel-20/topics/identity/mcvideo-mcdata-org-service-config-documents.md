# MCVideo、MCData 组织业务配置：文档怎么命名，谁能改？

**先选业务，再选组织。**MCVideo 和 MCData 各有自己的业务配置文档；对每一种业务，每个任务关键组织一份，位于 CMSXCAPROOT 的 `global` 树下。它不是每个用户、终端或业务服务器各一份。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.2/.8/.9、§10.4.2.2/.8/.9。

| 业务 | 应用用法标识 AUID（§.2） | 文档名（§.8） |
| --- | --- | --- |
| MCVideo | `org.3gpp.mcvideo.service-config` | `mcvideo-service-config.xml` |
| MCData | `org.3gpp.mcdata.service-config` | `mcdata-service-config.xml` |

AUID 用来区分应用用法，不是文件名或组织名。同一个组织的 Video 和 Data 也不合成一份业务配置文档。

## root 代表一个组织还是多个组织？

§9.4.2.9、§10.4.2.9 说，**可用 CMSXCAPROOT 区分组织**；若共用根，可用 `global` 下以任务关键组织名称命名的子目录来区分。下面是原文的四个 URI 示例，先核现场哪个根和组织名对应这笔请求，不靠示例猜部署。

| 业务 | 根对应一个组织 | 根服务多个组织 |
| --- | --- | --- |
| MCVideo | `mc-org-domain/mcorg12345/org.3gpp.mcvideo.service-config/global/mcvideo-service-config.xml` | `CMSXCAPROOTURI/org.3gpp.mcvideo.service-config/global/mc-org-name/mcvideo-service-config.xml` |
| MCData | `mc-org-domain/mcorg12345/org.3gpp.mcdata.service-config/global/mcdata-service-config.xml` | `CMSXCAPROOTURI/org.3gpp.mcdata.service-config/global/mc-org-name/mcdata-service-config.xml` |

每组织一份说的是该业务的文档，不是只有一台服务器或一份运行副本。这两节不规定组织名的编码、根地址与服务器的部署关系、唯一 URI 模板或两端实际取到的版本。同一文件名也不能代替组织定位。

## 文档在 global 下，不代表这次请求有权限

§9.4.2.9 和 §10.4.2.9 都写**用户只读，读写只允许该任务关键组织的系统管理员**。不能把别的组织的管理员、UE 用户或只被称为业务管理员的人自动当作这个组织的系统管理员。`global` 是文档所在的树，不是公开给任何访问者或允许写入的意思。角色和资源的规则也不证明这笔请求已获准、成功写入或被端侧采用。授权策略另见 §9.4.2.11、§10.4.2.11（指向 OMA XDM Core §5.1.5），这里不核目标正文或填凭据、响应码与操作程序。

问 UE 与业务服务器取哪些文档，转[两种接收角色的配置格式](mcvideo-mcdata-ue-server-config-formats.md)；问服务器怎样订阅、收到通知和取文，转[服务器取用组织配置](mcs-server-service-config.md)，其中 MCPTT 的例子保留在该页。问业务管理员能用哪种 UE 配置哪类文档，转[管理员配置范围](mcvideo-mcdata-admin-configuration.md)，不要把它当成这里的系统管理员身份判定。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-mcdata-org-service-config-documents.json)
