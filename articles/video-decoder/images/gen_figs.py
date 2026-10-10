# -*- coding: utf-8 -*-
"""生成「视频解码器产品综述」配套矢量示意图（4 张）。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

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


def box(ax, x, y, w, h, fc="#eef3fb", ec="#2f5f96", lw=1.6, radius=0.14, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={radius}",
                                facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=2))


def txt(ax, x, y, s, fs=9.0, color="#1f2a37", weight="normal", ha="center", va="center", zorder=6):
    ax.text(x, y, s, fontsize=fs, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, linespacing=1.35)


def arrow(ax, p1, p2, color="#c0392b", lw=1.8, ls="-", ms=11, zorder=5, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                                 color=color, linewidth=lw, linestyle=ls,
                                 zorder=zorder, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def dashed(ax, pts, color="#6b7280", lw=1.5, zorder=5):
    """带白描边的折线，跨线仍可读。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    line, = ax.plot(xs, ys, color=color, linewidth=lw, linestyle="--", zorder=zorder)
    line.set_path_effects([pe.withStroke(linewidth=3.6, foreground="white")])


C_MAIN = "#2f5f96"
C_ACC = "#c0392b"
C_HL = "#b8860b"
C_OK = "#2e7d5b"
C_GREY = "#6b7280"
BG = "#eef3fb"


