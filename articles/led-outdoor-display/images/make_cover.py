# -*- coding: utf-8 -*-
"""户外 LED 显示屏产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝夜空渐变背景 + 远处城市剪影
  2) 一面由像素点阵组成的户外大屏（代表 LED 屏的像素化自发光）
  3) 能量光带表现信号流动
  4) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
输出：cover_raw.png（底图）与 cover.png（成片）
"""
import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "cover_raw.png")
OUT = os.path.join(HERE, "cover.png")

W, H = 1536, 1024
random.seed(7)

# ---- 1. 深蓝夜空渐变背景 ----
top = np.array([6, 16, 38], dtype=float)        # 顶部深蓝夜空
bot = np.array([14, 34, 66], dtype=float)       # 底部稍亮
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 远处城市剪影 ----
base_y = int(H * 0.72)
x = 0
while x < W:
    rw = random.randint(60, 120)
    rh = random.randint(int(H * 0.18), int(H * 0.42))
    d.rectangle([x, base_y - rh, x + rw, H], fill=(4, 12, 26, 200))
    for sy in range(base_y - rh + 12, base_y - 8, 18):
        if random.random() < 0.25:
            lx = x + random.randint(8, max(9, rw - 14))
            col = random.choice([(90, 200, 240, 150), (255, 200, 120, 140)])
            d.rectangle([lx, sy, lx + 5, sy + 7], fill=col)
    x += rw + random.randint(8, 22)

# ---- 3. 户外大屏：像素点阵（自发光 LED 屏）----
sx0, sy0 = int(W * 0.10), int(H * 0.16)
scr_w, scr_h = int(W * 0.80), int(H * 0.42)
# 屏体深色底衬
d.rounded_rectangle([sx0 - 10, sy0 - 10, sx0 + scr_w + 10, sy0 + scr_h + 10],
                    radius=14, fill=(3, 8, 18, 235))
pitch = 14
colors = [(70, 160, 255), (90, 220, 170), (240, 180, 90), (220, 90, 140), (120, 200, 255)]
yy = sy0 + 6
while yy < sy0 + scr_h - 6:
    xx = sx0 + 6
    while xx < sx0 + scr_w - 6:
        if random.random() < 0.82:
            c = random.choice(colors)
            a = random.randint(120, 230)
            r = random.randint(3, 5)
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(c[0], c[1], c[2], a))
        xx += pitch
    yy += pitch
# 屏体高光描边
d.rounded_rectangle([sx0 - 10, sy0 - 10, sx0 + scr_w + 10, sy0 + scr_h + 10],
                    radius=14, outline=(90, 170, 240, 160), width=3)

# ---- 4. 能量光带（信号流动）----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(5):
    y0 = sy0 + scr_h + 30 + i * 40
    pts = []
    for t in range(0, 101, 2):
        xx = W * t / 100
        yy = y0 - 50 * math.sin(math.pi * t / 100) * (0.6 + 0.08 * i)
        pts.append((xx, yy))
    gd.line(pts, fill=(90, 170, 255, 60 - i * 8), width=4)
glow = glow.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save(RAW)
print("cover_raw.png done", img.size)

# ---- 5. 底部渐隐深色带 + 标题（与既有封面流程一致）----
band_h = int(H * 0.42)
band_y = H - band_h
band = Image.new("L", (W, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(28 + 200 * (i / band_h) ** 1.35)
    db.line([(0, i), (W, i)], fill=a)
img.paste(Image.new("RGB", (W, band_h), (4, 12, 26)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.65))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"
f_main = ImageFont.truetype(fy_bd, int(H * 0.058))
f_sub = ImageFont.truetype(fy, int(H * 0.0265))

mx, ty = int(W * 0.052), int(H * 0.700)
d.text((mx, ty), "户外 LED 显示屏产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "高亮度对抗阳光、IP65 抵御风雨、密闭结构扛太阳得热——远距离信息发布的户外显示装备",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "显控与显示 · 14 个可复现工程算例 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
