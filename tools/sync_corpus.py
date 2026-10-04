# -*- coding: utf-8 -*-
"""重建站内检索语料，并校验与站点实际文章是否一致。

背景：corpus.json 是生成物，每次发布新文章后必须重建，否则问答机器人
（尤其后端不可达时的本地离线检索）会检索不到新文章，且不会报错、只是"少几篇"。

用法：
    python tools/sync_corpus.py            # 重建并输出差异报告
    python tools/sync_corpus.py --check    # 只检查是否过期，不写文件（过期则退出码 1）
"""
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.normpath(os.path.join(HERE, ".."))
MANIFEST = os.path.join(BLOG, "articles.json")
CORPUS = os.path.join(BLOG, "assets", "qa", "corpus.json")
GENERATOR = os.path.normpath(os.path.join(BLOG, "..", "ai-chatbot", "build_corpus.py"))


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def report(manifest_arts, corpus):
    """返回 (站点篇数, 语料篇数, 缺失列表, 多余列表)"""
    site_slugs = [a.get("slug") for a in manifest_arts]
    corpus_slugs = [a.get("slug") for a in corpus.get("articles", [])]
    cs = set(corpus_slugs)
    ss = set(site_slugs)
    title_of = {a.get("slug"): a.get("title", "") for a in manifest_arts}
    missing = [(s, title_of.get(s, "")) for s in site_slugs if s not in cs]
    extra = [s for s in corpus_slugs if s not in ss]
    return len(site_slugs), len(corpus_slugs), missing, extra


def main():
    check_only = "--check" in sys.argv

    manifest = load(MANIFEST)
    arts = manifest.get("articles", [])
    if not os.path.exists(CORPUS):
        print("[错误] 语料不存在: %s" % CORPUS)
        return 1

    old = load(CORPUS)
    n_site, n_old, missing, extra = report(arts, old)

    print("站点文章: %d 篇" % n_site)
    print("现有语料: %d 篇 / %d 片段 （生成于 %s）"
          % (n_old, len(old.get("chunks", [])), old.get("generatedAt", "?")))

    if not missing and not extra:
        print("[一致] 语料与站点文章完全匹配，无需重建。")
        return 0

    if missing:
        print("\n[缺失] 站点有、语料没有（%d 篇）：" % len(missing))
        for s, t in missing:
            print("   - %s | %s" % (s, t))
    if extra:
        print("\n[多余] 语料有、站点已无（%d 篇）：" % len(extra))
        for s in extra:
            print("   - %s" % s)

    if check_only:
        print("\n[过期] 语料需要重建（完整命令：python tools/sync_corpus.py）")
        return 1

    if not os.path.exists(GENERATOR):
        print("\n[错误] 找不到生成器: %s" % GENERATOR)
        return 1

    print("\n[重建] 调用生成器 …")
    r = subprocess.run([sys.executable, GENERATOR, "--out", CORPUS],
                       cwd=os.path.dirname(GENERATOR))
    if r.returncode != 0:
        print("[失败] 生成器退出码 %d" % r.returncode)
        return r.returncode

    new = load(CORPUS)
    n_site2, n_new, missing2, extra2 = report(arts, new)
    print("\n[结果] 文章 %d → %d 篇，片段 %d → %d 条"
          % (n_old, n_new, len(old.get("chunks", [])), len(new.get("chunks", []))))
    if missing2 or extra2:
        print("[警告] 重建后仍不一致：缺失 %d / 多余 %d" % (len(missing2), len(extra2)))
        return 1
    print("[完成] 语料已与站点文章对齐。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
