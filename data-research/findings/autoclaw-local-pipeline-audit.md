# 本机 AutoClaw 数据管线审计（2026-11-13，老板令「对一下管线看有没有可补充的」）

## 翻查范围
- ~/Library/Application Support/AutoClaw（空壳）/ AutoClaw-official（Electron 主目录 40 项）
- accounts/*/user-notifications.json、account-profile.json、runtime/*
- logs/zwork-main-*.log（7 天×1.5MB）、model-token-usage.log（171KB）
- Cache/LocalStorage、/Applications/AutoClaw2.app 包内 JS（dist/renderer/assets）

## 审计结论：无可直接补充的新羊毛信源
1. **活动通知机制存在但当前为空**：客户端有 promotion_config 营销配置加载器（每 ~2h 拉一次，日志多见 load_failed network），当前 inputNoticeCount=0——无活动通知内容；通知只存 seenKeys ID（443648/443675~677），正文不落盘
2. **通知拉取端点被混淆**：app JS 未暴露 promotion_config URL 明文；且需登录态调用——不用老板凭证代调（合规边界）
3. Cache/LocalStorage 无活动 JSON 缓存
4. model-token-usage.log 是老板私有用量明细（GLM-5.3-Flash，provider=zwork-managed），非情报
5. 官方公告出口已被现有盯防覆盖：autoclaw-blog（News 福利）+ autoclaw-blog-all（全分类）+ autoclaw-invite-guide（已挂 175 源）

## 交叉验证副产品（站内数据准确性佐证）
- AutoClaw 的模型调用走 zwork-managed 网关、模型=zai_glm-5.3-flash——与站内 deep-autoclaw-promos 条目「GLM-5.3-Flash」口径一致 ✓
- 老板账号为重度用户（单会话 102 请求、缓存命中率 93.2%、runtime 2.3.0→2.4.1）
