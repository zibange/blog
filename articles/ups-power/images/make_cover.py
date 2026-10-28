# -*- coding: utf-8 -*-
"""UPS 不间断电源产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝渐变背景 + 机房机柜剪影 + 电池/能量光带
  2) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
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
random.seed(42)

# ---- 1. 深蓝渐变背景 ----
top = np.array([8, 20, 42], dtype=float)       # 顶部深蓝
bot = np.array([22, 50, 90], dtype=float)      # 底部稍亮
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 远景机房机柜剪影（两排，带点窗 LED）----
base_y = int(H * 0.74)
x = 0
while x < W:
    rw = random.randint(70, 130)
    rh = random.randint(int(H * 0.22), int(H * 0.40))
    d.rectangle([x, base_y - rh, x + rw, H], fill=(6, 14, 28, 170))
    # 机柜横向格栅 + LED 指示灯
    for sy in range(base_y - rh + 14, base_y - 10, 20):
        d.line([x + 8, sy, x + rw - 8, sy], fill=(30, 60, 100, 120), width=2)
        if random.random() < 0.30:
            lx = x + random.randint(10, max(11, rw - 16))
            col = random.choice([(90, 200, 160, 200), (120, 180, 240, 170), (240, 170, 90, 150)])
            d.ellipse([lx, sy - 5, lx + 6, sy + 1], fill=col)
    x += rw + random.randint(10, 30)

# ---- 3. 中景：蓄电池组与电缆剪影 ----
gy = base_y + int(H * 0.05)
# 三组电池（圆角矩形，顶部两个端子）
for bx in (int(W * 0.18), int(W * 0.34), int(W * 0.50)):
    d.rounded_rectangle([bx, gy - 70, bx + 110, gy], radius=10, fill=(12, 28, 52, 230))
    d.rectangle([bx + 18, gy - 82, bx + 34, gy - 70], fill=(70, 160, 255, 190))
    d.rectangle([bx + 76, gy - 82, bx + 92, gy - 70], fill=(70, 160, 255, 190))
    d.text((bx + 14, gy - 52), "+", fill=(90, 170, 240, 160))
# 连接电缆（折线）
d.line([(int(W * 0.235), gy - 30), (int(W * 0.28), gy - 10), (int(W * 0.34), gy - 30)],
       fill=(40, 90, 140, 210), width=6)
d.line([(int(W * 0.395), gy - 30), (int(W * 0.44), gy - 10), (int(W * 0.50), gy - 30)],
       fill=(40, 90, 140, 210), width=6)

# ---- 4. 能量光带（贝塞尔式弧线，表现电力流动）----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(6):
    y0 = base_y - 50 - i * 44
    pts = []
    for t in range(0, 101, 2):
        xx = W * t / 100
        yy = y0 - 66 * math.sin(math.pi * t / 100) * (0.6 + 0.08 * i)
        pts.append((xx, yy))
    gd.line(pts, fill=(70, 160, 255, 70 - i * 8), width=4)
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
img.paste(Image.new("RGB", (W, band_h), (5, 16, 30)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.65))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"
f_main = ImageFont.truetype(fy_bd, int(H * 0.058))
f_sub = ImageFont.truetype(fy, int(H * 0.0265))

mx, ty = int(W * 0.052), int(H * 0.700)
d.text((mx, ty), "UPS 不间断电源产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "整流、电池、逆变与旁路——把市电的不可靠挡在关键负载之外",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "供电与环境 · 14 个可复现工程算例 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
