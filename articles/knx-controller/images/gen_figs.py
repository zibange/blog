# -*- coding: utf-8 -*-
"""KNX 智能楼宇控制器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-topology      KNX 系统拓扑（支线/干线/耦合器/IP 路由）     （1.1）
  图2 group-address       组地址发布/订阅模型（无中心主机）            （2.1）
  图3 telegram-timing     报文时长与总线负载（50% 红线）               （3.2 / 3.3）
  图4 commissioning-flow  工程组态与调试流程（ETS 下载是停机操作）     （4.2）
"""
import os
import numpy as np
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
# 图 1：KNX 系统拓扑
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  KNX 系统拓扑：支线 — 干线 — 耦合器 — IP 路由",
          "设备并联挂总线，按组地址广播；耦合器按订阅相关性过滤转发")

    # IP 路由器（顶，高亮）—— top = 7.15，须低于副标题 y=7.58，避免压字
    rx, ry, rw, rh = 5.0, 5.90, 3.2, 1.25
    box(ax, rx, ry, rw, rh, "#F3ECFD", C5, lw=2.2, r=0.2)
    txt(ax, rx + rw / 2, ry + rh - 0.40, "KNX/IP 路由器", size=11.0, weight="bold", color=C5)
    txt(ax, rx + rw / 2, ry + 0.62, "隧道 / 路由 → 以太网 / 平台 / App", size=7.8, color=INK)
    txt(ax, rx + rw / 2, ry + 0.24, "上位访问 + 远程诊断", size=7.8, color=MUTED)

    # 干线（Backbone）粗线，「干线」标签放在粗线内部左端（避免右边界被裁）
    ax.add_patch(plt.Rectangle((1.0, 5.35), 11.2, 0.34, color=CGREY, zorder=1))
    txt(ax, 1.25, 5.52, "干线", size=7.6, color="#6B7680", ha="left", zorder=3)
    arrow(ax, rx + rw / 2, ry, rx + rw / 2, 5.69, color=C5, lw=2.0)

    # 3 个线路耦合器（顶边贴住干线底边）
    lines_x = [2.3, 6.6, 10.9]
    for cx in lines_x:
        cw, ch = 1.5, 0.85
        box(ax, cx - cw / 2, 4.50, cw, ch, "#FFFFFF", C1, lw=1.7)
        txt(ax, cx, 4.50 + ch - 0.30, "线路耦合器", size=8.4, weight="bold", color=C1)
        txt(ax, cx, 4.50 + 0.28, "智能过滤器", size=7.2, color=MUTED)
        arrow(ax, cx, 4.50, cx, 3.85, color=C1, lw=1.6)

    # 3 条支线总线 + 设备
    line_spans = [(0.6, 4.0), (4.9, 8.3), (9.0, 12.8)]
    bus_y = 3.55
    devs = [("开关驱动器", "面板", "传感器"),
            ("调光驱动器", "温控面板", "窗帘模块"),
            ("IP 接口", "二进制输入", "存在感应")]
    for i, (x0, x1) in enumerate(line_spans):
        ax.add_patch(plt.Rectangle((x0, bus_y), x1 - x0, 0.30, color=CGREY, zorder=1))
        txt(ax, (x0 + x1) / 2, bus_y - 0.34, "支线 %d（≤64 设备，≤1 A）" % (i + 1),
            size=7.6, color=MUTED)
        # 耦合器到总线
        arrow(ax, lines_x[i], 4.50, lines_x[i], bus_y + 0.30, color=C1, lw=1.4)
        # 3 个设备
        span = x1 - x0
        for j in range(3):
            dx = x0 + span * (j + 0.5) / 3
            dw, dh = 1.05, 0.95
            box(ax, dx - dw / 2, 1.85, dw, dh, "#FFFFFF", C2, lw=1.5)
            txt(ax, dx, 1.85 + dh / 2 + 0.14, devs[i][j], size=7.6, color=C2, weight="bold")
            txt(ax, dx, 1.85 + 0.30, "总线设备", size=6.8, color=MUTED)
            arrow(ax, dx, 2.80, dx, bus_y, color=CGREY, lw=1.0, ls=":")

    footer(ax, "注：拓扑分「支线—干线—区域」三级，耦合器按组地址订阅相关性过滤转发，压住干线负载；SELV 总线只供通信电流，执行器另接 220 V。示意图，设备数按工程基准。")
    fig.savefig(os.path.join(OUT, "arch-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：组地址发布/订阅模型
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  组地址发布/订阅模型：65536 个地址，订阅即响应",
          "无中心主机：一条报文打到组 G，所有订阅 G 的设备各自执行")

    # 发布者
    px, py, pw, ph = 0.7, 3.5, 2.5, 1.5
    box(ax, px, py, pw, ph, "#FFF7ED", C3, lw=1.8)
    txt(ax, px + pw / 2, py + ph - 0.40, "存在感应器（发布者）", size=9.4, weight="bold", color=C3)
    txt(ax, px + pw / 2, py + 0.62, "检测有人 → 发布", size=8.0, color=INK)
    txt(ax, px + pw / 2, py + 0.24, "组 G = 走廊照明", size=8.0, color=INK)

    # 组地址中心节点
    cx0, cy0, cw, ch = 5.0, 3.0, 3.2, 2.0
    box(ax, cx0, cy0, cw, ch, "#F3ECFD", C5, lw=2.2)
    txt(ax, cx0 + cw / 2, cy0 + ch - 0.45, "组地址 G", size=12.0, weight="bold", color=C5)
    txt(ax, cx0 + cw / 2, cy0 + 1.25, "16 位广播地址", size=8.4, color=INK)
    txt(ax, cx0 + cw / 2, cy0 + 0.85, "最多 65536 个", size=8.4, color=INK)
    txt(ax, cx0 + cw / 2, cy0 + 0.45, "发布/订阅的寻址对象", size=7.6, color=MUTED)

    # 发布箭头
    arrow(ax, px + pw, py + ph / 2, cx0, cy0 + ch * 0.65, color=C3, lw=2.0)
    txt(ax, (px + pw + cx0) / 2, py + ph / 2 + 0.35, "发布报文", size=8.0, color=C3, weight="bold")

    # 订阅者
    subs = [("开关驱动器", "执行开灯"), ("调光驱动器", "联动调光"), ("平台接口", "状态上报")]
    sy = 5.7
    sh = 1.0
    gap = 0.35
    for i, (name, desc) in enumerate(subs):
        y = sy - i * (sh + gap)
        box(ax, 9.6, y, 2.9, sh, "#EAF7F0", C2, lw=1.8)
        txt(ax, 9.6 + 0.20, y + sh - 0.32, name + "（订阅 G）", size=9.2, weight="bold", color=C2, ha="left")
        txt(ax, 9.6 + 0.20, y + 0.30, desc, size=8.0, color=INK, ha="left")
        arrow(ax, cx0 + cw, 3.7, 9.6, y + sh / 2, color=C2, lw=1.6)
    txt(ax, 10.6, 6.95, "订阅者各自执行", size=8.0, color=C2, weight="bold")

    footer(ax, "注：传统控制是「A→主机→B」星型转发；KNX 是「发布者打到组 G，订阅者响应」，无中心主机。换面板/换执行器只改组地址绑定，不改布线。示意图。")
    fig.savefig(os.path.join(OUT, "group-address.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：报文时长与总线负载
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  报文时序与总线负载：单报 ≈30 ms，50% 红线 ≈17 条/s",
          "100% 饱和 ≈33 条/s；推荐 ≤50% 即 ≤17 条/s，高频采样须错峰")

    # 左：单条报文时长
    lx, ly, lw, lh = 0.95, 2.2, 5.2, 4.2
    a1 = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a1.set_facecolor("#FFFFFF")
    a1.barh([0], [30], height=0.5, color=C1, alpha=0.85, edgecolor=C1, zorder=3)
    a1.set_xlim(0, 35); a1.set_ylim(-0.6, 1.2); a1.set_yticks([])
    a1.set_xlabel("单条标准报文时长（ms）", fontsize=9.0, color=INK)
    a1.set_title("一条满载报文 ≈ 30 ms", fontsize=9.4, color=C1, weight="bold", pad=8)
    a1.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9)
    for sp in a1.spines.values():
        sp.set_color(GRID)
    a1.tick_params(labelsize=8.0, colors=MUTED)
    a1.text(15, 0.0, "23 字节 × 11 位 / 9600 ≈ 30 ms", fontsize=8.4, color="#FFFFFF",
            weight="bold", ha="center", va="center", zorder=5)

    # 右：每秒报文数 vs 50% 红线
    rx, ry, rw, rh = 6.6, 2.2, 5.8, 4.2
    a2 = fig.add_axes([rx / W, ry / H, rw / W, rh / H])
    a2.set_facecolor("#FFFFFF")
    labels = ["64 传感每 5 s\n(13 条/s)", "64 传感每 1 s\n(64 条/s)", "能耗计量\n每 0.1 s"]
    vals = [13, 64, 100]
    colors = [C2, C4, C4]
    x = np.arange(len(labels))
    a2.bar(x, vals, width=0.5, color=colors, alpha=0.9, edgecolor=colors, linewidth=1.2,
           zorder=3, label="每秒报文数")
    a2.axhline(17, color=C4, ls="--", lw=1.6, zorder=4, label="50% 红线（≈17 条/s）")
    a2.legend(loc="upper left", fontsize=8.4, frameon=True, facecolor="#FFFFFF",
              edgecolor=GRID, framealpha=1.0)
    a2.set_xticks(x); a2.set_xticklabels(labels, fontsize=8.2, color=INK)
    a2.set_ylabel("每秒报文数（条/s）", fontsize=9.0, color=INK)
    a2.set_ylim(0, 110)
    a2.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a2.spines.values():
        sp.set_color(GRID)
    a2.tick_params(labelsize=8.0, colors=MUTED)
    # 值标签：首条太矮、贴近红线 → 放条内白字；其余放条顶上方
    a2.text(0, 6.5, "13", fontsize=8.6, color="#FFFFFF", ha="center", weight="bold", zorder=5)
    for i, v in [(1, 64), (2, 100)]:
        a2.text(i, v + 2.5, str(v), fontsize=8.6, color=INK, ha="center", weight="bold")

    footer(ax, "注：单报 ≈30 ms（23 字节帧，11 位曼彻斯特）；100% 饱和 ≈33 条/s，工程经验 ≤50% 即 ≤17 条/s；高频采样远超红线必拥堵（工程演示）。")
    fig.savefig(os.path.join(OUT, "telegram-timing.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：工程组态与调试流程
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  工程组态与调试流程：下载是「停机操作」",
          "先离线编全楼参数，再分批夜间下载；组地址表正确比速度更重要")

    steps = [("① 规划物理地址", "区域/线路/设备\n3 级 4/4/8 位", C5),
             ("② 分配组地址", "主/中/子 5/3/8\n绑定面板与负载", C1),
             ("③ 载入应用参数", "每设备功能配置\n哪路对应哪组", C2),
             ("④ 下载到设备", "停机操作\n2–5 s/台", C4),
             ("⑤ 全场景回归", "开会/离开/报警\n逐场景验证", C3)]
    n = len(steps)
    bw = 2.05
    gap = (W - 1.4 - n * bw) / (n - 1)
    x0 = 0.7
    sy = 5.0
    bh = 1.7
    for i, (name, desc, c) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, sy, bw, bh, "#FFFFFF", c, lw=1.8, r=0.2)
        txt(ax, x + bw / 2, sy + bh - 0.45, name, size=9.6, weight="bold", color=c)
        for k, dl in enumerate(desc.split("\n")):
            txt(ax, x + bw / 2, sy + 0.95 - k * 0.42, dl, size=7.8, color=INK)
        if i < n - 1:
            ax2 = x + bw
            arrow(ax, ax2, sy + bh / 2, ax2 + gap, sy + bh / 2, color=MUTED, lw=1.6)
            txt(ax, ax2 + gap / 2, sy + bh / 2 + 0.30, "→", size=9.0, color=MUTED, ha="center")

    # 下载时间账（底部说明框）
    gy = 2.4
    box(ax, 0.7, gy, W - 1.4, 1.6, "#FFF7ED", C3, lw=1.5)
    txt(ax, 0.9, gy + 1.28, "下载时间账（一条 64 设备支线，顺序下载）", size=9.4, weight="bold", color=C3, ha="left")
    txt(ax, 0.9, gy + 0.88,
        "T_dl ≈ 64 × 3.5 ≈ 224 s ≈ 3.7 min —— 下错要重来，先离线编对再夜间分批下",
        size=8.2, color=INK, ha="left")
    txt(ax, 0.9, gy + 0.40, "组地址表的正确性是第一优先级；下载期间该设备不响应正常报文，须避开使用时段",
        size=8.0, color=MUTED, ha="left")

    footer(ax, "注：ETS 工程文件 + 组地址表是 KNX 项目的核心资产，应纳入版本管理并每次改前备份。示意图。")
    fig.savefig(os.path.join(OUT, "commissioning-flow.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
