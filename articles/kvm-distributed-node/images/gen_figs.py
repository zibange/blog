# -*- coding: utf-8 -*-
"""分布式可视化坐席节点产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system     接入—分发—操控—扩展四层 + 独立管理同步通道（1.4）
  图2 bandwidth-delay 带宽预算链（左）+ 端到端延时五段分解（右）（2.2 算例1/2/4）
  图3 permission-jitter 四级权限矩阵（左）+ 软件/硬件延时分布对比（右）（2.2 算例8/10）
  图4 scene-topology  六类场景共用的操控骨架（五）

配色、坐标系用法沿用成熟模板（见 content-factory §7.3）：
  - newfig() 把整幅画布当成一个 axes（数据坐标 0~W, 0~H）；
  - footer() 单独开一个 add_axes（用图幅比例），不与绘图区混用 tight 裁剪；
  - 全局字体 Microsoft YaHei；戒用 ↔/✓/≪/⁻¹ 等无字形字符（用文字代替）。

Python 教学要点：
  - os.path.dirname(os.path.abspath(__file__))：拿到脚本所在目录，保证图片输出到本目录
    而不受运行时工作目录影响；
  - matplotlib.use("Agg")：无界面后端，服务器/自动化环境只出 PNG 不弹窗；
  - FancyBboxPatch / FancyArrowPatch：画圆角框与箭头；
  - add_axes([left,bottom,width,height])：用「图幅比例」精确定位子坐标系，
    适合做嵌入式小图（柱状图）和底部说明条。
"""
import os                      # 拼接路径、读取脚本所在目录
import numpy as np             # 数值计算与数组
import matplotlib              # 绘图库主模块
matplotlib.use("Agg")          # 无界面后端：只输出 PNG
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # 圆角框 / 箭头

# 全局字体：不设的话刻度/图例/标题会用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6  # 画布数据坐标范围

# ---- light 主题配色（浅底深字，适配浅色 IDE 主题）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（接入层 / 编码）
C2 = "#0E9F6E"   # 绿（分发层 / 组播）
C3 = "#E8833A"   # 橙（操控层 / 键鼠）
C4 = "#C2410C"   # 深橙（管理通道 / 临界）
C5 = "#7C3AED"   # 紫（扩展层 / 平台）
CGREY = "#CBD2D9"


def newfig():
    """整幅画布当成一个坐标轴：数据坐标 0~W / 0~H。"""
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-"):
    """圆角矩形：x/y 左下角，w/h 宽高，fc/ec 填充与描边。"""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       alpha=alpha, linestyle=ls, zorder=2)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=9.4, color=INK, weight="normal",
        ha="center", va="center", zorder=6):
    """统一文字样式：显式指定字体族，避免中文丢失。"""
    ax.text(x, y, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily="Microsoft YaHei")


def title(ax, t, sub=None):
    """图标题 + 副标题。顶边控制在 ~7.4 以内，给副标题（y≈7.6）让位。"""
    txt(ax, W / 2, H - 0.52, t, size=14.0, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.00, sub, size=8.6, color=MUTED, ha="center")


