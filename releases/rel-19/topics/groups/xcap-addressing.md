# XCAP 寻址：文档、节点与命名空间

适用于 TS24.481 V19.3.0 引用的 XCAP 操作。依据为 RFC4825，RFC 本身不属于 3GPP Release19。

文档地址由 XCAP root 与 document selector 组成。后者以 AUID 起始，再进入 `users/XUI/...` 或 `global/...`。root 本身不是可操作资源。节点地址则在文档地址后接 `/~~/` 与 node selector。[RFC4825 §6.1–6.3](https://www.rfc-editor.org/rfc/rfc4825.html#section-6)

node selector 只是受限选择语法，不是完整 XPath；中间步骤必须各选中一个元素，不能借多节点匹配实现批量修改。

URI 中的前缀由查询部分的 `xmlns()` 绑定解释。无前缀元素使用 application usage 的默认 document namespace；无前缀属性没有命名空间。不要直接沿用目标 XML 的前缀声明来解释 URI。[§5.2、§6.3–6.4](https://www.rfc-editor.org/rfc/rfc4825.html#section-6.4)

## 使用边界

这里解释通用 XCAP 规则，不提供完整 MCX 请求模板；应用 schema、具体文档 MIME 和授权仍须按对应应用核对。创建目标不匹配不表示能自动创建缺失祖先。

按问题继续：[操作层级](resource-operations.md)、[并发与 ETag](conditional-update.md)、[MCX 建组](creation.md)。

[结构化知识](./xcap-addressing.json) · [来源目录](../../sources.json)
