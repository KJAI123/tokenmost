# tokenmost 后端（v0.9）——折扣码众包托管

单文件 FastAPI + SQLite，密码/token 用标准库加密（pbkdf2 + HMAC），**零额外依赖**（requirements 只装 fastapi/uvicorn/pydantic）。

## 起服务

```bash
cd server/
pip install -r requirements.txt
ZHIPU_API_KEY=你的bigmodelkey ADMIN_TOKEN=自定管理口令 uvicorn app:app --port 8001
# 不配 ZHIPU_API_KEY：提交全部转人工（pending），功能不受影响
```

## 接口

| 方法/路径 | 说明 |
|---|---|
| POST /api/auth/register / login | 手机号+密码（HMAC token，30 天） |
| POST /api/coupons | 提交托管码（需登录）。**GLM-4.7-Flash（免费档）自动初审**：通过→直接上架；拒→rejected；无 KEY→pending 人工 |
| GET /api/coupons/public?provider=平台名 | 该平台已上架共享码（卡片小窗数据源） |
| POST /api/coupons/{id}/copy | 复制计数：同人同日去重；**达到 max_copies 自动下架** |
| GET /api/my/coupons | 我的码 + 被复制次数 |
| DELETE /api/coupons/{id} | 提交者主动下架 |
| POST /api/admin/coupons/{id}?action=active\|rejected | 管理员终审（Header: x-admin-token） |

## 合规与防刷

- Flash 初审提示词 + 代码级黑名单（多号/批量/代充/共享/接码/漏洞等）双重把关
- 复制计数按 用户ID 或 IP哈希 同日去重，防刷新计数
- 上限由提交者设定（1-10000），达限自动下架并记录原因
- 上线前必改：`TM_SECRET`、`ADMIN_TOKEN`；CORS 收紧为站点域名
