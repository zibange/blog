# -*- coding: utf-8 -*-
"""泄漏电缆入侵探测器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system          三层架构：前端传感(LCX双缆) + 主机处理 + 后端联动     （1.4）
  图2 field-attenuation    场强随距离指数衰减→探测半宽；埋深对地表场强的影响       （2.2 算例1/3）
  图3 zone-layout          周界 400m 分 4 防区 + RS-485 总线拓扑                  （2.2 算例5/13）
  图4 install-compare      埋地 vs 贴墙 两种敷设对比 + 转角/过车处理              （五/六 场景）
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
C1 = "#1F6FEB"   # 主蓝（前端传感/中心侧）
C2 = "#0E9F6E"   # 绿（主机/路由）
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
    title(ax, "图 1  泄漏电缆入侵探测器三层架构：前端传感 + 主机处理 + 后端联动",
          "双 LCX 形成电磁灵敏区，主机完成射频收发与判决，联动层触发视频预置位与平台")

    # 左：前端传感层
    lx, ly, lw, lh = 0.7, 2.3, 3.3, 4.6
    box(ax, lx, ly, lw, lh, "#EFF6FF", C1, lw=2.0)
    txt(ax, lx + lw / 2, ly + lh - 0.5, "前端传感层", size=12.0, weight="bold", color=C1)
    items = ["发射 LCX 泄漏电缆", "接收 LCX 泄漏电缆", "馈线 + 终端负载", "接地与防护"]
    for i, it in enumerate(items):
        yy = ly + lh - 1.55 - i * 0.62
        box(ax, lx + 0.35, yy, lw - 0.7, 0.5, "#FFFFFF", C1, lw=1.2)
        txt(ax, lx + lw / 2, yy + 0.25, it, size=8.8, color=INK)
    # 双缆示意（细条）：底部留白区，标签放条带上方
    ax.add_patch(FancyBboxPatch((lx + 0.5, ly + 0.55), lw - 1.0, 0.22,
                                boxstyle="round,pad=0,rounding_size=0.08",
                                linewidth=1.0, edgecolor=C1, facecolor="#DCEAFE", zorder=3))
    ax.add_patch(FancyBboxPatch((lx + 0.5, ly + 0.15), lw - 1.0, 0.22,
                                boxstyle="round,pad=0,rounding_size=0.08",
                                linewidth=1.0, edgecolor=C1, facecolor="#DCEAFE", zorder=3))
    txt(ax, lx + lw / 2, ly + 0.97, "电磁灵敏区（地表/墙面）", size=7.6, color=C1)

    # 中：主机处理层
    mx, my, mw, mh = 4.4, 2.3, 3.6, 4.6
    box(ax, mx, my, mw, mh, "#ECFDF5", C2, lw=2.2)
    txt(ax, mx + mw / 2, my + mh - 0.5, "主机处理层", size=12.0, weight="bold", color=C2)
    inner = [
        ("射频收发模块", 5.6),
        ("滤波 + 相关处理", 4.75),
        ("AGC 自动增益", 3.9),
        ("阈值 + 持续时长判决", 3.05),
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
    links = [("报警主机 / 继电器", C3, 5.55), ("视频预置位 (PTZ)", C1, 4.55),
             ("声光警号", C4, 3.55), ("安防平台", C5, 2.55)]
    for name, c, cy in links:
        box(ax, rx + 0.35, cy, rw - 0.7, 0.62, "#FFFFFF", c, lw=1.3)
        txt(ax, rx + rw / 2, cy + 0.31, name, size=9.0, color=c)

    # 主箭头：传感→主机→联动
    arrow(ax, lx + lw, ly + lh - 2.2, mx, my + mh - 2.2, color=C2, lw=1.6)
    arrow(ax, mx + mw, my + mh - 2.2, rx, ry + rh - 2.2, color=C3, lw=1.6)
    # 回传虚线（状态/自检）——不贴文字，说明放入 footer
    arrow(ax, rx, ry + 2.0, mx + mw, my + 2.0, color=MUTED, lw=1.1, ls="--")

    footer(ax, "注：前端双 LCX 收发电缆在沿线形成连续电磁灵敏区；主机完成射频收发、滤波相关、AGC 与阈值+持续时长判决；联动层把报警映射到视频预置位与平台。三层解耦便于分级运维。工程基准示意。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：场强衰减→探测半宽；埋深对地表场强
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  场强随距离指数衰减决定探测半宽，埋深越大地表场强越弱",
          "左：V_r=V0·e^(-d/λe)，d_max≈1.5 m、两缆间距 S≤3 m；右：埋深 0.1→0.5 m 地表场强剩 73%")

    # ---- 左图：场强衰减曲线 ----
    px, py, pw, ph = 0.7, 1.9, 5.8, 5.2
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    d = np.linspace(0, 4, 200)
    lam = 0.5
    V0, Vth = 1.0, 0.05
    V = V0 * np.exp(-d / lam)
    a.plot(d, V, color=C1, lw=2.2, zorder=4)
    # 阈值线
    a.axhline(Vth, color=C4, ls="--", lw=1.3, zorder=3)
    a.text(3.4, Vth + 0.02, "V_th=50 mV", fontsize=8.0, color=C4)
    # 标注 d_max
    dmax = lam * np.log(V0 / Vth)
    a.axvline(dmax, color=C2, ls=":", lw=1.3, zorder=3)
    a.annotate(f"d_max≈{dmax:.1f} m", (dmax, Vth),
               xytext=(dmax - 0.3, 0.55), fontsize=8.4, color=C2, weight="bold",
               arrowprops=dict(arrowstyle="->", color=C2, lw=1.1))
    # 两缆间距 S=2*dmax 示意
    a.annotate("", xy=(2 * dmax, 0.12), xytext=(0, 0.12),
               arrowprops=dict(arrowstyle="<->", color=C5, lw=1.4))
    a.text(dmax, 0.18, "S≈3 m (两缆间距)", fontsize=8.0, color=C5, ha="center")
    a.set_xlabel("到电缆距离 d (m)", fontsize=9.0, color=INK)
    a.set_ylabel("接收耦合电压 V_r (V)", fontsize=9.0, color=INK)
    a.set_xlim(0, 4); a.set_ylim(0, 1.1)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)

    # ---- 右图：埋深对地表场强（相对值）----
    px2, pw2 = 7.0, 5.5
    b = fig.add_axes([px2 / W, py / H, pw2 / W, ph / H])
    b.set_facecolor("#FFFFFF")
    alphas = np.array([0.4, 0.6, 0.8, 1.0, 1.2])
    depths = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    rel = np.exp(-alphas * (depths - 0.1))  # 以 0.1 m 为基准的相对场强
    bars = b.bar([f"{h:.1f} m" for h in depths], rel, color=C3, zorder=4, width=0.6)
    for bar, v in zip(bars, rel):
        b.text(bar.get_x() + bar.get_width() / 2, v + 0.02, f"{v:.2f}",
               ha="center", fontsize=8.4, color=INK, weight="bold")
    b.axhline(1.0, color=C1, ls="--", lw=1.1, zorder=3)
    b.text(3.6, 1.02, "0.1 m 基准", fontsize=8.0, color=C1)
    b.set_xlabel("埋深 h (m)", fontsize=9.0, color=INK)
    b.set_ylabel("地表相对场强 (0.1 m=1.0)", fontsize=9.0, color=INK)
    b.set_ylim(0, 1.15)
    b.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.text(1.5, 0.55, "0.1→0.5 m 剩 0.73 倍", ha="center", fontsize=8.4, color=C3,
           weight="bold", path_effects=[pe.withStroke(linewidth=3.0, foreground="white")], zorder=7)

    footer(ax, "注：左图 V_r(d)=V0·e^(-d/λe)，λe=0.5 m → d_max≈1.5 m、S_max≈3 m；右图埋深按 e^(-αh) 衰减，0.1→0.5 m 剩 73%，埋深建议 0.1–0.3 m。工程演示算例。")
    fig.savefig(os.path.join(OUT, "field-attenuation.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：周界 400m 分 4 防区 + RS-485 总线
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  周界 400 m 划分为 4 个防区，RS-485 总线轮询各防区",
          "单段 ≤80 m（射频衰减预算），4 防区独立报警输出，定位精度 100 m 级")

    # 主机（左）
    hx, hy, hw, hh = 0.7, 3.4, 1.8, 1.4
    box(ax, hx, hy, hw, hh, "#ECFDF5", C2, lw=2.2)
    txt(ax, hx + hw / 2, hy + hh - 0.42, "探测主机", size=10.5, weight="bold", color=C2)
    txt(ax, hx + hw / 2, hy + 0.5, "RS-485 总线", size=8.0, color=INK)

    # 周界带（分 4 段）：seg_w 收窄保证不越右界、不压「平台定位」框
    band_y, band_h = 3.5, 1.2
    seg_w = 1.8
    gap = 0.2
    x0 = 3.0
    zones = [("防区 1\n0–100 m", C1), ("防区 2\n100–200 m", C2),
             ("防区 3\n200–300 m", C5), ("防区 4\n300–400 m", C3)]
    for i, (name, c) in enumerate(zones):
        zx = x0 + i * (seg_w + gap)
        box(ax, zx, band_y, seg_w, band_h, "#FFFFFF", c, lw=1.8)
        # 段内画两条平行 LCX 细条（下半部），文字置顶不压条
        ax.add_patch(FancyBboxPatch((zx + 0.45, band_y + 0.18), seg_w - 0.9, 0.18,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    linewidth=0.8, edgecolor=c, facecolor="#DCEAFE", zorder=3))
        ax.add_patch(FancyBboxPatch((zx + 0.45, band_y + 0.46), seg_w - 0.9, 0.18,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    linewidth=0.8, edgecolor=c, facecolor="#DCEAFE", zorder=3))
        txt(ax, zx + seg_w / 2, band_y + band_h - 0.24, name, size=8.4, color=c, weight="bold")

    # RS-485 总线：主机下方水平总线 + 各防区垂直支线（避免长箭头横穿防区框）
    bus_y = 2.85
    bus_end = x0 + 3 * (seg_w + gap) + seg_w / 2
    ax.plot([hx + hw / 2, hx + hw / 2], [hy, bus_y], color=C5, lw=1.4, zorder=3)
    ax.plot([hx + hw / 2, bus_end], [bus_y, bus_y], color=C5, lw=1.4, zorder=3)
    for i in range(4):
        zx = x0 + i * (seg_w + gap)
        cx = zx + seg_w / 2
        arrow(ax, cx, bus_y, cx, band_y, color=C5, lw=1.2)
    # 末段 → 平台定位
    arrow(ax, x0 + 3 * (seg_w + gap) + seg_w, band_y + 0.6, 11.0, hy + 0.7,
          color=C4, lw=1.3)

    # 底部总线说明
    bx, by, bw, bh = 3.0, 1.6, 9.5, 0.9
    box(ax, bx, by, bw, bh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, bx + bw / 2, by + 0.45,
        "总线轮询：波特率 9600 时单防区约 30 ms，4 防区 t_poll≈120 ms << 报警延迟；任一防区断路/短路自检即报",
        size=8.6, color=MUTED)

    # 右侧定位说明
    rx, ry, rw, rh = 11.0, 3.4, 1.7, 1.4
    box(ax, rx, ry, rw, rh, "#FFF7ED", C4, lw=1.8)
    txt(ax, rx + rw / 2, ry + rh - 0.42, "平台定位", size=10.0, weight="bold", color=C4)
    txt(ax, rx + rw / 2, ry + 0.5, "到防区段", size=8.2, color=INK)

    footer(ax, "注：整周界 L=400 m 按单段 ≤100 m（工程取 80 m）划分为 4 防区，每段独立报警输出，定位精度达 100 m 级；RS-485 总线标准带 32 节点，4 防区余量充足。工程演示算例。")
    fig.savefig(os.path.join(OUT, "zone-layout.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：埋地 vs 贴墙 敷设对比 + 转角/过车
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  埋地式与贴墙式两种敷设对比，转角平滑过渡、过车穿管深埋",
          "埋地完全隐形但受土壤湿度影响；贴墙施工快、特性稳；两者算法一致仅标定不同")

    # 左：埋地式
    lx, ly, lw, lh = 0.7, 2.3, 5.6, 4.7
    box(ax, lx, ly, lw, lh, "#EFF6FF", C1, lw=2.0)
    txt(ax, lx + lw / 2, ly + lh - 0.5, "埋地式（完全隐形）", size=11.5, weight="bold", color=C1)
    # 地表线
    gy = ly + 2.6
    ax.plot([lx + 0.4, lx + lw - 0.4], [gy, gy], color="#78A078", lw=2, zorder=4)
    txt(ax, lx + 1.1, gy + 0.12, "地表", size=8.0, color="#507850")
    # 地下双缆
    for off in (0.5, 0.95):
        ax.add_patch(FancyBboxPatch((lx + 0.9, gy + off), lw - 1.8, 0.22,
                                    boxstyle="round,pad=0,rounding_size=0.08",
                                    linewidth=1.0, edgecolor=C1, facecolor="#DCEAFE", zorder=3))
    txt(ax, lx + lw / 2, gy + 1.25, "埋深 0.1–0.3 m 双 LCX", size=8.2, color=C1)
    # 特性标签
    notes_l = ["草坪/土路隐形", "受土壤湿度影响 (AGC)", "过车需穿管深埋"]
    for i, n in enumerate(notes_l):
        yy = ly + 0.5 + i * 0.55
        box(ax, lx + 0.5, yy, lw - 1.0, 0.45, "#FFFFFF", C1, lw=1.1)
        txt(ax, lx + lw / 2, yy + 0.23, n, size=8.6, color=INK)

    # 右：贴墙式
    rx, ry, rw, rh = 6.9, 2.3, 5.6, 4.7
    box(ax, rx, ry, rw, rh, "#ECFDF5", C2, lw=2.0)
    txt(ax, rx + rw / 2, ry + rh - 0.5, "贴墙/挂网式（利旧墙体）", size=11.5, weight="bold", color=C2)
    # 墙体（顶部压低，给标题让位）
    wx = rx + 1.2
    ax.add_patch(FancyBboxPatch((wx, ry + 0.6), 0.5, rh - 1.4,
                                boxstyle="round,pad=0,rounding_size=0.05",
                                linewidth=1.0, edgecolor="#969696", facecolor="#E2E8F0", zorder=3))
    txt(ax, wx + 0.25, ry + 0.4, "墙", size=8.0, color=MUTED)
    # 墙面平行双缆（置于上部，避开底部三行说明框）
    for off in (3.2, 3.6):
        ax.add_patch(FancyBboxPatch((wx + 0.8, ry + off), rw - 2.2, 0.22,
                                    boxstyle="round,pad=0,rounding_size=0.08",
                                    linewidth=1.0, edgecolor=C2, facecolor="#CDEFE0", zorder=3))
    txt(ax, rx + rw - 1.7, ry + 2.85, "墙面平行双缆", size=8.2, color=C2)
    notes_r = ["施工快、不受土壤影响", "特性稳定易标定", "可见性略高"]
    for i, n in enumerate(notes_r):
        yy = ry + 0.5 + i * 0.55
        box(ax, wx + 0.8, yy, rw - 2.4, 0.45, "#FFFFFF", C2, lw=1.1)
        txt(ax, wx + 0.8 + (rw - 2.4) / 2, yy + 0.23, n, size=8.6, color=INK)

    # 底部：转角/过车处理
    bx, by, bw, bh = 0.7, 0.95, 11.8, 0.85
    box(ax, bx, by, bw, bh, "#FFF7ED", C4, lw=1.2)
    txt(ax, bx + bw / 2, by + 0.42,
        "转角：弯曲半径 R_min≥10D≈13 cm 平滑过渡；过车：穿 PVC 管深埋 0.4 m 或承压 ≥1 MPa 护套",
        size=8.6, color=C4, weight="bold")

    footer(ax, "注：埋地与贴墙算法一致仅标定不同；埋地隐形但受土壤湿度影响需 AGC 补偿，贴墙稳定但可见。转角 R_min≥10D 平滑过渡，过车穿管深埋或承压护套。工程基准示意。")
    fig.savefig(os.path.join(OUT, "install-compare.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
