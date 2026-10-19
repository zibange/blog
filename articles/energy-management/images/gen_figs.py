# -*- coding: utf-8 -*-
"""能耗管理系统产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system       三级计量 + 三层架构            （1.1）
  图2 eui-benchmark     度日数回归基线 + 建筑类型对标  （2.2）
  图3 metering-error     CT 量程匹配 + 0.5S/0.2S 等级  （2.3）
  图4 retrofit-payback  帕累托 ABC + 改造回收期        （2.7 / 2.10）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

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
# 图 1：三级计量 + 三层架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  能耗管理系统的三级计量与三层架构",
          "计量越往下越能定位到设备；架构越往上越能做对标与诊断")

    # ---- 左：三级计量 ----
    txt(ax, 2.9, H - 1.55, "计量层级（GB 17167-2006）", size=10.2, weight="bold", ha="center")
    levels = [
        ("一级 · 进线总表", "建筑/核算单位受送电关口\n对账 · 总量考核 · 需量管理", C1),
        ("二级 · 分项表", "空调/照明/动力/特殊\n分项能耗入口（配备率 100%）", C2),
        ("三级 · 终端表", "回路/主要设备\n诊断落到设备的最后一环", C3),
    ]
    lx, lw_ = 0.7, 4.4
    top = H - 1.95
    bh = 1.18
    gap = 0.34
    for i, (name, desc, c) in enumerate(levels):
        y = top - i * (bh + gap) - bh
        box(ax, lx, y, lw_, bh, "#FFFFFF", c, lw=1.7)
        txt(ax, lx + 0.18, y + bh - 0.32, name, size=9.8, weight="bold", color=c, ha="left")
        txt(ax, lx + 0.18, y + 0.46, desc, size=8.3, color=INK, ha="left")
    # 层级间双箭头（数据上行 / 指令下行）
    for i in range(2):
        ytop = top - i * (bh + gap) - bh
        ybot = top - (i + 1) * (bh + gap)
        arrow(ax, lx + 1.1, ybot + 0.16, lx + 1.1, ytop - 0.16, color=CGREY, lw=1.2)
        arrow(ax, lx + lw_ - 1.1, ytop - 0.16, lx + lw_ - 1.1, ybot + 0.16, color=CGREY, lw=1.2)
    txt(ax, lx + 1.1, top + 0.28, "数据上行", size=7.8, color=MUTED, ha="center")
    txt(ax, lx + lw_ - 1.1, top + 0.28, "配置下行", size=7.8, color=MUTED, ha="center")

    # 左下方：四类能耗 chips
    chips = [("电", C1), ("水", C2), ("气", C3), ("暖", C4)]
    cw = 1.02
    cx0 = 0.70
    cy = 2.05
    txt(ax, cx0, cy + 0.78, "分项维度：四类能耗", size=8.6, weight="bold", color=MUTED, ha="left")
    for k, (lab, c) in enumerate(chips):
        x = cx0 + k * (cw + 0.10)
        box(ax, x, cy - 0.30, cw, 0.60, "#FFFFFF", c, lw=1.5)
        txt(ax, x + cw / 2, cy, lab, size=11.0, weight="bold", color=c, ha="center")

    # ---- 右：三层逻辑架构 ----
    txt(ax, 9.25, H - 1.55, "逻辑架构（四层）", size=10.2, weight="bold", ha="center")
    arch = [
        ("应用层", "能耗看板 · 对标报表 · 诊断告警\n与 BAS / 光伏 / 储能 / 充电桩联动", C5),
        ("数据平台层", "时序数据库 · 分项模型\n基线引擎 · 碳排与费用引擎", C1),
        ("采集网关层", "15 min 轮询 · 协议转换\n本地缓存 · 断点续传", C2),
        ("现场计量层", "智能电表 / 流量计 / 热量表\nModbus · MBus 输出", C3),
    ]
    rx, rw = 6.1, 6.3
    atop = H - 1.95
    abh = 1.0
    agap = 0.28
    for i, (name, desc, c) in enumerate(arch):
        y = atop - i * (abh + agap) - abh
        box(ax, rx, y, rw, abh, "#FFFFFF", c, lw=1.7)
        txt(ax, rx + 0.20, y + abh - 0.30, name, size=9.8, weight="bold", color=c, ha="left")
        txt(ax, rx + 0.20, y + 0.40, desc, size=8.3, color=INK, ha="left")
        arrow(ax, rx + rw - 0.5, y + 0.18, rx + rw - 0.5, y - 0.18 + (abh if i < 3 else 0), color=CGREY, lw=1.1) if False else None
    # 层间箭头
    for i in range(3):
        ytop = atop - i * (abh + agap) - abh
        ybot = atop - (i + 1) * (abh + agap)
        arrow(ax, rx + 0.6, ybot + 0.14, rx + 0.6, ytop - 0.14, color=CGREY, lw=1.2)
        arrow(ax, rx + rw - 0.6, ytop - 0.14, rx + rw - 0.6, ybot + 0.14, color=CGREY, lw=1.2)

    footer(ax, "注：计量层级对应 GB 17167-2006 的一/二/三级配备要求；逻辑架构与 BAS 共享现场总线，但 EMS 的准确度与分项维度通常更严。示意参数为工程基准。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：度日数回归基线 + 建筑类型 EUI 对标
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  度日数回归基线：把天气从节能效果里剥离 + 建筑类型 EUI 对标",
          "实际 vs 预测的差才是管理可控的节能；EUI 须按建筑类型分别对标")

    # 左：12 个月 实际 vs 预测 散点 + 对角
    px, py, pw, ph = 0.95, 1.55, 6.05, 5.45
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    import numpy as np
    rng = np.random.default_rng(7)
    pred = np.array([120, 138, 165, 188, 205, 220, 215, 198, 170, 145, 122, 116])
    actual = pred + rng.normal(0, 9, 12) - np.array([6, 4, 2, -3, 1, 5, 3, -2, 4, 6, 7, 5])
    months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    a.scatter(range(12), actual, color=C1, s=44, zorder=5, edgecolors="white", linewidths=1.1, label="实际 EUI")
    a.plot(range(12), pred, color=C2, lw=2.2, label="预测基线（度日数回归）", zorder=4)
    a.set_xticks(range(12))
    a.set_xticklabels(months, fontsize=8.2, color=INK)
    a.set_xlim(-0.6, 11.6)
    a.set_ylim(80, 245)
    a.set_xlabel("月份", fontsize=9.0, color=INK)
    a.set_ylabel("EUI（kWh/(m²·a)）", fontsize=9.0, color=INK)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.2, colors=MUTED)
    a.legend(loc="upper left", fontsize=8.2, frameon=True, facecolor="#FFFFFF",
             edgecolor=GRID, framealpha=1.0)
    # 标注节能差
    stroke = [pe.withStroke(linewidth=3.0, foreground="white")]
    a.annotate("夏季实际 < 预测\n管理节能约 11.6%", xy=(6, actual[6]), xytext=(6.2, 150),
               fontsize=8.2, color=C2, weight="bold", ha="left", zorder=7,
               path_effects=stroke, arrowprops=dict(arrowstyle="-", color=C2, lw=1.0))

    # 右：建筑类型 EUI 对标（范围条）
    bx = 7.35
    a2 = fig.add_axes([bx / W, py / H, 5.0 / W, ph / H])
    a2.set_facecolor("#FFFFFF")
    a2.set_xlim(0, 340)
    a2.set_ylim(-0.6, 4.6)
    types = [("数据中心", 1000, 1800, C4), ("商场", 150, 300, C3),
             ("酒店", 100, 200, C1), ("办公", 70, 150, C2), ("医院", 150, 300, C5)]
    for i, (name, lo, hi, c) in enumerate(types):
        y = 4 - i
        a2.barh(y, hi - lo, left=lo, height=0.42, color=c, alpha=0.55,
                edgecolor=c, linewidth=1.3, zorder=3)
        a2.text(hi + 8, y, "%d~%d" % (lo, hi), fontsize=8.2, color=INK, va="center", zorder=6)
    a2.set_yticks([4 - i for i in range(len(types))])
    a2.set_yticklabels([t[0] for t in types], fontsize=9.0, color=INK)
    a2.set_xlabel("EUI 量级（kWh/(m²·a)，对数轴更直观）", fontsize=8.4, color=INK)
    a2.set_xscale("log")
    a2.grid(True, axis="x", color=GRID, lw=0.8, alpha=0.9)
    for sp in a2.spines.values():
        sp.set_color(GRID)
    a2.tick_params(labelsize=8.0, colors=MUTED)

    footer(ax, "注：左图为某办公楼 12 个月「实际 vs 度日数回归预测」示意，夏季实际低于预测即管理节能空间；右图 EUI 量级按 GB 50189-2015 与工程基准，建筑类型差异可达 10 倍以上，对标必须同类。")
    fig.savefig(os.path.join(OUT, "eui-benchmark.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：CT 量程匹配 + 0.5S/0.2S 等级
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  电流互感器量程匹配：量程选大 3 倍，误差可能翻 5 倍",
          "综合误差随负载率下降而恶化；量程应按最大负载 1.4 倍选")

    # 左：负载率 vs 综合误差曲线
    px, py, pw, ph = 0.95, 1.55, 6.05, 5.45
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    import numpy as np
    x = np.linspace(5, 120, 200)
    # 经验模型：误差在轻载急剧上升，0.5S 级在量程附近 ≤0.5%
    err = 0.5 + 30.0 / (x + 6.0) + 0.02 * (x - 60) ** 2 / 100.0
    err = np.clip(err, 0.3, 12)
    a.plot(x, err, color=C1, lw=2.4, zorder=4, label="0.5S 级综合误差（演示模型）")
    a.axhline(0.5, color=C2, lw=1.4, ls="--", zorder=3)
    a.text(92, 1.0, "量程附近 ≤0.5%", fontsize=8.2, color=C2, weight="bold", va="center", zorder=6)
    # 两个工作点
    a.scatter([27], [err[np.argmin(abs(x - 27))]], s=70, color=C4, zorder=6, edgecolors="white", linewidths=1.2)
    a.scatter([71], [err[np.argmin(abs(x - 71))]], s=70, color=C2, zorder=6, edgecolors="white", linewidths=1.2)
    stroke = [pe.withStroke(linewidth=3.2, foreground="white")]
    a.annotate("1500 A CT → 负载率 27%\n误差 ~3.6%（淹没节能）", xy=(27, err[np.argmin(abs(x - 27))]),
               xytext=(30, 8.6), fontsize=8.4, color=C4, weight="bold", ha="left", va="center",
               zorder=7, path_effects=stroke, arrowprops=dict(arrowstyle="-", color=C4, lw=1.0))
    a.annotate("560 A CT → 负载率 71%\n误差 ≤0.5%（最佳区间）", xy=(71, err[np.argmin(abs(x - 71))]),
               xytext=(50, 3.6), fontsize=8.4, color=C2, weight="bold", ha="right", va="center",
               zorder=7, path_effects=stroke, arrowprops=dict(arrowstyle="-", color=C2, lw=1.0))
    a.set_xlim(5, 120)
    a.set_ylim(0, 12)
    a.set_xlabel("CT 负载率（%）", fontsize=9.0, color=INK)
    a.set_ylabel("综合计量误差（%）", fontsize=9.0, color=INK)
    a.grid(True, color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.2, colors=MUTED)
    a.legend(loc="upper right", fontsize=8.2, frameon=True, facecolor="#FFFFFF",
             edgecolor=GRID, framealpha=1.0)

    # 右：量程选择公式 + 等级对照
    cx, cw = 7.35, 5.0
    ty = H - 1.62
    box(ax, cx, ty - 2.05, cw, 2.05, "#FFF7ED", C3, lw=1.5)
    txt(ax, cx + 0.16, ty - 0.32, "量程反推公式", size=9.4, weight="bold", color=C4, ha="left")
    eqs = ["I_CT,1 ≈ 1.4 × I_load,max", "", "三相：I_load,max = S_max / (√3 · U)", "", "代入 400 A → 560 A（非 1500 A）"]
    for k, s in enumerate(eqs):
        txt(ax, cx + 0.20, ty - 0.74 - k * 0.40, s, size=8.6, color=INK, ha="left")
    ty2 = ty - 2.05 - 0.30
    box(ax, cx, ty2 - 2.35, cw, 2.35, "#EFF6FF", C1, lw=1.5)
    txt(ax, cx + 0.16, ty2 - 0.32, "准确度等级对照（GB 17167-2006）", size=9.4, weight="bold", color=C1, ha="left")
    rows = [("关口计量", "0.2S 级"), ("进线总表", "0.5S 级"), ("次级/主要设备", "1.0 级"), ("配备率", "一/二级 100%")]
    for i, (a_, b_) in enumerate(rows):
        yy = ty2 - 0.78 - i * 0.42
        txt(ax, cx + 0.22, yy, a_, size=8.6, color=INK, ha="left", weight="bold")
        txt(ax, cx + 2.6, yy, b_, size=8.6, color=C1, ha="left")

    footer(ax, "注：曲线为演示模型，刻画「轻载误差急剧恶化」的趋势而非某型号实测；0.5S 指 0.5 级（特殊）有功表，轻载段误差显著大于额定段。具体选型须按表计说明书与现场负载核算。")
    fig.savefig(os.path.join(OUT, "metering-error.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：帕累托 ABC + 改造回收期
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  能耗诊断帕累托（ABC）：20% 设备吃掉 80%，改造回收期约 3 年",
          "诊断资源压在 A 类；回收期对电价与改造范围极敏感")

    # 左：帕累托（按设备累计能耗，A/B/C 着色）
    px, py, pw, ph = 0.95, 1.55, 6.05, 5.45
    a = fig.add_axes([px / W, py / H, pw / W, ph / H])
    a.set_facecolor("#FFFFFF")
    import numpy as np
    n = 12
    cons = np.array([180, 150, 120, 95, 70, 55, 42, 33, 26, 20, 15, 12])  # 万台设备年耗电（相对）
    cum = np.cumsum(cons) / cons.sum() * 100
    colors = [C1 if i < 3 else (C2 if i < 7 else CGREY) for i in range(n)]
    a.bar(range(n), cons, color=colors, width=0.66, edgecolor="white", linewidth=1.0, zorder=3)
    a.plot(range(n), cum, color=C4, lw=2.2, marker="o", markersize=4.5, zorder=5)
    # ABC 分界竖虚线
    a.axvline(2.5, color=C1, ls="--", lw=1.2, zorder=2)
    a.axvline(6.5, color=C2, ls="--", lw=1.2, zorder=2)
    a.text(1.2, max(cons) * 0.92, "A 类", fontsize=9.0, color=C1, weight="bold", ha="center")
    a.text(4.7, max(cons) * 0.92, "B 类", fontsize=9.0, color=C2, weight="bold", ha="center")
    a.text(9.5, max(cons) * 0.92, "C 类", fontsize=9.0, color=MUTED, weight="bold", ha="center")
    a.text(6.5, 30, "前 20% 设备 ≈ 80% 能耗", fontsize=8.4, color=C4, weight="bold",
           ha="center", rotation=90, va="center", zorder=7,
           path_effects=[pe.withStroke(linewidth=3.0, foreground="white")])
    a.set_xlim(-0.6, n - 0.4)
    a.set_ylim(0, max(cons) * 1.18)
    a.set_xticks(range(n))
    a.set_xticklabels(["#%d" % (i + 1) for i in range(n)], fontsize=7.8, color=INK)
    a.set_xlabel("设备（按年耗电降序）", fontsize=9.0, color=INK)
    a.set_ylabel("年耗电（相对值）", fontsize=9.0, color=INK)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(labelsize=8.0, colors=MUTED)

    # 右：改造回收期
    cx, cw = 7.35, 5.0
    ty = H - 1.62
    box(ax, cx, ty - 2.45, cw, 2.45, "#FFFFFF", GRID, lw=1.3)
    txt(ax, cx + 0.16, ty - 0.30, "改造回收期（案例一写字楼）", size=9.4, weight="bold", ha="left")
    lines = ["投资：80 元/m² × 2 万 m² = 160 万",
             "年省：电费 + 需量 + 碳 ≈ 45 万",
             "T = 160 / 45 ≈ 3.6 年",
             "",
             "敏感度：电价 ↑30% → 回收期 ↓ 至 ~2.8 年",
             "范围减半 → 回收期 ↑ 至 ~5 年"]
    for k, s in enumerate(lines):
        col = C4 if "↓" in s or "3.6" in s else INK
        txt(ax, cx + 0.20, ty - 0.74 - k * 0.36, s, size=8.4, color=col, ha="left", weight=("bold" if "T =" in s else "normal"))
    ty2 = ty - 2.45 - 0.30
    box(ax, cx, ty2 - 1.55, cw, 1.55, "#ECFDF5", C2, lw=1.5)
    txt(ax, cx + 0.16, ty2 - 0.32, "工程含义", size=9.2, weight="bold", color=C2, ha="left")
    txt(ax, cx + 0.20, ty2 - 0.74, "把诊断资源压在 A 类设备，", size=8.4, color=INK, ha="left")
    txt(ax, cx + 0.20, ty2 - 1.12, "改造性价比远高于平均用力；", size=8.4, color=INK, ha="left")
    txt(ax, cx + 0.20, ty2 - 1.50, "C 类只做合规全覆盖。", size=8.4, color=INK, ha="left")

    footer(ax, "注：左图为帕累托示意（按设备年耗电降序累计），ABC 分界为经验比例；右图回收期按本文 §2.10 方法，对电价与改造范围极敏感。均为工程演示算例。")
    fig.savefig(os.path.join(OUT, "retrofit-payback.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
