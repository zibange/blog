# -*- coding: utf-8 -*-
"""无线网桥产品综述 —— 四张矢量示意图

图序严格按正文出现顺序：
  图1 arch-system          链路组成 + 三种组网形态（1.4）
  图2 link-budget-fresnel  链路预算瀑布（左）+ 菲涅尔区剖面与地球曲率（右）（算例 1/2/4/5）
  图3 antenna-eirp         天线增益/波束宽权衡（左）+ EIRP 法规天花板（右）（算例 6/7/9）
  图4 scene-topology       六类场景共用骨架（五）

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
"""
import os
import matplotlib
matplotlib.use("Agg")  # 必须在 import pyplot 之前设置后端
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Arc

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
C1 = "#1F6FEB"   # 主蓝（发射 / 点对点）
C2 = "#0E9F6E"   # 绿（接收 / 净空充足）
C3 = "#E8833A"   # 橙（损耗 / 曲率 / 障碍）
C4 = "#C2410C"   # 深橙（陷阱 / 告警 / 超标）
C5 = "#7C3AED"   # 紫（无线链路 / 天线 / PTMP）
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


def antenna(ax, x, y, scale=1.0, color=C5):
    """画一个小抛物面天线剪影：竖杆 + 碟形弧面，用于链路两端。"""
    ax.plot([x, x], [y, y + 1.0 * scale], color=MUTED, lw=2.0, zorder=3)  # 支撑杆
    # 用 Arc 画碟形（开口朝内），度数与角度按左右端在调用时调整
    return x


