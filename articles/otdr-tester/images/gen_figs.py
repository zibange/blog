# -*- coding: utf-8 -*-
"""光时域反射仪（OTDR）产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system         OTDR 内部四块：发射/收发接收/采样处理/人机接口（1.4）
  图2 backscatter-curve   背向散射曲线：斜率/台阶/尖峰/下凹/噪声底（2.2 算例 4~8）
  图3 tradeoff-pulse      脉宽—盲区—动态范围三角权衡（3.4）
  图4 scene-topology      四类落地场景共用「曲线→事件表→报告」输出链（六）

配色、坐标系用法沿用成熟模板：
  - newfig() 用整幅画布当一个 axes（0~W, 0~H），画图区与说明条分离
  - footer() 单独开一个 add_axes（图幅比例），不混用 tight 裁剪
  - 全局字体 Microsoft YaHei，避免中文/全角符号变空白
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# 全局字体：不设的话内置坐标轴（刻度/图例/标题）会用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- light 主题配色（浅底深字）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（发射）
C2 = "#0E9F6E"   # 绿（接收）
C3 = "#E8833A"   # 橙（采样处理）
C4 = "#C2410C"   # 深橙（事件/临界）
C5 = "#7C3AED"   # 紫（人机/总线）
CGREY = "#CBD2D9"


def newfig():
    """整幅画布当成一个坐标轴，数据坐标 0~W / 0~H，便于精确定位框线。"""
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


def txt(ax, x, y, s, size=9.4, color=INK, weight="normal",
        ha="center", va="center", zorder=6):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily="Microsoft YaHei")


def title(ax, t, sub=None):
    txt(ax, W / 2, H - 0.52, t, size=14.2, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.00, sub, size=8.8, color=MUTED, ha="center")


def footer(ax, s):
    """说明条单独开 axes，避免与绘图区坐标系混用导致错位。"""
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
# 图 1：OTDR 内部四块架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  OTDR 内部架构：发射 + 收发接收 + 采样处理 + 人机接口",
          "窄脉冲注入光纤，回波经环形器进 APD，ADC 采样平均后成 dB 曲线与事件表，导出 SOR 报告")

    # 四块横向排布：起点 0.45，块宽 2.75，间隙 0.55
    blocks = [
        ("发射单元", C1, "#EFF6FF", ["脉冲激光器", "1310/1550 nm", "脉冲调制(ns~µs)", "脉宽可调"]),
        ("收发与接收", C2, "#ECFDF5", ["环形器/耦合器", "发射回波分离", "APD 雪崩光电", "跨阻放大"]),
        ("采样与处理", C3, "#FFF7ED", ["高速 ADC 采样", "多次平均降噪", "对数转 dB", "事件搜索计算"]),
        ("人机与接口", C5, "#F5F3FF", ["曲线与事件表", "触摸屏操作", "SOR 轨迹文件", "USB/网口导出"]),
    ]
    bx, bw, gap = 0.45, 2.75, 0.55
    by, bh = 2.35, 4.55
    for i, (name, c, fill, items) in enumerate(blocks):
        x = bx + i * (bw + gap)
        box(ax, x, by, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, by + bh - 0.5, name, size=11.4, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = by + bh - 1.45 - j * 0.72
            box(ax, x + 0.28, yy, bw - 0.56, 0.55, "#FFFFFF", c, lw=1.2)
            txt(ax, x + bw / 2, yy + 0.275, it, size=8.8, color=INK)

    # 主箭头：发射→收发→采样→人机（水平，位于块间隙，不穿框）
    ay = by + 1.15
    for i in range(3):
        x1 = bx + i * (bw + gap) + bw
        x2 = bx + (i + 1) * (bw + gap)
        arrow(ax, x1, ay, x2, ay, color=MUTED, lw=1.6)

    # 底部：被测光纤长条 + 单端收发（回波沿原路返回）
    fx, fy, fw, fh = 0.9, 1.35, 11.4, 0.68
    box(ax, fx, fy, fw, fh, "#F6F8FA", CGREY, lw=1.1)
    txt(ax, fx + fw / 2, fy + fh / 2,
        "被测光纤：沿全长连续产生瑞利背向散射，事件处叠加菲涅尔反射（单端收发）",
        size=8.8, color=MUTED)
    # 收发块 ↔ 光纤：下行实线（注入）/ 上行虚线（回波），画「与」不画特殊箭头符
    rxc = bx + 1.0 * (bw + gap) + bw / 2
    arrow(ax, rxc, by, rxc, fy + fh, color=C1, lw=1.4)
    arrow(ax, rxc + 0.45, fy + fh, rxc + 0.45, by, color=C2, lw=1.3, ls="--")

    footer(ax, "注：发射窄脉冲、环形器分离回波、APD 接收后由 ADC 平均成 dB 曲线与事件表。脉宽、平均、折射率是影响测量的三个关键设置。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：背向散射曲线（衰减/台阶/尖峰/下凹/噪声底）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  背向散射曲线：从一条功率—距离曲线读出全部事件",
          "斜率=衰减系数；下降台阶=熔接损耗；上冲尖峰=菲涅尔反射；下凹无尖峰=宏弯；曲线没入底部即动态范围边界")

    # 插图坐标轴（有刻度/图例）：占画面主体
    px, py, pw, ph = 0.85, 1.75, 11.5, 5.35
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")

    np.random.seed(7)
    z = np.linspace(0, 50, 3000)                 # 距离 km
    p = -0.20 * z                                # 基础衰减斜率 0.20 dB/km

    # 造事件：用半高宽很窄的高斯/阶跃叠加，模拟真实曲线特征
    # 1) 近端连接器：z≈1 km 处一个尖峰（后续盲区内）
    p += 3.5 * np.exp(-((z - 1.0) / 0.12) ** 2)
    # 2) 熔接台阶：z=12 km 处下降 0.4 dB（之后整体下移）
    p += -0.4 * (z >= 12.0)
    # 3) 菲涅尔反射尖峰 + 台阶：z=25 km
    p += 4.2 * np.exp(-((z - 25.0) / 0.10) ** 2)
    p += -0.5 * (z >= 25.0)
    # 4) 宏弯：z=35 km 局部下凹 1.5 dB（高斯形，之后恢复）
    p += -1.5 * np.exp(-((z - 35.0) / 0.45) ** 2)
    # 5) 末端断点：z=45 km 大反射峰后骤降到噪声底
    p += 2.5 * np.exp(-((z - 45.0) / 0.15) ** 2)
    p -= 8.0 * (z >= 45.1)

    # 噪声底：一条浅色带，曲线没入其中即测不到
    noise_floor = -18.0
    a.axhspan(noise_floor - 2, noise_floor, color="#F0F2F5", zorder=1)
    a.axhline(noise_floor, color=CGREY, ls="--", lw=1.0, zorder=2)
    a.text(0.5, noise_floor + 0.35, "噪声底（动态范围边界）", fontsize=7.6,
           color=MUTED, ha="left", zorder=5)

    # 叠加随机噪声后画线
    p = p + np.random.normal(0, 0.06, size=z.size)
    a.plot(z, p, color=C1, lw=1.7, zorder=4)

    # 事件标注（带箭头 + 白描边，避免压线看不清）
    def mark(zx, pyv, label, color, dx, dy):
        a.annotate(label, xy=(zx, pyv), xytext=(zx + dx, pyv + dy),
                   fontsize=8.0, color=color, weight="bold",
                   bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, alpha=0.9),
                   arrowprops=dict(arrowstyle="->", color=color, lw=1.1), zorder=8)

    mark(12.3, -2.4 - 0.4, "熔接台阶 0.4 dB", C4, -6.5, -3.2)
    mark(25.0, -5.0 - 0.4, "菲涅尔反射尖峰", C3, -6.0, 2.2)
    mark(35.0, -7.0, "宏弯下凹 1.5 dB", C5, -5.0, -2.6)
    mark(45.0, -9.0, "断点", C4, -3.0, 2.0)
    # 斜率标注（在 5~10 km 的干净段）
    a.annotate("斜率 = 0.20 dB/km", xy=(7.5, -1.5), xytext=(3.5, -0.6),
               fontsize=8.2, color=C2, weight="bold",
               arrowprops=dict(arrowstyle="->", color=C2, lw=1.1), zorder=8)

    a.set_xlim(0, 50)
    a.set_ylim(-21, 5)
    a.set_xlabel("距离 (km)", fontsize=9.2, color=INK)
    a.set_ylabel("背向散射电平 (dB, 相对值)", fontsize=9.0, color=INK)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.2, colors=MUTED)

    footer(ax, "注：纵轴 dB 已按单程损耗标定，两点差除以距离即得衰减系数；台阶=熔接损耗，尖峰=连接器反射，下凹=宏弯，骤降=断点。双波长对比可确认宏弯。")
    fig.savefig(os.path.join(OUT, "backscatter-curve.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：脉宽—盲区—动态范围三角权衡
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  脉宽—盲区—动态范围：OTDR 选型的核心矛盾",
          "脉宽越大动态范围越高（测得远），但盲区同步变大（近处分不清）；平均次数是换动态范围的第二杠杆")

    # 左轴插图：动态范围随脉宽对数上升
    px, py, pw, ph = 1.1, 1.8, 10.6, 5.25
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")

    w_ns = np.logspace(np.log10(3), np.log10(20000), 200)   # 脉宽 3ns~20us
    n_g, c = 1.4682, 3e8
    blind_m = c * (w_ns * 1e-9) / (2 * n_g)                  # 事件盲区 (m)
    # 动态范围：经验拟合 3ns 约 22 dB，20us 约 45 dB（对数关系）
    dyn = 22 + (45 - 22) * (np.log10(w_ns / 3.0) / np.log10(20000.0 / 3.0))

    l1, = a.plot(w_ns, dyn, color=C1, lw=2.2, label="动态范围 (dB) — 左轴")
    a.set_xscale("log")
    a.set_xlabel("脉冲宽度 (ns，对数轴)", fontsize=9.2, color=INK)
    a.set_ylabel("动态范围 (dB)", fontsize=9.2, color=C1)
    a.tick_params(axis="y", labelcolor=C1, labelsize=8.2)
    a.set_xlim(3, 20000)
    a.set_ylim(15, 50)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)

    # 右轴：盲区随脉宽线性（对数图上呈上升曲线）
    b = a.twinx()
    l2, = b.plot(w_ns, blind_m, color=C4, lw=2.2, ls="--", label="事件盲区 (m) — 右轴")
    b.set_ylabel("事件盲区 (m)", fontsize=9.2, color=C4)
    b.tick_params(axis="y", labelcolor=C4, labelsize=8.2)
    b.set_ylim(0, 2100)

    # 工程常用窗口阴影（约 10ns~1us）
    a.axvspan(10, 1000, color="#ECFDF5", alpha=0.55, zorder=0)
    a.text(100, 47.5, "接入网/密集事件窗口", fontsize=8.0, color=C2,
           ha="center", weight="bold")
    a.text(5000, 47.5, "干线找断点窗口", fontsize=8.0, color=C4,
           ha="center", weight="bold")

    # 图例两行两列，避免互相堆叠裁切
    a.legend([l1, l2], ["动态范围 (dB, 左轴)", "事件盲区 (m, 右轴)"],
             loc="center right", fontsize=8.0, framealpha=0.92)

    footer(ax, "注：盲区随脉宽线性增大，动态范围随 log(脉宽) 提升，二者同步上升、无法同时最优。先长脉宽找断点，再短脉宽复核事件；平均次数可额外换取动态范围。")
    fig.savefig(os.path.join(OUT, "tradeoff-pulse.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：四类场景拓扑，共用「曲线→事件表→报告」输出链
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  四类落地场景：同一条曲线—事件表—报告输出链",
          "施工验收、断纤抢修、入户装维、干线在线监测，都用同一套背向散射曲线分析流程")

    # 左侧：OTDR 主机
    ox, oy, ow, oh = 0.5, 3.5, 2.6, 1.9
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.55, "OTDR 主机", size=11.2, weight="bold", color=C1)
    txt(ax, ox + ow / 2, oy + 0.75, "注入脉冲 / 接收回波", size=8.8, color=INK)
    txt(ax, ox + ow / 2, oy + 0.35, "测曲线 · 算事件", size=8.8, color=INK)

    # 右侧四个场景框（竖排）
    scenes = [
        ("施工验收", "双波长逐芯核对 · 熔接 ≤0.05 dB", C2, "#ECFDF5", 5.75),
        ("断纤抢修", "单端测距定位 · 折射率按标称设置", C4, "#FFF7ED", 4.45),
        ("入户装维", "短脉宽查近端 · 双波长识别宏弯", C5, "#F5F3FF", 3.15),
        ("在线监测", "模块+光开关周期扫描 · 越限告警", C3, "#FFF7ED", 1.85),
    ]
    sx, sw, sh = 6.4, 6.3, 1.05
    for name, desc, c, fill, sy in scenes:
        box(ax, sx, sy, sw, sh, fill, c, lw=1.7)
        txt(ax, sx + 0.25, sy + sh - 0.32, name, size=10.0, weight="bold", color=c, ha="left")
        txt(ax, sx + 0.25, sy + 0.33, desc, size=8.6, color=INK, ha="left")
        # OTDR → 场景框：从主机右侧水平引出到右框左侧（分四路，线走空白通道）
        arrow(ax, ox + ow, oy + oh / 2, sx, sy + sh / 2, color=CGREY, lw=1.2)

    # 底部：输出链路说明条
    bx, by, bw, bh = 0.5, 0.72, 12.2, 0.82
    box(ax, bx, by, bw, bh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, bx + bw / 2, by + bh / 2,
        "统一输出链：背向散射曲线  →  事件表(位置/损耗/反射)  →  衰减对账  →  SOR 轨迹 + 中文报告",
        size=9.0, color=INK)

    footer(ax, "注：四类场景的差异只在「测什么、怎么设参数」，底层都是同一套曲线分析——斜率定衰减、台阶定熔接损耗、尖峰定连接器、下凹定宏弯、骤降定断点。复用同一分析链使 OTDR 从施工到运维贯穿光缆全生命周期。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
