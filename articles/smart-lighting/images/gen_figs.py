# -*- coding: utf-8 -*-
"""智能照明控制系统产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system      四层架构与两条总线        （1.2）
  图2 dimming-perception 调光的三条曲线：功率/光通/感知  （2.2）
  图3 daylight-feedback 恒照度光反馈系数三种情形    （2.4）
  图4 energy-waterfall  节能四笔账瀑布（新建 vs 改造）（2.5）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches

# 全局字体：不设会让内置 axes（刻度/标签/图例/标题）用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- 全局样式（light 主题，浅底深字）----
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
    """说明条：单独开 axes，避免与绘图区坐标系混用"""
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
# 图 1：四层架构与两条总线
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  智能照明的四层架构与两条总线",
          "强电配电回路与控制总线彼此解耦：一条 DALI 线可跨多个强电回路，反之亦然")

    # ---- 左侧：四层 ----
    layers = [
        ("管理层（软件）", "上位机 / 云平台 · 能耗报表\n场景编排 · BMS 网关", "分钟 ~ 天", C5),
        ("控制层（网关）", "多回路 DALI 网关 · 区域应用控制器\nKNX / BACnet 网关", "100 ms ~ 秒", C1),
        ("现场层（总线设备）", "DALI 调光驱动 · 输入设备（传感器 / 面板）\n继电器 / 开关模块", "10 ~ 100 ms", C2),
        ("灯具层", "LED 模组 · 驱动 · 光学件", "ms", C3),
    ]
    lx, lw_ = 0.75, 4.55
    top = H - 1.55
    bh = 1.18
    gap = 0.30
    for i, (name, desc, ts, c) in enumerate(layers):
        y = top - i * (bh + gap) - bh
        box(ax, lx, y, lw_, bh, "#FFFFFF", c, lw=1.7)
        txt(ax, lx + 0.16, y + bh - 0.30, name, size=9.8, weight="bold", color=c, ha="left")
        txt(ax, lx + 0.16, y + 0.44, desc, size=8.3, color=INK, ha="left")
        txt(ax, lx + lw_ - 0.16, y + bh - 0.30, ts, size=8.3, color=MUTED, ha="right")

    # 层间双向箭头（数据上行 / 指令下行）
    for i in range(3):
        ytop = top - i * (bh + gap) - bh
        ybot = top - (i + 1) * (bh + gap)
        arrow(ax, lx + 1.05, ybot + 0.16, lx + 1.05, ytop - 0.16, color=CGREY, lw=1.2)
        arrow(ax, lx + lw_ - 1.05, ytop - 0.16, lx + lw_ - 1.05, ybot + 0.16, color=CGREY, lw=1.2)
    txt(ax, lx + 1.05, top + 0.30, "状态 · 能耗 · 故障", size=8.0, color=MUTED, ha="center")
    txt(ax, lx + lw_ - 1.05, top + 0.30, "指令 · 场景", size=8.0, color=MUTED, ha="center")

    # ---- 右侧：两条总线（竖排通道）----
    bx = 6.35
    bw = 5.95
    txt(ax, bx + bw / 2, H - 1.62, "两条走向完全不同的总线", size=9.8, weight="bold", ha="center")

    # 通道 1：强电
    y1 = 6.60
    h1 = 1.75
    box(ax, bx, y1 - h1, bw, h1, "#FFF7ED", C3, lw=1.5)
    txt(ax, bx + 0.18, y1 - 0.32, "① 强电配电总线  AC 220 / 380 V", size=9.4, weight="bold", color=C4, ha="left")
    rows1 = [("每个回路带载", "15 ~ 25 盏（受断路器额定电流与启动冲击限制）"),
             ("设计依据", "GB 51348 · GB 50303"),
             ("与控制的耦合", "无 —— 回路划分一旦确定，改分区就要动强电")]
    for k, (a, b) in enumerate(rows1):
        yy = y1 - 0.76 - k * 0.42
        txt(ax, bx + 0.30, yy, a, size=8.4, color=INK, ha="left", weight="bold")
        txt(ax, bx + 1.66, yy, b, size=8.4, color=MUTED, ha="left")

    # 通道 2：控制总线
    y2 = y1 - h1 - 0.30
    h2 = 2.45
    box(ax, bx, y2 - h2, bw, h2, "#EFF6FF", C1, lw=1.5)
    txt(ax, bx + 0.18, y2 - 0.32, "② 控制总线  DALI 两线制（标称 16 V）", size=9.4, weight="bold", color=C1, ha="left")
    rows2 = [("地址 / 组 / 场景", "64 地址 · 16 组 · 16 场景（每条线）"),
             ("电流 / 压降", "≤ 250 mA · 末端压降 ≤ 2 V"),
             ("线缆", "300 m @ 1.5 mm²（0.5 mm² 时约 190 m）"),
             ("敷设", "可与强电同缆 —— 只有基本绝缘，不是 SELV"),
             ("极性 / 终端电阻", "DALI-2 起无极性要求 · 无需终端电阻")]
    for k, (a, b) in enumerate(rows2):
        yy = y2 - 0.72 - k * 0.40
        txt(ax, bx + 0.30, yy, a, size=8.4, color=INK, ha="left", weight="bold")
        txt(ax, bx + 1.90, yy, b, size=8.4, color=MUTED, ha="left")

    # ---- 底部：解耦带来的运维陷阱 ----
    y3 = y2 - h2 - 0.30
    h3 = 0.98
    box(ax, bx, y3 - h3, bw, h3, "#F5F3FF", C5, lw=1.4)
    txt(ax, bx + 0.18, y3 - 0.30, "[!] 解耦的代价：故障定位变复杂", size=8.8, weight="bold", color=C5, ha="left")
    txt(ax, bx + 0.30, y3 - 0.62, "一个强电回路停电，会同时影响三条 DALI 线上的部分灯具。",
        size=8.2, color=INK, ha="left")
    txt(ax, bx + 0.30, y3 - 0.87, "对策：地址表强制标注所属强电回路编号，交付时提供双向对照表。",
        size=8.2, color=INK, ha="left")

    footer(ax, "注：DALI 地址与强电回路无需一一对应，这种解耦是「分区可软件重构」的物理基础。示意参数按 IEC 62386 与工程基准绘制。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：调光的三条曲线（功率 / 光通 / 感知亮度）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  调光的非线性：三条曲线决定了节能率与主观感受的错配",
          "感知亮度遵循 Stevens 幂律 B ∝ L^0.33；物理光通因 droop 而优于线性")

    # 绘图区（固定比例 axes）
    px, py, pw, ph = 1.05, 1.55, 7.85, 5.55
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    xs = [i / 100 for i in range(101)]
    # 功率设定 s -> 光通（含 droop 超线性）
    # 简化：L = s * (1 + 0.10 * (1 - s))  —— 低负载光效提升最多 10%
    L = [s * (1 + 0.10 * (1 - s)) for s in xs]
    B = [l ** 0.33 for l in L]
    lin = xs

    a.plot([x * 100 for x in xs], [l * 100 for l in L], color=C2, lw=2.4, label="物理光通 L（含 droop 超线性）", zorder=3)
    a.plot([x * 100 for x in xs], [b * 100 for b in B], color=C1, lw=2.4, label="主观亮度 B = L^0.33", zorder=4)
    a.plot([x * 100 for x in xs], [v * 100 for v in lin], color=CGREY, lw=1.6, ls="--", label="线性参考（功率设定）", zorder=2)

    # 标注点：垂点线 + 小圆点 + 白描边文字（白描边保证压线时仍可读）
    stroke = [pe.withStroke(linewidth=3.2, foreground="white")]
    pts = [50, 20, 10]
    for s in pts:
        a.plot([s, s], [0, B[s] * 100], color=CGREY, lw=1.0, ls=":", zorder=2)
        a.scatter([s], [L[s] * 100], s=32, color=C2, zorder=6, edgecolors="white", linewidths=1.2)
        a.scatter([s], [B[s] * 100], s=32, color=C1, zorder=6, edgecolors="white", linewidths=1.2)
    annos = [(50, L[50] * 100, 51.5, 43, C2, "光通 52%"),
             (50, B[50] * 100, 51.5, 88, C1, "主观 81%"),
             (20, L[20] * 100, 21.5, 14, C2, "光通 22%"),
             (20, B[20] * 100, 21.5, 66, C1, "主观 60%"),
             (10, L[10] * 100, 11.5, 5, C2, "光通 11%"),
             (10, B[10] * 100, 11.5, 41, C1, "主观 48%")]
    for ox, oy, tx, ty, c, s_ in annos:
        a.annotate(s_, xy=(ox, oy), xytext=(tx, ty), fontsize=8.2, color=c, weight="bold",
                   ha="left", va="center", zorder=7, path_effects=stroke,
                   arrowprops=dict(arrowstyle="-", color=c, lw=0.9, shrinkA=1, shrinkB=3))

    a.set_xlim(0, 100)
    a.set_ylim(0, 108)
    a.set_xlabel("功率设定（%）", fontsize=9.2, color=INK)
    a.set_ylabel("相对值（%）", fontsize=9.2, color=INK)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.4, colors=MUTED)
    a.legend(loc="lower right", fontsize=8.4, frameon=True, facecolor="#FFFFFF",
             edgecolor=GRID, framealpha=1.0)

    # ---- 右侧结论卡 ----
    cx, cw = 9.15, 3.20
    ty = H - 1.62
    box(ax, cx, ty - 2.05, cw, 2.05, "#FFF7ED", C3, lw=1.5)
    txt(ax, cx + 0.16, ty - 0.34, "结论一：小幅调光等于没调", size=9.0, weight="bold", color=C4, ha="left")
    lines1 = ["100% → 80%：光通 88%，主观只暗 4%",
              "用户几乎察觉不到，会认为",
              "「装了调光但没效果」。",
              "要让感知明显，幅度须 ≥ 50%。"]
    for k, s in enumerate(lines1):
        txt(ax, cx + 0.20, ty - 0.74 - k * 0.34, s, size=8.2, color=INK, ha="left")

    ty2 = ty - 2.05 - 0.30
    box(ax, cx, ty2 - 2.15, cw, 2.15, "#EFF6FF", C1, lw=1.5)
    txt(ax, cx + 0.16, ty2 - 0.34, "结论二：大幅调光体验上很安全", size=9.0, weight="bold", color=C1, ha="left")
    lines2 = ["20% 设定 → 光通 22%，主观仍有 60%",
              "下班 / 清洁模式设 20% 完全可接受。",
              "想主观「暗一半」，光通须降到 12.2%",
              "（0.5^(1/0.33)），功率约 11%。"]
    for k, s in enumerate(lines2):
        txt(ax, cx + 0.20, ty2 - 0.74 - k * 0.34, s, size=8.2, color=INK, ha="left")

    ty3 = ty2 - 2.15 - 0.30
    box(ax, cx, ty3 - 1.55, cw, 1.55, "#ECFDF5", C2, lw=1.5)
    txt(ax, cx + 0.16, ty3 - 0.34, "配套：渐变时间要不对称", size=9.0, weight="bold", color=C2, ha="left")
    lines3 = ["降亮度 3 ~ 5 s（暗适应慢）",
              "升亮度 0.3 ~ 0.7 s（明适应快）",
              "DALI-2 允许 100 ms ~ 16 min。"]
    for k, s in enumerate(lines3):
        txt(ax, cx + 0.20, ty3 - 0.74 - k * 0.34, s, size=8.2, color=INK, ha="left")

    footer(ax, "注：droop 超线性按「电流降至 50% 时芯片光效提升约 10%」的工程估算建模；Stevens 指数取 0.33（大面积光源，点光源约 0.5）。曲线为演示模型。")
    fig.savefig(os.path.join(OUT, "dimming-perception.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：恒照度光反馈系数 β 的三种情形
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  恒照度控制的光反馈系数 β：三种情形与系统性偏差",
          "E_w = E_set / β + E_d (1 − 1/β)  —— 传感器看到的不是工作面看到的")

    px, py, pw, ph = 1.05, 1.72, 7.85, 5.35
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")

    Eset = 500.0
    Ed = [i for i in range(0, 301)]
    cases = [(1.25, "β = 1.25  传感器视野里灯占大头", C3, "--", "欠补偿"),
             (1.00, "β = 1.00  视野与工作面一致（理想）", C2, "-", "完全补偿"),
             (0.80, "β = 0.80  传感器贴窗，主要看室外", C1, "-.", "过补偿")]
    for beta, lab, c, ls, tag in cases:
        Ew = [Eset / beta + e * (1 - 1 / beta) for e in Ed]
        a.plot(Ed, Ew, color=c, lw=2.3, ls=ls, label=lab, zorder=3)

    # 设定线（文字放在绿线上方的空白带，避免压线）
    a.axhline(Eset, color=MUTED, lw=1.3, ls=":", zorder=2)
    a.text(62, Eset + 22, "设定值 E_set = 500 lx", fontsize=8.6, color=MUTED,
           ha="left", va="center", zorder=7,
           path_effects=[pe.withStroke(linewidth=3.0, foreground="white")])

    # 起点标注（E_d = 0）
    for beta, lab, c, ls, tag in cases:
        v0 = Eset / beta
        a.scatter([0], [v0], s=40, color=c, zorder=6, edgecolors="white", linewidths=1.2)
        off = 30 if beta <= 1.0 else -34
        a.annotate(f"{v0:.0f} lx", xy=(0, v0), xytext=(16, v0 + off),
                   fontsize=8.4, color=c, weight="bold",
                   arrowprops=dict(arrowstyle="-", color=c, lw=1.0), zorder=7)

    # 终点（E_d = 300）：偏移方向按曲线所处高度分别指定，避免压到相邻曲线
    endoff = {1.25: -36, 1.00: 34, 0.80: 34}
    for beta, lab, c, ls, tag in cases:
        v1 = Eset / beta + 300 * (1 - 1 / beta)
        a.scatter([300], [v1], s=40, color=c, zorder=6, edgecolors="white", linewidths=1.2)
        a.annotate(f"{v1:.0f}", xy=(300, v1), xytext=(292, v1 + endoff[beta]),
                   fontsize=8.4, color=c, weight="bold", ha="right", va="center",
                   path_effects=[pe.withStroke(linewidth=3.0, foreground="white")],
                   arrowprops=dict(arrowstyle="-", color=c, lw=1.0, shrinkB=3), zorder=7)

    a.set_xlim(0, 315)
    a.set_ylim(330, 690)
    a.set_xlabel("自然光在工作面的照度 E_d（lx）", fontsize=9.2, color=INK)
    a.set_ylabel("工作面实际照度 E_w（lx）", fontsize=9.2, color=INK)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.4, colors=MUTED)
    a.legend(loc="upper right", fontsize=8.4, frameon=True, facecolor="#FFFFFF",
             edgecolor=GRID, framealpha=1.0)

    # ---- 右侧：三种情形对照 + 标定法 ----
    cx, cw = 9.15, 3.20
    ty = H - 1.78
    # 表格
    box(ax, cx, ty - 2.55, cw, 2.55, "#FFFFFF", GRID, lw=1.3)
    txt(ax, cx + 0.14, ty - 0.30, "三种情形", size=9.0, weight="bold", ha="left")
    hdr = ["β", "夜间偏差", "白天斜率"]
    for k, h in enumerate(hdr):
        txt(ax, cx + 0.22 + k * 1.02, ty - 0.66, h, size=8.2, weight="bold", color=MUTED, ha="left")
    rows = [("1.25", "−20%", "+0.20", C3),
            ("1.00", "0", "0", C2),
            ("0.80", "+25%", "−0.25", C1)]
    for i, (b, d, s, c) in enumerate(rows):
        yy = ty - 1.00 - i * 0.44
        txt(ax, cx + 0.22, yy, b, size=8.4, color=c, ha="left", weight="bold")
        txt(ax, cx + 1.24, yy, d, size=8.4, color=INK, ha="left")
        txt(ax, cx + 2.26, yy, s, size=8.4, color=INK, ha="left")
    txt(ax, cx + 0.14, ty - 2.38, "β < 1 时白天越亮、工作面反而越暗", size=8.0, color=C1, ha="left", weight="bold")

    # 标定法
    ty2 = ty - 2.55 - 0.28
    box(ax, cx, ty2 - 2.90, cw, 2.90, "#ECFDF5", C2, lw=1.5)
    txt(ax, cx + 0.16, ty2 - 0.32, "现场标定 β（夜里三步）", size=9.0, weight="bold", color=C2, ha="left")
    steps = ["1) 全关人工光，读 E_s,0（= E_d）",
             "2) 人工光开 100%，读 E_s,1 并用",
             "    照度计测工作面 E_w,1",
             "3) β = (E_s,1 − E_s,0) / (E_w,1 − E_s,0)",
             "",
             "β ≠ 1 时：设 E_set′ = β·E_set 可消除",
             "夜间偏差，但白天斜率修不好 —— 要挪",
             "传感器位置，或改开环日光采集。"]
    for k, s in enumerate(steps):
        txt(ax, cx + 0.20, ty2 - 0.74 - k * 0.29, s, size=8.2, color=INK, ha="left")

    footer(ax, "注：曲线按 E_w = E_set/β + E_d(1 − 1/β) 绘制，E_set = 500 lx。β 为「传感器对人工光的敏感度 / 对自然光的敏感度」，属现场可标定参数。")
    fig.savefig(os.path.join(OUT, "daylight-feedback.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：节能四笔账瀑布（新建 vs 改造）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  节能量的四笔账：新建与改造的绝对量差 2.16 倍",
          "同样是 50% 上下的节能率，能耗基数不同导致回收期天差地别")

    # ---------- 左：新建（只加控制） ----------
    lx, ly, lw_, lh = 1.00, 2.72, 5.30, 4.28
    a = fig.add_axes([lx / W, ly / H, lw_ / W, lh / H])
    a.set_facecolor("#FFFFFF")
    labels = ["基准\n无控制", "①光衰\n过设计", "②自然\n采光", "③公共区\n占空", "④工位\n离席", "⑤加班\n降级", "改造后"]
    base = 17280.0
    steps = [1918.0, 922.0, 3110.0, 968.0, 2016.0]
    run = base
    bottoms, heights, colors = [], [], []
    # 基准
    bottoms.append(0); heights.append(base); colors.append(MUTED)
    for s in steps:
        bottoms.append(run - s)
        heights.append(s)
        colors.append(C2)
        run -= s
    bottoms.append(0); heights.append(run); colors.append(C1)

    xs = list(range(len(labels)))
    a.bar(xs, heights, bottom=bottoms, color=colors, width=0.62,
          edgecolor="white", linewidth=1.0, zorder=3)
    for i, (b, h_, c) in enumerate(zip(bottoms, heights, colors)):
        if h_ > 900:
            a.text(i, b + h_ / 2, f"{h_:.0f}", ha="center", va="center",
                   fontsize=8.2, color="white", weight="bold", zorder=6)
        else:
            a.text(i, b + h_ + 330, f"−{h_:.0f}", ha="center", va="center",
                   fontsize=7.8, color=C4, weight="bold", zorder=6)
    a.set_xticks(xs)
    a.set_xticklabels(labels, fontsize=8.0, color=INK)
    a.set_ylabel("年耗电量（kWh/a）", fontsize=8.8, color=INK)
    a.set_ylim(0, 20200)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)
    a.set_title("新建全 LED（1200 m²，LPD 4.8 W/m²，3000 h）", fontsize=9.0, color=INK, pad=5)

    # 总节能标注
    a.annotate("", xy=(6, run), xytext=(0, base),
               arrowprops=dict(arrowstyle="<->", color=C4, lw=1.3, ls="--"), zorder=7)
    a.text(3.10, 16200, "节能量 8 934 kWh（51.7%）", fontsize=8.6,
           color=C4, weight="bold", ha="center", zorder=8,
           bbox=dict(boxstyle="round,pad=0.24", fc="#FFF7ED", ec=C3, lw=1.1))

    # ---------- 右：改造（换灯 + 控制） ----------
    rx = 7.10
    b = fig.add_axes([rx / W, ly / H, lw_ / W, lh / H])
    b.set_facecolor("#FFFFFF")
    labels2 = ["基准\nT8 荧光", "换 LED", "①光衰\n过设计", "②自然\n采光", "③公共区\n占空", "④工位\n离席", "⑤加班\n降级", "改造后"]
    base2 = 27720.0
    # 换 LED：从 7.7 W/m² 到 4.8 W/m²，27720 -> 17280
    d_led = base2 - base
    run2 = base2 - d_led
    bottoms2 = [0, run2]
    heights2 = [base2, d_led]
    colors2 = [MUTED, C5]
    for s in steps:
        bottoms2.append(run2 - s)
        heights2.append(s)
        colors2.append(C2)
        run2 -= s
    bottoms2.append(0); heights2.append(run2); colors2.append(C1)

    xs2 = list(range(len(labels2)))
    b.bar(xs2, heights2, bottom=bottoms2, color=colors2, width=0.62,
          edgecolor="white", linewidth=1.0, zorder=3)
    for i, (bt, h_, c) in enumerate(zip(bottoms2, heights2, colors2)):
        if h_ > 1200:
            b.text(i, bt + h_ / 2, f"{h_:.0f}", ha="center", va="center",
                   fontsize=8.0, color="white", weight="bold", zorder=6)
        else:
            b.text(i, bt + h_ + 620, f"−{h_:.0f}", ha="center", va="center",
                   fontsize=7.6, color=C4, weight="bold", zorder=6)
    b.set_xticks(xs2)
    b.set_xticklabels(labels2, fontsize=7.8, color=INK)
    b.set_ylabel("")
    b.set_ylim(0, 32000)
    b.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in b.spines.values():
        sp.set_color(GRID)
    b.tick_params(labelsize=8.0, colors=MUTED)
    b.set_title("既有改造（T8 7.7 W/m² → LED + 控制）", fontsize=9.0, color=INK, pad=5)

    b.annotate("", xy=(7, run2), xytext=(0, base2),
               arrowprops=dict(arrowstyle="<->", color=C4, lw=1.3, ls="--"), zorder=7)
    b.text(4.30, 21500, "节能量 19 374 kWh（69.9%）", fontsize=8.6,
           color=C4, weight="bold", ha="center", zorder=8,
           bbox=dict(boxstyle="round,pad=0.24", fc="#FFF7ED", ec=C3, lw=1.1))

    # ---------- 底部：回收期对照 ----------
    by = 2.00
    bh_ = 1.20
    box(ax, lx, by - bh_, 11.80, bh_, "#FFFFFF", GRID, lw=1.3)
    txt(ax, lx + 0.20, by - 0.30, "回收期（电价 1.0 元/kWh，3000 h/年）", size=8.8, weight="bold", ha="left")
    txt(ax, lx + 0.30, by - 0.68, "新建：投资 33.7 元/m² ÷ 年省 7.45 元/m²", size=8.2, color=INK, ha="left")
    txt(ax, lx + 0.30, by - 0.96, "→ 4.5 年（含非电费价值约 2.9 年）", size=8.2, color=C3, weight="bold", ha="left")
    txt(ax, lx + 6.20, by - 0.68, "改造：投资 64 元/m² ÷ 年省 16.1 元/m²", size=8.2, color=INK, ha="left")
    txt(ax, lx + 6.20, by - 0.96, "→ 4.0 年（2.16 倍的绝对节能量）", size=8.2, color=C2, weight="bold", ha="left")

    footer(ax, "注：两图纵轴刻度不同（左 0~20 200、右 0~32 000），对比时看数值标签而非柱高。均为按本文 §2.5 方法构造的工程演示算例。")
    fig.savefig(os.path.join(OUT, "energy-waterfall.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
