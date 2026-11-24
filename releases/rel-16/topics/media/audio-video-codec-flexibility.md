# MCPTT 和 MCVideo 必须使用固定的编解码器吗？MCData 也适用吗？

对 MCPTT 和 MCVideo，[R-5.13-001，印刷页 26](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=27) 要求业务能灵活使用不同的音频或视频编解码器。一次通话只选用一种编码，不与这项能力矛盾。条文没有列出必选的编解码器，也没有要求每台终端都支持所有音视频格式。

3GPP TS 22.280 V16.8.0（Release 16，Stage 1）[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)涵盖在网和离网。[表 A.1（MCPTT，印刷页 64）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=65)、[表 B.1（MCVideo，印刷页 75）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=76)都列出 R-5.13-001；[表 C.1（MCData，印刷页 86）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=87)把 §5.13 整行标为 NA。不能用这一条要求 MCData 支持多种编解码器，也不能据此禁止 MCData 处理含音视频的数据。

如果问「G 组首选哪个编码」，应查[在网组的管理员设置](../groups/onnetwork-administrative-group-settings.md)。如果手里是一份 MCPTT 组呼的 SDP，要判断其中的语音编码名为何出现，应查[组呼 SDP 的首选语音编码](../calls/group-speech-codec-preference.md)。§5.13 不指定怎样协商、何时转码，也没有给出码率或音画质量门限。
