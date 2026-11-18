# -*- coding: utf-8 -*-
"""视频存储服务器产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印、无文字）：
  1) 深蓝科技渐变背景 + 稀疏星点
  2) 左侧机架式存储服务器剪影（多盘位机箱 + 一排硬盘指示灯）
  3) 矩阵式磁盘阵列格（象征 RAID / 纠删码资源池）
  4) 右侧汇入的数据光带（象征多路码流写入）与冗余环（象征自愈）
  5) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
输出：cover_raw.png（底图）与 cover.png（成片）
"""
import os                                    # 拼接路径
import numpy as np                           # 数组与渐变计算
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # 图像绘制

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "cover_raw.png")
OUT = os.path.join(HERE, "cover.png")

W, H = 1536, 1024

# ---- 1. 深蓝科技渐变背景 ----
top = np.array([5, 14, 34], dtype=float)     # 顶部深蓝
bot = np.array([11, 30, 62], dtype=float)    # 底部略亮
grad = np.linspace(0, 1, H)[:, None, None]   # H×1×1 的 0~1 渐变权重
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)              # 沿宽度复制成 W×H×3
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# 稀疏星点/噪点纹理（固定随机种子，保证每次生成一致）
rng = np.random.default_rng(20)
for _ in range(170):
    sx = int(rng.integers(0, W))
    sy = int(rng.integers(0, int(H * 0.62)))
    r = int(rng.integers(1, 3))
    a = int(rng.integers(20, 70))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 195, 240, a))

# ---- 2. 机架式存储服务器剪影（左中部）----
rx, ry = int(W * 0.21), int(H * 0.40)
# 机箱外壳
d.rounded_rectangle([rx - 190, ry - 150, rx + 170, ry + 150],
                    radius=18, fill=(18, 40, 74, 255), outline=(90, 150, 210, 210), width=3)
# Top 高光条
d.rounded_rectangle([rx - 190, ry - 150, rx + 170, ry - 118],
                    radius=10, fill=(32, 66, 110, 230))
# 一排硬盘托架（6 行 × 每行盘位 + 指示灯）
row_h, disk_w = 38, 300
for row in range(5):
    yy = ry - 100 + row * 44
    d.rounded_rectangle([rx - 168, yy, rx + disk_w - 168, yy + row_h],
                        radius=6, fill=(12, 30, 56, 255), outline=(70, 125, 180, 170), width=1)
    # 盘位分隔竖线
    for k in range(1, 6):
        xx = rx - 168 + k * (disk_w / 6)
        d.line([(xx, yy + 4), (xx, yy + row_h - 4)], fill=(55, 100, 150, 140), width=1)
    # 硬盘活动指示灯（绿色/蓝色交替）
    led_col = (120, 235, 190, 230) if row % 2 == 0 else (110, 185, 245, 230)
    d.ellipse([rx + disk_w - 168 - 16, yy + 14, rx + disk_w - 168 - 6, yy + 24], fill=led_col)

# ---- 3. 右侧矩阵式磁盘阵列格（象征资源池 / 纠删码分布）----
gx0, gy0 = int(W * 0.55), int(H * 0.20)
cell, gap = 34, 12
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for r in range(6):
    for c in range(9):
        xx = gx0 + c * (cell + gap)
        yy = gy0 + r * (cell + gap)
        # 少量格子高亮成数据块/校验块
        is_parity = (r + c) % 5 == 0
        col = (90, 170, 235, 70) if not is_parity else (120, 235, 195, 150)
        gd.rounded_rectangle([xx, yy, xx + cell, yy + cell], radius=5,
                             fill=col, outline=(120, 190, 240, 90), width=1)
grid = grid.filter(ImageFilter.GaussianBlur(0.4))
img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 4. 汇入的数据光带（多路码流从右向左写入阵列）----
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
for k in range(7):
    y_off = gy0 + 20 + k * 62
    alpha = 30 - k * 2
    bd.line([(W - 30, y_off), (gx0 + 40, gy0 + 150)],
            fill=(90, 190, 240, alpha), width=6)
beams = beams.filter(ImageFilter.GaussianBlur(7))
img = Image.alpha_composite(img.convert("RGBA"), beams).convert("RGB")

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
fy = r"C:\Windows\Fonts\msyh.ttc"           # 微软雅黑常规
fy_bd = r"C:\Windows\Fonts\msyhbd.ttc"      # 微软雅黑粗体
f_main = ImageFont.truetype(fy_bd, int(H * 0.058))
f_sub = ImageFont.truetype(fy, int(H * 0.0265))

mx, ty = int(W * 0.052), int(H * 0.700)
d.text((mx, ty), "视频存储服务器产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "磁盘阵列承载大规模并发写入与长期留存，以冗余与可运维性撑起视频后端底座",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "视频物联 · 14 个工程算例（容量 / 带宽 / 纠删码 / 分层） ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0225)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
