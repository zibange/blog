# -*- coding: utf-8 -*-
"""访客管理系统产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝渐变背景 + 城市天际线/闸机通道剪影 + 数据光带
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
top = np.array([10, 22, 44], dtype=float)      # 顶部深蓝
bot = np.array([24, 52, 92], dtype=float)      # 底部稍亮
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 远景城市天际线剪影（更暗一层）----
base_y = int(H * 0.72)
x = 0
while x < W:
    bw = random.randint(60, 160)
    bh = random.randint(int(H * 0.10), int(H * 0.34))
    d.rectangle([x, base_y - bh, x + bw, H], fill=(6, 14, 28, 160))
    # 楼体点窗
    for wx in range(x + 10, x + bw - 10, 22):
        for wy in range(base_y - bh + 12, base_y - 8, 26):
            if random.random() < 0.18:
                d.rectangle([wx, wy, wx + 6, wy + 9], fill=(120, 180, 240, 70))
    x += bw + random.randint(6, 26)

# ---- 3. 中景闸机通道剪影（左右对称的翼闸）----
gy = base_y + int(H * 0.06)
for cx in (int(W * 0.30), int(W * 0.50), int(W * 0.70)):
    # 闸机立柱
    d.rounded_rectangle([cx - 14, gy - 90, cx + 14, gy], radius=8, fill=(16, 34, 60, 220))
    d.ellipse([cx - 8, gy - 98, cx + 8, gy - 82], fill=(90, 200, 160, 200))
    # 翼门（斜向短线）
    d.polygon([(cx - 12, gy - 60), (cx - 70, gy - 30), (cx - 70, gy - 22), (cx - 12, gy - 48)], fill=(40, 90, 140, 200))
    d.polygon([(cx + 12, gy - 60), (cx + 70, gy - 30), (cx + 70, gy - 22), (cx + 12, gy - 48)], fill=(40, 90, 140, 200))

# ---- 4. 数据光带（贝塞尔式弧线）----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(6):
    y0 = base_y - 40 - i * 46
    pts = []
    for t in range(0, 101, 2):
        xx = W * t / 100
        yy = y0 - 70 * math.sin(math.pi * t / 100) * (0.6 + 0.08 * i)
        pts.append((xx, yy))
    gd.line(pts, fill=(70, 160, 255, 70 - i * 8), width=4)
glow = glow.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 5. 访客/行人剪影（迎面走来的两个抽象人形）----
for px, ph, alpha in ((int(W * 0.42), 150, 200), (int(W * 0.58), 130, 170)):
    py = gy + 6
    hd = int(ph * 0.16)
    d.ellipse([px - hd // 2, py - ph, px + hd // 2, py - ph + hd], fill=(10, 20, 38, alpha))
    d.polygon([(px - int(ph * 0.16), py - ph + hd + 6), (px + int(ph * 0.16), py - ph + hd + 6),
               (px + int(ph * 0.10), py - int(ph * 0.30)), (px - int(ph * 0.10), py - int(ph * 0.30))],
              fill=(10, 20, 38, alpha))
    d.line([px, py - int(ph * 0.32), px - int(ph * 0.13), py], fill=(10, 20, 38, alpha), width=10)
    d.line([px, py - int(ph * 0.32), px + int(ph * 0.13), py], fill=(10, 20, 38, alpha), width=10)

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save(RAW)
print("cover_raw.png done", img.size)

# ---- 6. 底部渐隐深色带 + 标题（与既有封面流程一致）----
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
d.text((mx, ty), "访客管理系统产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "把身份核验、权限发放与轨迹留痕串成一条有时空边界、可追溯的临时通行链路",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "出入口控制 · 14 个可复现工程算例 ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
