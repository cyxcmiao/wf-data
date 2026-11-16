# 裂罅行情镜像（免 VPN 方案）部署说明

App 的行情统计通道：直连 warframestat.us → **快照镜像（本方案，Gitee 优先）** → WebView 过 CF → 本地缓存。
建好下面的仓库后，国内无 VPN 用户即可拉到小时级行情快照。

架构：GitHub Actions（海外机房，Cloudflare 不拦）每 6 小时抓一次快照 → 提交 GitHub 仓库 → 同步推送 Gitee 同名仓库。App 镜像链里 Gitee 排第一（国内直连最快最稳）。

## 建仓库（一次性）

**GitHub 侧（必需）：**
1. GitHub 新建**公开**仓库 `wf-data`（名字要一致，App 内置的是 `cyxcmiao/wf-data`）。
2. 把本目录两个文件放进仓库根目录，改名：
   - `fetch_rivens.py` → 仓库根目录
   - `wf-data.yml` → `.github/workflows/fetch-rivens.yml`
3. 仓库 Actions 页手动 Run 一次，确认根目录出现 `rivens_pc.json`。

**Gitee 侧（推荐，国内访问快）：**
1. Gitee 注册/实名认证（新账号需认证后才能建仓库），新建**公开**仓库 `wf-data`（同名）。
2. Gitee 个人设置 → 安全设置 → **私人令牌** → 生成新令牌，勾选 `projects` 权限，复制令牌。
3. 回到 GitHub 的 `wf-data` 仓库 → Settings → Secrets and variables → Actions → New repository secret：
   Name 填 `GITEE_TOKEN`，Secret 填刚才的令牌。
4. 配好后再手动 Run 一次 workflow，"push to gitee mirror" 步骤变绿即同步成功。

没配 Gitee 时 workflow 照常工作（该步骤自动跳过），随时可补。

## 验证

浏览器打开以下任一地址，应能看到 JSON：
- https://gitee.com/cyxcmiao/wf-data/raw/main/rivens_pc.json （国内直连）
- https://cdn.jsdelivr.net/gh/cyxcmiao/wf-data@main/rivens_pc.json

## 改用户名/仓库名

- App 镜像链：`app/src/main/java/com/wfapp/fissures/data/RivenMarket.kt` 的 `MIRROR_URLS`（companion object 内），改后重新打包。
- workflow 里 Gitee 克隆地址中的 `cyxcmiao` 同步改掉。

## 备用：WM 实时挂单若也被墙

WM 挂单是分钟级实时数据，快照方案不适用。若实测直连 `api.warframe.market` 不通，
唯一免 VPN 路线是国内云函数中转（腾讯云函数/阿里云函数计算免费额度即可）：
部署一个 HTTP 触发函数转发请求到 `api.warframe.market`，App 侧加一个中转基址回退即可。
需要时再实现。
