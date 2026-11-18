# -*- coding: utf-8 -*-
"""视频存储服务器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system        五层架构：接入/网络/计算缓存 + 存储/冗余/软件（1.4）
  图2 raid-ec-capacity   容量与冗余折算：RAID6 vs EC + 千路月存核算链（2.2 算例1~2）
  图3 bandwidth-tiering  写入带宽与冷热分层（2.2 算例3/5/10）
  图4 scene-topology     四类落地场景共用「写入→资源池→冗余自愈→检索回放」后端链（六）

配色、坐标系用法沿用成熟模板（见 content-factory §7.3）：
  - newfig() 把整幅画布当成一个 axes（数据坐标 0~W, 0~H），精确定位框线；
  - footer() 单独开一个 add_axes（用图幅比例），不与绘图区混用 tight 裁剪；
  - 全局字体 Microsoft YaHei：否则内置坐标轴（刻度/图例）走 DejaVu Sans，中文全空白；
  - 戒用 ↔(U+2194)/✓/≪/⁻¹ 等 Microsoft YaHei 无字形字符，改用「与」「[符合]」等。
"""
import os                      # 用于拼接路径、读取脚本所在目录
import numpy as np             # 数值计算与数组（柱状图坐标、渐变等）
import matplotlib              # 绘图库主模块
matplotlib.use("Agg")          # 无界面后端：服务器端只输出 PNG，不弹窗
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # 圆角框 / 箭头
import matplotlib.patheffects as pe                            # 文字白描边（跨线可读）

# 全局字体：不设的话刻度/图例/标题会用 DejaVu Sans，中文全变空白
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False  # 负号用 ASCII '-'，避免方框

# __file__ 是当前脚本路径；dirname 取它所在目录（images/），让输出跟着脚本走
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6  # 画布数据坐标范围（宽 13.2、高 8.6 单位）

# ---- light 主题配色（浅底深字，适配浅色 IDE 主题）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（接入/网络）
C2 = "#0E9F6E"   # 绿（计算/存储）
C3 = "#E8833A"   # 橙（冗余/带宽）
C4 = "#C2410C"   # 深橙（临界/成本）
C5 = "#7C3AED"   # 紫（软件/自愈）
CGREY = "#CBD2D9"


def newfig():
    """整幅画布当成一个坐标轴：数据坐标 0~W / 0~H，便于精确定位每个框线。"""
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])  # 占满整幅，比例坐标 [左,下,宽,高]
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")                   # 关掉刻度轴，自己用 box/txt 画
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-"):
    """画圆角矩形：x/y 是左下角，w/h 是宽高，fc/ec 是填充与描边色。"""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       alpha=alpha, linestyle=ls, zorder=2)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=9.4, color=INK, weight="normal",
        ha="center", va="center", zorder=6):
    """在指定数据坐标写文字；ha/va 控制对齐方式。"""
    ax.text(x, y, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily="Microsoft YaHei")


def title(ax, t, sub=None):
    """图标题 + 副标题。顶边控制在 ~7.4 以内，给副标题（y≈7.6）让位。"""
    txt(ax, W / 2, H - 0.52, t, size=14.2, weight="bold", ha="center")
    if sub:
        # 经验：画布顶部元素顶边不得超过 ~7.4，否则压住副标题
        txt(ax, W / 2, H - 1.00, sub, size=8.8, color=MUTED, ha="center")


