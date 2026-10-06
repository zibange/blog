# -*- coding: utf-8 -*-
"""人脸识别终端 · 配图生成（4 张矢量示意图）
字体：Microsoft YaHei（注意：U+2713 等符号无字形，一律用 [符合] 之类 ASCII 替代）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
LW = 1.6
C_MAIN = "#1F4E79"
C_ACC = "#C0504D"
C_GRN = "#2E7D52"
C_PUR = "#6A4A9C"
C_GOLD = "#B8860B"
C_FILL = "#EAF1F8"
C_FILL2 = "#FBEDEC"
C_FILL3 = "#EAF4EE"
C_GREY = "#5A5A5A"


def box(ax, x, y, w, h, text, fc=C_FILL, ec=C_MAIN, fs=10.5, tc="#1A1A1A", bold=False, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.010,rounding_size=0.03",
                                linewidth=LW, edgecolor=ec, facecolor=fc, zorder=z))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, zorder=z + 1, fontweight="bold" if bold else "normal", linespacing=1.45)


def arrow(ax, x1, y1, x2, y2, color=C_MAIN, ls="-", lw=LW, rad=0.0, ms=11):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
                                 linewidth=lw, color=color, linestyle=ls, zorder=5,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1))


def base(ax, W=13.2, H=8.6):
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    ax.set_aspect("equal")


# ================================================================ 图1 内部流水线
def fig_arch():
    fig, ax = plt.subplots(figsize=(13.2, 8.6), dpi=110)
    base(ax)
    ax.text(6.6, 8.20, "图 1  人脸识别终端内部流水线与对外接口",
            ha="center", fontsize=14.5, fontweight="bold", color="#1A1A1A")
    ax.text(6.6, 7.78, "从光子到继电器：六段流水 + 三类对外接口（功能分层示意，非厂商框图）",
            ha="center", fontsize=10.2, color=C_GREY)

    # ---- 左：光学输入
    box(ax, 0.30, 6.62, 2.30, 0.92, "光学输入\nRGB 摄像头 + 红外摄像头\n（可选 3D 结构光 / ToF）",
        fc="#FFF6E5", ec=C_GOLD, fs=9.4)
    box(ax, 0.30, 5.55, 2.30, 0.82, "补光与曝光控制\n850 / 940 nm 红外 LED\n宽动态 WDR ≥ 120 dB",
        fc="#FFF6E5", ec=C_GOLD, fs=9.2)

    # ---- 中：六段流水（2 列 x 3 行）
    X1, X2 = 2.90, 5.55
    stages = [
        (X1, 6.62, "1  图像预处理\nISP · 宽动态 · 降噪 · ROI", C_FILL, C_MAIN),
        (X2, 6.62, "2  活体检测 PAD\n纹理 / 深度 / 微动 / 反射", C_FILL2, C_ACC),
        (X1, 5.55, "3  检测与关键点\n人脸框 + 5/68/106 点", C_FILL, C_MAIN),
        (X2, 5.55, "4  对齐与归一化\n仿射对齐 · 裁 112x112", C_FILL, C_MAIN),
        (X1, 4.48, "5  特征提取\nCNN -> 512 维 embedding", C_FILL3, C_GRN),
        (X2, 4.48, "6  比对与决策\n余弦相似度 · 1:1 / 1:N", C_FILL, C_MAIN),
    ]
    BW, BH = 2.60, 0.92
    for x, y, t, fc, ec in stages:
        box(ax, x, y, BW, BH, t, fc=fc, ec=ec, fs=9.4)

    # 流水箭头（蛇形）
    arrow(ax, X1 + BW, 7.08, X2, 7.08)                       # 1 -> 2
    arrow(ax, X2 + BW / 2, 6.62, X2 + BW / 2, 6.47)          # 2 -> 4
    arrow(ax, X2, 6.01, X1 + BW, 6.01)                       # 4 -> 3
    arrow(ax, X1 + BW / 2, 5.55, X1 + BW / 2, 5.40)          # 3 -> 5
    arrow(ax, X1 + BW, 4.94, X2, 4.94)                       # 5 -> 6

    # 光学 -> 预处理
    arrow(ax, 2.60, 7.08, X1, 7.20)
    arrow(ax, 2.60, 5.96, X1, 6.74, ls="--", color=C_GOLD)

    # ---- 右上：对外接口
    box(ax, 8.45, 6.05, 4.45, 1.50,
        "对外接口（按门禁主机能力多选一或全配）\n"
        "继电器干接点 NO/NC · 韦根 Wiegand 26/34\n"
        "RS-485 / OSDP · RJ45（HTTP / SDK / MQTT）\n"
        "人机反馈：LCD 提示 · 语音 · 抓拍留证",
        fc="#E8F2FB", ec=C_MAIN, fs=9.3)
    arrow(ax, 8.15, 5.35, 8.45, 6.35, color=C_GRN)

    # ---- 右中：本地特征库
    box(ax, 8.45, 4.48, 4.45, 0.92,
        "本地特征库（离线可用）\n"
        "5 万条 x 512 维 float32 = 约 98 MB · 常驻内存",
        fc="#F6F2FB", ec=C_PUR, fs=9.3)
    arrow(ax, 8.45, 4.94, 8.15, 4.94, color=C_PUR, ls="--")
    arrow(ax, 8.15, 4.94, 8.45, 4.94, color=C_PUR, ls="--")

    # ---- 底部：验收口径
    box(ax, 0.30, 2.30, 12.60, 1.42, "", fc="#FAFAFA", ec="#C8C8C8", z=1)
    ax.text(0.55, 3.34, "验收口径（GA/T 1093-2023 第 6 章，摘录）", fontsize=10.8,
            fontweight="bold", color="#1A1A1A")
    items = [
        "辨认模式：FAR ≤ 1% 时 FRR ≤ 5%",
        "确认模式：FAR ≤ 0.1% 时 FRR ≤ 2%",
        "注册失败率 ≤ 0.1%",
        "响应时间 ≤ 1 s（活体关）/ ≤ 3 s（活体开）",
        "防照片攻击失败率 ≤ 5%",
        "防视频攻击失败率 ≤ 5%",
    ]
    for i, t in enumerate(items):
        r, c = divmod(i, 3)
        ax.text(0.68 + c * 4.20, 3.02 - r * 0.48, "· " + t, fontsize=9.4, color="#333333")
    ax.text(0.30, 1.92, "合规底线：只存特征不存原图 · 传输与存储加密 · 单独同意与最小必要（GB/T 41819-2022 / GB/T 35273-2020）",
            fontsize=9.4, color=C_ACC)
    ax.text(0.30, 1.48, "注：本图为功能分层示意，各厂商内部实现的顺序与合并方式不同；框内数值取自公开标准条款或工程基准，不构成任何型号的承诺指标。",
            fontsize=8.8, color=C_GREY)

    fig.savefig(os.path.join(OUT, "arch-pipeline.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ================================================================ 图2 阈值与 FAR/FRR
def fig_threshold():
    from math import erf, sqrt, pi, exp
    Phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
    Q = lambda x: 1 - Phi(x)
    pdf = lambda x, m, s: exp(-0.5 * ((x - m) / s) ** 2) / (s * sqrt(2 * pi))

    mu1, s1 = 0.72, 0.08
    mu0, s0 = 0.32, 0.10
    tau = 0.60

    fig = plt.figure(figsize=(13.2, 8.8), dpi=110)
    ax1 = fig.add_axes([0.070, 0.430, 0.545, 0.430])
    ax2 = fig.add_axes([0.685, 0.430, 0.290, 0.430])
    ax3 = fig.add_axes([0.070, 0.070, 0.905, 0.275])

    fig.text(0.5, 0.955, "图 2  相似度阈值如何同时决定误识与拒识（双高斯演示模型）",
             ha="center", fontsize=14.5, fontweight="bold")
    fig.text(0.5, 0.912, "类内与类间分布的重叠区，是全部「安全 vs 顺滑」矛盾的来源：阈值左移放行多也误识多，右移安全但拒识多",
             ha="center", fontsize=10.0, color=C_GREY)

    xs = np.linspace(0.0, 1.05, 900)
    ax1.plot(xs, [pdf(x, mu0, s0) for x in xs], color=C_ACC, lw=2.2,
             label=f"类间（不同人）　mu={mu0}, sigma={s0}")
    ax1.plot(xs, [pdf(x, mu1, s1) for x in xs], color=C_MAIN, lw=2.2,
             label=f"类内（同一人）　mu={mu1}, sigma={s1}")
    ax1.fill_between(xs, 0, [pdf(x, mu0, s0) for x in xs], where=xs >= tau, color=C_ACC, alpha=0.30)
    ax1.fill_between(xs, 0, [pdf(x, mu1, s1) for x in xs], where=xs <= tau, color=C_MAIN, alpha=0.30)
    ax1.axvline(tau, color="#333333", lw=2.0, ls="--")
    ax1.text(tau + 0.018, 5.05, f"阈值 tau = {tau:.2f}", fontsize=10.5, fontweight="bold")
    ax1.annotate("FAR　把别人认成你", xy=(0.86, 0.30), xytext=(0.72, 1.55),
                 fontsize=9.8, color=C_ACC, ha="center",
                 arrowprops=dict(arrowstyle="-|>", color=C_ACC, lw=1.2))
    ax1.annotate("FRR　把自己拒之门外", xy=(0.46, 0.28), xytext=(0.30, 1.55),
                 fontsize=9.8, color=C_MAIN, ha="center",
                 arrowprops=dict(arrowstyle="-|>", color=C_MAIN, lw=1.2))
    ax1.set_xlabel("余弦相似度 s", fontsize=10.5)
    ax1.set_ylabel("概率密度", fontsize=10.5)
    ax1.set_xlim(0, 1.05)
    ax1.set_ylim(0, 5.7)
    ax1.legend(fontsize=9.3, loc="upper left", framealpha=0.95)
    ax1.grid(alpha=0.22, ls=":")

    taus = np.linspace(0.35, 0.92, 400)
    ax2.plot(taus, [Q((t - mu0) / s0) * 100 for t in taus], color=C_ACC, lw=2.2, label="FAR")
    ax2.plot(taus, [Phi((t - mu1) / s1) * 100 for t in taus], color=C_MAIN, lw=2.2, label="FRR")
    ax2.set_yscale("log")
    ax2.set_ylim(1e-3, 130)
    ax2.axvline(tau, color="#333333", lw=1.6, ls="--")
    ax2.set_xlabel("阈值 tau", fontsize=10.5)
    ax2.set_ylabel("比率 %（对数轴）", fontsize=10.5)
    ax2.legend(fontsize=10, loc="center right", framealpha=0.95)
    ax2.grid(alpha=0.22, ls=":")

    ax3.axis("off")
    taus_tab = [0.50, 0.55, 0.60, 0.62, 0.65, 0.70]
    rows = [[f"{t:.2f}", f"{Q((t-mu0)/s0)*100:.4f}%", f"{Phi((t-mu1)/s1)*100:.2f}%",
             f"{100-Phi((t-mu1)/s1)*100:.2f}%"] for t in taus_tab]
    tab = ax3.table(cellText=rows,
                    colLabels=["阈值 tau", "FAR（误识）", "FRR（拒识）", "通过率 = 1 - FRR"],
                    cellLoc="center", loc="upper left", bbox=[0.002, 0.02, 0.415, 0.92])
    tab.auto_set_font_size(False)
    tab.set_fontsize(9.5)
    for (r, c), cell in tab.get_celld().items():
        cell.set_edgecolor("#BBBBBB")
        if r == 0:
            cell.set_facecolor(C_MAIN)
            cell.set_text_props(color="white", fontweight="bold")
        elif r == 3:
            cell.set_facecolor("#FBEDEC")

    ax3.text(0.465, 0.93, "两条硬结论（演示模型下）", fontsize=11.4, fontweight="bold", color="#1A1A1A")
    ax3.text(0.465, 0.72,
             "1.  阈值从 0.55 抬到 0.65：FAR 由 1.07% 降到 0.048%（改善 22 倍），\n"
             "     FRR 却由 1.68% 升到 19.08%，通过率从 98.3% 跌到 80.9%。\n"
             "     —— 更安全永远买不到更顺滑，两者只能换，不能同时要。",
             fontsize=9.8, color="#333333", va="top", linespacing=1.65)
    ax3.text(0.465, 0.20,
             "2.  等错误率 EER 约 1.31%（tau 约 0.542）。真实商用算法 EER 远低于此；\n"
             "     本模型只用来演示「阈值—代价」的定量权衡方向，不是任何产品的精度承诺。",
             fontsize=9.8, color=C_GREY, va="top", linespacing=1.65)

    fig.savefig(os.path.join(OUT, "threshold-far-frr.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ================================================================ 图3 镜头几何
def fig_lens():
    fig = plt.figure(figsize=(13.2, 7.6), dpi=110)
    axL = fig.add_axes([0.045, 0.335, 0.425, 0.520])
    axR = fig.add_axes([0.545, 0.155, 0.425, 0.660])

    fig.text(0.5, 0.945, "图 3  焦距—识别距离—瞳距像素 的几何换算",
             ha="center", fontsize=14.5, fontweight="bold")
    fig.text(0.5, 0.898, "关键结论：需求像素密度一旦定死，视场宽度就定死了；焦距只决定「这个视场摆在几米处」",
             ha="center", fontsize=10.0, color=C_GREY)

    # ---------- 左：几何示意（同一距离、两种焦距）
    axL.set_xlim(-0.45, 4.75)
    axL.set_ylim(-0.35, 3.45)
    axL.axis("off")
    axL.set_aspect("equal")
    d = 3.2
    axL.add_patch(Rectangle((-0.30, 1.05), 0.30, 0.72, facecolor=C_MAIN, edgecolor="none"))
    axL.text(-0.15, 0.88, "终端\n(镜头 + 传感器)", ha="center", va="top", fontsize=9.2, color=C_MAIN)

    for (wfov, col) in [(2.08, C_MAIN), (1.04, C_GOLD)]:
        h = wfov / 2
        axL.plot([0, d], [1.41 + h, 1.41 + h], color=col, lw=1.6)
        axL.plot([0, d], [1.41 - h, 1.41 - h], color=col, lw=1.6)
        axL.plot([d, d], [1.41 - h, 1.41 + h], color=col, lw=2.6)
        axL.plot([0], [1.41], marker="o", ms=4, color=col)
    axL.annotate("", xy=(d, 1.41), xytext=(0, 1.41),
                 arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.3))
    axL.text(d / 2, 1.52, "同一站位 d", ha="center", fontsize=9.6, fontweight="bold")

    axL.text(0.05, 3.20, "同一位置、同一距离：焦距翻倍 -> 视场减半、脸变大", fontsize=9.4, color="#333333")
    axL.text(3.34, 2.62, "f = 4 mm\n视场 2.08 m", fontsize=9.4, color=C_MAIN, fontweight="bold")
    axL.text(3.34, 0.28, "f = 8 mm\n视场 1.04 m", fontsize=9.4, color=C_GOLD, fontweight="bold")

    # ---------- 右侧换算说明（独立于坐标区，避免压字）
    fig.text(0.045, 0.272, "换算式（1920 px 宽 / 1/2.8 型 sensor，宽约 5.0 mm）",
             fontsize=9.8, fontweight="bold", color="#1A1A1A")
    fig.text(0.045, 0.228, "N_px = W_px · W_real · f / ( d · W_sensor )", fontsize=10.2, color=C_ACC)
    fig.text(0.045, 0.186, "d = 0.416 x f(mm)　（瞳距 0.065 m、目标 60 px）", fontsize=10.2, color=C_ACC)
    fig.text(0.045, 0.138, "视场宽 W_FOV = 1920 x 0.065 / 60 = 2.08 m，与焦距无关；焦距越长，同样清晰度站得越远，但水平视场角越窄。",
             fontsize=9.3, color="#333333")
    fig.text(0.045, 0.096, "焦距 2.8 / 4 / 6 / 8 mm 对应识别距离约 1.16 / 1.66 / 2.50 / 3.33 m，水平视场角约 84° / 64° / 45° / 35°。",
             fontsize=9.3, color="#333333")

    # ---------- 右：瞳距像素 vs 距离
    dd = np.linspace(0.3, 4.2, 500)
    Wpx, Ws, pup = 1920, 5.0e-3, 0.065
    for fmm, col in [(2.8, "#8FAADC"), (4.0, C_MAIN), (6.0, "#14304A"), (8.0, C_GOLD)]:
        f = fmm / 1000
        npx = Wpx * pup * f / (dd * Ws)
        axR.plot(dd, npx, color=col, lw=2.0, label=f"f = {fmm} mm")
        d60 = Wpx * pup * f / (60 * Ws)
        if d60 <= 4.2:
            axR.plot([d60], [60], marker="o", ms=7, color=col, zorder=5)
            axR.annotate(f"{d60:.2f} m", xy=(d60, 60), xytext=(d60 + 0.06, 74 - 14 * (fmm / 8)),
                         fontsize=9.2, color=col, fontweight="bold")
    axR.axhline(60, color=C_ACC, lw=1.8, ls="--")
    axR.text(0.42, 68, "瞳距 60 px 采集下限", fontsize=9.4, color=C_ACC, fontweight="bold")
    axR.axhspan(100, 320, color=C_GRN, alpha=0.10)
    axR.text(0.40, 250, "推荐区 100~160 px", fontsize=9.4, color=C_GRN, fontweight="bold")
    axR.set_xlabel("识别距离 d（m）", fontsize=10.5)
    axR.set_ylabel("瞳距像素数 N_px（px）", fontsize=10.5)
    axR.set_xlim(0.3, 4.2)
    axR.set_ylim(0, 320)
    axR.legend(fontsize=9.5, loc="upper right", framealpha=0.95)
    axR.grid(alpha=0.22, ls=":")

    fig.text(0.545, 0.055,
             "注：瞳距 60 px 为业内常用采集下限（ISO/IEC 19794-5 亦以瞳距像素作为人脸图像质量指标之一）；0.065 m 为成人瞳距工程基准。",
             fontsize=8.8, color=C_GREY)

    axR.set_title("瞳距像素随距离衰减：越远越模糊，60 px 是硬门槛", fontsize=10.6, pad=8)

    fig.savefig(os.path.join(OUT, "lens-geometry.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ================================================================ 图4 状态机
def fig_flow():
    fig, ax = plt.subplots(figsize=(13.2, 8.9), dpi=110)
    base(ax, 13.2, 8.9)
    ax.text(6.6, 8.55, "图 4  一次刷脸通行的状态机与五条异常分支",
            ha="center", fontsize=14.5, fontweight="bold", color="#1A1A1A")
    ax.text(6.6, 8.14, "主链在 GA/T 1093-2023 下须 ≤1 s（活体开 ≤3 s）；异常分支才决定现场体感的好坏",
            ha="center", fontsize=10.2, color=C_GREY)

    bc, bw, bh, step = 3.72, 2.55, 0.78, 0.95
    y_top = 7.15
    steps = [
        ("S0  待机 / 低功耗", "红外人感或雷达唤醒", C_FILL, C_MAIN),
        ("S1  抓拍与质量评估", "清晰度 · 姿态角 · 曝光 · 戴口罩", C_FILL, C_MAIN),
        ("S2  活体检测 PAD", "不通过即终止并本地告警", C_FILL2, C_ACC),
        ("S3  特征比对", "1:1 确认 / 1:N 辨认", C_FILL3, C_GRN),
        ("S4  权限与时段裁决", "门组 · 时段 · 有效期 · 反潜回", C_FILL, C_MAIN),
        ("S5  执行与留证", "继电器 / 韦根输出 + 抓拍入库", C_FILL, C_MAIN),
    ]
    ys = [y_top - i * step for i in range(len(steps))]
    for (t, d, fc, ec), yy in zip(steps, ys):
        box(ax, bc - bw / 2, yy, bw, bh, t + "\n" + d, fc=fc, ec=ec, fs=9.6, bold=(t.startswith("S2")))
    for i in range(len(steps) - 1):
        arrow(ax, bc, ys[i], bc, ys[i + 1] + bh)      # 向下：S(i) -> S(i+1)

    # 异常分支：i 为发起分支的阶段序号
    branches = [
        (1, "质量不合格 -> 提示重站 / 补光不足 / 摘口罩", C_GOLD),
        (2, "活体失败 -> 拒绝 + 本地告警 + 抓拍留存", C_ACC),
        (3, "未注册或相似度低于阈值 -> 拒绝并引导人工", C_ACC),
        (4, "权限不足 / 时段不符 -> 拒绝（记录不告警）", "#7F7F7F"),
        (5, "连续 3 次失败 -> 锁定该终端并上报平台", C_ACC),
    ]
    xr = 8.62
    for i, t, col in branches:
        yy = ys[i] + bh / 2
        ax.plot([bc + bw / 2, xr - 0.14], [yy, yy], color=col, lw=1.5, ls="--", zorder=1)
        ax.plot([xr - 0.14], [yy], marker="o", ms=5, color=col, zorder=4)
        ax.text(xr, yy, t, fontsize=9.2, color=col, va="center")

    # 左侧：贯穿约束
    ax.add_patch(FancyBboxPatch((0.28, 4.30), 2.08, 2.72,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                linewidth=1.4, edgecolor=C_PUR, facecolor="#F6F2FB", zorder=1))
    ax.text(0.40, 6.86, "贯穿全程的三条硬约束", fontsize=10.0, fontweight="bold", color=C_PUR)
    cons = [
        "· 断网自治\n  本地库可离线比对，\n  恢复后补传流水并校时",
        "· 通行能力\n  单通道 T ≤ 3.5 s，\n  折合 1029 人/小时",
        "· 合规\n  单独同意 + 只存特征，\n  留存到期即删",
    ]
    yy0 = 6.48
    for t in cons:
        ax.text(0.40, yy0, t, fontsize=8.6, color="#333333", va="top", linespacing=1.5)
        yy0 -= 0.86

    # 底部：三个非算法因素
    ax.add_patch(FancyBboxPatch((0.28, 0.55), 12.62, 1.76,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                linewidth=1.2, edgecolor="#C8C8C8", facecolor="#FAFAFA", zorder=1))
    ax.text(0.48, 2.06, "现场最常见的三个「不是算法的锅」", fontsize=10.8, fontweight="bold")
    ax.text(0.48, 1.66,
            "1.  逆光 / 顶光使人脸过曝或半脸全黑 —— 先改安装朝向、加遮阳罩；室外逆光点位宽动态需求常达 100~120 dB，换个角度比换算法便宜得多。",
            fontsize=9.3, color="#333333")
    ax.text(0.48, 1.32,
            "2.  安装高度与俯角不对 —— 面板中心对准 1.4~1.6 m 人脸高度、俯角尽量小于 15°；俯角过大时关键点定位会明显退化。",
            fontsize=9.3, color="#333333")
    ax.text(0.48, 0.98,
            "3.  1:N 库太大迫使阈值抬高 —— 库每扩大 10 倍，单次误识率就要再降 10 倍，才能维持同一系统级误识水平，代价就是通过率下滑。",
            fontsize=9.3, color="#333333")

    fig.savefig(os.path.join(OUT, "flow-pass.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig_arch()
    fig_threshold()
    fig_lens()
    fig_flow()
    for f in ["arch-pipeline.png", "threshold-far-frr.png", "lens-geometry.png", "flow-pass.png"]:
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p) // 1024, "KB")
