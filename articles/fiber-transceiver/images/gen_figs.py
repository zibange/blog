# -*- coding: utf-8 -*-
"""光纤收发器产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system    收发器链路架构 + 三种组网形态（1.4）
  图2 link-budget    链路预算瀑布分解（左）+ 单模/多模距离对比（右）（算例 1/2/5）
  图3 bidi-video     BIDI 波长交叉配对（左）+ 两类设备验收对比（右）（算例 6/9/10）
  图4 scene-topology 六类场景共用骨架（五）

配色、坐标系用法沿用成熟模板（见 content-factory §7.3）：
  - newfig() 把整幅画布当成一个 axes（数据坐标 0~W, 0~H）；
  - footer() 单独开一个 add_axes（用图幅比例），不与绘图区混用 tight 裁剪；
  - 嵌入式柱状图用 fig.add_axes([left,bottom,width,height])（图幅比例定位）；
  - 全局字体 Microsoft YaHei；戒用 ↔ / ✓ / ≪ 等无字形字符（用文字/箭头代替）。

Python 教学要点（本脚本刻意写清楚，方便当教学材料）：
  - os.path.dirname(os.path.abspath(__file__))：脚本所在目录，图片输出到本目录；
    用 __file__ 而非裸相对路径，保证从任意工作目录运行都能正确落盘。
  - matplotlib.use("Agg")：无界面后端，自动化/服务器环境只出 PNG 不开窗口。
  - FancyBboxPatch / FancyArrowPatch：画圆角框与带箭头连线。
  - add_axes([left,bottom,width,height], ...) 用的是「图幅比例 0~1」而非数据坐标，
    所以要把数据坐标的 lx/W、2.95/H 换算成 0~1 比例再传进去——
    这是「两种坐标系不要混用」的关键：主绘图区用数据坐标 0~W/0~H，
    嵌入式小图用图幅比例，二者通过除以 W、H 换算衔接。
  - a.set_yscale("log")：对数纵轴，用于跨数量级对比（550 m vs 85 km）。
"""
import os
import matplotlib
matplotlib.use("Agg")  # 必须在 import pyplot 之前设置后端
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# __file__ 是当前脚本路径；abspath 取绝对路径；dirname 取所在文件夹
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 13.2, 8.6

# ---- light 主题配色（浅底深字，适配浅色 IDE 主题）----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#5A6570"
GRID = "#E3E8EE"
C1 = "#1F6FEB"   # 主蓝（发射 / 以太网型）
C2 = "#0E9F6E"   # 绿（接收 / 预算充足）
C3 = "#E8833A"   # 橙（多模 / 短距 / 固定损耗）
C4 = "#C2410C"   # 深橙（陷阱 / 告警 / 余量）
C5 = "#7C3AED"   # 紫（光纤 / BIDI / 视频型）
CGREY = "#CBD2D9"


def newfig():
    """整幅画布当成一个坐标轴：数据坐标 0~W / 0~H，隐藏刻度与轴线。"""
    fig = plt.figure(figsize=(W / 1.32, H / 1.32), dpi=140, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=1.4, r=0.18, alpha=1.0, ls="-"):
    """圆角矩形：x/y 为左下角，w/h 为宽高，fc/ec 为填充与描边色。"""
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
    """图标题 + 副标题。顶边控制在 ~7.4 以内，避免与其他元素冲突。"""
    txt(ax, W / 2, H - 0.52, t, size=14.0, weight="bold", ha="center")
    if sub:
        txt(ax, W / 2, H - 1.00, sub, size=8.6, color=MUTED, ha="center")


def footer(ax, s):
    """底部说明条：单独开一个 axes（图幅比例），避免与绘图区坐标系混用。"""
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
    """带箭头连线：ms 是 arrowstyle，mutation_scale 控制箭头大小。"""
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=ms, mutation_scale=11,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0", zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def bidi_arrow(ax, x1, y1, x2, y2, color=C5, lw=2.0):
    """双向箭头：用 '<|-|>' 样式，表示单纤上的双向光流。"""
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="<|-|>", mutation_scale=12,
                        linewidth=lw, color=color,
                        connectionstyle="arc3,rad=0.0", zorder=4,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


