# -*- coding: utf-8 -*-
"""BACnet 楼宇控制器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system    三级网络 + 四类角色 + 统一对象模型（1.4）
  图2 priority-cov   16 级优先级数组仲裁（左）+ COV vs 轮询流量（右）（算例 6/8）
  图3 mstp-bibb      MS/TP 令牌环一轮时间分解（左）+ BIBB/PICS 覆盖率（右）（算例 3/14）
  图4 scene-topology 六类场景共用骨架（五）

配色、坐标系用法沿用成熟模板（见 content-factory §7.3）：
  - newfig() 把整幅画布当成一个 axes（数据坐标 0~W, 0~H）；
  - footer() 单独开一个 add_axes（用图幅比例），不与绘图区混用 tight 裁剪；
  - 全局字体 Microsoft YaHei；戒用 ↔/✓/≪ 等无字形字符（用文字代替）。

Python 教学要点：
  - os.path.dirname(os.path.abspath(__file__))：脚本所在目录，图片输出到本目录；
  - matplotlib.use("Agg")：无界面后端，自动化环境只出 PNG；
  - FancyBboxPatch / FancyArrowPatch：画圆角框与箭头；
  - add_axes([left,bottom,width,height])：图幅比例定位嵌入式小图（柱状图）。
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
C1 = "#1F6FEB"   # 主蓝（IP 管理层 / COV）
C2 = "#0E9F6E"   # 绿（路由集成 / 对象模型）
C3 = "#E8833A"   # 橙（MS/TP 现场 / 令牌）
C4 = "#C2410C"   # 深橙（优先级 / 告警）
C5 = "#7C3AED"   # 紫（BIBB / 安全）
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
# 图 1：三级网络 + 四类角色 + 统一对象模型
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  BACnet 三级网络 + 统一对象模型",
          "所有设备抽象成「对象 + 属性」；异构设备经网关映射入网，跨子网靠 BBMD 转发广播")

    # 三层横向网络带（自上而下：管理 / 集成 / 现场）
    layers = [
        ("管理层 · BACnet/IP", C1, "#EFF6FF", 6.05,
         ["中央工作站 B-OWS", "BMS 服务器 / 时序库", "UDP 47808 广播发现"]),
        ("集成层 · 路由与网关", C2, "#ECFDF5", 4.55,
         ["BACnet 路由器（IP 转 MS/TP）", "协议网关（Modbus/LonWorks）", "BBMD 跨子网转发"]),
        ("现场层 · BACnet MS/TP", C3, "#FFF7ED", 3.05,
         ["DDC 控制器 B-AAC/B-ASC", "RS-485 令牌总线 38400", "传感器 / 执行器"]),
    ]
    bx, bw = 0.6, 8.0
    for name, c, fill, yy, items in layers:
        box(ax, bx, yy, bw, 1.25, fill, c, lw=1.9)
        txt(ax, bx + 0.22, yy + 1.25 - 0.32, name, size=10.4, weight="bold", color=c, ha="left")
        for j, it in enumerate(items):
            txt(ax, bx + 0.22 + j * 2.62, yy + 0.38, it, size=7.9, color=INK, ha="left")
    # 层间箭头
    arrow(ax, bx + bw / 2, 6.05, bx + bw / 2, 5.80, color=C1, lw=1.7)
    arrow(ax, bx + bw / 2, 4.55, bx + bw / 2, 4.30, color=C2, lw=1.7)

    # 右侧统一对象模型竖块
    ox, oy, ow, oh = 9.05, 3.05, 3.55, 4.25
    box(ax, ox, oy, ow, oh, "#F5F3FF", C5, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.42, "统一对象模型", size=11.0, weight="bold", color=C5)
    objs = ["AI 模拟输入", "AO 模拟输出", "AV 模拟值", "BI/BO/BV 开关量",
            "MV 多态值", "Schedule 时间表", "Trend Log 趋势", "Notification 报警"]
    for i, o in enumerate(objs):
        yy = oy + oh - 1.02 - i * 0.40
        txt(ax, ox + 0.25, yy, o, size=8.6, color=INK, ha="left")
    arrow(ax, bx + bw, 5.2, ox, 5.2, color=C5, lw=1.5, ls="--")

    # 底部属性行
    axb = 0.6
    box(ax, axb, 1.75, 12.0, 0.92, "#F6F8FA", CGREY, lw=1.2)
    txt(ax, axb + 6.0, 2.42,
        "每个对象带属性：Present_Value（当前值）· Units（工程单位）· Status_Flags（状态）· Priority_Array（优先级）",
        size=8.6, color=INK, weight="bold")
    txt(ax, axb + 6.0, 2.02,
        "语义自描述是 BACnet 与 Modbus 裸寄存器的根本差别——拿到的是「送风温度 23.5 ℃」而非「40001=235」",
        size=8.0, color=MUTED)

    footer(ax, "注：依据 ASHRAE 135 / ISO 16484-5:2012 / GB/T 28847.5-2021；B-BC/B-AAC/B-ASC 为设备对象类型（PICS 声明）。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：优先级数组仲裁（左）+ COV vs 轮询流量（右）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  优先级仲裁 + COV 流量优化：两个核心机制",
          "最低非空槽位生效、写 NULL 释放回落；订阅把常态流量砍掉约 98%")

    # --- 左侧：16 级优先级数组（截取关键 5 级 + 生效结论）---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 优先级数组（16 级，1 最高）", size=10.2,
        weight="bold", color=C4)
    slots = [
        ("1  生命安全", "NULL", CGREY, 5.62),
        ("8  手动操作", "1  开", C4, 4.62),
        ("12 需求响应", "0  关", C3, 3.62),
        ("16 时间表", "1  开", C1, 2.62),
    ]
    for name, val, c, yy in slots:
        box(ax, lx, yy, lw, 0.86, "#FFFFFF", c, lw=1.5)
        txt(ax, lx + 0.2, yy + 0.43, name, size=9.6, weight="bold", color=c, ha="left")
        txt(ax, lx + lw - 0.2, yy + 0.43, val, size=9.6, weight="bold", color=INK, ha="right")
    box(ax, lx, 1.42, lw, 0.92, "#FFF1EE", C4, lw=1.7)
    txt(ax, lx + lw / 2, 2.06,
        "生效值 = 最低非空槽位 = 8 级「开」", size=8.8, color=C4, weight="bold")
    txt(ax, lx + lw / 2, 1.68,
        "释放 8 级后回落 12 级「关」——排障先读 Priority_Array",
        size=8.0, color=INK)

    # --- 右侧：COV vs 轮询流量（嵌入式柱状图）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② COV vs 轮询（纵轴 kB/s 对数，1000 点）", size=10.2,
        weight="bold", color=C1)
    # 修复：axes 底部抬到 2.95 给 x 轴标签腾位，高度缩到 3.15，避免压住结论条
    a = fig.add_axes([rx / W, 2.95 / H, rw / W, 3.15 / H])
    a.set_facecolor("#FFFFFF")
    labels = ["定时轮询\n1 s", "COV 订阅\n60 s"]
    vals = [100.0, 1.67]
    x = np.arange(2)
    bars = a.bar(x, vals, 0.5, color=[C4, C2], zorder=3)
    for bar in bars:
        a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
               f"{bar.get_height():.1f}", ha="center", va="bottom",
               fontsize=10, color=INK, weight="bold", zorder=5)
    a.set_yscale("log")
    a.set_ylim(0.5, 300)
    a.set_xticks(x)
    a.set_xticklabels(labels, fontsize=8.8, color=INK)
    # 去掉竖排 ylabel（会挤进左栏），单位已写进标题
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.2, colors=MUTED)
    box(ax, rx, 1.42, rw, 0.92, "#ECFDF5", C2, lw=1.7)
    txt(ax, rx + rw / 2, 2.06,
        "节约率 = 1 - f_cov/f_poll ≈ 98%", size=8.8, color=C2, weight="bold")
    txt(ax, rx + rw / 2, 1.68,
        "但订阅要 lifetime 续订（算例 7），阈值太小约等于轮询",
        size=8.0, color=INK)

    footer(ax, "注：算例 6 η=1-f_cov/f_poll；算例 8 生效值=min{非空优先级槽位}；MS/TP 慢总线上 COV 是「能否跑起来」的关键。")
    fig.savefig(os.path.join(OUT, "priority-cov.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：MS/TP 令牌环时间分解（左）+ BIBB/PICS 覆盖率（右）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  令牌环实时性 + 互操作覆盖率：两个木桶效应",
          "一轮 32 站约 0.66 s 决定现场段实时性下限；BIBB 取交集决定能否对接")

    # --- 左侧：令牌环一轮时间分解 ---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① MS/TP 一轮时间 T = N(t_turn + t_frame)", size=10.2,
        weight="bold", color=C3)
    stages = [
        ("turnaround", "38400 bps ≈ 15 字符", "4 ms", C1, 5.60),
        ("单帧传输", "64 B × 10 / 38400", "16.7 ms", C2, 4.52),
        ("单站合计", "4 + 16.7", "20.7 ms", C3, 3.44),
        ("32 站一轮", "32 × 20.7", "662 ms", C4, 2.36),
    ]
    sh = 0.88
    for name, desc, val, c, yy in stages:
        box(ax, lx, yy, lw, sh, "#F6F8FA", c, lw=1.5)
        txt(ax, lx + 0.18, yy + sh / 2, name, size=9.4, weight="bold", color=c, ha="left")
        txt(ax, lx + 1.75, yy + sh / 2, desc, size=8.4, color=INK, ha="left")
        txt(ax, lx + lw - 0.15, yy + sh / 2, val, size=9.4, weight="bold", color=c, ha="right")
    box(ax, lx, 1.15, lw, 0.92, "#FFF7ED", C3, lw=1.6)
    txt(ax, lx + lw / 2, 1.79,
        "告警到上位机最坏等约一轮 0.66 s", size=8.8, color=C3, weight="bold")
    txt(ax, lx + lw / 2, 1.41,
        "要更快：减节点 / 提波特率 / 用 COV 主动推", size=8.0, color=INK)

    # --- 右侧：BIBB/PICS 覆盖率（嵌入式横向条 + 木桶结论）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② BIBB 覆盖率（绿=已覆盖 / 橙=缺口）", size=10.2,
        weight="bold", color=C5)
    a = fig.add_axes([rx / W, 2.95 / H, rw / W, 3.15 / H])
    a.set_facecolor("#FFFFFF")
    vendors = ["厂商 A\n11/15", "厂商 B\n15/15"]
    # 修复：把 y 轴标签从「厂商 A (11/15)」缩短，给左侧多让位，避免越界到左栏；
    # 图例去掉（移入标题「绿=已覆盖/橙=缺口」），避免压住 y 轴标签与缺口数值。
    covered = [11, 15]
    missing = [4, 0]
    y = np.arange(2)
    a.barh(y, covered, 0.5, color=C2, zorder=3)
    a.barh(y, missing, 0.5, left=covered, color=C4, zorder=3)
    for i in range(2):
        a.text(covered[i] / 2, y[i], f"{covered[i]}", ha="center", va="center",
               fontsize=9, color="#FFFFFF", weight="bold", zorder=5)
        if missing[i]:
            a.text(covered[i] + missing[i] / 2, y[i], f"{missing[i]}", ha="center",
                   va="center", fontsize=9, color="#FFFFFF", weight="bold", zorder=5)
    a.set_yticks(y)
    a.set_yticklabels(vendors, fontsize=8.4, color=INK)
    a.set_xlim(0, 16)
    a.set_xlabel("招标要求的 BIBB 项数", fontsize=8.0, color=MUTED)
    a.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.2, colors=MUTED)
    box(ax, rx, 1.15, rw, 0.92, "#F5F3FF", C5, lw=1.6)
    txt(ax, rx + rw / 2, 1.79,
        "系统能力 = 各方 BIBB 交集；缺 DS-COV-B 则该对设备无法订阅",
        size=8.4, color=C5, weight="bold")
    txt(ax, rx + rw / 2, 1.41,
        "「支持 BACnet」不等于「能对接」——PICS 逐项核对 + BTL 认证",
        size=8.0, color=INK)

    footer(ax, "注：算例 3 T=N(t_turn+t_frame)，32 站@38400≈0.66s；算例 14 覆盖率=11/15=73%，互操作取交集。")
    fig.savefig(os.path.join(OUT, "mstp-bibb.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用骨架（左链 + 右六场景两列三行）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类场景共用一套骨架：设备 → 对象建模 → 承载 → BMS 集成",
          "商业办公 / 医院 / 数据中心 / 酒店院校 / 机场轨交 / 工业园区，差异只在规模、实时性与安全等级")

    # 左侧：共用骨架主轴（五个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.35, 3.15, 3.65
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.45, "共用骨架", size=11.2, weight="bold", color=C1)
    chain = ["现场设备接入", "抽象成标准对象", "IP/MS-TP 承载", "BMS 统一集成", "COV + 报警 + 趋势"]
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
        ("商业办公楼", "COV 降流量，统一节能", C2, "#ECFDF5"),
        ("医院", "报警死区，优先级保障", C4, "#FFF1EE"),
        ("数据中心", "趋势上传，7×24 稳定", C1, "#EFF6FF"),
        ("酒店与院校", "MS/TP 省线，多末端", C3, "#FFF7ED"),
        ("机场与轨交", "BBMD 分区，安全审计", C5, "#F5F3FF"),
        ("工业园区", "网关映射，异构利旧", C2, "#ECFDF5"),
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
        txt(ax, x + 0.25, y + 0.34, desc, size=8.5, color=INK, ha="left")

    footer(ax, "注：六类场景底层都是同一套「设备—对象—承载—集成」骨架，差异只在点数规模、实时性、协议边界与安全等级。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
