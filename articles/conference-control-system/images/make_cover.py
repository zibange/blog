# -*- coding: utf-8 -*-
"""会议中控系统产品综述 · 封面制作

底图为 ImageGen 生成的 AI 概念图（不含文字）。流程：
  1) 亮度阈值扫描定位右下角水印真实包围盒（ImageGen 通常无水印，则跳过替换）
  2) 底部渐隐深色带 + 标题白字
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "cover_raw.png")
OUT = os.path.join(HERE, "cover.png")

img = Image.open(RAW).convert("RGB")
w, h = img.size
px = img.load()
print("size:", w, h)

# ---- 1. 定位右下角水印包围盒（亮度阈值扫描）----
arr = np.asarray(img).astype(int)
x_lo, y_lo = int(w * 0.70), int(h * 0.86)
corner = arr[y_lo:, x_lo:]
mask = corner.min(axis=2) > 95          # 暗底上的亮字
ys, xs = np.where(mask)
if len(xs) > 50:
    cx0, cx1 = x_lo + int(xs.min()), x_lo + int(xs.max())
    cy0, cy1 = y_lo + int(ys.min()), y_lo + int(ys.max())
    print("watermark bbox:", cx0, cy0, cx1, cy1)
    sample = img.crop((max(0, cx0 - int(w * 0.20)), cy0, max(1, cx0 - 12), cy1 + 1))
    sp = list(sample.getdata())
    avg = tuple(int(sum(c[i] for c in sp) / max(1, len(sp))) for i in range(3))
    pad = 8
    x0, y0 = max(0, cx0 - pad), max(0, cy0 - pad)
    x1, y1 = min(w, cx1 + pad + 1), min(h, cy1 + pad + 1)
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            tx = min(1.0, (xx - x0) / pad) if pad > 0 else 1.0
            ty = min(1.0, (yy - y0) / pad) if pad > 0 else 1.0
            t = tx * ty
            r, g, b = px[xx, yy]
            px[xx, yy] = (int(avg[0] * t + r * (1 - t)),
                          int(avg[1] * t + g * (1 - t)),
                          int(avg[2] * t + b * (1 - t)))
    arr2 = np.asarray(img).astype(int)
    chk = arr2[cy0:cy1 + 1, cx0:cx1 + 1].min(axis=2)
    print("residual bright pixels:", int((chk > 95).sum()))
else:
    print("no significant watermark; skip removal")

# ---- 4. 底部渐隐深色带 + 标题 ----
band_h = int(h * 0.42)
band_y = h - band_h
band = Image.new("L", (w, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(28 + 200 * (i / band_h) ** 1.35)
    db.line([(0, i), (w, i)], fill=a)
img.paste(Image.new("RGB", (w, band_h), (5, 16, 30)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.65))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"
f_main = ImageFont.truetype(fy_bd, int(h * 0.058))
f_sub = ImageFont.truetype(fy, int(h * 0.0265))

mx, ty = int(w * 0.052), int(h * 0.700)
d.text((mx, ty), "会议中控系统产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(h * 0.078)),
       "把十几个遥控器的逻辑，收进一块主机的时序里",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(h * 0.120)),
       "中央控制 · 12 个可复现工程算例 ｜ 42 处 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(h * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
