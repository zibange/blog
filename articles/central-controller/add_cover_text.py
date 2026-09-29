# -*- coding: utf-8 -*-
"""封面文字叠加：主标题左上，副标题底部深色带（同时覆盖右下水印）。"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

SRC = r"d:\AiPython\zhinengshebei\智能中控网关\images\cover.jpg"
DST = r"d:\AiPython\zhinengshebei\智能中控网关\images\cover.png"

def font(sz, path):
    for p in [path, r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc",
              r"C:\Windows\Fonts\Deng.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                continue
    return ImageFont.load_default()

im = Image.open(SRC).convert("RGB")
W, H = im.size
d = ImageDraw.Draw(im, "RGBA")

# —— 底部副标题深色带（覆盖右下水印）——
band_h = int(H * 0.16)
band = Image.new("RGBA", (W, band_h), (10, 20, 45, 150))
im.paste(band, (0, H - band_h))
# 圆角打磨（用蒙版使带边缘柔和）
m = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(m)
md.rectangle([0, H - band_h, W, H], fill=255)
blur_r = int(H * 0.02)
m = m.filter(ImageFilter.GaussianBlur(blur_r))
im.paste(band, (0, H - band_h), m.crop((0, H - band_h, W, H)))

# —— 副标题文字 ——
f_sub = font(int(H * 0.032), r"C:\Windows\Fonts\msyh.ttc")
d = ImageDraw.Draw(im)
sub = "面向工程端 · 智能楼宇 / 办公园区 联动控制中枢"
d.text((int(W*0.045), H - band_h + int(band_h*0.30)), sub, font=f_sub, fill=(226, 236, 255, 255))
tag = "产品综述 · 选型与落地视角"
d.text((int(W*0.045), H - band_h + int(band_h*0.62)), tag, font=font(int(H*0.026), r"C:\Windows\Fonts\msyh.ttc"),
       fill=(191, 224, 255, 255))

# —— 主标题（左上纯净区，先深色半透明底衬再白字）——
t = "智能中控网关"
f_main = font(int(H * 0.075), r"C:\Windows\Fonts\msyhbd.ttc")
tl = int(W*0.06); top = int(H*0.10)
bbox = d.textbbox((0, 0), t, font=f_main)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
d.rounded_rectangle([tl - int(W*0.012), top - int(H*0.012),
                     tl + tw + int(W*0.012), top + th + int(H*0.012)],
                    radius=int(H*0.012), fill=(8, 18, 42, 165))
d.text((tl, top), t, font=f_main, fill=(244, 248, 255, 255))

im.save(DST)
print("saved", DST, im.size)