# -*- coding: utf-8 -*-
"""光纤光栅解调仪产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝科技渐变背景
  2. 光纤母题：一根光纤沿对角线延伸，刻写周期性布拉格光栅（光栅刻槽）
  3. 右侧光谱仪意象：反射谱的多个波长峰 (WDM 复用)
  4) 解调仪机箱剪影 + 信号光带
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
top = np.array([6, 16, 38], dtype=float)
bot = np.array([12, 30, 62], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 2. 光纤 + 布拉格光栅母题（对角线）----
# 光纤中心线
x0, y0 = int(W * 0.10), int(H * 0.78)
x1, y1 = int(W * 0.62), int(H * 0.30)
fiber_w = 22
# 画一条粗线表示光纤护套
d.line([(x0, y0), (x1, y1)], fill=(120, 170, 230, 150), width=fiber_w + 10)
d.line([(x0, y0), (x1, y1)], fill=(190, 220, 250, 220), width=fiber_w)

# 沿光纤方向刻写周期性布拉格光栅（垂直于光纤的短刻槽）
n_ticks = 26
for i in range(n_ticks):
    t = i / (n_ticks - 1)
    px = x0 + (x1 - x0) * t
    py = y0 + (y1 - y0) * t
    # 垂直光纤方向的法向量
    dx, dy = (x1 - x0), (y1 - y0)
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    half = fiber_w / 2 + 6
    d.line([(px + nx * half, py + ny * half), (px - nx * half, py - ny * half)],
           fill=(90, 200, 170, 200), width=4)

# ---- 3. 右侧光谱仪意象：反射谱多峰 (WDM 复用) ----
spec_x0, spec_y0 = int(W * 0.70), int(H * 0.18)
spec_w, spec_h = int(W * 0.26), int(H * 0.50)
# 坐标框
d.rectangle([spec_x0, spec_y0, spec_x0 + spec_w, spec_y0 + spec_h],
            outline=(120, 170, 230, 120), width=2)
# 基线
d.line([(spec_x0 + 6, spec_y0 + spec_h - 10), (spec_x0 + spec_w - 6, spec_y0 + spec_h - 10)],
       fill=(150, 200, 230, 150), width=2)
# 多个高斯峰（不同中心波长 = 不同光栅测点）
peaks = [0.12, 0.28, 0.44, 0.60, 0.76, 0.92]
for frac in peaks:
    cx = spec_x0 + 10 + frac * (spec_w - 20)
    amp = spec_h * 0.72
    # 画一个峰
    for k in range(-40, 41):
        xx = cx + k * (spec_w / 220.0)
        if xx < spec_x0 + 6 or xx > spec_x0 + spec_w - 6:
            continue
        g = amp * math.exp(-(k / 12.0) ** 2)
        yy = spec_y0 + spec_h - 10 - g
        d.point((xx, yy), fill=(90, 200, 170, 230))
# 标注
d.text((spec_x0 + 6, spec_y0 + 4), "反射光谱 (WDM 复用)", fill=(168, 212, 235, 220),
       font=ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", int(H * 0.020)))

# ---- 4. 解调仪机箱剪影（左下）----
bx, by, bw, bh = int(W * 0.06), int(H * 0.40), int(W * 0.20), int(H * 0.34)
d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=14, fill=(20, 34, 60, 230),
                    outline=(120, 170, 230, 160), width=3)
# 前面板指示灯/接口
for j in range(4):
    d.ellipse([bx + 24, by + 30 + j * 40, bx + 44, by + 50 + j * 40], fill=(90, 200, 170, 220))
d.rectangle([bx + bw - 60, by + 30, bx + bw - 24, by + 70], fill=(10, 22, 44, 230),
            outline=(120, 170, 230, 160), width=2)
d.text((bx + 16, by + bh - 36), "解调仪", fill=(190, 220, 250, 230),
       font=ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", int(H * 0.022)))

# 信号光带：解调仪 -> 光谱（连线）
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.line([(bx + bw, by + bh / 2), (spec_x0, spec_y0 + spec_h / 2)], fill=(150, 220, 200, 70), width=5)
glow = glow.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

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
d.text((mx, ty), "光纤光栅解调仪产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "宽带光扫描光栅阵，解析布拉格波长漂移，1 pm 分辨率换算温度/应变——准分布式传感主机",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "光纤传感 · 14 个工程算例 ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
