# -*- coding: utf-8 -*-
"""分布式可视化坐席节点产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印、无文字）：
  1) 深蓝科技渐变背景 + 稀疏星点
  2) 中部多屏坐席剪影（三屏 + 键鼠漫游光带）
  3) 右侧机房主机机柜剪影（多行主机指示灯）
  4) 从坐席到机柜的双向数据光带（键鼠去 / 画面回）
  5) 底部渐隐深色带 + 白字标题（与既有封面视觉一致）
输出：cover_raw.png（底图）与 cover.png（成片）

Python 教学要点：
  - np.linspace / np.repeat：构造纵向渐变数组，再沿宽度方向复制；
  - ImageDraw.Draw(img,"RGBA")：在 RGB 图上叠加半透明图形（第四通道 alpha）；
  - Image.alpha_composite：把带透明通道的光带图层合成到底图；
  - GaussianBlur：对光带做柔化，营造发光效果；
  - ImageFont.truetype：加载微软雅黑字体渲染中文标题。
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
rng = np.random.default_rng(37)
for _ in range(150):
    sx = int(rng.integers(0, W))
    sy = int(rng.integers(0, int(H * 0.6)))
    r = int(rng.integers(1, 3))
    a = int(rng.integers(20, 70))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 195, 240, a))

# ---- 2. 中部多屏坐席剪影（三屏）----
cx, cy = int(W * 0.34), int(H * 0.40)
for k in range(3):
    off = (k - 1) * 210
    sx = cx + off
    d.rounded_rectangle([sx - 96, cy - 62, sx + 96, cy + 62],
                        radius=10, fill=(14, 34, 62, 255), outline=(95, 155, 215, 220), width=3)
    # 屏内细线（示意画面内容）
    for ln in range(4):
        ly = cy - 42 + ln * 24
        d.line([(sx - 74, ly), (sx + 74 - ln * 14, ly)],
               fill=(90, 150, 210, 90), width=3)
    # 中间屏高亮（当前操控焦点）
    if k == 1:
        d.rounded_rectangle([sx - 96, cy - 62, sx + 96, cy + 62],
                            radius=10, outline=(120, 225, 190, 235), width=3)
# 键鼠剪影
kx, ky = cx, cy + 110
d.rounded_rectangle([kx - 40, ky - 14, kx + 40, ky + 14],
                    radius=6, fill=(20, 44, 80, 255), outline=(120, 205, 245, 200), width=2)
d.ellipse([kx + 58, ky - 18, kx + 82, ky + 6], fill=(120, 205, 245, 200))

# ---- 3. 右侧机房主机机柜剪影 ----
gx, gy = int(W * 0.79), int(H * 0.40)
gw, gh = 190, 400
d.rounded_rectangle([gx - gw // 2, gy - gh // 2, gx + gw // 2, gy + gh // 2],
                    radius=14, fill=(16, 38, 70, 255), outline=(95, 155, 215, 220), width=3)
# 机柜内多行主机 + 指示灯
for k in range(8):
    yy = gy - gh // 2 + 24 + k * 46
    d.rounded_rectangle([gx - gw // 2 + 16, yy, gx + gw // 2 - 16, yy + 34],
                        radius=6, fill=(10, 26, 50, 255), outline=(70, 120, 170, 180), width=1)
    on = k in (1, 3, 4, 6)
    col = (120, 235, 190, 235) if on else (70, 105, 140, 120)
    d.ellipse([gx - gw // 2 + 26, yy + 13, gx - gw // 2 + 36, yy + 23], fill=col)

# ---- 4. 坐席 ↔ 机柜 双向数据光带（键鼠去 / 画面回）----
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
x0, x1 = int(W * 0.42), gx - gw // 2
# 上行光带（画面回，蓝）
for k in range(9):
    y_off = cy - 70 + k * 18
    bd.line([(x0, y_off), (x1, gy - 90 + k * 20)],
            fill=(90, 195, 245, 46 - k * 4), width=5)
# 下行光带（键鼠去，绿）
for k in range(6):
    y_off = ky - 20 + k * 10
    bd.line([(x0, y_off), (x1, gy + 40 + k * 16)],
            fill=(120, 225, 190, 40 - k * 4), width=4)
for k in range(6):
    nx = x0 + (x1 - x0) * (k + 1) / 7
    ny = cy - 60 + k * 26
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
d.text((mx, ty), "分布式可视化坐席节点产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "把远端主机打包上局域网，一人多机、跨楼层协作——人在坐席、机在机房",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "中央控制 · 14 个工程算例（带宽 / 延时 / 权限 / 冗余 / 国密） ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0215)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
