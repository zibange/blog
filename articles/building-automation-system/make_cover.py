# -*- coding: utf-8 -*-
"""楼宇自控系统（BAS）产品综述 · 封面制作

底图为 AI 生成（不含文字）。流程：
  1) 亮度阈值扫描定位右下角水印真实包围盒（不凭感觉设框）
  2) 从同高度的紧邻区域取底色
  3) 内侧 100% 替换，仅在左缘 / 上缘留窄羽化 —— 避免弱羽化造成角点残留
  4) 底部渐隐深色带 + 标题白字
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")

RAW = None
for f in sorted(os.listdir(IMG_DIR)):
    if f.endswith(".png") and f.startswith("Abstract_technical_concept_ill"):
        RAW = os.path.join(IMG_DIR, f)
        break
assert RAW, "未找到 AI 底图"
BASE = os.path.join(IMG_DIR, "cover_raw.png")
OUT = os.path.join(IMG_DIR, "cover.png")

img = Image.open(RAW).convert("RGB")
img.save(BASE)
w, h = img.size
px = img.load()
print("size:", w, h)

# ---- 1. 定位右下角水印包围盒（亮度阈值扫描）----
arr = np.asarray(img).astype(int)
x_lo, y_lo = int(w * 0.78), int(h * 0.86)
corner = arr[y_lo:, x_lo:]
mask = corner.min(axis=2) > 95          # 暗底上的亮字
ys, xs = np.where(mask)
if len(xs) > 0:
    cx0, cx1 = x_lo + int(xs.min()), x_lo + int(xs.max())
    cy0, cy1 = y_lo + int(ys.min()), y_lo + int(ys.max())
else:
    cx0, cy0, cx1, cy1 = int(w * 0.88), int(h * 0.92), w, h
print("watermark bbox:", cx0, cy0, cx1, cy1,
      "| rel:", round(cx0 / w, 3), round(cy0 / h, 3), round(cx1 / w, 3), round(cy1 / h, 3))

# ---- 2. 同高度紧邻区域取底色（从水印左侧同高度取）----
sample = img.crop((max(0, cx0 - int(w * 0.20)), cy0, max(1, cx0 - 12), cy1 + 1))
sp = list(sample.getdata())
avg = tuple(int(sum(c[i] for c in sp) / max(1, len(sp))) for i in range(3))
print("avg base color:", avg)

# ---- 3. 内侧全替换，仅左/上缘窄羽化 ----
pad = 6
x0, y0 = max(0, cx0 - pad), max(0, cy0 - pad)
x1, y1 = min(w, cx1 + pad + 1), min(h, cy1 + pad + 1)
feather_x, feather_y = float(pad), float(pad)
for yy in range(y0, y1):
    for xx in range(x0, x1):
        tx = min(1.0, (xx - x0) / feather_x) if feather_x > 0 else 1.0
        ty = min(1.0, (yy - y0) / feather_y) if feather_y > 0 else 1.0
        t = tx * ty
        r, g, b = px[xx, yy]
        px[xx, yy] = (int(avg[0] * t + r * (1 - t)),
                      int(avg[1] * t + g * (1 - t)),
                      int(avg[2] * t + b * (1 - t)))

# 替换后再复核一次：确认残留亮点已消失
arr2 = np.asarray(img).astype(int)
chk = arr2[cy0:cy1 + 1, cx0:cx1 + 1].min(axis=2)
print("residual bright pixels after clean:", int((chk > 95).sum()))

# ---- 4. 底部渐隐深色带 + 标题 ----
band_h = int(h * 0.38)
band_y = h - band_h
band = Image.new("L", (w, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(40 + 185 * (i / band_h) ** 1.25)
    db.line([(0, i), (w, i)], fill=a)
img.paste(Image.new("RGB", (w, band_h), (5, 17, 33)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.65))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"
f_main = ImageFont.truetype(fy_bd, int(h * 0.062))
f_sub = ImageFont.truetype(fy, int(h * 0.0265))

mx, ty = int(w * 0.052), int(h * 0.735)
d.text((mx, ty), "楼宇自控系统（BAS）产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(h * 0.082)),
       "法定门槛之上，拼的不是设备清单而是参数整定",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(h * 0.124)),
       "四层架构 · 三层时间尺度 ｜ MS/TP 带宽账 ｜ 10 个可复现工程算例 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(h * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
