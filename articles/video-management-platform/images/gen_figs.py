# -*- coding: utf-8 -*-
"""生成「视频监控管理平台（VMS）产品综述」配套矢量示意图（4 张）。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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


def box(ax, x, y, w, h, fc="#eef3fb", ec="#2f5f96", lw=1.6, radius=0.14, ls="-", zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={radius}",
                                facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=zorder))


def txt(ax, x, y, s, fs=9.0, color="#1f2a37", weight="normal", ha="center", va="center",
        zorder=6, bbox=None):
    kw = {}
    if bbox:
        kw = dict(bbox=dict(boxstyle="round,pad=0.18", facecolor=bbox, edgecolor="none"))
    ax.text(x, y, s, fontsize=fs, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, linespacing=1.35, **kw)


def arrow(ax, p1, p2, color="#c0392b", lw=1.8, ls="-", ms=11, zorder=5, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                                 color=color, linewidth=lw, linestyle=ls,
                                 zorder=zorder, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def dashed(ax, pts, color="#6b7280", lw=1.5, zorder=5):
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
# 图 1：VMS 六层架构与两条通道
# ============================================================
def fig1():
    h = 8.2
    fig, ax = newfig(h)
    txt(ax, 0.4, 7.62, "图 1　VMS 六层架构：会话通道与媒体流通道是分开的两条",
        fs=12.4, color="#16324f", weight="bold", ha="left")

    layers = [
        ("接入层", "IPC / NVR / 编码器 / 下级平台 / 报警主机", "#e8f0f9"),
        ("信令层", "中心信令控制服务器（SIP）：注册 · 心跳 · 目录 · 控制 · 订阅", "#dfeaf7"),
        ("媒体层", "流媒体服务器：实时点播 · 历史回放 · 转发复制 · 级联中转", "#dfeaf7"),
        ("存储层", "录像写入 · I 帧索引 · 抽帧降级 · 归档与防覆盖锁定", "#e8f0f9"),
        ("业务层", "预览 · 回放 · 电子地图 · 报警联动 · 智能分析 · 权限审计", "#eaf2fb"),
        ("接口层", "北向 API / SDK · ONVIF 下联 · GB/T 28181 上联 · 门禁报警集成", "#eaf2fb"),
    ]
    bx, bw = 0.5, 7.6
    top, step, bh = 7.10, 1.02, 0.80
    for i, (name, sub, fc) in enumerate(layers):
        y = top - i * step - bh
        box(ax, bx, y, bw, bh, fc=fc, ec=C_MAIN, lw=1.5)
        txt(ax, bx + 0.95, y + bh * 0.62, name, fs=10.2, color="#16324f", weight="bold")
        txt(ax, bx + 4.75, y + bh * 0.30, sub, fs=7.9, color="#42566b")

    # 两条通道竖带
    ch_top, ch_bot = 7.10, 1.20
    ch1x, ch2x, chw = 8.75, 10.65, 1.55
    box(ax, ch1x, ch_bot, chw, ch_top - ch_bot, fc="#fdf3e3", ec=C_HL, lw=1.8, radius=0.10)
    box(ax, ch2x, ch_bot, chw, ch_top - ch_bot, fc="#eaf6ef", ec=C_OK, lw=1.8, radius=0.10)
    for i, s in enumerate(["会话通道", "SIP", "MANSCDP", "MANSRTSP", "（信令）"]):
        txt(ax, ch1x + chw / 2, ch_top - 0.85 - i * 0.62, s, fs=8.4, color="#8a6510", weight="bold")
    for i, s in enumerate(["媒体流通道", "RTP / RTCP", "PS over RTP", "H.265 / H.264", "（视音频）"]):
        txt(ax, ch2x + chw / 2, ch_top - 0.85 - i * 0.62, s, fs=8.4, color="#1d6b4c", weight="bold")

    # 层 → 通道 虚线连接
    def cy(i):
        return top - i * step - bh / 2
    for i in (0, 1, 4, 5):
        dashed(ax, [(bx + bw, cy(i)), (ch1x, cy(i))], color="#b8860b", lw=1.3)
    for i in (0, 2, 3, 4):
        dashed(ax, [(bx + bw, cy(i)), (ch2x, cy(i))], color="#2e7d5b", lw=1.3)

    # 底部结论
    box(ax, 0.5, 0.25, 11.7, 0.72, fc="#fbf1f0", ec=C_ACC, lw=1.5, radius=0.10)
    txt(ax, 0.72, 0.61,
        "两条通道故障现象完全不同：信令挂 → 设备掉线但画面还在播；媒体挂 → 设备全部在线，却一路也点不开",
        fs=9.0, color="#8f2f22", ha="left")

    fig.savefig(os.path.join(OUT, "arch-platform.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("fig1 ok")


# ============================================================
# 图 2：扇出复制账（直连 vs 转发）
# ============================================================
def fig2():
    h = 8.4
    fig, ax = newfig(h)
    txt(ax, 0.3, 7.92, "图 2　扇出复制这笔账：流媒体转发替摄像机扛下了 R 倍复制压力",
        fs=12.4, color="#16324f", weight="bold", ha="left")

    NC = 6
    cw, gap = 0.80, 0.13

    # ---------- 左：直连 ----------
    p1x0, p1x1 = 0.25, 6.45
    box(ax, p1x0, 0.85, p1x1 - p1x0, 6.15, fc="#fbf7f6", ec="#c98a80", lw=1.5, radius=0.10)
    txt(ax, (p1x0 + p1x1) / 2, 7.28, "直连模式（无转发）", fs=10.6, color="#8f2f22", weight="bold")

    cam_c = 3.35
    box(ax, cam_c - 1.1, 5.85, 2.2, 0.65, fc="#fdeceb", ec=C_ACC, lw=1.8)
    txt(ax, cam_c, 6.18, "1080P 摄像机", fs=9.4, color="#8f2f22", weight="bold")

    cstart = cam_c - (NC * cw + (NC - 1) * gap) / 2
    cxs = [cstart + i * (cw + gap) + cw / 2 for i in range(NC)]
    for i, cx in enumerate(cxs):
        box(ax, cx - cw / 2, 1.70, cw, 0.65, fc="#ffffff", ec="#8a9bad", lw=1.2, radius=0.08)
        txt(ax, cx, 2.02, f"客户端{i + 1}", fs=7.2, color="#42566b")
        arrow(ax, (cam_c, 5.85), (cx, 2.35), color=C_ACC, lw=1.5, ms=9)

    txt(ax, cam_c, 5.42, "摄像机上行 = R × r = 6 × 4 = 24 Mbps", fs=9.2,
        color="#8f2f22", weight="bold", bbox="white")

    box(ax, 0.55, 0.98, 5.6, 0.55, fc="#fdeceb", ec=C_ACC, lw=1.3, radius=0.08)
    txt(ax, 3.35, 1.25, "R = 20 时上行达 80 Mbps → 百兆口 IPC 被自己打死",
        fs=8.6, color="#8f2f22", weight="bold")

    # ---------- 右：转发 ----------
    p2x0, p2x1 = 6.75, 12.95
    box(ax, p2x0, 0.85, p2x1 - p2x0, 6.15, fc="#f4f9f6", ec="#79a98f", lw=1.5, radius=0.10)
    txt(ax, (p2x0 + p2x1) / 2, 7.28, "流媒体转发模式（VMS）", fs=10.6, color="#1d6b4c", weight="bold")

    srv_c = 9.85
    box(ax, srv_c - 1.1, 5.85, 2.2, 0.65, fc="#e8f3ec", ec=C_OK, lw=1.8)
    txt(ax, srv_c, 6.18, "1080P 摄像机", fs=9.4, color="#1d6b4c", weight="bold")

    box(ax, srv_c - 1.75, 3.85, 3.5, 0.85, fc="#dff0e6", ec=C_OK, lw=2.0, radius=0.12)
    txt(ax, srv_c, 4.46, "流媒体转发服务器", fs=10.0, color="#14503a", weight="bold")
    txt(ax, srv_c, 4.11, "收 1 份 · 复制 R 份（内存拷贝 ≈ 2 × 出向）", fs=7.6, color="#2e7d5b")

    arrow(ax, (srv_c, 5.85), (srv_c, 4.70), color=C_OK, lw=2.0, ms=11)
    txt(ax, srv_c + 1.95, 5.28, "仅 4 Mbps", fs=8.6, color="#14503a", weight="bold", ha="left",
        bbox="white")

    cstart2 = srv_c - (NC * cw + (NC - 1) * gap) / 2
    cxs2 = [cstart2 + i * (cw + gap) + cw / 2 for i in range(NC)]
    for i, cx in enumerate(cxs2):
        box(ax, cx - cw / 2, 1.70, cw, 0.65, fc="#ffffff", ec="#8a9bad", lw=1.2, radius=0.08)
        txt(ax, cx, 2.02, f"客户端{i + 1}", fs=7.2, color="#42566b")
        arrow(ax, (srv_c, 3.85), (cx, 2.35), color=C_OK, lw=1.5, ms=9)

    txt(ax, srv_c, 3.42, "摄像机上行恒为 r = 4 Mbps；平台出向 = R × r = 24 Mbps", fs=8.8,
        color="#14503a", weight="bold", bbox="white")

    box(ax, 7.05, 0.98, 5.6, 0.55, fc="#dff0e6", ec=C_OK, lw=1.3, radius=0.08)
    txt(ax, 9.85, 1.25, "R 再大也只是平台加节点，摄像机始终只出一份",
        fs=8.6, color="#14503a", weight="bold")

    fig.savefig(os.path.join(OUT, "fanout-bw.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("fig2 ok")


# ============================================================
# 图 3：存储容量瀑布（码率 → 盘数 → 柜数）
# ============================================================
def fig3():
    import numpy as np
    fig = plt.figure(figsize=(W, 8.5), dpi=140)
    ax1 = fig.add_axes([0.0, 0.50, 1.0, 0.46])
    ax2 = fig.add_axes([0.085, 0.085, 0.885, 0.335])
    for a in (ax1,):
        a.set_xlim(0, W)
        a.set_ylim(0, 3.6)
        a.axis("off")
        a.set_aspect("equal")

    txt(ax1, 0.3, 3.35, "图 3　存储容量瀑布：从码率到机柜，四道折算一步都不能省",
        fs=12.4, color="#16324f", weight="bold", ha="left")

    steps = [
        ("① 码率", "4 Mbps", "1080P H.265 工程基准\n（按峰值，不按平均）", "#e8f0f9"),
        ("② 单路单日", "40.2 GiB", "r × 86400 ÷ 8\n= 43.2 GB（十进制）", "#dfeaf7"),
        ("③ × 3000 路 × 30 天", "3536 TiB", "= 3888 TB\nGB 与 GiB 差 7.4%", "#dfeaf7"),
        ("④ ÷ 10.9 TiB/盘", "324 块", "14.55 TiB × 0.75\n（RAID6 + 热备 + 水位）", "#e8f0f9"),
        ("⑤ ÷ 36 盘位/柜", "9 台柜", "4U 36 盘位\n企业级存储柜", "#eaf2fb"),
    ]
    sw = 2.36
    total = 5 * sw + 4 * 0.30
    x0 = (W - total) / 2
    yb, bh = 0.95, 2.05
    for i, (t, v, note, fc) in enumerate(steps):
        x = x0 + i * (sw + 0.30)
        box(ax1, x, yb, sw, bh, fc=fc, ec=C_MAIN, lw=1.5, radius=0.12)
        txt(ax1, x + sw / 2, yb + bh - 0.32, t, fs=8.6, color="#16324f", weight="bold")
        txt(ax1, x + sw / 2, yb + bh - 0.85, v, fs=13.0, color=C_ACC, weight="bold")
        txt(ax1, x + sw / 2, yb + 0.62, note, fs=7.3, color="#42566b")
        if i < 4:
            arrow(ax1, (x + sw + 0.02, yb + bh / 2), (x + sw + 0.28, yb + bh / 2),
                  color=C_MAIN, lw=1.8, ms=11)

    txt(ax1, 0.3, 0.55, "口径陷阱：厂商按 TB 报容量、系统按 TiB 显示，1 TB = 0.909 TiB —— 差出来的 9% 直接吃进预算",
        fs=8.6, color="#8f2f22", ha="left")

    # ---- 下方柱状：全量 vs 分级 ----
    labels = ["全部点位 30 天", "分级：1000 路 30 天\n+ 2000 路 15 天"]
    caps = [3536, 2357]
    disks = [324, 216]
    xpos = [0.0, 1.0]
    bars = ax2.bar(xpos, caps, width=0.52, color=["#c0392b", "#2e7d5b"],
                   edgecolor="#16324f", linewidth=1.2, zorder=3)
    ax2.set_xticks(xpos)
    ax2.set_xticklabels(labels, fontsize=9.6, color="#1f2a37")
    ax2.set_ylabel("裸容量（TiB）", fontsize=9.6, color="#1f2a37")
    ax2.set_ylim(0, 4100)
    ax2.grid(axis="y", linestyle=":", color="#c3ccd6", zorder=0)
    ax2.set_axisbelow(True)
    for b, cap, dk in zip(bars, caps, disks):
        ax2.text(b.get_x() + b.get_width() / 2, cap + 90, f"{cap} TiB",
                 fontsize=11.0, color="#16324f", weight="bold", ha="center")
        ax2.text(b.get_x() + b.get_width() / 2, cap * 0.42, f"≈ {dk} 块 16 TB 盘\n≈ {dk // 36} 台 36 盘位柜",
                 fontsize=9.2, color="white", ha="center", va="center", weight="bold",
                 linespacing=1.45)
    ax2.annotate("", xy=(0.70, 2357), xytext=(0.70, 3536),
                 arrowprops=dict(arrowstyle="-|>", color="#2e7d5b", lw=1.6))
    ax2.text(0.65, (3536 + 2357) / 2, "省 33%\n（1179 TiB）", fontsize=9.4,
             color="#1d6b4c", weight="bold", va="center", ha="right")
    for s in ax2.spines.values():
        s.set_color("#c3ccd6")

    fig.savefig(os.path.join(OUT, "storage-capacity.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("fig3 ok")


# ============================================================
# 图 4：落地七步 + 注册风暴异常分支
# ============================================================
def fig4():
    h = 8.6
    fig, ax = newfig(h)
    txt(ax, 0.3, 8.08, "图 4　落地七步与注册风暴异常分支（级联项目必做的回退环）",
        fs=12.4, color="#16324f", weight="bold", ha="left")

    steps = [
        ("① 需求与点位清单", "设备数 / 路数 / 通道数"),
        ("② 容量核算", "接入 · 转发 · 存储三笔"),
        ("③ 网络与地址规划", "VLAN · 收敛比 · NAT 穿透"),
        ("④ 平台部署与集群", "转发 N+1 · 信令主备"),
        ("⑤ 设备接入与目录", "命名规范 · 目录树治理"),
        ("⑥ 权限 · 时钟 · 安全基线", "NTP · GB 35114 分级"),
        ("⑦ 联调 · 演练 · 验收", "含断电恢复演练"),
    ]
    sw, sh = 2.5, 0.92

    def place(i):
        if i < 4:
            return 0.4 + i * 3.1, 6.30
        return 0.4 + (i - 4) * 3.1, 3.40

    for i, (t, sub) in enumerate(steps):
        x, y = place(i)
        fc = "#e8f0f9" if i < 4 else "#eaf2fb"
        box(ax, x, y, sw, sh, fc=fc, ec=C_MAIN, lw=1.5)
        txt(ax, x + sw / 2, y + sh * 0.66, t, fs=9.4, color="#16324f", weight="bold")
        txt(ax, x + sw / 2, y + sh * 0.27, sub, fs=7.6, color="#42566b")

    # 第一行：横向箭头
    for i in range(3):
        x, y = place(i)
        arrow(ax, (x + sw, y + sh / 2), (x + sw + 0.60, y + sh / 2), color=C_MAIN, lw=1.8, ms=11)
    # 换行：S4 → S5
    x4, y4 = place(3)
    x5, y5 = place(4)
    dashed(ax, [(x4 + sw / 2, y4), (x4 + sw / 2, 5.10), (x5 + sw / 2, 5.10), (x5 + sw / 2, y5 + sh)],
           color=C_MAIN, lw=1.7)
    arrow(ax, (x5 + sw / 2, 5.10), (x5 + sw / 2, y5 + sh - 0.02), color=C_MAIN, lw=1.7, ms=10)
    # 第二行：横向箭头
    for i in range(4, 6):
        x, y = place(i)
        arrow(ax, (x + sw, y + sh / 2), (x + sw + 0.60, y + sh / 2), color=C_MAIN, lw=1.8, ms=11)

    # 异常分支框
    x7, y7 = place(6)
    ex_x, ex_y, ex_w, ex_h = 9.7, 3.40, 3.1, 1.45
    box(ax, ex_x, ex_y, ex_w, ex_h, fc="#fdeceb", ec=C_ACC, lw=1.9, radius=0.12)
    txt(ax, ex_x + ex_w / 2, ex_y + ex_h - 0.24, "异常分支：注册风暴", fs=9.4,
        color="#8f2f22", weight="bold")
    txt(ax, ex_x + ex_w / 2, ex_y + ex_h - 0.66, "全网恢复瞬时数千 QPS", fs=7.8, color="#8f2f22")
    txt(ax, ex_x + ex_w / 2, ex_y + 0.46, "退避窗口 W = 300 s\n10000 台 → 均值 33 QPS", fs=7.8,
        color="#8f2f22")
    arrow(ax, (x7 + sw, y7 + sh / 2), (ex_x - 0.02, y7 + sh / 2 + 0.26), color=C_ACC, lw=1.9, ms=11)
    # 回退到 ⑤
    dashed(ax, [(ex_x + ex_w / 2, ex_y), (ex_x + ex_w / 2, 2.45),
                (x5 + sw / 2, 2.45), (x5 + sw / 2, y5)],
           color=C_ACC, lw=1.7)
    txt(ax, (ex_x + ex_w / 2 + x5 + sw / 2) / 2, 2.20, "回退：在接入阶段施加随机退避与分批注册上限",
        fs=8.2, color="#8f2f22", bbox="white")

    # 底部结论条
    box(ax, 0.4, 0.55, 12.4, 1.15, fc="#fbf1f0", ec=C_ACC, lw=1.5, radius=0.10)
    txt(ax, 0.65, 1.42, "稳态 QPS 从不出问题，出问题的一定是断电恢复那一瞬间 —— 验收清单里必须写进「断电恢复演练」",
        fs=9.0, color="#8f2f22", ha="left", weight="bold")
    txt(ax, 0.65, 0.92, "稳态 Q = N / T_hb + N / T_reg　（心跳 60 s、重注册 3600 s：10000 台 ≈ 169 QPS，可控）",
        fs=8.6, color="#8f2f22", ha="left")
    txt(ax, 0.65, 0.72, "退避后 Q均值 = N / W　（W = 300 s：10000 台 → 均值 33 QPS，峰值约 70~100 QPS）",
        fs=8.6, color="#8f2f22", ha="left")

    fig.savefig(os.path.join(OUT, "flow-cascade.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("fig4 ok")


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
