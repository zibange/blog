# -*- coding: utf-8 -*-
"""无线网桥产品综述 —— 封面图（程序化生成，无 AI 位图/无水印）

构图：深蓝渐变夜空 + 两端楼顶塔架 + 抛物面天线剪影 + 一条带辉光的微波波束
      + 波束内的菲涅尔椭球光点与自由空间损耗标注节点。
封面文字用 PIL 叠加「深色半透明圆角底衬 + 白字」，保证对比度。

Python 教学要点：
  - PIL 的 ImageDraw.rounded_rectangle 画圆角矩形/底衬；
  - 逐行填充实现垂直渐变（O(H) 而非 O(W*H)，更高效）；
  - Image.alpha_composite 把半透明图层叠回底图（RGBA 混合）；
  - ImageFilter.GaussianBlur 做轻微辉光；
  - ImageFont.truetype 加载微软雅黑，找不到时回退默认字体；
  - draw.arc / draw.line 画弧线与折线，用 joint="curve" 平滑折点。
"""
import os
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
    """深蓝垂直渐变：顶部夜空 #08152B -> 底部 #133A60。逐行画横线实现。"""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top = (8, 21, 43)
    bot = (19, 58, 96)
    for y in range(H):
        t = y / (H - 1)  # 归一化位置 0~1
        # 线性插值：每个颜色通道按 t 从 top 过渡到 bot
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img


def glow_line(draw, pts, color, width=6, glow=22):
    """带辉光的折线：先画粗的半透明辉光层，再画亮的细线。"""
    draw.line(pts, fill=tuple(int(c * 0.35) for c in color), width=glow, joint="curve")
    draw.line(pts, fill=color, width=width, joint="curve")


def dish(draw, cx, cy, face_right=True):
    """画一个抛物面天线剪影：三角支架 + 碟形弧 + 馈源亮点。"""
    color = (150, 195, 235, 255)
    # 碟形用椭圆弧近似（开口朝对端）
    if face_right:
        box = [cx - 46, cy - 62, cx + 18, cy + 62]
        feed = (cx + 34, cy)
    else:
        box = [cx - 18, cy - 62, cx + 46, cy + 62]
        feed = (cx - 34, cy)
    draw.arc(box, start=-80, end=80, fill=color, width=7)
    # 馈源支杆 + 亮点
    draw.line([(cx, cy), feed], fill=color, width=3)
    draw.ellipse([feed[0] - 7, feed[1] - 7, feed[0] + 7, feed[1] + 7],
                 fill=(190, 235, 255, 255))
    # 支撑杆
    draw.line([(cx, cy + 50), (cx, cy + 150)], fill=(90, 125, 165, 255), width=6)


def draw_scene(img):
    """在底图上画两端楼顶塔架、抛物面天线、微波波束与菲涅尔光点。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # --- 左右两端楼体剪影（地面到屋面）---
    roof_y = 700
    d.rectangle([40, roof_y, 360, H], fill=(16, 40, 70, 245), outline=(70, 120, 170, 180), width=2)
    d.rectangle([W - 360, roof_y, W - 40, H], fill=(16, 40, 70, 245), outline=(70, 120, 170, 180), width=2)
    # 楼体窗格光点
    for i in range(4):
        for j in range(3):
            wx = 70 + i * 70
            wy = roof_y + 60 + j * 80
            d.rectangle([wx, wy, wx + 40, wy + 46], fill=(30, 62, 100, 255))
            d.ellipse([wx + 12, wy + 16, wx + 24, wy + 28], fill=(120, 180, 230, 200))
            wx2 = W - 330 + i * 70
            d.rectangle([wx2, wy, wx2 + 40, wy + 46], fill=(30, 62, 100, 255))
            d.ellipse([wx2 + 12, wy + 16, wx2 + 24, wy + 28], fill=(120, 180, 230, 200))

    # --- 两端塔架与抛物面天线 ---
    left_ant = (300, 560)
    right_ant = (W - 300, 560)
    dish(d, left_ant[0], left_ant[1], face_right=True)
    dish(d, right_ant[0], right_ant[1], face_right=False)

    # --- 微波波束光带（两端馈源之间，微微上拱的视距线）---
    lf = (left_ant[0] + 34, left_ant[1])
    rf = (right_ant[0] - 34, right_ant[1])
    mid_y = 470
    beam_pts = [lf, (W // 2, mid_y), rf]
    # 主瓣上下两条边界（菲涅尔区包络），浅绿半透明
    d.polygon([lf, (W // 2, mid_y - 46), rf, (W // 2, mid_y + 46)],
              fill=(60, 200, 150, 34))
    glow_line(d, beam_pts, (110, 235, 185, 220), width=5, glow=22)

    # --- 菲涅尔净空光点：沿波束的几个节点（发射→中点→接收）---
    for cx, cy in [(lf[0] + 90, 520), (W // 2, mid_y), (rf[0] - 90, 520)]:
        for r, a in [(20, 34), (11, 90), (6, 235)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 245, 205, a))

    # --- 中点障碍剪影（被波束跨过的楼顶女儿墙），示意净空概念 ---
    d.rectangle([W // 2 - 26, 640, W // 2 + 26, 700], fill=(46, 74, 108, 230))

    # 轻微辉光模糊叠回底图（alpha_composite 需要两张同尺寸 RGBA 图）
    layer = layer.filter(ImageFilter.GaussianBlur(0.5))
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return img.convert("RGB")


def add_title(img):
    """叠加标题：深色半透明圆角底衬 + 白字。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([120, 96, W - 120, 300], radius=26,
                        fill=(6, 18, 36, 205), outline=(120, 165, 215, 160), width=2)
    f1 = font(76, bold=True)
    f2 = font(34, bold=False)
    main = "无线网桥"
    sub = "视距链路 · 菲涅尔净空 · EIRP 合规 —— 把没法拉缆的两端接起来"
    d.text((W // 2, 168), main, font=f1, fill=(255, 255, 255, 255), anchor="mm")
    d.text((W // 2, 252), sub, font=f2, fill=(175, 210, 245, 255), anchor="mm")
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
    # 留一份 cover_raw（无标题底图）便于复核
    raw_img = gradient_bg()
    raw_img = draw_scene(raw_img)
    raw_img.save(os.path.join(OUT, "cover_raw.png"), "PNG")
    print("cover saved:", path, img.size)
