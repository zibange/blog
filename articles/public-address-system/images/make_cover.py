# -*- coding: utf-8 -*-
"""
公共广播系统封面生成脚本
AI 场景底图 + 标题一步叠加（禁止多次叠加避免叠影）
"""
from PIL import Image, ImageDraw, ImageFont
import os

DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(DIR, 'cover_raw.jpg')
OUT = os.path.join(DIR, 'cover.png')

# 标题文本（必须与成稿完全一致）
MAIN_TITLE = '公共广播系统（PA）产品综述'
SUB_TITLE = '· 面向工程端'

def main():
    img = Image.open(RAW).convert('RGBA')
    W, H = img.size
    draw = ImageDraw.Draw(img)

    # 字体
    try:
        font_main = ImageFont.truetype('msyhbd.ttc', int(W * 0.052))  # 主标题 ~5% 宽
        font_sub = ImageFont.truetype('msyh.ttc', int(W * 0.028))     # 副标题 ~2.8% 宽
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 计算文字尺寸
    bbox_main = draw.textbbox((0, 0), MAIN_TITLE, font=font_main)
    tw_main = bbox_main[2] - bbox_main[0]
    th_main = bbox_main[3] - bbox_main[1]

    bbox_sub = draw.textbbox((0, 0), SUB_TITLE, font=font_sub)
    tw_sub = bbox_sub[2] - bbox_sub[0]
    th_sub = bbox_sub[3] - bbox_sub[1]

    # 位置：水平居中，垂直偏下（y ≈ 70%）
    y_center = int(H * 0.72)
    total_h = th_main + 10 + th_sub
    y_main = y_center - total_h // 2
    y_sub = y_main + th_main + 10

    x_main = (W - tw_main) // 2
    x_sub = (W - tw_sub) // 2

    # 深色半透明圆角底衬（增强对比度）
    pad_x = int(W * 0.03)
    pad_y = int(H * 0.025)
    rect_x0 = min(x_main, x_sub) - pad_x
    rect_y0 = y_main - pad_y
    rect_x1 = max(x_main + tw_main, x_sub + tw_sub) + pad_x
    rect_y1 = y_sub + th_sub + pad_y

    # 半透明黑色底衬
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rounded_rectangle(
        [rect_x0, rect_y0, rect_x1, rect_y1],
        radius=int(H * 0.02),
        fill=(0, 0, 0, 140)
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # 主标题（白色）
    draw.text((x_main, y_main), MAIN_TITLE, font=font_main, fill=(255, 255, 255, 255))
    # 副标题（浅灰色）
    draw.text((x_sub, y_sub), SUB_TITLE, font=font_sub, fill=(220, 220, 220, 255))

    # 保存
    img.convert('RGB').save(OUT, 'PNG')
    print(f'✓ 封面已生成: {OUT}')
    print(f'  主标题: {MAIN_TITLE}')
    print(f'  副标题: {SUB_TITLE}')
    print(f'  尺寸: {W}x{H}')

if __name__ == '__main__':
    main()
