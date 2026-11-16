# 组呼终接参与功能：模式入口与预建立会话选择

TS24.379 V19.4.0，普通非优先预安排组呼；终接参与功能收到面向自己的初始SIP INVITE。

排除emergency-ind=true、imminentperil-ind=true及任何Priv-Answer-Mode头；不覆盖远程监听、重组扩展。


§10.1.1.3.2的资源、isfocus、客户端服务设置及身份绑定检查未拒绝请求。

## 无 Answer-Mode 时的自动入口

适用条件：INVITE没有Answer-Mode头，且已收到被邀请客户端的Answer-Mode Indication=auto-answer。

执行§6.3.2.2.5.1自动接续及RFC5373相关过程。

依据：§10.1.1.3.2 step7。

## 无 Answer-Mode 时的手动入口

适用条件：INVITE没有Answer-Mode头，且已收到被邀请客户端的Answer-Mode Indication=manual-answer。

执行§6.3.2.2.6.1手动接续及RFC5373相关过程。

依据：§10.1.1.3.2 step8。

## 空闲与两个媒体段均须匹配

适用条件：已经确定自动或手动接续模式。

只有同时满足以下三项才选择对应预建立分支：被邀请客户端至少有一个尚未关联MCPTT呼叫的预建立会话；所提供语音流的media-level section与该现有预建立会话的语音段相同；所提供话权控制实体的media-level section与该预建立会话的话权段相同。不满足则选择对应按需分支；不是只要已注册或存在任意预建立会话即可。

依据：§6.3.2.2.5.1;6.3.2.2.6.1。

## 证据边界

- 完整SIP fork/多分支失败合并未由这些条款定义；24.229依赖未核。
- 未核24.380媒体实施，不能将响应等同全组建立或话权授予。
- 显式Answer-Mode入口选择不从10.1.1.3.2无头条件反推。
- 6.3.2.2.6.3以reINVITE调用初始INVITE生成条款，保留原交叉引用，不改写成新dialog。

## 按需继续

- [group-terminating-addressing](group-terminating-addressing.md)
- [group-terminating-responses](group-terminating-responses.md)
- [group-acknowledged-start](group-acknowledged-start.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页288、118、121；仅本版本。

- [客户端接收与应答](../groups/terminating-client-acceptance.md)
