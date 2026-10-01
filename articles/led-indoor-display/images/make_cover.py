"""
室内 LED 显示屏产品封面生成脚本
流程：AI场景底图 → 去水印 → 标题叠加 → cover.png

遵循封面生成工作流规范：
- 主标题：大字号，白色，深色半透明圆角底衬
- 副标题：主标题下方，字号较小
- 位置：水平居中，垂直偏下（y=70%左右）
- 字体：微软雅黑（系统中文字体）
- 一步叠加，避免多次叠加产生叠影
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(BASE_DIR, "cover_raw.jpg")
OUTPUT_FILE = os.path.join(BASE_DIR, "cover.png")

# 标题文本
MAIN_TITLE = "室内 LED 显示屏产品综述"
SUB_TITLE = "· 面向工程端"


def remove_watermark(img):
    """去除右下角'AI生成'水印
    使用背景色填充 + 边缘羽化的方式（近似 inpaint）
    """
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # 水印区域（右下角）
    wm_w, wm_h = 200, 70
    wm_x = width - wm_w - 30
    wm_y = height - wm_h - 30

    # 采样水印区域上方的平均色作为填充色
    sample_box = (wm_x, wm_y - 25, wm_x + wm_w, wm_y)
    sample_region = img.crop(sample_box)

    pixels = list(sample_region.getdata())
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)

    fill_color = (avg_r, avg_g, avg_b)

    # 用填充色覆盖水印区域
    draw.rectangle([wm_x, wm_y, wm_x + wm_w, wm_y + wm_h], fill=fill_color)

    # 边缘羽化处理
    feather = 18
    for i in range(feather):
        alpha = int(255 * (1 - i / feather))
        # 顶部边缘
        draw.line(
            [(wm_x, wm_y + i), (wm_x + wm_w, wm_y + i)],
            fill=fill_color,
            width=1
        )
        # 底部边缘
        draw.line(
            [(wm_x, wm_y + wm_h - i), (wm_x + wm_w, wm_y + wm_h - i)],
            fill=fill_color,
            width=1
        )
        # 左侧边缘
        draw.line(
            [(wm_x + i, wm_y), (wm_x + i, wm_y + wm_h)],
            fill=fill_color,
            width=1
        )
        # 右侧边缘
        draw.line(
            [(wm_x + wm_w - i, wm_y), (wm_x + wm_w - i, wm_y + wm_h)],
            fill=fill_color,
            width=1
        )

    # 高斯模糊让边缘更自然
    blur_box = (wm_x - 12, wm_y - 12, wm_x + wm_w + 12, wm_y + wm_h + 12)
    blur_region = img.crop(blur_box)
    blur_region = blur_region.filter(ImageFilter.GaussianBlur(radius=2.5))
    img.paste(blur_region, blur_box)

    return img


def add_title(img):
    """在底图上一步叠加标题文字"""
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # 尝试加载中文字体
    font_paths = [
        "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
        "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
    ]

    main_font = None
    sub_font = None

    for fp in font_paths:
        if os.path.exists(fp):
            main_size = int(width * 0.055)
            sub_size = int(main_size * 0.45)
            try:
                main_font = ImageFont.truetype(fp, main_size)
                sub_font = ImageFont.truetype(fp, sub_size)
                break
            except:
                continue

    if main_font is None:
        main_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # 计算文字尺寸
    main_bbox = draw.textbbox((0, 0), MAIN_TITLE, font=main_font)
    main_w = main_bbox[2] - main_bbox[0]
    main_h = main_bbox[3] - main_bbox[1]

    sub_bbox = draw.textbbox((0, 0), SUB_TITLE, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_h = sub_bbox[3] - sub_bbox[1]

    # 位置：水平居中，垂直偏下（y 约 72% 处）
    center_x = width / 2
    base_y = height * 0.72

    # 深色半透明圆角底衬
    padding_x = int(main_w * 0.08)
    padding_y = int(main_h * 0.5)
    total_w = main_w + padding_x * 2
    total_h = main_h + sub_h + padding_y * 2 + 12

    bg_x = center_x - total_w / 2
    bg_y = base_y - total_h / 2

    # 绘制圆角矩形底衬
    def draw_rounded_rect(draw, xy, radius, fill):
        x1, y1, x2, y2 = xy
        draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
        draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
        draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
        draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)

    bg_radius = int(total_h * 0.2)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    draw_rounded_rect(
        overlay_draw,
        (bg_x, bg_y, bg_x + total_w, bg_y + total_h),
        bg_radius,
        (0, 0, 0, 145)
    )

    # 将半透明底衬合成到原图
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # 绘制主标题（白色）
    main_x = center_x - main_w / 2
    main_y = bg_y + padding_y
    draw.text((main_x, main_y), MAIN_TITLE, font=main_font, fill=(255, 255, 255, 255))

    # 绘制副标题（浅灰色）
    sub_x = center_x - sub_w / 2
    sub_y = main_y + main_h + 14
    draw.text((sub_x, sub_y), SUB_TITLE, font=sub_font, fill=(220, 220, 220, 255))

    return img


def main():
    print("正在生成封面图...")

    # 1. 加载底图
    if not os.path.exists(RAW_FILE):
        print(f"错误：底图文件不存在: {RAW_FILE}")
        return

    img = Image.open(RAW_FILE)
    print(f"  底图尺寸: {img.size}")

    # 2. 去水印
    print("  去除水印...")
    img = remove_watermark(img)

    # 3. 叠加标题
    print("  叠加标题文字...")
    img = add_title(img)

    # 4. 保存封面
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (0, 0, 0))
        bg.paste(img, mask=img.split()[3])
        bg.save(OUTPUT_FILE, "PNG")
    else:
        img.save(OUTPUT_FILE, "PNG")

    print(f"✓ 封面已生成: {OUTPUT_FILE}")
    print(f"  主标题: {MAIN_TITLE}")
    print(f"  副标题: {SUB_TITLE}")


if __name__ == "__main__":
    main()
