# -*- coding: utf-8 -*-
"""电梯楼层控制器产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印、无文字）：
  1) 深蓝科技渐变背景 + 稀疏星点
  2) 中部电梯轿厢剖视剪影（带楼层按键COP面板）
  3) 左侧刷卡/读头光点 + 权限光带连向轿厢
  4) 右侧竖向楼层刻度条 + 授权层高亮（未授权层灰暗）
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
bot = np.array([12, 32, 60], dtype=float)    # 底部略亮
grad = np.linspace(0, 1, H)[:, None, None]
arr = top[None, None, :] * (1 - grad) + bot[None, None, :] * grad
arr = np.repeat(arr, W, axis=1)
img = Image.fromarray(arr.astype("uint8"), "RGB")
d = ImageDraw.Draw(img, "RGBA")

# 稀疏星点（固定随机种子，保证可复现）
rng = np.random.default_rng(31)
for _ in range(150):
    sx = int(rng.integers(0, W))
    sy = int(rng.integers(0, int(H * 0.6)))
    r = int(rng.integers(1, 3))
    a = int(rng.integers(20, 70))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 195, 240, a))

# ---- 2. 中部电梯轿厢剖视剪影 + COP 面板 ----
cx, cy = int(W * 0.46), int(H * 0.40)
cw, ch = 300, 430
# 轿厢外框
d.rounded_rectangle([cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2],
                    radius=22, fill=(16, 38, 70, 255), outline=(95, 155, 215, 220), width=3)
# 轿门中缝
d.line([(cx, cy - ch // 2 + 20), (cx, cy + ch // 2 - 20)],
       fill=(70, 125, 180, 150), width=3)
# 顶部指示灯
d.rounded_rectangle([cx - 60, cy - ch // 2 + 18, cx + 60, cy - ch // 2 + 44],
                    radius=8, fill=(30, 66, 110, 230))
d.text((cx + 28, cy - ch // 2 + 31), "8", fill=(150, 225, 200, 255))
# COP 楼层按键面板（轿厢右侧内壁）
px, py = cx + cw // 2 - 78, cy - 60
d.rounded_rectangle([px, py, px + 58, py + 190],
                    radius=10, fill=(10, 26, 50, 255), outline=(95, 155, 215, 200), width=2)
for k in range(5):
    on = k in (2, 3)   # 授权层高亮
    col = (120, 235, 190, 235) if on else (70, 105, 140, 130)
    yy = py + 14 + k * 34
    d.rounded_rectangle([px + 12, yy, px + 46, yy + 24],
                        radius=6, fill=(16, 40, 72, 255), outline=col, width=2)

# ---- 3. 左侧读头刷卡光点 + 权限光带 ----
hx, hy = int(W * 0.16), int(H * 0.40)
d.rounded_rectangle([hx - 34, hy - 46, hx + 34, hy + 46],
                    radius=12, fill=(20, 44, 80, 255), outline=(95, 155, 215, 220), width=3)
d.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=(120, 205, 245, 210))
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
bx0, bx1 = hx + 44, cx - cw // 2
for k in range(7):
    y_off = hy - 70 + k * 24
    bd.line([(bx0, y_off), (bx1, cy - 40 + k * 14)],
            fill=(90, 195, 245, 42 - k * 4), width=5)
for k in range(5):
    nx = bx0 + (bx1 - bx0) * (k + 1) / 6
    ny = hy - 60 + k * 28
    bd.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(150, 225, 200, 190))
beams = beams.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img.convert("RGBA"), beams).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 4. 右侧竖向楼层刻度条（授权层高亮）----
fx = int(W * 0.80)
d.rounded_rectangle([fx - 30, int(H * 0.16), fx + 30, int(H * 0.62)],
                    radius=12, fill=(16, 38, 70, 255), outline=(90, 150, 210, 210), width=2)
for k in range(8):
    yy = int(H * 0.19) + k * 54
    on = k in (1, 2, 4, 5)
    col = (120, 235, 190, 230) if on else (70, 105, 140, 120)
    d.rounded_rectangle([fx - 20, yy, fx + 20, yy + 34],
                        radius=6, fill=(10, 26, 50, 255), outline=col, width=2)
    d.line([(fx + 30, yy + 17), (fx + 52, yy + 17)], fill=col, width=3)

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
d.text((mx, ty), "电梯楼层控制器产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "刷卡核对楼层权限，授权层点亮、未授权层失效——垂直方向的出入口控制",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "出入口控制 · 14 个工程算例（容量 / 时延 / 消防强切 / 楼层映射） ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0215)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
