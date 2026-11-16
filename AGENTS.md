# Agent 使用说明

1. 从 [catalog.json](catalog.json) 选择问题所需 Release；版本不明确且会影响结论时先澄清。
2. 读该 Release 的轻量主题索引，根据问题定位正文。通常只需读取命中主题；跨步骤问题可参考该 Release 的 reading-paths.json，按其中条件取下一页。
3. 需要结构化条件、关系及条款时，读取该主题的 knowledge_record；需要核验来源身份时读取 sources.json 对应记录。

claim 若带自己的 source_id，用该条指定的来源核对条款；否则使用主题的 source_id。claim 若列出 source_references，按每项的 source_id、clauses 和 printed_pages 分别追溯；不要把主来源的版本和页码套到其他来源。多来源引用不等于跨版本互通已经验证。外部 RFC 作为依赖引用，不因此变成 3GPP Release 规范。

每条 claim 继承主题的全部 common_conditions，再叠加自身 conditions。不要孤立摘取 claim，或把可选关联当作必做流程。

先看 standard_stage：Stage 1 要求、Stage 2 流程与 Stage 3 协议不能互相替代。

回答保留标准编号、版本、条款及影响结论的条件。原文复核尚未完成时如实说明，不把公开可读理解为完整验收。

索引未命中或询问完整流程时，读 Release README 的覆盖边界，再说明缺口。条件不满足时也说明缺口，不从另一个 Release 静默补齐。编写规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。
