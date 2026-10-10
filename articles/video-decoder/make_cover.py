# -*- coding: utf-8 -*-
"""视频解码器产品综述 · 封面制作
底图为 AI 生成（无文字内容）。流程：亮度阈值扫描定位右下角水印真实包围盒
→ 同高度紧邻区域取底色、内侧全替换 / 外缘窄羽化 → 底部渐隐深色带 + 标题白字。
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
px = img.load()

# ---- 1. 定位右下角水印包围盒（亮度阈值扫描，只扫右下角区域）----
import numpy as np
arr = np.asarray(img).astype(int)
corner = arr[int(h * 0.85):, int(w * 0.80):]
mask = corner.min(axis=2) > 110
ys, xs = np.where(mask)
if len(xs) > 0:
    cx0, cx1 = int(w * 0.80) + xs.min(), int(w * 0.80) + xs.max()
    cy0, cy1 = int(h * 0.85) + ys.min(), int(h * 0.85) + ys.max()
else:
    cx0, cy0, cx1, cy1 = int(w * 0.90), int(h * 0.93), w, h
print("watermark bbox:", cx0, cy0, cx1, cy1)

# 同高度紧邻区域取底色（从水印左侧取，不从画面中部取）
clean = img.crop((max(0, cx0 - int(w * 0.16)), cy0, max(1, cx0 - 10), cy1 + 1))
pc = list(clean.getdata())
avg = tuple(int(sum(c[i] for c in pc) / max(1, len(pc))) for i in range(3))

pad = 8
x0, y0 = max(0, cx0 - pad), max(0, cy0 - pad)
x1, y1 = min(w, cx1 + pad), min(h, cy1 + pad)
# 羽化只发生在 pad 缓冲带内——到水印真实边缘必须已 100% 替换，否则上缘残留
fx, fy2 = pad, pad
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
d.text((mx, ty), "视频解码器产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(h * 0.079)),
       "从码流到大屏，解码能力这笔账到底怎么算 ｜ 面向工程端 · 选型与落地视角",
       font=f_sub, fill=(160, 208, 230))

img.save(OUT)
print("cover.png done", img.size, "| inpaint avg =", avg)
