# Agent 使用说明

1. 从 [catalog.json](catalog.json) 选择问题所需 Release；版本不明确且会影响结论时先澄清。
2. 若该 Release 提供 domains.json，先选业务域并读其 index，根据问题定位正文；没有该入口时读 topics.json。全量 topics.json 保留供跨域检索，不要求每次加载。通常只读命中主题。跨角色或跨步骤时，可从 reading-paths.json 选择要了解的问题；查规范不需要先有抓包。
3. 需要结构化条件、关系及条款时，读取该主题的 knowledge_record；需要核验来源身份时读取 sources.json 对应记录。

claim 若带自己的 source_id，用该条指定的来源核对条款；否则使用主题的 source_id。claim 若列出 source_references，按每项的 source_id、clauses 和 printed_pages 分别追溯；不要把主来源的版本和页码套到其他来源。多来源引用不等于跨版本互通已经验证。外部 RFC 作为依赖引用，不因此变成 3GPP Release 规范。

每条 claim 继承主题的全部 common_conditions，再叠加自身 conditions。不要孤立摘取 claim，或把可选关联当作必做流程。

先看 standard_stage：Stage 1 要求、Stage 2 流程与 Stage 3 协议不能互相替代。

回答保留标准编号、版本、条款及影响结论的条件。原文复核尚未完成时如实说明，不把公开可读理解为完整验收。

索引未命中或询问完整流程时，查本版覆盖说明。区分本库没收录、某个规范分支不适用，以及现有证据不足以判断某次通信；不从其他 Release 静默补齐。编写规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。
