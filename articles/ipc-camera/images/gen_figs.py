# -*- coding: utf-8 -*-
"""网络摄像机（IPC）产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system         IPC 六块架构：光学/传感器/ISP/编码SoC/网络/结构（1.4）
  图2 imaging-dori        DORI 四级像素密度与识别距离（2.2 算例 1~3）
  图3 bandwidth-storage   码率—存储—PoE 预算三角（2.2 算例 4~6）
  图4 scene-topology      四类落地场景共用「取像→ISP→编码→网络输出」前端链（六）

配色、坐标系用法沿用成熟模板：
  - newfig() 用整幅画布当一个 axes（0~W, 0~H），画图区与说明条分离
  - footer() 单独开一个 add_axes（图幅比例），不混用 tight 裁剪
  - 全局字体 Microsoft YaHei，避免中文/全角符号变空白
  - 戒用 ↔(U+2194)/✓/≪/⁻¹ 等 Microsoft YaHei 无字形字符
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# 全局字体：不设的话内置坐标轴（刻度/图例/标题）会用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- light 主题配色（浅底深字）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（光学/成像）
C2 = "#0E9F6E"   # 绿（处理/网络）
C3 = "#E8833A"   # 橙（编码/码率）
C4 = "#C2410C"   # 深橙（临界/DORI高等级）
C5 = "#7C3AED"   # 紫（结构/ISP）
CGREY = "#CBD2D9"


def newfig():
    """整幅画布当成一个坐标轴，数据坐标 0~W / 0~H，便于精确定位框线。"""
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       alpha=alpha, linestyle=ls, zorder=2)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=9.4, color=INK, weight="normal",
        ha="center", va="center", zorder=6):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily="Microsoft YaHei")


def title(ax, t, sub=None):
    txt(ax, W / 2, H - 0.52, t, size=14.2, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.00, sub, size=8.8, color=MUTED, ha="center")


def footer(ax, s):
    """说明条单独开 axes，避免与绘图区坐标系混用导致错位。"""
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=1)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=7.3, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：IPC 六块架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  IPC 内部架构：光学 + 成像 + 处理 + 编码 + 网络 + 结构",
          "光经镜头成像、CMOS 转电、ISP 处理、SoC 编码，最后经网口以 PoE 供电并输出码流")

    # 上排三块：光学 → 传感器 → ISP
    blocks_top = [
        ("光学镜头", C1, "#EFF6FF", ["定焦/变焦镜头", "决定视场角", "光圈 F 值", "进光量"]),
        ("CMOS 传感器", C1, "#EFF6FF", ["1/2.8 / 1/1.8 靶面", "光电转换", "像元尺寸", "决定低照度"]),
        ("ISP 图像处理", C5, "#F5F3FF", ["AE / AWB", "WDR 宽动态", "3D 降噪", "ICR 日夜切换"]),
    ]
    bx, bw, gap = 0.45, 3.55, 0.72
    ty, bh = 4.75, 2.65
    for i, (name, c, fill, items) in enumerate(blocks_top):
        x = bx + i * (bw + gap)
        box(ax, x, ty, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, ty + bh - 0.45, name, size=11.2, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = ty + bh - 1.10 - j * 0.42
            txt(ax, x + bw / 2, yy, it, size=8.6, color=INK)
    ay = ty + bh / 2
    for i in range(2):
        arrow(ax, bx + i * (bw + gap) + bw, ay,
              bx + (i + 1) * (bw + gap), ay, color=MUTED, lw=1.6)

    # 下排三块：编码 SoC → 网络接口 → 结构护罩
    blocks_bot = [
        ("编码 SoC", C3, "#FFF7ED", ["H.264/H.265/SVAC", "码率控制", "前端智能分析", "主/子码流"]),
        ("网络接口", C2, "#ECFDF5", ["RJ45 网口", "PoE 受电", "GB28181/ONVIF", "TF 卡本地存储"]),
        ("结构护罩", C4, "#FFF1EE", ["枪机/半球/球机", "IP66/IK10 防护", "红外灯板", "安装支架"]),
    ]
    by = 1.75
    for i, (name, c, fill, items) in enumerate(blocks_bot):
        x = bx + i * (bw + gap)
        box(ax, x, by, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, by + bh - 0.45, name, size=11.2, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = by + bh - 1.10 - j * 0.42
            txt(ax, x + bw / 2, yy, it, size=8.6, color=INK)
    ay2 = by + bh / 2
    for i in range(2):
        arrow(ax, bx + i * (bw + gap) + bw, ay2,
              bx + (i + 1) * (bw + gap), ay2, color=MUTED, lw=1.6)

    # 上排 ISP → 下排 编码 SoC：竖向连接（从 ISP 底部到 SoC 顶部，同列 x）
    isp_cx = bx + 2 * (bw + gap) + bw / 2          # ISP 中心 x
    soc_cx = bx + bw / 2                            # 编码 SoC 中心 x
    # 走右侧下降再水平回到 SoC 顶：用两段折线箭头（走空白通道，不穿框）
    arrow(ax, isp_cx, ty, isp_cx, by + bh + 0.25, color=C5, lw=1.4)
    arrow(ax, isp_cx, by + bh + 0.25, soc_cx, by + bh + 0.25, color=C5, lw=1.4, ls="--")
    arrow(ax, soc_cx, by + bh + 0.25, soc_cx, by + bh, color=C5, lw=1.4)

    # 底部输出：码流去向
    ox, oy, ow, oh = 3.0, 0.72, 7.2, 0.62
    box(ax, ox, oy, ow, oh, "#F6F8FA", CGREY, lw=1.1)
    txt(ax, ox + ow / 2, oy + oh / 2,
        "交换机 → NVR 存储 / VMS 平台 / 解码上墙 / 云端（数字码流，一根网线供电+传数据）",
        size=8.4, color=MUTED)
    net_cx = bx + 1 * (bw + gap) + bw / 2
    arrow(ax, net_cx, by, net_cx, oy + oh, color=C2, lw=1.4)

    footer(ax, "注：镜头焦距与靶面定识别距离，光圈与传感器定夜视，ISP 定逆光能否看清，编码定带宽存储，PoE 定供电距离。六块互相牵制，选型需整体权衡。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：DORI 四级像素密度与识别距离
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  DORI 像素密度与识别距离：同一台摄像机差十倍",
          "由 d = N(px)·f / (w(s)·rho) 反推；2MP / 4 mm / 靶面 5.57 mm，四级距离按 1/rho 缩放")

    # 左边界留足空间给 yticklabels（DORI 中文标签较长），否则首字被裁
    px, py, pw, ph = 2.15, 1.85, 10.05, 5.15
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")

    # 四级 DORI：侦测25/观察63/识别125/辨认250 px/m
    levels = [
        ("侦测 Detect", 25, 55.2, C2, "#ECFDF5"),
        ("观察 Observe", 63, 21.9, C1, "#EFF6FF"),
        ("识别 Recognize", 125, 11.0, C3, "#FFF7ED"),
        ("辨认 Identify", 250, 5.5, C4, "#FFF1EE"),
    ]
    names = [l[0] for l in levels]
    dists = [l[2] for l in levels]
    colors = [l[3] for l in levels]
    y = np.arange(len(levels))
    bars = a.barh(y, dists, color=colors, height=0.62, zorder=3)
    # 距离标签（按柱宽反推位置，右侧留白）
    for i, (bar, d) in enumerate(zip(bars, dists)):
        a.text(d + 0.9, bar.get_y() + bar.get_height() / 2,
               f"{d} m", va="center", ha="left", fontsize=9.6,
               color=INK, weight="bold", zorder=5)
        # 像素密度标注放柱内左侧
        a.text(1.0, bar.get_y() + bar.get_height() / 2,
               f"{levels[i][1]} px/m", va="center", ha="left", fontsize=8.6,
               color="white", weight="bold", zorder=5,
               path_effects=[pe.withStroke(linewidth=2.8, foreground=colors[i])])
    a.set_yticks(y)
    a.set_yticklabels(names, fontsize=9.8, color=INK)
    a.invert_yaxis()
    a.set_xlim(0, 66)
    a.set_xlabel("该级别下的最远可用距离 (m)", fontsize=9.2, color=INK)
    a.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="x", labelsize=8.2, colors=MUTED)

    # 提示框放 axes 内的相对坐标右下空白处（不压柱、不压 x 轴刻度）
    a.text(0.70, 0.12, "分辨率 2MP → 8MP\n各级别距离整体约翻倍",
           transform=a.transAxes, fontsize=8.0, color=C4, weight="bold",
           ha="center", va="center",
           bbox=dict(boxstyle="round,pad=0.35", fc="#FFF7ED", ec=C3, alpha=0.95), zorder=6)

    footer(ax, "注：DORI 源自 IEC 62676-4（人脸宽 16 cm），距离与所需像素密度成反比。厂商标称最远距离多为侦测级，按辨认级选型时距离约为其十分之一，务必按业务需要锁定级别。")
    fig.savefig(os.path.join(OUT, "imaging-dori.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：码率—存储—PoE 预算三角
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  码率—存储—PoE 预算：一台摄像机能否落地的三道账",
          "码率定带宽与硬盘，供电方式定能否一根网线交付；三者共同约束选型")

    # --- 左：编码格式省一半存储（柱状） ---
    lx, ly, lw, lh = 0.6, 2.0, 3.55, 4.9
    a = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a.set_facecolor("#FFFFFF")
    fmt = ["H.264\n8 Mbps", "H.265\n4 Mbps"]
    cap = [31.6, 15.8]   # 100路30天 TB
    bars = a.bar(fmt, cap, color=[CGREY, C2], width=0.55, zorder=3)
    for bar, v in zip(bars, cap):
        a.text(bar.get_x() + bar.get_width() / 2, v + 0.6,
               f"{v} TB", ha="center", va="bottom", fontsize=9.6,
               color=INK, weight="bold", zorder=5)
    a.annotate("省约一半", xy=(1, 17.2), xytext=(0.55, 30),
               fontsize=9.0, color=C4, weight="bold", ha="center",
               arrowprops=dict(arrowstyle="->", color=C4, lw=1.3))
    a.set_ylim(0, 38)
    a.set_ylabel("100 路 × 30 天存储 (TB)", fontsize=8.8, color=INK)
    a.set_title("① 编码定存储", fontsize=10.2, color=C1, weight="bold", pad=8)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.2, colors=MUTED)

    # --- 中：带宽能带几路（纵向柱，避免横向标签互相压）---
    mx, mw = 4.5, 3.55
    b = fig.add_axes([mx / W, ly / H, mw / W, lh / H])
    b.set_facecolor("#FFFFFF")
    ports = ["百兆口", "千兆口"]
    routes = [17, 177]
    bb = b.bar(ports, routes, color=[C3, C2], width=0.5, zorder=3)
    for bar, v in zip(bb, routes):
        b.text(bar.get_x() + bar.get_width() / 2, v + 3,
               f"{v} 路", ha="center", va="bottom", fontsize=9.6,
               color=INK, weight="bold", zorder=5)
    b.text(0.5, 0.93, "按 80% 可用带宽", transform=b.transAxes,
           ha="center", va="top", fontsize=8.0, color=MUTED, zorder=6)
    b.set_ylim(0, 210)
    b.set_ylabel("")
    b.set_title("② 带宽定路数（4MP 路数）", fontsize=10.2, color=C1, weight="bold", pad=8)
    b.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(axis="both", labelsize=8.2, colors=MUTED)

    # --- 右：PoE 功率阶梯（柱状，横向） ---
    rx, rw = 8.65, 3.95
    c = fig.add_axes([rx / W, ly / H, rw / W, lh / H])
    c.set_facecolor("#FFFFFF")
    poe = ["802.3af", "802.3at", "802.3bt\nT3", "802.3bt\nT4"]
    pwr = [12.95, 25.5, 51, 71]
    yc = np.arange(len(poe))
    cols = [CGREY, C1, C3, C4]
    bc = c.barh(yc, pwr, color=cols, height=0.58, zorder=3)
    for bar, v in zip(bc, pwr):
        c.text(v + 0.8, bar.get_y() + bar.get_height() / 2,
               f"{v} W", va="center", ha="left", fontsize=9.2,
               color=INK, weight="bold", zorder=5)
    c.set_yticks(yc)
    c.set_yticklabels(poe, fontsize=8.4, color=INK)
    c.tick_params(axis="y", pad=6)
    c.invert_yaxis()
    c.set_xlim(0, 88)
    c.set_xlabel("受电端最大功率 (W)", fontsize=8.8, color=INK)
    c.set_title("③ 供电定机型", fontsize=10.2, color=C1, weight="bold", pad=8)
    c.text(0.52, 0.055, "百米末端压降约 4~5 V，线损约 2~3 W",
           transform=c.transAxes, fontsize=7.6, color=MUTED, ha="center", va="bottom",
           bbox=dict(boxstyle="round,pad=0.25", fc="#F6F8FA", ec=GRID, alpha=0.95), zorder=6)
    c.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in c.spines.values():
        sp.set_color(GRID)
    c.tick_params(axis="x", labelsize=8.2, colors=MUTED)

    footer(ax, "注：单路按主码流 4 Mbps + 子码流 0.5 Mbps 估算；存储按 100 路×30 天、H.265 省一半；PoE 为受电端功率。球机（云台+加热）需 802.3bt 或本地供电。")
    fig.savefig(os.path.join(OUT, "bandwidth-storage.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：四类场景拓扑，共用前端取像链
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  四类落地场景：同一条「取像—ISP—编码—网络输出」前端链",
          "周界夜视、出入口取证、连锁巡店、广场追踪，差异只在镜头、照度与码率配置")

    # 左侧：前端链路主框
    ox, oy, ow, oh = 0.45, 2.9, 3.2, 3.1
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.5, "IPC 前端链", size=11.4, weight="bold", color=C1)
    chain = ["镜头取像", "ISP 处理", "SoC 编码", "PoE + 网口输出"]
    for i, s in enumerate(chain):
        # 步长 0.54，起点下移量 1.05：最后子框(i=3)底 yy-0.18 = oy+0.39，稳在主框内
        yy = oy + oh - 1.05 - i * 0.54
        box(ax, ox + 0.3, yy - 0.18, ow - 0.6, 0.46, "#FFFFFF", C1, lw=1.0)
        txt(ax, ox + ow / 2, yy + 0.05, s, size=8.8, color=INK)
        if i < len(chain) - 1:
            arrow(ax, ox + ow / 2, yy - 0.2, ox + ow / 2, yy - 0.54,
                  color=C1, lw=1.0, ms="-|>")

    # 右侧四个场景框（竖排）
    scenes = [
        ("周界夜视", "低照度+红外枪机 · 前端越界侦测", C2, "#ECFDF5", 5.95),
        ("出入口取证", "长焦高密度+真WDR · 人脸/车牌", C4, "#FFF1EE", 4.60),
        ("连锁巡店", "PoE半球+主子码流 · 带宽分级", C3, "#FFF7ED", 3.25),
        ("广场追踪", "球机PTZ+全景拼接 · 前端结构化", C5, "#F5F3FF", 1.90),
    ]
    sx, sw, sh = 5.3, 7.45, 1.08
    for name, desc, c, fill, sy in scenes:
        box(ax, sx, sy, sw, sh, fill, c, lw=1.7)
        txt(ax, sx + 0.28, sy + sh - 0.34, name, size=10.2, weight="bold", color=c, ha="left")
        txt(ax, sx + 0.28, sy + 0.34, desc, size=8.8, color=INK, ha="left")
        arrow(ax, ox + ow, oy + oh / 2, sx, sy + sh / 2, color=CGREY, lw=1.2)

    # 底部：输出链路说明条
    bx, by, bw, bh = 0.45, 0.68, 12.3, 0.78
    box(ax, bx, by, bw, bh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, bx + bw / 2, by + bh / 2,
        "统一输出链：数字码流  →  交换机汇聚  →  NVR 存储 / VMS 平台 / 解码上墙 / 云端智能分析",
        size=8.8, color=INK)

    footer(ax, "注：四类场景底层都是同一套前端取像链，差异只在镜头焦距、传感器照度与码率配置——按业务需要锁定 DORI 级别与夜视方案，再算带宽供电，即可落地。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
