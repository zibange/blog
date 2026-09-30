# -*- coding: utf-8 -*-
"""
封面制作：AI场景图 去水印 + 标题一步叠加 + 多尺寸输出
修复：标题叠加改为独立 block，主标题/英文副标题/面向工程端 三行显式分行，
用 textlength 实测宽度，用字号×行高系数 显式给行距，杜绝字体重叠。
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

BASE = os.path.dirname(os.path.abspath(__file__))
raw = os.path.join(BASE, "cover_raw.jpg")
out  = os.path.join(BASE, "cover.png")
out_sq = os.path.join(BASE, "cover_square.png")

FONT_PATH = None
for cand in [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc",
             r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\SimHei.ttf"]:
    if os.path.exists(cand):
        FONT_PATH = cand
        break
if not FONT_PATH:
    raise SystemExit("no CJK font")


def inpaint_watermark(im):
    w, h = im.size
    x0 = int(w*0.80); y0 = int(h*0.86); x1 = int(w*0.985); y1 = int(h*0.995)
    px = im.load()
    samples = []
    for xx in range(x0, x1, 6):
        yy = int(y0*0.92)
        if 0 <= yy < h and 0 <= xx < w:
            samples.append(px[xx, yy][:3])
    for yy in range(y0, y1, 6):
        xx = int(x0*0.96)
        if 0 <= xx < w and 0 <= yy < h:
            samples.append(px[xx, yy][:3])
    for xx in range(x0, x1, 8):
        yy = min(h-2, int(y1*0.97))
        samples.append(px[xx, yy][:3])
    avg = tuple(round(sum(c[i] for c in samples)/len(samples)) for i in range(3))
    fill = Image.new("RGB", im.size, avg)
    fill_mask = Image.new("L", im.size, 0)
    fd = ImageDraw.Draw(fill_mask)
    cx = (x0+x1)/2; cy = (y0+y1)/2
    ex = (x1-x0)*1.25; ey = (y1-y0)*1.6
    fd.ellipse([cx-ex, cy-ey, cx+ex, cy+ey], fill=255)
    fill_mask = fill_mask.filter(ImageFilter.GaussianBlur(18))
    return Image.composite(fill, im, fill_mask)


def add_title_block(im, main, sub1, sub2, font_main, font_sub, row_gap_ratio=0.42):
    """在顶部干净区一步叠加三层标题。row_gap_ratio 为行距(相对主字号)。"""
    im = im.convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    fh = font_main.getbbox("中")[3]  # 主字号实际高度(基线到底)
    mh_main = font_main.getbbox(main)[3]
    mh_sub = font_sub.getbbox(sub1)[3]

    # 三行总高度（含行距显式累加，不透支到底）
    row_gap = int(fh * row_gap_ratio)
    total_h = mh_main + row_gap + mh_sub + row_gap + mh_sub

    # 宽度取 max
    mw_main = d.textlength(main, font=font_main)
    mw_sub1 = d.textlength(sub1, font=font_sub)
    mw_sub2 = d.textlength(sub2, font=font_sub)
    maxw = max(mw_main, mw_sub1, mw_sub2)
    pad = int(w*0.04)

    # 底衬
    box_y0 = int(h*0.10)
    box_y1 = int(box_y0 + total_h + pad*1.6)
    d.rounded_rectangle([int(w/2-maxw/2-pad), box_y0,
                         int(w/2+maxw/2+pad), box_y1],
                        radius=int(w*0.02), fill=(12, 22, 40, 170))

    # 三行文字（逐行 y 累加，绝不重叠）
    y = box_y0 + pad
    d.text((w/2 - mw_main/2, y), main, font=font_main, fill=(255,255,255,255))
    y += mh_main + row_gap
    d.text((w/2 - mw_sub1/2, y), sub1, font=font_sub, fill=(205,218,235,255))
    y += mh_sub + row_gap
    d.text((w/2 - mw_sub2/2, y), sub2, font=font_sub, fill=(205,218,235,255))

    return Image.alpha_composite(im, overlay).convert("RGB")


im = Image.open(raw).convert("RGB")

# 横版封面（16:9 原图）
W, H = im.size
f_main = ImageFont.truetype(FONT_PATH, int(W*0.05))
f_sub  = ImageFont.truetype(FONT_PATH, int(W*0.022))
im1 = inpaint_watermark(im)
im1 = add_title_block(
    im1,
    "楼宇对讲系统技术综述",
    "BUILDING INTERCOM SYSTEM",
    "面向工程端  ·  技术综述",
    f_main, f_sub)
im1.save(out)

# 方版封面（裁中央偏上）
side = min(W, H)
crop = im.crop(((W-side)//2, int(H*0.12), (W+side)//2, int(H*0.12)+side))
crop = inpaint_watermark(crop.copy())
cw, ch = crop.size
f_main2 = ImageFont.truetype(FONT_PATH, int(cw*0.058))
f_sub2  = ImageFont.truetype(FONT_PATH, int(cw*0.026))
crop = add_title_block(
    crop,
    "楼宇对讲系统技术综述",
    "BUILDING INTERCOM SYSTEM",
    "面向工程端  ·  技术综述",
    f_main2, f_sub2)
crop.save(out_sq)

print("saved", out, os.path.getsize(out))
print("saved", out_sq, os.path.getsize(out_sq))