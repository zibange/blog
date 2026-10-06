# -*- coding: utf-8 -*-
"""发布后线上验证：轮询等待 GitHub Pages 构建生效，最多 25 分钟。"""
import json
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://hardwarewatch.de5.net"
SLUG = "face-recognition-terminal"
MD = "articles/face-recognition-terminal/人脸识别终端产品综述.md"
ASSETS = [
    "articles/face-recognition-terminal/images/cover.png",
    "articles/face-recognition-terminal/images/arch-pipeline.png",
    "articles/face-recognition-terminal/images/threshold-far-frr.png",
    "articles/face-recognition-terminal/images/lens-geometry.png",
    "articles/face-recognition-terminal/images/flow-pass.png",
]
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(path, ts, timeout=30):
    # 路径含中文文件名时必须百分号编码，否则 urllib 会直接抛异常（返回 -1）
    url = f"{BASE}/{urllib.parse.quote(path)}?cb={ts}"
    req = urllib.request.Request(url, headers={
        "Cache-Control": "no-cache", "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (verifier)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return -1, str(e).encode()


def gh_head():
    try:
        out = subprocess.run(
            ["curl", "-s", "-H", "Cache-Control: no-cache",
             "https://api.github.com/repos/zibange/blog/commits?per_page=1"],
            capture_output=True, timeout=30)
        d = json.loads(out.stdout.decode("utf-8", "ignore"))
        return d[0]["sha"][:7], d[0]["commit"]["message"].split("\n")[0][:40]
    except Exception as e:
        return "?", str(e)[:60]


def main():
    deadline = time.time() + 25 * 60
    round_i = 0
    while True:
        round_i += 1
        ts = int(time.time() * 1000)
        gh, msg = gh_head()
        st, body = fetch("articles.json", ts)
        n, last = -1, ""
        if st == 200:
            try:
                d = json.loads(body.decode("utf-8"))
                arts = d["articles"]
                n = len(arts)
                last = arts[-1]["slug"]
            except Exception:
                pass
        print(f"[{round_i:02d}] {time.strftime('%H:%M:%S')} GitHub={gh} "
              f"articles.json={st} 篇数={n} last={last}", flush=True)

        if st == 200 and n == 22 and last == SLUG and gh == "b23fc95":
            break
        if time.time() > deadline:
            print("!! 等待超时，按当前状态收尾", flush=True)
            break
        time.sleep(60)

    ts = int(time.time() * 1000)
    print("\n================ 关键指标 ================")
    st, body = fetch("articles.json", ts)
    d = json.loads(body.decode("utf-8"))
    e = [a for a in d["articles"] if a["slug"] == SLUG][0]
    print(f"articles.json      {st}  篇数={len(d['articles'])}  last={d['articles'][-1]['slug']}")
    print(f"  新条目 date={e['date']} readTime={e['readTime']} category={e['category']}")

    print("\n================ 资源 200 校验 ================")
    for p in [MD] + ASSETS:
        st, body = fetch(p, ts)
        print(f"  {st:>3}  {len(body):>9,} B  {p}")

    print("\n================ 语料校验 ================")
    for _ in range(6):
        ts = int(time.time() * 1000)
        st, body = fetch("assets/qa/corpus.json", ts)
        cnt = -1
        if st == 200:
            try:
                c = json.loads(body.decode("utf-8"))
                chunks = c.get("chunks") or c.get("items") or []
                cnt = len(chunks)
                meta = f"generatedAt={c.get('generatedAt', '?')}"
            except Exception as ex:
                meta = f"解析失败 {ex}"
        print(f"  corpus.json {st} 片段={cnt} {meta if st == 200 else ''}")
        if cnt == 1155:
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
