# -*- coding: utf-8 -*-
"""
GitHub Actions 定时任务：抓取 warframestat.us 全量裂罅行情快照 → rivens_pc.json。

GitHub Actions 的美国机房 IP 不会被 Cloudflare 质询拦截（与国内住宅网络不同），
快照经 jsDelivr / ghfast 等镜像供 App 无 VPN 拉取。数据源本身小时级更新，6 小时一次足够。
"""
import json
import urllib.request

URL = "https://api.warframestat.us/pc/rivens"
OUT = "rivens_pc.json"


def main() -> None:
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "wf-data-snapshot/1.0 (GitHub Actions; contact: cyxcmiao)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    data = json.loads(raw)  # 校验是合法 JSON，抓到错误页直接让 Action 失败
    if not isinstance(data, dict) or not data:
        raise SystemExit("快照内容异常：非对象或为空")
    with open(OUT, "wb") as f:
        f.write(raw)
    print(f"已保存 {OUT}: {len(raw)} 字节, {sum(len(v) for v in data.values())} 个武器")


if __name__ == "__main__":
    main()
