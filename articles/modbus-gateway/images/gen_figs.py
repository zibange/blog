# -*- coding: utf-8 -*-
"""Modbus 协议网关产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-topology    Modbus 网关系统拓扑（南向 RS-485 多设备 → 网关 → 北向以太网）  （1.1）
  图2 poll-timing      轮询周期与串口负载（30 台≈1.6 s，2 s 刷新红线）                 （2.2）
  图3 point-map        寄存器点表映射（从站寄存器 → 网关点表 → 北向点位）              （2.5）
  图4 byte-order       字节序/字序（float32 跨 2 寄存器 4 种拼法）                     （2.6）
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
# 图 1：Modbus 网关系统拓扑
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  Modbus 网关系统拓扑：南向串口 → 网关 → 北向以太网",
          "网关是协议边界也是主站边界：串口侧当唯一主站，北向把串口扇出成并发 TCP 服务")

    # 北向上位（顶，高亮紫）—— top 须低于副标题 y=7.58
    nx, ny, nw, nh = 4.4, 5.95, 4.4, 1.25
    box(ax, nx, ny, nw, nh, "#F3ECFD", C5, lw=2.2, r=0.2)
    txt(ax, nx + nw / 2, ny + nh - 0.40, "北向上位系统", size=11.0, weight="bold", color=C5)
    txt(ax, nx + nw / 2, ny + 0.62, "SCADA / 楼宇 BA / 能源平台", size=7.8, color=INK)
    txt(ax, nx + nw / 2, ny + 0.24, "Modbus TCP :502 / MQTT / OPC UA", size=7.8, color=MUTED)

    # 网关（中央高亮橙）
    gx, gy, gw, gh = 5.0, 4.20, 3.2, 1.35
    box(ax, gx, gy, gw, gh, "#FFF1E6", C3, lw=2.4, r=0.22)
    txt(ax, gx + gw / 2, gy + gh - 0.42, "Modbus 协议网关", size=11.4, weight="bold", color=C4)
    txt(ax, gx + gw / 2, gy + 0.66, "转换引擎 + 点表", size=8.0, color=INK)
    txt(ax, gx + gw / 2, gy + 0.28, "串口主站 → TCP 服务", size=8.0, color=MUTED)
    arrow(ax, nx + nw / 2, ny, nx + nw / 2, gy + gh, color=C5, lw=2.0)
    txt(ax, nx + nw / 2 + 0.28, (ny + gy + gh) / 2, "北向并发", size=7.6, color=C5, weight="bold", ha="left")

    # 两路 RS-485 总线 + 设备
    bus_y = 2.35
    bus_spans = [(0.6, 5.2), (7.7, 12.6)]
    seg_labels = ["RS-485 网段 A（≤32 节点）", "RS-485 网段 B（≤32 节点）"]
    devs = [("电能表", "变频器", "温控表"), ("流量计", "PLC", "传感器")]
    for i, (x0, x1) in enumerate(bus_spans):
        # 网关到总线
        arrow(ax, gx + gw / 2 + (i - 0.5) * 1.4, gy, (x0 + x1) / 2, bus_y + 0.30, color=C3, lw=1.6)
        ax.add_patch(plt.Rectangle((x0, bus_y), x1 - x0, 0.30, color=CGREY, zorder=1))
        txt(ax, (x0 + x1) / 2, bus_y - 0.34, seg_labels[i], size=7.6, color=MUTED)
        span = x1 - x0
        for j in range(3):
            dx = x0 + span * (j + 0.5) / 3
            dw, dh = 1.35, 1.05
            box(ax, dx - dw / 2, 0.70, dw, dh, "#EAFFF4", C2, lw=1.5)
            txt(ax, dx, 0.70 + dh / 2 + 0.16, devs[i][j], size=7.8, color=C2, weight="bold")
            txt(ax, dx, 0.70 + 0.32, "Modbus 从站", size=6.6, color=MUTED)
            arrow(ax, dx, 1.75, dx, bus_y, color=CGREY, lw=1.0, ls=":")
    txt(ax, 6.6, bus_y + 0.62, "120 Ω 终端电阻（两端）+ 屏蔽单点接地", size=7.4, color=MUTED)

    footer(ax, "注：网关在串口侧独占主站、北向把串口扇出成可并发访问的 TCP 服务；一条 RS-485 节点上限 32、最长 1200 m@9600。示意图，设备数按工程基准。")
    fig.savefig(os.path.join(OUT, "arch-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：轮询周期与串口负载
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  轮询周期与串口负载：30 台 ≈1.6 s，60 台 ≈3.3 s",
          "@9600 单帧≈13 ms；刷新要求 2 s 时 30 台达标、60 台越线")

    # 左：单条读帧往返 ≈54 ms
    lx, ly, lw, lh = 0.95, 2.2, 5.2, 4.2
    a1 = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a1.set_facecolor("#FFFFFF")
    a1.barh([0], [54], height=0.5, color=C1, alpha=0.85, edgecolor=C1, zorder=3)
    a1.set_xlim(0, 60); a1.set_ylim(-0.6, 1.2); a1.set_yticks([])
    a1.set_xlabel("单台读帧往返（ms）", fontsize=9.0, color=INK)
    a1.set_title("一台表读 10 寄存器 ≈ 54 ms", fontsize=9.4, color=C1, weight="bold", pad=8)
    a1.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9)
    for sp in a1.spines.values():
        sp.set_color(GRID)
    a1.tick_params(labelsize=8.0, colors=MUTED)
    a1.text(27, 0.0, "请求 13 + 应答 29 + 静默 12 ≈ 54 ms", fontsize=8.0, color="#FFFFFF",
            weight="bold", ha="center", va="center", zorder=5)

    # 右：轮询周期 vs 设备数
    rx, ry, rw, rh = 6.6, 2.2, 5.8, 4.2
    a2 = fig.add_axes([rx / W, ry / H, rw / W, rh / H])
    a2.set_facecolor("#FFFFFF")
    labels = ["20 台\n(1.1 s)", "30 台\n(1.6 s)", "60 台\n(3.3 s)", "120 台\n(6.5 s)"]
    vals = [1.09, 1.63, 3.26, 6.52]
    colors = [C2, C2, C4, C4]
    x = np.arange(len(labels))
    a2.bar(x, vals, width=0.5, color=colors, alpha=0.9, edgecolor=colors, linewidth=1.2,
           zorder=3, label="轮询一圈周期 (s)")
    a2.axhline(2.0, color=C4, ls="--", lw=1.6, zorder=4, label="2 s 刷新红线")
    a2.legend(loc="upper left", fontsize=8.4, frameon=True, facecolor="#FFFFFF",
              edgecolor=GRID, framealpha=1.0)
    a2.set_xticks(x); a2.set_xticklabels(labels, fontsize=8.2, color=INK)
    a2.set_ylabel("轮询周期（秒/圈）", fontsize=9.0, color=INK)
    a2.set_ylim(0, 7.2)
    a2.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a2.spines.values():
        sp.set_color(GRID)
    a2.tick_params(labelsize=8.0, colors=MUTED)
    for i, v in enumerate(vals):
        a2.text(i, v + 0.18, "%.2f" % v, fontsize=8.4, color=INK, ha="center", weight="bold")

    footer(ax, "注：轮询周期 = 设备数 × 单台往返（@9600，每字节 11 位）；刷新要求 2 s 时 30 台达标、60 台越线，须提波特率或拆网段（工程演示）。")
    fig.savefig(os.path.join(OUT, "poll-timing.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：寄存器点表映射
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  寄存器点表映射：从站寄存器 → 网关点表 → 北向点位",
          "Modbus 无自动发现，网关靠一张人工点表活着；偏移与区前缀须逐项对齐")

    # 列1：从站寄存器
    c1x, c1y, c1w, c1h = 0.7, 2.4, 3.4, 4.3
    box(ax, c1x, c1y, c1w, c1h, "#EAFFF4", C2, lw=1.8)
    txt(ax, c1x + c1w / 2, c1y + c1h - 0.40, "南向：从站寄存器", size=11.0, weight="bold", color=C2)
    rows1 = [("从站 #5", "功能码 03"), ("保持寄存器 40100", "偏移 0x0063"),
             ("保持寄存器 40101", "偏移 0x0064"), ("数据类型 float32", "2 寄存器")]
    for k, (a, b) in enumerate(rows1):
        y = c1y + c1h - 1.05 - k * 0.78
        txt(ax, c1x + 0.30, y, a, size=8.6, color=INK, ha="left", weight="bold")
        txt(ax, c1x + 0.30, y - 0.32, b, size=7.8, color=MUTED, ha="left")

    # 列2：网关点表
    c2x, c2y, c2w, c2h = 4.9, 2.0, 3.4, 5.1
    box(ax, c2x, c2y, c2w, c2h, "#FFF1E6", C3, lw=2.2)
    txt(ax, c2x + c2w / 2, c2y + c2h - 0.42, "网关点表（灵魂）", size=11.4, weight="bold", color=C4)
    rows2 = [("从站 5 · 03 · 100", "→ 北向点名"), ("float32 · CDAB", "→ 字节序"),
             ("× 0.01 缩放", "→ 工程量"), ("scan-on-change", "→ 上云策略")]
    for k, (a, b) in enumerate(rows2):
        y = c2y + c2h - 1.15 - k * 0.92
        txt(ax, c2x + 0.28, y, a, size=8.6, color=INK, ha="left", weight="bold")
        txt(ax, c2x + 0.28, y - 0.34, b, size=7.8, color=MUTED, ha="left")

    # 列3：北向点位
    c3x, c3y, c3w, c3h = 9.1, 2.4, 3.4, 4.3
    box(ax, c3x, c3y, c3w, c3h, "#F3ECFD", C5, lw=1.8)
    txt(ax, c3x + c3w / 2, c3y + c3h - 0.40, "北向：统一点位", size=11.0, weight="bold", color=C5)
    rows3 = [("point.temp.5", "MQTT 主题"), ("BACnet AV 3201", "楼控对象"),
             ("寄存器值 23.50", "工程量值"), ("2 s / 变化上报", "刷新策略")]
    for k, (a, b) in enumerate(rows3):
        y = c3y + c3h - 1.05 - k * 0.78
        txt(ax, c3x + 0.30, y, a, size=8.6, color=INK, ha="left", weight="bold")
        txt(ax, c3x + 0.30, y - 0.32, b, size=7.8, color=MUTED, ha="left")

    arrow(ax, c1x + c1w, c1y + c1h * 0.55, c2x, c2y + c2h * 0.55, color=C3, lw=2.0)
    txt(ax, (c1x + c1w + c2x) / 2, c1y + c1h * 0.55 + 0.35, "解析+映射", size=8.0, color=C3, weight="bold")
    arrow(ax, c2x + c2w, c2y + c2h * 0.55, c3x, c3y + c3h * 0.55, color=C5, lw=2.0)
    txt(ax, (c2x + c2w + c3x) / 2, c2y + c2h * 0.55 + 0.35, "封装北向", size=8.0, color=C5, weight="bold")

    footer(ax, "注：点表把「从站+功能码+寄存器+字节序+缩放」映射成「北向点名」，是 Modbus 工程最值钱的文件；偏移 40001 与 0x0000 须逐项对齐（图2 正文 2.5）。示意图。")
    fig.savefig(os.path.join(OUT, "point-map.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：字节序 / 字序
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  字节序/字序：float32 跨 2 寄存器有 4 种拼法",
          "Modbus 只搬 16 位寄存器；配错一种读到的是与真值无关的乱数，且不报错")

    items = [("ABCD", "A B | C D", "大端字+大端字节（常见）", C1),
             ("CDAB", "C D | A B", "字交换 Word Swap（常见）", C3),
             ("BADC", "B A | D C", "字节交换 Byte Swap", C4),
             ("DCBA", "D C | B A", "小端 Intel（少见）", C5)]
    n = len(items)
    bw = 2.85
    gap = (W - 1.2 - n * bw) / (n - 1)
    x0 = 0.6
    sy = 4.55
    bh = 2.55
    for i, (name, layout, desc, c) in enumerate(items):
        x = x0 + i * (bw + gap)
        box(ax, x, sy, bw, bh, "#FFFFFF", c, lw=1.9, r=0.2)
        txt(ax, x + bw / 2, sy + bh - 0.38, name, size=12.0, weight="bold", color=c)
        # 两寄存器框
        rw, rh = 1.15, 0.72
        rgap = 0.18
        rx0 = x + (bw - (2 * rw + rgap)) / 2
        for j in range(2):
            bx = rx0 + j * (rw + rgap)
            box(ax, bx, sy + 1.15, rw, rh, "#F6F8FA", c, lw=1.4)
            reg = "reg1" if j == 0 else "reg2"
            txt(ax, bx + rw / 2, sy + 1.15 + rh / 2, reg, size=8.2, color=INK, weight="bold")
        txt(ax, x + bw / 2, sy + 0.78, layout, size=8.6, color=INK, weight="bold")
        txt(ax, x + bw / 2, sy + 0.32, desc, size=7.4, color=MUTED)

    # 底部说明框（真实值示例 + 建表核对方法）
    gy = 1.45
    box(ax, 0.6, gy, W - 1.2, 2.05, "#FFF7ED", C3, lw=1.5)
    txt(ax, 0.9, gy + 1.62, "真实值示例：温度 23.50 ℃ 占两个 16 位寄存器（字节 A B | C D）",
        size=9.4, weight="bold", color=C3, ha="left")
    txt(ax, 0.9, gy + 1.10,
        "设备按 CDAB 发、网关按 ABCD 解 → 前后两寄存器对调，读数与真值无关（页面显示正常、不报错）",
        size=8.4, color=INK, ha="left")
    txt(ax, 0.9, gy + 0.60,
        "建表前先用一台真设备读已知浮点，四种拼法逐一核对找到正确项，再批量套用",
        size=8.4, color=MUTED, ha="left")

    footer(ax, "注：网关须支持四种字节序可配；建点表前用一台真设备读已知浮点、四种拼法逐一核对，找到正确项再批量套用（正文 2.6）。示意图。")
    fig.savefig(os.path.join(OUT, "byte-order.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
