# -*- coding: utf-8 -*-
"""执法记录仪与采集站产品综述 · 封面制作

底图为本脚本程序化生成的抽象科技风格图（无 AI 水印、无文字）：
  1) 深蓝科技渐变背景 + 稀疏星点
  2) 左侧胸前佩戴的执法记录仪剪影（镜头 + 摄录红点 + 背夹）
  3) 中部证据链光带（记录仪 → 数据光流 → 采集站机柜多仓位）
  4) 右侧采集站机柜（多仓位指示灯 + 校验对勾意象）
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
rng = np.random.default_rng(29)
for _ in range(160):
    sx = int(rng.integers(0, W))
    sy = int(rng.integers(0, int(H * 0.6)))
    r = int(rng.integers(1, 3))
    a = int(rng.integers(20, 70))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 195, 240, a))

# ---- 2. 左侧执法记录仪剪影（胸前佩戴）----
cx, cy = int(W * 0.20), int(H * 0.42)
# 机身
d.rounded_rectangle([cx - 78, cy - 150, cx + 78, cy + 140],
                    radius=26, fill=(20, 44, 80, 255), outline=(95, 155, 215, 220), width=3)
# 顶部高光条
d.rounded_rectangle([cx - 78, cy - 150, cx + 78, cy - 118],
                    radius=14, fill=(34, 70, 114, 230))
# 镜头（同心圆）
lens_y = cy - 52
for rr, col in [(56, (60, 120, 180, 220)), (42, (18, 40, 70, 255)),
                (30, (40, 90, 140, 255)), (16, (10, 24, 44, 255))]:
    d.ellipse([cx - rr, lens_y - rr, cx + rr, lens_y + rr], fill=col)
d.ellipse([cx - 9, lens_y - 9, cx + 9, lens_y + 9], fill=(120, 205, 245, 210))
# 摄录状态红点
d.ellipse([cx + 52, cy - 132, cx + 68, cy - 116], fill=(240, 70, 70, 245))
# 小屏幕
d.rounded_rectangle([cx - 60, cy + 18, cx + 60, cy + 96],
                    radius=10, fill=(12, 30, 56, 255), outline=(80, 140, 195, 180), width=2)
# 背夹
d.rounded_rectangle([cx - 26, cy + 140, cx + 26, cy + 196],
                    radius=8, fill=(30, 60, 100, 220), outline=(95, 155, 215, 180), width=2)

# ---- 3. 中部证据链数据光带（记录仪 → 采集站）----
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
bx0 = cx + 100
bx1 = int(W * 0.66)
for k in range(6):
    y_off = cy - 90 + k * 34
    bd.line([(bx0, y_off), (bx1, cy - 40 + k * 8)],
            fill=(90, 195, 245, 45 - k * 4), width=5)
# 几个证据节点光点
for k in range(5):
    nx = bx0 + (bx1 - bx0) * (k + 1) / 6
    ny = cy - 80 + k * 26
    bd.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(150, 225, 200, 190))
beams = beams.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img.convert("RGBA"), beams).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- 4. 右侧采集站机柜（多仓位）----
sx, sy = int(W * 0.70), int(H * 0.30)
d.rounded_rectangle([sx - 26, sy - 40, sx + 250, sy + 430],
                    radius=18, fill=(16, 38, 70, 255), outline=(90, 150, 210, 210), width=3)
d.rounded_rectangle([sx - 26, sy - 40, sx + 250, sy - 4],
                    radius=10, fill=(32, 66, 110, 230))
# 4×4 仓位网格 + 状态灯
cs, cg = 44, 12
for r in range(4):
    for c in range(4):
        xx = sx + 4 + c * (cs + cg)
        yy = sy + 30 + r * (cs + cg + 6)
        on = (r + c) % 3 != 0
        col = (120, 235, 190, 220) if on else (70, 110, 150, 140)
        d.rounded_rectangle([xx, yy, xx + cs, yy + cs],
                            radius=6, fill=(10, 26, 50, 255), outline=col, width=2)
        d.ellipse([xx + cs - 14, yy + 8, xx + cs - 5, yy + 17], fill=col)

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
d.text((mx, ty), "执法记录仪与采集站产品综述", font=f_main, fill=(255, 255, 255))
d.text((mx, ty + int(H * 0.082)),
       "前端随身防篡改取证，归队自动上传校验充电归档，串起完整证据链",
       font=f_sub, fill=(168, 212, 235))
d.text((mx, ty + int(H * 0.124)),
       "视频物联 · 14 个工程算例（容量 / 续航 / 并发上传 / 证据链） ｜ 含 KaTeX 公式 ｜ 面向工程端",
       font=ImageFont.truetype(fy, int(H * 0.0215)), fill=(126, 174, 205))

img.save(RAW)
img.save(OUT)
print("cover.png done", img.size)
