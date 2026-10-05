# -*- coding: utf-8 -*-
"""
停车场管理系统配图生成脚本（v2：修正层序与走线，避免压字）
链路绘制规范：正交分支、线型语义一致、无悬空箭头
线型语义：主链路=绿实线、控制/下行=蓝虚线、异常与兜底=红虚线、标注=灰
输出：图1 arch-system / 图2 lane-geometry / 图3 scene-layout / 图4 flow-order
注意：Microsoft YaHei 无 U+2713 字形，达标标记一律用 [达标]
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Circle

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

OUT = os.path.dirname(os.path.abspath(__file__))

C_MAIN = '#27ae60'
C_CTRL = '#2980b9'
C_ERR = '#c0392b'
C_NOTE = '#7f8c8d'
C_BOX = '#2c3e50'
C_TEXT = '#2d3436'
C_TAG = '#34495e'
C_FILL = '#ffffff'


def box(ax, x, y, w, h, text, fill=C_FILL, edge=C_BOX, fs=9, fw='normal', tc=C_TEXT, ls='-', lw=1.4):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.06",
                       linewidth=lw, edgecolor=edge, facecolor=fill, linestyle=ls, zorder=3)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            fontweight=fw, color=tc, zorder=5, linespacing=1.35)


def diamond(ax, cx, cy, w, h, text, fill='#fff6e5', edge='#d68910', fs=8.2):
    pts = [(cx - w / 2, cy), (cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor=edge, linewidth=1.4, zorder=3))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, color=C_TEXT, zorder=5, linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None,
          lx=None, ly=None, lw=1.6, fs=8, ha='center'):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                 arrowstyle='->,head_width=0.07,head_length=0.1',
                                 color=color, linewidth=lw, linestyle=ls,
                                 mutation_scale=11, zorder=4))
    if label:
        tx = lx if lx is not None else (x1 + x2) / 2
        ty = ly if ly is not None else (y1 + y2) / 2 + 0.06
        ax.text(tx, ty, label, ha=ha, va='bottom', fontsize=fs, color=color, zorder=6,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))


def path(ax, pts, color=C_ERR, style='dashed', lw=1.4):
    """正交折线（最后一段带箭头）"""
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs[:-1], ys[:-1], color=color, lw=lw, ls=ls, zorder=4,
            solid_capstyle='round', dash_capstyle='round')
    arrow(ax, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], color=color, style=style, lw=lw)


def note(ax, x, y, text, color=C_NOTE, fs=8.2, ha='left', boxed=True, **kw):
    b = dict(boxstyle='round,pad=0.28', fc='#fbfcfd', ec=color, alpha=0.95, lw=1.0) if boxed else {}
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=color, zorder=6, linespacing=1.45, bbox=b, **kw)


def setup(title, xlim, ylim, figsize, ax=None):
    fig, ax = (plt.subplots(figsize=figsize, dpi=150) if ax is None else (ax.figure, ax))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=13, fontweight='bold', color=C_TEXT, pad=12)
    return fig, ax


# ------------------------------------------------------------------ 图1 五层架构
def fig_arch():
    fig, ax = setup('图1  停车场管理系统五层架构（数据自下而上：感知执行 → 边缘控制 → 平台业务 → 数据服务 → 应用入口）',
                    (0, 13.4), (0, 9.5), (13.4, 9.2))
    layers = [
        ('L1', '感知执行层', ['车牌识别抓拍单元 + 补光灯', '道闸 + 防砸检测', '地感线圈 / 毫米波雷达',
                              '车位探测器 · 指示灯 · 引导屏', '自助缴费机 / 对讲终端'], '#f4f1fb'),
        ('L2', '边缘控制层', ['出入口控制机（车道逻辑）', '区域 / 集中控制器', '边缘 AI 盒子',
                              '本地白名单 · 费率 · 流水缓存'], '#e8f4fd'),
        ('L3', '平台业务层', ['订单与计费引擎', '会员月卡 / 优惠券', '支付核销 / 电子发票', '报表对账与日切'], '#fdf2e9'),
        ('L4', '数据服务层', ['API 网关 / 消息总线', '视频安防联动 GB/T 28181', '门禁与消防联动', '城市停车平台接入'], '#eef7ef'),
        ('L5', '应用入口层', ['岗亭客户端', '云坐席值守', '车主小程序 / APP', '反向寻车查询终端'], '#eaf2f8'),
    ]
    y0, h_band, gap = 0.5, 1.42, 0.24
    x0, x1 = 2.05, 13.15
    n_layer = len(layers)
    for idx, (code, name, items, band_color) in enumerate(layers):
        yb = y0 + idx * (h_band + gap)
        ax.add_patch(FancyBboxPatch((x0, yb), x1 - x0, h_band,
                                    boxstyle="round,pad=0.01,rounding_size=0.08",
                                    linewidth=1.0, edgecolor='#d5dde4', facecolor=band_color, zorder=1))
        box(ax, x0 + 0.12, yb + 0.30, 1.42, 0.82, f'{code}\n{name}',
            fill=C_TAG, edge=C_TAG, fs=8.6, fw='bold', tc='white')
        bx0 = x0 + 1.72
        bw_total = x1 - 0.18 - bx0
        n = len(items)
        g = 0.16
        w = (bw_total - (n - 1) * g) / n
        for j, it in enumerate(items):
            box(ax, bx0 + j * (w + g), yb + 0.34, w, 0.74, it, fs=8.2)
        if idx < n_layer - 1:
            arrow(ax, x0 + 0.83, yb + h_band + 0.02, x0 + 0.83, yb + h_band + gap - 0.01,
                  color=C_MAIN, lw=1.5)

    ax.text(1.06, 4.9, '数\n据\n上\n行', ha='center', va='center', fontsize=9, color=C_MAIN, linespacing=1.15, zorder=6)
    arrow(ax, 1.06, 0.9, 1.06, 8.55, color=C_MAIN, lw=1.7)
    ax.text(0.52, 4.9, '指\n令\n下\n行', ha='center', va='center', fontsize=9, color=C_CTRL, linespacing=1.15, zorder=6)
    arrow(ax, 0.52, 8.55, 0.52, 0.9, color=C_CTRL, lw=1.7, style='dashed')

    note(ax, 2.05, 9.0, 'L2 边缘控制层的自治能力是「断网不堵口」的前提：本地必须能独立完成「识别 — 计费 — 放行」全链路',
         color=C_ERR, fs=8.4)
    fig.tight_layout()
    p = os.path.join(OUT, 'arch-system.png')
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', p)


# ------------------------------------------------- 图2 车道识别几何 + 像素距离曲线
def fig_lane():
    fig, axes = plt.subplots(1, 2, figsize=(14.4, 6.6), dpi=150, gridspec_kw={'width_ratios': [1.2, 1]})
    fig.suptitle('图2  出入口车道识别几何：相机距离与角度、识别区长度，以及号牌像素—距离关系',
                 fontsize=13, fontweight='bold', color=C_TEXT, y=0.985)

    # ---------- (a) 车道侧视
    ax = axes[0]
    ax.set_xlim(0, 16.8)
    ax.set_ylim(-0.5, 3.9)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title('（a）车道侧视：车辆前牌 → 抓拍单元 → 触发点 → 闸杆', fontsize=10.5, color=C_TEXT, pad=8)
    ax.plot([0, 16.8], [0, 0], color='#95a5a6', lw=2.2, zorder=1)
    ax.add_patch(Rectangle((0, -0.42), 16.8, 0.42, facecolor='#eceff1', edgecolor='none', zorder=0))

    # 车辆（车头朝右，前牌照面对相机）
    ax.add_patch(FancyBboxPatch((0.35, 0.12), 4.8, 1.32, boxstyle="round,pad=0.01,rounding_size=0.12",
                                linewidth=1.4, edgecolor=C_CTRL, facecolor='#d6eaf8', zorder=3))
    for wx in (1.25, 4.25):
        ax.add_patch(Circle((wx, 0.12), 0.22, facecolor='#5d6d7e', edgecolor='none', zorder=4))
    ax.add_patch(Rectangle((5.09, 0.52), 0.14, 0.34, facecolor='#f7dc6f', edgecolor='#b7950b', lw=1.2, zorder=5))
    ax.text(5.38, 1.75, '号牌 0.44 m（新能源 0.48 m）', ha='left', va='center', fontsize=7.9, color='#7d6608', zorder=6)
    ax.text(1.05, 0.78, '车辆\n4.8 m', ha='center', va='center', fontsize=8.2, color=C_TEXT, zorder=6)

    # 抓拍单元与补光灯（安全岛）
    ax.add_patch(Rectangle((10.95, 0), 0.5, 0.2, facecolor='#d5d8dc', edgecolor='#839192', lw=1.0, zorder=3))
    ax.text(11.2, -0.2, '安全岛（识读装置）', ha='center', va='center', fontsize=7.8, color=C_NOTE, zorder=6)
    ax.plot([11.2, 11.2], [0.2, 1.52], color='#5d6d7e', lw=3.0, zorder=3)
    ax.add_patch(Rectangle((10.98, 1.42), 0.44, 0.24, facecolor='#34495e', edgecolor='none', zorder=5))
    ax.text(10.8, 1.62, '抓拍单元 1.2~1.6 m', ha='right', va='center', fontsize=7.9, color=C_TEXT, zorder=6)
    ax.plot([11.82, 11.82], [0.2, 2.0], color='#5d6d7e', lw=2.0, zorder=3)
    ax.add_patch(Rectangle((11.64, 1.95), 0.36, 0.2, facecolor='#f39c12', edgecolor='none', zorder=5))
    ax.text(11.95, 2.9, '补光灯\n（与相机夹角 40°）', ha='left', va='center', fontsize=7.9, color='#b9770e', zorder=6)

    # 视线与光锥
    ax.plot([11.0, 5.16], [1.5, 0.66], color=C_CTRL, lw=1.4, ls='--', zorder=4)
    ax.plot([11.72, 5.2], [2.0, 0.72], color='#f39c12', lw=1.1, ls=':', zorder=4)
    ax.annotate('d ≈ 5.9 m\nN = 905/d ≈ 153 px', xy=(8.2, 1.11), xytext=(7.5, 2.5),
                ha='center', va='center', fontsize=8.2, color=C_CTRL, zorder=6,
                arrowprops=dict(arrowstyle='->', color=C_CTRL, lw=1.1, ls='--'),
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=C_CTRL, lw=1.0, alpha=0.95))

    # 触发线圈
    ax.add_patch(Rectangle((8.6, 0.0), 0.62, 0.1, facecolor=C_ERR, edgecolor='none', zorder=5))
    ax.text(8.91, -0.2, '触发线圈', ha='center', va='center', fontsize=7.8, color=C_ERR, zorder=6)

    # 闸机与闸杆
    ax.add_patch(Rectangle((14.3, 0), 0.78, 1.02, facecolor='#85929e', edgecolor='#5d6d7e', lw=1.2, zorder=4))
    ax.text(14.69, 0.5, '闸机', ha='center', va='center', fontsize=8, color='white', zorder=6, fontweight='bold')
    ax.plot([14.3, 12.72], [0.95, 2.28], color=C_MAIN, lw=4.2, zorder=5)
    ax.plot([14.3, 11.9], [0.95, 0.95], color='#aab7b8', lw=2.0, ls='--', zorder=4)
    ax.text(15.2, 0.55, '闸杆\n启杆到位 ≤2 s', ha='left', va='center', fontsize=7.9, color=C_MAIN, zorder=6)

    # 行驶方向
    arrow(ax, 0.35, 2.05, 2.75, 2.05, color=C_NOTE, lw=1.4)
    ax.text(0.4, 2.2, '行驶方向 · 限速 10 km/h', ha='left', va='bottom', fontsize=7.9, color=C_NOTE, zorder=6)

    # 识别区标注（触发点 → 闸杆）
    ax.annotate('', xy=(14.3, 3.5), xytext=(8.91, 3.5), arrowprops=dict(arrowstyle='<->', color=C_MAIN, lw=1.6))
    ax.plot([8.91, 8.91], [0.2, 3.5], color=C_MAIN, lw=1.0, ls=':', zorder=2)
    ax.plot([14.3, 14.3], [1.1, 3.5], color=C_MAIN, lw=1.0, ls=':', zorder=2)
    ax.text(11.6, 3.62, '识别区 L ≥ v × 2.4 s ≈ 6.0 m（10 km/h，按 GA/T 761 的 2 s 留余量）',
            ha='center', va='bottom', fontsize=8.3, color=C_MAIN, fontweight='bold', zorder=6)
    # 识读装置—闸杆间距
    ax.annotate('', xy=(14.3, 0.34), xytext=(11.2, 0.34), arrowprops=dict(arrowstyle='<->', color=C_ERR, lw=1.3))
    ax.text(12.75, 0.44, '3.1 m > 2 800 mm', ha='center', va='bottom', fontsize=7.8, color=C_ERR, zorder=6)

    ax.text(0, -0.085, 'GA/T 761-2008 7.2：识读 / 人机装置中心距挡车器宜 >2 800 mm；操作（读卡）区域安装高度宜 >900 mm；'
                       '出入口应设置安全岛与防撞设施。',
            transform=ax.transAxes, ha='left', va='top', fontsize=7.9, color=C_ERR, zorder=6,
            bbox=dict(boxstyle='round,pad=0.3', fc='#fdf2f2', ec=C_ERR, lw=1.0, alpha=0.95))

    # ---------- (b) 像素—距离曲线
    ax2 = axes[1]
    d = np.linspace(2.0, 20.0, 500)
    Wpx, Wsen, Wplate = 1920.0, 5.6, 0.44
    ax2.set_title('（b）号牌水平像素  N = Wpx · f · W_plate / (d · W_sensor)', fontsize=10.5, color=C_TEXT, pad=8)
    for f, col, lab in [(4, '#7f8c8d', 'f = 4 mm'), (6, C_CTRL, 'f = 6 mm'),
                        (8, C_MAIN, 'f = 8 mm'), (12, '#8e44ad', 'f = 12 mm')]:
        ax2.plot(d, Wpx * f * Wplate / (d * Wsen), color=col, lw=2.0, label=lab, zorder=3)
    ax2.axhspan(100, 160, color=C_MAIN, alpha=0.13, zorder=1)
    ax2.axhline(100, color=C_MAIN, lw=1.1, ls='--', zorder=2)
    ax2.axhline(160, color=C_MAIN, lw=1.1, ls='--', zorder=2)
    ax2.text(19.7, 103, '100 px 下限', ha='right', va='bottom', fontsize=8, color=C_MAIN)
    ax2.text(19.7, 163, '160 px 上限', ha='right', va='bottom', fontsize=8, color=C_MAIN)
    ax2.axvspan(5.7, 9.0, color=C_CTRL, alpha=0.10, zorder=1)
    ax2.plot([6.0], [151], 'o', color=C_CTRL, ms=7, zorder=5)
    ax2.annotate('本案例取值\nd ≈ 6.0 m，N ≈ 151 px', xy=(6.0, 151), xytext=(9.6, 250),
                 fontsize=8.3, color=C_CTRL, zorder=6,
                 arrowprops=dict(arrowstyle='->', color=C_CTRL, lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=C_CTRL, lw=1.0, alpha=0.95))
    ax2.text(7.35, 372, '6 mm 镜头推荐安装窗（5.7~9.0 m）', ha='center', va='center', fontsize=8,
             color=C_CTRL, zorder=6, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9))
    ax2.set_xlim(2, 20); ax2.set_ylim(0, 400)
    ax2.set_xlabel('相机到号牌距离 d（m）', fontsize=9.5)
    ax2.set_ylabel('号牌水平像素 N（px）', fontsize=9.5)
    ax2.grid(alpha=0.25, ls=':')
    ax2.legend(loc='upper right', fontsize=8.6, framealpha=0.95)
    ax2.tick_params(labelsize=8.6)
    ax2.text(0, -0.115, '镜头选型读法：先按现场可用距离 d 定目标像素 100~160 px，再反选焦距 f；同一焦距下视场宽度/距离为定值。',
             transform=ax2.transAxes, ha='left', va='top', fontsize=7.9, color=C_NOTE,
             bbox=dict(boxstyle='round,pad=0.3', fc='#fbfcfd', ec=C_NOTE, lw=1.0, alpha=0.95))

    fig.tight_layout(rect=[0, 0, 1, 0.945])
    p = os.path.join(OUT, 'lane-geometry.png')
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', p)


# ------------------------------------------------- 图3 分级引导与反向寻车拓扑
def fig_scene():
    fig, ax = setup('图3  场内分级引导与反向寻车拓扑（左列：出入口与车主侧；右区：感知 → 处理 → 发布）',
                    (0, 13.6), (0, 9.4), (13.6, 9.2))

    # 左列
    box(ax, 0.3, 6.15, 2.25, 1.1, '入口抓拍识别单元\n入场车牌 · 车辆特征', fill='#f4f1fb', edge='#6c5ce7', fs=8.6)
    box(ax, 0.3, 2.85, 2.25, 1.15, '车主小程序 /\n反向寻车查询终端\n输入车牌 → 车位 + 路径',
        fill='#fdf2e9', edge='#ca6f1e', fs=8.4)

    # 右区三行
    xr0, xr1 = 3.0, 13.4
    gap = 0.2
    w4 = (xr1 - xr0 - 3 * gap) / 4
    xs4 = [xr0 + i * (w4 + gap) for i in range(4)]
    c4 = [x + w4 / 2 for x in xs4]

    y1, h1 = 7.5, 1.15
    row1 = ['一级引导屏\n场外 / 入口总余位', '二级引导屏\n分区余位 + 方向',
            '车位指示灯\n红 / 绿 / 蓝', '异常告警\n消防通道占用 · 长时间滞留']
    for x, t in zip(xs4, row1):
        box(ax, x, y1, w4, h1, t, fill='#eafaf1', edge=C_MAIN, fs=8.5, fw='bold')

    y2, h2 = 5.15, 1.3
    box(ax, xr0, y2, 4.6, h2, '引导与寻车服务器\n「车牌 — 车位 — 时间」索引 / 路径计算 / 分区统计',
        fill='#e8f4fd', edge=C_CTRL, fs=8.8, fw='bold')
    box(ax, 7.85, y2, 2.6, h2, '区域 / 集中控制器\n每区 60~120 台探测器', fs=8.5)
    box(ax, 10.8, y2, 2.6, h2, '云坐席 / 物业端\n远程开闸 · 工单 · 留痕', fs=8.5)

    y3, h3 = 2.85, 1.15
    row3 = ['视频车位探测器\n一拖二 · 识别车牌', '超声波 / 地磁探测器\n补盲（立体车库 · 户外）',
            '场内自助缴费机\n提前缴费 · 缩短闸口停留', '支付网关 / 电子发票\n清分对账 · 数据上报']
    for x, t in zip(xs4, row3):
        box(ax, x, y3, w4, h3, t, fill='#f4f1fb', edge='#6c5ce7', fs=8.5)

    # 上行箭头：感知 → 处理 → 发布
    for i, x in enumerate(c4):
        arrow(ax, x, y3 + h3, x, y2 - 0.02, color=C_MAIN, lw=1.5)
        arrow(ax, x, y2 + h2, x, y1 - 0.02, color=C_MAIN, lw=1.5)
    ax.text(c4[0] - 0.15, 4.42, '车位状态 + 车位车牌', ha='center', va='center', fontsize=8,
            color=C_MAIN, zorder=6, bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.92))
    ax.text(c4[0] - 0.15, 6.62, '余位 / 灯色 / 路径下发', ha='center', va='center', fontsize=8,
            color=C_MAIN, zorder=6, bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.92))

    # 入场车牌 → 服务器（斜向虚线）
    arrow(ax, 2.55, 6.72, 3.95, 6.46, color='#6c5ce7', style='dashed', lw=1.5)
    ax.text(3.32, 6.92, '入场车牌', ha='center', va='bottom', fontsize=8, color='#6c5ce7', zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))

    # 服务器 → 车主应用（正交下行）
    path(ax, [(3.0, 5.62), (1.62, 5.62), (1.62, 4.02)], color=C_CTRL, style='dashed', lw=1.6)
    ax.text(2.35, 5.78, '索引查询 → 车位与路径', ha='center', va='bottom', fontsize=7.9, color=C_CTRL, zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))

    note(ax, 0.3, 1.05, '绑定链：① 入场识别车牌  ② 车位二次识别  ③ 绑定「车牌 — 车位 — 时间」→ 反向寻车成立\n'
                        '兜底：无牌 / 污损 / 识别失败 → 车辆特征（颜色 · 车型）+ 区域模糊查询 + 人工协助',
         color=C_ERR, fs=8.4)
    fig.tight_layout()
    p = os.path.join(OUT, 'scene-layout.png')
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', p)


# ------------------------------------------------- 图4 识别链路 + 订单状态机
def fig_flow():
    fig, axes = plt.subplots(2, 1, figsize=(13.4, 9.8), dpi=150, gridspec_kw={'height_ratios': [1, 1.25]})
    fig.suptitle('图4  车牌识别算法链路（上）与出入口订单状态机及异常分支（下）',
                 fontsize=13, fontweight='bold', color=C_TEXT, y=0.985)

    # ---------- (a) 算法链路
    ax = axes[0]
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlim(0, 13.4); ax.set_ylim(0, 5.5)
    ax.set_title('（a）识别六级流水线：从一帧图像到一串字符', fontsize=10.5, color=C_TEXT, pad=8)

    stages = ['① 车辆 / 号牌\n检测', '② 号牌定位\n与角点回归', '③ 几何矫正\n（透视变换）',
              '④ 字符切分 /\n序列识别', '⑤ 规则后处理\n（号牌语法）', '⑥ 置信度\n裁决']
    w, h, y, x0, step = 1.78, 1.05, 3.85, 0.3, 2.13
    for i, t in enumerate(stages):
        x = x0 + i * step
        box(ax, x, y, w, h, t, fill='#eef7ef', edge=C_MAIN, fs=8.6, fw='bold')
        if i < len(stages) - 1:
            arrow(ax, x + w, y + h / 2, x + step - 0.02, y + h / 2, color=C_MAIN, lw=1.6)

    outs = [(0.45, 3.35, '高置信\n直接放行', C_MAIN),
            (4.15, 3.35, '中置信\n模糊匹配入场记录 → 命中即放行', '#16a085'),
            (8.05, 3.75, '低置信\n二次抓拍 → 人工 / 二维码', C_ERR)]
    cx_last = x0 + 5 * step + w / 2
    bus_y = 2.95
    path(ax, [(cx_last, y - 0.02), (cx_last, bus_y), (2.125, bus_y)], color=C_MAIN, style='solid', lw=1.5)
    for x, ww, t, col in outs:
        bx = x + ww / 2
        arrow(ax, bx, bus_y, bx, 2.07, color=col, lw=1.5, style='dashed')
        box(ax, x, 1.05, ww, 1.0, t, fill='#fbfcfd', edge=col, fs=8.6, fw='bold', tc=col)

    note(ax, 0.3, 0.5, '规则后处理把「形似错识」压下去：省份汉字集 · 第 2 位为发牌机关字母 · 新能源 8 位且第 3 位 D/F · '
                       '易混字符对（0/D、8/B、2/Z、5/S）的位置约束', color=C_NOTE, fs=8.2)

    # ---------- (b) 订单状态机
    ax = axes[1]
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlim(0, 13.4); ax.set_ylim(0, 6.6)
    ax.set_title('（b）一次通行的状态机：待机 → 触发 → 识别 → 判定 → 放行 → 过车计数 → 落杆 → 订单',
                 fontsize=10.5, color=C_TEXT, pad=8)

    ya, h = 4.6, 0.92
    for x, ww, t in [(0.3, 1.42, '待机'), (2.02, 1.95, '触发\n地感 / 视频 / 雷达'), (4.27, 1.95, '抓拍识别\n≤3 帧投票')]:
        box(ax, x, ya, ww, h, t, fill='#eef7ef', edge=C_MAIN, fs=8.4, fw='bold')
    arrow(ax, 1.72, ya + h / 2, 2.0, ya + h / 2, color=C_MAIN, lw=1.6)
    arrow(ax, 3.97, ya + h / 2, 4.25, ya + h / 2, color=C_MAIN, lw=1.6)
    arrow(ax, 6.22, ya + h / 2, 6.6, ya + h / 2, color=C_MAIN, lw=1.6)
    diamond(ax, 8.0, ya + h / 2, 2.3, 1.4, '凭证判定\n月租 / 临停\n黑名单 / 免费', fs=8.2)
    arrow(ax, 9.15, ya + h / 2, 9.55, ya + h / 2, color=C_MAIN, lw=1.6)
    box(ax, 9.55, ya, 1.62, h, '放行指令', fill='#eef7ef', edge=C_MAIN, fs=8.4, fw='bold')
    arrow(ax, 11.17, ya + h / 2, 11.55, ya + h / 2, color=C_MAIN, lw=1.6)
    box(ax, 11.55, ya, 1.55, h, '抬杆\n≤2 s', fill='#eef7ef', edge=C_MAIN, fs=8.4, fw='bold')

    yb, hb = 2.2, 0.95
    box(ax, 9.75, yb, 2.0, hb, '过车计数\n存在检测确认', fill='#eef7ef', edge=C_MAIN, fs=8.4, fw='bold')
    box(ax, 6.95, yb, 2.0, hb, '落杆', fill='#eef7ef', edge=C_MAIN, fs=8.6, fw='bold')
    box(ax, 3.55, yb, 2.75, hb, '订单落库 / 断网后补传', fill='#eef7ef', edge=C_MAIN, fs=8.4, fw='bold')
    box(ax, 0.3, yb, 0.68, hb, '待机', fill='#d5f5e3', edge=C_MAIN, fs=8.0, fw='bold')
    arrow(ax, 12.32, ya - 0.02, 10.9, yb + hb + 0.02, color=C_MAIN, lw=1.6)
    arrow(ax, 9.73, yb + hb / 2, 8.97, yb + hb / 2, color=C_MAIN, lw=1.6)
    arrow(ax, 6.93, yb + hb / 2, 6.32, yb + hb / 2, color=C_MAIN, lw=1.6)
    arrow(ax, 3.53, yb + hb / 2, 1.0, yb + hb / 2, color=C_MAIN, lw=1.6)

    # 异常分支（正交走线，只走下方自由通道，避免穿越状态框）
    exc = [(1.6, 3.0, '识别失败：二次抓拍 → 模糊匹配 → 人工 / 二维码'),
           (4.9, 3.0, '无牌 / 黑名单：ID 码入场 + 车辆特征存档'),
           (8.2, 2.8, '跟车（尾随）：告警留痕 + 后车按临停'),
           (11.1, 2.2, '倒车退出\n撤销预生成订单')]
    for x, ww, t in exc:
        box(ax, x, 0.75, ww, 0.95, t, fill='#fdecea', edge=C_ERR, fs=7.9, tc='#922b21', ls='--')
    path(ax, [(5.25, ya - 0.02), (5.25, 3.86), (3.2, 3.86), (3.2, 1.72)], color=C_ERR, style='dashed', lw=1.3)
    path(ax, [(8.0, ya - 0.72), (8.0, 3.72), (6.6, 3.72), (6.6, 1.72)], color=C_ERR, style='dashed', lw=1.3)
    path(ax, [(9.75, yb + hb / 2), (9.35, yb + hb / 2), (9.35, 1.72)], color=C_ERR, style='dashed', lw=1.3)
    path(ax, [(11.75, yb + hb / 2), (12.2, yb + hb / 2), (12.2, 1.72)], color=C_ERR, style='dashed', lw=1.3)

    note(ax, 0.3, 0.32, '全部异常分支必须落在同一套可追溯日志里；倒车场景需撤销预生成订单，避免「幽灵订单」占用订单号。',
         color=C_ERR, fs=8.2)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p = os.path.join(OUT, 'flow-order.png')
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', p)


if __name__ == '__main__':
    fig_arch()
    fig_lane()
    fig_scene()
    fig_flow()
