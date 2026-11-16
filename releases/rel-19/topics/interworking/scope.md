# LMR 互通：IWF 的规范边界

适用：Release 19，TS 23.283 V19.5.0。

本规范覆盖 MC 与陆地移动无线电（LMR）系统互通，包括 MCPTT、MCCoRe 及 MCData 的 SDS 范围；不能由此推定所有 MCData 业务已被覆盖（§1，p11）。

规范定义 IWF 与 MC 系统之间的参考点及交互，不规定 IWF 自身的结构和功能实现。IWF 连同 LMR 在接口交互中视作对等互联 MC 系统，但这不是强制的部署模型（§1、§4，p11、13）。

“User homed in the IWF”指在 MC 系统中代表 LMR 用户的 MC service ID；不要把这个身份模型直接当成用户终端的物理驻留位置（§3.1，p12；后半句为建模提示）。

[来源](../../sources.json) · [结构化条件](scope.json)。本页解释范围与术语，不覆盖呼叫、媒体、安全或 SDS 流程。
