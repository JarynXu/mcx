# 未知XML扩展：忽略元素不等于删除授权条件

TS24.481 V19.3.0，区分普通组文档、GKTP文档与GMOP。

## 组文档先看must-understand和所在位置

适用条件：元素未在§7.2.2定义。

must-understand=true时忽略整个文档。否则，不在conditions后代中的未知元素被忽略；conditions后代则按RFC4745的未知元素规则求值，不能直接删掉再按无条件处理。未定义属性除must-understand外忽略。

依据：§7.2.8。

## GKTP和GMOP并非同一扩展规则

适用条件：处理GKTP或GMOP中的未知内容。

GKTP未知元素带must-understand=true时忽略整个文档，否则忽略元素；未知属性除must-understand外忽略。GMOP则规定忽略未知元素和属性。不要把GMOP的简化规则用于组文档授权条件。

依据：§7.7.8; 7.3.4.1。

## 证据边界

- 本页不定义忽略文档对应的HTTP/SIP错误码。
- RFC4745明确的是未知或不支持命名空间中的所列子元素；不能推广为任何名字未知、任意嵌套位置都使用相同求值规则。

## 按需继续

- [document-access](document-access.md)
- [gktp-access](gktp-access.md)
- [temporary-group-lifecycle](temporary-group-lifecycle.md)

[ETSI官方TS24.481 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)，印刷页48、49、66、75；仅本版本。

## 被引用的RFC具体规定

RFC4745 §7、§7.1.1规定：conditions或identity的子元素使用未知或不支持命名空间时，该子元素为FALSE；identity子元素按OR组合，因此不能把局部FALSE写成整个identity必然FALSE。

依据：[RFC4745 §7](https://www.rfc-editor.org/rfc/rfc4745.html#section-7)、[§7.1.1](https://www.rfc-editor.org/rfc/rfc4745.html#section-7.1.1)。仅核这些规则，不代表整套策略求值已经实现或验证。
