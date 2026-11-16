# 组话权本地过滤：通过预选不等于最终授予

ETSI正式发布的TS23.283 V19.5.0，Release19，Stage2。

## 组归属LMR；MC侧配置本地过滤；双方用户已归属，互通组呼进行中且话权空闲

示例先在MC侧选中客户端1并拒绝客户端2，再将选中的请求交IWF作最终决定；须待最终granted传回客户端1后才开始发送。 [§10.5.5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组归属MCPTT且已在GMS定义；LMR侧本地过滤；双方用户已归属，互通组呼进行中且话权空闲

多个LMR请求先依本地策略仲裁，只向MC侧呈现一个请求。MC服务器仍作最终仲裁；示例MC用户胜出并不构成MC用户永远优先的规则。 [§10.5.6](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在LMR，MC配置不本地过滤而转交竞争请求；双方用户已归属，互通组呼进行中且话权空闲

MC服务器把竞争请求都交IWF作最终决定，再把针对各用户的授予、拒绝和占用通知送回；不在MC侧先淘汰一个请求。 [§10.5.7](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在MCPTT，LMR侧配置转交全部竞争请求；双方用户已归属，互通组呼进行中且话权空闲

此过程还要求IWF不代理LMR用户归属，所有LMR组归属均透传给MC服务器；不能把它直接套到IWF代理归属模式。 [§10.5.8 preconditions](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 边界

只核指定空闲话权示例及前提；不把示例胜者或到达时间变成固定调度算法。

[floor-control-owner](floor-control-owner.md) · [affiliation-representation](affiliation-representation.md) · [floor-signals](floor-signals.md) · [结构化条件](floor-filtering.json)
