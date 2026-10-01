# -*- coding: utf-8 -*-
"""
FBG 光纤光栅传感器产品综述 - 封面生成脚本
流程：AI 场景底图 → 去右下角"AI生成"水印 → 一步叠加标题文字 → cover.png
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# 配置
RAW_IMAGE = 'cover_raw.jpg'
OUTPUT_IMAGE = 'cover.png'

# 标题文字（与成稿标题完全一致）
MAIN_TITLE = '光纤光栅传感器（FBG）产品综述'
SUB_TITLE = '· 面向工程端'

def remove_watermark(img):
    """去除右下角'AI生成'水印 - 用背景色填充 + 羽化边缘"""
    width, height = img.size
    # 水印大致位置：右下角，约 200x80 像素区域
    wm_w, wm_h = 220, 90
    x0 = width - wm_w - 30
    y0 = height - wm_h - 30

    # 创建蒙版
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    # 在水印区域画一个稍微大一点的圆角矩形
    mask_draw.rounded_rectangle(
        [x0 - 20, y0 - 10, x0 + wm_w + 20, y0 + wm_h + 10],
        radius=20, fill=255
    )
    # 羽化蒙版边缘
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8))

    # 采样水印周围的背景色（取多个点求平均）
    # 从水印区域上方和左方采样天空/背景色
    sample_points = [
        (x0 - 50, y0 - 30),
        (x0 + wm_w // 2, y0 - 40),
        (x0 - 30, y0 + wm_h // 2),
    ]
    pixels = img.load()
    r_sum, g_sum, b_sum = 0, 0, 0
    for px, py in sample_points:
        r, g, b = pixels[px, py]
        r_sum += r
        g_sum += g
        b_sum += b
    n = len(sample_points)
    bg_color = (r_sum // n, g_sum // n, b_sum // n)

    # 创建填充层
    fill_layer = Image.new('RGB', (width, height), bg_color)

    # 用蒙版合成
    result = img.copy()
    result.paste(fill_layer, mask=mask)

    return result


def add_title(img):
    """在底图上叠加标题文字 - 一步完成"""
    width, height = img.size
    draw = ImageDraw.Draw(img, 'RGBA')

    # 字体路径（Windows 微软雅黑）
    font_paths = [
        'C:/Windows/Fonts/msyhbd.ttc',  # 微软雅黑粗体
        'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
    ]

    main_font = None
    sub_font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                main_font = ImageFont.truetype(fp, int(width * 0.042))
                sub_font = ImageFont.truetype(fp, int(width * 0.022))
                break
            except:
                continue

    if main_font is None:
        main_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # 主标题位置：水平居中，垂直偏下（约 68% 处）
    main_text = MAIN_TITLE
    sub_text = SUB_TITLE

    # 计算文字尺寸
    try:
        main_bbox = draw.textbbox((0, 0), main_text, font=main_font)
        main_w = main_bbox[2] - main_bbox[0]
        main_h = main_bbox[3] - main_bbox[1]
        sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_h = sub_bbox[3] - sub_bbox[1]
    except:
        main_w, main_h = len(main_text) * 50, 60
        sub_w, sub_h = len(sub_text) * 25, 30

    main_x = (width - main_w) / 2
    main_y = int(height * 0.66)

    # 副标题位置：主标题下方
    sub_x = (width - sub_w) / 2
    sub_y = main_y + main_h + int(height * 0.015)

    # 总高度（用于深色半透明底衬）
    total_h = sub_y + sub_h - main_y + int(height * 0.04)
    total_w = max(main_w, sub_w) + int(width * 0.06)
    total_x = (width - total_w) / 2
    total_y = main_y - int(height * 0.02)

    # 绘制深色半透明圆角底衬
    draw.rounded_rectangle(
        [total_x, total_y, total_x + total_w, total_y + total_h],
        radius=int(height * 0.02),
        fill=(0, 0, 0, 150)
    )

    # 绘制主标题（白色）
    draw.text((main_x, main_y), main_text, font=main_font, fill=(255, 255, 255, 255))

    # 绘制副标题（浅灰色）
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=(220, 220, 220, 255))

    return img


def main():
    if not os.path.exists(RAW_IMAGE):
        print(f"错误：找不到底图文件 {RAW_IMAGE}")
        return

    # 1. 打开底图
    img = Image.open(RAW_IMAGE).convert('RGB')
    print(f"底图尺寸：{img.size}")

    # 2. 去水印
    img = remove_watermark(img)
    print("水印去除完成")

    # 3. 叠加标题
    img = add_title(img)
    print(f"标题叠加完成：主标题「{MAIN_TITLE}」副标题「{SUB_TITLE}」")

    # 4. 保存
    img.save(OUTPUT_IMAGE, 'PNG')
    print(f"封面图已保存：{OUTPUT_IMAGE}")


if __name__ == '__main__':
    main()