def footer(ax, s):
    """底部说明条：单独开一个 axes，避免与绘图区坐标系混用导致错位。"""
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=1)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=7.3, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    """箭头：shrinkA/shrinkB=0 让箭头从坐标点起始/结束，不自动留白。"""
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：接入—分发—操控—扩展四层 + 独立管理同步通道
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  分布式坐席四层架构 + 独立管理同步通道",
          "接入 → 分发 → 操控 → 扩展；管理面只做调度策略、转发下放到节点，与业务码流隔离")

    # 四列主块：接入 / 分发 / 操控 / 扩展
    # 列宽与间距：bx + 4*bw + 3*gap = 0.35 + 4*2.85 + 3*0.40 = 12.95 < 13.2
    cols = [
        ("接入层（节点）", C1, "#EFF6FF",
         ["输入：HDMI/DP 采集", "KVM：USB 键鼠注入", "输出：解码回显", "编码 H.265/JPEG2000"]),
        ("分发层（网络）", C2, "#ECFDF5",
         ["万兆/25G 核心交换", "组播 IGMP Snooping", "QoS 优先级 DSCP", "PTPv2 时钟同步"]),
        ("操控层（坐席）", C3, "#FFF7ED",
         ["信号预览(缩略图)", "拖拽推送/回显", "键鼠漫游一人多机", "场景预案调用"]),
        ("扩展层", C5, "#F5F3FF",
         ["大屏拼控 LED/LCD", "会商 H.323/SIP", "录播归档审计", "GB/T 28181/ONVIF"]),
    ]
    bx, bw, gap = 0.35, 2.85, 0.40
    by, bh = 2.45, 3.35
    for i, (name, c, fill, items) in enumerate(cols):
        x = bx + i * (bw + gap)
        box(ax, x, by, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, by + bh - 0.48, name, size=10.6, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = by + bh - 1.05 - j * 0.52
            txt(ax, x + bw / 2, yy, it, size=8.2, color=INK)
    ay = by + bh / 2
    for i in range(3):
        arrow(ax, bx + i * (bw + gap) + bw, ay,
              bx + (i + 1) * (bw + gap), ay, color=MUTED, lw=1.8)

    # 顶部管理同步通道（单列，绕过四层）
    fx, fy, fw, fh = 0.35, 6.35, 12.6, 0.62
    box(ax, fx, fy, fw, fh, "#FFF1EE", C4, lw=1.8)
    txt(ax, fx + fw / 2, fy + fh / 2,
        "独立管理同步通道：节点管理 / 状态监测 / 日志 / 时钟同步（独立 VLAN）——业务码流拥塞时仍可管、可复位",
        size=8.7, color=C4, weight="bold")
    arrow(ax, 6.6, fy, 6.6, by + bh + 0.05, color=C4, lw=1.6, ls="--")

    # 底部转发面说明
    ox, oy, ow, oh = 0.4, 1.35, 12.4, 0.92
    box(ax, ox, oy, ow, oh, "#F6F8FA", CGREY, lw=1.1)
    txt(ax, ox + ow / 2, oy + oh - 0.28,
        "转发面下放到节点：节点间本地直达，管理软件宕机时已下发的切换/显示照常跑",
        size=8.5, color=INK)
    txt(ax, ox + ow / 2, oy + 0.26,
        "验收试金石：拔掉管理服务器网线，坐席仍能切换与操控 = 真去中心化；否则是假分布式",
        size=8.0, color=MUTED)

    footer(ax, "注：依据 GB 50348-2018、GB 50174-2017、GB/T 22239-2019；管理面与转发面分离是可用性的关键。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：带宽预算链（左）+ 端到端延时五段分解（右）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  带宽预算链 + 延时五段分解：两个口径别混着比",
          "裸流 11.9 → 编码 0.6 → 40 路 24 Gbps；核心编解码段约 22 ms，全程含帧对齐约 55 ms")

    # --- 左侧：带宽预算链（四个阶段横条 + 换算）---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 带宽预算链（单路 → 并发）", size=10.2,
        weight="bold", color=C1)
    stages = [
        ("裸流", "4K60 4:4:4 未压缩", "11.9 Gbps", C4, 5.55),
        ("H.265", "压缩约 20:1", "0.6 Gbps", C1, 4.50),
        ("40 路并发", "40 × 0.6", "24 Gbps", C3, 3.45),
        ("+30% 余量", "24 × 1.3", "31.2 Gbps", C2, 2.40),
    ]
    sh = 0.92
    for name, desc, val, c, yy in stages:
        box(ax, lx, yy, lw, sh, "#F6F8FA", c, lw=1.5)
        txt(ax, lx + 0.18, yy + sh / 2, name, size=9.4, weight="bold", color=c, ha="left")
        txt(ax, lx + 1.55, yy + sh / 2, desc, size=8.6, color=INK, ha="left")
        txt(ax, lx + lw - 0.15, yy + sh / 2, val, size=9.4, weight="bold", color=c, ha="right")
    for i in range(3):
        arrow(ax, lx + lw / 2, stages[i][4],
              lx + lw / 2, stages[i + 1][4] + sh, color=MUTED, lw=1.3)
    box(ax, lx, 1.55, lw, 0.72, "#ECFDF5", C2, lw=1.4)
    txt(ax, lx + lw / 2, 1.91,
        "25G 核心 + 组播：K=10 个坐席同看省约 90% 上联带宽",
        size=8.6, color=INK, weight="bold")

    # --- 右侧：延时五段分解（五段横条 + 两种口径）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② 端到端延时五段分解", size=10.2,
        weight="bold", color=C3)
    segs = [
        ("采集", "凑一帧 @60fps", "16.7 ms", C1),
        ("编码", "H.265 帧间缓冲", "10 ms", C2),
        ("网络", "局域网传输", "2 ms", C3),
        ("解码", "还原画面", "10 ms", C5),
        ("显示", "帧对齐输出", "16.7 ms", C4),
    ]
    y0, step, sh2 = 5.55, 0.83, 0.70
    for i, (name, desc, val, c) in enumerate(segs):
        yy = y0 - i * step
        box(ax, rx, yy, rw, sh2, "#F6F8FA", c, lw=1.4)
        txt(ax, rx + 0.18, yy + sh2 / 2, name, size=9.2, weight="bold", color=c, ha="left")
        txt(ax, rx + 1.05, yy + sh2 / 2, desc, size=8.3, color=INK, ha="left")
        txt(ax, rx + rw - 0.15, yy + sh2 / 2, val, size=9.0, color=c, ha="right")
    # 两种口径结论
    box(ax, rx, 1.42, rw, 0.82, "#FFF7ED", C3, lw=1.6)
    txt(ax, rx + rw / 2, 1.96,
        "核心编解码段 ≈ 22 ms（厂商口径）｜ 全程含帧对齐 ≈ 55 ms",
        size=8.5, color=C4, weight="bold")

    footer(ax, "注：算例1 B=W·H·b·f；算例2 并发 24 Gbps 留 30% 余量；算例4 厂商测核心段、操作者感受全程，测法须写清。")
    fig.savefig(os.path.join(OUT, "bandwidth-delay.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：四级权限矩阵（左）+ 软件/硬件延时分布对比（右）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  四级权限矩阵 + 延时确定性：均值接近，P99 差很多",
          "权限按角色模板下发、共享抢占需会签；验收看 P99 而非平均值")

    # --- 左侧：四级权限矩阵（四行权限 + 规模结论）---
    lx, lw = 0.55, 5.95
    txt(ax, lx + lw / 2, 6.62, "① 四级权限（角色 × 资源 × 动作）", size=10.2,
        weight="bold", color=C5)
    perms = [
        ("独占 Exclusive", "一人操控，他人不可见", C4, 5.55),
        ("共享 Share", "多人同看，按规则抢占", C3, 4.48),
        ("私有 Private", "仅授权者可见可控", C2, 3.41),
        ("只读 View only", "看得见、控不了", C1, 2.34),
    ]
    for name, desc, c, yy in perms:
        box(ax, lx, yy, lw, 0.92, "#FFFFFF", c, lw=1.5)
        txt(ax, lx + 0.18, yy + 0.62, name, size=9.6, weight="bold", color=c, ha="left")
        txt(ax, lx + 0.18, yy + 0.24, desc, size=8.2, color=INK, ha="left")
    # 结论条下移到 y=1.30，给柱状图 x 轴标签腾出空间（避免被压字）
    box(ax, lx, 1.30, lw, 0.72, "#F5F3FF", C5, lw=1.4)
    txt(ax, lx + lw / 2, 1.66,
        "6 角色 × 40 主机 × 4 动作 = 960 条 → 模板化后约 24 条基线",
        size=8.5, color=INK, weight="bold")

    # --- 右侧：软件 vs 硬件 均值/P99 对比（嵌入式柱状图）---
    # 修复要点：① axes 底部抬到 2.50、高度缩到 3.70，使 x 轴标签落在结论条上方；
    #           ② 去掉竖排 ylabel（会挤进左栏），改为标题内标注单位；
    #           ③ ylim 提到 52、图例改右上角，避免压住 38.6 的数值标注。
    rx, rw = 6.95, 5.65
    txt(ax, rx + rw / 2, 6.62, "② 延时确定性：均值 vs P99（单位 ms）", size=10.2,
        weight="bold", color=C3)
    a = fig.add_axes([rx / W, 2.50 / H, rw / W, 3.70 / H])
    a.set_facecolor("#FFFFFF")
    groups = ["软件方案\n(通用 CPU)", "硬件方案\n(FPGA)"]
    mean = [20.0, 18.0]
    p99 = [38.6, 21.5]
    x = np.arange(2)
    bw = 0.32
    b1 = a.bar(x - bw / 2, mean, bw, label="均值", color=[C1, C1], zorder=3)
    b2 = a.bar(x + bw / 2, p99, bw, label="P99", color=[C4, C2], zorder=3)
    for bars in (b1, b2):
        for bar in bars:
            a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.0,
                   f"{bar.get_height():.1f}", ha="center", va="bottom",
                   fontsize=9.2, color=INK, weight="bold", zorder=5)
    a.axhline(30, color=C4, ls="--", lw=1.4, zorder=4, label="验收线 P99 ≤ 30 ms")
    a.set_xticks(x)
    a.set_xticklabels(groups, fontsize=8.8, color=INK)
    a.set_ylim(0, 52)
    a.legend(loc="upper right", fontsize=7.6, frameon=True)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.2, colors=MUTED)
    # 结论条（数据坐标），与左栏结论条同一 y 对齐
    box(ax, rx, 1.30, rw, 0.72, "#FFF1EE", C4, lw=1.4)
    txt(ax, rx + rw / 2, 1.66,
        "均值只差 2 ms，P99 差约 17 ms —— 拖拽感全在那 17 ms 里",
        size=8.5, color=C4, weight="bold")

    footer(ax, "注：算例8 P99≈均值+2.33σ，软件 σ=8ms、硬件 σ=1.5ms；算例10 权限 960 条须模板化 + 抢占会签。")
    fig.savefig(os.path.join(OUT, "permission-jitter.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用操控骨架（左链 + 右六场景两列三行）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类场景共用一套操控骨架：接入 → 分发 → 操控 → 扩展",
          "指挥中心 / 机房运维 / 广电播控 / 电力调度 / 金融交易 / 轨道交通，差异只在规模、画质、权限与合规")

    # 左侧：共用骨架主轴（五个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.35, 3.15, 3.65
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.45, "共用骨架", size=11.2, weight="bold", color=C1)
    chain = ["节点接入信号", "网络组播分发", "坐席预览推送", "键鼠漫游操控", "录制归档审计"]
    step, subh = 0.56, 0.42
    top_c = oy + oh - 1.15
    for i, s in enumerate(chain):
        yc = top_c - i * step
        box(ax, ox + 0.25, yc - subh / 2, ow - 0.5, subh, "#FFFFFF", C1, lw=1.0)
        txt(ax, ox + ow / 2, yc, s, size=8.5, color=INK)
        if i < len(chain) - 1:
            arrow(ax, ox + ow / 2, yc - subh / 2 - 0.01,
                  ox + ow / 2, yc - step + subh / 2 + 0.01, color=C1, lw=1.0)

    # 右侧六个场景框（两列三行），y 顶边 ≤7.4 给副标题让位
    scenes = [
        ("应急指挥中心", "多席协同，一键推大屏", C2, "#ECFDF5"),
        ("机房运维", "人机分离，单线 PoE", C1, "#EFF6FF"),
        ("广电播控", "JPEG2000 无损，无黑场", C3, "#FFF7ED"),
        ("电力调度", "硬件确定性，国密冗余", C4, "#FFF1EE"),
        ("金融交易", "4:4:4 清晰，全程审计", C5, "#F5F3FF"),
        ("轨道交通", "多路上墙，平台利旧", C2, "#ECFDF5"),
    ]
    sx0, sw, sh = 4.15, 4.15, 1.35
    gx, gy = 0.35, 0.22
    for i, (name, desc, c, fill) in enumerate(scenes):
        col = i % 2
        row = i // 2
        x = sx0 + col * (sw + gx)
        y = 5.95 - row * (sh + gy)
        box(ax, x, y, sw, sh, fill, c, lw=1.6)
        txt(ax, x + 0.25, y + sh - 0.36, name, size=10.0, weight="bold", color=c, ha="left")
        txt(ax, x + 0.25, y + 0.34, desc, size=8.5, color=INK, ha="left")

    footer(ax, "注：六类场景底层都是同一套接入—分发—操控—扩展骨架，差异只在并发规模、画质、权限粒度、冗余等级与合规红线。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