def footer(ax, s):
    """底部说明条：单独开一个 axes，避免与绘图区坐标系混用导致错位。"""
    ax2 = ax.figure.add_axes([0.055, 0.018, 0.89, 0.052], zorder=1)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    p = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.16",
                       linewidth=1.0, edgecolor=GRID, facecolor="#F6F8FA", zorder=1)
    ax2.add_patch(p)
    ax2.text(0.5, 0.5, s, fontsize=7.6, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    """FancyArrowPatch 画带箭头连线；shrinkA/B=0 让端点精确落在框边。"""
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：五层系统架构（参照 IPC fig1 的 3+3 分块，避免框重叠）
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  视频存储服务器五层架构：接入 + 网络 + 计算缓存 + 存储 + 冗余 + 软件",
          "IPC 码流经直存或流媒体转发写入资源池，再供检索、回放、下载与平台调度")

    # 上排三块：接入层 → 网络层 → 计算缓存层
    blocks_top = [
        ("接入层", C1, "#EFF6FF", ["IPC 码流接入", "直存 / 流媒体转发", "类型码 210 注册", "GB/T 28181 取流"]),
        ("网络层", C1, "#EFF6FF", ["多千兆口捆绑", "万兆上联", "并发写带宽", "端口负载均衡"]),
        ("计算缓存层", C2, "#ECFDF5", ["多核 CPU", "写缓存", "纠删码编解码", "条带计算"]),
    ]
    bx, bw, gap = 0.45, 3.55, 0.72
    ty, bh = 4.75, 2.65
    for i, (name, c, fill, items) in enumerate(blocks_top):
        x = bx + i * (bw + gap)
        box(ax, x, ty, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, ty + bh - 0.45, name, size=11.2, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = ty + bh - 1.10 - j * 0.42
            txt(ax, x + bw / 2, yy, it, size=8.6, color=INK)
    ay = ty + bh / 2
    for i in range(2):
        arrow(ax, bx + i * (bw + gap) + bw, ay,
              bx + (i + 1) * (bw + gap), ay, color=MUTED, lw=1.6)

    # 下排三块：存储层 → 冗余层 → 软件层
    blocks_bot = [
        ("存储层", C2, "#ECFDF5", ["24~36 盘位", "企业级硬盘", "SSD 热分层", "裸容量/资源池"]),
        ("冗余层", C3, "#FFF7ED", ["RAID 6 / N+M EC", "热备盘", "冗余热插拔电源", "坏盘自愈重构"]),
        ("存储软件层", C5, "#F5F3FF", ["统一命名空间", "检索/回放/锁定", "双层负载均衡", "SNMP 网管"]),
    ]
    by = 1.75
    for i, (name, c, fill, items) in enumerate(blocks_bot):
        x = bx + i * (bw + gap)
        box(ax, x, by, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, by + bh - 0.45, name, size=11.2, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = by + bh - 1.10 - j * 0.42
            txt(ax, x + bw / 2, yy, it, size=8.6, color=INK)
    ay2 = by + bh / 2
    for i in range(2):
        arrow(ax, bx + i * (bw + gap) + bw, ay2,
              bx + (i + 1) * (bw + gap), ay2, color=MUTED, lw=1.6)

    # 计算缓存层(上排第3列) → 存储层(下排第1列)：走右侧下降 + 水平回左，不穿框
    calc_cx = bx + 2 * (bw + gap) + bw / 2
    stor_cx = bx + bw / 2
    arrow(ax, calc_cx, ty, calc_cx, by + bh + 0.25, color=C2, lw=1.4)
    arrow(ax, calc_cx, by + bh + 0.25, stor_cx, by + bh + 0.25, color=C2, lw=1.4, ls="--")
    arrow(ax, stor_cx, by + bh + 0.25, stor_cx, by + bh, color=C2, lw=1.4)

    # 底部输出条：码流去向
    ox, oy, ow, oh = 2.6, 0.72, 8.0, 0.62
    box(ax, ox, oy, ow, oh, "#F6F8FA", CGREY, lw=1.1)
    txt(ax, ox + ow / 2, oy + oh / 2,
        "对外服务：平台调度 / 按时间通道检索 / RTSP 回放 / 录像下载与锁定 / 二次开发 SDK",
        size=8.4, color=MUTED)
    sw_cx = bx + 2 * (bw + gap) + bw / 2  # 软件层中心（下排第3列）
    arrow(ax, sw_cx, by, sw_cx, oy + oh, color=C5, lw=1.4)

    footer(ax, "注：五层互相配合——接入层定取流方式，网络层定写入带宽，计算缓存做纠删码，存储层给容量，冗余层保不丢，软件层管检索与自愈。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：容量与冗余折算（左侧柱状利用率 + 右侧核算链文本框）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  容量与冗余折算：RAID 利用率更高，EC 换节点级容错",
          "36 盘位 × 8 TB = 288 TB 裸容量；千路月存约 1.15 PiB，需 6~8 台节点")

    # --- 左侧：三种冗余方式的空间利用率柱状图（独立 add_axes，比例坐标）---
    lx, ly, lw, lh = 0.75, 2.05, 5.5, 4.85
    a = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a.set_facecolor("#FFFFFF")
    labels = ["RAID 6\n(36盘-2校验)", "EC 8+2\n(80%)", "EC 12+3\n(80%)"]
    util = [94.4, 80.0, 80.0]           # 空间利用率 %
    avail = [272, 230, 230]             # 可用容量 TB
    cols = [C2, C1, C5]
    bars = a.bar(labels, util, color=cols, width=0.58, zorder=3)
    for bar, u, av in zip(bars, util, avail):
        a.text(bar.get_x() + bar.get_width() / 2, u + 1.5,
               f"{u}%", ha="center", va="bottom", fontsize=10.2,
               color=INK, weight="bold", zorder=5)
        a.text(bar.get_x() + bar.get_width() / 2, u / 2,
               f"可用 {av} TB", ha="center", va="center", fontsize=8.8,
               color="white", weight="bold", zorder=5,
               path_effects=[pe.withStroke(linewidth=2.6, foreground=cols[util.index(u)])])
    a.set_ylim(0, 112)
    a.set_ylabel("空间利用率 (%)", fontsize=9.0, color=INK)
    a.set_title("① 冗余方式定可用容量", fontsize=10.4, color=C1, weight="bold", pad=8)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.4, colors=MUTED)

    # --- 右侧：千路月存核算链（全画布坐标画框，四步自上而下）---
    rx, rw = 6.85, 5.9
    steps = [
        ("单路 1 天", "4 Mbps × 86400 s / 8 = 43.2 GB", C1, "#EFF6FF", 5.75),
        ("单路 30 天", "43.2 GB × 30 = 1296 GB ≈ 1.18 TiB", C2, "#ECFDF5", 4.50),
        ("1000 路 30 天", "1296 GB × 1000 ≈ 1.15 PiB", C3, "#FFF7ED", 3.25),
        ("折合节点数", "1.15 PiB / 209 TiB ≈ 6 台 (取 8 留余量)", C4, "#FFF1EE", 2.00),
    ]
    sh = 1.02
    for name, desc, c, fill, sy in steps:
        box(ax, rx, sy, rw, sh, fill, c, lw=1.7)
        txt(ax, rx + 0.25, sy + sh - 0.32, name, size=10.6, weight="bold", color=c, ha="left")
        txt(ax, rx + 0.25, sy + 0.28, desc, size=8.9, color=INK, ha="left")
    # 步骤间向下箭头（走框间自由通道，不穿框）
    for i in range(3):
        top = steps[i][4]           # 当前框左下 y
        nxt = steps[i + 1][4] + sh  # 下一框顶
        arrow(ax, rx + rw / 2, top, rx + rw / 2, nxt, color=MUTED, lw=1.8)

    footer(ax, "注：RAID 6 利用率 (n-2)/n 更高，但只能在单机内容错；EC N+M 牺牲一点空间，换节点级容错与在线扩容。千路月存已达 PiB 级。")
    fig.savefig(os.path.join(OUT, "raid-ec-capacity.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：写入带宽与冷热分层（左侧带宽柱状 + 右侧分层成本）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  带宽与分层：写要扛住 4 Gbps，读要靠冷热分层才不卡",
          "写入是顺序的、回放是随机的——同一台存储「写很稳、读会卡」的根因")

    # --- 左侧：不同路数的并发写入带宽（独立 add_axes）---
    lx, ly, lw, lh = 0.75, 2.05, 5.5, 4.85
    a = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a.set_facecolor("#FFFFFF")
    labels = ["100 路", "500 路", "1000 路", "1200 路"]
    gbps = [0.4, 2.0, 4.0, 4.8]        # 4 Mbps/路
    cols = [C2, C1, C3, C4]
    bars = a.bar(labels, gbps, color=cols, width=0.58, zorder=3)
    for bar, v in zip(bars, gbps):
        a.text(bar.get_x() + bar.get_width() / 2, v + 0.1,
               f"{v} Gbps", ha="center", va="bottom", fontsize=9.6,
               color=INK, weight="bold", zorder=5)
    # 万兆上联可用带宽参考线（legend 标注，不在线间贴文字）
    a.axhline(9.2, color=C5, ls="--", lw=1.6, zorder=4, label="万兆上联可用 ~9.2 Gbps")
    a.legend(loc="upper left", fontsize=8.0, frameon=True)
    a.set_ylim(0, 10.5)
    a.set_ylabel("并发写入带宽 (Gbps)", fontsize=9.0, color=INK)
    a.set_title("① 写入：端口捆绑/万兆上联", fontsize=10.4, color=C1, weight="bold", pad=8)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.6, colors=MUTED)

    # --- 右侧：冷热分层（全画布坐标画三个横条 + 说明）---
    rx, rw = 6.85, 5.9
    txt(ax, rx + rw / 2, 6.68, "② 回放读：按时间局部性分层", size=10.4,
        weight="bold", color=C1)
    tiers = [
        ("热数据 · SSD", "近 7 天，承担绝大多数点播", "8% 容量", C2, "#ECFDF5", 5.45),
        ("温数据 · 机械盘", "30 天内，低成本顺序留存", "32% 容量", C1, "#EFF6FF", 4.15),
        ("冷数据 · 归档", "90 天以上，磁带/低速盘", "60% 容量", C3, "#FFF7ED", 2.85),
    ]
    th = 1.05
    for name, desc, cap, c, fill, sy in tiers:
        box(ax, rx, sy, rw, th, fill, c, lw=1.7)
        txt(ax, rx + 0.25, sy + th - 0.32, name, size=10.6, weight="bold", color=c, ha="left")
        txt(ax, rx + 0.25, sy + 0.27, desc, size=8.6, color=INK, ha="left")
        txt(ax, rx + rw - 0.25, sy + th / 2, cap, size=9.6, weight="bold", color=c, ha="right")
    # 分层成本结论框
    box(ax, rx, 1.70, rw, 0.82, "#F6F8FA", GRID, lw=1.0)
    txt(ax, rx + rw / 2, 2.11,
        "分层约 ¥14.6 万/PB：用机械盘的价，买 SSD 的点播读性能",
        size=8.8, color=INK)

    footer(ax, "注：写入带宽 = 路数 × 单路码率，千路约 4 Gbps，靠多网口捆绑或万兆上联；回放随机读远慢于顺序读，靠 SSD 热分层把点播从机械盘挪走。")
    fig.savefig(os.path.join(OUT, "bandwidth-tiering.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：四类场景共用后端链路（参照 IPC fig4，右侧四场景竖排）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  四类落地场景：同一条「写入 → 资源池 → 冗余自愈 → 检索回放」后端链",
          "平安城市、政法取证、园区扩容、轨交回放，差异只在冗余级别、分层策略与合规强度")

    # 左侧：后端链路主框（四个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.9, 3.2, 3.1
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.5, "后端链路", size=11.4, weight="bold", color=C1)
    chain = ["码流写入", "资源池化", "冗余自愈", "检索回放"]
    for i, s in enumerate(chain):
        # 步长 0.54、起点下移 1.05：最后子框(i=3)底 = oy+0.39，稳在主框内
        yy = oy + oh - 1.05 - i * 0.54
        box(ax, ox + 0.3, yy - 0.18, ow - 0.6, 0.46, "#FFFFFF", C1, lw=1.0)
        txt(ax, ox + ow / 2, yy + 0.05, s, size=8.8, color=INK)
        if i < len(chain) - 1:
            arrow(ax, ox + ow / 2, yy - 0.2, ox + ow / 2, yy - 0.54,
                  color=C1, lw=1.0, ms="-|>")

    # 右侧四个场景框（竖排），y 坐标显式错开，避免与副标题（y≈7.6）冲突：顶边 ≤7.4
    scenes = [
        ("平安城市", "千路级 EC 8+2 集群 · 直存 · 在线扩容", C2, "#ECFDF5", 5.95),
        ("政法取证", "锁定录像升 12+3 · 加密 · 毫秒检索", C4, "#FFF1EE", 4.60),
        ("园区扩容", "不停机加节点 · 自适应限速重构", C3, "#FFF7ED", 3.25),
        ("轨交回放", "SSD 热分层 · 多点并发点播不卡", C5, "#F5F3FF", 1.90),
    ]
    sx, sw, sh = 5.3, 7.45, 1.08
    for name, desc, c, fill, sy in scenes:
        box(ax, sx, sy, sw, sh, fill, c, lw=1.7)
        txt(ax, sx + 0.28, sy + sh - 0.34, name, size=10.2, weight="bold", color=c, ha="left")
        txt(ax, sx + 0.28, sy + 0.34, desc, size=8.8, color=INK, ha="left")
        arrow(ax, ox + ow, oy + oh / 2, sx, sy + sh / 2, color=CGREY, lw=1.2)

    # 底部：输出链路说明条
    bx, by, bw, bh = 0.45, 0.68, 12.3, 0.78
    box(ax, bx, by, bw, bh, "#F6F8FA", GRID, lw=1.0)
    txt(ax, bx + bw / 2, by + bh / 2,
        "统一后端：视频码流  →  资源池写入  →  冗余自愈  →  检索 / 回放 / 下载 / 平台调度",
        size=8.8, color=INK)

    footer(ax, "注：四类场景底层都是同一套后端存储链，差异只在冗余级别（RAID/EC）、分层策略（SSD/机械/归档）与合规强度（GB 35114 加密）。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
