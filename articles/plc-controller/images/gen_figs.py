# -*- coding: utf-8 -*-
"""PLC 可编程逻辑控制器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system     PLC 系统架构（电源/CPU/通信/IO 模块 + 背板 + 现场设备）  （1.1）
  图2 scan-cycle      循环扫描时序（输入采样→程序执行→输出刷新 + 各段时长 + 滤波）（2.1）
  图3 io-power        I/O 点数规划与背板电源容量核算                            （2.2/2.10）
  图4 distributed     分布式 I/O 拓扑（中央 CPU + 远程 I/O 站 + 通信链路）        （1.2）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝
C2 = "#0E9F6E"   # 绿
C3 = "#E8833A"   # 橙
C4 = "#C2410C"   # 深橙
C5 = "#7C3AED"   # 紫
CGREY = "#CBD2D9"


def newfig():
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-", zorder=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       alpha=alpha, linestyle=ls, zorder=zorder)
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
# 图 1：PLC 系统架构（模块挂在背板导轨上）
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  PLC 系统架构：电源 + CPU + 通信 + I/O 模块，挂在背板/导轨上",
          "模块按需插拔；CPU 是背板主，电源沿背板供 5 V，I/O 对外接现场设备")

    # 导轨（在模块下方，整条可见）
    rail_y, rail_h = 3.18, 0.40
    box(ax, 0.7, rail_y, 11.9, rail_h, "#EEF1F5", CGREY, lw=1.2, r=0.06, zorder=1)
    txt(ax, 0.7 + 11.9 / 2, rail_y + rail_h / 2,
        "背板总线（DIN 导轨 + 5 V 供电 + 数据链路）", size=8.4, color=MUTED, weight="bold")

    # 四个模块（坐在导轨上）
    mods = [
        ("电源模块", "220V/24V → 5V\n背板供电", C2, 0.90, 2.20),
        ("CPU 模块\n(扫描内核)", "处理器 + 工作内存\n集成 I/O + 通信口", C3, 3.40, 2.55),
        ("通信模块", "PROFINET / Modbus\nEtherCAT / EIP", C5, 6.35, 2.40),
        ("I/O 模块组", "DI / DO / AI / AO\n按需插拔", C1, 9.15, 3.30),
    ]
    my, mh = 3.58, 2.42
    for name, sub, c, x, mw in mods:
        box(ax, x, my, mw, mh, "#FFFFFF", c, lw=2.0, r=0.20)
        txt(ax, x + mw / 2, my + mh - 0.52, name, size=10.4, weight="bold", color=c)
        for i, line in enumerate(sub.split("\n")):
            txt(ax, x + mw / 2, my + mh - 1.10 - i * 0.42, line, size=7.8, color=INK)
        # 连接脚（模块底 → 导轨）
        ax.add_patch(Rectangle((x + mw / 2 - 0.12, rail_y + rail_h), 0.24, my - (rail_y + rail_h),
                               facecolor=CGREY, edgecolor="none", zorder=2))

    # 上位机（顶部，接通信模块）
    up_x, up_y, up_w, up_h = 4.55, 6.55, 4.05, 0.66
    box(ax, up_x, up_y, up_w, up_h, "#F3ECFD", C5, lw=2.0, r=0.16)
    txt(ax, up_x + up_w / 2, up_y + up_h / 2, "上位机 / SCADA / HMI", size=9.6, weight="bold", color=C5)
    arrow(ax, 6.35 + 2.40 / 2, my + mh, up_x + up_w / 2, up_y, color=C5, lw=2.0)
    txt(ax, 8.05, 6.22, "北向", size=7.4, color=C5, weight="bold")

    # 现场设备（底部，单盒避免重叠）
    fx, fy, fw, fh = 9.15, 1.10, 3.30, 1.15
    box(ax, fx, fy, fw, fh, "#EAFFF4", C2, lw=1.8)
    txt(ax, fx + fw / 2, fy + fh - 0.36, "现场设备", size=9.4, weight="bold", color=C2)
    txt(ax, fx + fw / 2, fy + 0.52, "按钮 · 接触器 · 变送器 · 变频器", size=7.8, color=INK)
    txt(ax, fx + fw / 2, fy + 0.20, "信号线就近接入 I/O 模块端子", size=7.4, color=MUTED)
    arrow(ax, fx + fw / 2, fy + fh, fx + fw / 2, my, color=C1, lw=1.8, ls="-")

    footer(ax, "注：模块化按需插拔——产线加 16 个检测点只需插一块 DI 卡，不必重画控制柜。源/漏型（NPN/PNP）须整柜统一（正文 1.1/2.3）。示意图。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：循环扫描时序（全画布坐标绘制，避免双坐标系错位）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  循环扫描时序：最坏输出响应 ≈ 2×扫描周期 + 输入滤波",
          "PLC 先整批采样、再整批输出，确定性来自固定节拍（正文 2.1）")

    X0, S = 1.2, 2.7          # 时间轴起点与每单位时间的数据宽度
    bar_h = 0.42

    def seg(t0, t1, y, color, num, alpha=0.92, ls="-"):
        x = X0 + t0 * S
        w = (t1 - t0) * S
        ax.add_patch(Rectangle((x, y), w, bar_h, facecolor=color, edgecolor=color,
                               alpha=alpha, linewidth=1.2, linestyle=ls, zorder=3))
        txt(ax, x + w / 2, y + bar_h / 2, str(num), size=9.2, color="#FFFFFF", weight="bold", zorder=5)
        return x, x + w

    # ---- 第 1 个扫描周期 ----
    y1 = 4.55
    s1 = seg(0.00, 0.15, y1, C1, 1)
    s2 = seg(0.15, 0.60, y1, C3, 2)
    s3 = seg(0.60, 0.80, y1, C2, 3)
    s4 = seg(0.80, 0.95, y1, C5, 4)
    labels = [("采样", s1), ("程序执行", s2), ("输出刷新", s3), ("诊断", s4)]
    for name, (xa, xb) in labels:
        txt(ax, (xa + xb) / 2, y1 + bar_h + 0.20, name, size=7.6, color=INK)

    # ---- 第 2 个扫描周期（浅色示意）----
    y2 = 3.70
    seg(1.00, 1.15, y2, C1, 1, alpha=0.45, ls="--")
    seg(1.15, 1.60, y2, C3, 2, alpha=0.45, ls="--")
    seg(1.60, 1.80, y2, C2, 3, alpha=0.45, ls="--")
    seg(1.80, 1.95, y2, C5, 4, alpha=0.45, ls="--")
    txt(ax, X0 + 0.975 * S, y2 + bar_h + 0.18, "下一个周期（T_scan 循环往复）",
        size=7.4, color=MUTED)

    # ---- 最坏响应标注（从周期1采样末 → 周期2输出）----
    xa = X0 + 0.15 * S
    xb = X0 + 1.80 * S
    ax.annotate("", xy=(xb, 3.32), xytext=(xa, 3.32),
                arrowprops=dict(arrowstyle="<->", color=C4, lw=1.7))
    txt(ax, (xa + xb) / 2, 3.05,
        "输入事件 → 最坏输出响应 ≈ 2×T_scan + 输入滤波 t_f", size=8.0, color=C4, weight="bold")

    # 时间轴
    ax.annotate("", xy=(X0 + 2.0 * S, 2.55), xytext=(X0, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
    txt(ax, X0 + 1.0 * S, 2.30, "时间（1 个单位 ≈ 1 个扫描周期 T_scan）", size=7.6, color=MUTED)

    # ---- 右侧图例 ----
    lx, ly, lw_, lh = 7.15, 3.05, 5.55, 3.35
    box(ax, lx, ly, lw_, lh, "#F8FAFC", GRID, lw=1.2)
    txt(ax, lx + lw_ / 2, ly + lh - 0.40, "一个扫描周期 T_scan 的四段", size=10.2, weight="bold", color=INK)
    items = [(C1, "① 输入采样", "把端子状态读进 I/O 映像区（约 15%）"),
             (C3, "② 程序执行", "按顺序跑用户逻辑，读写映像而非端子（约 45%）"),
             (C2, "③ 输出刷新", "把映像一次性推到输出端子（约 20%）"),
             (C5, "④ 自诊断+通信", "看门狗、模块诊断、与上位/远程站交换（约 15%）")]
    for i, (c, name, desc) in enumerate(items):
        yy = ly + lh - 1.05 - i * 0.66
        ax.add_patch(Rectangle((lx + 0.32, yy - 0.10), 0.28, 0.28, facecolor=c,
                               edgecolor=c, zorder=3))
        txt(ax, lx + 0.78, yy + 0.04, name, size=8.8, color=c, weight="bold", ha="left")
        txt(ax, lx + 0.78, yy - 0.26, desc, size=7.4, color=INK, ha="left")

    footer(ax, "注：事件在最坏位置发生时，要等「下一次采样读入 + 再下一次输出推出」才在端子上体现。要求响应 ≤10 ms 时 T_scan 须 ≤(10-t_f)/2（正文 2.1）。示意图。")
    fig.savefig(os.path.join(OUT, "scan-cycle.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：I/O 点数规划 + 背板电源容量
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  I/O 点数规划与背板 5 V 容量核算",
          "点数乘 1.15 留余量；各模块 5 V 消耗求和不得超电源上限（正文 2.2/2.10）")

    # 左列：点数规划
    c1x, c1y, c1w, c1h = 0.7, 2.60, 5.55, 4.00
    box(ax, c1x, c1y, c1w, c1h, "#EEF4FF", C1, lw=1.8)
    txt(ax, c1x + c1w / 2, c1y + c1h - 0.42, "I/O 点数规划（余量 15%）", size=11.0, weight="bold", color=C1)
    rows1 = [("DI", "实际 86 → 规划 112（7×16）"),
             ("DO", "实际 54 → 规划 64（4×16）"),
             ("AI", "实际 12 → 规划 16（2×8）"),
             ("AO", "实际 4 → 规划 8（1×8）")]
    for k, (a, b) in enumerate(rows1):
        y = c1y + c1h - 1.02 - k * 0.80
        txt(ax, c1x + 0.35, y, a, size=9.6, color=C1, weight="bold", ha="left")
        txt(ax, c1x + 0.35, y - 0.32, b, size=8.2, color=INK, ha="left")

    # 右列：背板 5 V 预算
    c2x, c2y, c2w, c2h = 6.75, 2.60, 5.55, 4.00
    box(ax, c2x, c2y, c2w, c2h, "#FFF1E6", C3, lw=1.8)
    txt(ax, c2x + c2w / 2, c2y + c2h - 0.42, "背板 5 V 预算（CPU 上限 2.0 A）", size=11.0, weight="bold", color=C4)
    rows2 = [("8×DI（80 mA）", "0.64 A"),
             ("6×DO（120 mA）", "0.72 A"),
             ("2×AI（150 mA）", "0.30 A"),
             ("CPU 自身", "0.20 A")]
    for k, (a, b) in enumerate(rows2):
        y = c2y + c2h - 1.05 - k * 0.60
        txt(ax, c2x + 0.35, y, a, size=8.8, color=INK, ha="left")
        txt(ax, c2x + c2w - 0.35, y, b, size=8.8, color=C4, weight="bold", ha="right")
    # 求和条（低于最后一行，避免压字）
    sy = c2y + 0.28
    box(ax, c2x + 0.32, sy, c2w - 0.64, 0.60, "#FDECEA", C4, lw=1.6)
    txt(ax, c2x + c2w / 2, sy + 0.30,
        "合计 ≈1.86 A → 逼近 2.0 A 上限，须外接 PS 或减模块", size=8.2, color=C4, weight="bold")

    # 两列之间的虚线箭头（无文字，避免压框）
    arrow(ax, c1x + c1w, c1y + c1h * 0.5, c2x, c2y + c2h * 0.5, color=MUTED, lw=1.5, ls=":")

    footer(ax, "注：背板 5 V 由 CPU 电源模块沿背板供给各模块逻辑电路，有上限；现场 24 V（接触器/传感器）由独立电源承担（正文 2.10）。示意图。")
    fig.savefig(os.path.join(OUT, "io-power.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：分布式 I/O 拓扑
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  分布式 I/O 拓扑：中央 CPU + 远程 I/O 站 + 实时工业以太网",
          "把 I/O 下放到现场，短信号线换成强实时网；响应多算一程网络刷新（正文 1.2/2.8）")

    # 中央 PLC（高亮橙，左上）
    cx, cy, cw, ch = 0.7, 5.10, 3.2, 1.45
    box(ax, cx, cy, cw, ch, "#FFF1E6", C3, lw=2.4, r=0.22)
    txt(ax, cx + cw / 2, cy + ch - 0.45, "中央 PLC（CPU）", size=11.0, weight="bold", color=C4)
    txt(ax, cx + cw / 2, cy + 0.62, "背板 I/O + 实时以太网主站", size=7.8, color=INK)
    txt(ax, cx + cw / 2, cy + 0.24, "PROFINET / Modbus TCP", size=7.8, color=MUTED)

    # 通信链路（竖向主干）
    net_x = 6.6
    box(ax, net_x - 0.06, 1.30, 0.12, 5.10, C5, C5, lw=1.2, r=0.04, alpha=0.55)
    txt(ax, net_x + 0.45, 6.95, "实时以太网 RT 1~4 ms", size=7.4, color=C5, weight="bold", ha="left")
    arrow(ax, cx + cw, cy + ch / 2, net_x - 0.06, cy + ch / 2, color=C5, lw=2.0)

    # 三个远程 I/O 站
    stations = [("远程 I/O 站 A", "阀岛 · 8 工位"),
                ("远程 I/O 站 B", "电机旁 · 12 工位"),
                ("远程 I/O 站 C", "厂房另一端 · 12 工位")]
    sy_top, sh, sstep = 5.75, 1.35, 1.95
    last_y = None
    for i, (name, sub) in enumerate(stations):
        y = sy_top - i * sstep
        sx, sw = 8.4, 4.0
        box(ax, sx, y, sw, sh, "#EAFFF4", C2, lw=1.8)
        txt(ax, sx + sw / 2, y + sh - 0.42, name, size=10.4, weight="bold", color=C2)
        txt(ax, sx + sw / 2, y + 0.62, sub, size=8.0, color=INK)
        txt(ax, sx + sw / 2, y + 0.24, "DI/DO/AI 现场就近接入", size=7.6, color=MUTED)
        arrow(ax, net_x + 0.06, y + sh / 2, sx, y + sh / 2, color=C2, lw=1.6)
        last_y = y

    # 现场设备（站 C 下方）
    arrow(ax, 8.4 + 4.0 / 2, last_y, 8.4 + 4.0 / 2, 1.10, color=CGREY, lw=1.2, ls=":")
    box(ax, 8.4 + 4.0 / 2 - 0.80, 0.55, 1.60, 0.55, "#F6F8FA", C1, lw=1.3)
    txt(ax, 8.4 + 4.0 / 2, 0.82, "现场传感器/执行器", size=7.4, color=INK)

    footer(ax, "注：分布式把「长弱信号线」换成「短信号线 + 实时网」，降低接线成本与干扰，但响应要加一程网络刷新（负载见正文 2.8）。示意图。")
    fig.savefig(os.path.join(OUT, "distributed.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
