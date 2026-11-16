# -*- coding: utf-8 -*-
"""
GitHub Actions 定时任务：抓取 warframestat.us 全量裂罅行情快照 → rivens_pc.json。

GitHub Actions 的美国机房 IP 不会被 Cloudflare 质询拦截（与国内住宅网络不同），
快照经 Gitee / jsDelivr 等镜像供 App 无 VPN 拉取。数据源本身小时级更新，6 小时一次足够。
warframestat.us 偶发响应挂起（实测出现过读超时），带重试与退避。
"""
import json
import time
import urllib.request

URL = "https://api.warframestat.us/pc/rivens"
OUT = "rivens_pc.json"
ATTEMPTS = 4
TIMEOUT = 90


def fetch() -> bytes:
    last: Exception = RuntimeError("未尝试")
    for i in range(ATTEMPTS):
        try:
            req = urllib.request.Request(
                URL,
                headers={"User-Agent": "wf-data-snapshot/1.0 (GitHub Actions; contact: cyxcmiao)"},
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                raw = resp.read()
            data = json.loads(raw)  # 校验是合法 JSON，抓到错误页直接视为失败重试
            if not isinstance(data, dict) or not data:
                raise ValueError("快照内容异常：非对象或为空")
            return raw
        except Exception as e:  # noqa: BLE001 网络类异常统一退避重试
            last = e
            print(f"第 {i + 1}/{ATTEMPTS} 次尝试失败: {e}")
            if i < ATTEMPTS - 1:
                time.sleep(10 * (i + 1))
    raise last


def main() -> None:
    raw = fetch()
    with open(OUT, "wb") as f:
        f.write(raw)
    print(f"已保存 {OUT}: {len(raw)} 字节")


if __name__ == "__main__":
    main()
