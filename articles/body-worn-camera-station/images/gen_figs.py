# -*- coding: utf-8 -*-
"""执法记录仪与采集站产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system         端—站—管三层系统架构（1.4）
  图2 capacity-endurance  终端参数与单班容量/续航权衡（2.2 算例1/3/4）
  图3 upload-charge       采集站并发上传 + 归档存储 + 充电配电（2.2 算例8/9/11）
  图4 scene-topology      六类场景共用的「现场摄录→归队上传→校验归档→授权取证」证据链（六）

配色、坐标系用法沿用成熟模板（见 content-factory §7.3）：
  - newfig() 把整幅画布当成一个 axes（数据坐标 0~W, 0~H）；
  - footer() 单独开一个 add_axes（用图幅比例），不与绘图区混用 tight 裁剪；
  - 全局字体 Microsoft YaHei；戒用 ↔/✓/≪/⁻¹ 等无字形字符。
"""
import os                      # 拼接路径、读取脚本所在目录
import numpy as np             # 数值计算与数组
import matplotlib              # 绘图库主模块
matplotlib.use("Agg")          # 无界面后端：只输出 PNG
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # 圆角框 / 箭头
import matplotlib.patheffects as pe                            # 文字白描边

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
C1 = "#1F6FEB"   # 主蓝（终端/摄录）
C2 = "#0E9F6E"   # 绿（采集/归档）
C3 = "#E8833A"   # 橙（容量/带宽）
C4 = "#C2410C"   # 深橙（临界/代价）
C5 = "#7C3AED"   # 紫（平台/取证）
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
    ax2.text(0.5, 0.5, s, fontsize=7.4, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：端—站—管三层系统架构
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  端—站—管三层架构：单警执法视音频记录系统（GA/T 947-2015）",
          "前端随身摄录并本机防篡改 → 归队采集站自动上传/校验/充电/清仓 → 平台归档与分级取证")

    # 三列大块：终端 / 采集站 / 管理平台
    cols = [
        ("执法记录仪（终端）", C1, "#EFF6FF",
         ["随身摄录 · H.265 编码", "本机防篡改存储", "水印+哈希+时间戳", "IP68 · 长续航"]),
        ("数据采集站", C2, "#ECFDF5",
         ["自动识别警号", "断点续传+完整性校验", "多仓充电+授权清仓", "归档入库"]),
        ("管理平台", C5, "#F5F3FF",
         ["人员/设备管理", "分级授权检索", "点播+导出审计", "对接公安业务系统"]),
    ]
    bx, bw, gap = 0.45, 3.55, 0.72
    by, bh = 2.55, 3.55
    for i, (name, c, fill, items) in enumerate(cols):
        x = bx + i * (bw + gap)
        box(ax, x, by, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, by + bh - 0.5, name, size=11.0, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = by + bh - 1.15 - j * 0.52
            txt(ax, x + bw / 2, yy, it, size=8.5, color=INK)
    ay = by + bh / 2
    for i in range(2):
        arrow(ax, bx + i * (bw + gap) + bw, ay,
              bx + (i + 1) * (bw + gap), ay, color=MUTED, lw=1.8)
    # 箭头上的阶段说明
    txt(ax, bx + bw + gap / 2, ay + 0.32, "归队上传", size=8.2, color=C2)
    txt(ax, bx + 2 * (bw + gap) - gap / 2, ay + 0.32, "归档入库", size=8.2, color=C5)

    # 底部证据链主轴
    ox, oy, ow, oh = 0.5, 1.25, 12.2, 0.75
    box(ax, ox, oy, ow, oh, "#F6F8FA", CGREY, lw=1.1)
    txt(ax, ox + ow / 2, oy + oh / 2,
        "证据链主轴：现场摄录  →  本机防篡改  →  归队上传  →  完整性校验  →  归档取证（全程不丢 / 不改 / 可追溯）",
        size=8.4, color=INK)

    footer(ax, "注：对应 GA/T 947 四部分——第2部分终端、第3部分管理平台（含采集站）、第4部分数据接口；采集站让证据从终端到归档不经人手，杜绝拷漏与中途被改。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：终端参数与单班容量/续航权衡（左侧柱状 + 右侧测算链）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  终端参数与单班容量/续航：码率、分辨率、续航三者互相牵制",
          "1080P H.265 单班约 18 GB；分辨率翻倍码率约×4，夜视/回传让续航腰斩")

    # --- 左侧：不同编码/分辨率的单班容量柱状（独立 add_axes）---
    lx, ly, lw, lh = 0.7, 2.05, 5.5, 4.85
    a = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a.set_facecolor("#FFFFFF")
    labels = ["1080P\nH.265\n4 Mbps", "1080P\nH.264\n8 Mbps", "2.5K\nH.265\n7 Mbps", "4K\nH.265\n16 Mbps"]
    cap = [18, 36, 32, 72]       # 单班 10h 容量 GB
    cols = [C2, C1, C3, C4]
    bars = a.bar(labels, cap, color=cols, width=0.62, zorder=3)
    for bar, v in zip(bars, cap):
        a.text(bar.get_x() + bar.get_width() / 2, v + 1.2,
               f"{v} GB", ha="center", va="bottom", fontsize=9.8,
               color=INK, weight="bold", zorder=5)
    # 32GB 本机存储参考线
    a.axhline(32, color=C5, ls="--", lw=1.6, zorder=4, label="本机存储 32 GB")
    a.legend(loc="upper left", fontsize=8.0, frameon=True)
    a.set_ylim(0, 84)
    a.set_ylabel("单班录像容量 (GB / 10h)", fontsize=8.8, color=INK)
    a.set_title("① 码率决定单班容量", fontsize=10.2, color=C1, weight="bold", pad=8)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.0, colors=MUTED)

    # --- 右侧：续航测算链（全画布坐标画框）---
    rx, rw = 6.75, 5.95
    txt(ax, rx + rw / 2, 6.72, "② 续航 t = U·Q / P", size=10.2,
        weight="bold", color=C1)
    steps = [
        ("电池能量", "3.7 V × 4000 mAh = 14.8 Wh", C1, "#EFF6FF", 5.45),
        ("理想工况", "功耗 1.3 W → 续航 ≈ 11.4 h", C2, "#ECFDF5", 4.15),
        ("开夜视+回传", "功耗 2.0~2.6 W → 续航 5.7~7.4 h", C4, "#FFF1EE", 2.85),
    ]
    sh = 1.02
    for name, desc, c, fill, sy in steps:
        box(ax, rx, sy, rw, sh, fill, c, lw=1.7)
        txt(ax, rx + 0.25, sy + sh - 0.32, name, size=10.4, weight="bold", color=c, ha="left")
        txt(ax, rx + 0.25, sy + 0.28, desc, size=8.7, color=INK, ha="left")
    for i in range(2):
        top = steps[i][4]
        nxt = steps[i + 1][4] + sh
        arrow(ax, rx + rw / 2, top, rx + rw / 2, nxt, color=MUTED, lw=1.8)
    # 结论框
    box(ax, rx, 1.55, rw, 0.85, "#F6F8FA", GRID, lw=1.0)
    txt(ax, rx + rw / 2, 1.98,
        "标称 ≥10 h 多为理想工况；配单须按最坏功耗重算并备换电",
        size=8.5, color=INK)

    footer(ax, "注：单班容量 C=BT/8（算例1），码率随像素数×帧率近似平方增长（算例3）；续航 t=UQ/P，夜视与4G回传抬高整机功耗，显著缩短实际续航（算例4）。")
    fig.savefig(os.path.join(OUT, "capacity-endurance.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：采集站并发上传 + 归档存储 + 充电配电（三块）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  采集站三本账：并发上传窗口、归档容量、满仓充电功率",
          "30 台并发上传约 1.4 h；90 天归档约 47 TiB；满仓充电约 400 W 需散热配电")

    # --- 左侧：并发上传耗时柱状（独立 add_axes）---
    lx, ly, lw, lh = 0.85, 2.05, 4.20, 4.85
    a = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a.set_facecolor("#FFFFFF")
    labels = ["10 台", "20 台", "30 台", "40 台"]
    hours = [0.47, 0.94, 1.40, 1.87]     # 千兆口有效 112.5 MB/s, 18GB/台
    cols = [C2, C1, C3, C4]
    bars = a.bar(labels, hours, color=cols, width=0.6, zorder=3)
    for bar, v in zip(bars, hours):
        a.text(bar.get_x() + bar.get_width() / 2, v + 0.04,
               f"{v:.2f} h", ha="center", va="bottom", fontsize=9.2,
               color=INK, weight="bold", zorder=5)
    a.axhline(2.0, color=C5, ls="--", lw=1.6, zorder=4, label="交班上传窗口 2 h")
    a.legend(loc="upper left", fontsize=7.8, frameon=True)
    a.set_ylim(0, 2.5)
    a.set_ylabel("全部上传耗时 (h)", fontsize=8.8, color=INK)
    a.set_title("① 并发上传窗口", fontsize=10.2, color=C1, weight="bold", pad=8)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.2, colors=MUTED)

    # --- 右上：归档容量测算链 ---
    rx, rw = 5.25, 7.45
    txt(ax, rx + rw / 2, 6.7, "② 归档容量 C = N × C班 × 留存天数", size=10.0,
        weight="bold", color=C1)
    cap_steps = [
        ("单中队 30 台 × 90 天", "30 × 18 GB × 90 ≈ 47 TiB", C2, "#ECFDF5", 5.25),
        ("RAID6 折算", "裸容量 ≈ 47 / 0.833 ≈ 57 TiB", C1, "#EFF6FF", 4.05),
        ("区县 10 中队", "约 474 TiB，须集中分层归档", C4, "#FFF1EE", 2.85),
    ]
    sh = 1.0
    for name, desc, c, fill, sy in cap_steps:
        box(ax, rx, sy, rw, sh, fill, c, lw=1.6)
        txt(ax, rx + 0.25, sy + sh - 0.3, name, size=9.9, weight="bold", color=c, ha="left")
        txt(ax, rx + 0.25, sy + 0.27, desc, size=8.5, color=INK, ha="left")
    for i in range(2):
        arrow(ax, rx + rw / 2, cap_steps[i][4],
              rx + rw / 2, cap_steps[i + 1][4] + sh, color=MUTED, lw=1.6)

    # --- 右下：充电功率结论条 ---
    box(ax, rx, 1.5, rw, 0.88, "#F6F8FA", GRID, lw=1.0)
    txt(ax, rx + rw / 2, 1.94,
        "③ 满仓充电 P = N·UI/η：30 仓约 400 W，几乎全变热量 → 留散热风道 + 0.5 kW/站配电",
        size=8.3, color=INK)

    footer(ax, "注：上传耗时 t=N·C/B（算例8，千兆口有效约112.5MB/s）；归档按RAID6利用率(n-2)/n折算（算例9）；充电损耗与线损使满仓机柜成为400W级热源（算例11）。")
    fig.savefig(os.path.join(OUT, "upload-charge.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用的证据链（左侧链主轴 + 右侧六场景两列三行）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类场景共用同一条证据链：现场摄录 → 归队上传 → 校验归档 → 授权取证",
          "交警 / 治安 / 城管 / 办案区 / 应急 / 法院安检，差异只在终端数量、上传窗口与归档留存")

    # 左侧：证据链主轴（五个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.35, 3.15, 3.65
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.45, "证据链主轴", size=11.2, weight="bold", color=C1)
    chain = ["现场摄录", "本机防篡改", "归队上传", "校验归档", "授权取证"]
    step, subh = 0.56, 0.42
    top_c = oy + oh - 1.15          # 第一个子框中心 y
    for i, s in enumerate(chain):
        yc = top_c - i * step
        box(ax, ox + 0.25, yc - subh / 2, ow - 0.5, subh, "#FFFFFF", C1, lw=1.0)
        txt(ax, ox + ow / 2, yc, s, size=8.6, color=INK)
        if i < len(chain) - 1:
            # 箭头只走子框之间的自由通道（当前框底 → 下一框顶），不穿框压字
            arrow(ax, ox + ow / 2, yc - subh / 2 - 0.01,
                  ox + ow / 2, yc - step + subh / 2 + 0.01, color=C1, lw=1.0)

    # 右侧六个场景框（两列三行），y 顶边 ≤7.4 给副标题让位
    scenes = [
        ("交警路面执法", "处罚争议可回溯", C2, "#ECFDF5"),
        ("治安巡逻盘查", "广角记录现场全貌", C1, "#EFF6FF"),
        ("城管综合执法", "冲突现场可信取证", C3, "#FFF7ED"),
        ("办案区讯问", "全程留痕防补录", C4, "#FFF1EE"),
        ("应急处突", "IP68+夜视全天候", C5, "#F5F3FF"),
        ("法院/安检", "GA/T 947.4 对接", C2, "#ECFDF5"),
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
        txt(ax, x + 0.25, y + 0.34, desc, size=8.6, color=INK, ha="left")

    footer(ax, "注：六类场景底层都是同一条端—站—管证据链，差异只在终端数量、上传窗口（算例8）与归档留存策略（算例9、14）；核心目标是证据「不丢、不改、可追溯」。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
