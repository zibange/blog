# -*- coding: utf-8 -*-
"""
停车场管理系统封面生成脚本
AI 场景底图 + 标题一步叠加（禁止多次叠加避免叠影）
"""
from PIL import Image, ImageDraw, ImageFont
import os

DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(DIR, 'cover_raw.png')
OUT = os.path.join(DIR, 'cover.png')

MAIN_TITLE = '停车场管理系统产品综述'
SUB_TITLE = '以车牌为凭证，把一次通行压进两秒'


def remove_watermark(img):
    W, H = img.size
    bw, bh = int(W * 0.30), int(H * 0.17)
    x0, y0 = W - bw, H - bh
    src = img.crop((x0 - bw, y0, x0, y0 + bh))
    mask = Image.new('L', (bw, bh), 255)
    md = ImageDraw.Draw(mask)
    feather = max(10, int(min(bw, bh) * 0.18))
    for i in range(feather):
        alpha = int(255 * (i + 1) / feather)
        md.line([(0, i), (bw, i)], fill=alpha)
    for i in range(feather):
        alpha = int(255 * (i + 1) / feather)
        md.line([(i, feather), (i, bh)], fill=alpha)
    img.paste(src, (x0, y0), mask)
    return img


def main():
    img = Image.open(RAW).convert('RGBA')
    img = remove_watermark(img)
    W, H = img.size
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype('msyhbd.ttc', int(W * 0.050))
        font_sub = ImageFont.truetype('msyh.ttc', int(W * 0.023))
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    bbox_main = draw.textbbox((0, 0), MAIN_TITLE, font=font_main)
    tw_main = bbox_main[2] - bbox_main[0]
    th_main = bbox_main[3] - bbox_main[1]

    bbox_sub = draw.textbbox((0, 0), SUB_TITLE, font=font_sub)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    th_sub = bbox_sub[3] - bbox_sub[1]

    y_center = int(H * 0.74)
    total_h = th_main + 14 + th_sub
    y_main = y_center - total_h // 2
    y_sub = y_main + th_main + 14

    x_main = (W - tw_main) // 2
    x_sub = (W - tw_sub) // 2

    pad_x = int(W * 0.03)
    pad_y = int(H * 0.028)
    rect_x0 = min(x_main, x_sub) - pad_x
    rect_y0 = y_main - pad_y
    rect_x1 = max(x_main + tw_main, x_sub + tw_sub) + pad_x
    rect_y1 = y_sub + th_sub + pad_y

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rounded_rectangle(
        [rect_x0, rect_y0, rect_x1, rect_y1],
        radius=int(H * 0.02),
        fill=(0, 0, 0, 158)
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    draw.text((x_main, y_main), MAIN_TITLE, font=font_main, fill=(255, 255, 255, 255))
    draw.text((x_sub, y_sub), SUB_TITLE, font=font_sub, fill=(226, 226, 226, 255))

    img.convert('RGB').save(OUT, 'PNG')
    print(f'OK cover: {OUT}')
    print(f'  main: {MAIN_TITLE} / sub: {SUB_TITLE}')
    print(f'  size: {W}x{H}')


if __name__ == '__main__':
    main()
