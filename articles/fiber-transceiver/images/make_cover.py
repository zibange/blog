# -*- coding: utf-8 -*-
"""光纤收发器产品综述 —— 封面图（程序化生成，无 AI 位图/无水印）

构图：深蓝渐变背景 + 一对收发器（左电口设备 → 收发器 → 光纤 → 收发器 → 右设备）
      + 一条带辉光的双向光纤光带（1310/1550 两色）+ 链路预算节点光点。
封面文字用 PIL 叠加「深色半透明圆角底衬 + 白字」，保证对比度。

Python 教学要点：
  - PIL 的 ImageDraw.rounded_rectangle 画圆角矩形/底衬；
  - 逐行填充实现垂直渐变（O(H) 而非 O(W*H)，更高效）；
  - Image.alpha_composite 把半透明图层叠回底图（RGBA 混合）；
  - ImageFilter.GaussianBlur 做轻微辉光；
  - ImageFont.truetype 加载微软雅黑，找不到时回退默认字体。
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
    """深蓝垂直渐变：顶部 #0B1E3A -> 底部 #123A63。逐行画横线实现。"""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top = (11, 30, 58)
    bot = (18, 58, 99)
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


def draw_scene(img):
    """在底图上画两端设备、收发器、双向光纤光带与链路预算光点。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    dev_y0, dev_y1 = 470, 700

    # --- 左端设备（交换机/摄像机阵列剪影）---
    ld_x0, ld_x1 = 90, 330
    d.rounded_rectangle([ld_x0, dev_y0, ld_x1, dev_y1], radius=12,
                        fill=(24, 52, 88, 240), outline=(90, 140, 195, 200), width=2)
    for i in range(5):
        yy = dev_y0 + 34 + i * 42
        d.rounded_rectangle([ld_x0 + 18, yy, ld_x1 - 18, yy + 28], radius=5,
                            fill=(36, 66, 104, 255), outline=(100, 145, 190, 180), width=1)
        d.ellipse([ld_x0 + 30, yy + 9, ld_x0 + 42, yy + 21], fill=(60, 220, 150, 255))

    # --- 右端设备（服务器/交换机阵列剪影）---
    rd_x0, rd_x1 = 1206, 1446
    d.rounded_rectangle([rd_x0, dev_y0, rd_x1, dev_y1], radius=12,
                        fill=(24, 52, 88, 240), outline=(90, 140, 195, 200), width=2)
    for i in range(5):
        yy = dev_y0 + 34 + i * 42
        d.rounded_rectangle([rd_x0 + 18, yy, rd_x1 - 18, yy + 28], radius=5,
                            fill=(36, 66, 104, 255), outline=(100, 145, 190, 180), width=1)
        d.ellipse([rd_x1 - 42, yy + 9, rd_x1 - 30, yy + 21], fill=(80, 170, 255, 255))

    # --- 两台收发器（中部左右对称的小盒子）---
    tx_x0, tx_x1 = 470, 620
    rx_x0, rx_x1 = 916, 1066
    box_y0, box_y1 = 510, 660
    for (x0, x1, label) in [(tx_x0, tx_x1, "A"), (rx_x0, rx_x1, "B")]:
        d.rounded_rectangle([x0, box_y0, x1, box_y1], radius=10,
                            fill=(42, 70, 108, 255), outline=(130, 175, 220, 230), width=2)
        # 面板指示灯
        for k in range(4):
            d.ellipse([x0 + 24 + k * 30, box_y1 - 34, x0 + 34 + k * 30, box_y1 - 24],
                      fill=(60, 220, 150, 255) if k % 2 == 0 else (140, 200, 255, 255))
        # 光口亮点
        d.ellipse([x1 - 44, box_y0 + 70, x1 - 20, box_y0 + 94], fill=(180, 235, 255, 255))

    # --- 电口连线（设备 ↔ 收发器，绿色数据光带）---
    glow_line(d, [(ld_x1, 585), (tx_x0, 585)], (70, 200, 150, 220), width=4, glow=14)
    glow_line(d, [(rx_x1, 585), (rd_x0, 585)], (90, 170, 255, 220), width=4, glow=14)

    # --- 光纤链路（收发器 A ↔ B，双向两色光带）---
    # 1310 nm 去程（橙红），1550 nm 回程（蓝紫），略微上下错位避免重叠
    glow_line(d, [(tx_x1, 560), (W // 2, 500), (rx_x0, 560)],
              (255, 150, 90, 230), width=5, glow=20)
    glow_line(d, [(tx_x1, 610), (W // 2, 670), (rx_x0, 610)],
              (150, 160, 255, 230), width=5, glow=20)
    # 链路上的预算节点光点（发射 → 衰减 → 熔接 → 接收）
    for cx, cy in [(690, 512), (768, 500), (845, 512)]:
        for r, a in [(16, 40), (9, 100), (5, 230)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 210, 160, a))

    # 轻微辉光模糊叠回底图（alpha_composite 需要两张同尺寸 RGBA 图）
    layer = layer.filter(ImageFilter.GaussianBlur(0.4))
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return img.convert("RGB")


def add_title(img):
    """叠加标题：深色半透明圆角底衬 + 白字。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([120, 96, W - 120, 300], radius=26,
                        fill=(6, 18, 36, 205), outline=(120, 165, 215, 160), width=2)
    f1 = font(76, bold=True)
    f2 = font(36, bold=False)
    main = "光纤收发器"
    sub = "电光转换 · 链路预算 · 单纤双向 —— 把铜缆够不着的地方接过去"
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
