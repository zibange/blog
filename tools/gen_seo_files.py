# -*- coding: utf-8 -*-
"""从 articles.json 生成 sitemap.xml 与 robots.txt。

用法：
    python gen_seo_files.py [--base https://hardwarewatch.de5.net] [--root ../]

发布新文章后跑一次即可。站点地址变更时改 --base。
"""
import argparse
import json
import os
import sys
from xml.sax.saxutils import escape


def build_urls(base, articles):
    urls = [{"loc": base + "/", "lastmod": "", "priority": "1.0", "changefreq": "daily"}]
    for a in articles:
        slug = a.get("slug")
        if not slug:
            continue
        urls.append({
            "loc": "%s/article.html?slug=%s" % (base, slug),
            "lastmod": a.get("date", ""),
            "priority": "0.8",
            "changefreq": "monthly",
        })
    return urls


def render_sitemap(urls):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        out.append("  <url>")
        # loc 里的 & 必须转义，否则 sitemap 校验不通过
        out.append("    <loc>%s</loc>" % escape(u["loc"]))
        if u["lastmod"]:
            out.append("    <lastmod>%s</lastmod>" % u["lastmod"])
        out.append("    <changefreq>%s</changefreq>" % u["changefreq"])
        out.append("    <priority>%s</priority>" % u["priority"])
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def render_robots(base):
    return "\n".join([
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: %s/sitemap.xml" % base,
        "",
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="博客根目录（articles.json 所在目录）")
    ap.add_argument("--base", default="https://hardwarewatch.de5.net", help="站点根地址")
    args = ap.parse_args()

    src = os.path.join(args.root, "articles.json")
    if not os.path.exists(src):
        sys.exit("找不到 %s" % src)
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    articles = data.get("articles", []) if isinstance(data, dict) else data
    if not articles:
        sys.exit("articles.json 中没有文章")

    base = args.base.rstrip("/")
    urls = build_urls(base, articles)

    spath = os.path.join(args.root, "sitemap.xml")
    rpath = os.path.join(args.root, "robots.txt")
    with open(spath, "w", encoding="utf-8") as f:
        f.write(render_sitemap(urls))
    with open(rpath, "w", encoding="utf-8") as f:
        f.write(render_robots(base))

    print("已生成 %s（%d 条 URL）" % (spath, len(urls)))
    print("已生成 %s（Sitemap: %s/sitemap.xml）" % (rpath, base))


if __name__ == "__main__":
    main()
