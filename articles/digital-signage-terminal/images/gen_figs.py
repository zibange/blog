# -*- coding: utf-8 -*-
"""信息发布终端产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system          系统架构：CMS 中心 + 网络 + 终端一体机 + 电源散热 四域   （1.4）
  图2 brightness-ambient   亮度-环境照度对比度 + 视距-像素间距                          （2.2 算例3/4）
  图3 storage-bandwidth    循环缓存容量 vs 存储档 + 日下发带宽随终端数                （2.2 算例1/2）
  图4 scene-topology       多网点拓扑：CMS 中心 → 边缘网关 → 各终端分组               （五/六 场景）
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
C1 = "#1F6FEB"   # 主蓝（CMS/中心侧）
C2 = "#0E9F6E"   # 绿（终端/路由）
C3 = "#E8833A"   # 橙（显示/场景）
C4 = "#C2410C"   # 深橙（告警/临界）
C5 = "#7C3AED"   # 紫（网络/电源）
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
# 图 1：系统架构（四域）
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  信息发布终端系统架构：CMS 中心 + 网络 + 终端一体机 + 电源散热",
          "排期与素材由中心下发、状态由终端回传；终端本体 = 播放器主板 + 显示屏 + 壳体散热")

    # 左：CMS 中心
    cbx, cby, cbw, cbh = 0.7, 2.3, 3.0, 4.6
    box(ax, cbx, cby, cbw, cbh, "#EFF6FF", C1, lw=2.0)
    txt(ax, cbx + cbw / 2, cby + cbh - 0.5, "CMS 中心", size=12.0, weight="bold", color=C1)
    txt(ax, cbx + cbw / 2, cby + cbh - 1.0, "私有化 / SaaS", size=8.4, color=INK)
    cms_items = ["素材库", "排期引擎", "监播看板", "分组 / 权限"]
    for i, it in enumerate(cms_items):
        yy = cby + cbh - 1.7 - i * 0.72
        box(ax, cbx + 0.35, yy, cbw - 0.7, 0.55, "#FFFFFF", C1, lw=1.2)
        txt(ax, cbx + cbw / 2, yy + 0.28, it, size=9.0, color=INK)

    # 中：网络层
    nbx, nby, nbw, nbh = 4.05, 3.7, 1.65, 1.9
    box(ax, nbx, nby, nbw, nbh, "#FBF5FF", C5, lw=1.7)
    txt(ax, nbx + nbw / 2, nby + nbh - 0.42, "网络层", size=10.5, weight="bold", color=C5)
    txt(ax, nbx + nbw / 2, nby + 0.75, "有线/WiFi", size=8.0, color=INK)
    txt(ax, nbx + nbw / 2, nby + 0.42, "4G / 5G", size=8.0, color=INK)

    # 右：终端一体机（大框 + 内部三块）
    tbx, tby, tbw, tbh = 6.2, 2.3, 4.0, 4.6
    box(ax, tbx, tby, tbw, tbh, "#ECFDF5", C2, lw=2.2)
    txt(ax, tbx + tbw / 2, tby + tbh - 0.5, "信息发布终端（一体机）", size=11.5, weight="bold", color=C2)
    inner = [
        ("播放器主板 SoC+VPU+存储", 5.55),
        ("合成与排期引擎", 4.45),
        ("显示屏 LCD / OLED", 3.35),
        ("壳体 + 强制风冷", 2.55),
    ]
    for name, cy in inner:
        box(ax, tbx + 0.35, cy, tbw - 0.7, 0.62, "#FFFFFF", C2, lw=1.3)
        txt(ax, tbx + tbw / 2, cy + 0.31, name, size=9.2, color=INK)

    # 最右：显示输出 + 电源
    obx, oby, obw, obh = 10.7, 2.3, 1.95, 4.6
    box(ax, obx, oby, obw, obh, "#FFF7ED", C3, lw=1.7)
    txt(ax, obx + obw / 2, oby + obh - 0.5, "输出 / 供电", size=10.5, weight="bold", color=C3)
    box(ax, obx + 0.25, oby + 2.7, obw - 0.5, 0.9, "#FFFFFF", C3, lw=1.3)
    txt(ax, obx + obw / 2, oby + 3.15, "屏幕输出", size=9.0, color=INK)
    box(ax, obx + 0.25, oby + 1.1, obw - 0.5, 0.9, "#FFFFFF", C4, lw=1.3)
    txt(ax, obx + obw / 2, oby + 1.55, "220V + 风冷", size=9.0, color=C4)

    # 主箭头：CMS -> 网络 -> 终端 -> 输出
    arrow(ax, cbx + cbw, cby + cbh - 2.2, nbx, nby + nbh / 2, color=C5, lw=1.5)
    arrow(ax, nbx + nbw, nby + nbh / 2, tbx, tby + tbh - 2.2, color=C2, lw=1.6)
    arrow(ax, tbx + tbw, tby + tbh - 2.2, obx, oby + 3.15, color=C3, lw=1.5)

    # 底部：终端回传能力
    suby = 1.15
    subs = [
        ("断网续播（本地缓存）", C2, 0.7),
        ("心跳上报 / 在线率", C1, 4.0),
        ("远程控制 / 日志", C5, 7.3),
        ("MD5 一致性校验", C4, 10.6),
    ]
    for name, c, x in subs:
        box(ax, x, suby, 2.5, 0.85, "#FFFFFF", c, lw=1.5)
        txt(ax, x + 1.25, suby + 0.45, name, size=8.8, weight="bold", color=c)
    arrow(ax, 1.95, suby + 0.85, tbx + 0.8, tby, color=C2, lw=1.1, ls="--")
    arrow(ax, 5.25, suby + 0.85, tbx + 1.7, tby, color=C1, lw=1.1, ls="--")
    arrow(ax, 8.55, suby + 0.85, tbx + 2.6, tby, color=C5, lw=1.1, ls="--")
    arrow(ax, 11.85, suby + 0.85, tbx + 3.4, tby, color=C4, lw=1.1, ls="--")

    footer(ax, "注：一体机本体含播放器主板（硬解+合成+排期）、显示屏、壳体与散热；CMS 下发排期/素材，终端回传心跳/监播/哈希。四域解耦便于分级运维。工程基准示意。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：亮度-环境照度 + 视距-像素间距
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  亮度须随环境照度抬升，视距由像素间距与字号决定",
          "左：不同场景最小可读屏亮（对数轴）；右：24 px 标题最小视距随像素间距变化")

    # ---- 左图：最小屏亮（对数轴）----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    labels = ["室内暗厅\n300 lx", "靠窗营业厅\n1500 lx", "半户外\n5000 lx", "户外直射\n30000 lx"]
    vals = [24, 119, 398, 2390]
    colors = [C1, C3, C4, C4]
    bars = a.bar(range(len(vals)), vals, color=colors, zorder=4, width=0.6)
    for i, v in enumerate(vals):
        a.text(i, v * 1.15, f"{v}", ha="center", fontsize=8.4, color=INK, weight="bold")
    a.set_yscale("log")
    a.set_ylim(10, 5000)
    a.set_xticks(range(len(labels)))
    a.set_xticklabels(labels, fontsize=8.0)
    a.set_ylabel("最小可读屏亮 (cd/m², 对数轴)", fontsize=9.0, color=INK)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    # 用 legend 标注常用屏亮档（避免两线间贴字被裁）
    a.axhline(500, color=C1, ls="--", lw=1.2, zorder=3)
    a.axhline(1500, color=C4, ls="--", lw=1.2, zorder=3)
    a.plot([], [], color=C1, ls="--", label="室内屏 300–700 档")
    a.plot([], [], color=C4, ls="--", label="靠窗/半户外 800–2000 档")
    a.legend(loc="upper left", fontsize=7.8, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    # ---- 右图：视距 vs 像素间距（24 px 标题）---
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    p = np.array([0.1, 0.2, 0.315, 0.5, 0.8])  # 像素间距 mm
    theta = 0.3 * np.pi / 180.0
    Dmin = 24 * p / (2 * np.tan(theta)) / 1000.0  # 米
    b.plot(p, Dmin, color=C2, lw=2.2, marker="o", ms=6, zorder=4)
    for pp, dd in zip(p, Dmin):
        b.annotate(f"{dd:.2f} m", (pp, dd), textcoords="offset points",
                   xytext=(6, -2), fontsize=8.0, color=INK)
    b.set_xlabel("像素间距 p (mm)", fontsize=9.0, color=INK)
    b.set_ylabel("最小视距 D_min (m, 24 px 标题)", fontsize=9.0, color=INK)
    b.set_xlim(0.05, 0.9)
    b.set_ylim(0, 3.2)
    b.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.text(0.5, 2.7, "55″ 4K: p≈0.315 mm → 最近约 0.72 m", fontsize=8.4,
           color=C2, ha="center", weight="bold")

    footer(ax, "注：左图按 L_min=C_r·E_amb·ρ/π（C_r=5, ρ=0.05），靠窗/半户外需 800–2000 cd/m² 室内屏才达标；右图 D_min=h_px·p/(2·tanθ_min)，θ_min≈0.3°。工程演示算例。")
    fig.savefig(os.path.join(OUT, "brightness-ambient.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：存储容量 vs 存储档 + 日下发带宽
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  循环缓存容量压着 32 GB 临界，中心下发带宽随终端数线性增长",
          "左：7 天循环需 25.2 GB，16 GB 不足、32 GB 临界、64 GB 舒适；右：日更 2 GB 下带宽随终端数")

    # ---- 左图：存储档 ----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    groups = ["需求\n25.2GB", "16 GB\n(不足)", "32 GB\n(临界)", "64 GB\n(舒适)"]
    vals = [25.2, 16, 32, 64]
    colors = [C4, C4, C3, C2]
    bars = a.bar(range(len(vals)), vals, color=colors, zorder=4, width=0.6)
    for i, v in enumerate(vals):
        a.text(i, v + 1.5, str(v), ha="center", fontsize=8.6, color=INK, weight="bold")
    a.set_xticks(range(len(groups)))
    a.set_xticklabels(groups, fontsize=8.2)
    a.set_ylabel("容量 (GB)", fontsize=9.0, color=INK)
    a.set_ylim(0, 75)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.text(1.5, 40, "16 GB 差 9.2 GB → 爆盘", ha="center", fontsize=8.2, color=C4,
           weight="bold", path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)

    # ---- 右图：下发带宽随终端数 ----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    N = np.array([50, 200, 800])
    B = N * 2 * 8000 / 7200.0  # Mbps
    bars = b.bar([str(n) for n in N], B, color=C5, zorder=4, width=0.55)
    for bar, v in zip(bars, B):
        b.text(bar.get_x() + bar.get_width() / 2, v + 30, f"{v:.0f}", ha="center",
               fontsize=8.6, color=INK, weight="bold")
    b.set_xlabel("终端数 N（日更 2 GB / 2h 窗口）", fontsize=9.0, color=INK)
    b.set_ylabel("中心下发带宽 (Mbps)", fontsize=9.0, color=INK)
    b.set_ylim(0, 2100)
    b.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.text(1.0, 1500, "800 店 ≈ 1.78 Gbps\n需 CDN 边缘分摊", ha="center", fontsize=8.4,
           color=C5, weight="bold", path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)

    footer(ax, "注：左图 C=R·T·N·D/8000=20×60×24×7/8000≈25.2 GB（R=20Mbps,T=60s,N=24次,D=7天），32 GB 是临界档；右图 B=N·S·8000/t_win，终端数每翻 10 倍带宽翻 10 倍。工程演示算例。")
    fig.savefig(os.path.join(OUT, "storage-bandwidth.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：多网点拓扑（CMS 中心 → 边缘 → 终端分组）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  多网点发布拓扑：CMS 中心统一编排，边缘网关落地到各终端分组",
          "营业厅/门店/医院各分组本地缓存 + 断网续播，中心只看在线率与一致性")

    # 顶部：CMS 中心（mcy=6.05，给副标题 y≈7.6 留出空间，避免压字）
    mcx, mcy, mcw, mch = 4.6, 6.05, 4.0, 1.1
    box(ax, mcx, mcy, mcw, mch, "#EFF6FF", C1, lw=2.2)
    txt(ax, mcx + mcw / 2, mcy + mch - 0.42, "CMS 中心（统一排期/素材/监播）", size=10.6, weight="bold", color=C1)
    txt(ax, mcx + mcw / 2, mcy + 0.42, "私有化 / SaaS · 分组管理 · 权限", size=8.2, color=INK)

    # 中部：三个边缘网关
    gws = [
        ("营业厅分组", C1, 0.7),
        ("门店分组", C2, 5.0),
        ("医院/交通分组", C5, 9.3),
    ]
    gw_y = 4.2
    for name, c, x in gws:
        box(ax, x, gw_y, 3.0, 1.0, "#FFFFFF", c, lw=1.8)
        txt(ax, x + 1.5, gw_y + 0.5, name, size=9.6, weight="bold", color=c)
        arrow(ax, mcx + mcw / 2, mcy, x + 1.5, gw_y + 1.0, color=c, lw=1.4, ls="--")
        # 网关下挂 3 个终端
        for j in range(3):
            tx = x + 0.3 + j * 0.95
            ty = 2.0
            box(ax, tx, ty, 0.82, 0.95, "#FFF7ED", C3, lw=1.4)
            txt(ax, tx + 0.41, ty + 0.5, "终端", size=8.2, color=C3, weight="bold")
            arrow(ax, x + 1.5, gw_y, tx + 0.41, ty + 0.95, color=c, lw=1.0)

    # 底部说明框（单独框，避免压字）
    bx, by, bw, bh = 0.7, 0.95, 11.8, 0.8
    box(ax, bx, by, bw, bh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, bx + bw / 2, by + 0.42, "断网续播：本地缓存当前+待播，断网照常按排期播放，恢复后静默补拉差异；30 s 心跳+MD5 回传保证在线率与一致性可监",
        size=8.6, color=MUTED)

    footer(ax, "注：中心只管「编排与监播」，边缘网关负责落地与本地缓存，终端分组自治；任一网点断网不影响其余。多门店/多网点批量运维典型拓扑。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
