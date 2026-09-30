# -*- coding: utf-8 -*-
"""NVR 封面制作：去 AI 水印（背景填充+边缘羽化，非裁剪）→ 一步叠加标题 → 产出 cover.png
按技能 §9：封面文字在干净底图上一遍完成；深色半透明渐隐底衬保证对比度。"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, math

BASE = os.path.join(os.path.dirname(__file__), "images", "cover_clean.jpg")
OUT = os.path.join(os.path.dirname(__file__), "images", "cover.png")

img = Image.open(BASE).convert("RGB")
w, h = img.size

# ---- 1. 去右下角"AI生成"水印：以角点为最强羽化核心，向外衰减（近似 inpaint，非裁剪）----
x0, y0, x1, y1 = int(w * 0.84), int(h * 0.86), w, h
# 取水印上方/左侧同为底部色带的"干净带"均值作为填充底色
clean = img.crop((int(w * 0.5), int(h * 0.78), int(w * 0.74), int(h * 0.95)))
avg = tuple(int(sum(c[i] for c in clean.getdata()) / max(1, clean.size[0] * clean.size[1])) for i in range(3))
px = img.load()
dw = x1 - x0; dh = y1 - y0
for yy in range(y0, y1):
    for xx in range(x0, x1):
        u = (xx - x0) / dw          # 越靠右下(贴近水印)越大
        v = (yy - y0) / dh
        t = max(u, v) ** 2.4        # 右下角最强=1，向内快速衰减
        r, g, b = px[xx, yy]
        px[xx, yy] = (int(avg[0] * t + r * (1 - t)),
                      int(avg[1] * t + g * (1 - t)),
                      int(avg[2] * t + b * (1 - t)))

# ---- 2. 底部深色渐隐带 + 标题文字（一步完成）----
band_h = int(h * 0.28)
band_y = h - band_h
band = Image.new("L", (w, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(40 + 175 * (i / band_h))                  # 自上而下渐深
    db.line([(0, i), (w, i)], fill=a)
black = Image.new("RGB", (w, band_h), (6, 18, 34))
img.paste(black, (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(1))          # 轻微柔化使羽化/叠加浑然一体

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"                      # 微软雅黑（含 CJK）
f_main = ImageFont.truetype(fy, int(h * 0.072))
f_sub = ImageFont.truetype(fy, int(h * 0.031))

mx = int(w * 0.055); ty = int(h * 0.79)
d.text((mx, ty), "网络硬盘录像机（NVR）", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(h * 0.082)), "视频监控系统的中心节点 ｜ 面向工程端 · 选型与落地视角",
       font=f_sub, fill=(168, 210, 232))

img.save(OUT)
print("cover.png done", img.size, "| inpaint avg_color=", avg)