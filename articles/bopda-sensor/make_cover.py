# -*- coding: utf-8 -*-
"""分布式光纤应变传感（BOTDA）· 封面制作
底图为 AI 生成（无文字内容），流程：去右下角平台水印（同高度紧邻区域取底色 + 内侧全替换、外缘窄羽化）
→ 底部渐隐深色带 + 标题白字。按内容引擎配图规范：封面文字在干净底图上一遍完成。
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")
RAW = None
for f in sorted(os.listdir(IMG_DIR)):
    if f.startswith("Wide_cinematic") and f.endswith(".png"):
        RAW = os.path.join(IMG_DIR, f)
        break
BASE = os.path.join(IMG_DIR, "cover_raw.png")
OUT = os.path.join(IMG_DIR, "cover.png")

img = Image.open(RAW).convert("RGB")
img.save(BASE)
w, h = img.size

# ---- 1. 去右下角水印 ----
x0, y0, x1, y1 = int(w * 0.865), int(h * 0.895), w, h
# 同高度的紧邻区域取底色（不是从画面中部取）
clean = img.crop((int(w * 0.66), y0, int(w * 0.85), y1))
px_clean = list(clean.getdata())
avg = tuple(int(sum(c[i] for c in px_clean) / max(1, len(px_clean))) for i in range(3))
px = img.load()
dw, dh = x1 - x0, y1 - y0
fx, fy2 = max(1, int(dw * 0.20)), max(1, int(dh * 0.30))
for yy in range(y0, y1):
    for xx in range(x0, x1):
        u = min(1.0, (xx - x0) / fx)      # 左缘窄羽化，内侧立即全替换
        v = min(1.0, (yy - y0) / fy2)     # 上缘窄羽化
        t = u * v
        r, g, b = px[xx, yy]
        px[xx, yy] = (int(avg[0] * t + r * (1 - t)),
                      int(avg[1] * t + g * (1 - t)),
                      int(avg[2] * t + b * (1 - t)))

# ---- 2. 底部深色渐隐带 + 标题（一步完成）----
band_h = int(h * 0.32)
band_y = h - band_h
band = Image.new("L", (w, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(45 + 175 * (i / band_h) ** 1.15)
    db.line([(0, i), (w, i)], fill=a)
img.paste(Image.new("RGB", (w, band_h), (6, 18, 34)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.7))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
f_main = ImageFont.truetype(fy, int(h * 0.062))
f_sub = ImageFont.truetype(fy, int(h * 0.028))

mx, ty = int(w * 0.055), int(h * 0.760)
d.text((mx, ty), "分布式光纤应变传感（BOTDA）", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(h * 0.079)),
       "把一根光缆变成上万个测点的传感神经 ｜ 面向工程端 · 选型与落地视角",
       font=f_sub, fill=(160, 208, 230))

img.save(OUT)
print("cover.png done", img.size, "| inpaint avg =", avg)
