# -*- coding: utf-8 -*-
"""户外 LED 显示屏产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system       户外屏物理结构与三防剖面        （1.2 / 1.3）
  图2 brightness-ambient 屏面亮度-环境光对比度 + 结温降额 （2.1 / 2.3）
  图3 wind-load         基本风压与总风力               （2.5）
  图4 pitch-density     点间距-像素密度-最佳视距        （2.2）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# 全局字体：不设会让内置 axes（刻度/标签/图例/标题）用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- 全局样式（light 主题，浅底深字）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（光/信号侧）
C2 = "#0E9F6E"   # 绿（散热/防护）
C3 = "#E8833A"   # 橙（环境/风/太阳）
C4 = "#C2410C"   # 深橙（告警/临界）
C5 = "#7C3AED"   # 紫（结构/配电）
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
             fontfamily="Microsoft YaHei", zorder=3, wrap=True)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", rad=0.0, zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：户外屏物理结构与三防剖面
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  户外 LED 显示屏物理结构与三防剖面",
          "把光、热、水、尘分别管住：面罩抗光抗 UV、灌胶封水、鳍片散热")

    # 左侧：屏体剖面大框
    bx, by, bw, bh = 0.7, 1.9, 6.2, 4.9
    box(ax, bx, by, bw, bh, "#FFFFFF", MUTED, lw=2.2)
    # 内部四层（自上而下）
    layers = [
        ("面罩层", "哑光黑 · 抗 UV 老化 · 吸杂光", by + bh - 0.7, 0.7, "#EEF2F6", C5),
        ("灯板层", "LED 灯珠 + PU/硅胶灌封", by + bh - 1.75, 1.05, "#EFF6FF", C1),
        ("箱体密封层", "整箱气密 · 拼缝胶条 · 出水孔", by + bh - 2.85, 1.10, "#ECFDF5", C2),
        ("背壳散热层", "铝合金鳍片 · 自然对流 / 风冷", by + bh - 4.9, 2.05, "#FFF7ED", C3),
    ]
    for name, desc, y, h, fc, c in layers:
        box(ax, bx + 0.25, y, bw - 0.5, h, fc, c, lw=1.5)
        txt(ax, bx + bw / 2, y + h * 0.62, name, size=10.2, weight="bold", color=c)
        txt(ax, bx + bw / 2, y + h * 0.30, desc, size=8.0, color=INK)
    # 散热鳍片（在背壳层内画几条竖线）
    fy0, fy1 = by + bh - 4.55, by + bh - 2.95
    for fx in np.linspace(bx + 0.5, bx + bw - 0.5, 11):
        ax.plot([fx, fx], [fy0, fy1], color=C3, lw=1.1, alpha=0.55, zorder=3)

    # 右侧：三防要点（顺序与左侧层级对应，避免箭头交叉）
    rx, rw = 8.2, 4.4
    notes = [
        ("抗 UV 不发黄", "面罩抗老化，避免一两年色偏整屏发黄", C5, 5.75),
        ("防水 IP65", "灌胶 + 防水胶条 + PG 防水接头，雨水不渗入", C2, 4.25),
        ("散热扛太阳", "背壳鳍片 / 电源舱风冷，扛太阳辐照得热", C3, 2.75),
    ]
    for name, desc, c, ny in notes:
        box(ax, rx, ny, rw, 1.05, "#FFFFFF", c, lw=1.7)
        txt(ax, rx + 0.25, ny + 0.70, name, size=10.4, weight="bold", color=c, ha="left")
        txt(ax, rx + 0.25, ny + 0.32, desc, size=8.2, color=INK, ha="left")
    # 连接箭头：面罩->抗UV、灯板/箱体->防水、背壳->散热（一一对应不交叉）
    arrow(ax, bx + bw, by + bh - 0.4, rx, 6.25, color=C5, lw=1.3)
    arrow(ax, bx + bw, by + bh - 2.3, rx, 4.75, color=C2, lw=1.3)
    arrow(ax, bx + bw, by + bh - 3.9, rx, 3.25, color=C3, lw=1.3)

    # 顶部：阳光直射 与 雨水被挡
    arrow(ax, 2.0, 7.0, 2.0, by + bh, color=C3, lw=1.6)
    txt(ax, 2.0, 7.35, "阳光直射", size=8.4, color=C4, weight="bold")
    # 雨水（落在面罩外被挡）
    box(ax, 4.6, 6.95, 1.5, 0.55, "#EAF2FB", C1, lw=1.2, ls="--")
    txt(ax, 5.35, 7.22, "雨水·被挡", size=8.2, color=C1, weight="bold")
    arrow(ax, 5.35, 6.95, 5.35, by + bh, color=C1, lw=1.2, ls="--")

    footer(ax, "注：剖面自上而下承担抗光/封水/密封/散热职责；户外屏失效多源于胶开裂进水、风扇停转闷烧或面罩发黄，而非灯珠本身。工程基准示意。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：屏面亮度-环境光对比度 + 结温降额
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  屏面亮度 vs 可视对比度，以及结温亮度降额",
          "左：环境反射 318 cd/m² 基准下 CAR 随屏面亮度变化；右：结温每升 1℃ 亮度降额")

    # ---- 左图：CAR vs L_scr ----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    L = np.linspace(500, 9000, 200)
    Lamb = 318.0
    CAR = L / (L + Lamb)
    a.plot(L, CAR * 100, color=C1, lw=2.4, zorder=4, label="可视对比度 CAR (%)")
    for Lm, c in [(7000, C2), (3000, C3), (1500, C4)]:
        car = Lm / (Lm + Lamb) * 100
        a.scatter([Lm], [car], s=70, color=c, zorder=6, edgecolors="white", linewidths=1.2)
        stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
        a.annotate(f"{Lm}\n{car:.1f}%", xy=(Lm, car), xytext=(Lm + 250, car - 9),
                   fontsize=8.2, color=c, weight="bold", ha="left", va="top", zorder=7,
                   path_effects=stroke)
    a.axhline(90, color=MUTED, ls="--", lw=1.1, zorder=3)
    a.text(8200, 91.2, "CAR=90% 线", fontsize=7.8, color=MUTED, ha="right")
    a.set_xlabel("屏面亮度 L_scr (cd/m²)", fontsize=9.0, color=INK)
    a.set_ylabel("可视对比度 CAR (%)", fontsize=9.0, color=INK)
    a.set_xlim(0, 9200); a.set_ylim(40, 100)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.legend(loc="lower right", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    # ---- 右图：结温降额 ----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    Tj = np.linspace(25, 80, 200)
    kR, kBG = 0.003, 0.002
    relR = (1 - (Tj - 25) * kR) * 100
    relBG = (1 - (Tj - 25) * kBG) * 100
    b.plot(Tj, relR, color=C4, lw=2.4, zorder=4, label="红管 -0.3%/℃")
    b.plot(Tj, relBG, color=C1, lw=2.4, ls="--", zorder=4, label="蓝绿管 -0.2%/℃")
    idx65 = int(np.argmin(np.abs(Tj - 65)))
    b.scatter([65], [relR[idx65]], s=70, color=C4, zorder=6,
              edgecolors="white", linewidths=1.2)
    stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
    b.annotate("65℃ 红管约 88%", xy=(65, relR[idx65]),
               xytext=(50, 80), fontsize=8.2, color=C4, weight="bold", ha="left", zorder=7,
               path_effects=stroke,
               arrowprops=dict(arrowstyle="-", color=C4, lw=1.0))
    b.axhline(100, color=MUTED, ls="--", lw=1.0, zorder=3)
    b.text(80, 101, "25℃ 标定 100%", fontsize=7.6, color=MUTED, ha="right")
    b.set_xlabel("灯珠结温 Tj (℃)", fontsize=9.0, color=INK)
    b.set_ylabel("相对亮度 (%)", fontsize=9.0, color=INK)
    b.set_xlim(20, 85); b.set_ylim(70, 102)
    b.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.legend(loc="lower left", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    footer(ax, "注：左图按环境照度 50000 lux、反射率 2% 估算（反射亮度约 318 cd/m²）；右图红管 -0.3%/℃、蓝绿管 -0.2%/℃。工程演示算例。")
    fig.savefig(os.path.join(OUT, "brightness-ambient.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：基本风压与总风力
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  基本风压随风速平方增长，及 60 m² 屏体所受总风力",
          "w0=0.5·ρ·v²；计入阵风与体型系数后迎风面积越大受力越惊人")

    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    v = np.linspace(0, 45, 200)
    rho = 1.25
    w0 = 0.5 * rho * v**2
    a.plot(v, w0, color=C3, lw=2.4, zorder=4, label="基本风压 w0 (Pa)")
    for vv, lab in [(30, "11级 30 m/s"), (37, "12级 37 m/s")]:
        w = 0.5 * rho * vv**2
        a.scatter([vv], [w], s=70, color=C4, zorder=6, edgecolors="white", linewidths=1.2)
        stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
        a.annotate(f"{lab}\n{w:.0f} Pa", xy=(vv, w), xytext=(vv + 1.5, w + 120),
                   fontsize=8.2, color=C4, weight="bold", ha="left", zorder=7, path_effects=stroke)
    a.set_xlabel("风速 v (m/s)", fontsize=9.0, color=INK)
    a.set_ylabel("基本风压 w0 (Pa)", fontsize=9.0, color=INK)
    a.set_xlim(0, 46); a.set_ylim(0, 1100)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.legend(loc="upper left", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    # 右图：总风力（含阵风1.5×体型1.3） vs 风速
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    area = 60.0
    F = w0 * 1.5 * 1.3 * area
    b.plot(v, F / 1000, color=C5, lw=2.4, zorder=4, label="总风力 F (kN)")
    for vv, lab in [(30, "11级"), (37, "12级")]:
        ff = 0.5 * rho * vv**2 * 1.5 * 1.3 * area / 1000
        b.scatter([vv], [ff], s=70, color=C4, zorder=6, edgecolors="white", linewidths=1.2)
        stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
        b.annotate(f"{lab}\n{ff:.0f} kN", xy=(vv, ff), xytext=(vv + 1.5, ff + 12),
                   fontsize=8.2, color=C4, weight="bold", ha="left", zorder=7, path_effects=stroke)
    b.set_xlabel("风速 v (m/s)", fontsize=9.0, color=INK)
    b.set_ylabel("总风力 F (kN)", fontsize=9.0, color=INK)
    b.set_xlim(0, 46); b.set_ylim(0, 135)
    b.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.legend(loc="upper left", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    footer(ax, "注：总风力 = 基本风压 × 阵风(1.5) × 体型(1.3) × 面积；60 m² 屏在 11 级风下约受 65 kN。沿海台风区需抗风计算书。")
    fig.savefig(os.path.join(OUT, "wind-load.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：点间距 - 像素密度 - 最佳视距
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  点间距越小：像素密度越高、最佳视距越近",
          "D=(1000/p)²；户外最佳视距经验系数取 2.5~3.0")

    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    p = np.linspace(3, 16, 200)
    D = (1000.0 / p) ** 2
    a.plot(p, D / 1000, color=C1, lw=2.4, zorder=4, label="像素密度 D (千点/m²)")
    for pp, lab in [(4, "P4"), (6, "P6"), (10, "P10"), (16, "P16")]:
        dd = (1000.0 / pp) ** 2 / 1000
        a.scatter([pp], [dd], s=70, color=C2, zorder=6, edgecolors="white", linewidths=1.2)
        stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
        a.annotate(lab, xy=(pp, dd), xytext=(pp + 0.3, dd * 1.05),
                   fontsize=8.2, color=C2, weight="bold", ha="left", zorder=7, path_effects=stroke)
    a.set_xlabel("点间距 p (mm)", fontsize=9.0, color=INK)
    a.set_ylabel("像素密度 D (千点/m²)", fontsize=9.0, color=INK)
    a.set_xlim(2.5, 16.5); a.set_ylim(0, 120)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.legend(loc="upper right", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    # 右图：最佳视距 vs 点间距
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    V = p * 2.75
    b.plot(p, V, color=C3, lw=2.4, zorder=4, label="最佳视距 V≈p×2.75 (m)")
    for pp, lab in [(4, "P4"), (6, "P6"), (10, "P10"), (16, "P16")]:
        vv = pp * 2.75
        b.scatter([pp], [vv], s=70, color=C4, zorder=6, edgecolors="white", linewidths=1.2)
        stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
        b.annotate(f"{lab}\n{vv:.0f} m", xy=(pp, vv), xytext=(pp + 0.3, vv + 3),
                   fontsize=8.2, color=C4, weight="bold", ha="left", zorder=7, path_effects=stroke)
    b.set_xlabel("点间距 p (mm)", fontsize=9.0, color=INK)
    b.set_ylabel("最佳视距 V (m)", fontsize=9.0, color=INK)
    b.set_xlim(2.5, 16.5); b.set_ylim(0, 50)
    b.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.legend(loc="upper left", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)

    footer(ax, "注：D=(1000/p)²，P10=10000 点/m²；户外最佳视距取 p×(2.5~3.0)，距离 40 m 选 P10~P12。工程演示算例。")
    fig.savefig(os.path.join(OUT, "pitch-density.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
