# 媒体面文件分发：自动接收判定与终端下载决定

## 适用范围

- 固定TS24.282 V19.7.0，普通在网、本地、单播的one-to-one媒体FD或普通非重组group standalone媒体FD。每项使用所列角色实际收到的事件；不预设前一角色已成功。
- 不含HTTP、SDS、紧急/迫近危险、别名、预建立会话和跨系统；终端不处于本文所排除的优先业务分支，入站不请求emergency/alert/imminentperil；终端接受说明限定未收到关联CANCEL。
- CF的缺IE条件不施加到所有终端claim：终端可以收到已经带MANDATORY DOWNLOAD的邀请。前序准入和资源/安全拒绝仍有效；本页不是完整建会、媒体传输或唯一响应仲裁算法。

## CF依据媒体请求决定是否补强制下载指示

适用主体：CF。

适用条件：已按媒体FD准入到达§10.2.5.4.3邀请过程；入站FD SIGNALLING PAYLOAD未包含Mandatory download IE。

4.3 step9A调用§11.2。媒体分支在请求含metadata时，从SDP的m=message媒体段fileselector属性取得filesize；私聊比较max-data-size-auto-recv-bytes，普通组比较mcdata-on-network-max-data-size-auto-recv，均为小于或等于。metadata取值条件成立且对应阈值条件满足时，CF判定需要加入指示，由caller在出站FD SIGNALLING PAYLOAD加入MANDATORY DOWNLOAD。

- §11.2媒体step4把条件1和条件2或3组合，但没有括号；本结论只覆盖metadata存在且对应业务阈值满足这一确定交集，不将缺metadata的组分支推为确定结果。
- 媒体分支没有HTTP上半所写的无metadata时按URL取得大小步骤，也没有另给缺失metadata或配置数值的默认算法。不能复制HTTP回退。
- 已含Mandatory download IE时不满足step9A条件，不据此删除、覆盖或再次判定该IE；自动接收阈值也不是§11.1发送许可上限。

规范强度：shall，明确可选行为为may；边界说明不新增协议规则。

依据：TS24.282 V19.7.0 §10.2.5.4.3 step9A；§10.2.5.4.4 steps8b(ii),9j (callers)；§11.2 media-plane branch；§11.2 HTTP branch (comparison only)；§11.1 steps4,6 (comparison only)，印刷页 304, 307, 308, 312, 311。

## 强制下载指示不越过终端资源和安全检查

适用主体：终接客户端。

适用条件：实际收到§6.2.1.2分类的媒体FD INVITE；分别执行前置检查以及到达step6后的接受条件；未收到关联CANCEL。

终端仍可因资源不足或规范外原因拒绝；已拒绝时发送相应拒绝响应并停止，获准限制失败原因时可用无Warning的480。存在MIKEY-SAKKE I_MESSAGE且认证失败时，必须488/Warning136并停止。通过前序后，Mandatory download IE为MANDATORY DOWNLOAD或用户已接受，step6要求接受INVITE并生成200，含FD Contact标签、Require:timer、Session-Expires/refresher=uas及按10.2.5.2.2生成的answer。无关联CANCEL才发送这个200。

- 客户端分类依FD Accept-Contact ICSI-ref、FD P-Asserted-Service与one-to-one-fd/group-fd；不能把任意带Mandatory IE的消息当本入口。
- 完整安全算法与SDP编码未展开。200是INVITE接受，不是文件下载完成。后续ACK的媒体调用及完成指示另见既有接收报告主题，并须满足其适用条件。
- 若有关联CANCEL，step6g另调用6.2.8.4.1；本页范围排除此分支，不把上面的200发送规则套到取消。

规范强度：shall，明确可选行为为may；边界说明不新增协议规则。

依据：TS24.282 V19.7.0 §6.2.1.2 FD client classification；§10.2.5.2.4 steps1–3,6，印刷页 56, 291, 292, 293。

## 无强制IE时的等待、拒绝与延期不能套HTTP计时流程

适用主体：终接客户端。

适用条件：媒体FD INVITE中FD SIGNALLING PAYLOAD没有Mandatory download IE；前置资源/安全检查未停止；未收到关联CANCEL。

step7要求通知用户并等待接受、拒绝或延期。其明确拒绝分支发送480/Warning110并停止；延期分支发送480/Warning231并停止；接受分支生成FD会话200，带timer、refresher=uas、FD Contact标签和answer，未收到关联CANCEL时发送，并可保存Conversation ID、Message ID、InReplyTo及时间。

- 同一过程step6的otherwise又对未接受/已拒绝写403，step7末尾也写403；因此这些文字存在重叠，本页只列条件化要求，不宣称已得到唯一响应优先级或完整确定状态机。
- Mandatory IE缺失才触发step7；“存在但值不是MANDATORY DOWNLOAD”不能直接归为这一缺失分支。
- 本媒体段没有写HTTP下载决策中的TDU2等待/延期规则，不从HTTP页移植计时器或自动超时结果。接受、拒绝、延期的SIP响应不等于HTTP FD的独立disposition通知；本页不推导PF收到延期后的暂存或后续下载。

规范强度：shall，明确可选行为为may；边界说明不新增协议规则。

依据：TS24.282 V19.7.0 §10.2.5.2.4 steps6 otherwise,7，印刷页 293, 294。

依据：TS24.282 V19.7.0 §10.2.1.2.3 steps3–8；§F.2.3 TDU2（仅HTTP对照），印刷页267、268、640。

## 按条件继续

- [私聊CF邀请与建会结果，仅one-to-one范围](media-fd-private-controller-setup.md)
- [文件发送大小许可，不是自动接收阈值](fd-size-admission.md)
- [实际文件接收、完成指示与ACK媒体调用差异](fd-media-reception-and-signalling-report.md)

[ETSI TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)。
