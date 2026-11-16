# Agent 使用说明

1. 从 [catalog.json](catalog.json) 选择问题所需 Release；版本不明确且会影响结论时先澄清。
2. 读该 Release 的轻量主题索引，根据问题定位正文。通常只需读取命中主题；跨步骤问题可参考该 Release 的 reading-paths.json，按其中条件取下一页。
3. 需要结构化条件、关系及条款时，读取该主题的 knowledge_record；需要核验来源身份时读取 sources.json 对应记录。

每条 claim 继承主题的全部 common_conditions，再叠加自身 conditions。不要孤立摘取 claim，或把可选关联当作必做流程。

先看 standard_stage：Stage 1 要求、Stage 2 流程与 Stage 3 协议不能互相替代。

回答保留标准编号、版本、条款及影响结论的条件。原文复核尚未完成时如实说明，不把公开可读理解为完整验收。

索引未命中或询问完整流程时，读 Release README 的覆盖边界，再说明缺口。条件不满足时也说明缺口，不从另一个 Release 静默补齐。编写规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。
