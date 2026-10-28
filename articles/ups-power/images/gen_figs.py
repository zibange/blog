# -*- coding: utf-8 -*-
"""UPS 不间断电源产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system        双变换在线式总体架构与供电路径      （1.1）
  图2 topology-compare   在线式 / 互动式 / 后备式 拓扑对比   （1.2 / 四）
  图3 capacity-battery   容量规划与后备时间算例             （2.1 / 2.2）
  图4 redundancy-flow    N+1 并机与 2N 冗余切换架构         （2.7）
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
C1 = "#1F6FEB"   # 主蓝（输入/市电侧）
C2 = "#0E9F6E"   # 绿（电池/直流侧）
C3 = "#E8833A"   # 橙（输出/负载侧）
C4 = "#C2410C"   # 深橙（旁路/告警）
C5 = "#7C3AED"   # 紫（控制/监控）
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
    txt(ax, W / 2, H - 0.52, t, size=15.2, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.02, sub, size=9.2, color=MUTED, ha="center")


def footer(ax, s):
    """说明条：单独开 axes，避免与绘图区坐标系混用"""
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=1)
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=8.2, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", rad=0.0, zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：双变换在线式 UPS 总体架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  双变换在线式 UPS 总体架构与供电路径",
          "负载的电永远由逆变器产生，与输入解耦——输入中断/畸变不传导到负载")

    # 主链路（一行）：市电 → PFC 整流器 → 逆变器 → 关键负载
    y0, bh = 4.9, 1.0
    boxes = [
        ("市电输入", "交流 220/380 V", 0.7, C1, "#EFF6FF"),
        ("PFC 整流器", "交流 → 直流", 3.6, C1, "#FFFFFF"),
        ("逆变器", "直流 → 纯净交流", 7.5, C3, "#FFF7ED"),
        ("关键负载", "服务器 / 医疗设备", 10.4, C3, "#FFFFFF"),
    ]
    for name, desc, x, c, fc in boxes:
        box(ax, x, y0, 2.2, bh, fc, c, lw=1.6)
        txt(ax, x + 1.1, y0 + 0.62, name, size=9.6, weight="bold", color=c, ha="center")
        txt(ax, x + 1.1, y0 + 0.28, desc, size=8.0, color=INK, ha="center")
    arrow(ax, 2.9, y0 + 0.5, 3.6, y0 + 0.5, color=C1, lw=1.6)
    arrow(ax, 5.8, y0 + 0.5, 7.5, y0 + 0.5, color=MUTED, lw=1.4)
    arrow(ax, 9.7, y0 + 0.5, 10.4, y0 + 0.5, color=C3, lw=1.6)

    # 直流母线（横条，位于整流器与逆变器之间下方）
    box(ax, 3.6, 3.3, 6.1, 0.5, "#ECFDF5", C2, lw=1.5)
    txt(ax, 6.65, 3.55, "直流母线 DC Bus（整流器、电池在此汇合）", size=8.4, color=C2, ha="center", weight="bold")
    arrow(ax, 4.7, y0, 4.7, 3.8, color=C1, lw=1.4)     # 整流器 -> 母线
    arrow(ax, 8.6, 3.8, 8.6, y0, color=C2, lw=1.4)     # 母线 -> 逆变器

    # 电池组 -> DC/DC -> 母线
    box(ax, 3.6, 1.5, 2.2, 1.0, "#FFFFFF", C2, lw=1.6)
    txt(ax, 4.7, 2.02, "蓄电池组", size=9.4, weight="bold", color=C2, ha="center")
    txt(ax, 4.7, 1.60, "铅酸 / 锂电", size=8.0, color=INK, ha="center")
    box(ax, 6.6, 1.5, 2.0, 1.0, "#FFFFFF", C2, lw=1.5, ls="--")
    txt(ax, 7.6, 2.02, "DC/DC", size=9.2, weight="bold", color=C2, ha="center")
    txt(ax, 7.6, 1.60, "升压 / 稳压", size=8.0, color=INK, ha="center")
    arrow(ax, 5.8, 2.0, 6.6, 2.0, color=C2, lw=1.4)
    arrow(ax, 7.6, 2.5, 7.6, 3.3, color=C2, lw=1.4, ls="--")

    # 监控模块（右下）
    box(ax, 10.4, 1.5, 2.2, 1.0, "#F5F3FF", C5, lw=1.5)
    txt(ax, 11.5, 2.02, "监控模块", size=9.2, weight="bold", color=C5, ha="center")
    txt(ax, 11.5, 1.60, "SNMP / Modbus", size=7.8, color=INK, ha="center")
    arrow(ax, 11.5, 2.5, 9.2, 4.85, color=C5, lw=0.9, ls=":", zorder=3)

    # 静态旁路开关（右上）
    box(ax, 10.4, 6.7, 2.2, 1.0, "#FEF2E8", C4, lw=1.6, ls="--")
    txt(ax, 11.5, 7.22, "静态旁路开关", size=9.2, weight="bold", color=C4, ha="center")
    txt(ax, 11.5, 6.80, "异常时 0ms 切换", size=7.8, color=INK, ha="center")
    # 旁路路径：市电顶部 -> 横线 -> 静态开关 -> 负载
    arrow(ax, 1.8, 5.9, 1.8, 7.2, color=C4, lw=1.3, ls="--")
    arrow(ax, 1.8, 7.2, 10.4, 7.2, color=C4, lw=1.3, ls="--")
    arrow(ax, 11.5, 6.7, 11.5, 5.9, color=C4, lw=1.3, ls="--")

    # 模式标注
    txt(ax, 5.6, 6.72, "① 正常：市电→整流→逆变→负载，电池浮充", size=8.2, color=MUTED, ha="center")
    txt(ax, 5.6, 6.28, "② 异常：电池→DC/DC→逆变→负载（0 切换）", size=8.2, color=C2, ha="center")

    footer(ax, "注：双变换在线式（Double-Conversion Online）的负载始终由逆变器供电，输入中断/浪涌/谐波被完全隔离；静态旁路仅在过载或逆变器故障时介入。示意参数为工程基准。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：三种拓扑对比
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  三种 UPS 拓扑对比：隔离度、切换时间与成本的取舍",
          "在线式最贵但负载零感知；后备式便宜但切换瞬间可能丢电")

    rows = [
        ("在线式\nDouble-Conversion", C1, "0 ms", "90~95%", "高", "完全隔离（负载恒在逆变器）"),
        ("互动式\nLine-Interactive", C2, "2~4 ms", "95~98%", "中", "稳压但不隔离（缺省旁路供电）"),
        ("后备式\nOff-Line", C3, "4~10 ms", "98~99%", "低", "平时直通市电，异常才切逆变"),
    ]
    cols = ["拓扑", "切换时间", "效率", "成本", "对负载的保护"]
    x0, y0 = 0.7, H - 2.0
    col_w = [3.0, 2.2, 2.0, 1.8, 3.5]
    row_h = 1.5
    xs = [x0]
    for w in col_w[:-1]:
        xs.append(xs[-1] + w)
    # 表头
    for j, c in enumerate(cols):
        box(ax, xs[j], y0, col_w[j], 0.7, "#F1F5F9", MUTED, lw=1.2)
        txt(ax, xs[j] + col_w[j] / 2, y0 + 0.35, c, size=9.4, weight="bold", color=INK, ha="center")
    # 数据行
    for i, (name, c, t, eff, cost, prot) in enumerate(rows):
        y = y0 - (i + 1) * row_h
        box(ax, xs[0], y, col_w[0], row_h, "#FFFFFF", c, lw=1.6)
        txt(ax, xs[0] + col_w[0] / 2, y + row_h / 2, name, size=9.4, weight="bold", color=c, ha="center")
        vals = [t, eff, cost, prot]
        for j in range(1, 5):
            box(ax, xs[j], y, col_w[j], row_h, "#FFFFFF" if j != 4 else "#F8FAFC", CGREY, lw=1.0)
            txt(ax, xs[j] + col_w[j] / 2, y + row_h / 2, vals[j - 1], size=9.0, color=INK, ha="center")
    footer(ax, "注：切换时间指输入异常到逆变器接管的时间；在线式因负载本就在逆变器上故为 0 ms。效率为典型值，互动式/后备式在旁路模式更省电但牺牲隔离。具体指标以厂商规格书为准。")
    fig.savefig(os.path.join(OUT, "topology-compare.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：容量规划与后备时间
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  容量规划与后备时间：从负载功率反推视在功率与电池配置",
          "S = P / PF；后备时间由电池能量与负载功率决定")

    # 左：容量反推流程（框 + 箭头）
    txt(ax, 2.5, H - 1.6, "容量反推链", size=10.2, weight="bold", ha="center")
    steps = [
        ("负载有功 P = 3000 W", C3),
        ("÷ 功率因数 PF = 0.9", C1),
        ("视在功率 S = 3333 VA", C1),
        ("选 5 kVA（留余量）", C2),
    ]
    sx, sy = 0.7, H - 2.1
    sh = 0.95
    for i, (s, c) in enumerate(steps):
        y = sy - i * (sh + 0.45) - sh
        box(ax, sx, y, 4.6, sh, "#FFFFFF", c, lw=1.6)
        txt(ax, sx + 0.2, y + sh / 2, s, size=9.0, color=c, ha="left", weight="bold")
        if i < 3:
            arrow(ax, sx + 2.3, y, sx + 2.3, y - 0.42, color=CGREY, lw=1.3)
    txt(ax, sx + 2.3, sy + 0.30, "逐步反推", size=7.8, color=MUTED, ha="center")

    # 右：后备时间曲线 t = E_bat / P_load
    px, py, pw, ph = 6.4, 1.7, 5.9, 5.0
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    # 电池能量（Wh）随节数/容量变化，后备时间 = 能量×η / 负载
    cap = np.array([4, 8, 12, 16, 20]) * 12 * 12   # 12V×N Ah 简化，N=4..20
    eff = 0.9
    P = 3000.0
    t_min = cap * eff / P * 60  # 分钟
    a.plot(cap, t_min, color=C2, lw=2.4, marker="o", markersize=5, zorder=4, label="后备时间 t（min）")
    # 目标 10 min 线
    a.axhline(10, color=C4, ls="--", lw=1.3, zorder=3)
    a.text(cap[3] + 60, 11.0, "目标 10 min", fontsize=8.2, color=C4, weight="bold", ha="left")
    a.scatter([cap[0]], [t_min[0]], s=70, color=C4, zorder=6, edgecolors="white", linewidths=1.2)
    stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
    a.annotate("4×12V×12Ah ≈ 576 Wh → 约 10.4 min", xy=(cap[0], t_min[0]),
               xytext=(cap[0] + 150, 34), fontsize=8.2, color=C4, weight="bold",
               ha="left", va="bottom", zorder=7, path_effects=stroke,
               arrowprops=dict(arrowstyle="-", color=C4, lw=1.0))
    a.set_xlabel("电池组可用能量 E（Wh，示意）", fontsize=9.0, color=INK)
    a.set_ylabel("后备时间 t（min）", fontsize=9.0, color=INK)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.legend(loc="upper left", fontsize=8.0, frameon=True, facecolor="#FFFFFF", edgecolor=GRID)
    a.set_xlim(cap[0] - 80, cap[-1] + 200)
    a.set_ylim(0, max(t_min) * 1.28)

    footer(ax, "注：公式 t = (V_bat × Ah × N × η_d) / P_load（η_d 为放电效率≈0.9）；视在功率 S = P / PF。左链为 3000 W 负载的选型反推，最终选 5 kVA 留 ~33% 余量。均为工程演示算例。")
    fig.savefig(os.path.join(OUT, "capacity-battery.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：N+1 并机与 2N 冗余
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  N+1 并机与 2N 冗余：把单点故障变成可承受的降级",
          "并机均分负载；任一台故障，剩余容量仍覆盖总负载")

    # 左：N+1 并机
    txt(ax, 3.35, H - 1.6, "N+1 并机（2×10 kVA 带 15 kVA 负载）", size=9.8, weight="bold", ha="center")
    box(ax, 0.7, 5.0, 2.6, 1.0, "#EFF6FF", C1, lw=1.6)
    txt(ax, 2.0, 5.55, "UPS-A 10 kVA", size=9.0, weight="bold", color=C1, ha="center")
    txt(ax, 2.0, 5.10, "带 7.5 kVA（75%）", size=7.8, color=INK, ha="center")
    box(ax, 0.7, 3.5, 2.6, 1.0, "#EFF6FF", C1, lw=1.6)
    txt(ax, 2.0, 4.05, "UPS-B 10 kVA", size=9.0, weight="bold", color=C1, ha="center")
    txt(ax, 2.0, 3.60, "带 7.5 kVA（75%）", size=7.8, color=INK, ha="center")
    # 并机母线
    box(ax, 3.7, 4.0, 2.6, 1.0, "#ECFDF5", C2, lw=1.5)
    txt(ax, 5.0, 4.55, "并机母线", size=9.2, weight="bold", color=C2, ha="center")
    txt(ax, 5.0, 4.10, "均流 / 同步", size=7.8, color=INK, ha="center")
    box(ax, 6.9, 4.0, 2.4, 1.0, "#FFF7ED", C3, lw=1.6)
    txt(ax, 8.1, 4.55, "负载 15 kVA", size=9.2, weight="bold", color=C3, ha="center")
    txt(ax, 8.1, 4.10, "总负载率 75%", size=7.8, color=INK, ha="center")
    arrow(ax, 3.3, 5.5, 3.7, 4.9, color=C1, lw=1.4)
    arrow(ax, 3.3, 4.0, 3.7, 4.3, color=C1, lw=1.4)
    arrow(ax, 6.3, 4.5, 6.9, 4.5, color=C2, lw=1.5)
    # 故障注释
    box(ax, 0.7, 1.45, 2.6, 1.35, "#FEF2E8", C4, lw=1.4, ls="--")
    txt(ax, 2.0, 2.48, "B 故障", size=9.0, weight="bold", color=C4, ha="center")
    txt(ax, 2.0, 2.06, "A 独带 15 kVA", size=7.8, color=INK, ha="center")
    txt(ax, 2.0, 1.66, "= 150% 但可短时", size=7.4, color=C4, ha="center")
    arrow(ax, 2.0, 2.8, 2.0, 3.5, color=C4, lw=1.0, ls=":", zorder=3)

    # 右：2N 冗余
    txt(ax, 9.95, H - 1.6, "2N 双总线（A/B 路独立）", size=9.8, weight="bold", ha="center")
    box(ax, 8.3, 5.2, 2.3, 1.0, "#EFF6FF", C1, lw=1.6)
    txt(ax, 9.45, 5.75, "UPS-A 总线", size=9.0, weight="bold", color=C1, ha="center")
    txt(ax, 9.45, 5.30, "N 容量", size=7.8, color=INK, ha="center")
    box(ax, 10.8, 5.2, 2.3, 1.0, "#F5F3FF", C5, lw=1.6)
    txt(ax, 11.95, 5.75, "UPS-B 总线", size=9.0, weight="bold", color=C5, ha="center")
    txt(ax, 11.95, 5.30, "N 容量", size=7.8, color=INK, ha="center")
    box(ax, 9.4, 3.4, 3.7, 1.0, "#FFF7ED", C3, lw=1.6)
    txt(ax, 11.25, 3.95, "双电源负载（两路各取 N）", size=8.6, weight="bold", color=C3, ha="center")
    txt(ax, 11.25, 3.50, "A 或 B 全断，负载不中断", size=7.8, color=INK, ha="center")
    arrow(ax, 9.45, 5.2, 10.3, 4.4, color=C1, lw=1.4)
    arrow(ax, 11.95, 5.2, 11.9, 4.4, color=C5, lw=1.4)

    footer(ax, "注：N+1 用一台冗余覆盖单台故障，负载率控制在 70~80% 以留切换裕度；2N 是两条完全独立的 N 容量总线，任一链路失效负载仍由另一路完整供电（A 级机房 GB 50174 要求）。示意图。")
    fig.savefig(os.path.join(OUT, "redundancy-flow.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
