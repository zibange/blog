# -*- coding: utf-8 -*-
"""工业以太网交换机产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system     三层组网 + 四类角色 + 冗余供电（1.4）
  图2 ring-recovery   环网倒换时间对比（左）+ 50 ms 四段分解与 MAC 表陷阱（右）（算例 4/5）
  图3 power-budget    N+1 冗余电源带载核算（左）+ PoE 功率预算与线损（右）（算例 7/8）
  图4 scene-topology  六类场景共用骨架（五）

配色、坐标系用法沿用成熟模板（见 content-factory §7.3）：
  - newfig() 把整幅画布当成一个 axes（数据坐标 0~W, 0~H）；
  - footer() 单独开一个 add_axes（用图幅比例），不与绘图区混用 tight 裁剪；
  - 全局字体 Microsoft YaHei；戒用 ↔/✓/≪ 等无字形字符（用文字代替）。

Python 教学要点：
  - os.path.dirname(os.path.abspath(__file__))：脚本所在目录，图片输出到本目录；
  - matplotlib.use("Agg")：无界面后端，自动化环境只出 PNG；
  - FancyBboxPatch / FancyArrowPatch：画圆角框与箭头；
  - add_axes([left,bottom,width,height])：图幅比例定位嵌入式小图（柱状图）；
  - a.set_yscale("log")：对数纵轴，用于跨数量级的倒换时间对比。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- light 主题配色（浅底深字，适配浅色 IDE 主题）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（核心管理 / ERPS）
C2 = "#0E9F6E"   # 绿（汇聚 / PoE 受控）
C3 = "#E8833A"   # 橙（现场接入 / MRP）
C4 = "#C2410C"   # 深橙（RSTP / 陷阱 / 告警）
C5 = "#7C3AED"   # 紫（供电 / PTP / 安全）
CGREY = "#CBD2D9"


def newfig():
    """整幅画布当成一个坐标轴：数据坐标 0~W / 0~H。"""
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-"):
    """圆角矩形：x/y 左下角，w/h 宽高，fc/ec 填充与描边。"""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       alpha=alpha, linestyle=ls, zorder=2)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=9.4, color=INK, weight="normal",
        ha="center", va="center", zorder=6):
    """统一文字样式：显式指定字体族，避免中文丢失。"""
    ax.text(x, y, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily="Microsoft YaHei")


def title(ax, t, sub=None):
    """图标题 + 副标题。顶边控制在 ~7.4 以内。"""
    txt(ax, W / 2, H - 0.52, t, size=14.0, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.00, sub, size=8.6, color=MUTED, ha="center")


def footer(ax, s):
    """底部说明条：单独开一个 axes，避免与绘图区坐标系混用。"""
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=1)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=7.3, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：三层网络 + 四类角色 + 冗余供电
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  工业以太网三层组网 + 冗余供电",
          "现场接入环自愈、汇聚层跨环隔离、核心层统一网管；宽温与冗余电源贯穿现场")

    # 三层横向网络带（自上而下：核心 / 汇聚 / 现场）
    layers = [
        ("核心 / 管理层 · 万兆上联", C1, "#EFF6FF", 6.05,
         ["监控平台 / SCADA 服务器", "核心交换机 + 网管平台", "SNMP Trap / 日志 / 端口镜像"]),
        ("汇聚层 · 跨环三层隔离", C2, "#ECFDF5", 4.55,
         ["汇聚交换机（万兆光口）", "VLAN 间路由 / 环域隔离", "链路聚合 LACP + RSTP 兜底"]),
        ("现场接入层 · ERPS / MRP 光环", C3, "#FFF7ED", 3.05,
         ["导轨式交换机（电口接 PLC/摄像机）", "光纤首尾成环，断链 50 ms 自愈", "PoE 供电 / 宽温 -40~75 ℃"]),
    ]
    bx, bw = 0.6, 8.0
    for name, c, fill, yy, items in layers:
        box(ax, bx, yy, bw, 1.25, fill, c, lw=1.9)
        txt(ax, bx + 0.22, yy + 1.25 - 0.32, name, size=10.4, weight="bold", color=c, ha="left")
        for j, it in enumerate(items):
            txt(ax, bx + 0.22 + j * 2.62, yy + 0.38, it, size=7.6, color=INK, ha="left")
    # 层间箭头
    arrow(ax, bx + bw / 2, 6.05, bx + bw / 2, 5.80, color=C1, lw=1.7)
    arrow(ax, bx + bw / 2, 4.55, bx + bw / 2, 4.30, color=C2, lw=1.7)

    # 右侧冗余供电与工业硬化竖块
    ox, oy, ow, oh = 9.05, 3.05, 3.55, 4.25
    box(ax, ox, oy, ow, oh, "#F5F3FF", C5, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.42, "工业硬化 / 冗余供电", size=10.6, weight="bold", color=C5)
    items = [
        "双路宽压电源（N+1 带全载）",
        "PoE：af/at/bt 15.4~90 W",
        "无风扇金属壳 IP40",
        "宽温 -40~+75 ℃",
        "GB/T 17626 EMC 抗扰",
        "硬件 PTP 纳秒级对时",
        "光纤上联抗电磁耦合",
        "SNMP/Web/CLI 统一网管",
    ]
    for i, s in enumerate(items):
        yy = oy + oh - 1.02 - i * 0.40
        txt(ax, ox + 0.25, yy, s, size=8.5, color=INK, ha="left")
    arrow(ax, bx + bw, 5.2, ox, 5.2, color=C5, lw=1.5, ls="--")

    # 底部属性行
    axb = 0.6
    box(ax, axb, 1.75, 12.0, 0.92, "#F6F8FA", CGREY, lw=1.2)
    txt(ax, axb + 6.0, 2.42,
        "核心指标：交换容量（背板带宽） · 包转发率（按 64 B 小包） · 环网倒换与业务恢复 · 供电与 PoE 预算",
        size=8.8, color=INK, weight="bold")
    txt(ax, axb + 6.0, 2.02,
        "先定业务可容忍的中断时间与环境等级，再倒推协议与硬件——不是先看 datasheet 上哪个数字最小",
        size=8.0, color=MUTED)

    footer(ax, "注：依据 GB/T 30094-2013、DL/T 1241-2024、IEC 62439-2/-3、ITU-T G.8032；环网倒换 ERPS <50 ms、MRP ≤200 ms、RSTP 1~2 s。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：环网倒换时间对比（左）+ 50 ms 四段分解与 MAC 表陷阱（右）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  环网倒换时间 + 业务恢复陷阱",
          "左：协议倒换跨数量级（对数轴）；右：50 ms 四段分解，MAC/ARP 表未刷新会把中断拉长到分钟级")

    # --- 左侧：倒换时间对比（嵌入式对数柱状图）---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 协议倒换时间对比（纵轴 ms，对数）", size=10.2,
        weight="bold", color=C4)
    # 修复：axes 底部抬到 2.95 给 x 轴标签腾位，高度缩到 3.15
    a = fig.add_axes([lx / W, 2.95 / H, lw / W, 3.15 / H])
    a.set_facecolor("#FFFFFF")
    labels = ["RSTP\n1~2 s", "MRP\n≤200 ms", "ERPS\n<50 ms"]
    vals = [1500.0, 200.0, 50.0]
    x = np.arange(3)
    bars = a.bar(x, vals, 0.52, color=[C4, C3, C2], zorder=3)
    for bar, lab in zip(bars, ["1500", "200", "50"]):
        a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.12,
               lab, ha="center", va="bottom", fontsize=9.5, color=INK,
               weight="bold", zorder=5)
    a.set_yscale("log")
    a.set_ylim(20, 4000)
    a.set_xticks(x)
    a.set_xticklabels(labels, fontsize=8.6, color=INK)
    # 去掉竖排 ylabel（会挤进左栏被裁），单位已写进小标题
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.0, colors=MUTED)
    box(ax, lx, 1.42, lw, 0.92, "#ECFDF5", C2, lw=1.7)
    txt(ax, lx + lw / 2, 2.06,
        "PRP / HSR（IEC 62439-3）：双发选收，0 切换、0 丢帧",
        size=8.4, color=C2, weight="bold")
    txt(ax, lx + lw / 2, 1.68,
        "能忍秒级用 RSTP；产线要毫秒级；变电站保护要零中断",
        size=7.9, color=INK)

    # --- 右侧：50 ms 四段分解（分段横条）+ 陷阱结论 ---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② 50 ms 倒换的四段分解（工程估算）", size=10.2,
        weight="bold", color=C1)
    stages = [
        ("故障检测", "链路 down 快速检测", "约 10 ms", C1, 5.62),
        ("R-APS 传播", "每站约 1 ms × 站数", "约 4 ms", C2, 4.62),
        ("放开 RPL 端口", "阻塞转转发", "数 ms", C3, 3.62),
        ("刷 MAC 表", "flush 触发重学习", "数 ms", C5, 2.62),
    ]
    for name, desc, val, c, yy in stages:
        box(ax, rx, yy, rw, 0.88, "#F6F8FA", c, lw=1.5)
        txt(ax, rx + 0.18, yy + 0.44, name, size=9.2, weight="bold", color=c, ha="left")
        txt(ax, rx + 1.65, yy + 0.44, desc, size=8.2, color=INK, ha="left")
        txt(ax, rx + rw - 0.15, yy + 0.44, val, size=9.0, weight="bold", color=c, ha="right")
    box(ax, rx, 1.42, rw, 0.92, "#FFF1EE", C4, lw=1.7)
    txt(ax, rx + rw / 2, 2.06,
        "陷阱：MAC 表老化 300 s / ARP 约 240 s（算例 5）",
        size=8.4, color=C4, weight="bold")
    txt(ax, rx + rw / 2, 1.68,
        "未 flush 则帧仍走断口，业务恢复最坏≈300 s，远大于 50 ms",
        size=7.8, color=INK)

    footer(ax, "注：协议倒换时间取自标准与厂商公开口径、未独立复现；业务恢复=协议倒换+MAC/ARP 表刷新+摄像机注册等。")
    fig.savefig(os.path.join(OUT, "ring-recovery.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：N+1 冗余电源带载核算（左）+ PoE 功率预算/线损（右）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  冗余电源带载 + PoE 功率预算",
          "冗余是「每路都能带全载」不是「两路加起来够」；PoE 100 m 大功率要算压降余量")

    # --- 左侧：N+1 冗余电源带载核算 ---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① N+1 冗余电源带载核算（算例 7）", size=10.2,
        weight="bold", color=C5)
    # 负载构成三段
    loads = [
        ("8 口 PoE 端口负载", "8 × 30 W = 240 W", C2, 5.62),
        ("交换机自身功耗", "20 W", C3, 4.62),
        ("总需求 P_total", "240 + 20 = 260 W", C5, 3.62),
    ]
    for name, val, c, yy in loads:
        box(ax, lx, yy, lw, 0.86, "#FFFFFF", c, lw=1.5)
        txt(ax, lx + 0.2, yy + 0.43, name, size=9.4, weight="bold", color=c, ha="left")
        txt(ax, lx + lw - 0.2, yy + 0.43, val, size=9.4, weight="bold", color=INK, ha="right")
    # 两路电源对比框
    box(ax, lx, 2.42, lw, 0.92, "#FFF1EE", C4, lw=1.6)
    txt(ax, lx + lw / 2, 3.04,
        "错误：两路 150 W —— 断开一路只剩 150 W < 260 W",
        size=8.4, color=C4, weight="bold")
    txt(ax, lx + lw / 2, 2.66,
        "正确：每路 ≥260 W（如 480 W），断一路仍带全载",
        size=8.2, color=INK)
    box(ax, lx, 1.42, lw, 0.80, "#F5F3FF", C5, lw=1.6)
    txt(ax, lx + lw / 2, 1.98,
        "24 V 输入电流 I = 260/24 ≈ 10.8 A，配线/空开按 ≥15 A",
        size=8.2, color=C5, weight="bold")

    # --- 右侧：PoE 端口功率预算 + 100 m 线损（嵌入式柱状图）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② PoE 功率等级（W）+ 100 m 压降（算例 8）", size=10.2,
        weight="bold", color=C2)
    a = fig.add_axes([rx / W, 3.05 / H, rw / W, 3.05 / H])
    a.set_facecolor("#FFFFFF")
    labels = ["802.3af\n15.4 W", "802.3at\n30 W", "802.3bt\n90 W"]
    vals = [15.4, 30.0, 90.0]
    x = np.arange(3)
    bars = a.bar(x, vals, 0.52, color=[C2, C1, C5], zorder=3)
    for bar in bars:
        a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
               f"{bar.get_height():.1f}", ha="center", va="bottom",
               fontsize=9.5, color=INK, weight="bold", zorder=5)
    a.set_ylim(0, 108)
    a.set_xticks(x)
    a.set_xticklabels(labels, fontsize=8.4, color=INK)
    # 去掉竖排 ylabel（会越界压住左侧框），单位已写进小标题
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.0, colors=MUTED)
    box(ax, rx, 1.42, rw, 1.15, "#FFF7ED", C3, lw=1.6)
    txt(ax, rx + rw / 2, 2.22,
        "100 m Cat5e：I≈30/48≈0.625 A，环路电阻≈12 Ω",
        size=8.2, color=C3, weight="bold")
    txt(ax, rx + rw / 2, 1.86,
        "压降 ΔU=IR≈7.5 V，受电端约 42.5 V，逼近 44 V 下限",
        size=7.9, color=INK)

    footer(ax, "注：PoE 功率为 IEEE 802.3 标准上限；线损为演示估算，随线径/温度/线材变化，须按最热工况留余量。")
    fig.savefig(os.path.join(OUT, "power-budget.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用骨架（左链 + 右六场景两列三行）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类场景共用一套骨架：现场接入 → 汇聚隔离 → 核心网管",
          "产线 / 变电站 / 轨交 / 视频监控 / 隧道管廊 / 园区楼宇，差异只在规模、实时性、环境等级与供电")

    # 左侧：共用骨架主轴（五个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.35, 3.15, 3.65
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.45, "共用骨架", size=11.2, weight="bold", color=C1)
    chain = ["现场设备接入", "VLAN 分类 / QoS", "环网冗余自愈", "汇聚跨环隔离", "核心网管 + 告警"]
    step, subh = 0.56, 0.42
    top_c = oy + oh - 1.15
    for i, s in enumerate(chain):
        yc = top_c - i * step
        box(ax, ox + 0.25, yc - subh / 2, ow - 0.5, subh, "#FFFFFF", C1, lw=1.0)
        txt(ax, ox + ow / 2, yc, s, size=8.5, color=INK)
        if i < len(chain) - 1:
            arrow(ax, ox + ow / 2, yc - subh / 2 - 0.01,
                  ox + ow / 2, yc - step + subh / 2 + 0.01, color=C1, lw=1.0)

    # 右侧六个场景框（两列三行）
    scenes = [
        ("智能制造产线", "ERPS 毫秒自愈，控制优先", C2, "#ECFDF5"),
        ("变电站 / 电力", "PRP 零切换 + 硬件 PTP", C4, "#FFF1EE"),
        ("城市轨道交通", "EN 50155 宽温，断纤自愈", C3, "#FFF7ED"),
        ("视频监控", "Snooping 省 90% 组播", C1, "#EFF6FF"),
        ("隧道 / 管廊", "光纤远距 + PoE 供电", C5, "#F5F3FF"),
        ("园区 / 楼宇", "VLAN 隔离，接入可控", C2, "#ECFDF5"),
    ]
    sx0, sw, sh = 4.15, 4.15, 1.35
    gx, gy = 0.35, 0.22
    for i, (name, desc, c, fill) in enumerate(scenes):
        col = i % 2
        row = i // 2
        x = sx0 + col * (sw + gx)
        y = 5.95 - row * (sh + gy)
        box(ax, x, y, sw, sh, fill, c, lw=1.6)
        txt(ax, x + 0.25, y + sh - 0.36, name, size=10.0, weight="bold", color=c, ha="left")
        txt(ax, x + 0.25, y + 0.34, desc, size=8.3, color=INK, ha="left")

    footer(ax, "注：六类场景底层都是同一套「接入—分类—冗余—隔离—网管」骨架，差异只在节点规模、实时性、环境等级与供电方式。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
