# -*- coding: utf-8 -*-
"""人脸识别终端 · 封面制作
底图为 AI 生成（无文字），流程：去右下角水印（背景填充 + 边缘羽化，非裁剪）→ 底部渐隐深色带 + 标题白字。
按内容引擎配图规范：封面文字在干净底图上一遍完成，深色半透明底衬保证对比度。
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "images", "cover_raw.png")
OUT = os.path.join(HERE, "images", "cover.png")

img = Image.open(BASE).convert("RGB")
w, h = img.size

# ---- 1. 去右下角水印：同高度紧邻区域取底色 + 大范围硬替换，仅外缘做窄羽化（近似 inpaint，非裁剪）----
x0, y0, x1, y1 = int(w * 0.80), int(h * 0.855), w, h
clean = img.crop((int(w * 0.60), int(h * 0.87), int(w * 0.78), h))
px_clean = list(clean.getdata())
avg = tuple(int(sum(c[i] for c in px_clean) / max(1, len(px_clean))) for i in range(3))
px = img.load()
dw, dh = x1 - x0, y1 - y0
fx, fy2 = max(1, int(dw * 0.18)), max(1, int(dh * 0.26))
for yy in range(y0, y1):
    for xx in range(x0, x1):
        u = min(1.0, (xx - x0) / fx)     # 左缘窄羽化，内侧立即全替换
        v = min(1.0, (yy - y0) / fy2)    # 上缘窄羽化
        t = u * v
        r, g, b = px[xx, yy]
        px[xx, yy] = (int(avg[0] * t + r * (1 - t)),
                      int(avg[1] * t + g * (1 - t)),
                      int(avg[2] * t + b * (1 - t)))

# ---- 2. 底部深色渐隐带 + 标题（一步完成）----
band_h = int(h * 0.30)
band_y = h - band_h
band = Image.new("L", (w, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(35 + 180 * (i / band_h) ** 1.15)
    db.line([(0, i), (w, i)], fill=a)
img.paste(Image.new("RGB", (w, band_h), (6, 18, 34)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.8))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
f_main = ImageFont.truetype(fy, int(h * 0.070))
f_sub = ImageFont.truetype(fy, int(h * 0.030))

mx, ty = int(w * 0.055), int(h * 0.775)
d.text((mx, ty), "人脸识别终端", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(h * 0.084)),
       "把一张脸变成通行凭证 ｜ 面向工程端 · 选型与落地视角",
       font=f_sub, fill=(168, 210, 232))

img.save(OUT)
print("cover.png done", img.size, "| inpaint avg =", avg)
