# -*- coding: utf-8 -*-
"""电梯楼层控制器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system    识别—控制—管理四层 + 单列消防通道（1.4）
  图2 auth-delay     楼层位图授权表 + 刷卡时延预算链（2.2 算例1/2）
  图3 bus-fire       RS-485 总线取舍 + 消防强切两路径（2.2 算例4/6）
  图4 scene-topology 六类场景共用的授权骨架（五）

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
C1 = "#1F6FEB"   # 主蓝（识别/读头）
C2 = "#0E9F6E"   # 绿（授权/使能）
C3 = "#E8833A"   # 橙（总线/时延）
C4 = "#C2410C"   # 深橙（消防/临界）
C5 = "#7C3AED"   # 紫（平台/管理层）
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
    ax2.text(0.5, 0.5, s, fontsize=7.3, color=MUTED, ha="center", va="center",
             fontfamily="Microsoft YaHei", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, ls="-", ms="-|>", zorder=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：识别—控制—管理四层 + 单列消防通道
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  梯控四层架构 + 最高优先级消防通道",
          "识别 → 控制 → 管理三层授权闭环；FAS 火警经独立硬线直解全楼层并迫降，不经平台软件")

    # 三列主块：识别层 / 控制层 / 管理层
    cols = [
        ("识别层", C1, "#EFF6FF",
         ["轿内 COP 读卡器", "人脸 / 二维码终端", "厅外目的层终端", "CPU 卡 + OSDP 加密"]),
        ("控制层", C2, "#ECFDF5",
         ["梯控主板本地判定", "楼层扩展板(干接点)", "三级授权表缓存", "离线可用 + 事件留痕"]),
        ("管理层", C5, "#F5F3FF",
         ["统一身份源(HR/门禁)", "发卡与授权下发", "事件审计 / 等保日志", "对接一卡通 / IoT"]),
    ]
    bx, bw, gap = 0.45, 3.55, 0.72
    by, bh = 2.65, 3.30
    for i, (name, c, fill, items) in enumerate(cols):
        x = bx + i * (bw + gap)
        box(ax, x, by, bw, bh, fill, c, lw=2.0)
        txt(ax, x + bw / 2, by + bh - 0.48, name, size=11.0, weight="bold", color=c)
        for j, it in enumerate(items):
            yy = by + bh - 1.05 - j * 0.50
            txt(ax, x + bw / 2, yy, it, size=8.4, color=INK)
    ay = by + bh / 2
    for i in range(2):
        arrow(ax, bx + i * (bw + gap) + bw, ay,
              bx + (i + 1) * (bw + gap), ay, color=MUTED, lw=1.8)
    txt(ax, bx + bw + gap / 2, ay + 0.30, "刷卡/鉴权", size=7.9, color=C1)
    txt(ax, bx + 2 * (bw + gap) - gap / 2, ay + 0.30, "授权下发/回传", size=7.9, color=C5)

    # 顶部消防通道（单列，绕过三列）
    fx, fy, fw, fh = 0.45, 6.35, 12.3, 0.62
    box(ax, fx, fy, fw, fh, "#FFF1EE", C4, lw=1.8)
    txt(ax, fx + fw / 2, fy + fh / 2,
        "消防通道（独立硬线）：FAS 火警 → 梯控全楼层失电释放（≈30 ms）+ 电梯迫降 → 不经平台、不由软件代理",
        size=8.9, color=C4, weight="bold")
    # 消防线向下点到控制层的示意（短竖线，走列间通道）
    arrow(ax, 6.6, fy, 6.6, by + bh + 0.05, color=C4, lw=1.6, ls="--")

    # 底部责任边界主轴
    ox, oy, ow, oh = 0.5, 1.35, 12.2, 0.92
    box(ax, ox, oy, ow, oh, "#F6F8FA", CGREY, lw=1.1)
    txt(ax, ox + ow / 2, oy + oh - 0.28,
        "责任边界：门禁/读头/控制器/授权平台/干接点接口 = 安防集成方",
        size=8.4, color=INK)
    txt(ax, ox + ow / 2, oy + 0.26,
        "轿厢布线 / 楼层按键回路 / 安全回路 / 消防员服务 / 机械曳引 = 电梯 OEM 或授权维保（特种设备）",
        size=8.0, color=MUTED)

    footer(ax, "注：依据 GB 55029-2022、GB 50348-2018、GB 50396-2007（9.0.1 紧急逃生联动）、GB/T 7588.1-2020；消防硬线是本图与门禁系统最关键的区别。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：楼层位图授权表（左）+ 刷卡时延预算链（右）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  授权位图压缩 + 刷卡时延预算：容量不是瓶颈，一致性才是",
          "每用户约 7 B 存楼层/时段/群组；本地判定把一次刷卡压到约 240 ms")

    # --- 左侧：授权表结构示意（三行位图条 + 容量结论）---
    lx, ly, lw = 0.55, 1.65, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 楼层位图授权表（每用户约 7 B）", size=10.2,
        weight="bold", color=C1)
    users = [("用户 A", "0010 1000 0000 …", C2, 5.55),
             ("用户 B", "1111 1111 1100 …", C3, 4.45),
             ("用户 C", "0000 0001 1000 …", C5, 3.35)]
    for name, bits, c, yy in users:
        box(ax, lx, yy, lw, 0.92, "#FFFFFF", c, lw=1.5)
        txt(ax, lx + 0.15, yy + 0.62, name, size=9.6, weight="bold", color=c, ha="left")
        txt(ax, lx + 1.35, yy + 0.62, bits, size=9.4, color=INK, ha="left")
        txt(ax, lx + 0.15, yy + 0.24, "楼层位图 4 B + 时段索引 1 B + 群组号 2 B",
            size=7.6, color=MUTED, ha="left")
    box(ax, lx, 2.05, lw, 0.88, "#ECFDF5", C2, lw=1.4)
    txt(ax, lx + lw / 2, 2.49,
        "5000 用户授权表 ≈ 34 KB —— 容量从来不是瓶颈",
        size=8.8, color=INK, weight="bold")

    # --- 右侧：时延预算链（四个阶段横条 + 合计）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② 一次刷卡的时延预算链", size=10.2,
        weight="bold", color=C3)
    stages = [
        ("读卡", "CPU 卡交互 200 ms", C1, 5.55),
        ("鉴权", "本地查表 10 ms", C2, 4.55),
        ("总线", "485 往返 15 ms", C3, 3.55),
        ("输出", "继电器动作 15 ms", C5, 2.55),
    ]
    sh = 0.82
    for name, desc, c, yy in stages:
        box(ax, rx, yy, rw, sh, "#F6F8FA", c, lw=1.4)
        txt(ax, rx + 0.2, yy + sh / 2, name, size=9.6, weight="bold", color=c, ha="left")
        txt(ax, rx + 1.15, yy + sh / 2, desc, size=8.8, color=INK, ha="left")
    for i in range(3):
        arrow(ax, rx + rw / 2, stages[i][3],
              rx + rw / 2, stages[i + 1][3] + sh, color=MUTED, lw=1.3)
    box(ax, rx, 1.55, rw, 0.82, "#FFF7ED", C3, lw=1.6)
    txt(ax, rx + rw / 2, 1.96,
        "合计 ≈ 240 ms < 1 s，用户无感（回平台在线鉴权则引入断网失效）",
        size=8.5, color=C4, weight="bold")

    footer(ax, "注：算例1 位图授权 S=N·S_user 约 34 KB；算例2 时延 t=t_read+t_auth+t_bus+t_out 约 240 ms；本地判定是离线可用的前提。")
    fig.savefig(os.path.join(OUT, "auth-delay.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：RS-485 总线取舍（左）+ 消防强切两路径（右）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  总线带载与消防强切：一个要「稳」，一个要「硬」",
          "RS-485 33 节点需分段或换收发器；消防硬线 30 ms，软件代理秒级且带单点故障")

    # --- 左侧：RS-485 速率—距离与节点 ---
    lx, ly, lw, lh = 0.7, 2.05, 5.5, 4.85
    a = fig.add_axes([lx / W, ly / H, lw / W, lh / H])
    a.set_facecolor("#FFFFFF")
    labels = ["9600\nbps", "19200\nbps", "38400\nbps", "115200\nbps"]
    dist = [1200, 900, 400, 100]     # 典型可靠距离 m（工程基准）
    cols = [C2, C1, C3, C4]
    bars = a.bar(labels, dist, color=cols, width=0.6, zorder=3)
    for bar, v in zip(bars, dist):
        a.text(bar.get_x() + bar.get_width() / 2, v + 25,
               f"{v} m", ha="center", va="bottom", fontsize=9.4,
               color=INK, weight="bold", zorder=5)
    a.axhline(50, color=C5, ls="--", lw=1.5, zorder=4, label="井道典型长度 50 m")
    a.legend(loc="upper right", fontsize=7.8, frameon=True)
    a.set_ylim(0, 1400)
    a.set_ylabel("可靠通信距离 (m)", fontsize=8.8, color=INK)
    a.set_title("① 速率越高，距离越短（井道要降速）", fontsize=10.0, color=C1, weight="bold", pad=8)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.2, colors=MUTED)

    # --- 右侧：消防强切两路径对比 ---
    rx, rw = 6.75, 5.85
    txt(ax, rx + rw / 2, 6.62, "② 消防强切：两条路径的差别", size=10.2,
        weight="bold", color=C4)
    # 硬线路径（绿）
    box(ax, rx, 4.55, rw, 1.45, "#ECFDF5", C2, lw=1.8)
    txt(ax, rx + 0.2, 5.75, "硬线（推荐）", size=10.2, weight="bold", color=C2, ha="left")
    txt(ax, rx + 0.2, 5.25, "FAS 干接点 → 输入防抖 20 ms → 继电器失电 10 ms",
        size=8.7, color=INK, ha="left")
    txt(ax, rx + 0.2, 4.78, "≈ 30 ms，远小于 2 s；不经过平台，无单点故障",
        size=8.7, color=C2, ha="left", weight="bold")
    # 软件代理路径（红）
    box(ax, rx, 2.72, rw, 1.45, "#FFF1EE", C4, lw=1.8)
    txt(ax, rx + 0.2, 3.92, "软件代理（禁止）", size=10.2, weight="bold", color=C4, ha="left")
    txt(ax, rx + 0.2, 3.42, "FAS → 平台 → 网络 → 梯控（排队/丢包/平台故障）",
        size=8.7, color=INK, ha="left")
    txt(ax, rx + 0.2, 2.95, "秒级甚至失效 —— 违反 GB 50396 9.0.1",
        size=8.7, color=C4, ha="left", weight="bold")
    # 结论条
    box(ax, rx, 1.55, rw, 0.82, "#F6F8FA", GRID, lw=1.0)
    txt(ax, rx + rw / 2, 1.96,
        "33 节点 > 32：分段总线或换 1/4 负载收发器（可挂 128 点）",
        size=8.4, color=INK)

    footer(ax, "注：算例4 RS-485 32 节点/1200 m@9600bps，33 节点需分段；算例6 消防硬切 20+10ms≈30ms，远小于 2s 硬指标。")
    fig.savefig(os.path.join(OUT, "bus-fire.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用的授权骨架（左链 + 右六场景两列三行）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类场景共用同一套授权骨架：身份源 → 授权表 → 楼层使能 → 事件审计",
          "住宅 / 写字楼 / 酒店 / 医院 / 数据中心 / 工业园区，差异只在识别方式、可达层与访客规则")

    # 左侧：授权骨架主轴（五个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.35, 3.15, 3.65
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.45, "授权骨架", size=11.2, weight="bold", color=C1)
    chain = ["统一身份源", "三级授权表", "刷卡本地判定", "楼层使能输出", "事件留痕复核"]
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
        ("住宅小区", "一层一卡，访客临时授权", C2, "#ECFDF5"),
        ("写字楼", "群组分层，DCS 分流", C1, "#EFF6FF"),
        ("酒店", "房卡即梯卡，随入住回收", C3, "#FFF7ED"),
        ("医院", "时段探视，消防零障碍", C4, "#FFF1EE"),
        ("数据中心", "双因素 + 等保审计", C5, "#F5F3FF"),
        ("工业园区", "访客限时限层，动线分离", C2, "#ECFDF5"),
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

    footer(ax, "注：六类场景底层都是同一套身份源—授权—使能—审计骨架，差异只在识别方式、可达层策略、访客规则与消防联动细节。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
