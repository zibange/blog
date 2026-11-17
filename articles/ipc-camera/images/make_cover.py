# -*- coding: utf-8 -*-
"""网络摄像机（IPC）产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印，无文字）：
  1) 深蓝科技渐变背景
  2) 左侧摄像机枪机剪影 + 镜头
  3) 镜头发出的锥形视场光带，投射到远处
  4) 视场内四个 DORI 目标光点（近清远糊的层次）
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
bot = np.array([11, 30, 62], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# 稀疏星点/噪点纹理
rng = np.random.default_rng(11)
for _ in range(160):
    sx = int(rng.integers(0, W))
    sy = int(rng.integers(0, int(H * 0.62)))
    r = int(rng.integers(1, 3))
    a = int(rng.integers(20, 70))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 200, 240, a))

# ---- 2. 摄像机枪机剪影（左中部）----
cam_x, cam_y = int(W * 0.20), int(H * 0.40)
# 机身（圆角矩形）
d.rounded_rectangle([cam_x - 150, cam_y - 78, cam_x + 120, cam_y + 78],
                    radius=26, fill=(18, 40, 74, 255), outline=(90, 150, 210, 200), width=3)
# 上盖高光
d.rounded_rectangle([cam_x - 150, cam_y - 78, cam_x + 120, cam_y - 40],
                    radius=20, fill=(30, 62, 104, 220))
# 镜头（同心圆）
for r, col in [(74, (70, 130, 190, 210)), (58, (16, 34, 60, 255)),
               (44, (90, 170, 225, 230)), (30, (10, 24, 46, 255)),
               (16, (150, 220, 255, 245))]:
    d.ellipse([cam_x + 120 - r, cam_y - r, cam_x + 120 + r, cam_y + r], fill=col)
# 镜头高光点
d.ellipse([cam_x + 150, cam_y - 30, cam_x + 170, cam_y - 10], fill=(225, 245, 255, 235))
# 支架
d.rounded_rectangle([cam_x - 30, cam_y + 78, cam_x + 10, cam_y + 165],
                    radius=8, fill=(16, 36, 66, 255), outline=(70, 120, 175, 180), width=2)

# ---- 3. 视场锥形光带（镜头射向右侧远方）----
apex_x, apex_y = cam_x + 190, cam_y
cone = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cone)
far_x = int(W * 0.92)
cone_half_near, cone_half_far = 26, 300
# 多层半透明三角，叠加出光锥
for k in range(6):
    alpha = 14 - k * 2
    cd.polygon([(apex_x, apex_y - cone_half_near // 2),
                (far_x, apex_y - cone_half_far + k * 36),
                (far_x, apex_y + cone_half_far - k * 36),
                (apex_x, apex_y + cone_half_near // 2)],
               fill=(90, 180, 235, alpha))
# 视场上下边界线
cd.line([(apex_x, apex_y - cone_half_near // 2), (far_x, apex_y - cone_half_far)],
        fill=(120, 205, 250, 150), width=2)
cd.line([(apex_x, apex_y + cone_half_near // 2), (far_x, apex_y + cone_half_far)],
        fill=(120, 205, 250, 150), width=2)
cone = cone.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img.convert("RGBA"), cone).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 4. 视场内四个 DORI 目标光点（越远越暗越小）----
targets = [(0.42, 0.40, 26, (120, 235, 205)),
           (0.58, 0.52, 20, (120, 200, 245)),
           (0.72, 0.44, 14, (170, 200, 240)),
           (0.85, 0.56, 9, (190, 205, 230))]
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for fx, fy, r, col in targets:
    tx, ty = int(W * fx), int(H * fy)
    for rr in range(r * 3, 0, -max(2, r // 4)):
        gd.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=(*col, 10))
    gd.ellipse([tx - r // 2, ty - r // 2, tx + r // 2, ty + r // 2], fill=(*col, 220))
glow = glow.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

# ---- 5. 底部渐隐深色带 + 标题 ----
band_h = int(H * 0.42)
band_y = H - band_h
band = Image.new("L", (W, band_h))
db = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(28 + 205 * (i / band_h) ** 1.35)
    db.line([(0, i), (W, i)], fill=a)
img.paste(Image.new("RGB", (W, band_h), (4, 12, 26)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.65))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"
f_main = ImageFont.truetype(fy_bd, int(H * 0.058))
f_sub = ImageFont.truetype(fy, int(H * 0.0265))

mx, ty = int(W * 0.052), int(H * 0.700)
d.text((mx, ty), "网络摄像机（IPC）产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "前端完成取像、处理、编码与网络输出——整个视频监控系统取像的第一环节",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "视频物联 · 14 个工程算例（DORI / 码率 / PoE）｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
