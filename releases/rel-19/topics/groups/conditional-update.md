# XCAP 并发修改：ETag 与 412

适用：Rel19 TS24.481 V19.3.0 所引用的 XCAP 操作，依据 RFC4825 §7.11。RFC 本身没有 3GPP Release；这里不替代组文档授权或应用约束。

同一文档及其元素、属性资源共享 ETag。修改单个节点也可能因文档其他位置变化而发生版本冲突。

客户端希望仅在已知版本仍有效时修改，可在 PUT 中使用 If-Match。若文档版本已改变，服务器返回412；应失效旧缓存、重新取得完整文档和新 ETag，再据新版本重试。工程上还需核对原修改意图是否仍成立，不能把更新 ETag 当成冲突已自动合并。

带 If-Match 的条件 DELETE 也适用。节点删除成功后返回的 ETag 对应仍存在的文档及其他资源，不意味着被删节点仍存在。

GET 的 If-None-Match 则用于缓存验证：版本相同返回304，不同才返回200及内容。不要把读缓存验证与写入前置条件混为一谈。

[操作目标与方法](resource-operations.md) · [组文档权限](document-access.md) · [RFC4825 §7.11](https://www.rfc-editor.org/rfc/rfc4825.html#section-7.11)

本页不提供跨文档事务、自动合并或所有HTTP状态码处理。412与[建组409](creation.md)含义不同。
