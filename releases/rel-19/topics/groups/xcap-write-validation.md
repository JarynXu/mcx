# XCAP 写入：替换范围与 409 校验

适用于 TS24.481 V19.3.0 引用的 XCAP 操作。依据为 RFC4825，RFC 本身不属于 3GPP Release19。

整文档 PUT 是创建或完整替换，使用 application usage 规定的 MIME；元素 PUT 提交完整元素，使用 `application/xcap-el+xml`；属性 PUT 使用 `application/xcap-att+xml`，正文按 XML AttValue 格式，不能套用 URI 百分号编码。[RFC4825 §7.1、§7.4、§7.7](https://www.rfc-editor.org/rfc/rfc4825.html#section-7.1)

创建时 selector 当前不匹配，但写入后必须选中新对象；替换时须同时匹配旧、新对象。用旧属性值定位元素、又修改该属性，可能收到 409。[§7.4、§7.7](https://www.rfc-editor.org/rfc/rfc4825.html#section-7.7)

删除后 selector 若会改为选中另一元素，服务器必须拒绝删除并返回 409。位置选择尤其要注意。[§7.5、§8.4](https://www.rfc-editor.org/rfc/rfc4825.html#section-8.4)

409 还可能由 schema、唯一性或其他应用约束引起，不能统一当作组 ID 冲突重试。[§8.2.5](https://www.rfc-editor.org/rfc/rfc4825.html#section-8.2.5)

## 使用边界

这里解释通用 XCAP 规则，不提供完整 MCX 请求模板；应用 schema、具体文档 MIME 和授权仍须按对应应用核对。创建目标不匹配不表示能自动创建缺失祖先。

按问题继续：[操作层级](resource-operations.md)、[并发与 ETag](conditional-update.md)、[MCX 建组](creation.md)。

[结构化知识](./xcap-write-validation.json) · [来源目录](../../sources.json)
