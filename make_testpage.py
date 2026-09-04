# -*- coding: utf-8 -*-
# 生成 A4 防堵墨测试页 PDF（跨平台：Windows 本地 / Linux GitHub Runner）
from PIL import Image, ImageDraw, ImageFont
import datetime, os, glob

W, H = 2480, 3508  # A4 @ 300dpi
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def find_font(bold=False):
    if os.name == 'nt':  # Windows
        return "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    cands = [
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    for p in glob.glob("/usr/share/fonts/**/*CJK*.ttc", recursive=True):
        return p
    return None


def font(size, bold=False):
    p = find_font(bold)
    if p:
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()


img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

M = 150
content_w = W - 2 * M
title_f = font(90, bold=True)
sub_f = font(50)
small_f = font(36)

# 标题
d.text((M, 120), "Epson L4260 喷头防堵测试页", font=title_f, fill=BLACK)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
d.text((M, 250), "打印时间: " + now, font=sub_f, fill=BLACK)

# 四色块（CMYK 检测）
swatch_y = 380
swatch_h = int(H * 0.14)
gap = 40
swatch_w = (content_w - gap * 3) // 4
colors = [(0, 0, 0), (0, 180, 180), (200, 0, 150), (250, 210, 0)]
names = ["Black 黑", "Cyan 青", "Magenta 洋红", "Yellow 黄"]
for i in range(4):
    x = M + i * (swatch_w + gap)
    d.rectangle([x, swatch_y, x + swatch_w, swatch_y + swatch_h], fill=colors[i])
    d.text((x, swatch_y + swatch_h + 20), names[i], font=small_f, fill=BLACK)

# 灰度渐变条
grad_y = swatch_y + swatch_h + 120
grad_h = int(H * 0.05)
for i in range(content_w):
    v = int(255 * i / content_w)
    d.line([(M + i, grad_y), (M + i, grad_y + grad_h)], fill=(v, v, v))
d.text((M, grad_y + grad_h + 15), "灰度渐变（检测黑色喷头）", font=small_f, fill=BLACK)

# 喷嘴检测网格
grid_y = grad_y + grad_h + 110
grid_bottom = H - 250
step = 60
for x in range(M, M + content_w + 1, step):
    d.line([(x, grid_y), (x, grid_bottom)], fill=BLACK, width=3)
for y in range(grid_y, grid_bottom + 1, step):
    d.line([(M, y), (M + content_w, y)], fill=BLACK, width=3)
d.text((M, grid_y - 60), "喷嘴检测网格（出现断线说明对应喷嘴堵塞）", font=small_f, fill=BLACK)

# 底部
d.text((M, H - 180), "每周自动打印 · 防喷头堵墨", font=small_f, fill=(120, 120, 120))

img.save("testpage.png")
img.save("testpage.pdf", "PDF", resolution=300)
print("PDF OK")
