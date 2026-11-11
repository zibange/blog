# -*- coding: utf-8 -*-
"""周界警戒雷达产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system          三层架构：前端感知(雷达头) + 信号处理 + 后端联动     （1.4）
  图2 coverage-range       作用距离方程(R_max≈265m) + 120度扇区覆盖面积          （2.2 算例1/5）
  图3 multi-target         多部雷达 300m 杆距扇区拼合，重叠>=20m 消除盲区       （2.2 算例10）
  图4 scene-topology       雷达→球机预置位→视频复核→平台 联动链 + 时延预算      （2.2 算例12/六 场景）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Wedge
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
C1 = "#1F6FEB"   # 主蓝（前端感知/中心侧）
C2 = "#0E9F6E"   # 绿（信号处理/路由）
C3 = "#E8833A"   # 橙（联动/场景）
C4 = "#C2410C"   # 深橙（告警/临界）
C5 = "#7C3AED"   # 紫（总线/电源）
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
# 图 1：三层架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  周界警戒雷达三层架构：前端感知 + 信号处理 + 后端联动",
          "雷达收发头采集回波，信号处理完成 FMCW 解算与 TWS 跟踪，联动层触发球机预置位与平台")

    # 左：前端感知层
    lx, ly, lw, lh = 0.7, 2.3, 3.3, 4.6
    box(ax, lx, ly, lw, lh, "#EFF6FF", C1, lw=2.0)
    txt(ax, lx + lw / 2, ly + lh - 0.5, "前端感知层", size=12.0, weight="bold", color=C1)
    items = ["雷达收发头(天线+射频)", "高速 ADC 采样", "立杆/壁装支架", "防护外壳 IP66"]
    for i, it in enumerate(items):
        yy = ly + lh - 1.55 - i * 0.62
        box(ax, lx + 0.35, yy, lw - 0.7, 0.5, "#FFFFFF", C1, lw=1.2)
        txt(ax, lx + lw / 2, yy + 0.25, it, size=8.8, color=INK)

    # 中：信号处理层
    mx, my, mw, mh = 4.4, 2.3, 3.6, 4.6
    box(ax, mx, my, mw, mh, "#ECFDF5", C2, lw=2.2)
    txt(ax, mx + mw / 2, my + mh - 0.5, "信号处理层", size=12.0, weight="bold", color=C2)
    inner = [
        ("FMCW 距离/速度解算", 5.6),
        ("CFAR 恒虚警检测", 4.75),
        ("点迹凝聚", 3.9),
        ("TWS 航迹关联", 3.05),
    ]
    for name, cy in inner:
        box(ax, mx + 0.35, cy, mw - 0.7, 0.58, "#FFFFFF", C2, lw=1.3)
        txt(ax, mx + mw / 2, cy + 0.29, name, size=9.0, color=INK)
    box(ax, mx + 0.35, my + 0.1, mw - 0.7, 0.55, "#FFF7ED", C4, lw=1.3)
    txt(ax, mx + mw / 2, my + 0.375, "供电 + 防雷", size=9.2, color=C4, weight="bold")

    # 右：后端联动层
    rx, ry, rw, rh = 8.5, 2.3, 4.0, 4.6
    box(ax, rx, ry, rw, rh, "#FFF7ED", C3, lw=2.0)
    txt(ax, rx + rw / 2, ry + rh - 0.5, "后端联动层", size=12.0, weight="bold", color=C3)
    links = [("报警主机 / 继电器", C3, 5.55), ("球机预置位 (PTZ)", C1, 4.55),
             ("声光警号", C4, 3.55), ("安防平台", C5, 2.55)]
    for name, c, cy in links:
        box(ax, rx + 0.35, cy, rw - 0.7, 0.62, "#FFFFFF", c, lw=1.3)
        txt(ax, rx + rw / 2, cy + 0.31, name, size=9.0, color=c)

    # 主箭头：感知→处理→联动（与数据上行同向）
    arrow(ax, lx + lw, ly + lh - 2.2, mx, my + mh - 2.2, color=C2, lw=1.6)
    arrow(ax, mx + mw, my + mh - 2.2, rx, ry + rh - 2.2, color=C3, lw=1.6)
    # 回传虚线（状态/自检）—— 不贴文字
    arrow(ax, rx, ry + 2.0, mx + mw, my + 2.0, color=MUTED, lw=1.1, ls="--")

    footer(ax, "注：前端雷达收发头采集回波，信号处理层完成 FMCW 解距离/速度、CFAR 检测、点迹凝聚与 TWS 航迹关联，联动层把报警映射到球机预置位与平台。三层解耦便于分级运维。工程基准示意。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：作用距离方程 + 扇区覆盖面积
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  雷达作用距离方程给出 R_max≈265 m，120 度扇区单部覆盖约 4.2 万 m2",
          "左：接收功率随距离 R^4 衰减，信噪比门限 -114 dBm 处 R_max≈265 m；右：120 度/200 m 扇区面积")

    # ---- 左图：接收功率(dBm) vs 距离 ----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    R = np.linspace(50, 400, 200)
    # P_r(dBm) = -17.04 - 40*log10(R)  (来自雷达方程与 -114 dBm 灵敏度)
    Pr = -17.04 - 40 * np.log10(R)
    a.plot(R, Pr, color=C1, lw=2.2, zorder=4)
    a.axhline(-114, color=C4, ls="--", lw=1.3, zorder=3)
    a.text(330, -111, "信噪比门限 -114 dBm", fontsize=8.0, color=C4)
    # 标注 R_max
    a.axvline(265, color=C2, ls=":", lw=1.3, zorder=3)
    a.annotate("R_max≈265 m", (265, -114),
               xytext=(265 - 8, -78), fontsize=8.6, color=C2, weight="bold",
               arrowprops=dict(arrowstyle="->", color=C2, lw=1.1))
    a.set_xlabel("距离 R (m)", fontsize=9.0, color=INK)
    a.set_ylabel("接收功率 P_r (dBm)", fontsize=9.0, color=INK)
    a.set_xlim(50, 400); a.set_ylim(-125, -75)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)

    # ---- 右图：120 度扇区覆盖 ----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    b.set_xlim(-2.3, 2.3); b.set_ylim(-0.4, 2.4)
    b.axis("off")
    # 120 度扇区 (中心向上 90 度，30..150 度)
    wed = Wedge((0, 0), 2.0, 30, 150, facecolor="#DCEAFE", edgecolor=C1, linewidth=1.6, zorder=2)
    b.add_patch(wed)
    # 半径线
    b.plot([0, 2.0 * np.cos(np.radians(30))], [0, 2.0 * np.sin(np.radians(30))], color=C1, lw=1.0, ls=":", zorder=3)
    b.plot([0, 0], [0, 2.0], color=C1, lw=1.0, ls=":", zorder=3)
    b.plot([0, 2.0 * np.cos(np.radians(150))], [0, 2.0 * np.sin(np.radians(150))], color=C1, lw=1.0, ls=":", zorder=3)
    # 半径标注
    b.text(0.05, 1.05, "R=200 m", fontsize=8.6, color=C1, weight="bold")
    # 角度弧
    arc = Wedge((0, 0), 0.5, 30, 150, facecolor="none", edgecolor=MUTED, linewidth=1.0, zorder=3)
    b.add_patch(arc)
    b.text(0.30, 0.62, "120 度", fontsize=8.6, color=MUTED)
    # 面积标注
    b.text(0.0, 0.95, "约 4.2 万 m2", fontsize=9.4, color=C2, weight="bold",
           ha="center", path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)
    # 目标点
    b.scatter([0.2, -0.5, 0.6], [1.4, 0.9, 0.5], s=26, color=C4, zorder=6)
    b.text(1.4, 0.1, "目标点迹", fontsize=8.4, color=C4)

    footer(ax, "注：左图 P_r(dBm)=-17.04-40 log10(R) 来自雷达方程，信噪比门限 -114 dBm 对应 R_max≈265 m（人体 RCS 1 m2）；右图 120 度/200 m 扇区面积 A=theta/360*pi*R^2≈4.2 万 m2。工程演示算例。")
    fig.savefig(os.path.join(OUT, "coverage-range.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：多部雷达 300m 杆距扇区拼合，重叠消除盲区
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  多部雷达 300 m 杆距沿界排布，相邻扇区重叠 >=20 m 消除接合盲区",
          "单部 120 度扇区覆盖 4.2 万 m2；杆距取 326 m 时相邻重叠约 20 m，长周界连续无死角")

    # 周界墙线（底部）
    wall_y = 1.7
    ax.plot([0.6, 12.6], [wall_y, wall_y], color="#969696", lw=2.5, zorder=3)
    txt(ax, 12.7, wall_y, "周界", size=8.0, color=MUTED, ha="left", va="center")

    # 比例尺说明
    txt(ax, 0.7, wall_y - 0.45, "示意比例：1 单位长度≈100 m（扇区半径 200 m、杆距 326 m）", size=8.0, color=MUTED)

    # 三座雷达杆（间距 3.26 单位≈326 m）
    poles = [1.5, 4.76, 8.02]
    Rsec = 2.0
    colors = [C1, C2, C5]
    for i, (cx, c) in enumerate(zip(poles, colors)):
        # 杆
        ax.plot([cx, cx], [wall_y, wall_y + 0.5], color="#6B7280", lw=2.4, zorder=4)
        # 120 度扇区（中心向上 90 度，30..150）
        wed = Wedge((cx, wall_y), Rsec, 30, 150, facecolor="#DCEAFE", edgecolor=c,
                    linewidth=1.6, alpha=0.55, zorder=2)
        ax.add_patch(wed)
        # 杆标签
        txt(ax, cx, wall_y + 0.75, f"雷达 {i+1}", size=8.6, color=c, weight="bold")
        txt(ax, cx, wall_y - 0.05, "", size=8.0)

    # 重叠区高亮（雷达1与2之间、雷达2与3之间）
    for i in range(len(poles) - 1):
        cx1, cx2 = poles[i], poles[i + 1]
        # 重叠带中心
        mid = (cx1 + cx2) / 2
        ov = Wedge((mid, wall_y), 0.0, 0, 0)  # placeholder, 下面用矩形高亮
        # 用竖直高亮条标重叠区
        ax.add_patch(FancyBboxPatch((mid - 0.12, wall_y), 0.24, 1.2,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    linewidth=0, edgecolor="none", facecolor="#FCA5A5", alpha=0.45, zorder=3))
        txt(ax, mid, wall_y + 1.35, "重叠≥20 m", size=7.6, color=C4, weight="bold")

    # 目标点迹（放在重叠区与扇区内）
    ax.scatter([poles[0] + 0.9, poles[1] - 0.9, poles[2] + 0.6],
               [wall_y + 0.9, wall_y + 1.1, wall_y + 0.7], s=26, color=C4, zorder=6)
    txt(ax, poles[0] + 0.9, wall_y + 1.45, "入侵目标", size=8.0, color=C4, ha="center")

    # 杆距标注
    arrow(ax, poles[0], wall_y - 0.75, poles[1], wall_y - 0.75, color=MUTED, lw=1.2)
    txt(ax, (poles[0] + poles[1]) / 2, wall_y - 0.95, "杆距≈326 m", size=8.2, color=MUTED)

    footer(ax, "注：相邻 120 度扇区在杆距 326 m 时重叠约 20 m，消除接合盲区；单部覆盖 4.2 万 m2，长周界少布点。工程中重叠取 >=20 m 并留 30% 距离余量。工程基准示意。")
    fig.savefig(os.path.join(OUT, "multi-target.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：场景联动拓扑（雷达→球机→复核→平台）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  探测到目标即驱动球机预置位做二次复核，2–5 s 内完成闭环",
          "雷达报警输出→球机预置位→视频复核→安防平台；时延链 t_link=t_det+t_comm+t_slew")

    # 主链路：5 个节点
    nodes = [
        ("雷达探测\n(目标航迹)", C1, 0.7),
        ("报警输出\n(方位/距离)", C2, 3.1),
        ("球机预置位\n(PTZ)", C3, 5.5),
        ("视频复核\n(人工/AI)", C4, 7.9),
        ("安防平台\n(处置/记录)", C5, 10.3),
    ]
    nw, nh = 2.0, 1.5
    ny = 4.4
    for name, c, nx in nodes:
        box(ax, nx, ny, nw, nh, "#FFFFFF", c, lw=1.8)
        # 两行文字
        lines = name.split("\n")
        txt(ax, nx + nw / 2, ny + nh - 0.42, lines[0], size=9.4, color=c, weight="bold")
        txt(ax, nx + nw / 2, ny + 0.5, lines[1], size=8.6, color=INK)
    # 主箭头（流程同向）
    for i in range(len(nodes) - 1):
        x1 = nodes[i][2] + nw
        x2 = nodes[i + 1][2]
        arrow(ax, x1, ny + nh / 2, x2, ny + nh / 2, color=MUTED, lw=1.5)

    # 时延预算说明条（节点下方）
    bx, by, bw, bh = 0.7, 2.6, 11.6, 1.0
    box(ax, bx, by, bw, bh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, bx + bw / 2, by + 0.5,
        "时延预算：t_det(扫描 1–3 s) + t_comm(<0.5 s) + t_slew(球机转 60 度≈1 s) = 2–5 s；目标 2 m/s 仅移动 4–10 m，仍在扇区内",
        size=8.8, color=INK)

    # 供电/防雷分支（顶部）
    sx, sy, sw, sh = 5.5, 6.3, 2.0, 0.9
    box(ax, sx, sy, sw, sh, "#FFF7ED", C4, lw=1.3)
    txt(ax, sx + sw / 2, sy + sh / 2, "供电 + 防雷 (IP66)", size=8.6, color=C4, weight="bold")
    arrow(ax, sx + sw / 2, sy, nodes[0][2] + nw / 2, ny + nh, color=C4, lw=1.2, ls="--")

    # 右侧复核结果框
    rx, ry, rw, rh = 10.3, 6.3, 2.2, 0.9
    box(ax, rx, ry, rw, rh, "#ECFDF5", C2, lw=1.3)
    txt(ax, rx + rw / 2, ry + rh / 2, "真实入侵 / 误报过滤", size=8.4, color=C2, weight="bold")
    arrow(ax, nodes[3][2] + nw / 2, ny + nh, rx + rw / 2, ry, color=C2, lw=1.2, ls="--")

    footer(ax, "注：雷达给出方位/距离后即时驱动球机预置位，2–5 s 内完成视频二次复核；CFAR+航迹确认已在雷达端过滤飞鸟风雨，复核只针对稳定航迹目标。工程基准示意。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
