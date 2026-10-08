# -*- coding: utf-8 -*-
"""生成 BOTDA 文章配套矢量示意图（4 张）。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W = 13.2


def newfig(h):
    fig, ax = plt.subplots(figsize=(W, h), dpi=140)
    ax.set_xlim(0, W)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def box(ax, x, y, w, h, fc="#eef3fb", ec="#2f5f96", lw=1.6, radius=0.16, style="round,pad=0.02"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style,
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))


def txt(ax, x, y, s, fs=9.4, color="#1f2a37", weight="normal", ha="center", va="center", zorder=6):
    ax.text(x, y, s, fontsize=fs, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, linespacing=1.35)


def arrow(ax, p1, p2, color="#c0392b", lw=1.8, ls="-", ms=11, zorder=5, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                                 color=color, linewidth=lw, linestyle=ls,
                                 zorder=zorder, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


C_MAIN = "#2f5f96"
C_ACC = "#c0392b"
C_HL = "#b8860b"
C_OK = "#2e7d5b"
C_GREY = "#6b7280"
BG = "#eef3fb"

# ============================================================
# 图 1：BOTDA 环路型光路与时域定位
# ============================================================
def fig1():
    H = 8.8
    fig, ax = newfig(H)

    txt(ax, W / 2, H - 0.5, "BOTDA 环路型光路结构与时间—空间映射 ", fs=13.5, weight="bold", color="#12263f")

    fy, fh = 4.70, 0.44
    x0, x1 = 1.95, 10.35

    # 传感光缆本体
    ax.add_patch(Rectangle((x0, fy), x1 - x0, fh, facecolor="#d6dee9",
                           edgecolor="#334e68", linewidth=1.5, zorder=2))
    txt(ax, 3.30, fy + fh / 2, "传感光缆（长度 L）", fs=9.6, weight="bold", color="#334e68")

    # A 端设备
    box(ax, 0.25, fy - 0.95, 1.55, 2.05, fc="#fdecea", ec=C_ACC, lw=1.8)
    txt(ax, 1.025, fy + 0.72, "A 端", fs=10, weight="bold", color=C_ACC)
    txt(ax, 1.025, fy + 0.08, "泵浦脉冲\n入射 + 接收", fs=8.4, color="#7d2a22")

    # B 端设备
    box(ax, 11.0, fy - 0.95, 1.95, 2.05, fc="#e8f5ee", ec=C_OK, lw=1.8)
    txt(ax, 11.975, fy + 0.72, "B 端", fs=10, weight="bold", color=C_OK)
    txt(ax, 11.975, fy + 0.08, "探测连续光\n入射", fs=8.4, color="#245c43")

    # 泵浦脉冲：A -> 右
    arrow(ax, (1.83, fy + fh + 0.52), (10.28, fy + fh + 0.52), color=C_ACC, lw=2.2)
    txt(ax, 3.65, fy + fh + 0.68, "泵浦脉冲 Pump（宽频扫频，脉宽 τ）", fs=9.2, color=C_ACC, weight="bold", va="bottom")

    # 探测连续光：B -> 左
    arrow(ax, (10.92, fy - 0.52), (2.05, fy - 0.52), color=C_OK, lw=2.2)
    txt(ax, 8.75, fy - 0.68, "探测连续光 Probe（与泵浦频差 ≈ ν_B）", fs=9.2, color=C_OK, weight="bold", va="top")

    # 沿程测点提示
    txt(ax, 8.55, fy + fh / 2, "沿程连续测点：Δz ≈ 0.102·τ", fs=8.8, color="#5b6472")

    # 相互作用区
    cx = 6.15
    ax.add_patch(Rectangle((cx - 0.62, fy - 0.16), 1.24, fh + 0.32, facecolor="#fff4d6",
                           edgecolor=C_HL, linewidth=1.6, zorder=3, alpha=0.97))
    for k in range(4):
        xx = cx - 0.44 + k * 0.29
        ax.plot([xx, xx], [fy + 0.06, fy + fh - 0.06], color=C_HL, lw=1.4, zorder=4)

    # 虚线连接（白描边保证跨过箭头仍清晰）
    ln = ax.plot([cx, cx], [fy + fh, 6.34], color="#9aa7b6", lw=1.4, ls=(0, (4, 3)), zorder=4)[0]
    ln.set_path_effects([pe.withStroke(linewidth=3.6, foreground="white")])

    txt(ax, 5.95, 6.60, "受激布里渊放大：相遇点能量由泵浦转移给探测光", fs=9.0, weight="bold", color="#8a6300")
    txt(ax, 9.60, 6.66, "两光束相向而行，\n相遇点以半速前移", fs=8.6, color="#8a6300")

    # ---- 时间轴面板 ----
    ty = 1.64
    box(ax, 0.55, ty - 0.34, 12.1, 2.02, fc="#f7f9fc", ec="#b9c6d6", lw=1.4)
    txt(ax, 0.83, ty + 1.38, "时域定位", fs=9.4, weight="bold", color=C_MAIN, ha="left")

    ax.plot([1.35, 11.35], [ty + 0.52, ty + 0.52], color="#334e68", lw=1.8, zorder=3)
    for xx, lab in [(1.35, "0"), (5.20, "z"), (11.35, "L")]:
        ax.plot([xx], [ty + 0.52], marker="o", ms=5, color="#334e68", zorder=4)
        txt(ax, xx, ty + 0.22, lab, fs=9.0, color="#334e68", weight="bold")

    txt(ax, 1.30, ty + 1.02, "接收信号时间轴 t：0", fs=8.6, color=C_GREY, ha="left")
    txt(ax, 5.20, ty + 1.02, "t = 2nz/c", fs=8.6, color=C_GREY)
    txt(ax, 11.40, ty + 1.02, "t = 2nL/c（时窗）", fs=8.6, color=C_GREY, ha="right")

    txt(ax, 6.35, ty - 0.05,
        "位置反演：z = c·t / (2n)        接收时窗：t_win = 2nL/c ≈ 9.8 µs/km   （30 km ≈ 294 µs）",
        fs=9.0, color="#1f2a37", weight="bold")

    # ---- 底部结论 ----
    box(ax, 0.55, 0.22, 12.1, 0.90, fc="#fff4d6", ec=C_HL, lw=1.5)
    txt(ax, 6.6, 0.83,
        "国标 GB/T 43256-2023 称之为「环路型」：光脉冲入射端与散射光接收端分处光纤两端。",
        fs=9.2, weight="bold", color="#8a6300")
    txt(ax, 6.6, 0.44,
        "工程含义——两端都必须接入且可达；任一端光缆被挖断或尾纤被拔，整条线路立即失测。",
        fs=9.2, color="#a06a1a")

    fig.savefig(os.path.join(OUT, "arch-loop.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================
# 图 2：空间分辨率与应变精度的孪生权衡
# ============================================================
def fig2():
    H = 7.4
    fig = plt.figure(figsize=(W, H), dpi=140)

    dz = np.array([0.1, 0.2, 0.5, 1.0, 2.0, 5.0])
    tau = 9.8 * dz                       # ns
    dnu = 0.886 / (tau * 1e-9) / 1e6     # MHz, -3dB 带宽
    nuB = 30.0                           # MHz, BGS 自然线宽
    eta = 1.0 / np.sqrt(1.0 + (dnu / nuB) ** 2)
    snr = eta * tau                      # 归一化 SNR 因子

    # ---- 上：频谱展宽比 ----
    ax1 = fig.add_axes([0.10, 0.56, 0.83, 0.365])
    ax1.plot(dz, dnu / nuB, "-o", color=C_ACC, lw=2.2, ms=6, label="泵浦谱宽 / 增益谱线宽")
    ax1.axhline(1.0, color=C_HL, ls="--", lw=1.8, label="Δν_pulse = Δν_BGS（临界点）")
    ax1.set_xscale("log")
    ax1.set_ylabel("谱宽比", fontsize=10)
    ax1.set_title("① 脉宽越窄，泵浦谱越宽 —— 超出增益谱的那部分功率参与不了受激放大",
                  fontsize=11, weight="bold", color="#12263f", pad=10)
    ax1.grid(alpha=0.28, ls=":")
    ax1.set_xticks(dz)
    ax1.set_xticklabels([])
    ax1.legend(fontsize=8.8, loc="upper right", framealpha=0.95)
    ax1.set_xlim(0.08, 6.6)
    for s in ["top", "right"]:
        ax1.spines[s].set_visible(False)

    # 填充「浪费」区
    ax1.axvspan(0.08, 1.05, color="#fdecea", alpha=0.55, zorder=0)
    ax1.text(0.115, ax1.get_ylim()[1] * 0.13, "谱已明显宽于增益谱", fontsize=8.6,
             color="#7d2a22", weight="bold")

    # ---- 下：SNR 代价 ----
    ax2 = fig.add_axes([0.10, 0.10, 0.83, 0.375])
    ax2.plot(dz, snr, "-o", color=C_MAIN, lw=2.4, ms=6.5)
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    ax2.set_xticks(dz)
    ax2.set_xticklabels(["0.1 m", "0.2 m", "0.5 m", "1.0 m", "2.0 m", "5.0 m"], fontsize=9.4)
    ax2.set_xlabel("空间分辨率 Δz（= 0.102 × 脉宽 ns）", fontsize=10.5)
    ax2.set_ylabel("归一化 SNR 因子 η·τ", fontsize=10)
    ax2.set_title("② 叠加「脉宽变短 → 总能量线性下降」之后：信号随分辨率提高而急剧衰减",
                  fontsize=11, weight="bold", color="#12263f", pad=10)
    ax2.grid(alpha=0.28, ls=":")
    ax2.set_xlim(0.08, 6.6)
    for s in ["top", "right"]:
        ax2.spines[s].set_visible(False)

    labels = {0.1: "×1/1400", 0.2: "×1/319", 0.5: "×1/52", 1.0: "×1/13.4", 2.0: "×1/3.9", 5.0: "基准"}
    for x, y, lb in zip(dz, snr, [labels[v] for v in dz]):
        ax2.annotate(lb, (x, y), textcoords="offset points", xytext=(0, 9),
                     ha="center", fontsize=8.8, color="#12263f", weight="bold")
    ax2.annotate("维持同等精度所需测量时间 ∝ 信号损失的平方\n（1 m 相对 5 m：约 180 倍）",
                 (0.13, 6.0), fontsize=9.2, color="#7d2a22", weight="bold")

    fig.savefig(os.path.join(OUT, "tradeoff-res.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================
# 图 3：温度 / 应变交叉敏感与双缆解耦
# ============================================================
def fig3():
    H = 8.6
    fig, ax = newfig(H)
    txt(ax, W / 2, H - 0.5, "一个方程两个未知数：双缆温度解耦与那笔 24 µε/℃ 的账",
        fs=13.2, weight="bold", color="#12263f")

    # ---- 左侧：结构断面示意 ----
    sx, sy, sw, sh = 0.55, 4.30, 4.45, 3.25
    ax.add_patch(Rectangle((sx, sy), sw, sh, facecolor="#f2f4f7", edgecolor="#8a93a0", lw=1.6, zorder=2))
    txt(ax, sx + sw / 2, sy + sh - 0.32, "被测结构断面（混凝土基体）", fs=9.2, weight="bold", color="#5b6472")

    # A 缆：粘结
    ya = sy + 1.85
    for k in range(7):
        xx = sx + 0.72 + k * 0.56
        ax.plot([xx, xx], [ya + 0.30, ya + 0.46], color="#7d2a22", lw=1.0, zorder=3)
    ax.add_patch(Rectangle((sx + 0.35, ya), sw - 0.7, 0.30, facecolor=C_ACC,
                           edgecolor="#7d2a22", lw=1.2, zorder=3))
    txt(ax, sx + sw / 2, ya + 0.68, "A 缆：金属基应变传感缆（全长粘结 / 植入）", fs=8.9, weight="bold", color="#7d2a22")

    # B 缆：松套自由
    yb = sy + 0.75
    for k in range(6):
        xx = sx + 0.70 + k * 0.58
        ax.add_patch(Rectangle((xx, yb + 0.32), 0.20, 0.16, facecolor="#cfe3d8",
                               edgecolor="#2e7d5b", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((sx + 0.35, yb), sw - 0.7, 0.30, facecolor=C_OK,
                           edgecolor="#245c43", lw=1.2, zorder=3))
    txt(ax, sx + sw / 2, yb - 0.30, "B 缆：松套管松弛测温缆（必须保持自由）", fs=8.9, weight="bold", color="#245c43")
    txt(ax, sx + sw / 2, sy + 0.18, "两缆同位置、同深度、同朝向，间距宜在数厘米内", fs=8.3, color=C_GREY)

    # ---- 右侧：方程组 ----
    bx, by, bw, bh = 5.35, 4.30, 7.30, 3.02
    box(ax, bx, by, bw, bh, fc="#f7f9fc", ec=C_MAIN, lw=1.6)
    txt(ax, bx + bw / 2, by + bh - 0.32, "双缆解耦方程组", fs=10.5, weight="bold", color=C_MAIN)
    rows = [
        ("主方程（一个式子两个未知量，无法单独求解）", "normal", 9.0, "#5b6472"),
        ("Δν_B  =  C_ε · Δε  +  C_T · ΔT", "bold", 10.6, C_ACC),
        ("", "normal", 9.0, "#5b6472"),
        ("A 缆（同时感受应变与温度）   Δν_A = C_ε·Δε + C_T·ΔT", "bold", 9.2, "#12263f"),
        ("B 缆（松弛，不感受结构应变） Δν_B = C_T·ΔT", "bold", 9.2, "#12263f"),
        ("相减即得结构应变            Δε = ( Δν_A − Δν_B ) / C_ε", "bold", 9.2, C_OK),
    ]
    yy = by + bh - 0.90
    for s, wt, fs, col in rows:
        txt(ax, bx + bw / 2, yy, s, fs=fs, color=col, weight=wt)
        yy -= 0.34 if s else 0.18

    # ---- 下：假应变 vs 真应变 对比条 ----
    box(ax, 0.55, 1.10, 12.1, 2.60, fc="#fff4d6", ec=C_HL, lw=1.5)
    txt(ax, 6.6, 3.42, "为什么温度解耦是生死线：假信号比真信号还大",
        fs=10.5, weight="bold", color="#8a6300")

    barw = 11.2
    ax.add_patch(Rectangle((0.98, 2.55), barw, 0.42, facecolor=C_ACC, edgecolor="#7d2a22", zorder=3))
    txt(ax, 0.98 + barw / 2, 2.76, "24 µε/℃ ←  温度解耦误差每 1 ℃ 所生成的假应变",
        fs=9.3, color="white", weight="bold")

    gw = barw * 10.0 / 24.0
    ax.add_patch(Rectangle((0.98, 1.85), gw, 0.42, facecolor=C_OK, edgecolor="#245c43", zorder=3))
    txt(ax, 0.98 + gw + 0.16, 2.06, "10 µε/℃ ←  混凝土热胀冷缩的真实应变",
        fs=9.3, color="#245c43", weight="bold", ha="left")

    txt(ax, 6.6, 1.40,
        "假 / 真 ≈ 2.4 : 1 —— 要把假应变压到真实信号的 1/2 以内，温度解耦误差须控制在 0.2 ℃ 上下。",
        fs=9.4, weight="bold", color="#8a6300")

    fig.savefig(os.path.join(OUT, "dual-cable.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================
# 图 4：从目标到验收的落地流程
# ============================================================
def fig4():
    H = 6.4
    fig, ax = newfig(H)
    txt(ax, W / 2, H - 0.45, "BOTDA 监测系统落地流程：决定成败的是第 2 步与第 4 步",
        fs=13.2, weight="bold", color="#12263f")

    stages = {
        1: ("定目标与量值\n应变 / 温度量程", BG, C_MAIN),
        2: ("选传感缆\n能否传递应变", "#fdecea", C_ACC),
        3: ("定敷设工艺\n粘结 / 植入 / 自由", BG, C_MAIN),
        4: ("温度解耦设计\n松弛测温缆 + 基线", "#fdecea", C_ACC),
        5: ("链路与周期核算\n损耗预算 · 单次时长", BG, C_MAIN),
        6: ("施工熔接与验收\n损耗 ≤0.05 dB/点", BG, C_MAIN),
        7: ("基线建立与移交\n桩号映射 · 分级预警", "#e8f5ee", C_OK),
    }

    bw, bh = 2.42, 1.95
    gap = (W - 1.30 - 4 * bw) / 3
    colx = [0.65 + k * (bw + gap) for k in range(4)]
    y_top, y_bot = 3.55, 1.05
    pos = {1: (colx[0], y_top), 2: (colx[1], y_top), 3: (colx[2], y_top), 4: (colx[3], y_top),
           5: (colx[2], y_bot), 6: (colx[1], y_bot), 7: (colx[0], y_bot)}

    for i in [1, 2, 3, 4, 5, 6, 7]:
        ss, fc, ec = stages[i]
        px, py = pos[i]
        key = i in (2, 4)
        box(ax, px, py, bw, bh, fc=fc, ec=ec, lw=2.4 if key else 1.6)
        ax.add_patch(plt.Circle((px + bw / 2, py + bh - 0.28), 0.21, facecolor=ec,
                                edgecolor="white", linewidth=1.2, zorder=5))
        txt(ax, px + bw / 2, py + bh - 0.28, str(i), fs=9.4, color="white", weight="bold", zorder=6)
        txt(ax, px + bw / 2, py + bh / 2 - 0.24, ss, fs=8.9,
            color="#1f2a37", weight="bold" if key else "normal")

    # 第一排 1→2→3→4
    for a, b in [(1, 2), (2, 3), (3, 4)]:
        xa, ya = pos[a]
        xb, yb = pos[b]
        arrow(ax, (xa + bw, ya + bh / 2), (xb, yb + bh / 2), color="#334e68", lw=1.8)

    # 4 ↓ 5（先下到两排之间，再左移到第 3 列，再下到 5）
    x4, y4 = pos[4]
    x5, y5 = pos[5]
    mid = (y4 + y5 + bh) / 2
    ax.plot([x4 + bw / 2, x4 + bw / 2], [y4, mid], color="#334e68", lw=1.8)
    ax.plot([x4 + bw / 2, x5 + bw / 2], [mid, mid], color="#334e68", lw=1.8)
    arrow(ax, (x5 + bw / 2, mid), (x5 + bw / 2, y5 + bh), color="#334e68", lw=1.8)

    # 第二排 5→6→7（向左）
    for a, b in [(5, 6), (6, 7)]:
        xa, ya = pos[a]
        xb, yb = pos[b]
        arrow(ax, (xa, ya + bh / 2), (xb + bw, yb + bh / 2), color="#334e68", lw=1.8)

    # 复核回路 7 → 1
    x7, y7 = pos[7]
    x1, y1 = pos[1]
    ax.add_patch(FancyArrowPatch((x7 + bw / 2, y7), (x1 + bw / 2, y1),
                                 arrowstyle="-|>", mutation_scale=12, color="#9aa7b6",
                                 lw=1.5, ls=(0, (5, 3)), connectionstyle="arc3,rad=-0.30", zorder=1))
    txt(ax, W / 2, 0.38, "预警值须回归结构分析复核（GB 50982-2014 3.4.5）：判据不在设备说明书里，而在结构分析中",
        fs=9.0, color=C_GREY)

    fig.savefig(os.path.join(OUT, "flow-install.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    for f in ["arch-loop.png", "tradeoff-res.png", "dual-cable.png", "flow-install.png"]:
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p))
