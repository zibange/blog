# -*- coding: utf-8 -*-
"""信息发布终端产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝夜空渐变背景
  2) 信息分发母题：左上中心节点（CMS）经光带向右下多块「屏幕」扇出内容
  3) 屏幕内含内容条块与光点，表现「按排期播放」
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
random.seed(23)

# ---- 1. 深蓝夜空渐变背景 ----
top = np.array([6, 16, 38], dtype=float)
bot = np.array([14, 34, 66], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 信息分发母题 ----
# 左上中心节点（CMS）
cx, cy = int(W * 0.18), int(H * 0.20)

# 右下多块屏幕（错落矩形）
screens = [
    (0.52, 0.58, 0.20, 0.13),
    (0.76, 0.46, 0.16, 0.10),
    (0.66, 0.74, 0.18, 0.12),
    (0.88, 0.68, 0.14, 0.09),
    (0.40, 0.78, 0.13, 0.09),
]
scr_px = [(int(W * x), int(H * y), int(W * w), int(H * h)) for (x, y, w, h) in screens]

cblue = (90, 170, 240, 80)
cgreen = (90, 220, 170, 70)
corange = (240, 170, 90, 70)

# 中心到各屏的光带连线
for (sx, sy, sw, sh) in scr_px:
    tx, ty = sx + sw // 2, sy + sh // 2
    # 折线：先水平后斜向，形成「分发」感
    midx = cx + (tx - cx) // 2
    d.line([(cx, cy), (midx, cy)], fill=cblue, width=2)
    d.line([(midx, cy), (tx, ty)], fill=cgreen, width=2)
    # 端点光点
    d.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=(140, 220, 255, 190))

# 中心节点：双环 + 内核
d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=(90, 170, 240, 200), width=3)
d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=(90, 170, 240, 140), width=2)
d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(120, 200, 255, 220))

# 屏幕矩形：外框 + 内部内容条块（标题条 + 两行正文 + 高亮块）
for (sx, sy, sw, sh) in scr_px:
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8,
                        outline=(120, 200, 255, 170), width=3)
    pad = max(6, sw // 14)
    # 标题条
    d.rounded_rectangle([sx + pad, sy + pad, sx + sw - pad, sy + pad + sh // 5],
                        radius=4, fill=(90, 170, 240, 110))
    # 正文两行
    y1 = sy + pad + sh // 5 + pad
    d.rounded_rectangle([sx + pad, y1, sx + sw * 0.72, y1 + sh // 8],
                        radius=3, fill=(200, 220, 240, 80))
    y2 = y1 + sh // 8 + pad // 2
    d.rounded_rectangle([sx + pad, y2, sx + sw * 0.55, y2 + sh // 8],
                        radius=3, fill=(200, 220, 240, 60))
    # 高亮块（右下）
    d.rounded_rectangle([sx + sw * 0.55, sy + sh * 0.62, sx + sw - pad, sy + sh - pad],
                        radius=4, fill=(90, 220, 170, 90))

# ---- 3. 能量光带（信号流动）----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(4):
    y0 = H * (0.24 + 0.12 * i)
    pts = []
    for t in range(0, 101, 2):
        xx = W * t / 100
        yy = y0 - 30 * math.sin(math.pi * t / 100) * (0.6 + 0.08 * i)
        pts.append((xx, yy))
    gd.line(pts, fill=(90, 170, 255, 50 - i * 8), width=4)
glow = glow.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

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
d.text((mx, ty), "信息发布终端产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "工控播放器+显示屏+CMS 按排期自动播放、集中运维——营业厅/电梯厅/门店的边缘内容节点",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "显控与显示 · 14 个工程算例 ｜ 58 处公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
