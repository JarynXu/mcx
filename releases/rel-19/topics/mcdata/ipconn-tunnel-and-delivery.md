# IPCONN媒体路径：隧道建立、逐跳中继与IP交付

## 适用范围

- 普通在网、两个MCData客户端之间的直接IPCONN；目标已确定且相应信令准入未拒绝。排除组、离网、功能别名、跨域、预建立复用、SDS/FD和紧急扩展。
- 媒体结论固定TS24.582 V19.0.0，信令结论固定TS24.282 V19.7.0，每条分别标明来源；同属Rel19不证明该版本组合完整互通。
- 每条独立继承共同条件并叠加自身角色、状态和触发条件；SIP响应、媒体建立、实际IP数据到达、应用处理结果和逐段资源释放分别判断。
- 未读取RFC8086、2784、791、8200及完整SIP/RFC状态机，不补隧道探测、超时、重传、安全或应用确认算法。

## 建隧道与交付IP应用

适用条件：发起客户端收到用户请求或IP应用数据并经20.2.1处理；终接客户端成功完成20.2.2；发送/接收数据分支以IP隧道已经建立为条件。

媒体§13.1.2要求发起端按20.2.1处理，并以200 SDP中的IP地址/端口建立GRE-in-UDP隧道；§13.1.3将终接信令过程成功作为开始建隧道的触发。隧道建立后，发起端向answer地址/端口、终接端向offer地址/端口发送封装UDP；收到隧道数据时，客户端须先去掉UDP/GRE封装再交IP应用。信令20.2.1的2xx后是ACK、Session timer、媒体调用，终接20.2.2则收到ACK才调用媒体；两端调用点不能当作已经交换数据或应用完成的证明。

- IP应用可在UE内或外部非3GPP主机；该接口为实现相关。未推导外部主机自动路由、探测成功或应用应答。
- 这补充已发布200/ACK入口的媒体含义，不另造信令准入结论。

依据：3GPP TS 24.582 V19.0.0 §13.1.1–3，印刷页 54、55。

依据：3GPP TS24.282 V19.7.0 §20.2.1 2xx;20.2.2 ACK，印刷页 445、447。

## 中继以实际媒体路径为条件

适用条件：分别对O-PF、T-PF或CF判断：该功能实际处于客户端间的数据交换路径中。

仅在此条件下，该功能须提供面向两个相邻方向的UDP端点，按SDP offer/answer交换的IP和端口中继UDP流量。O-PF一端面向主叫，T-PF一端面向被叫，CF两端面向两个方向的下一跳。不能从信令路经某服务器推导媒体必经它，也不能把relay解释为终端应用已经处理数据。

- 此处未写服务器终止并重新创建应用层事务，也未给旁路选择算法。两侧端点/地址按实际SDP，不把目标MCData ID当IP地址。

依据：3GPP TS 24.582 V19.0.0 §13.2.1–2;13.3，印刷页 55。

## 封装条件不是MSRP响应

适用条件：IPCONN客户端执行13.4的GRE-in-UDP封装；以该条对RFC8086的澄清为限。

IPv4和IPv6封装都须使用UDP checksum，不能使用GRE keys；UDP端口可自由选择并通过SDP交换。该媒体不是SDS的MSRP SEND/200链，不能用SDS最后一个MSRP200来判断IPCONN应用成功或自动结束隧道。

- 未读取RFC8086/2784，故不提供完整包格式、分片、MTU、拥塞处理或安全配置。checksum不是应用确认或保密保证。

依据：3GPP TS 24.582 V19.0.0 §4.1.4;13.4，印刷页 11、55、56。

## 源端口语义与原文字面差异

适用条件：客户端/服务器协商GRE-in-UDP媒体的SDP offer/answer，关注13.5–13.6的媒体描述和源端口参数。

表13.5.2.1-1规定媒体为application、端口为UDP端口、协议为udp、格式为MCDATA。13.6.2.2将mcdata-ipconn-sport解释为隧道UDP源端口；但13.6.2.3的attr-param使用mcdata-ipconn-s-port，而下一产生式命名又写mcdata-ipconn-sport，字符串写mcdata-ipconn-s-port。示例还只给mcdata-ipconn。因此只能分别报告语义和原文字面，不能宣布已有无歧义可复制的fmtp编码。

- 20032只是示例，不是固定或默认端口；不静默统一sport/s-port或补正ABNF引号。
- 应与现有ipconn-media-and-success-evidence的未核fmtp边界关联；单纯补此来源不解决24.282 CF answer对offer/answer的另一措辞冲突。

依据：3GPP TS 24.582 V19.0.0 §13.5.2.1;13.6.2.1–3，印刷页 56、57。

## 证据边界

- GRE-in-UDP完整RFC处理不在已核范围内，不提供可运行封装器。

## 按需继续

- [IP Connectivity 的媒体协商、应用信息和失败证据](ipconn-media-and-success-evidence.md)
- [IP Connectivity 的服务器路径与分段响应](ipconn-server-path.md)
- [MCData 会话的服务器释放：无预告 BYE、原因与参与者范围](session-server-release.md)
- [SDS 媒体面收尾：结果 BYE 与逐段释放](sds-media-result-and-release.md)

[3GPP TS 24.582 V19.0.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)；仅所列版本和条款。

[3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅所列版本和条款。
