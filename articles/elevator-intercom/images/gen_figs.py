# -*- coding: utf-8 -*-
"""电梯五方对讲系统产品综述 —— 四张矢量示意图（v2，修正布局）

图序严格按正文出现顺序：
  图1 arch-five-party   五方对讲系统架构（轿厢/轿顶/底坑/机房/监控中心 + 随行电缆总线）  （1.1）
  图2 topology-compare  总线型 vs IP 型 组网拓扑对比                                  （1.2）
  图3 voltage-drop      随行电缆 24V 供电压降核算（线径 vs 末端电压，18V 阈值线）        （2.3）
  图4 install-protect   井道安装工艺与防雷隔离（对讲线/动力线分离、120Ω、防护标注）      （1.3/四）
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
C1 = "#1F6FEB"
C2 = "#0E9F6E"
C3 = "#E8833A"
C4 = "#C2410C"
C5 = "#7C3AED"
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
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=10)
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
# 图 1：五方对讲系统架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  五方对讲系统架构：四路现场分机经随行电缆汇聚到监控中心",
          "轿厢/轿顶/底坑/机房(紧急操作处)/监控中心五方；全部由应急电源供电（正文 1.1）")

    # 井道轮廓（左），顶部 5.8，避开标题区
    sx, sy, sw, sh = 0.9, 1.30, 2.6, 4.50
    box(ax, sx, sy, sw, sh, "#F4F7FB", C1, lw=1.6, r=0.10)

    # 机房 / 紧急操作处（坐在井道顶部）
    m_x, m_w, m_h = sx - 0.10, sw + 0.20, 0.80
    m_y = sy + sh
    box(ax, m_x, m_y, m_w, m_h, "#FFF1E6", C3, lw=2.0, r=0.16)
    txt(ax, m_x + m_w / 2, m_y + m_h - 0.26, "机房 / 紧急操作处", size=9.4, weight="bold", color=C4)
    txt(ax, m_x + m_w / 2, m_y + 0.28, "分机 + 总线控制器（应急电源）", size=7.4, color=INK)

    # 井道内三个分机（轿顶/轿厢/底坑），竖排不重叠
    stations = [("轿顶分机", 4.95), ("轿厢分机（报警按钮）", 3.55), ("底坑分机", 2.00)]
    for name, yy in stations:
        box(ax, sx + 0.25, yy - 0.31, sw - 0.50, 0.62, "#EAFFF4", C2, lw=1.6)
        txt(ax, sx + sw / 2, yy, name, size=8.4, weight="bold", color=C2)

    # 随行电缆（竖直线）
    cable_x = sx + 1.30
    ax.add_patch(Rectangle((cable_x - 0.05, sy + 0.10), 0.10, sh - 0.20, facecolor=C1,
                           edgecolor=C1, alpha=0.5, zorder=2))
    txt(ax, sx + sw / 2, sy + sh - 0.30, "电梯井道", size=7.6, color=C1)

    # 监控中心主机（右下）
    c_x, c_y, c_w, c_h = 9.3, 2.20, 3.1, 1.50
    box(ax, c_x, c_y, c_w, c_h, "#F3ECFD", C5, lw=2.2, r=0.18)
    txt(ax, c_x + c_w / 2, c_y + c_h - 0.40, "监控中心主机（值班室）", size=10.2, weight="bold", color=C5)
    txt(ax, c_x + c_w / 2, c_y + 0.80, "接听 · 调度 · 录音 · 联动视频", size=7.8, color=INK)
    txt(ax, c_x + c_w / 2, c_y + 0.38, "应急电源供电", size=7.6, color=C4)

    # 机房 → 监控中心 的布线（水平 + 下行进入主机顶部）
    cx = c_x + c_w / 2
    arrow(ax, m_x + m_w, m_y + 0.30, cx, m_y + 0.30, color=C5, lw=2.0)
    arrow(ax, cx, m_y + 0.30, cx, c_y + c_h, color=C5, lw=2.0)
    txt(ax, 6.9, m_y + 0.55, "楼内布线 / 总线汇聚", size=8.0, color=C5, weight="bold")

    # 五方小注
    txt(ax, sx + sw / 2, 0.78, "五方：轿厢 · 轿顶 · 底坑 · 机房(紧急操作处) · 监控中心",
        size=8.0, color=MUTED)

    footer(ax, "注：四路现场分机都汇聚到监控中心主机，中心是调度与录音核心；同时行程>30m 时轿厢与紧急操作处另设直连对讲（正文 1.4/2.14）。示意图。")
    fig.savefig(os.path.join(OUT, "arch-five-party.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：总线型 vs IP 型 组网拓扑对比
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  组网拓扑对比：总线型（皮实省线）vs IP 型（联动智能）",
          "井道电磁环境恶劣，选型看「可靠保底」与「智能联动」两条诉求（正文 1.2）")

    p1x, p2x, p1y, pw, ph = 0.7, 6.9, 1.7, 5.5, 4.9
    top = p1y + ph  # 6.6
    box(ax, p1x, p1y, pw, ph, "#EEF4FF", C1, lw=1.8)
    box(ax, p2x, p1y, pw, ph, "#F6F2FF", C5, lw=1.8)
    txt(ax, p1x + pw / 2, top - 0.42, "总线型（RS-485 / CAN）", size=11.6, weight="bold", color=C1)
    txt(ax, p2x + pw / 2, top - 0.42, "IP 网络型", size=11.6, weight="bold", color=C5)

    # ---------- 左：总线型 ----------
    cxp = p1x + pw / 2
    box(ax, p1x + 0.35, 5.00, pw - 0.70, 0.75, "#FFFFFF", C1, lw=1.6)
    txt(ax, cxp, 5.375, "总线控制器 / 监控主机", size=8.6, weight="bold", color=C1)
    bus_y = 4.25
    ax.add_patch(Rectangle((p1x + 0.35, bus_y - 0.05), pw - 0.70, 0.10, facecolor=C1, edgecolor=C1, zorder=2))
    arrow(ax, cxp, 5.00, cxp, bus_y + 0.05, color=C1, lw=1.4)
    txt(ax, cxp, bus_y + 0.28, "二/四总线（两端 120Ω 终端）", size=7.6, color=C1)
    # 三台电梯一排，短竖箭头直上总线（不交叉）
    eh = 0.55
    exs = [p1x + 0.45, p1x + 2.05, p1x + 3.65]
    ew = 1.45
    for i, bx0 in enumerate(exs):
        box(ax, bx0, 2.80, ew, eh, "#EAFFF4", C2, lw=1.3)
        txt(ax, bx0 + ew / 2, 2.80 + eh / 2, "梯%d" % (i + 1), size=8.2, color=C2, weight="bold")
        arrow(ax, bx0 + ew / 2, 2.80 + eh, bx0 + ew / 2, bus_y - 0.05, color=C2, lw=1.3)
    txt(ax, cxp, 2.40, "优点：抗干扰·省线·断网不失联", size=7.4, color=MUTED)
    txt(ax, cxp, 2.10, "缺点：联动 / 存储弱", size=7.4, color=MUTED)

    # ---------- 右：IP 型 ----------
    cxp2 = p2x + pw / 2
    box(ax, p2x + 0.35, 5.00, pw - 0.70, 0.75, "#FFFFFF", C5, lw=1.6)
    txt(ax, cxp2, 5.375, "中心软件 / NVR 联动", size=8.6, weight="bold", color=C5)
    box(ax, p2x + 0.35, 3.85, pw - 0.70, 0.55, "#FFFFFF", C5, lw=1.4)
    txt(ax, cxp2, 4.125, "网络交换机（屏蔽网线 + 防雷）", size=8.0, color=C5, weight="bold")
    arrow(ax, cxp2, 5.00, cxp2, 4.40, color=C5, lw=1.4)
    for i, bx0 in enumerate([p2x + 0.45, p2x + 2.05, p2x + 3.65]):
        box(ax, bx0, 2.80, ew, eh, "#EAFFF4", C2, lw=1.3)
        txt(ax, bx0 + ew / 2, 2.80 + eh / 2, "梯%d" % (i + 1), size=8.2, color=C2, weight="bold")
        arrow(ax, bx0 + ew / 2, 2.80 + eh, bx0 + ew / 2, 3.85, color=C2, lw=1.3)
    txt(ax, cxp2, 2.40, "优点：联动·存储·跨网", size=7.4, color=MUTED)
    txt(ax, cxp2, 2.10, "缺点：依赖楼内网·防雷是坑", size=7.4, color=MUTED)

    footer(ax, "注：总线型做「可靠保底」，IP 型做「智能联动」，无线做「无布线兜底」；高层项目常三者叠加（正文 1.2/4.2）。示意图。")
    fig.savefig(os.path.join(OUT, "topology-compare.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：随行电缆 24V 供电压降核算（公式放坐标轴内，避免被盖）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  随行电缆 24V 供电压降核算：线径 vs 末端电压（120 m，0.5 A）",
          "回路电阻算双程 2l；末端电压须落在 18~28 V 工作窗内（正文 2.3）")

    axp = fig.add_axes([0.12, 0.17, 0.76, 0.58])
    S = [0.30, 0.50, 0.75, 1.00]
    Uend = [17.0, 19.8, 21.2, 21.9]
    axp.plot(S, Uend, "-o", color=C1, lw=2.2, markersize=8, zorder=3)
    for x, y in zip(S, Uend):
        dy = 9 if y > 18.5 else -16
        axp.annotate("%.1f V" % y, (x, y), textcoords="offset points",
                     xytext=(-4, dy), ha="right", fontsize=8.4, color=C1,
                     fontfamily="Microsoft YaHei")
    axp.axhline(18.0, color=C4, ls="--", lw=1.8, zorder=2)
    # 公式框放左上空白区（inside axes，避免被轴盖住）
    axp.text(0.24, 22.55,
             "U_end = U0 - I·R_loop\nR_loop = ρ·2l/S\n(ρ≈0.0175 Ω·mm²/m, l=120 m, I=0.5 A)",
             fontsize=8.3, color=INK, va="top", ha="left", fontfamily="Microsoft YaHei",
             bbox=dict(boxstyle="round,pad=0.35", fc="#F8FAFC", ec=GRID, lw=1.0), zorder=5)
    axp.text(0.46, 17.42, "0.3 mm² 已临界（<18V）", fontsize=8.2, color=C4,
             fontfamily="Microsoft YaHei", weight="bold")
    axp.set_xlabel("铜线截面积 S (mm²)", fontsize=9.0, color=INK, fontfamily="Microsoft YaHei")
    axp.set_ylabel("末端电压 U_end (V)", fontsize=9.0, color=INK, fontfamily="Microsoft YaHei")
    axp.set_ylim(15.5, 23.2)
    axp.set_xlim(0.20, 1.12)
    axp.grid(True, ls=":", color=GRID)
    axp.tick_params(labelsize=8.0)
    for lab in axp.get_xticklabels() + axp.get_yticklabels():
        lab.set_fontname("Microsoft YaHei")

    footer(ax, "注：高层电梯随行电缆对讲线别用太细；若电量由多台分机均摊，总电流更大，线径要再放余量（正文 2.3）。示意图。")
    fig.savefig(os.path.join(OUT, "voltage-drop.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：井道安装工艺与防雷隔离
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  井道安装工艺与防雷隔离：对讲线 / 动力线分离，屏蔽单端接地",
          "三条铁律：屏蔽层单端接地、总线两端 120Ω、入口两级防雷（正文 1.3/1.5/2.10）")

    # 井道轮廓（左）
    sx, sy, sw, sh = 0.9, 1.6, 2.9, 4.4
    box(ax, sx, sy, sw, sh, "#F4F7FB", C1, lw=1.6, r=0.10)
    txt(ax, sx + sw / 2, sy + sh - 0.35, "电梯井道（竖井）", size=8.6, color=C1, weight="bold")

    pow_x = 1.55
    bus_x = 3.15
    ax.add_patch(Rectangle((pow_x - 0.08, sy + 0.15), 0.16, sh - 0.55, facecolor=C3, edgecolor=C3, zorder=2))
    ax.add_patch(Rectangle((bus_x - 0.08, sy + 0.15), 0.16, sh - 0.55, facecolor=C1, edgecolor=C1, zorder=2))
    txt(ax, pow_x, 5.35, "动力线", size=7.6, color=C3, weight="bold")
    txt(ax, bus_x, 5.35, "对讲总线", size=7.6, color=C1, weight="bold")
    # 间距标注
    arrow(ax, pow_x + 0.10, 2.60, bus_x - 0.10, 2.60, color=MUTED, lw=1.3, ls=":", ms="<|-|>")
    txt(ax, (pow_x + bus_x) / 2, 2.85, "间距≥200~300mm", size=7.2, color=MUTED, weight="bold")
    # 120Ω 终端（底部一端示意）
    box(ax, bus_x - 0.40, sy + 0.02, 0.80, 0.30, "#FDECEA", C4, lw=1.4)
    txt(ax, bus_x, sy + 0.17, "120Ω", size=7.6, color=C4, weight="bold")
    txt(ax, bus_x + 0.95, sy + 0.17, "总线两端终端（消除反射/啸叫）", size=7.2, color=C4, ha="left")

    # 顶部单行防护条（跨整个井道，不与标题冲突）
    box(ax, sx, sy + sh + 0.12, sw, 0.68, "#FFF1E6", C3, lw=1.6)
    txt(ax, sx + sw / 2, sy + sh + 0.56, "入口防护：TVS + GDT 两级防雷", size=7.8, color=C4, weight="bold")
    txt(ax, sx + sw / 2, sy + sh + 0.28, "屏蔽层单端接地（仅一端）", size=7.8, color=C4, weight="bold")

    # 右侧五条铁律
    rx, ry, rw, rh = 4.5, 1.7, 8.1, 4.9
    box(ax, rx, ry, rw, rh, "#F8FAFC", GRID, lw=1.4)
    txt(ax, rx + rw / 2, ry + rh - 0.42, "五条现场铁律（故障多源于此）", size=10.6, weight="bold", color=INK)
    laws = [
        ("屏蔽层单端接地", "两端接地会形成地电位环流，反而引入噪声；只在中心一端接地", C1),
        ("总线两端 120Ω 终端", "特征阻抗匹配吸收信号，省掉/漏接一端必啸叫、误码、掉线", C4),
        ("入口两级防雷", "GDT 泄放大电流 + TVS 钳位残压，挡井道感应雷/地反击", C3),
        ("与动力线分开捆扎", "间距≥200~300mm 或穿金属管，斩断容性/感性耦合", C2),
        ("地址表竣工留档", "哪台梯哪个终端对应哪地址，错一位救援跑错楼", C5),
    ]
    for i, (head, desc, c) in enumerate(laws):
        yy = ry + rh - 1.02 - i * 0.78
        ax.add_patch(Rectangle((rx + 0.30, yy - 0.11), 0.26, 0.26, facecolor=c, edgecolor=c, zorder=3))
        txt(ax, rx + 0.43, yy + 0.02, str(i + 1), size=8.4, color="#FFFFFF", weight="bold")
        txt(ax, rx + 0.72, yy + 0.10, head, size=8.8, color=c, weight="bold", ha="left")
        txt(ax, rx + 0.72, yy - 0.22, desc, size=7.3, color=INK, ha="left")

    footer(ax, "注：井道是电梯变频器、曳引机、抱闸的电磁重灾区，也是高层引雷路径；工艺做对，平时正常、出事不掉链（正文 2.8/2.10/2.11）。示意图。")
    fig.savefig(os.path.join(OUT, "install-protect.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
