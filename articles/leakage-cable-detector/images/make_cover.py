# -*- coding: utf-8 -*-
"""泄漏电缆入侵探测器产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝夜空渐变背景
  2. 隐形周界母题：地表线下方两条平行泄漏电缆（LCX），向外辐射出淡蓝/淡绿电磁场晕
  3. 一个入侵者剪影扰动场，场晕在此处变形/高亮，表现「扰动即报警」
  4. 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
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

# ---- 1. 深蓝夜空渐变背景 ----
top = np.array([6, 16, 38], dtype=float)
bot = np.array([14, 34, 66], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# 地表线位置
ground_y = int(H * 0.62)

# ---- 2. 两条平行泄漏电缆 + 辐射场晕 ----
cable_colors = [(90, 170, 240, 90), (90, 220, 170, 80)]
cable_ys = [ground_y + 70, ground_y + 110]  # 地下两条
for k, cy in enumerate(cable_ys):
    # 辐射场晕：在电缆两侧用半透明径向晕
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for x in range(0, W, 26):
        for off in (-1, 1):
            gx = x
            gy = cy + off * 26
            r = 60
            gd.ellipse([gx - r, gy - r, gx + r, gy + r],
                       fill=cable_colors[k][:3] + (18,))
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    # 电缆本体
    d.line([(0, cy), (W, cy)], fill=cable_colors[k], width=4)

# 地表线
d.line([(0, ground_y), (W, ground_y)], fill=(150, 200, 230, 200), width=3)

# 地面以上淡淡的草坪/边界示意（点状）
for x in range(40, W, 36):
    d.ellipse([x, ground_y - 6, x + 6, ground_y], fill=(90, 170, 130, 120))

# ---- 3. 入侵者剪影扰动场（在两条电缆之间中段）----
px, py = int(W * 0.50), ground_y - 4  # 站在地表、脚踩灵敏区
# 人体剪影（简化）：头+身+两腿
d.ellipse([px - 16, py - 150, px + 16, py - 118], fill=(20, 30, 50, 220))  # 头
d.line([(px, py - 120), (px, py - 50)], fill=(20, 30, 50, 220), width=22)   # 身
d.line([(px, py - 52), (px - 18, py)], fill=(20, 30, 50, 220), width=16)    # 左腿
d.line([(px, py - 52), (px + 18, py)], fill=(20, 30, 50, 220), width=16)    # 右腿
# 扰动高亮：在入侵者脚下画一圈高亮场畸变
hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
for i in range(5):
    rr = 40 + i * 16
    hd.ellipse([px - rr, ground_y + 30 - rr * 0.6, px + rr, ground_y + 30 + rr * 0.6],
               outline=(240, 170, 90, 150 - i * 25), width=3)
hl = hl.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img.convert("RGBA"), hl).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# 报警波纹（从入侵者向外扩散的弧）
for i in range(3):
    a = 70 + i * 34
    d.arc([px - a, py - a, px + a, py + a], start=20, end=160,
          fill=(240, 170, 90, 130 - i * 35), width=3)

# ---- 4. 底部渐隐深色带 + 标题 ----
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
d.text((mx, ty), "泄漏电缆入侵探测器产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "收发电缆间形成隐形电磁场，人员扰动即报警——埋地/贴墙隐形周界，视觉不可见",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "周界安防 · 14 个工程算例 ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