# ============================================================
# 图 1：链路组成 + 三种组网形态
# ============================================================
def fig1():
    fig, ax = newfig()
    title(ax, "图 1  无线网桥链路组成 + 三种组网形态",
          "左端电口设备 → 网桥 → 定向天线 → 微波链路 → 对端 → 电口设备；下方对比 PTP / PTMP / 中继")

    # --- 上半部：链路主通道（自左向右五个节点）---
    # 节点框顶边 = ny + 1.15，需低于副标题(y=7.6)留出间距，故 ny 取 5.95
    ny = 5.95
    nodes = [
        (0.55, 1.85, "电口设备", "交换机 / 摄像机\n二层接入", C1, "#EFF6FF"),
        (2.85, 1.95, "网桥 A", "射频调制\n发射 Tx", C5, "#F5F3FF"),
        (5.30, 2.55, "微波链路", "2.4 / 5.8 GHz\n视距 + 净空", C3, "#FFF7ED"),
        (8.35, 1.95, "网桥 B", "接收解调\n转发 Rx", C5, "#F5F3FF"),
        (10.75, 1.85, "电口设备", "交换机 / 服务器\n二层输出", C1, "#EFF6FF"),
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
    # 注：链路损耗与净空的逐项标注放在图 2 展开，此处不重复堆字，避免与副标题/框顶挤压。

    # --- 下半部：三种组网形态（三列）---
    base = 3.15
    txt(ax, W / 2, base + 2.35, "三种组网形态", size=11.0, weight="bold", color=INK)
    forms = [
        (0.55, "点对点 PTP", ["两端定向天线互指", "带宽独享、最稳定", "两端单点故障即断"], C1, "#EFF6FF"),
        (4.85, "点对多点 PTMP", ["中心扇区带多远端", "省中心设备与频率", "共享带宽、中心单点"], C5, "#F5F3FF"),
        (9.15, "中继 / 冗余备份", ["超距或遮挡加中继", "双链路主备切换", "逐段核算预算与时延"], C3, "#FFF7ED"),
    ]
    for x, name, items, c, fill in forms:
        box(ax, x, base, 3.55, 2.05, fill, c, lw=1.8)
        txt(ax, x + 1.78, base + 1.68, name, size=10.0, weight="bold", color=c)
        for i, it in enumerate(items):
            txt(ax, x + 0.22, base + 1.18 - i * 0.42, it, size=8.2, color=INK, ha="left")

    footer(ax, "注：无线网桥在二层透明桥接 MAC 帧，不改 IP；室外固定台站须型号核准与电台执照（工信部无〔2021〕129 号）。")
    fig.savefig(os.path.join(OUT, "arch-system.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 2：链路预算瀑布（左）+ 菲涅尔区剖面与地球曲率（右）
# ============================================================
def fig2():
    fig, ax = newfig()
    title(ax, "图 2  链路预算瀑布 + 菲涅尔区剖面与地球曲率",
          "左：发射功率加增益、扣损耗，落到接收电平与灵敏度余量；右：60% 菲涅尔净空与地球凸起决定天线高度")

    # --- 左侧：链路预算瀑布分解（五段框）---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 链路预算瀑布（算例 1/2，单位 dBm/dB）",
        size=10.0, weight="bold", color=C4)
    steps = [
        ("发射功率 P_t", "20 dBm（合规上限内）", C1, 5.62),
        ("两端天线增益", "+24 dBi +24 dBi", C5, 4.72),
        ("自由空间损耗", "-127.7 dB（10 km@5.8G）", C3, 3.82),
        ("馈线与接头", "-2 dB", C4, 2.92),
    ]
    for name, val, c, yy in steps:
        box(ax, lx, yy, lw, 0.78, "#F6F8FA", c, lw=1.5)
        txt(ax, lx + 0.18, yy + 0.39, name, size=9.2, weight="bold", color=c, ha="left")
        txt(ax, lx + lw - 0.18, yy + 0.39, val, size=8.6, weight="bold", color=INK, ha="right")
        if yy > 3.0:
            arrow(ax, lx + lw / 2, yy - 0.02, lx + lw / 2, yy - 0.88, color=c, lw=1.2)
    box(ax, lx, 1.55, lw, 1.05, "#ECFDF5", C2, lw=1.8)
    txt(ax, lx + lw / 2, 2.24,
        "P_rx = 20+24+24-127.7-2 = -61.7 dBm",
        size=9.2, weight="bold", color=C2)
    txt(ax, lx + lw / 2, 1.86,
        "灵敏度 -75 dBm → 余量 13.3 dB（偏紧，建议 ≥15）",
        size=8.0, color=INK)

    # --- 右侧：菲涅尔区剖面 + 地球曲率（矢量示意，非嵌入式 axes）---
    rx, rw = 7.15, 5.45
    txt(ax, rx + rw / 2, 6.62, "② 菲涅尔净空 + 地球曲率（算例 4/5）",
        size=10.0, weight="bold", color=C5)
    # 两端天线杆与碟面
    y_ground = 2.05
    box(ax, rx + 0.30, y_ground, 0.55, 0.18, GRID, MUTED, lw=1.0, r=0.05)  # 左塔基
    box(ax, rx + rw - 0.85, y_ground, 0.55, 0.18, GRID, MUTED, lw=1.0, r=0.05)  # 右塔基
    ax.plot([rx + 0.58, rx + 0.58], [y_ground + 0.18, 5.55], color=MUTED, lw=2.0, zorder=3)
    ax.plot([rx + rw - 0.58, rx + rw - 0.58], [y_ground + 0.18, 5.55], color=MUTED, lw=2.0, zorder=3)
    # 碟形天线（简化为小椭圆弧，开口朝内）
    ell_l = Ellipse((rx + 0.58, 5.62), 0.30, 0.72, angle=0,
                    facecolor="#F5F3FF", edgecolor=C5, lw=1.8, zorder=4)
    ell_r = Ellipse((rx + rw - 0.58, 5.62), 0.30, 0.72, angle=0,
                    facecolor="#F5F3FF", edgecolor=C5, lw=1.8, zorder=4)
    ax.add_patch(ell_l)
    ax.add_patch(ell_r)
    # 第一菲涅尔区椭球（60% 净空椭圆，浅色）：中心在链路中点
    cx = rx + rw / 2
    fr = Ellipse((cx, 5.62), rw - 1.5, 1.70, angle=0,
                 facecolor="#ECFDF5", edgecolor=C2, lw=1.6, ls="--", alpha=0.9, zorder=1)
    ax.add_patch(fr)
    # 标签放在椭圆内部靠上（y=6.20），与副标题(y=6.62)拉开 0.42，避免压字
    txt(ax, cx, 6.20, "第一菲涅尔区（60% 净空）", size=8.4, color=C2, weight="bold")
    # 视距直线（两端天线中心连线）
    ax.plot([rx + 0.58, rx + rw - 0.58], [5.62, 5.62], color=C1, lw=1.6, zorder=3)
    txt(ax, cx, 5.72, "视距 LOS", size=7.8, color=C1)
    # 地球曲率凸起（向下弯的弧）+ 中点障碍物
    arc = Arc((cx, 3.20), rw - 1.0, 2.60, theta1=20, theta2=160,
              color=C3, lw=2.0, zorder=3)
    ax.add_patch(arc)
    # 文字上移到 y=3.32，与下方结论框顶(2.97)拉开 0.35，不再压框边
    txt(ax, cx, 3.32, "地球凸起约 1.5~2 m（10 km）", size=8.0, color=C3, weight="bold")
    # 中点障碍（女儿墙/树梢）侵入净空：框加宽到 1.5、文字放框内，避免压在椭圆虚线边缘
    box(ax, cx - 0.75, 4.55, 1.50, 0.62, "#FFF1EE", C4, lw=1.4, r=0.05)
    txt(ax, cx, 4.86, "障碍侵入净空", size=8.0, color=C4, weight="bold")
    # 杆高结论
    box(ax, rx, 2.25, rw, 0.72, "#FFF7ED", C3, lw=1.6)
    txt(ax, rx + rw / 2, 2.61, "杆高 ≈ 障碍顶 + 60% 菲涅尔半径 + 地球凸起",
        size=8.4, color=C3, weight="bold")

    footer(ax, "注：FSPL、菲涅尔半径与地球凸起为工程基准/演示估算（算例 1/4/5），实际以现场勘测与链路测试为准。")
    fig.savefig(os.path.join(OUT, "link-budget-fresnel.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 3：天线增益/波束宽权衡（左）+ EIRP 法规天花板（右）
# ============================================================
def fig3():
    fig, ax = newfig()
    title(ax, "图 3  天线增益/波束宽权衡 + EIRP 法规天花板",
          "左：增益越高波束越窄、对准越难（算例 6/7）；右：发射功率加天线增益不得越过 33 dBm 硬限（算例 9）")

    # --- 左侧：增益与波束宽对比（两个天线示意 + 数据表）---
    lx, lw = 0.55, 6.05
    txt(ax, lx + lw / 2, 6.62, "① 增益与波束宽此消彼长（算例 6/7）",
        size=10.0, weight="bold", color=C5)
    # 平板天线（宽波束）
    box(ax, lx, 4.55, 2.65, 1.55, "#EFF6FF", C1, lw=1.8)
    txt(ax, lx + 1.32, 5.76, "窄平板天线", size=9.8, weight="bold", color=C1)
    txt(ax, lx + 1.32, 5.34, "增益 16~19 dBi", size=8.8, color=INK)
    txt(ax, lx + 1.32, 4.94, "HPBW 约 30°", size=8.8, color=INK)
    txt(ax, lx + 1.32, 4.68, "免精调、中距", size=8.0, color=MUTED)
    # 抛物面天线（窄波束）
    bx2 = lx + 3.15
    box(ax, bx2, 4.55, 2.90, 1.55, "#F5F3FF", C5, lw=1.8)
    txt(ax, bx2 + 1.45, 5.76, "抛物面天线", size=9.8, weight="bold", color=C5)
    txt(ax, bx2 + 1.45, 5.34, "增益 23~34 dBi", size=8.8, color=INK)
    txt(ax, bx2 + 1.45, 4.94, "HPBW 约 7~10°", size=8.8, color=INK)
    txt(ax, bx2 + 1.45, 4.68, "需微调机构、远距", size=8.0, color=MUTED)
    # 对准惩罚结论框
    box(ax, lx, 3.05, lw, 1.25, "#FFF1EE", C4, lw=1.8)
    txt(ax, lx + lw / 2, 3.92, "指向偏差 ≤ HPBW / 4", size=9.6, weight="bold", color=C4)
    txt(ax, lx + lw / 2, 3.50, "7° 天线偏 3° 损约 2.8 dB，偏 6° 超 11 dB",
        size=8.4, color=INK)
    txt(ax, lx + lw / 2, 3.20, "20 dB 余量链路，仅对准失误就吃掉近一半",
        size=7.8, color=MUTED)
    # 极化失配提示
    box(ax, lx, 2.05, lw, 0.78, "#F6F8FA", CGREY, lw=1.3)
    txt(ax, lx + lw / 2, 2.44, "另：极化方向装反白丢约 20 dB（算例 8）",
        size=8.4, color=INK, weight="bold")

    # --- 右侧：EIRP 法规天花板（嵌入式横向柱状图）---
    rx, rw = 7.15, 5.45
    txt(ax, rx + rw / 2, 6.62, "② EIRP 合规核算（算例 9，单位 dBm）",
        size=10.0, weight="bold", color=C4)
    # axes 底部抬到 3.05 给 x 轴标签腾位，高度缩到 3.00
    a = fig.add_axes([rx / W, 3.05 / H, rw / W, 3.00 / H])
    a.set_facecolor("#FFFFFF")
    # 两类方案：超标方案 20+24=44；合规方案 9+24=33
    labels = ["超标配置\n20 dBm + 24 dBi", "合规配置\n9 dBm + 24 dBi"]
    vals = [44, 33]
    x = range(len(vals))
    bars = a.bar(x, vals, 0.50, color=[C4, C2], zorder=3)
    for bar, lab in zip(bars, ["44", "33"]):
        a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.02,
               lab, ha="center", va="bottom", fontsize=9.5, color=INK,
               weight="bold", zorder=5)
    # 法规上限 33 dBm 水平线
    a.axhline(33, color=C1, lw=1.8, ls="--", zorder=4)
    a.text(1.48, 33.6, "法规上限 33 dBm", ha="right", va="bottom",
           fontsize=8.4, color=C1, weight="bold", zorder=5)
    a.set_ylim(0, 52)
    a.set_xticks(list(x))
    a.set_xticklabels(labels, fontsize=8.0, color=INK)
    a.grid(True, axis="y", color=GRID, lw=0.8, alpha=0.9, zorder=0)
    for sp in a.spines.values():
        sp.set_color(GRID)
    a.tick_params(axis="both", labelsize=8.0, colors=MUTED)
    # 结论框（在嵌入式 axes 下方，数据坐标）
    box(ax, rx, 1.55, rw, 0.92, "#FFF1EE", C4, lw=1.6)
    txt(ax, rx + rw / 2, 2.16, "EIRP = P_t + G_t ≤ 33 dBm（5.8 GHz 硬限）",
        size=8.6, color=C4, weight="bold")
    txt(ax, rx + rw / 2, 1.80, "超 11 dB → 须降发射功率，不得擅自加天线/功放",
        size=7.8, color=INK)

    footer(ax, "注：天线增益与 EIRP 限值为工程基准/厂商口径（算例 6/9），合规以型号核准证与实测 EIRP 为准。")
    fig.savefig(os.path.join(OUT, "antenna-eirp.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 图 4：六类场景共用骨架
# ============================================================
def fig4():
    fig, ax = newfig()
    title(ax, "图 4  六类典型应用场景",
          "远端设备经无线网桥接入中心网络；每类标注距离、频段与关键约束")

    # 链路说明行放在副标题(y=7.6)下方 y=7.18；卡片顶边须低于它，避免盖住标题区
    txt(ax, W / 2, 7.18,
        "远端设备  →  网桥 + 定向天线  →  视距微波链路  →  网桥 + 天线  →  中心网络",
        size=9.4, color=C5, weight="bold")

    # 2 行 × 3 列场景卡片（高 2.20）
    # 第一行 y=4.85 → 顶边 7.05，低于说明行 7.18；第二行 y=2.25 → 顶边 4.45，与第一行底 4.85 留 0.40 间隔
    scenes = [
        (0.55, 4.85, "跨路跨河接入", ["8~30 km 点对点", "5.8 G + 抛物面", "替代顶管施工"], C1, "#EFF6FF"),
        (4.85, 4.85, "视频监控回传", ["1~10 km 点对多点", "5.8 G + 扇区", "GB 50348 可靠性"], C5, "#F5F3FF"),
        (9.15, 4.85, "园区 PTMP 汇聚", ["1~5 km 一点多远端", "共享带宽核算", "中心站单点风险"], C3, "#FFF7ED"),
        (0.55, 2.25, "临时应急布控", ["0.5~3 km 快速架设", "2.4 G 绕射好", "电池供电"], C2, "#ECFDF5"),
        (4.85, 2.25, "强电磁 / 腐蚀", ["工业级硬化机型", "光纤隔离防雷", "IP65+ 宽温"], C4, "#FFF1EE"),
        (9.15, 2.25, "移动载体通信", ["AGV / 无人车", "TDMA 快速切换", "漫游不中断"], C5, "#F5F3FF"),
    ]
    for x, y, name, items, c, fill in scenes:
        box(ax, x, y, 3.55, 2.20, fill, c, lw=1.8)
        txt(ax, x + 1.78, y + 1.82, name, size=10.2, weight="bold", color=c)
        for i, it in enumerate(items):
            txt(ax, x + 0.22, y + 1.34 - i * 0.44, it, size=8.4, color=INK, ha="left")

    footer(ax, "注：场景为工程典型用法示意；距离与频段为示例，实际以链路预算、菲涅尔净空与型号核准为准。")
    fig.savefig(os.path.join(OUT, "scene-topology.png"), dpi=140, facecolor=BG)
    plt.close(fig)


# ============================================================
# 主入口：依次生成四张图
# ============================================================
if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    print("四张矢量图已生成：", OUT)
