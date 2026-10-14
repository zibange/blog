# -*- coding: utf-8 -*-
"""生成「楼宇自控系统（BAS）产品综述」配套矢量示意图（4 张）。

图 1 四层架构与三层时间尺度
图 2 对象时间常数决定控制周期 + 送风温度回路预算分解
图 3 Trim-and-Respond 设定值轨迹与风机功率对照
图 4 案例三既有建筑改造的投资回收排序
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W = 13.2

C_MAIN = "#2f5f96"
C_ACC = "#b3282d"
C_HL = "#b8860b"
C_OK = "#1f7a4d"
C_GREY = "#6b7280"
BG = "#eef3fb"


def newfig(h):
    fig, ax = plt.subplots(figsize=(W, h), dpi=140)
    ax.set_xlim(0, W)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def box(ax, x, y, w, h, fc=BG, ec=C_MAIN, lw=1.6, radius=0.13, ls="-", zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=%.2f" % radius,
                                facecolor=fc, edgecolor=ec, linewidth=lw,
                                linestyle=ls, zorder=zorder))


def txt(ax, x, y, s, fs=9.0, color="#1f2a37", weight="normal", ha="center",
        va="center", zorder=6, bbox=None, ls=1.35):
    kw = {}
    if bbox:
        kw = dict(bbox=dict(boxstyle="round,pad=0.20", facecolor=bbox, edgecolor="none"))
    ax.text(x, y, s, fontsize=fs, color=color, weight=weight, ha=ha, va=va,
            zorder=zorder, linespacing=ls, **kw)


def arrow(ax, p1, p2, color=C_ACC, lw=1.8, ls="-", ms=12, zorder=5, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                                 color=color, linewidth=lw, linestyle=ls,
                                 zorder=zorder, shrinkA=0, shrinkB=0,
                                 connectionstyle="arc3,rad=%.2f" % rad))


def wline(ax, xs, ys, color=C_GREY, lw=1.5, ls="--", zorder=5, stroke=True):
    line, = ax.plot(xs, ys, color=color, linewidth=lw, linestyle=ls, zorder=zorder)
    if stroke:
        line.set_path_effects([pe.withStroke(linewidth=3.6, foreground="white")])


# ============================================================
# 图 1：四层架构与三层时间尺度
# ============================================================
def fig1():
    h = 8.6
    fig, ax = newfig(h)
    txt(ax, 0.5, 8.05, "图 1　BAS 四层架构与三层时间尺度：越短的回路，越不能依赖通信",
        fs=12.2, color="#16324f", weight="bold", ha="left")

    layers = [
        ("管理层", "工作站 / 服务器 / 历史数据库 / 报表 / Web 发布", "#e8f0f9"),
        ("网络层", "BACnet/IP 骨干（以太网 · UDP 47808）+ 路由器 / 网关", "#dfeaf7"),
        ("控制层", "DDC 通用 + 专用控制器（VAV 箱 / 风机盘管）｜现场总线 BACnet MS/TP（RS-485）", "#dfeaf7"),
        ("现场层", "传感器（温度 · 湿度 · 压差 · 流量 · CO2 · 电量）｜执行器（调节阀 · 风阀 · 变频器）", "#e8f0f9"),
    ]
    bx, bw = 0.5, 7.9
    top, bh, step = 7.30, 0.92, 1.10
    for i, (name, sub, fc) in enumerate(layers):
        y = top - i * step - bh
        box(ax, bx, y, bw, bh, fc=fc, ec=C_MAIN, lw=1.5)
        ax.text(bx + 0.30, y + bh * 0.52, name, fontsize=10.4, color="#16324f",
                weight="bold", ha="left", va="center", zorder=7)
        ax.text(bx + 1.72, y + bh * 0.52, sub, fontsize=7.7, color="#42566b",
                ha="left", va="center", zorder=7)
    # 层间上下行箭头（标签统一放到列下方，避免与框线相撞）
    for i in range(3):
        y1 = top - i * step - bh
        y2 = top - (i + 1) * step
        arrow(ax, (bx + 5.9, y1 - 0.02), (bx + 5.9, y2 + 0.02),
              color=C_MAIN, lw=1.5, ms=9)
    txt(ax, bx + 0.30, 2.86, "↓ 指令下行（设定值 / 启停）　　↑ 数据上行（状态 / 趋势 / 报警）",
        fs=7.6, color=C_GREY, ha="left")

    # 右侧三层时间尺度
    bands = [
        ("系统级优化", "10 min ~ 1 h", "冷机群控 · 最优启停 · 需量控制", "允许通信抖动", "#f2f7fd", C_MAIN, C_OK),
        ("设备级协调", "10 s ~ 10 min", "加减机 · 静压重设 · 阀位联动", "段内通信即可", "#fdf7ea", C_HL, C_HL),
        ("现场闭环", "1 ~ 10 s", "送风温度 PID · 房间温度 · 压差", "不允许依赖网络", "#fdf0ef", C_ACC, C_ACC),
    ]
    rx, rw = 8.75, 3.95
    b_top, b_bot, gap = 7.30, 3.08, 0.20
    bh2 = (b_top - b_bot - 2 * gap) / 3.0
    for i, (name, span, content, dep, fc, ec, dc) in enumerate(bands):
        y = b_top - i * (bh2 + gap) - bh2
        box(ax, rx, y, rw, bh2, fc=fc, ec=ec, lw=1.7, radius=0.11)
        txt(ax, rx + 0.24, y + bh2 - 0.30, name, fs=10.4, color=ec, weight="bold", ha="left")
        txt(ax, rx + rw - 0.22, y + bh2 - 0.32, span, fs=8.8, color=ec, weight="bold", ha="right")
        txt(ax, rx + 0.24, y + bh2 * 0.46, content, fs=7.6, color="#42566b", ha="left")
        txt(ax, rx + 0.24, y + 0.28, dep, fs=7.8, color=dc, weight="bold", ha="left")

    # 底部结论
    box(ax, 0.5, 1.48, 12.2, 1.24, fc="#f4f8fc", ec=C_MAIN, lw=1.5, radius=0.12)
    txt(ax, 0.80, 2.46, "结论：时间尺度越短，越不能依赖通信。",
        fs=10.2, color="#16324f", weight="bold", ha="left")
    txt(ax, 0.80, 2.06,
        "送风温度回路的控制周期预算只有 24 s，而 MS/TP 全点表刷新一次需 7.7 s —— 通信就吃掉 32%。",
        fs=8.6, color="#42566b", ha="left")
    txt(ax, 0.80, 1.74,
        "因此现场闭环必须由本地 DDC 完成，中央站只做监督与设定值下发（§2.7、§3.3）。",
        fs=8.6, color="#42566b", ha="left")
    txt(ax, 0.5, 1.10,
        "注：速率与周期均为「工程基准」量级，实际取值须按现场设备数量、点表规模与总线速率核算。",
        fs=7.6, color=C_GREY, ha="left")

    fig.savefig(os.path.join(OUT, "arch-four-layers.png"), bbox_inches="tight",
                facecolor="white", pad_inches=0.16)
    plt.close(fig)


# ============================================================
# 图 2：对象时间常数 → 控制周期；送风温度回路预算分解
# ============================================================
def fig2():
    h = 7.6
    fig = plt.figure(figsize=(W, h), dpi=140)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.42, 1.0], wspace=0.26,
                          left=0.035, right=0.985, top=0.855, bottom=0.115)
    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    fig.text(0.035, 0.955, "图 2　对象时间常数决定控制周期，通信延迟决定回路归属",
             fontsize=12.2, color="#16324f", weight="bold", ha="left")

    # ---------- 左：τ 范围条形图（对数轴） ----------
    objs = [
        ("风管静压", 1, 10, 1.0),
        ("水系统压差", 5, 30, 3.0),
        ("送风温度", 180, 300, 24.0),
        ("冷冻水供水温度", 300, 900, 60.0),
        ("房间温度", 1800, 7200, 300.0),
        ("冷机群控", 600, 1800, 900.0),
    ]
    ypos = np.arange(len(objs))[::-1]
    for y, (name, t1, t2, tctrl) in zip(ypos, objs):
        ax.barh(y, t2 - t1, left=t1, height=0.42, color="#cfe0f2",
                edgecolor=C_MAIN, linewidth=1.3, zorder=3)
        ax.plot([tctrl], [y], marker="D", markersize=9.5, color=C_ACC,
                markeredgecolor="white", markeredgewidth=1.1, zorder=6)
        ax.text(t2 * 1.30, y, "τ %g~%g s" % (t1, t2), fontsize=7.4,
                color="#42566b", va="center", ha="left", zorder=6)

    h_r = ax.axvline(7.7, color=C_ACC, linestyle="--", linewidth=1.9, zorder=5)
    h_g = ax.axvline(24.0, color=C_HL, linestyle=":", linewidth=2.0, zorder=5)
    ax.legend([h_r, h_g], ["MS/TP 全点表刷新 7.7 s", "送风温度控制周期预算 24 s"],
              fontsize=7.8, loc="upper right", framealpha=0.96,
              edgecolor="#c8d4e2", handlelength=2.0, borderpad=0.55,
              labelspacing=0.55)

    ax.set_xscale("log")
    ax.set_xlim(0.6, 200000)
    ax.set_ylim(-0.80, 5.75)
    ax.set_yticks(ypos)
    ax.set_yticklabels([o[0] for o in objs], fontsize=9.4, color="#16324f")
    ax.set_xlabel("时间尺度（s，对数刻度）　　浅蓝条 = 对象主导时间常数 τ 范围　　"
                  "红菱形 = 允许的控制周期上限 τ/10",
                  fontsize=8.2, color="#42566b", labelpad=7)
    ax.grid(axis="x", linestyle=":", color="#c8d4e2", linewidth=0.9, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c8d4e2")
    ax.tick_params(axis="x", labelsize=7.6, colors="#42566b")

    # ---------- 右：送风温度回路控制周期预算分解 ----------
    ax2.set_xlim(0, 11.4)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    ax2.text(0.0, 9.75, "送风温度回路：24 s 控制周期怎么花掉",
             fontsize=10.2, color="#16324f", weight="bold", ha="left")

    segs = [
        ("现场闭环（推荐）", [
            ("控制器计算", 1.0, "#2e5f96"),
            ("传感器 / 变送滞后", 5.0, "#4a83c0"),
            ("执行器小信号行程", 10.0, "#78a9d8"),
            ("通信分摊", 0.2, "#1f7a4d"),
        ], 16.2),
        ("中央站控制（不推荐）", [
            ("通信往返（全点表刷新）", 7.7, "#b3282d"),
            ("控制器计算", 1.0, "#2e5f96"),
            ("传感器 / 变送滞后", 5.0, "#4a83c0"),
            ("执行器小信号行程", 10.0, "#78a9d8"),
        ], 23.7),
    ]
    barw = 10.0
    for k, (title, parts, total) in enumerate(segs):
        y0 = 6.35 - k * 3.05
        ax2.text(0.0, y0 + 0.98, title, fontsize=9.2, color="#16324f",
                 weight="bold", ha="left")
        x = 0.0
        for name, val, color in parts:
            wseg = val / 24.0 * barw
            ax2.add_patch(Rectangle((x, y0), wseg, 0.72, facecolor=color,
                                    edgecolor="white", linewidth=1.2, zorder=3))
            if wseg > 1.45:
                ax2.text(x + wseg / 2, y0 + 0.36, "%.1fs" % val, fontsize=7.6,
                         color="white", weight="bold", ha="center", va="center", zorder=5)
            x += wseg
        ax2.plot([barw + 0.06, barw + 0.06], [y0 - 0.20, y0 + 0.94], color=C_ACC,
                 linewidth=2.0, zorder=6)
        ax2.text(barw + 0.22, y0 + 0.36, "24s", fontsize=8.2, color=C_ACC,
                 weight="bold", va="center", ha="left")
        rem = 24.0 - total
        ax2.text(0.0, y0 - 0.44, "已占用 %.1f s　→　余量 %.1f s" % (total, rem),
                 fontsize=8.2, color=(C_OK if rem > 5 else C_ACC), weight="bold", ha="left")

    # 图例（两行两列，避免右侧越界）
    leg_rows = [
        ([("通信开销", "#b3282d", 0.0), ("计算与传感", "#2e5f96", 3.05)], 0.66),
        ([("执行器行程", "#78a9d8", 0.0), ("通信占比极小（余量充足）", "#1f7a4d", 3.05)], 0.20),
    ]
    for row, yy in leg_rows:
        for name, color, lx in row:
            ax2.add_patch(Rectangle((lx, yy), 0.34, 0.34, facecolor=color,
                                    edgecolor="white", linewidth=0.8))
            ax2.text(lx + 0.46, yy + 0.17, name, fontsize=7.6, color="#42566b",
                     va="center", ha="left")

    fig.savefig(os.path.join(OUT, "loop-timescale.png"), bbox_inches="tight",
                facecolor="white", pad_inches=0.16)
    plt.close(fig)


# ============================================================
# 图 3：Trim-and-Respond 轨迹与风机功率
# ============================================================
def fig3():
    h = 7.5
    fig = plt.figure(figsize=(W, h), dpi=140)
    fig.text(0.022, 0.945, "图 3　Trim-and-Respond：静压设定值降下来，风机功率按 1.5 次幂跟着掉",
             fontsize=12.2, color="#16324f", weight="bold", ha="left")

    axp = fig.add_axes([0.078, 0.215, 0.845, 0.680])
    axq = axp.twinx()

    t = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40,
                  46, 52, 58, 64, 70, 78, 86, 94])
    sp = np.array([0.94, 1.00, 1.10, 1.25, 1.25, 1.31, 1.27, 1.23, 1.19, 1.15,
                   1.12, 1.08, 1.05, 1.02, 0.99, 0.96, 0.99, 0.95, 0.91, 0.86,
                   0.81, 0.75, 0.69, 0.65])
    power = (sp / 1.25) ** 1.5

    axp.plot(t, sp, color=C_MAIN, linewidth=2.6, marker="o", markersize=4.4,
             markerfacecolor="white", markeredgewidth=1.5, zorder=6,
             label="静压设定值（in.w.g.）")
    axq.plot(t, power, color=C_HL, linewidth=2.4, zorder=6,
             label="相对风机功率 P/P0")
    axq.fill_between(t, 0, power, color=C_HL, alpha=0.10, zorder=2)

    axp.set_xlim(-2, 96)
    axp.set_ylim(0.50, 1.46)
    axq.set_ylim(0.0, 1.30)
    axp.set_xlabel("距整定开始的时间（min）", fontsize=8.8, color="#42566b")
    axp.set_ylabel("静压设定值（in.w.g.）", fontsize=8.8, color=C_MAIN)
    axq.set_ylabel("相对风机功率 P/P0（无量纲）", fontsize=8.8, color=C_HL)
    axp.tick_params(labelsize=8.0, colors=C_MAIN)
    axq.tick_params(labelsize=8.0, colors=C_HL)
    axp.grid(axis="y", linestyle=":", color="#c8d4e2", linewidth=0.9, zorder=0)
    axp.spines["top"].set_visible(False)
    axq.spines["top"].set_visible(False)

    # 六个请求被限幅的那一步
    axp.annotate("R=6，期望 +0.24\n被 SP_res-max 限为 +0.15",
                 xy=(10, 1.31), xytext=(19.0, 1.415), fontsize=8.0, color=C_ACC,
                 weight="bold", va="center", ha="left",
                 arrowprops=dict(arrowstyle="-|>", color=C_ACC, linewidth=1.5,
                                 shrinkA=3, shrinkB=3))

    # 起调段请求数序列（放到下方空白区，避免与刻度挤在一起）
    axp.text(15.5, 0.60, "起调段请求数序列（每 2 min 一次）：R = 3 → 4 → 6 → 3 → 0",
             fontsize=8.0, color=C_GREY, ha="left", va="center", zorder=8,
             bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                       edgecolor="#c8d4e2", linewidth=1.0))

    # 终点标注
    axp.plot([94], [0.65], marker="o", markersize=8, color=C_ACC, zorder=8)
    axp.annotate("0.65 in.w.g.（相对设计静压 1.25）",
                 xy=(94, 0.65), xytext=(92, 0.94), fontsize=8.2, color=C_ACC,
                 weight="bold", va="center", ha="right",
                 arrowprops=dict(arrowstyle="-|>", color=C_ACC, linewidth=1.5,
                                 shrinkA=3, shrinkB=5))
    axq.plot([94], [power[-1]], marker="o", markersize=8, color=C_HL, zorder=8)
    axq.annotate("P/P0 = 0.375（省 62.5%）",
                 xy=(94, power[-1]), xytext=(92, 0.20), fontsize=8.4, color=C_HL,
                 weight="bold", va="center", ha="right",
                 arrowprops=dict(arrowstyle="-|>", color=C_HL, linewidth=1.5,
                                 shrinkA=3, shrinkB=5))

    h1, l1 = axp.get_legend_handles_labels()
    h2, l2 = axq.get_legend_handles_labels()
    axp.legend(h1 + h2, l1 + l2, fontsize=8.0, loc="upper right",
               framealpha=0.95, edgecolor="#c8d4e2")

    # 公式说明条（独立坐标区，不与绘图区重叠）
    axc = fig.add_axes([0.022, 0.030, 0.956, 0.125])
    axc.set_xlim(0, 10)
    axc.set_ylim(0, 10)
    axc.axis("off")
    box(axc, 0.0, -1.4, 10.0, 12.6, fc="#f4f8fc", ec=C_MAIN, lw=1.3, radius=0.22)
    axc.text(0.28, 6.6,
             "推导：管网上风量与静压近似 Q ∝ √ΔP，风机功率 P ∝ Q³，故 P/P0 = (SP/SP0)^1.5。",
             fontsize=8.4, color="#42566b", ha="left", va="center")
    axc.text(0.28, 2.6,
             "代入 0.65 / 1.25 得 (0.52)^1.5 = 0.375 —— 与 LBNL 实测的风机节电 40%~60% 量级一致。",
             fontsize=8.4, color="#42566b", ha="left", va="center")

    fig.savefig(os.path.join(OUT, "trim-respond.png"), facecolor="white")
    plt.close(fig)


# ============================================================
# 图 4：案例三改造投资回收排序
# ============================================================
def fig4():
    h = 7.9
    fig = plt.figure(figsize=(W, h), dpi=140)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.30, 1.0], wspace=0.34,
                          left=0.245, right=0.985, top=0.845, bottom=0.135)
    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    fig.text(0.035, 0.955, "图 4　1.2 万 m² 既有办公改造：先修后改，回收期从 0.5 年排到 4.5 年",
             fontsize=12.2, color="#16324f", weight="bold", ha="left")

    items = [
        ("① 清洗冷凝器 + 冷却塔整治", 8.0, 16.2, 0.5, "#1f7a4d"),
        ("② 治温差病（拆三通阀 + 调旁通）", 12.0, 9.5, 1.3, "#4a9e6f"),
        ("③ 变频 + 静压 T&R + 送风温度重设", 22.0, 14.7, 1.5, "#8bbf9f"),
        ("④ 末端加装室温调控装置", 18.0, 4.0, 4.5, "#c9d9e6"),
        ("⑤ 冷热源与机房能量计量", 4.0, 0.0, None, "#dfe5ec"),
        ("⑥ 监控系统改造（记录 1 年以上）", 26.0, 0.0, None, "#dfe5ec"),
    ]
    ypos = np.arange(len(items))[::-1]
    barh = 0.34

    for y, (name, inv, ret, pay, col) in zip(ypos, items):
        ax.barh(y + 0.20, inv, height=barh, color=col, edgecolor="white",
                linewidth=1.0, zorder=3)
        if ret > 0:
            ax.barh(y - 0.20, ret, height=barh, color=C_HL, edgecolor="white",
                    linewidth=1.0, alpha=0.92, zorder=3)
            ax.text(ret + 0.7, y - 0.20, "%.1f 万" % ret, fontsize=7.6,
                    color="#8a6608", va="center", ha="left", weight="bold", zorder=6)
        else:
            ax.text(0.7, y - 0.20, "仅间接收益（提供依据 / 可验证性）", fontsize=7.4,
                    color=C_GREY, va="center", ha="left", zorder=6)
        ax.text(inv + 0.7, y + 0.20, "%.0f 万" % inv, fontsize=7.6,
                color="#16324f", va="center", ha="left", weight="bold", zorder=6)

    ax.set_yticks(ypos)
    ax.set_yticklabels([i[0] for i in items], fontsize=8.5, color="#16324f")
    ax.set_xlim(0, 33)
    ax.set_ylim(-0.75, len(items) - 0.25)
    ax.set_xlabel("金额（万元）　深色 = 一次性投入，金色 = 年收益", fontsize=8.4,
                  color="#42566b")
    ax.grid(axis="x", linestyle=":", color="#c8d4e2", linewidth=0.9, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c8d4e2")
    ax.tick_params(axis="x", labelsize=7.8, colors="#42566b")

    # ---------- 右：回收期 ----------
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    ax2.text(0.0, 9.80, "投资回收期（年，越短越优先）",
             fontsize=10.2, color="#16324f", weight="bold", ha="left")

    pays = [i for i in items if i[3] is not None]
    short = ["① 清洗冷凝器", "② 治温差病", "③ 变频 + T&R", "④ 末端室温调控"]
    maxy = 5.0
    for k, ((name, inv, ret, pay, col), sn) in enumerate(zip(pays, short)):
        y0 = 7.55 - k * 1.42
        ax2.text(0.0, y0 + 0.62, sn, fontsize=8.4, color="#16324f", ha="left")
        wbar = pay / maxy * 8.0
        ax2.add_patch(Rectangle((0.0, y0), wbar, 0.46, facecolor=col,
                                edgecolor="white", linewidth=1.0, zorder=3))
        ax2.text(wbar + 0.16, y0 + 0.23, "%.1f 年" % pay, fontsize=8.4,
                 color="#16324f", weight="bold", va="center", ha="left", zorder=5)
    ax2.plot([0, 8.0], [1.62, 1.62], color="#c8d4e2", linewidth=1.2)
    ax2.text(0.0, 1.22, "①②③ 合计：投入 42 万，年收益 40.4 万",
             fontsize=8.6, color="#16324f", weight="bold", ha="left")
    ax2.text(0.0, 0.72, "回收期约 1.04 年（收益打 60% 折仍 < 1.7 年）",
             fontsize=8.6, color=C_OK, weight="bold", ha="left")
    ax2.text(0.0, 0.24, "④⑤⑥ 回收期偏长，但 ⑤⑥ 是「让收益可验证」的基础设施",
             fontsize=7.6, color=C_GREY, ha="left")

    fig.savefig(os.path.join(OUT, "retrofit-payback.png"), bbox_inches="tight",
                facecolor="white", pad_inches=0.16)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    print("done")
