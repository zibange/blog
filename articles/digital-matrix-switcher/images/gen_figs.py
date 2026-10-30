# -*- coding: utf-8 -*-
"""数字矩阵切换器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system        系统架构：N 输入 × M 输出交叉点交换 + 控制/EDID/级联/双电源 （1.2）
  图2 bandwidth-resolution 带宽-分辨率（HDMI2.0 18G 天花板）+ 切换延迟 矩阵 vs IP   （2.1/2.2）
  图3 crosspoint-scale   直连 vs 矩阵布线节省 + 级联等效规模 P_eq=n^2             （2.2）
  图4 scene-topology     指挥大厅多源多屏拓扑（矩阵 + 中控一键预设）              （5）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# 全局字体：不设会让内置 axes 用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- 全局样式（light 主题，浅底深字）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（信号/输入侧）
C2 = "#0E9F6E"   # 绿（交叉点/路由）
C3 = "#E8833A"   # 橙（输出/场景）
C4 = "#C2410C"   # 深橙（告警/临界）
C5 = "#7C3AED"   # 紫（控制/级联/电源）
CGREY = "#CBD2D9"


def newfig():
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


def txt(ax, x, y, s, size=9.4, color=INK, weight="normal", ha="center", va="center", zorder=6):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily="Microsoft YaHei")


def title(ax, t, sub=None):
    txt(ax, W / 2, H - 0.52, t, size=14.6, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.00, sub, size=9.0, color=MUTED, ha="center")


def footer(ax, s):
    """说明条：单独开 axes，避免与绘图区坐标系混用"""
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=1)
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=8.0, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", rad=0.0, zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：系统架构（交叉点交换 + 外围子系统）
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  数字矩阵切换器系统架构：交叉点任意路由 + 外围支撑",
          "N 路输入经均衡重定时进入 N×M 交叉点，任意映射到 M 路输出；控制/EDID/级联/双电源共同支撑")

    # 左侧：输入（大框 + 内部多条输入线示意）
    ibx, iby, ibw, ibh = 0.7, 2.2, 2.1, 4.5
    box(ax, ibx, iby, ibw, ibh, "#EFF6FF", C1, lw=1.8)
    txt(ax, ibx + ibw / 2, iby + ibh - 0.55, "N 路输入", size=11.0, weight="bold", color=C1)
    txt(ax, ibx + ibw / 2, iby + ibh - 1.05, "HDMI / SDI / DP", size=8.4, color=INK)
    for i, yy in enumerate(np.linspace(iby + 0.95, iby + ibh - 1.5, 5)):
        ax.plot([ibx + 0.2, ibx + ibw - 0.2], [yy, yy], color=C1, lw=1.1, alpha=0.5, zorder=3)
    txt(ax, ibx + ibw / 2, iby + 0.45, "基带音视频信号", size=7.8, color=MUTED)

    # 均衡/重定时 小框（输入与交叉点之间顶部）
    ebx, eby, ebw, ebh = 3.15, 5.95, 1.9, 0.95
    box(ax, ebx, eby, ebw, ebh, "#FFFFFF", C5, lw=1.5)
    txt(ax, ebx + ebw / 2, eby + 0.62, "电缆均衡", size=9.6, weight="bold", color=C5)
    txt(ax, ebx + ebw / 2, eby + 0.25, "重定时 reclocking", size=7.8, color=INK)

    # 中间：交叉点大框
    cbx, cby, cbw, cbh = 5.25, 2.2, 3.1, 4.5
    box(ax, cbx, cby, cbw, cbh, "#ECFDF5", C2, lw=2.2)
    txt(ax, cbx + cbw / 2, cby + cbh - 0.55, "交叉点交换", size=12.0, weight="bold", color=C2)
    txt(ax, cbx + cbw / 2, cby + cbh - 1.05, "N×M 任意路由", size=8.6, color=INK)
    # 内部开关网格
    gx0, gy0, gx1, gy1 = cbx + 0.45, cby + 0.55, cbx + cbw - 0.45, cby + cbh - 1.45
    for i in range(4):
        for j in range(3):
            cx = gx0 + (gx1 - gx0) * (i + 0.5) / 4
            cy = gy0 + (gy1 - gy0) * (j + 0.5) / 3
            ax.add_patch(plt.Circle((cx, cy), 0.11, color=C2, alpha=0.55, zorder=3))
            if (i + j) % 2 == 0:  # 示意部分闭合
                ax.plot([cx - 0.06, cx + 0.06], [cy - 0.06, cy + 0.06], color="#0B7A52", lw=1.4, zorder=4)
    txt(ax, cbx + cbw / 2, cby + 0.30, "每个交叉点独立通断", size=7.6, color=MUTED)

    # 右侧：输出
    obx, oby, obw, obh = 10.6, 2.2, 2.1, 4.5
    box(ax, obx, oby, obw, obh, "#FFF7ED", C3, lw=1.8)
    txt(ax, obx + obw / 2, oby + obh - 0.55, "M 路输出", size=11.0, weight="bold", color=C3)
    txt(ax, obx + obw / 2, oby + obh - 1.05, "到显示单元", size=8.4, color=INK)
    for i, yy in enumerate(np.linspace(oby + 0.95, oby + obh - 1.5, 5)):
        ax.plot([obx + 0.2, obx + obw - 0.2], [yy, yy], color=C3, lw=1.1, alpha=0.5, zorder=3)
    txt(ax, obx + obw / 2, oby + 0.45, "屏 / 电视墙 / 录播", size=7.8, color=MUTED)

    # 主箭头：输入 -> 均衡 -> 交叉点 -> 输出
    arrow(ax, ibx + ibw, iby + ibh - 0.55, ebx, eby + 0.47, color=C5, lw=1.4)
    arrow(ax, ebx + ebw, eby + 0.47, cbx, cby + cbh - 0.55, color=C5, lw=1.4)
    arrow(ax, cbx + cbw, cby + cbh - 0.55, obx, oby + obh - 0.55, color=C3, lw=1.6)

    # 底部外环子系统（四个框等距不重叠：0.7-3.2 / 3.9-6.4 / 7.1-9.6 / 10.3-12.8）
    suby = 1.15
    subs = [
        ("控制 IR/RS-232/IP", C5, 0.7),
        ("EDID / HDCP 管理", C4, 3.9),
        ("级联扩展 256×256", C5, 7.1),
        ("双电源 N+1 冗余", C2, 10.3),
    ]
    for name, c, x in subs:
        box(ax, x, suby, 2.5, 0.85, "#FFFFFF", c, lw=1.6)
        txt(ax, x + 1.25, suby + 0.45, name, size=9.2, weight="bold", color=c)
    arrow(ax, 1.95, suby + 0.85, cbx + 0.6, cby, color=C5, lw=1.1, ls="--")
    arrow(ax, 5.15, suby + 0.85, cbx + 1.55, cby, color=C4, lw=1.1, ls="--")
    arrow(ax, 8.35, suby + 0.85, cbx + 2.5, cby, color=C5, lw=1.1, ls="--")
    # 双电源箭头走低位近水平，避免穿过右侧输出框
    arrow(ax, 11.55, suby + 0.85, cbx + cbw - 0.4, cby, color=C2, lw=1.1, ls="--")

    footer(ax, "注：交叉点只转发光通道、不解码，故延迟仅帧级；均衡重定时清零长距离抖动是 4K60 稳定的关键；EDID/HDCP 处理不当是工程黑屏主因。工程基准示意。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：带宽-分辨率 + 切换延迟对照
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  链路带宽随分辨率逼近 HDMI 2.0 天花板，以及切换延迟量级对照",
          "左：1080p60→4K60 8bit 已顶满 18 Gbps；右：矩阵硬切 ≤1 帧 vs IP 软解 ~250 ms")

    # ---- 左图：带宽柱状 ----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    labels = ["1080p60", "4K30", "4K60\n8bit", "4K60\n10bit HDR"]
    vals = [4.46, 8.91, 17.82, 22.28]
    colors = [C1, C1, C2, C4]
    bars = a.bar(range(len(vals)), vals, color=colors, zorder=4, width=0.6)
    for i, v in enumerate(vals):
        a.text(i, v + 0.4, f"{v:.2f}", ha="center", fontsize=8.4, color=INK, weight="bold")
    a.axhline(18.0, color=C4, ls="--", lw=1.3, zorder=3)
    a.text(-0.45, 19.4, "HDMI 2.0 上限 18 Gbps", fontsize=7.8, color=C4, ha="left", weight="bold",
           path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)
    a.set_xticks(range(len(labels)))
    a.set_xticklabels(labels, fontsize=8.2)
    a.set_xlabel("分辨率 / 刷新 / 色深", fontsize=9.0, color=INK)
    a.set_ylabel("链路带宽 (Gbps)", fontsize=9.0, color=INK)
    a.set_ylim(0, 26)
    a.set_xlim(-0.6, 3.6)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)

    # ---- 右图：切换延迟（对数）----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    labs = ["矩阵硬切\n(≤1 帧)", "IP 软解\n(编码+解码)"]
    lats = [16.7, 250.0]
    lat_labs = ["16.7 ms", "250 ms"]
    b.bar([0, 1], lats, color=[C2, C4], width=0.55, zorder=4)
    for i, (v, lab) in enumerate(zip(lats, lat_labs)):
        b.text(i, v * 1.08, lab, ha="center", fontsize=8.6, color=INK, weight="bold")
    b.set_yscale("log")
    b.set_ylim(5, 600)
    b.set_xticks([0, 1])
    b.set_xticklabels(labs, fontsize=8.2)
    b.set_ylabel("切换延迟 (ms, 对数轴)", fontsize=9.0, color=INK)
    b.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.text(0.5, 60, "快约 15 倍", fontsize=9.0, color=C2, ha="center", weight="bold")

    footer(ax, "注：带宽按 B=f_p×24×10/8，4K60 8bit 已逼近 18 Gbps 天花板，10bit HDR 需 HDMI 2.1；延迟为工程典型值，矩阵对齐帧消隐切换。")
    fig.savefig(os.path.join(OUT, "bandwidth-resolution.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：直连 vs 矩阵布线 + 级联等效规模
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  矩阵把布线从 N×M 降到 N+M，级联以 n² 放大等效规模",
          "左：8×8/16×16 直连根数 vs 矩阵根数；右：二级级联等效端口 P_eq=n² 随 n 平方增长")

    # ---- 左图：布线根数（分组柱状）----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    groups = ["8×8", "16×16"]
    direct = [64, 256]
    matrix = [16, 32]
    x = np.arange(len(groups))
    w = 0.36
    a.bar(x - w / 2, direct, w, color=C4, label="直连 N×M", zorder=4)
    a.bar(x + w / 2, matrix, w, color=C2, label="矩阵 N+M", zorder=4)
    for i in range(len(groups)):
        a.text(x[i] - w / 2, direct[i] + 6, str(direct[i]), ha="center", fontsize=8.4, color=C4, weight="bold")
        a.text(x[i] + w / 2, matrix[i] + 6, str(matrix[i]), ha="center", fontsize=8.4, color=C2, weight="bold")
    a.set_xticks(x); a.set_xticklabels(groups, fontsize=8.6)
    a.set_xlabel("矩阵规模", fontsize=9.0, color=INK)
    a.set_ylabel("布线根数", fontsize=9.0, color=INK)
    a.set_xlim(-0.7, 1.6)
    a.set_ylim(0, 300)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.legend(loc="upper left", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)
    # 注记放在 8×8 组上方空白区，避免被 16×16 柱体遮挡
    a.text(0.0, 130, "16×16 省 224 根（约 87.5%）", ha="center", fontsize=8.4,
           color=C2, weight="bold",
           path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)

    # ---- 右图：级联等效规模 ----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    n = np.array([4, 8, 16, 32])
    Peq = n ** 2
    bars = b.bar([str(x) for x in n], Peq, color=C5, zorder=4, width=0.6)
    for bar, v in zip(bars, Peq):
        b.text(bar.get_x() + bar.get_width() / 2, v + 20, str(v), ha="center",
               fontsize=8.4, color=INK, weight="bold")
    b.set_xlabel("单级规模 n（二级级联）", fontsize=9.0, color=INK)
    b.set_ylabel("等效端口数 P_eq = n²", fontsize=9.0, color=INK)
    b.set_ylim(0, 1100)
    b.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)

    footer(ax, "注：左图 N×M 直连需为每源到每屏各拉一根线，矩阵仅 N+M；右图二级 Clos 用 32 台 16×16 即得 256×256 等效，延迟仅加 1 帧。工程演示算例。")
    fig.savefig(os.path.join(OUT, "crosspoint-scale.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：指挥大厅多源多屏拓扑
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  指挥大厅多源多屏拓扑：数字矩阵 + 中控一键预设",
          "多路 HDMI/SDI 源经矩阵任意路由到显示单元，中控下发预设场景，区别于逐根直连")

    # 左侧：信号源（4 个）
    sx, sy0, sw, sh = 0.7, 2.4, 2.3, 0.95
    srcs = [("摄像头 / 监控", C1), ("电脑 / 笔记本", C1), ("会议终端", C1), ("机顶盒 / 解码", C1)]
    for i, (name, c) in enumerate(srcs):
        y = sy0 + i * 1.18
        box(ax, sx, y, sw, sh, "#EFF6FF", c, lw=1.6)
        txt(ax, sx + sw / 2, y + sh / 2, name, size=9.2, weight="bold", color=c)

    # 中间：矩阵
    mbx, mby, mbw, mbh = 5.0, 2.7, 3.2, 4.0
    box(ax, mbx, mby, mbw, mbh, "#ECFDF5", C2, lw=2.2)
    txt(ax, mbx + mbw / 2, mby + mbh - 0.5, "数字矩阵", size=12.5, weight="bold", color=C2)
    txt(ax, mbx + mbw / 2, mby + mbh - 1.0, "32×32 等效（级联）", size=8.4, color=INK)
    # 内部交叉点示意
    gx0, gy0, gx1, gy1 = mbx + 0.4, mby + 0.55, mbx + mbw - 0.4, mby + mbh - 1.4
    for i in range(5):
        for j in range(4):
            cx = gx0 + (gx1 - gx0) * (i + 0.5) / 5
            cy = gy0 + (gy1 - gy0) * (j + 0.5) / 4
            ax.add_patch(plt.Circle((cx, cy), 0.09, color=C2, alpha=0.5, zorder=3))
    txt(ax, mbx + mbw / 2, mby + 0.32, "任意路由 · 帧级切换", size=7.8, color=MUTED)

    # 右侧：显示单元（2×3 网格，收窄并左移避免出右界）
    dx0, dy0, dw, dh, gap = 9.35, 2.6, 1.05, 1.05, 0.22
    screen_x = []
    screen_y = []
    for r in range(2):
        for c in range(3):
            x = dx0 + c * (dw + gap)
            y = dy0 + r * (dh + gap)
            screen_x.append(x)
            screen_y.append(y)
            box(ax, x, y, dw, dh, "#FFF7ED", C3, lw=1.5)
            txt(ax, x + dw / 2, y + dh / 2, "屏", size=9.0, color=C3, weight="bold")

    # 源 -> 矩阵（下源进下口，序一致不交叉）
    for i, (name, c) in enumerate(srcs):
        y = sy0 + i * 1.18 + sh / 2
        arrow(ax, sx + sw, y, mbx, mby + 0.55 + i * 0.85, color=C1, lw=1.3)

    # 矩阵 -> 显示单元：先汇入右侧竖向总线，再水平短箭头进各屏（避免箭头穿屏）
    bus_x = 9.05
    bus_ymin = screen_y[0] + 0.15
    bus_ymax = screen_y[3] + dh - 0.15
    ax.plot([bus_x, bus_x], [bus_ymin, bus_ymax], color=C3, lw=2.0, alpha=0.55, zorder=3)
    # 矩阵右侧三个出口 -> 总线（上/中/下，序一致不交叉）
    exits = [mby + mbh - 0.7, mby + mbh / 2, mby + 0.7]
    bus_targets = [bus_ymax - 0.2, (bus_ymin + bus_ymax) / 2, bus_ymin + 0.2]
    for ye, yb in zip(exits, bus_targets):
        arrow(ax, mbx + mbw, ye, bus_x, yb, color=C3, lw=1.2)
    # 总线 -> 各屏（水平）
    for x, y in zip(screen_x, screen_y):
        arrow(ax, bus_x, y + dh / 2, x, y + dh / 2, color=C3, lw=1.1)

    # 底部：中控
    cx0, cyb, cwid, chh = 5.0, 1.1, 3.2, 0.85
    box(ax, cx0, cyb, cwid, chh, "#FFFFFF", C5, lw=1.7)
    txt(ax, cx0 + cwid / 2, cyb + 0.45, "中控（RS-232 / IP）一键预设", size=9.0, weight="bold", color=C5)
    arrow(ax, cx0 + cwid / 2, cyb + chh, mbx + mbw / 2, mby, color=C5, lw=1.3, ls="--")

    footer(ax, "注：中控把「哪几路源上哪几块屏」存成场景预设，一键秒切；源与屏只各连矩阵一次，免逐根直连。指挥大厅典型拓扑。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
