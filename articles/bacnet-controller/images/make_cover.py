# -*- coding: utf-8 -*-
"""BACnet 楼宇控制器产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印、无文字）：
  1) 深蓝科技渐变背景 + 稀疏星点
  2) 中部暖通空调机组（AHU）剖视剪影（表冷器盘管 + 风阀 + 风机）
  3) 右侧楼宇剖面多层剪影（各层挂 BACnet 对象节点光点）
  4) 从现场设备到楼层的对象数据光带（AI/AO/COV）
  5) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
输出：cover_raw.png（底图）与 cover.png（成片）

Python 教学要点：
  - np.linspace / np.repeat：构造纵向渐变数组，再沿宽度方向复制；
  - ImageDraw.Draw(img,"RGBA")：在 RGB 图上叠加半透明图形（第四通道 alpha）；
  - Image.alpha_composite：把带透明通道的光带图层合成到底图；
  - GaussianBlur：对光带做柔化，营造发光效果；
  - ImageFont.truetype：加载微软雅黑字体渲染中文标题。
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "cover_raw.png")
OUT = os.path.join(HERE, "cover.png")

W, H = 1536, 1024

# ---- 1. 深蓝科技渐变背景 ----
top = np.array([5, 14, 34], dtype=float)
bot = np.array([12, 32, 60], dtype=float)
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# 稀疏星点（固定随机种子，保证可复现）
rng = np.random.default_rng(135)
for _ in range(150):
    sx = int(rng.integers(0, W))
    sy = int(rng.integers(0, int(H * 0.6)))
    r = int(rng.integers(1, 3))
    a = int(rng.integers(20, 70))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 195, 240, a))

# ---- 2. 中部 AHU 空调机组剖视剪影 ----
ax, ay = int(W * 0.30), int(H * 0.40)
aw, ah = 300, 220
d.rounded_rectangle([ax - aw // 2, ay - ah // 2, ax + aw // 2, ay + ah // 2],
                    radius=14, fill=(14, 34, 62, 255), outline=(95, 155, 215, 220), width=3)
# 表冷器盘管（蛇形折线）+ 风阀叶片 + 风机圆
for k in range(6):
    yy = ay - ah // 2 + 30 + k * 18
    d.line([(ax - aw // 2 + 24, yy), (ax - aw // 2 + 130, yy)],
           fill=(90, 150, 210, 120), width=3)
d.line([(ax - aw // 2 + 170, ay - 50), (ax - aw // 2 + 170, ay + 50)],
       fill=(120, 205, 245, 200), width=4)
for k in range(3):
    d.line([(ax - aw // 2 + 158, ay - 40 + k * 40),
            (ax - aw // 2 + 182, ay - 30 + k * 40)], fill=(120, 205, 245, 180), width=3)
fanx, fany = ax + aw // 2 - 55, ay
d.ellipse([fanx - 34, fany - 34, fanx + 34, fany + 34],
          outline=(120, 225, 190, 220), width=3)
for k in range(4):
    a0 = k * 1.57
    d.line([(fanx, fany), (fanx + 28 * np.cos(a0), fany + 28 * np.sin(a0))],
           fill=(120, 225, 190, 200), width=3)

# ---- 3. 右侧楼宇剖面多层剪影 ----
bx, by = int(W * 0.78), int(H * 0.40)
bw, bh = 240, 400
d.rounded_rectangle([bx - bw // 2, by - bh // 2, bx + bw // 2, by + bh // 2],
                    radius=12, fill=(16, 38, 70, 255), outline=(95, 155, 215, 220), width=3)
for k in range(6):
    yy = by - bh // 2 + 18 + k * 64
    d.line([(bx - bw // 2 + 10, yy), (bx + bw // 2 - 10, yy)],
           fill=(70, 120, 170, 180), width=2)
    # 每层挂 3 个 BACnet 对象节点光点（AI/AO/COV）
    for j in range(3):
        nx = bx - bw // 2 + 40 + j * 70
        on = (k + j) % 3 != 0
        col = (120, 235, 190, 235) if on else (70, 105, 140, 120)
        d.ellipse([nx - 5, yy + 26, nx + 5, yy + 36], fill=col)

# ---- 4. 现场设备 ↔ 楼层 对象数据光带（AI/AO/COV）----
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
x0, x1 = ax + aw // 2, bx - bw // 2
for k in range(9):
    y_off = ay - 70 + k * 18
    bd.line([(x0, y_off), (x1, by - 100 + k * 22)],
            fill=(90, 195, 245, 46 - k * 4), width=5)
for k in range(6):
    nx = x0 + (x1 - x0) * (k + 1) / 7
    ny = ay - 50 + k * 24
    bd.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(150, 225, 200, 190))
beams = beams.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img.convert("RGBA"), beams).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 5. 底部渐隐深色带 + 标题 ----
band_h = int(H * 0.42)
band_y = H - band_h
band = Image.new("L", (W, band_h))
dband = ImageDraw.Draw(band)
for i in range(band_h):
    a = int(28 + 205 * (i / band_h) ** 1.35)
    dband.line([(0, i), (W, i)], fill=a)
img.paste(Image.new("RGB", (W, band_h), (4, 12, 26)), (0, band_y), band)
img = img.filter(ImageFilter.GaussianBlur(0.65))

d = ImageDraw.Draw(img)
fy = r"C:\Windows\Fonts\msyh.ttc"
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"
f_main = ImageFont.truetype(fy_bd, int(H * 0.058))
f_sub = ImageFont.truetype(fy, int(H * 0.025))

mx, ty = int(W * 0.052), int(H * 0.700)
d.text((mx, ty), "BACnet 楼宇控制器产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "不同厂家的空调与机电设备，在同一套标准对象里对话——开放、可互操作、不被锁死",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "中央控制 · 14 个工程算例（编址 / 令牌 / COV / 优先级 / BBMD / 安全 / BIBB） ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0215)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
