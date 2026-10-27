# -*- coding: utf-8 -*-
"""访客管理系统产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system     访客管理系统总体架构（云-边-端三层 + 轨迹库）        （1.1）
  图2 flow-visitor    访客全流程时序（8 段闭环）                          （1.2）
  图3 throughput      闸机通道数 vs 分钟通行量（峰值线）                  （2.4）
  图4 comparison      访客登记方式对比（6 种方式取舍）                    （4.2）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"
C2 = "#0E9F6E"
C3 = "#E8833A"
C4 = "#C2410C"
C5 = "#7C3AED"
CGREY = "#CBD2D9"


def newfig():
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-", zorder=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       alpha=alpha, linestyle=ls, zorder=zorder)
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
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=10)
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=8.2, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3, wrap=True)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：访客管理系统总体架构（云-边-端）
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  访客管理系统总体架构：云-边-端三层与轨迹库",
          "云端编排审计、边缘本地验签与离线兜底、端侧核验放行（正文 1.1）")

    # 云端管理平台
    cx, cy, cw, ch = 3.0, 5.90, 7.2, 0.95
    box(ax, cx, cy, cw, ch, "#EEF4FF", C1, lw=2.0, r=0.16)
    txt(ax, cx + cw / 2, cy + ch - 0.30, "云端管理平台", size=11.0, weight="bold", color=C1)
    txt(ax, cx + cw / 2, cy + 0.32, "权限编排 · 审计 · 合规留存 · 黑名单", size=8.0, color=INK)

    # 边缘节点
    ex, ey, ew, eh = 1.9, 4.00, 7.6, 0.95
    box(ax, ex, ey, ew, eh, "#FFF1E6", C3, lw=2.0, r=0.16)
    txt(ax, ex + ew / 2, ey + eh - 0.30, "边缘节点（楼栋 / 闸机控制器）", size=10.6, weight="bold", color=C4)
    txt(ax, ex + ew / 2, ey + 0.32, "本地验签 · 离线兜底 · 临时白名单下发", size=8.0, color=INK)

    # 轨迹库（右侧，与边缘同层）
    tx, ty, tw, th = 9.9, 4.00, 2.5, 0.95
    box(ax, tx, ty, tw, th, "#F3ECFD", C5, lw=1.8, r=0.16)
    txt(ax, tx + tw / 2, ty + th - 0.28, "轨迹库", size=10.0, weight="bold", color=C5)
    txt(ax, tx + tw / 2, ty + 0.30, "点位关联时间轴", size=7.6, color=INK)

    # 端侧 5 个设备
    devs = ["预约平台", "核验终端(访客机)", "二维码发卡服务", "闸机 / 门禁", "移动端 App"]
    dy, dh, dw = 1.55, 1.20, 2.05
    xs = [0.5, 3.11, 5.72, 8.33, 10.94]
    for name, dx0 in zip(devs, xs):
        box(ax, dx0, dy, dw, dh, "#EAFFF4", C2, lw=1.5, r=0.14)
        txt(ax, dx0 + dw / 2, dy + dh / 2, name, size=8.2, weight="bold", color=C2)

    # 云端 -> 边缘
    arrow(ax, cx + cw / 2, cy, cx + cw / 2, ey + eh, color=C1, lw=2.0)
    txt(ax, cx + cw / 2 + 1.6, (cy + ey + eh) / 2, "下行指令 / 审计回传", size=7.6, color=C1, ha="left")

    # 边缘 -> 各端设备
    for dx0 in xs:
        arrow(ax, dx0 + dw / 2, ey, dx0 + dw / 2, dy + dh, color=C3, lw=1.4)
    # 边缘 -> 轨迹库
    arrow(ax, ex + ew, ey + eh / 2, tx, ty + th / 2, color=C5, lw=1.6)
    txt(ax, (ex + ew + tx) / 2, ty + th + 0.28, "轨迹归档", size=7.4, color=C5, weight="bold")

    footer(ax, "注：断网时边缘与端凭离线签名码完成核验，恢复后回传审计；轨迹库与安全/应急联动，用于回答「谁还在楼内」（正文 1.1/3.5/四）。示意图。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：访客全流程时序（8 段）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  访客全流程时序：从预约到轨迹归档的 8 段闭环",
          "签离常被省略，但它决定轨迹是否闭合、应急能否回答「谁还在楼里」（正文 1.2）")

    stages = ["线上预约", "审批", "到访登记", "身份核验", "权限发放", "通行放行", "签离", "轨迹归档"]
    n = len(stages)
    bw, gap = 1.40, 0.27
    total = n * bw + (n - 1) * gap
    x0 = (W - total) / 2
    yb, bh = 5.00, 1.25
    step = bw + gap
    for i, s in enumerate(stages):
        x = x0 + i * step
        fc = "#EEF4FF" if i % 2 == 0 else "#FFF1E6"
        ec = C1 if i % 2 == 0 else C3
        box(ax, x, yb, bw, bh, fc, ec, lw=1.6, r=0.14)
        txt(ax, x + bw / 2, yb + bh - 0.32, "%d" % (i + 1), size=8.2, color=MUTED)
        # 两行显示（4 字折行）
        if len(s) > 2:
            txt(ax, x + bw / 2, yb + 0.62, s[:2], size=8.2, weight="bold", color=ec)
            txt(ax, x + bw / 2, yb + 0.28, s[2:], size=8.2, weight="bold", color=ec)
        else:
            txt(ax, x + bw / 2, yb + bh / 2, s, size=8.6, weight="bold", color=ec)
        if i < n - 1:
            arrow(ax, x + bw, yb + bh / 2, x + bw + gap, yb + bh / 2, color=MUTED, lw=1.6)

    # 分组标注：平台侧(1-2) 与 现场侧(5-8)，居中放在对应组上方
    g12 = x0 + (0 * step + bw / 2 + 1 * step + bw / 2) / 2
    g58 = x0 + (4 * step + bw / 2 + 7 * step + bw / 2) / 2
    txt(ax, g12, yb + bh + 0.32, "访客平台侧", size=8.4, color=C1, weight="bold")
    txt(ax, g58, yb + bh + 0.32, "现场侧", size=8.4, color=C3, weight="bold")
    txt(ax, x0, yb - 0.55, "受邀访客：审批阶段免审预批，分流人工审核压力", size=7.8, color=MUTED, ha="left")
    txt(ax, x0, yb - 0.95, "权限三元组：区域 × 时段 × 次数，过期/超次自动回收", size=7.8, color=MUTED, ha="left")

    footer(ax, "注：核验不通过直接拒绝、不进入后续链路；二维码一次性使用，截图转发即废（正文 1.2/2.1/3.2）。示意图。")
    fig.savefig(os.path.join(OUT, "flow-visitor.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：闸机通道数 vs 分钟通行量
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  闸机通道数 vs 分钟通行量：1 通道不够，2 通道压到 17 s",
          "单通道有效速率 18 人/min；早高峰峰值 30 人/min，需 2 通道（正文 2.4）")

    axp = fig.add_axes([0.12, 0.17, 0.76, 0.58])
    chs = [1, 2, 3, 4]
    cap = [c * 18 for c in chs]
    colors = [C4, C1, C1, C1]  # 1 通道不足标红
    bars = axp.bar([str(c) for c in chs], cap, color=colors, width=0.55, zorder=3)
    labels = ["18 人/min（不足）", "36 人/min", "54 人/min", "72 人/min"]
    for b, v, s, c in zip(bars, cap, labels, colors):
        axp.annotate(s, (b.get_x() + b.get_width() / 2, v),
                     textcoords="offset points", xytext=(0, 6), ha="center",
                     fontsize=8.4, color=c, fontfamily="Microsoft YaHei", weight="bold")
    axp.axhline(30.0, color=C4, ls="--", lw=2.0, zorder=2)
    axp.set_xlim(-0.55, 3.55)
    axp.text(-0.48, 31.5, "早高峰峰值 30 人/min", fontsize=8.6, color=C4,
             fontfamily="Microsoft YaHei", weight="bold", ha="left", va="bottom")
    axp.text(-0.40, 76,
             "N_ch = Q_peak / n_single\n= 30 / 18 = 1.67 \u2192 2",
             fontsize=8.6, color=INK, va="top", ha="left", fontfamily="Microsoft YaHei",
             bbox=dict(boxstyle="round,pad=0.35", fc="#F8FAFC", ec=GRID, lw=1.0), zorder=5)
    axp.set_xlabel("闸机通道数", fontsize=9.0, color=INK, fontfamily="Microsoft YaHei")
    axp.set_ylabel("分钟通行能力 (人/min)", fontsize=9.0, color=INK, fontfamily="Microsoft YaHei")
    axp.set_ylim(0, 80)
    axp.grid(True, ls=":", color=GRID)
    axp.tick_params(labelsize=8.2)
    for lab in axp.get_xticklabels() + axp.get_yticklabels():
        lab.set_fontname("Microsoft YaHei")

    footer(ax, "注：单通道利用率 >1 时 M/M/1 队列发散；2 通道每通道 0.83，平均等待约 17 s（正文 2.3/2.4）。示意图。")
    fig.savefig(os.path.join(OUT, "throughput.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：访客登记方式对比
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  访客登记方式对比：体验、成本、安全的三方取舍",
          "没有万能方式，工程上常组合部署（正文 4.2）")

    cards = [
        ("自助预约", "体验好成本低，依赖被访人确认闭环", C1),
        ("前台登记", "兜底强可控，但占人力易排队", C2),
        ("移动端扫码", "无需硬件部署快，依赖手机网络", C3),
        ("访客卡", "物理凭证离线可用，回收挂失是痛点", C4),
        ("二维码", "动态防伪可离线，重心在有效期管理", C5),
        ("人脸", "无感通行最佳，合规与误识是硬约束", "#0E9F6E"),
    ]
    # 2 列 3 行
    cw, ch = 5.7, 1.55
    gx, gy = 0.55, 0.70  # 起始
    colgap, rowgap = 0.55, 0.45
    for i, (head, desc, c) in enumerate(cards):
        col = i % 2
        row = i // 2
        x = gx + col * (cw + colgap)
        y = gy + (2 - row) * (ch + rowgap) - ch  # 从上往下
        y = 5.55 - row * (ch + rowgap)
        box(ax, x, y, cw, ch, "#F8FAFC", GRID, lw=1.4, r=0.14)
        # 左侧色块 + 序号
        ax.add_patch(Rectangle((x + 0.18, y + 0.30), 0.30, 0.30, facecolor=c, edgecolor=c, zorder=3))
        txt(ax, x + 0.33, y + 0.45, str(i + 1), size=9.0, color="#FFFFFF", weight="bold")
        txt(ax, x + 0.66, y + ch - 0.42, head, size=10.4, color=c, weight="bold", ha="left")
        txt(ax, x + 0.66, y + 0.40, desc, size=8.2, color=INK, ha="left")

    footer(ax, "注：纯人脸做访客核验需压低单次误识（库 5000 时需 2e-6），建议「人脸+二维码」双因子（正文 2.2/4.2）。示意图。")
    fig.savefig(os.path.join(OUT, "comparison.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
