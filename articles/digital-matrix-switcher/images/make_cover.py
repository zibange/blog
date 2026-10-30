# -*- coding: utf-8 -*-
"""数字矩阵切换器产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝夜空渐变背景
  2) 交叉点路由母题：左侧多路输入线汇聚到中部交叉点网格、再扇出到右侧多屏
  3) 信号光点与流动光带表现「任意路由」
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
random.seed(11)

# ---- 1. 深蓝夜空渐变背景 ----
top = np.array([6, 16, 38], dtype=float)
bot = np.array([14, 34, 66], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 交叉点路由母题 ----
# 左侧输入端口（垂直排列的小光点）
sx0 = int(W * 0.06)
sy0, sy1 = int(H * 0.20), int(H * 0.78)
inputs = 7
in_pts = [(sx0, sy0 + (sy1 - sy0) * i / (inputs - 1)) for i in range(inputs)]

# 中部交叉点网格
gx0, gy0 = int(W * 0.42), int(H * 0.18)
gx1, gy1 = int(W * 0.58), int(H * 0.82)

# 右侧输出端口
ox0 = int(W * 0.94)
outputs = 9
out_pts = [(ox0, sy0 + (sy1 - sy0) * i / (outputs - 1)) for i in range(outputs)]

# 画交叉连线（输入 -> 中部 -> 输出），只画部分避免过密
cblue = (90, 170, 240, 70)
cgreen = (90, 220, 170, 60)
for (ix, iy) in in_pts:
    mxi = gx0 + random.uniform(0, gx1 - gx0)
    myi = gy0 + random.uniform(0, gy1 - gy0)
    d.line([(ix, iy), (mxi, myi)], fill=cblue, width=2)
    (ox, oy) = random.choice(out_pts)
    mox = gx1 - random.uniform(0, gx1 - gx0)
    moy = gy0 + random.uniform(0, gy1 - gy0)
    d.line([(mox, moy), (ox, oy)], fill=cgreen, width=2)

# 交叉点网格节点
for i in range(5):
    for j in range(7):
        cx = gx0 + (gx1 - gx0) * (i + 0.5) / 5
        cy = gy0 + (gy1 - gy0) * (j + 0.5) / 7
        r = random.choice([3, 4])
        a = random.randint(90, 200)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 200, 255, a))

# 中部高亮框
d.rounded_rectangle([gx0 - 16, gy0 - 16, gx1 + 16, gy1 + 16], radius=14,
                    outline=(90, 170, 240, 150), width=3)

# 输入/输出端口小方块
for (ix, iy) in in_pts:
    d.rounded_rectangle([ix - 10, iy - 8, ix + 10, iy + 8], radius=4, fill=(70, 160, 255, 170))
for (ox, oy) in out_pts:
    d.rounded_rectangle([ox - 10, oy - 8, ox + 10, oy + 8], radius=4, fill=(90, 220, 170, 170))

# ---- 3. 能量光带（信号流动）----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(4):
    y0 = H * (0.28 + 0.12 * i)
    pts = []
    for t in range(0, 101, 2):
        xx = W * t / 100
        yy = y0 - 30 * math.sin(math.pi * t / 100) * (0.6 + 0.08 * i)
        pts.append((xx, yy))
    gd.line(pts, fill=(90, 170, 255, 50 - i * 8), width=4)
glow = glow.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save(RAW)
print("cover_raw.png done", img.size)

# ---- 4. 底部渐隐深色带 + 标题（与既有封面流程一致）----
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
d.text((mx, ty), "数字矩阵切换器产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "交叉点硬件路由、零解码、微秒级切换——指挥大厅与会议室的多源多屏视听中枢",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "显控与显示 · 14 个可复现工程算例 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