# ============================================================
# 图 1：从码流到像素的七段链路
# ============================================================
def fig1():
    H = 8.6
    fig, ax = newfig(H)
    txt(ax, W / 2, H - 0.45, "图 1　视频解码器：从码流到像素的七段链路",
        fs=13.5, weight="bold", color="#12263f")
    txt(ax, W / 2, H - 0.92, "前三段决定「能不能解出来」，第五段决定「摆成你要的样子」，第六七段决定「点得亮、点得稳」",
        fs=9.0, color=C_GREY)

    bw, gap = 1.30, 0.24
    x0 = (W - (7 * bw + 6 * gap)) / 2          # 1.33
    by, bh = 5.20, 2.10
    cx = [x0 + bw / 2 + i * (bw + gap) for i in range(7)]

    stages = [
        ("① 取流与信令", "SIP / RTSP\nONVIF 取流", "#e8f1fb", C_MAIN),
        ("② 解封装", "RTP 解包\nPS / TS 解析", "#e8f1fb", C_MAIN),
        ("③ 硬解码", "H.265 / H.264\nSVAC / AV1", "#fdecea", C_ACC),
        ("④ 图像后处理", "去隔行 · 缩放\nOSD 叠加", "#e8f1fb", C_MAIN),
        ("⑤ 拼控与开窗", "裁剪 · 图层\n预案切换", "#fdf5e3", C_HL),
        ("⑥ 输出编码", "HDMI / DP\nSDI 串行化", "#e8f5ee", C_OK),
        ("⑦ 显示终端", "LCD 拼接 / LED\n专业监视器", "#e8f5ee", C_OK),
    ]
    for i, (name, body, fc, ec) in enumerate(stages):
        box(ax, cx[i] - bw / 2, by, bw, bh, fc=fc, ec=ec, lw=1.7)
        txt(ax, cx[i], by + bh - 0.42, name, fs=9.0, weight="bold", color=ec)
        txt(ax, cx[i], by + 0.72, body, fs=8.0, color="#334e68")

    # 段间箭头
    for i in range(6):
        arrow(ax, (cx[i] + bw / 2 + 0.02, by + bh / 2),
              (cx[i + 1] - bw / 2 - 0.02, by + bh / 2), color=C_ACC, lw=1.9, ms=10)

    # 两侧输入/输出
    box(ax, 0.15, by + 0.45, 0.85, 1.20, fc="#eceff3", ec=C_GREY, lw=1.4)
    txt(ax, 0.575, by + 1.28, "网络", fs=8.4, weight="bold", color="#374151")
    txt(ax, 0.575, by + 0.78, "码流", fs=8.4, weight="bold", color="#374151")
    arrow(ax, (1.02, by + bh / 2), (x0 - 0.04, by + bh / 2), color=C_ACC, lw=1.9, ms=10)

    box(ax, 12.20, by + 0.45, 0.85, 1.20, fc="#eceff3", ec=C_GREY, lw=1.4)
    txt(ax, 12.625, by + 1.28, "屏幕", fs=8.4, weight="bold", color="#374151")
    txt(ax, 12.625, by + 0.78, "像素", fs=8.4, weight="bold", color="#374151")
    arrow(ax, (x0 + 7 * bw + 6 * gap + 0.04, by + bh / 2), (12.18, by + bh / 2),
          color=C_ACC, lw=1.9, ms=10)

    # 每段瓶颈
    necks = ["设备编码\n与鉴权", "丢包与\n时间戳", "像素吞吐率\n内存带宽",
             "缩放倍数\n图层数", "窗口数\n× 图层数", "链路速率\n与线材", "拼缝与\n屏体延迟"]
    for i, s in enumerate(necks):
        txt(ax, cx[i], by - 0.42, s, fs=7.8, color=C_GREY)

    # 三组括注
    groups = [(0, 3, "能不能解出来", C_ACC),
              (4, 4, "摆成你要的样子", C_HL),
              (5, 6, "点得亮、点得稳", C_OK)]
    gy = by - 1.55
    for a, b, label, col in groups:
        xa = cx[a] - bw / 2
        xb = cx[b] + bw / 2
        ax.plot([xa, xa, xb, xb], [gy + 0.22, gy, gy, gy + 0.22],
                color=col, linewidth=1.6, zorder=4)
        txt(ax, (xa + xb) / 2, gy - 0.30, label, fs=9.2, weight="bold", color=col)

    # 底部说明
    box(ax, 1.10, 2.30, W - 2.20, 1.00, fc="#fbfcfd", ec="#c8d3e0", lw=1.2, radius=0.10)
    txt(ax, 1.35, 2.80, "注", fs=8.4, weight="bold", color=C_MAIN, ha="left")
    txt(ax, 1.70, 2.80,
        "第 ③ 段的瓶颈通常不是算力而是内存带宽：帧间预测要反复读写参考帧，1080P@30 单路约需 326 MB/s，32 路约 10.4 GB/s。",
        fs=8.6, color="#334e68", ha="left")
    txt(ax, 1.70, 2.45,
        "这也是「当量换算只做上限判断、实际配置留 30% 余量」的物理来源——总线争抢、缓存失效与调度开销都要占位置。",
        fs=8.6, color="#334e68", ha="left")

    fig.savefig(os.path.join(OUT, "arch-pipeline.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================
# 图 2：解码当量换算 + 输出接口带宽对照
# ============================================================
def fig2():
    H = 10.4
    fig, ax = newfig(H)
    txt(ax, W / 2, H - 0.45, "图 2　解码当量换算与输出接口带宽对照",
        fs=13.5, weight="bold", color="#12263f")

    # ---------- 区块 A：解码当量 ----------
    txt(ax, 0.30, H - 1.05, "① 解码当量换算（1080P@30 = 62.2 Mpx/s 定义为 1 当量；条形长度 = 当量值）",
        fs=9.6, weight="bold", color=C_MAIN, ha="left")

    rows = [
        ("D1 704×576@25", 0.16, 200),
        ("720P@25", 0.37, 86),
        ("1080P@25", 0.83, 38),
        ("1080P@30（基准）", 1.00, 32),
        ("1080P@60", 2.00, 16),
        ("4MP 2560×1440@25", 1.48, 21),
        ("4K@25", 3.33, 9),
        ("4K@30", 4.00, 8),
        ("4K@60", 8.00, 4),
    ]
    lx, bx0 = 0.30, 3.05
    scale = 5.55 / 8.0            # 8.0 当量 -> 5.55 单位
    ytop, step = H - 1.60, 0.455
    for i, (name, eq, n) in enumerate(rows):
        y = ytop - i * step
        txt(ax, lx, y, name, fs=8.6, color="#1f2a37", ha="left")
        col = C_ACC if eq >= 3.3 else (C_HL if eq >= 1.9 else C_MAIN)
        ax.add_patch(Rectangle((bx0, y - 0.13), max(eq * scale, 0.035), 0.26,
                               facecolor=col, edgecolor="none", zorder=3))
        txt(ax, bx0 + max(eq * scale, 0.035) + 0.10, y, f"{eq:.2f}", fs=8.6,
            color=col, weight="bold", ha="left")
        txt(ax, bx0 + 6.35, y, f"32 当量机型约 {n} 路", fs=8.4, color="#334e68", ha="left")

    a_bottom = ytop - (len(rows) - 1) * step - 0.32
    txt(ax, lx, a_bottom,
        "推论：标称「32 路 1080P@30」的机器，接 4K@30 只有 8 路、接 4K@60 只有 4 路——不是虚标，是同一条管线按像素计费。",
        fs=8.8, color="#7d2a22", ha="left", weight="bold")

    # ---------- 区块 B：接口带宽 ----------
    txt(ax, 0.30, a_bottom - 0.62, "② 输出接口带宽对照（链路速率 = 像素时钟 × 每像素比特数 × 10/8）",
        fs=9.6, weight="bold", color=C_MAIN, ha="left")

    bars = [
        ("1080p60 8bit", 148.5, 4.455, "可行"),
        ("4K30 8bit", 297.0, 8.91, "可行（占 HDMI 1.4 的 87%）"),
        ("4K60 8bit 4:4:4", 594.0, 17.82, "可行，但占 HDMI 2.0 的 99%"),
        ("4K60 12bit 4:2:0", 594.0, 13.37, "可行（占 74%）"),
        ("4K60 10bit 4:2:2", 594.0, 14.85, "可行（占 82%）"),
        ("4K60 10bit 4:4:4", 594.0, 22.28, "超出 HDMI 2.0"),
    ]
    bx0b, sc = 3.05, 6.10 / 24.0     # 24 Gbps -> 6.10 单位
    ytopb, stepb = a_bottom - 1.18, 0.50
    for i, (name, pclk, rate, verdict) in enumerate(bars):
        y = ytopb - i * stepb
        txt(ax, lx, y, name, fs=8.6, color="#1f2a37", ha="left")
        txt(ax, lx + 1.62, y, f"{pclk:.0f} MHz", fs=8.0, color=C_GREY, ha="left")
        bad = "超出" in verdict
        col = "#b8860b" if "99%" in verdict else (C_ACC if bad else C_OK)
        ax.add_patch(Rectangle((bx0b, y - 0.13), rate * sc, 0.26,
                               facecolor=col, edgecolor="none", zorder=3))
        txt(ax, bx0b + rate * sc + 0.10, y, f"{rate:.2f} Gbps", fs=8.6,
            color=col, weight="bold", ha="left")
        txt(ax, bx0b + 7.00, y, verdict, fs=8.4, color=col, ha="left")

    # 上限参考线（标签放线下端，避开区块标题）
    for lim, lab, col in [(10.2, "HDMI 1.4 上限 10.2", C_MAIN), (18.0, "HDMI 2.0 上限 18.0", C_ACC)]:
        xl = bx0b + lim * sc
        yb_line = ytopb - (len(bars) - 1) * stepb - 0.32
        ax.plot([xl, xl], [ytopb + 0.26, yb_line], color=col, linewidth=1.6,
                linestyle="--", zorder=5)
        txt(ax, xl, yb_line - 0.28, lab, fs=8.4, color=col, weight="bold")

    b_bottom = ytopb - (len(bars) - 1) * stepb - 1.00
    box(ax, 0.30, b_bottom - 1.30, W - 0.60, 1.15, fc="#fbfcfd", ec="#c8d3e0", lw=1.2, radius=0.10)
    txt(ax, 0.55, b_bottom - 0.48, "注", fs=8.4, weight="bold", color=C_MAIN, ha="left")
    txt(ax, 0.90, b_bottom - 0.48,
        "4K@60 8 bit 贴着 HDMI 2.0 天花板跑，余量仅 1%：线材不是耗材，是主材，超过 5 m 必须用有源线或光纤 HDMI。",
        fs=8.6, color="#334e68", ha="left")
    txt(ax, 0.90, b_bottom - 0.85,
        "DP 1.4（HBR3）有效带宽 25.92 Gbps，比 HDMI 2.0 的 14.4 Gbps 高 80%——同一块 5K 级大屏，DP 一口能带，HDMI 2.0 要拆两个口。",
        fs=8.6, color="#334e68", ha="left")

    fig.savefig(os.path.join(OUT, "throughput-budget.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================
# 图 3：端到端延迟分解 + GOP 起播等待
# ============================================================
def fig3():
    H = 10.2
    fig, ax = newfig(H)
    txt(ax, W / 2, H - 0.45, "图 3　端到端延迟分解与 GOP 起播等待",
        fs=13.5, weight="bold", color="#12263f")

    # ---------- 区块 A：延迟分解 ----------
    txt(ax, 0.30, H - 1.05, "① 端到端延迟＝六段相加（横轴为毫秒，条为常见取值区间，◆ 为典型值）",
        fs=9.6, weight="bold", color=C_MAIN, ha="left")

    items = [
        ("网络传输", 1, 30, 5, C_OK, "局域网 <1 ms；跨城 10~30 ms"),
        ("抖动缓冲", 100, 500, 300, C_ACC, "最大人为可调项，与延迟线性相关"),
        ("解码", 33, 100, 66, C_MAIN, "硬解通常 1 帧；软解受调度影响"),
        ("后处理", 30, 40, 33, C_MAIN, "去隔行、缩放，基本固定"),
        ("图层合成", 30, 40, 33, C_MAIN, "与窗口数相关"),
        ("屏体处理", 5, 20, 12, C_HL, "电视 MEMC 另加，必须关掉"),
    ]
    lx, bx0 = 0.30, 2.95
    sc = 8.30 / 520.0
    ytop, step = H - 1.60, 0.52
    for i, (name, lo, hi, typ, col, note) in enumerate(items):
        y = ytop - i * step
        txt(ax, lx, y, name, fs=8.8, color="#1f2a37", ha="left", weight="bold")
        ax.add_patch(Rectangle((bx0 + lo * sc, y - 0.13), (hi - lo) * sc, 0.26,
                               facecolor=col, edgecolor="none", alpha=0.85, zorder=3))
        ax.plot(bx0 + typ * sc, y, marker="D", markersize=5.2, color="#12263f", zorder=6)
        # 宽条把数值放条内白字，窄条放右侧；屏体行数值并入延伸条右侧标注
        if i == 5:
            pass
        elif (hi - lo) * sc > 1.25:
            txt(ax, bx0 + (lo + hi) / 2 * sc, y, f"{lo}~{hi} ms", fs=8.4,
                color="white", ha="center", weight="bold", zorder=7)
        else:
            txt(ax, bx0 + hi * sc + 0.14, y, f"{lo}~{hi} ms", fs=8.4,
                color=col, ha="left", weight="bold")
        txt(ax, 11.30, y, note, fs=8.2, color=C_GREY, ha="left")

    # 电视 MEMC 延伸条
    yv = ytop - 5 * step
    ax.add_patch(Rectangle((bx0 + 20 * sc, yv - 0.13), (120 - 20) * sc, 0.26,
                           facecolor="#ffffff", edgecolor=C_HL, hatch="///", linewidth=1.1, zorder=3))
    txt(ax, bx0 + 120 * sc + 0.16, yv, "5~20 ms，电视 MEMC 另加 50~100 ms",
        fs=8.2, color=C_HL, ha="left", weight="bold")

    # 刻度
    ax.plot([bx0, bx0 + 520 * sc], [ytop - 5 * step - 0.42] * 2, color="#c8d3e0", linewidth=1.2, zorder=2)
    for t in [0, 100, 200, 300, 400, 500]:
        ax.plot([bx0 + t * sc] * 2, [ytop - 5 * step - 0.42, ytop - 5 * step - 0.54],
                color="#c8d3e0", linewidth=1.0, zorder=2)
        txt(ax, bx0 + t * sc, ytop - 5 * step - 0.72, str(t), fs=8.0, color=C_GREY)

    a_bottom = ytop - 5 * step - 1.05
    txt(ax, lx, a_bottom,
        "典型合计 250~750 ms。云台控制是往返延迟（2 倍 + 机械响应 200~500 ms），这是上墙项目最常见的体验投诉来源。",
        fs=8.8, color="#7d2a22", ha="left", weight="bold")

    # ---------- 区块 B：GOP ----------
    txt(ax, 0.30, a_bottom - 0.62, "② 起播＝等到下一个 IDR：这笔账决定了「上墙先黑两秒」",
        fs=9.6, weight="bold", color=C_MAIN, ha="left")

    fy, fh = a_bottom - 2.75, 0.62
    cw, cg = 0.44, 0.07
    n_cell = 15
    fx0 = 1.20
    for i in range(n_cell):
        is_i = (i == 0 or i == n_cell - 1)
        ax.add_patch(Rectangle((fx0 + i * (cw + cg), fy), cw, fh,
                               facecolor="#fdecea" if is_i else "#eceff3",
                               edgecolor=C_ACC if is_i else "#9aa7b4", linewidth=1.4, zorder=3))
        txt(ax, fx0 + i * (cw + cg) + cw / 2, fy + fh / 2, "I" if is_i else "P",
            fs=8.6, weight="bold", color=C_ACC if is_i else "#5b6672")

    # 接入点
    join_i = 5
    jx = fx0 + join_i * (cw + cg) + cw / 2
    ax.plot([jx, jx], [fy + fh + 0.95, fy + fh + 0.06], color=C_OK, linewidth=1.6, zorder=5)
    ax.plot(jx, fy + fh + 0.06, marker="v", markersize=7, color=C_OK, zorder=6)
    txt(ax, jx, fy + fh + 1.18, "解码器接入这一路", fs=8.6, color=C_OK, weight="bold")

    # 等待跨度括线
    wx1 = jx
    wx2 = fx0 + (n_cell - 1) * (cw + cg)
    wy = fy - 0.30
    ax.plot([wx1, wx1, wx2, wx2], [wy + 0.20, wy, wy, wy + 0.20], color=C_ACC, linewidth=1.6, zorder=4)
    txt(ax, (wx1 + wx2) / 2, wy - 0.32, "要等到下一个 I 帧才出画面", fs=8.8, color=C_ACC, weight="bold")

    # GOP 跨度括线
    gy2 = fy + fh + 0.22
    gx1 = fx0
    gx2 = fx0 + (n_cell - 1) * (cw + cg) + cw
    ax.plot([gx1, gx1, gx2, gx2], [gy2 + 0.20, gy2, gy2, gy2 + 0.20], color=C_MAIN, linewidth=1.5, zorder=4)
    txt(ax, (gx1 + gx2) / 2, gy2 + 0.42, "GOP（两个 IDR 之间的一组帧）", fs=8.6, color=C_MAIN, weight="bold")

    # 右侧算式
    bx, byy, bww, bhh = 9.55, fy - 0.85, 3.35, 2.40
    box(ax, bx, byy, bww, bhh, fc="#fbfcfd", ec="#c8d3e0", lw=1.2, radius=0.10)
    txt(ax, bx + bww / 2, byy + bhh - 0.32, "首帧等待时间", fs=9.0, weight="bold", color=C_MAIN)
    txt(ax, bx + bww / 2, byy + bhh - 0.78, "T(first) ≤ N(GOP) / f", fs=9.4, color=C_ACC, weight="bold")
    txt(ax, bx + 0.18, byy + 0.72,
        "25 fps、GOP = 50 帧\n最长等 2.0 s\n\nGOP 压到 25 帧\n最长等 1.0 s\n代价：码率 +5%~15%",
        fs=8.4, color="#334e68", ha="left", va="center")

    txt(ax, 0.30, byy - 0.45,
        "对策：把摄像机 GOP 统一压到 1 s 以内，或让解码器主动强制请求 I 帧；轮巡周期必须大于「首帧 + 稳定时间」。",
        fs=8.8, color="#7d2a22", ha="left", weight="bold")

    fig.savefig(os.path.join(OUT, "latency-gop.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ============================================================
# 图 4：落地七步
# ============================================================
def fig4():
    H = 9.4
    fig, ax = newfig(H)
    txt(ax, W / 2, H - 0.45, "图 4　视频上墙项目落地七步（第 3、4 步返工成本最高，必须前置于设备采购）",
        fs=13.0, weight="bold", color="#12263f")

    bw, gap = 1.30, 0.24
    x0 = (W - (7 * bw + 6 * gap)) / 2
    by, bh = 5.55, 2.30
    cx = [x0 + bw / 2 + i * (bw + gap) for i in range(7)]

    steps = [
        ("1 定来源与协议", "来源清单\n平台版本\n协议类型", "#e8f1fb", C_MAIN),
        ("2 定分辨率帧率", "主/子码流\n分辨率 帧率\nGOP 长度", "#e8f1fb", C_MAIN),
        ("3 定屏体参数", "单元尺寸\n物理分辨率\n拼缝/点间距", "#fdf5e3", C_HL),
        ("4 算输出口与线材", "逻辑分辨率\n每口占用率\n线缆等级", "#fdf5e3", C_HL),
        ("5 开窗与预案", "窗口数\n图层数\n预案数", "#e8f1fb", C_MAIN),
        ("6 调延迟与轮巡", "抖动缓冲\n屏体后处理\n轮巡周期", "#e8f1fb", C_MAIN),
        ("7 验收与压测", "点对点测试\n72h 压测\n弹窗时间", "#e8f5ee", C_OK),
    ]
    for i, (name, body, fc, ec) in enumerate(steps):
        lw = 2.4 if i in (2, 3) else 1.6
        box(ax, cx[i] - bw / 2, by, bw, bh, fc=fc, ec=ec, lw=lw)
        txt(ax, cx[i], by + bh - 0.40, name, fs=8.8, weight="bold", color=ec)
        txt(ax, cx[i], by + 0.72, body, fs=8.0, color="#334e68")

    for i in range(6):
        arrow(ax, (cx[i] + bw / 2 + 0.02, by + bh / 2),
              (cx[i + 1] - bw / 2 - 0.02, by + bh / 2), color=C_ACC, lw=1.9, ms=10)

    # 高亮标记
    for i in (2, 3):
        txt(ax, cx[i], by + bh + 0.30, "返工成本最高", fs=8.4, weight="bold", color=C_HL)
    txt(ax, (cx[2] + cx[3]) / 2, by + bh + 0.78, "屏买了不能改，口不够要加卡",
        fs=8.6, color="#7d5a12", weight="bold")

    # 异常分支：第 7 步验收不通过 -> 回到第 3 步
    ych = by - 0.95
    dashed(ax, [(cx[6], by - 0.04), (cx[6], ych), (cx[2], ych), (cx[2], by - 0.04)],
           color=C_ACC, lw=1.6)
    ax.add_patch(FancyArrowPatch((cx[2], ych + 0.02), (cx[2], by - 0.06),
                                 arrowstyle="-|>", mutation_scale=10,
                                 color=C_ACC, linewidth=1.6, zorder=6, shrinkA=0, shrinkB=0))
    txt(ax, (cx[2] + cx[6]) / 2, ych + 0.34, "验收不通过（掉帧 / 点不亮 / 轮巡黑屏）→ 回到第 3 步重新核算",
        fs=8.8, color=C_ACC, weight="bold")

    # 底部说明
    box(ax, 0.90, 2.95, W - 1.80, 1.35, fc="#fbfcfd", ec="#c8d3e0", lw=1.2, radius=0.10)
    txt(ax, 1.15, 3.90, "判据", fs=8.4, weight="bold", color=C_MAIN, ha="left")
    txt(ax, 1.55, 3.90,
        "把「满配连续运行 72 小时无掉帧、无重启」写进验收条款，比任何参数表都更能筛出稳定性差距。",
        fs=8.8, color="#334e68", ha="left")
    txt(ax, 1.15, 3.47, "判据", fs=8.4, weight="bold", color=C_MAIN, ha="left")
    txt(ax, 1.55, 3.47,
        "规格书必须单列「最大合成窗口数、单口分辨率帧率上限、编码格式清单、上墙延迟、冗余要求」五项，只写解码路数一定招到纯解码机型。",
        fs=8.8, color="#334e68", ha="left")
    txt(ax, 1.15, 3.10, "判据", fs=8.4, weight="bold", color=C_MAIN, ha="left")
    txt(ax, 1.55, 3.10,
        "输出口一律锁死分辨率（不依赖 EDID 协商），上电顺序固定为「先屏后设备」，可消除绝大多数「时好时坏的假故障」。",
        fs=8.8, color="#334e68", ha="left")

    fig.savefig(os.path.join(OUT, "flow-deploy.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    for f in ["arch-pipeline.png", "throughput-budget.png", "latency-gop.png", "flow-deploy.png"]:
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p))
