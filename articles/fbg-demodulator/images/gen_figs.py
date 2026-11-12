# -*- coding: utf-8 -*-
"""光纤光栅解调仪产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system          解调仪内部架构：光路前端 + 波长测量引擎 + 数据换算输出  （1.4）
  图2 demod-principle      布拉格波长随应变/温度漂移(双线) + 单纤波长分复用(WDM)示意  （2.2 算例1/2/4）
  图3 multiplex-switch     16 通道 x 每纤复用拓扑 + 光开关轮询时序(有效采样率)         （2.2 算例5/11）
  图4 scene-platform       光栅阵→解调仪→监测平台→告警联动 场景拓扑 + 时延预算        （2.2 算例12/六 场景）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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
C1 = "#1F6FEB"   # 主蓝（光路前端）
C2 = "#0E9F6E"   # 绿（波长测量引擎）
C3 = "#E8833A"   # 橙（数据换算与联动）
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
    ax2.text(0.5, 0.5, s, fontsize=7.4, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：解调仪内部架构（三层功能面板）
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  光纤光栅解调仪内部架构：光路前端 + 波长测量引擎 + 数据换算输出",
          "宽带光经耦合器与光开关进入光栅阵，反射光谱由测量引擎解析波长，峰值检测后换算为温度/应变并上传平台")

    # 左：光路前端
    lx, ly, lw, lh = 0.7, 2.3, 3.3, 4.6
    box(ax, lx, ly, lw, lh, "#EFF6FF", C1, lw=2.0)
    txt(ax, lx + lw / 2, ly + lh - 0.5, "光路前端", size=12.0, weight="bold", color=C1)
    items = ["宽带光源 (ASE/SLED)", "耦合器 / 环形器", "1xN 光开关", "参考光栅(源漂移补偿)"]
    for i, it in enumerate(items):
        yy = ly + lh - 1.55 - i * 0.62
        box(ax, lx + 0.35, yy, lw - 0.7, 0.5, "#FFFFFF", C1, lw=1.2)
        txt(ax, lx + lw / 2, yy + 0.25, it, size=8.8, color=INK)

    # 中：波长测量引擎
    mx, my, mw, mh = 4.4, 2.3, 3.6, 4.6
    box(ax, mx, my, mw, mh, "#ECFDF5", C2, lw=2.2)
    txt(ax, mx + mw / 2, my + mh - 0.5, "波长测量引擎", size=12.0, weight="bold", color=C2)
    inner = [
        ("可调 FP 滤波 / 光谱阵列", 5.55),
        ("光电转换 + AD 采样", 4.7),
        ("峰值检测(高斯/质心拟合)", 3.85),
        ("波长-物理量换算", 3.0),
    ]
    for name, cy in inner:
        box(ax, mx + 0.35, cy, mw - 0.7, 0.58, "#FFFFFF", C2, lw=1.3)
        txt(ax, mx + mw / 2, cy + 0.29, name, size=9.0, color=INK)
    box(ax, mx + 0.35, my + 0.1, mw - 0.7, 0.55, "#FFF7ED", C4, lw=1.3)
    txt(ax, mx + mw / 2, my + 0.375, "信号同步与触发", size=9.2, color=C4, weight="bold")

    # 右：数据换算与输出
    rx, ry, rw, rh = 8.5, 2.3, 4.0, 4.6
    box(ax, rx, ry, rw, rh, "#FFF7ED", C3, lw=2.0)
    txt(ax, rx + rw / 2, ry + rh - 0.5, "数据换算与输出", size=12.0, weight="bold", color=C3)
    links = [("温度 / 应变 / 位移", C3, 5.55), ("以太网 / Modbus", C5, 4.55),
             ("阈值告警输出", C4, 3.55), ("监测平台对接", C1, 2.55)]
    for name, c, cy in links:
        box(ax, rx + 0.35, cy, rw - 0.7, 0.62, "#FFFFFF", c, lw=1.3)
        txt(ax, rx + rw / 2, cy + 0.31, name, size=9.0, color=c)

    # 主箭头：前端→引擎→输出（与数据上行同向）
    arrow(ax, lx + lw, ly + lh - 2.2, mx, my + mh - 2.2, color=C2, lw=1.6)
    arrow(ax, mx + mw, my + mh - 2.2, rx, ry + rh - 2.2, color=C3, lw=1.6)
    # 回传虚线（状态/自检）—— 不贴文字
    arrow(ax, rx, ry + 2.0, mx + mw, my + 2.0, color=MUTED, lw=1.1, ls="--")

    footer(ax, "注：前端提供宽带光并经光开关选通光栅阵；波长测量引擎完成光谱采集与峰值定位；输出层把波长漂移换算为温度/应变并上传平台。参考光栅补偿光源波长漂移。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：布拉格波长漂移（应变/温度双线）+ 单纤 WDM 复用
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  布拉格波长随应变与温度漂移，单纤靠波长分复用串接约 40 个测点",
          "左：应变灵敏度 1.2 pm/微应变、温度灵敏度 10.4 pm/摄氏度；右：C 波段 40 nm 窗内多光栅独立编码")

    # ---- 左图：波长漂移 vs 应变，叠加温度等效 ----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    eps = np.linspace(0, 2000, 200)          # 应变 微应变
    dL_strain = 1.2 * eps / 1000.0           # nm，Kε=1.2 pm/微应变
    # 温度交叉：1 摄氏度 = 8.7 微应变当量，换算成同样纵轴的等效漂移
    dT = np.linspace(0, 50, 200)
    dL_temp = 10.4 * dT / 1000.0             # nm，KT=10.4 pm/摄氏度
    a.plot(eps, dL_strain, color=C1, lw=2.2, label="应变漂移 (Kε=1.2 pm/微应变)", zorder=4)
    a.plot(dT * 8.7, dL_temp, color=C4, lw=2.0, ls="--", label="温度当量 (1 摄氏度=8.7 微应变)", zorder=4)
    # 标注 1000 微应变
    a.axvline(1000, color=MUTED, ls=":", lw=1.2, zorder=3)
    a.annotate("1000 微应变 -> 1.2 nm", (1000, 1.2), xytext=(1000 - 760, 1.55),
               fontsize=8.4, color=C1, weight="bold",
               arrowprops=dict(arrowstyle="->", color=C1, lw=1.1))
    a.set_xlabel("应变 (微应变) / 温度当量", fontsize=9.0, color=INK)
    a.set_ylabel("布拉格波长漂移 Delta 波长 (nm)", fontsize=8.6, color=INK)
    a.set_xlim(0, 2200); a.set_ylim(0, 2.6)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.legend(loc="upper left", fontsize=7.8, framealpha=0.9)

    # ---- 右图：单纤 WDM 复用（波长窗 + 反射峰）----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    b.set_xlim(1505, 1605); b.set_ylim(0, 1.2)
    b.set_xlabel("波长 (nm)", fontsize=9.0, color=INK)
    b.set_ylabel("反射强度 (a.u.)", fontsize=9.0, color=INK)
    # 40 nm 窗口阴影
    b.axvspan(1510, 1590, color="#DCEAFE", alpha=0.5, zorder=1)
    b.text(1550, 1.08, "C 波段可用窗 40 nm", fontsize=8.2, color=C1, ha="center", weight="bold")
    # 8 个反射峰，间距 10 nm（示意 40 nm 内约 40 点）
    peaks = np.arange(1515, 1591, 10)
    for p in peaks:
        xr = np.linspace(p - 1.2, p + 1.2, 60)
        b.plot(xr, 0.9 * np.exp(-((xr - p) / 0.35) ** 2), color=C2, lw=1.6, zorder=3)
        b.axvline(p, color=C2, ls=":", lw=0.7, zorder=2)
    b.text(1550, 0.42, "每峰独立编码 -> 约 40 个测点/纤", fontsize=8.4, color=C2, ha="center",
           weight="bold", path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)
    b.set_ylim(0, 1.2)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.grid(True, color=GRID, lw=0.8, alpha=0.9)

    footer(ax, "注：左图 Kε=1.2 pm/微应变、KT=10.4 pm/摄氏度，温度对应变有交叉敏感（1 摄氏度约等于 8.7 微应变），须用同点温度光栅补偿；右图单纤靠不同中心波长串接，40 nm 窗内约 40 测点。")
    fig.savefig(os.path.join(OUT, "demod-principle.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：16 通道 x 每纤复用拓扑 + 光开关轮询时序
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  1x16 光开关把 16 纤并入一台主机，总测点约 640 个但轮询拉低有效采样率",
          "左：光开关选通 16 条光纤、每纤约 40 点；右：轮询时序——64 点一轮约 1.6 s，单点有效采样率仅 0.62 Hz")

    # ---- 左：复用拓扑 ----
    ox, oy, ow, oh = 0.7, 1.9, 5.6, 5.2
    box(ax, ox, oy, ow, oh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, ox + ow / 2, oy + oh - 0.35, "1x16 光开关 + 16 条传感光纤", size=10.0, weight="bold", color=C5)
    # 光开关方块
    box(ax, ox + 0.5, oy + 1.7, 1.4, 1.3, "#FFFFFF", C5, lw=1.6)
    txt(ax, ox + 1.2, oy + 2.35, "光开关", size=8.6, color=C5, weight="bold")
    # 16 条光纤（简化为 16 竖线 + 每纤 8 个代表测点）
    nfib = 16
    for i in range(nfib):
        fx = ox + 2.3 + i * (ow - 2.5) / (nfib - 1)
        ax.plot([fx, fx], [oy + 0.4, oy + 1.7], color=C1, lw=1.0, zorder=3)
        # 测点（每纤画 5 个代表，标注每纤约 40）
        for j in range(5):
            ax.scatter([fx], [oy + 0.55 + j * 0.26], s=14, color=C2, zorder=5)
    txt(ax, ox + ow - 1.4, oy + 0.25, "每纤约 40 点", size=8.0, color=C2, weight="bold")
    txt(ax, ox + ow / 2, oy + 0.05, "总测点 = 16 通道 x 40 = 约 640 点/台", size=8.4, color=C4, weight="bold")

    # ---- 右：轮询时序 ----
    rx, ry, rw, rh = 7.0, 1.9, 5.5, 5.2
    box(ax, rx, ry, rw, rh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, rx + rw / 2, ry + rh - 0.35, "光开关轮询时序", size=10.0, weight="bold", color=C4)
    # 时间轴
    t0 = rx + 0.5
    tw = rw - 1.0
    ty = ry + 2.3
    nslots = 8
    slot = tw / nslots
    for i in range(nslots):
        sx = t0 + i * slot
        col = C2 if i % 2 == 0 else C1
        ax.add_patch(FancyBboxPatch((sx + 0.04, ty - 0.35), slot - 0.08, 0.7,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    linewidth=1.0, edgecolor=col, facecolor=col, alpha=0.25, zorder=3))
        txt(ax, sx + slot / 2, ty + 0.0, "测点", size=7.4, color=INK)
    # 时间点刻度
    ax.plot([t0, t0 + tw], [ty - 0.6, ty - 0.6], color=MUTED, lw=1.2, zorder=3)
    for i in range(nslots + 1):
        ax.plot([t0 + i * slot, t0 + i * slot], [ty - 0.6, ty - 0.75], color=MUTED, lw=1.0, zorder=3)
    txt(ax, t0 + tw / 2, ty - 0.95, "一轮 = 64 点 x 25 ms = 1.6 s", size=8.2, color=C4, weight="bold")
    txt(ax, t0 + tw / 2, ry + 0.55, "单点有效采样率 = 1/1.6 s = 0.62 Hz（静态监测够用，动态不足）",
        size=8.2, color=INK)
    txt(ax, t0 + tw / 2, ry + 0.18, "注：动态场景需减少单次轮询点数或改并行光谱阵列", size=7.8, color=MUTED)

    footer(ax, "注：1x16 光开关把 16 条光纤并入一台主机，总测点约 640 个；但串行轮询使单点有效采样率仅约 0.62 Hz——静态监测够用，动态振动需减点数或换并行探测。")
    fig.savefig(os.path.join(OUT, "multiplex-switch.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：场景联动拓扑（光栅阵→解调仪→平台→告警）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  解调仪把各点波长实时换算为物理量并上传平台，触发阈值告警与联动",
          "光栅阵→解调仪(2 ms/通道扫描)→监测平台→阈值告警/视频联动；单帧解调时延随通道数线性增长")

    # 主链路：4 个节点
    nodes = [
        ("光栅传感阵\n(无源测点)", C1, 0.7),
        ("解调仪\n(波长解析)", C2, 3.1),
        ("监测平台\n(呈现/趋势)", C5, 5.5),
        ("阈值告警\n(视频联动)", C4, 7.9),
    ]
    nw, nh = 2.0, 1.5
    ny = 4.4
    for name, c, nx in nodes:
        box(ax, nx, ny, nw, nh, "#FFFFFF", c, lw=1.8)
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
        "单帧解调时延：16 通道 x 2 ms/通道 = 32 ms；动态模式须 <1 ms/通道，需减通道或并行探测；平台侧告警延迟取决于轮询周期",
        size=8.8, color=INK)

    # 供电分支（顶部）
    sx, sy, sw, sh = 3.1, 6.3, 2.0, 0.9
    box(ax, sx, sy, sw, sh, "#FFF7ED", C4, lw=1.3)
    txt(ax, sx + sw / 2, sy + sh / 2, "供电 DC24V / PoE", size=8.6, color=C4, weight="bold")
    arrow(ax, sx + sw / 2, sy, nodes[1][2] + nw / 2, ny + nh, color=C4, lw=1.2, ls="--")

    # 右侧参考光栅框
    rx, ry, rw, rh = 10.3, 6.3, 2.2, 0.9
    box(ax, rx, ry, rw, rh, "#ECFDF5", C2, lw=1.3)
    txt(ax, rx + rw / 2, ry + rh / 2, "参考光栅\n(源漂移补偿)", size=8.0, color=C2, weight="bold")
    arrow(ax, rx + rw / 2, ry, nodes[1][2] + nw / 2, ny + nh, color=C2, lw=1.2, ls="--")

    footer(ax, "注：解调仪逐帧解析光栅阵列波长、换算为温度/应变并上传平台；平台按阈值与变化速率告警并联动视频。单帧时延随通道数线性增长，动态应用须控制通道数或改并行探测。")
    fig.savefig(os.path.join(OUT, "scene-platform.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
