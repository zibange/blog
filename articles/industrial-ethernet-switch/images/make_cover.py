# -*- coding: utf-8 -*-
"""工业以太网交换机产品综述 —— 封面图（程序化生成，无 AI 位图/无水印）

构图：深蓝渐变背景 + 机柜中一排导轨交换机 + 光纤环网光带 + 上联数据光流。
封面文字用 PIL 叠加「深色半透明圆角底衬 + 白字」，保证对比度。

Python 教学要点：
  - PIL 的 ImageDraw.rounded_rectangle 画圆角底衬；
  - 逐像素/逐行填充实现垂直渐变（O(H) 而非 O(W*H)，更高效）；
  - Image.alpha_composite 把半透明文字层叠回底图；
  - ImageFont.truetype 加载微软雅黑，找不到时回退默认字体。
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1536, 1024


def font(size, bold=False):
    """加载字体：优先微软雅黑（粗体用 msyhbd），失败回退默认。"""
    name = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


def gradient_bg():
    """深蓝垂直渐变：顶部 #0B1E3A -> 底部 #123A63。"""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top = (11, 30, 58)
    bot = (18, 58, 99)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img


def glow_line(draw, pts, color, width=6, glow=22):
    """带辉光的折线：先画粗的半透明辉光层，再画亮线（此处在 RGB 上模拟）。"""
    draw.line(pts, fill=tuple(int(c * 0.35) for c in color), width=glow, joint="curve")
    draw.line(pts, fill=color, width=width, joint="curve")


def draw_scene(img):
    """在底图上画机柜、导轨交换机、光纤环与上联光流。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # --- 机柜外框（中下部）---
    cab_x0, cab_y0, cab_x1, cab_y1 = 250, 430, 1290, 900
    d.rounded_rectangle([cab_x0, cab_y0, cab_x1, cab_y1], radius=18,
                        fill=(20, 45, 78, 235), outline=(90, 140, 195, 200), width=3)
    # 机柜立柱纹理
    for xx in range(cab_x0 + 30, cab_x1 - 10, 90):
        d.line([(xx, cab_y0 + 20), (xx, cab_y1 - 20)], fill=(40, 75, 118, 120), width=3)

    # --- 一排导轨式交换机（4 台，带端口与指示灯）---
    sw_y0, sw_y1 = 560, 690
    sw_w, gap = 210, 26
    start_x = cab_x0 + 45
    switch_centers = []
    for i in range(4):
        sx0 = start_x + i * (sw_w + gap)
        sx1 = sx0 + sw_w
        d.rounded_rectangle([sx0, sw_y0, sx1, sw_y1], radius=8,
                            fill=(36, 62, 96, 255), outline=(120, 165, 215, 220), width=2)
        # 端口格
        for p in range(6):
            px0 = sx0 + 16 + p * 30
            d.rectangle([px0, sw_y0 + 18, px0 + 20, sw_y0 + 44],
                        fill=(14, 28, 48, 255), outline=(90, 130, 175, 200), width=1)
        # 状态指示灯（绿/蓝交替，带辉光）
        for p in range(6):
            lx = sx0 + 26 + p * 30
            col = (60, 220, 150, 255) if p % 2 == 0 else (80, 170, 255, 255)
            d.ellipse([lx - 4, sw_y1 - 26, lx + 4, sw_y1 - 18], fill=col)
        switch_centers.append(((sx0 + sx1) // 2, sw_y0))

    # --- 光纤环网光带：在交换机上方连成一条环 ---
    ring_y = 470
    ring_pts = [switch_centers[0], (switch_centers[0][0], ring_y),
                (switch_centers[-1][0], ring_y), switch_centers[-1]]
    glow_line(d, ring_pts, (90, 200, 255, 230), width=5, glow=20)
    # 环上节点光点
    for (cx, cy) in switch_centers:
        d.ellipse([cx - 6, ring_y - 6, cx + 6, ring_y + 6], fill=(140, 225, 255, 255))

    # --- 上联数据光流：从中间两台交换机向上汇聚到核心 ---
    for cx, cy in switch_centers[1:3]:
        glow_line(d, [(cx, sw_y0), (cx, 380), (W // 2, 300)],
                  (120, 160, 255, 200), width=4, glow=16)

    # --- 核心节点（顶部中央的光球）---
    core = (W // 2, 290)
    for r, a in [(60, 30), (42, 55), (26, 110), (14, 220)]:
        d.ellipse([core[0] - r, core[1] - r, core[0] + r, core[1] + r],
                  fill=(110, 190, 255, a))
    d.ellipse([core[0] - 8, core[1] - 8, core[0] + 8, core[1] + 8], fill=(230, 245, 255, 255))

    # 轻微辉光模糊叠回
    layer = layer.filter(ImageFilter.GaussianBlur(0.4))
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return img.convert("RGB")


def add_title(img):
    """叠加标题：深色半透明圆角底衬 + 白字。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # 底衬
    d.rounded_rectangle([120, 96, W - 120, 300], radius=26,
                        fill=(6, 18, 36, 205), outline=(120, 165, 215, 160), width=2)
    f1 = font(76, bold=True)
    f2 = font(38, bold=False)
    main = "工业以太网交换机"
    sub = "宽温 · 冗余电源 · 环网自愈 —— 现场网络的骨干"
    d.text((W // 2, 168), main, font=f1, fill=(255, 255, 255, 255), anchor="mm")
    d.text((W // 2, 252), sub, font=f2, fill=(175, 210, 245, 255), anchor="mm")
    # 角标
    f3 = font(28, bold=False)
    d.text((W - 150, H - 60), "product overview", font=f3,
           fill=(150, 185, 220, 180), anchor="mm")
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


if __name__ == "__main__":
    img = gradient_bg()
    img = draw_scene(img)
    img = add_title(img)
    path = os.path.join(OUT, "cover.png")
    img.save(path, "PNG")
    # 同时留一份 cover_raw（无标题底图）便于复核
    raw = gradient_bg()
    raw = draw_scene(raw)
    raw.save(os.path.join(OUT, "cover_raw.png"), "PNG")
    print("cover saved:", path, img.size)