# ============================================================
# 图 1：收发器链路架构 + 三种组网形态
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  光纤收发器链路架构 + 三种组网形态",
          "左端电口设备 → 收发器 → 光纤链路 → 收发器 → 右端电口设备；链路上逐项标注损耗")

    # --- 上半部：链路主通道（自左向右六个节点）---
    # 节点框顶边 = ny + 1.15，需低于副标题(y=7.6)留出间距，故 ny 取 5.95
    ny = 5.95
    nodes = [
        (0.55, 1.85, "电口设备", "交换机 / 摄像机\nRJ45 电口", C1, "#EFF6FF"),
        (2.85, 1.95, "收发器 A", "电口 → 光口\n发射 Tx", C5, "#F5F3FF"),
        (5.30, 2.55, "光纤链路", "单模 / 多模\n逐项扣损耗", C3, "#FFF7ED"),
        (8.35, 1.95, "收发器 B", "光口 → 电口\n接收 Rx", C5, "#F5F3FF"),
        (10.75, 1.85, "电口设备", "交换机 / 服务器\nRJ45 电口", C1, "#EFF6FF"),
    ]
    for x, w, name, desc, c, fill in nodes:
        box(ax, x, ny, w, 1.15, fill, c, lw=1.8)
        txt(ax, x + w / 2, ny + 0.78, name, size=10.2, weight="bold", color=c)
        txt(ax, x + w / 2, ny + 0.32, desc, size=7.8, color=INK)
    # 节点间箭头
    arrow(ax, 2.40, ny + 0.58, 2.85, ny + 0.58, color=C1, lw=1.6)
    arrow(ax, 4.80, ny + 0.58, 5.30, ny + 0.58, color=C5, lw=1.6)
    arrow(ax, 7.85, ny + 0.58, 8.35, ny + 0.58, color=C3, lw=1.6)
    arrow(ax, 10.30, ny + 0.58, 10.75, ny + 0.58, color=C5, lw=1.6)

    # --- 下半部：三种组网形态（三列）---
    base = 3.15
    txt(ax, W / 2, base + 2.35, "三种组网形态", size=11.0, weight="bold", color=INK)
    forms = [
        (0.55, "点对点（1 光 1 电 ×2）", ["两端各一台，光纤直连", "最简单可靠", "坏一台整条链路断"], C1, "#EFF6FF"),
        (4.85, "星型汇聚（机架式插卡）", ["前端多台 → 中心机架", "集中供电与网管", "中心单点影响面大"], C2, "#ECFDF5"),
        (9.15, "单纤双向 BIDI", ["一根光纤跑双向", "1310/1550 交叉配对", "省一半光纤，备件成对"], C5, "#F5F3FF"),
    ]
    for x, name, items, c, fill in forms:
        box(ax, x, base, 3.55, 2.05, fill, c, lw=1.8)
        txt(ax, x + 1.78, base + 1.68, name, size=9.8, weight="bold", color=c)
        for i, it in enumerate(items):
            txt(ax, x + 0.22, base + 1.18 - i * 0.42, it, size=8.2, color=INK, ha="left")

    footer(ax, "注：以太网型收发器按 YD/T 1528-2016、IEEE 802.3；安防视频光端机按 GA/T 1178-2014。链路能否开通由链路预算决定（算例 1）。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：链路预算瀑布分解（左）+ 单模/多模距离对比（右，对数轴）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  链路预算分解 + 单模/多模距离对比",
          "左：发射功率逐项扣减到接收灵敏度（瀑布分解）；右：不同介质/波长的距离跨数量级（对数轴）")

    # --- 左侧：链路预算瀑布分解（五段框）---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 链路预算瀑布分解（算例 1，单位 dBm/dB）",
        size=10.0, weight="bold", color=C4)
    steps = [
        ("发射功率 P_Tx", "-9 dBm（厂商口径）", C1, 5.62),
        ("固定损耗 L_fixed", "-1.4 dB（4 熔接+2 连接）", C3, 4.72),
        ("线路 + 余量", "-5.6 dB(16km) -3 dB 余量", C4, 3.82),
        ("接收灵敏度 P_Rx", "-32 dBm（灵敏度门限）", C2, 2.92),
    ]
    for name, val, c, yy in steps:
        box(ax, lx, yy, lw, 0.78, "#F6F8FA", c, lw=1.5)
        txt(ax, lx + 0.18, yy + 0.39, name, size=9.2, weight="bold", color=c, ha="left")
        txt(ax, lx + lw - 0.18, yy + 0.39, val, size=8.8, weight="bold", color=INK, ha="right")
        if yy > 3.0:
            arrow(ax, lx + lw / 2, yy - 0.02, lx + lw / 2, yy - 0.88, color=c, lw=1.2)
    box(ax, lx, 1.62, lw, 1.0, "#ECFDF5", C2, lw=1.8)
    txt(ax, lx + lw / 2, 2.28,
        "L_可用 = -9 -(-32) -1.4 -3 = 18.6 dB",
        size=9.2, weight="bold", color=C2)
    txt(ax, lx + lw / 2, 1.90,
        "16 km 只占 5.6 dB 线路损耗 → 余量充足、一次开通",
        size=8.0, color=INK)

    # --- 右侧：距离对比（嵌入式对数柱状图）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② 不同介质/波长的距离（纵轴 km，对数）",
        size=10.0, weight="bold", color=C5)
    # axes 底部抬到 3.05 给 x 轴两行标签腾位（标签落在 ~2.5-3.0，高于结论框顶 2.40），
    # 高度缩到 3.00，避免标签被下方橙色结论框压住（图幅比例换算：除以 W/H）
    a = fig.add_axes([rx / W, 3.05 / H, rw / W, 3.00 / H])
    a.set_facecolor("#FFFFFF")
    # 用米统一换算成 km 后画：- 多模 OM3 千兆 0.55 km、万兆 0.3 km；
    #   单模 1310 nm 约 53 km、1550 nm 约 85 km（算例 1、2、5）
    labels = ["多模 OM3\n千兆 550m", "多模 OM3\n万兆 300m", "单模1310\n约53km", "单模1550\n约85km"]
    vals = [0.55, 0.30, 53.0, 85.0]
    x = range(len(vals))
    bars = a.bar(x, vals, 0.56, color=[C3, C3, C1, C5], zorder=3)
    for bar, lab in zip(bars, ["0.55", "0.30", "53", "85"]):
        a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.15,
               lab, ha="center", va="bottom", fontsize=9.0, color=INK,
               weight="bold", zorder=5)
    a.set_yscale("log")
    a.set_ylim(0.2, 400)
    a.set_xticks(list(x))
    a.set_xticklabels(labels, fontsize=7.9, color=INK)
    # 去竖排 ylabel（历史上多次被裁），单位「km」写进小标题
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.0, colors=MUTED)
    box(ax, rx, 1.55, rw, 0.85, "#FFF7ED", C3, lw=1.6)
    txt(ax, rx + rw / 2, 2.16,
        "多模/单模混接 = 假通：模场失配、余量近零（算例 5）",
        size=8.2, color=C3, weight="bold")
    txt(ax, rx + rw / 2, 1.78,
        "距离是预算算出来的：d = L_可用 / 每公里衰减系数",
        size=7.8, color=INK)

    footer(ax, "注：距离取工程基准/厂商口径的演示估算，未独立复现；实际以 OTDR 实测链路损耗与误码测试为准。")
    fig.savefig(os.path.join(OUT, "link-budget.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：BIDI 波长交叉配对（左）+ 两类设备验收对比（右）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  BIDI 波长配对 + 两类设备验收对比",
          "左：单纤双向 1310/1550 严格交叉、备件成对；右：以太网型 vs 安防视频光端机是两套标准与指标")

    # --- 左侧：BIDI 波长交叉配对 ---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 单纤双向 BIDI 波长交叉配对（算例 6）",
        size=10.0, weight="bold", color=C5)
    # A 端框
    box(ax, lx, 4.55, 2.05, 1.45, "#EFF6FF", C1, lw=1.8)
    txt(ax, lx + 1.02, 5.68, "A 端收发器", size=9.8, weight="bold", color=C1)
    txt(ax, lx + 1.02, 5.22, "发 1310 nm", size=8.8, color=C4, weight="bold")
    txt(ax, lx + 1.02, 4.82, "收 1550 nm", size=8.8, color=C5, weight="bold")
    # B 端框
    bx2 = lx + lw - 2.05
    box(ax, bx2, 4.55, 2.05, 1.45, "#F5F3FF", C5, lw=1.8)
    txt(ax, bx2 + 1.02, 5.68, "B 端收发器", size=9.8, weight="bold", color=C5)
    txt(ax, bx2 + 1.02, 5.22, "发 1550 nm", size=8.8, color=C5, weight="bold")
    txt(ax, bx2 + 1.02, 4.82, "收 1310 nm", size=8.8, color=C4, weight="bold")
    # 中间单纤双向箭头（两条错位，分别标波长）
    bidi_arrow(ax, lx + 2.10, 5.35, bx2 - 0.05, 5.35, color=C4, lw=1.8)
    txt(ax, (lx + bx2 + 2.05) / 2, 5.62, "1310 nm  →", size=8.0, color=C4)
    bidi_arrow(ax, lx + 2.10, 4.88, bx2 - 0.05, 4.88, color=C5, lw=1.8)
    txt(ax, (lx + bx2 + 2.05) / 2, 4.62, "←  1550 nm", size=8.0, color=C5)
    box(ax, lx, 2.55, lw, 1.55, "#FFF1EE", C4, lw=1.8)
    txt(ax, lx + lw / 2, 3.68, "陷阱：备件必须按方向成对备", size=9.4, weight="bold", color=C4)
    txt(ax, lx + lw / 2, 3.24, "拿错方向 → 两端同波长发 → 链路不通", size=8.4, color=INK)
    txt(ax, lx + lw / 2, 2.85, "CWDM 更细：1471~1611 nm 按波道一一对应", size=8.0, color=MUTED)
    box(ax, lx, 1.55, lw, 0.80, "#F6F8FA", CGREY, lw=1.3)
    txt(ax, lx + lw / 2, 1.95, "省一半光纤，代价是波长/方向严格配对", size=8.2, color=INK)

    # --- 右侧：两类设备验收对比（表格式两列）---
    rx, rw = 7.05, 5.55
    txt(ax, rx + rw / 2, 6.62, "② 以太网收发器 vs 安防视频光端机（算例 9/10）",
        size=9.6, weight="bold", color=C1)
    # 表头
    col1, col2 = 2.35, 2.95
    box(ax, rx, 5.72, col1, 0.68, "#1F2933", INK, lw=1.0)
    txt(ax, rx + col1 / 2, 6.06, "对比维度", size=9.2, weight="bold", color="#FFFFFF")
    box(ax, rx + col1, 5.72, 1.42, 0.68, C1, C1, lw=1.0)
    txt(ax, rx + col1 + 0.71, 6.06, "以太网型", size=9.0, weight="bold", color="#FFFFFF")
    box(ax, rx + col1 + 1.42, 5.72, col2 - 1.42, 0.68, C5, C5, lw=1.0)
    txt(ax, rx + col1 + 1.42 + (col2 - 1.42) / 2, 6.06, "视频光端机", size=9.0, weight="bold", color="#FFFFFF")
    rows = [
        ("执行标准", "YD/T 1528-2016", "GA/T 1178-2014"),
        ("业务口", "RJ45 电口", "BNC+音频+数据+网口"),
        ("验收指标", "吞吐/丢包/误码", "S/N≥60dB、DG/DP≤2%"),
        ("单路开销", "4 Mbps(H.265)", "约 270 Mbps(SDI)"),
        ("拓扑", "点对点/汇聚", "点对点/星型"),
    ]
    # 行高缩到 0.62：5 行最后一行底边 = 5.04-4*0.62 = 2.56，高于下方橙框顶 2.33
    rh = 0.62
    for i, (dim, a_val, b_val) in enumerate(rows):
        yy = 5.04 - i * rh
        fill = "#FFFFFF" if i % 2 == 0 else "#F6F8FA"
        box(ax, rx, yy, col1, rh, fill, GRID, lw=0.8)
        txt(ax, rx + 0.12, yy + rh / 2, dim, size=8.6, weight="bold", color=INK, ha="left")
        box(ax, rx + col1, yy, 1.42, rh, fill, GRID, lw=0.8)
        txt(ax, rx + col1 + 0.71, yy + rh / 2, a_val, size=7.7, color=C1, ha="center")
        box(ax, rx + col1 + 1.42, yy, col2 - 1.42, rh, fill, GRID, lw=0.8)
        txt(ax, rx + col1 + 1.42 + (col2 - 1.42) / 2, yy + rh / 2, b_val,
            size=7.5, color=C5, ha="center")
    # 橙色框顶部 = 1.45+0.88 = 2.33，低于表格最后一行底边 2.56，留 0.23 间距
    box(ax, rx, 1.45, rw, 0.88, "#FFF7ED", C3, lw=1.6)
    txt(ax, rx + rw / 2, 2.00, "JT/T 830-2012《视频光端机》已废止（2022-07-01）",
        size=8.4, color=C3, weight="bold")
    txt(ax, rx + rw / 2, 1.66, "招标若仍引用旧标准，是废标与验收纠纷隐患", size=7.9, color=INK)

    footer(ax, "注：波长、接口与指标取自 YD/T 1528-2016、GA/T 1178-2014 等公开标准口径；两类设备业务模型不同，验收表不可混用。")
    fig.savefig(os.path.join(OUT, "bidi-video.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用骨架（左链 + 右六场景两列三行）
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类场景共用一套骨架：电口设备 → 收发器 → 光纤 → 收发器 → 电口设备",
          "园区跨楼 / 视频回传 / 强电磁现场 / 单纤租纤 / 长距中继 / 室外无人值守，差异只在距离、波长、业务与环境")

    # 左侧：共用骨架主轴（五个子步骤竖排）
    ox, oy, ow, oh = 0.45, 2.35, 3.15, 3.65
    box(ax, ox, oy, ow, oh, "#EFF6FF", C1, lw=2.0)
    txt(ax, ox + ow / 2, oy + oh - 0.45, "共用骨架", size=11.2, weight="bold", color=C1)
    chain = ["电口设备接入", "电/光转换 Tx", "光纤链路传输", "光/电转换 Rx", "对端设备输出"]
    step, subh = 0.56, 0.42
    top_c = oy + oh - 1.15
    for i, s in enumerate(chain):
        yc = top_c - i * step
        box(ax, ox + 0.25, yc - subh / 2, ow - 0.5, subh, "#FFFFFF", C1, lw=1.0)
        txt(ax, ox + ow / 2, yc, s, size=8.5, color=INK)
        if i < len(chain) - 1:
            arrow(ax, ox + ow / 2, yc - subh / 2 - 0.01,
                  ox + ow / 2, yc - step + subh / 2 + 0.01, color=C1, lw=1.0)

    # 右侧六个场景框（两列三行）
    scenes = [
        ("园区跨楼互联", "单模点对点，预算富余", C2, "#ECFDF5"),
        ("视频监控回传", "1光8电 或 视频光端机", C5, "#F5F3FF"),
        ("强电磁工业现场", "光纤隔离，无地环流", C4, "#FFF1EE"),
        ("单纤/租纤场景", "BIDI 省一半纤芯", C1, "#EFF6FF"),
        ("长距骨干/中继", "1550nm + 分段中继", C3, "#FFF7ED"),
        ("室外/无人值守", "宽温+防雷+PoE", C2, "#ECFDF5"),
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
        txt(ax, x + 0.25, y + 0.34, desc, size=8.3, color=INK, ha="left")

    footer(ax, "注：六类场景底层都是同一套「电口—转换—光纤—转换—电口」骨架，差异只在距离、波长、业务类型与环境等级。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1(); print("fig1 ok")
    fig2(); print("fig2 ok")
    fig3(); print("fig3 ok")
    fig4(); print("fig4 ok")
