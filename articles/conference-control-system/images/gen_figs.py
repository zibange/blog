# -*- coding: utf-8 -*-
"""会议中控系统产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system       中控系统架构（主机为中心 / 接口分类型）      （1.1）
  图2 scene-timing      一键「开会」场景时序：串行 vs 混合编排       （2.2）
  图3 interface-capacity 控制接口容量 vs 项目需求（串口缺口）         （2.1 / 2.11）
  图4 flow-control      场景联动状态机：状态 + 联锁 + 异常处理        （3.4 / 2.9）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

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
# 图 1：中控系统架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  会议中控系统架构：主机为中心，接口分类型连受控设备",
          "触摸屏经控制网络连主机；受控设备按被控方式分四族")

    # 主机（中心高亮）
    hx, hy, hw, hh = 5.0, 3.15, 3.2, 1.95
    box(ax, hx, hy, hw, hh, "#EAF2FF", C1, lw=2.2, r=0.22)
    txt(ax, hx + hw / 2, hy + hh - 0.45, "中央控制主机", size=11.0, weight="bold", color=C1)
    txt(ax, hx + hw / 2, hy + 0.78, "协议翻译 + 时序编排", size=8.4, color=INK)
    txt(ax, hx + hw / 2, hy + 0.42, "宏引擎 + 设备对象", size=8.4, color=INK)
    txt(ax, hx + hw / 2, hy + 0.06, "COM / IR / 继电器 / I-O / IP", size=7.8, color=MUTED)

    # 触摸屏（左）
    tx, ty, tw, th = 0.6, 3.45, 2.2, 1.35
    box(ax, tx, ty, tw, th, "#FFFFFF", C5, lw=1.7)
    txt(ax, tx + tw / 2, ty + th - 0.32, "触摸屏 / 墙面面板", size=9.2, weight="bold", color=C5)
    txt(ax, tx + tw / 2, ty + 0.40, "一键场景 · 状态可视", size=8.0, color=INK)
    arrow(ax, tx + tw, ty + th / 2, hx, hy + hh / 2, color=C5, lw=1.8)
    txt(ax, (tx + tw + hx) / 2, ty + th / 2 + 0.32, "控制网络 TCP/IP", size=7.8, color=C5, weight="bold")

    # 四族（上左 / 上右 / 下左 / 下右）
    fams = [
        (0.7, 5.72, 5.6, 1.42, "串口族 · RS-232 / RS-485", "投影机 · 音视频矩阵 · PTZ 摄像机 · 电源时序器 · 调光", C1),
        (6.9, 5.72, 5.6, 1.42, "红外族 · IR（单向学习）", "电视 · 蓝光 / DVD · 功放 · 机顶盒", C3),
        (0.7, 1.15, 5.6, 1.55, "强电族 · 继电器 / 干接点", "电动幕布 · 窗帘电机 · 电动吊架 · 电源控制器", C4),
        (6.9, 1.15, 5.6, 1.55, "网络族 · TCP/IP", "IP 摄像机 · 网络化调光 · 第三方系统 / BA 对接", C2),
    ]
    # 主机中心
    hcx, hcy = hx + hw / 2, hy + hh / 2
    conn = [
        (3.5, 5.72, 5.4, hcy + 0.55, "RS-232/485", C1),   # 上左
        (9.7, 5.72, 7.8, hcy + 0.55, "IR 红外", C3),        # 上右
        (3.5, 2.70, 5.4, hy, "继电器/干接点", C4),          # 下左
        (9.7, 2.70, 7.8, hy, "TCP/IP", C2),                 # 下右
    ]
    for (x, y, w, h, name, desc, c) in fams:
        box(ax, x, y, w, h, "#FFFFFF", c, lw=1.7)
        txt(ax, x + 0.22, y + h - 0.34, name, size=9.6, weight="bold", color=c, ha="left")
        txt(ax, x + 0.22, y + 0.42, desc, size=8.2, color=INK, ha="left")
    for (cx, cby, fx, fy, lab, c) in conn:
        arrow(ax, fx, fy, cx, cby, color=c, lw=1.6)
        txt(ax, (fx + cx) / 2 + 0.1, (fy + cby) / 2 + 0.18, lab, size=7.6, color=c, weight="bold")

    footer(ax, "注：主机抽象不同接口为统一设备对象，对外把用户操作翻译成设备指令；触摸屏与主机走独立控制网络，避免与办公网广播风暴互相拖累。示意图，接口数按工程基准。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：场景时序 串行 vs 混合编排
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 3  一键「开会」场景时序：串行 ACK 1.8 s vs 混合编排 350 ms（理论）",
          "关键路径串行 + 非关键并行；案例实测 2.1 s，均 < 3 s 目标")

    # 左：混合编排 Gantt（6 步，依赖关系）
    px, py, pw, ph = 1.25, 1.7, 6.1, 5.4
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    steps = ["①关主灯", "②放幕布", "③降吊架", "④开投影(预热)", "⑤切矩阵", "⑥解静音"]
    ypos = list(range(6))[::-1]
    # 并行分组：②∥③ 并行；⑤∥⑥ 并行；④ 后台；① 先；gate 在 ④ 前
    segs = [
        (0, 0.0, 0.3, C1),   # ①
        (1, 0.3, 0.9, C2),   # ② 并行
        (2, 0.3, 0.9, C2),   # ③ 并行
        (3, 0.9, 2.1, C5),   # ④ 后台(预热)
        (4, 2.1, 2.4, C3),   # ⑤
        (5, 2.1, 2.35, C3),  # ⑥ 并行
    ]
    for (i, x0, x1, c) in segs:
        a.barh(ypos[i], x1 - x0, left=x0, height=0.5, color=c, alpha=0.85,
               edgecolor=c, linewidth=1.1, zorder=3)
    a.set_yticks(ypos); a.set_yticklabels(steps, fontsize=8.6, color=INK)
    a.set_xlim(0, 2.5); a.set_ylim(-0.6, 6.4)
    a.set_xlabel("时间（秒，理论）", fontsize=9.0, color=INK)
    a.set_title("混合编排（关键路径串行 + 非关键并行）", fontsize=9.4, color=C1, weight="bold", pad=8)
    a.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    # 标注并行区
    a.annotate("", xy=(0.9, 5.4), xytext=(0.3, 5.4),
               arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.0))
    a.text(0.6, 5.55, "并行", fontsize=7.6, color=MUTED, ha="center")

    # 右：两条总时间对比
    rx, ry, rw, rh = 7.7, 5.4, 4.7, 0.95
    box(ax, rx, ry, rw, rh, "#FDECEA", C4, lw=1.6)
    txt(ax, rx + 0.22, ry + rh - 0.30, "纯串行等待 ACK", size=9.2, weight="bold", color=C4, ha="left")
    txt(ax, rx + 0.22, ry + 0.34, "6×300 ms = 1800 ms", size=9.0, color=INK, ha="left")
    ry2 = ry - 1.25
    box(ax, rx, ry2, rw, rh, "#EAF7F0", C2, lw=1.6)
    txt(ax, rx + 0.22, ry2 + rh - 0.30, "混合编排（理论）", size=9.2, weight="bold", color=C2, ha="left")
    txt(ax, rx + 0.22, ry2 + 0.34, "80 + 220 + 50 ≈ 350 ms", size=9.0, color=INK, ha="left")
    ry3 = ry2 - 1.25
    box(ax, rx, ry3, rw, rh, "#EAF2FF", C1, lw=1.6)
    txt(ax, rx + 0.22, ry3 + rh - 0.30, "案例实测（12 间均值）", size=9.2, weight="bold", color=C1, ha="left")
    txt(ax, rx + 0.22, ry3 + 0.34, "开会 2.1 s / 离开 1.4 s", size=9.0, color=INK, ha="left")

    ry4 = ry3 - 1.35
    box(ax, rx, ry4, rw, 1.1, "#FFF7ED", C3, lw=1.5)
    txt(ax, rx + 0.18, ry4 + 0.82, "工程含义", size=9.0, weight="bold", color=C3, ha="left")
    txt(ax, rx + 0.18, ry4 + 0.46, "场景不是指令清单，而是带依赖的", size=8.0, color=INK, ha="left")
    txt(ax, rx + 0.18, ry4 + 0.12, "DAG：先画依赖，再写宏。", size=8.0, color=INK, ha="left")

    footer(ax, "注：左图为「开会」六步的混合编排时序示意（②与③并行、⑤与⑥并行、④投影预热后台进行）；右图三段时间为演示/案例值，目标 ≤3 s。参数为工程演示算例。")
    fig.savefig(os.path.join(OUT, "scene-timing.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：控制接口容量 vs 项目需求
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 2  控制接口容量 vs 项目需求：4 口主机的串口缺口要补",
          "串口族决定选型第一道闸；强电/IO 通常富余")

    px, py, pw, ph = 0.95, 1.7, 11.3, 5.3
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    import numpy as np
    labels = ["COM 口", "继电器路", "I/O 路", "红外口"]
    need = [6, 4, 4, 3]
    cap = [4, 16, 16, 4]
    x = np.arange(len(labels))
    wbar = 0.36
    a.bar(x - wbar / 2, need, width=wbar, color=C4, alpha=0.9, edgecolor=C4, label="本项目需求", zorder=3)
    a.bar(x + wbar / 2, cap, width=wbar, color=C1, alpha=0.55, edgecolor=C1, linewidth=1.3, label="标准主机容量", zorder=3)
    # 缺口标注
    a.annotate("缺口 2 路\n→ 走 485 链", xy=(0 - wbar / 2, 6.7), xytext=(-0.48, 11.8),
               fontsize=8.2, color=C4, weight="bold", ha="left",
               path_effects=[pe.withStroke(linewidth=3.0, foreground="white")],
               arrowprops=dict(arrowstyle="-", color=C4, lw=1.0))
    a.set_xticks(x); a.set_xticklabels(labels, fontsize=9.4, color=INK)
    a.set_ylabel("数量（路 / 口）", fontsize=9.0, color=INK)
    a.set_ylim(0, 19)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.4, colors=MUTED)
    a.legend(loc="upper right", fontsize=8.6, frameon=True, facecolor="#FFFFFF", edgecolor=GRID, framealpha=1.0)
    for i in range(len(labels)):
        a.text(x[i] - wbar / 2, need[i] + 0.4, str(need[i]), fontsize=8.4, color=C4, ha="center", weight="bold",
               path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
        a.text(x[i] + wbar / 2, cap[i] + 0.4, str(cap[i]), fontsize=8.4, color=C1, ha="center", weight="bold",
               path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])

    footer(ax, "注：6 路串口设备 vs 标准 4 COM 口主机，缺口靠 485 链补（见算例 4）；继电器与 I/O 富余。参数为工程基准演示。")
    fig.savefig(os.path.join(OUT, "interface-capacity.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：场景联动状态机
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  场景联动状态机：5 个状态 + 联锁条件 + 异常处理",
          "进入「视频」前必须 幕布已下 + 灯已暗；场景可中断、可回滚")

    # 5 个状态框（一排）
    states = [("待机", C5), ("开会", C1), ("培训", C2), ("视频", C3), ("离开", C4)]
    n = len(states)
    bw = 1.9
    gap = (W - 1.4 - n * bw) / (n - 1)
    x0 = 0.7
    sy = 5.25
    bh = 1.15
    for i, (name, c) in enumerate(states):
        x = x0 + i * (bw + gap)
        box(ax, x, sy, bw, bh, "#FFFFFF", c, lw=1.8, r=0.2)
        txt(ax, x + bw / 2, sy + bh / 2, "「" + name + "」", size=10.6, weight="bold", color=c)
        if i < n - 1:
            ax2 = x + bw
            arrow(ax, ax2, sy + bh / 2, ax2 + gap, sy + bh / 2, color=MUTED, lw=1.6)
            txt(ax, ax2 + gap / 2, sy + bh / 2 + 0.28, "切换", size=7.4, color=MUTED, ha="center")

    # 联锁条件框（中）
    gy = 2.95
    box(ax, 0.7, gy, W - 1.4, 1.45, "#EAF2FF", C1, lw=1.5)
    txt(ax, 0.9, gy + 1.18, "联锁条件（进入前必须为真）", size=9.4, weight="bold", color=C1, ha="left")
    txt(ax, 0.9, gy + 0.80, "进入「视频」：幕布已下 ∧ 灯已暗 → 否则投影亮度被环境光吃掉", size=8.4, color=INK, ha="left")
    txt(ax, 0.9, gy + 0.42, "进入「离开」：投影已关 ∧ 吊架已升 → 否则设备带病收工", size=8.4, color=INK, ha="left")

    # 异常处理框（下，两列）
    ey = 1.05
    ew = (W - 1.4 - 0.3) / 2
    box(ax, 0.7, ey, ew, 1.55, "#FDECEA", C4, lw=1.5)
    txt(ax, 0.9, ey + 1.20, "异常处理（状态机回滚）", size=9.2, weight="bold", color=C4, ha="left")
    txt(ax, 0.9, ey + 0.82, "· 中途按「离开」→ 中止未完成序列", size=8.2, color=INK, ha="left")
    txt(ax, 0.9, ey + 0.46, "  幕布下降转上升（可中断）", size=8.2, color=INK, ha="left")
    txt(ax, 0.9, ey + 0.12, "· 幕布未到位 → 禁止开投影", size=8.2, color=INK, ha="left")
    box(ax, 0.7 + ew + 0.3, ey, ew, 1.55, "#FFF7ED", C3, lw=1.5)
    txt(ax, 0.9 + ew + 0.3, ey + 1.20, "反馈与可靠性", size=9.2, weight="bold", color=C3, ha="left")
    txt(ax, 0.9 + ew + 0.3, ey + 0.82, "· 关键设备用 I/O 反馈（非查询）", size=8.2, color=INK, ha="left")
    txt(ax, 0.9 + ew + 0.3, ey + 0.46, "  把状态陈旧率压到 <3%", size=8.2, color=INK, ha="left")
    txt(ax, 0.9 + ew + 0.3, ey + 0.12, "· 设备离线 → 状态告警", size=8.2, color=INK, ha="left")

    footer(ax, "注：场景切换建模为可中断状态机 S(t+1)=f(S(t),e)，事件优先级 离开>开会；联锁写错会让场景互相打架。示意，具体逻辑按工程文件编写。")
    fig.savefig(os.path.join(OUT, "flow-control.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
