# -*- coding: utf-8 -*-
"""周界警戒雷达产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝夜空渐变背景
  2. 雷达母题：中心雷达站 + 扇形扫描波束 + 同心距离环 + 目标光点 + 报警波纹
  3) 一台球机剪影做二次复核意象
  4) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
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

# 地面线位置
ground_y = int(H * 0.66)

# ---- 2. 雷达母题 ----
radar_cx, radar_cy = int(W * 0.46), ground_y - 30

# 同心距离环
for k in range(4):
    r = 120 + k * 110
    d.ellipse([radar_cx - r, radar_cy - r, radar_cx + r, radar_cy + r],
              outline=(90, 150, 230, 70 - k * 8), width=2)

# 扇形扫描波束（向上 120 度）
sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sweep)
sweep_color = (90, 200, 170, 60)
# 用多条射线近似扇形
for ang in range(30, 151, 4):
    a = math.radians(ang)
    ex = radar_cx + 470 * math.cos(a)
    ey = radar_cy - 470 * math.sin(a)
    sd.line([(radar_cx, radar_cy), (ex, ey)], fill=sweep_color, width=6)
sweep = sweep.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img.convert("RGBA"), sweep).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# 扫描前沿亮线（一条约 70 度的亮带）
front = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(front)
for ang in range(64, 77, 2):
    a = math.radians(ang)
    ex = radar_cx + 470 * math.cos(a)
    ey = radar_cy - 470 * math.sin(a)
    fd.line([(radar_cx, radar_cy), (ex, ey)], fill=(150, 240, 200, 150), width=7)
front = front.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img.convert("RGBA"), front).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# 雷达站（中心小塔）
d.ellipse([radar_cx - 16, radar_cy - 16, radar_cx + 16, radar_cy + 16], fill=(20, 30, 50, 230))
d.line([(radar_cx, radar_cy), (radar_cx, radar_cy - 70)], fill=(170, 210, 240, 230), width=6)
d.ellipse([radar_cx - 10, radar_cy - 80, radar_cx + 10, radar_cy - 60], fill=(170, 210, 240, 230))

# 目标光点（被扫描到的入侵目标）
for tx, ty, rr in [(radar_cx + 210, radar_cy - 150, 9), (radar_cx - 160, radar_cy - 230, 8)]:
    d.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=(240, 170, 90, 230))
    # 报警波纹
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    for i in range(3):
        a = 16 + i * 14
        hd.ellipse([tx - a, ty - a, tx + a, ty + a], outline=(240, 170, 90, 130 - i * 35), width=3)
    hl = hl.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img.convert("RGBA"), hl).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

# 地面线
d.line([(0, ground_y), (W, ground_y)], fill=(150, 200, 230, 200), width=3)

# 球机剪影（右侧，二次复核意象）
cam_x = int(W * 0.80)
cam_y = ground_y - 60
d.ellipse([cam_x - 26, cam_y - 26, cam_x + 26, cam_y + 26], fill=(30, 45, 75, 220))
d.rectangle([cam_x - 30, cam_y + 20, cam_x + 30, cam_y + 70], fill=(30, 45, 75, 220))
# 球机视锥
cone = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cone)
cd.polygon([(cam_x, cam_y), (cam_x - 180, ground_y), (cam_x + 60, ground_y)],
            fill=(120, 180, 240, 40))
cone = cone.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img.convert("RGBA"), cone).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 3. 底部渐隐深色带 + 标题 ----
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
d.text((mx, ty), "周界警戒雷达产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "毫米波扇形扫描，主动解算距离/方位/速度，联动球机二次复核——全天候大范围警戒带",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "周界安防 · 14 个工程算例 ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(OUT)
print("cover.png done", img.size)
