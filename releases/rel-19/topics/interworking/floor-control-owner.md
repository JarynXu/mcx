# 话权仲裁：组归属与私呼主控

ETSI正式发布的TS23.283 V19.5.0，Release19，Stage2。

## 互通组话权控制

组归属MCPTT系统时由其服务器主控；组归属LMR系统时由IWF代表主控。MCPTT组的主系统由配置定义并通过组ID识别，不能按当前发言者所在地更换主控。 [§10.5.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 互通私呼采用话权控制

IWF或MCPTT服务器中的一方负责双方请求仲裁，非主控方必须不加过滤地转交其用户的全部话权请求。主控可按发起侧或其他方式分配；手动建立示例中的发起侧责任不能扩张为所有场景的唯一分配规则。 [§10.5.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 边界

仅核主控及转交职责，不规定主控选举、故障迁移或部署拓扑。

[private-manual](private-manual.md) · [floor-filtering](floor-filtering.md) · [floor-signals](floor-signals.md) · [结构化条件](floor-control-owner.json)
