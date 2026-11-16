# -*- coding: utf-8 -*-
"""光时域反射仪（OTDR）产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝科技渐变背景
  2) 一条光纤沿画面延伸，略有弯折（暗示链路）
  3) OTDR 发出的脉冲光点沿光纤传播，尾部拖出背向散射回波光带
  4) 右侧叠一条「功率—距离」背向散射曲线示意（下降 + 台阶 + 尖峰 + 断点骤降）
  5) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
输出：cover_raw.png（底图）与 cover.png（成片）
"""
import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "cover_raw.png")
OUT = os.path.join(HERE, "cover.png")

W, H = 1536, 1024

# ---- 1. 深蓝科技渐变背景 ----
top = np.array([5, 14, 34], dtype=float)
bot = np.array([11, 28, 58], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 光纤主干（一条略带弯折的曲线，从左下延伸到右侧）----
def fiber_y(x):
    # 平滑正弦缓弯，模拟敷设光缆
    return int(H * 0.42 + 70 * math.sin((x / W) * math.pi * 1.3))

pts = [(x, fiber_y(x)) for x in range(0, W, 6)]
d.line(pts, fill=(90, 140, 200, 90), width=34)      # 外圈光晕
d.line(pts, fill=(150, 205, 245, 200), width=16)    # 纤芯
d.line(pts, fill=(215, 238, 255, 235), width=5)     # 高光芯

# ---- 3. 发射脉冲光点 + 背向散射回波光带 ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
px = int(W * 0.34)
py = fiber_y(px)
# 入射脉冲亮点
for r in range(60, 0, -6):
    gd.ellipse([px - r, py - r, px + r, py + r], fill=(120, 220, 255, 12))
gd.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(220, 250, 255, 235))
# 回波：从亮点向右沿光纤拖出渐弱的光带
for x in range(px, int(W * 0.92), 6):
    yy = fiber_y(x)
    t = (x - px) / (W * 0.92 - px)
    a = int(150 * (1 - t) ** 1.6)
    gd.line([(x, yy - 3), (x, yy + 3)], fill=(120, 255, 215, max(a, 0)), width=3)
glow = glow.filter(ImageFilter.GaussianBlur(7))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 4. 右侧背向散射曲线示意（功率随距离下降 + 事件）----
sx0, sy0 = int(W * 0.60), int(H * 0.14)
sw, sh = int(W * 0.36), int(H * 0.42)
d.rectangle([sx0, sy0, sx0 + sw, sy0 + sh], outline=(120, 170, 230, 90), width=2)
base_y = sy0 + sh - 16
d.line([(sx0 + 8, base_y), (sx0 + sw - 8, base_y)], fill=(150, 200, 230, 120), width=2)
# 下降曲线
curve_pts = []
for i in range(160):
    t = i / 159
    xx = sx0 + 8 + t * (sw - 16)
    yy = sy0 + 20 + t * (sh * 0.62)
    curve_pts.append((xx, yy))
d.line(curve_pts, fill=(90, 200, 170, 210), width=3)
# 一个菲涅尔尖峰
sp = sx0 + int(sw * 0.45)
d.line([(sp - 4, curve_pts[70][1] + 46), (sp, sy0 + 24), (sp + 4, curve_pts[72][1] + 46)],
       fill=(255, 190, 90, 230), width=3)
# 末端断点骤降
ep = sx0 + sw - 30
d.line([(ep, curve_pts[150][1]), (ep, base_y)], fill=(255, 120, 110, 220), width=3)
d.text((sx0 + 8, sy0 + 4), "背向散射曲线 / 事件定位", fill=(168, 212, 235, 210),
       font=ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", int(H * 0.019)))

# ---- 5. 底部渐隐深色带 + 标题 ----
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
d.text((mx, ty), "光时域反射仪（OTDR）产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "单端注入脉冲，读背向散射曲线，测衰减、熔接损耗、宏弯与断点——光缆链路体检仪",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "光纤传感 · 14 个工程算例 ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
