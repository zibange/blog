# -*- coding: utf-8 -*-
"""发布后线上验证（通用版）：轮询等待 GitHub Pages 构建生效，最长 25 分钟。

用法：
    python tools/verify_publish.py --slug bopda-sensor --commit 20a4a13
    python tools/verify_publish.py --slug xxx --expected-articles 23 --expected-chunks 1254

自动从 articles.json 定位该 slug 的正文文件名，并扫描其 images/ 目录下所有 png 作为待校验资源。
"""
import argparse
import glob
import json
import os
import ssl
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://hardwarewatch.de5.net"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(path, ts, timeout=40):
    # 路径含中文文件名时必须百分号编码，否则 urllib 直接抛异常（返回 -1）
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
             "https://api.github.com/repos/zibange/blog/commits?per_page=3"],
            capture_output=True, timeout=40)
        d = json.loads(out.stdout.decode("utf-8", "ignore"))
        return [(c["sha"][:7], c["commit"]["message"].split("\n")[0][:46]) for c in d]
    except Exception as e:
        return [("?", str(e)[:60])]


def local_meta(slug):
    d = json.load(open(os.path.join(ROOT, "articles.json"), encoding="utf-8"))
    art = [a for a in d["articles"] if a["slug"] == slug][0]
    return d, art


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--commit", default=None, help="期望的 GitHub 短 sha（7 位）")
    ap.add_argument("--expected-articles", type=int, default=None)
    ap.add_argument("--expected-chunks", type=int, default=None)
    ap.add_argument("--timeout-min", type=int, default=25)
    args = ap.parse_args()

    d_local, art = local_meta(args.slug)
    exp_articles = args.expected_articles or len(d_local["articles"])
    dirp = os.path.join(ROOT, "articles", args.slug)
    md_path = f"articles/{args.slug}/{art['file']}"
    assets = [f"articles/{args.slug}/images/{os.path.basename(p)}"
              for p in sorted(glob.glob(os.path.join(dirp, "images", "*.png")))]

    print(f"slug={args.slug}  期望篇数={exp_articles}  期望片段={args.expected_chunks}  "
          f"期望 commit={args.commit}")
    print(f"正文={md_path}")
    print(f"资源={assets}\n")

    deadline = time.time() + args.timeout_min * 60
    rnd = 0
    while True:
        rnd += 1
        ts = int(time.time() * 1000)
        heads = gh_head()
        st, body = fetch("articles.json", ts)
        n, last = -1, ""
        if st == 200:
            try:
                j = json.loads(body.decode("utf-8"))
                arts = j["articles"]
                n, last = len(arts), arts[-1]["slug"]
            except Exception:
                pass
        print(f"[{rnd:02d}] {time.strftime('%H:%M:%S')} GitHub={heads[0][0]} "
              f"articles.json={st} 篇数={n} last={last}", flush=True)

        ok_gh = (args.commit is None) or any(h[0] == args.commit for h in heads)
        if st == 200 and n == exp_articles and last == args.slug and ok_gh:
            break
        if time.time() > deadline:
            print("!! 等待超时，按当前状态收尾", flush=True)
            break
        time.sleep(60)

    ts = int(time.time() * 1000)
    print("\n================ 关键指标 ================")
    st, body = fetch("articles.json", ts)
    j = json.loads(body.decode("utf-8"))
    e = [a for a in j["articles"] if a["slug"] == args.slug][0]
    print(f"articles.json  {st}  篇数={len(j['articles'])}  last={j['articles'][-1]['slug']}")
    print(f"  新条目 date={e['date']} readTime={e['readTime']} category={e['category']}")
    print(f"  title={e['title']}")

    print("\n================ 资源 200 校验 ================")
    for p in [md_path, "article.html", "index.html", "sitemap.xml", "assets/js/article.js"] + assets:
        st, body = fetch(p, ts)
        print(f"  {st:>4}  {len(body):>10,} B  {p}")

    print("\n================ 语料校验 ================")
    want = args.expected_chunks
    for _ in range(6):
        ts = int(time.time() * 1000)
        st, body = fetch("assets/qa/corpus.json", ts)
        cnt, meta = -1, ""
        if st == 200:
            try:
                c = json.loads(body.decode("utf-8"))
                chunks = c.get("chunks") or c.get("items") or []
                cnt = len(chunks)
                meta = f"generatedAt={c.get('generatedAt', '?')}"
            except Exception as ex:
                meta = f"解析失败 {ex}"
        print(f"  corpus.json {st} 片段={cnt} {meta if st == 200 else ''}")
        if want is None or cnt == want:
            break
        time.sleep(60)

    print("\n================ sitemap 校验 ================")
    st, body = fetch("sitemap.xml", ts)
    if st == 200:
        locs = body.decode("utf-8", "ignore").count("<loc>")
        print(f"  <loc> 条数 = {locs}（应为 文章数 + 1 = {exp_articles + 1}）")


if __name__ == "__main__":
    main()
