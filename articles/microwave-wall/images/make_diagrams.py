# -*- coding: utf-8 -*-
"""
微波对射探测器配图生成脚本
遵循链路绘制规范：正交分支、双色线型编码、无悬空箭头
图例：主链路=绿实线、状态/自适应=蓝虚线、异常/报警=红虚线
输出：图1 arch-system / 图2 geo-fresnel / 图3 flow-signal / 图4 scene-topology
注意：Microsoft YaHei 无 U+2713 字形，符合标记一律用 [符合] / [不足]
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle, Ellipse
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

C_MAIN = '#2ecc71'
C_OUT = '#3498db'
C_ERR = '#e74c3c'
C_BOX = '#2c3e50'
C_FILL = '#ecf0f1'
C_TITLE = '#2d3436'
C_WALL = '#7f8c8d'
C_WIRE = '#95a5a6'


def draw_box(ax, x, y, w, h, text, fill=C_FILL, edge=C_BOX, fontsize=10,
             fontweight='normal', textcolor=C_TITLE):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=1.5, edgecolor=edge, facecolor=fill, zorder=2)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, color=textcolor, zorder=3)


def draw_diamond(ax, cx, cy, w, h, text, fill='#fff3cd', edge='#d4a017', fontsize=9):
    pts = [(cx - w / 2, cy), (cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2)]
    poly = Polygon(pts, closed=True, facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=2)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            color=C_TITLE, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None,
          label_pos=0.5, label_offset=(0.0, 0.06), lw=1.8, ha='center'):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=lw, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(lx, ly, label, ha=ha, va='bottom', fontsize=8, color=color, zorder=5,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


def fig_setup(title, xlim=(0, 10), ylim=(0, 8), figsize=(12, 8)):
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=13.5, fontweight='bold', color=C_TITLE, pad=14)
    return fig, ax


def legend(ax, items, ncol=3, loc='lower left', anchor=(0.02, -0.02)):
    handles = [mpatches.Patch(facecolor='none', edgecolor=c, linewidth=2.2,
                              linestyle=ls, label=t) for t, c, ls in items]
    ax.legend(handles=handles, loc=loc, bbox_to_anchor=anchor,
              fontsize=9, frameon=True, ncol=ncol)


# ---------------------------------------------------------------- 图1 四层架构
def fig_arch():
    fig, ax = fig_setup('图1 微波对射周界报警系统四层架构（示意）', (0, 10.6), (0, 9.4))
    ax.set_xticks([])
    ax.set_yticks([])

    layers = [
        (7.9, '① 前端微波收发层', '发射机 / 接收机 · X 或 K 波段天线 · 方波调制载波 · 立杆与指向支架', '#d5f5e3', C_MAIN),
        (6.2, '② 信号处理与控制层', '接收电平检测 · AGC 慢变跟随 · 快变判定 · 异频通道 · 防拆与链路自检', '#d6eaf8', C_OUT),
        (4.5, '③ 传输与供电层', '无电位常闭触点 / 总线地址码 · DC12~24V 分区供电 · 防雷接地与等电位', '#fdebd0', '#d4a017'),
        (2.8, '④ 平台与联动层', '报警管理 · 电子地图定位 · 视频预置位复核 · 声光警号 · 照明联动 · 运维工单', '#fadbd8', C_ERR),
    ]
    for y, title, desc, fill, edge in layers:
        bar = FancyBboxPatch((1.15, y), 8.5, 1.25,
                             boxstyle="round,pad=0.02,rounding_size=0.10",
                             linewidth=1.6, edgecolor=edge, facecolor=fill, zorder=2)
        ax.add_patch(bar)
        ax.text(5.4, y + 0.85, title, ha='center', va='center', fontsize=11.5,
                fontweight='bold', color=C_TITLE, zorder=3)
        ax.text(5.4, y + 0.34, desc, ha='center', va='center', fontsize=8.4,
                color='#34495e', zorder=3)

    for i in range(3):
        y1 = 7.9 - i * 1.7
        y2 = y1 - 0.45
        arrow(ax, 5.4, y2, 5.4, y1, color=C_MAIN, style='solid')

    ax.text(0.28, 8.5, '电磁场\n（发射→散射）', ha='left', va='center', fontsize=8.3,
            color='#1e8449', fontweight='bold')
    ax.text(0.28, 6.85, '电平变化\n（快变 ΔL）', ha='left', va='center', fontsize=8.3,
            color='#1a5490', fontweight='bold')
    ax.text(0.28, 5.15, '开关量 / 报文', ha='left', va='center', fontsize=8.3,
            color='#9a6d00', fontweight='bold')
    ax.text(0.28, 3.45, '处置动作', ha='left', va='center', fontsize=8.3,
            color='#a93226', fontweight='bold')

    arrow(ax, 9.95, 3.4, 9.95, 8.5, color=C_OUT, style='dashed',
          label='远程读取链路余量 / 灵敏度档位 / 复位', label_pos=0.5, label_offset=(-3.15, 0))

    ax.text(5.0, 1.35, '注：对射微波的「传感器」不只是两台设备 —— 波束穿过的整个空间都是传感器，\n'
                       '净空走廊内的地被、积雪、积水与反射物都参与成像，必须纳入设计与管理。',
            ha='center', va='center', fontsize=8.4, color='#5d6d7e',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fbfcfc', ec='#d5dbdb'))

    legend(ax, [('主链路（场→电→报）', C_MAIN, '-'), ('控制 / 状态反馈', C_OUT, '--'),
                ('平台联动', C_ERR, '-')])
    out = os.path.join(OUT_DIR, 'arch-system.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


# ------------------------------------------------- 图2 探测区几何与菲涅耳净空
def fig_geo():
    fig, ax = fig_setup('图2 探测区几何与第一菲涅耳区净空（示意；两栏垂直同比例尺，水平为示意压缩）',
                        (-0.85, 21.3), (-1.05, 3.55), figsize=(13.5, 5.4))

    def device(ax, x, h_center, ghost=False):
        ls = '--' if ghost else '-'
        ec = C_ERR if ghost else C_BOX
        ax.add_patch(Rectangle((x - 0.05, 0), 0.10, h_center - 0.02,
                               facecolor='none' if ghost else '#bdc3c7',
                               edgecolor=ec, linewidth=1.1, linestyle=ls, zorder=3))
        if not ghost:
            ax.add_patch(Rectangle((x - 0.14, -0.03), 0.28, 0.08, facecolor='#5d6d7e',
                                   edgecolor='#2c3e50', linewidth=1.0, zorder=3))
        ax.add_patch(Rectangle((x - 0.16, h_center - 0.10), 0.32, 0.20,
                               facecolor='none' if ghost else '#34495e',
                               edgecolor=ec, linewidth=1.4, linestyle=ls, zorder=4))
        ax.plot([x + 0.16], [h_center], marker='>', markersize=5,
                color=ec, zorder=5, linestyle=ls)

    def grass(ax, x0, x1, hmax=0.30, seed=3):
        for gx in np.arange(x0 + 0.15, x1 - 0.1, 0.32):
            h = hmax * (0.55 + 0.45 * np.sin(gx * seed * 7.3))
            ax.plot([gx, gx + 0.05, gx + 0.10], [0, h, 0], color='#7d6608',
                    linewidth=1.0, zorder=3)

    def dim(ax, x, y0, y1, color=C_ERR):
        ax.annotate('', xy=(x, y1), xytext=(x, y0),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))

    # ================= 左：D = 100 m =================
    x0, x1 = 0.9, 7.5
    ax.text(4.2, 3.22, '链路 D = 100 m（r1 ≈ 0.84 m，安装高度 0.9 m）', ha='center',
            va='center', fontsize=11, fontweight='bold', color=C_TITLE)

    ax.add_patch(Ellipse(((x0 + x1) / 2, 0.9), x1 - x0, 2.5, facecolor='#aed6f1',
                         alpha=0.30, edgecolor=C_OUT, linewidth=1.4, linestyle='--', zorder=1))
    ax.add_patch(Ellipse(((x0 + x1) / 2, 0.9), x1 - x0, 2 * 0.84, facecolor='none',
                         edgecolor='#d4a017', linewidth=1.5, linestyle='-', zorder=2))
    y_cl = 0.9 - 0.6 * 0.84
    ax.plot([x0 + 0.3, x1 - 0.3], [y_cl, y_cl], color=C_ERR, linewidth=1.2,
            linestyle='--', zorder=3)
    ax.text(4.2, y_cl + 0.06, '净空线 0.6·F1 ≈ 0.50 m（低于此线不可有遮挡）',
            ha='center', va='bottom', fontsize=7.8, color=C_ERR,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))

    device(ax, x0, 0.9)
    device(ax, x1, 0.9)
    grass(ax, x0, x1, 0.30)

    dim(ax, 0.30, 0.0, 0.9)
    ax.text(0.30, 1.02, '安装高度 0.9 m', ha='center', va='bottom', fontsize=8,
            color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.text(4.2, -0.14, '地被限值：草高 ≤ 0.3 m，积雪 ≤ 0.5 m，净空余量 ≈ 0.40 m [符合]',
            ha='center', va='top', fontsize=8.4, color='#1e8449', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#eafaf1', ec='#a9dfbf'))

    # ================= 右：D = 200 m =================
    x0b, x1b = 10.6, 17.2
    ax.text(13.9, 3.22, '链路 D = 200 m（r1 ≈ 1.19 m，安装高度须抬高至 1.2 m）', ha='center',
            va='center', fontsize=11, fontweight='bold', color=C_TITLE)

    ax.add_patch(Ellipse(((x0b + x1b) / 2, 1.2), x1b - x0b, 2.5, facecolor='#aed6f1',
                         alpha=0.30, edgecolor=C_OUT, linewidth=1.4, linestyle='--', zorder=1))
    ax.add_patch(Ellipse(((x0b + x1b) / 2, 1.2), x1b - x0b, 2 * 1.19, facecolor='none',
                         edgecolor='#d4a017', linewidth=1.5, linestyle='-', zorder=2))
    y_cl2 = 1.2 - 0.6 * 1.19
    ax.plot([x0b + 0.3, x1b - 0.3], [y_cl2, y_cl2], color=C_ERR, linewidth=1.2,
            linestyle='--', zorder=3)
    ax.text(13.9, y_cl2 + 0.06, '净空线 0.6·F1 ≈ 0.72 m（长链路菲涅耳区更大、更贴地）',
            ha='center', va='bottom', fontsize=7.8, color=C_ERR,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))

    device(ax, x0b, 1.2)
    device(ax, x1b, 1.2)
    device(ax, x0b, 0.9, ghost=True)
    device(ax, x1b, 0.9, ghost=True)
    grass(ax, x0b, x1b, 0.30)

    dim(ax, 10.10, 0.0, 1.2)
    ax.text(10.10, 1.32, '抬高至 1.2 m', ha='center', va='bottom', fontsize=8,
            color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    dim(ax, 18.55, 0.0, 0.9, color=C_ERR)
    ax.text(18.68, 0.45, '仍装 0.9 m：净空仅 0.18 m\n低于草高 0.3 m [不足]', ha='left',
            va='center', fontsize=7.8, color=C_ERR,
            bbox=dict(boxstyle='round,pad=0.18', fc='#fdedec', ec=C_ERR, alpha=0.95))
    ax.text(13.9, -0.14, '抬高至 1.2 m：净空 0.48 m ≥ 草高 0.3 m + 余量 [符合] —— 长链路必须抬高安装高度',
            ha='center', va='top', fontsize=8.4, color='#1e8449', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#eafaf1', ec='#a9dfbf'))

    # 地面线
    ax.plot([-0.7, 21.1], [0, 0], color=C_WALL, linewidth=1.6, zorder=2)

    ax.text(10.2, -0.72, '核算：r1 = 0.5·√(λ·D)，λ = 2.85 cm（10.525 GHz）｜净空 = 安装高度 − 0.6·r1 ≥ 地被限值 —— '
                         '由此反推的安装高度与厂家「草 ≤ 0.3 m / 雪 ≤ 0.5 m」限值吻合（工程基准）',
            ha='center', va='center', fontsize=8.4, color='#5d6d7e')

    out = os.path.join(OUT_DIR, 'geo-fresnel.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


# ------------------------------------------- 图3 电平变化检测与判定链路
def fig_flow():
    fig, ax = fig_setup('图3 接收电平变化检测与判定链路（示意）', (0, 13.9), (0, 8.8))

    # 顶部主链路
    draw_box(ax, 0.35, 7.0, 2.6, 1.0, '发射机\n10.525 GHz 载波\n方波调制 2.83~15.45 kHz',
             fill='#d5f5e3', edge=C_MAIN, fontsize=8.2)
    draw_box(ax, 3.35, 7.0, 2.6, 1.0, '空间传播\n自由空间损耗 ≈ 93 dB @100 m\n能量约束在菲涅耳走廊',
             fill='#d5f5e3', edge=C_MAIN, fontsize=8.2)
    draw_box(ax, 6.35, 7.0, 2.6, 1.0, '人体入侵\n散射 + 遮挡\n接收电平突变 ΔL',
             fill='#d5f5e3', edge=C_MAIN, fontsize=8.2)
    draw_box(ax, 9.35, 7.0, 2.9, 1.0, '接收处理\n检波 → 对数放大\n得到链路电平曲线',
             fill='#d6eaf8', edge=C_OUT, fontsize=8.2)

    for y in (7.5,):
        for xx1, xx2 in ((2.95, 3.35), (5.95, 6.35), (8.95, 9.35)):
            arrow(ax, xx1, y, xx2, y, color=C_MAIN, style='solid')

    # 分成慢变 / 快变
    arrow(ax, 9.6, 7.0, 6.9, 6.28, color=C_OUT, style='dashed',
          label='同一电平曲线', label_pos=0.45, label_offset=(-0.9, 0.05))
    arrow(ax, 10.9, 7.0, 11.05, 6.28, color=C_OUT, style='solid')

    draw_box(ax, 5.4, 5.35, 3.0, 0.9, 'AGC 慢变跟随\n雨雪 / 温漂 / 老化\n自动回调整定，不报警',
             fill='#d6eaf8', edge=C_OUT, fontsize=8.2)
    draw_box(ax, 9.8, 5.35, 2.5, 0.9, '快变检测\n捕捉 ΔL 与\n其时间特征', fill='#d6eaf8',
             edge=C_OUT, fontsize=8.2)

    arrow(ax, 7.6, 5.35, 8.9, 4.33, color=C_OUT, style='dashed', lw=1.4,
          label='跟随基线', label_pos=0.45, label_offset=(-1.05, 0.02))
    arrow(ax, 11.05, 5.35, 10.2, 4.62, color=C_ERR, style='solid', lw=1.6)

    draw_diamond(ax, 9.85, 3.85, 4.9, 1.5,
                 'ΔL ≥ 门限（3~6 dB 工程基准）\n且速率落在人体速度窗\n0.1~10 m/s（室外型）？',
                 fill='#fff3cd', edge='#d4a017', fontsize=8.0)

    # 是 → 报警
    arrow(ax, 7.40, 3.85, 6.75, 3.85, color=C_ERR, style='solid', label='是',
          label_pos=0.5, label_offset=(0.0, 0.10))
    draw_box(ax, 4.2, 3.35, 2.55, 1.0, '报警输出\n无电位触点 / 总线上报\n警戒恢复 ≤ 10 s',
             fill='#fadbd8', edge=C_ERR, fontsize=8.2, fontweight='bold')
    # 否 → 维持警戒
    arrow(ax, 12.30, 3.85, 12.64, 3.85, color=C_MAIN, style='solid', label='否',
          label_pos=0.5, label_offset=(0.0, 0.10))
    draw_box(ax, 12.64, 3.35, 0.95, 1.0, '维持\n警戒', fill='#d5f5e3', edge=C_MAIN,
             fontsize=8.4)

    # 左侧：误报源与抑制
    draw_box(ax, 0.4, 5.35, 3.4, 1.15, '典型误报源\n小动物 / 飘动树枝 / 水洼反射\n相邻设备串扰 / 大风植被摆动',
             fill='#fdebd0', edge='#d4a017', fontsize=8.0)
    draw_box(ax, 0.4, 3.35, 3.4, 1.0, '抑制手段\n速度窗 · 异频交叉 · AGC\n多级灵敏度 · 净空走廊维护',
             fill='#d6eaf8', edge=C_OUT, fontsize=8.0)
    arrow(ax, 3.8, 5.9, 4.3, 3.95, color=C_OUT, style='dashed', lw=1.3,
          label='逐项对治', label_pos=0.5, label_offset=(0.12, 0.0), ha='left')

    # 底部说明
    ax.text(6.95, 1.9, '检测的不是「有没有信号」，而是「电平为什么变」：\n'
                      '慢变交给 AGC，快变才进入判定；自监督保证链路余量不足时\n'
                      '报「故障」而不是漏报 —— 这是微波对射低误报的底层逻辑。',
            ha='center', va='center', fontsize=8.6, color='#5d6d7e',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fbfcfc', ec='#d5dbdb'))
    ax.text(6.95, 0.55, '参考基准：室外型速度窗 0.1~10 m/s、室内型 0.1~3 m/s（国标整合版征求意见稿 5.3.4）；\n'
                       '警戒恢复 ≤ 10 s、7 天探测距离稳定性 ≤ 10%（GB 10408.3-2000 同族指标，工程基准）。',
            ha='center', va='center', fontsize=8.2, color='#5d6d7e')

    legend(ax, [('主链路（场→电→判定）', C_MAIN, '-'),
                ('自适应 / 状态反馈', C_OUT, '--'),
                ('入侵 / 报警分支', C_ERR, '-')], ncol=3, loc='lower left',
              anchor=(0.02, -0.02))
    out = os.path.join(OUT_DIR, 'flow-signal.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


# ---------------------------------- 图4 交叉布防俯视（案例一：1200 m 变电站）
def fig_scene():
    fig, ax = fig_setup('图4 案例一 1200 m 变电站周界交叉布防（俯视示意，400 m × 200 m）',
                        (0, 13.6), (0, 10.3), figsize=(13, 9.3))

    # 周界：400 m × 200 m，比例 40 m/单位
    px0, py0, pw, ph = 1.0, 2.2, 10.0, 5.0
    ax.text(px0 + pw / 2, py0 + ph / 2, '变电站围墙区\n400 m × 200 m（周界 1200 m）',
            ha='center', va='center', fontsize=11, color='#85929e', fontweight='bold')

    def point_at(s):
        w, h = pw, ph
        if s < w:
            return px0 + s, py0 + ph
        s -= w
        if s < h:
            return px0 + w, py0 + ph - s
        s -= h
        if s < w:
            return px0 + w - s, py0
        s -= w
        return px0, py0 + s

    # 15 对探测器，均匀步进 80 m，起点偏移 45 m（避开四角）
    step = 80 / 40.0
    marks = [point_at((45 + i * 80) / 40.0) for i in range(15)]

    # 供电分区着色：A = 0~400 m（上边），B = 400~800 m（右边+右下），C = 800~1200 m
    seg_colors = [('#1e8449', (0, 400)), ('#1a5490', (400, 800)), ('#9a6d00', (800, 1200))]
    for colr, (s0, s1) in seg_colors:
        seg_pts = [point_at(s / 40.0) for s in range(s0, s1 + 1, 10)]
        xs = [p[0] for p in seg_pts]
        ys = [p[1] for p in seg_pts]
        ax.plot(xs, ys, color=colr, linewidth=3.2, zorder=2,
                solid_capstyle='round')

    # 相邻两对波束交叠虚线（仅同一条边上相连，不跨角）
    for i in range(len(marks) - 1):
        x0, y0 = marks[i]
        x1, y1 = marks[i + 1]
        if abs(x0 - x1) < 1e-6 or abs(y0 - y1) < 1e-6:
            ax.plot([x0, x1], [y0, y1], color='#7fb3d5', linewidth=1.0,
                    linestyle='--', alpha=0.8, zorder=3)

    for (x, y) in marks:
        ax.plot([x], [y], marker='o', markersize=6.5, color='#1a5490',
                markeredgecolor='white', zorder=6)

    # 交叉段高亮（右边 445~525 m 段之间）+ 右上放大图
    hy = py0 + ph - ((445 + 80 / 2) - 400) / 40.0
    ax.add_patch(Rectangle((px0 + pw - 0.40, hy - 0.50), 0.80, 1.00, facecolor='none',
                           edgecolor=C_ERR, linewidth=1.5, linestyle='--', zorder=6))
    ax.text(px0 + pw - 0.50, hy, '交叉段\n（右上放大）', ha='right', va='center',
            fontsize=7.8, color=C_ERR, zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))

    zx, zy, zw, zh = 11.25, 8.35, 2.1, 1.45
    ax.add_patch(Rectangle((zx, zy), zw, zh, facecolor='white',
                           edgecolor=C_ERR, linewidth=1.3, zorder=7))
    ax.add_patch(Ellipse((zx + 0.60, zy + 0.72), 1.42, 0.92, facecolor='#d5f5e3',
                         edgecolor='#1e8449', linewidth=1.2, zorder=8, alpha=0.9))
    ax.add_patch(Ellipse((zx + 1.50, zy + 0.72), 1.42, 0.92, facecolor='#d6eaf8',
                         edgecolor='#1a5490', linewidth=1.2, zorder=9, alpha=0.72))
    ax.plot([zx + 0.60], [zy + 0.72], marker='o', markersize=4, color='#1e8449', zorder=10)
    ax.plot([zx + 1.50], [zy + 0.72], marker='o', markersize=4, color='#1a5490', zorder=10)
    ax.annotate('', xy=(zx + 1.22, zy + 1.28), xytext=(zx + 0.88, zy + 1.28),
                arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.2))
    ax.text(zx + 1.05, zy + 1.33, '交叉 ≥ 3 m（工程取 20 m）', ha='center', va='bottom',
            fontsize=7.4, color='#c0392b', zorder=11,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.text(zx + zw / 2, zy - 0.10, '相邻两对的探测区首尾交叠，消除端头盲区',
            ha='center', va='top', fontsize=7.6, color='#5d6d7e', zorder=11)

    # 供电电源点（位于各分区中段外侧）
    for sx, sy in [(6.0, py0 + ph + 0.22), (px0 + pw + 0.24, 3.2), (3.5, py0 - 0.26)]:
        ax.add_patch(Rectangle((sx - 0.20, sy - 0.14), 0.40, 0.28, facecolor='#fdebd0',
                               edgecolor='#d4a017', linewidth=1.3, zorder=6))
        ax.text(sx, sy, 'AC/DC', ha='center', va='center', fontsize=6.2,
                color='#9a6d00', fontweight='bold', zorder=7)

    # 图例
    handles = [
        plt.Line2D([0], [0], marker='o', color='none', markerfacecolor='#1a5490',
                   markeredgecolor='white', markersize=8,
                   label='微波对射（1 对 = 发 + 收，共 15 对 / 30 台）'),
        plt.Line2D([0], [0], color='#7fb3d5', lw=1.2, linestyle='--',
                   label='相邻波束交叠（步进 80 m，交叉 20 m）'),
        plt.Line2D([0], [0], color='#1e8449', lw=3.2, label='供电分区 A（1~5 对）'),
        plt.Line2D([0], [0], color='#1a5490', lw=3.2, label='供电分区 B（6~10 对）'),
        plt.Line2D([0], [0], color='#9a6d00', lw=3.2, label='供电分区 C（11~15 对，干线 2.5 mm² 校核）'),
    ]
    ax.legend(handles=handles, loc='lower left', fontsize=8.2, ncol=2,
              frameon=True, bbox_to_anchor=(0.02, 0.0))

    ax.text(0.55, 10.15, '案例一：1200 m 周界\n15 对 · 均匀步进 80 m（交叉 20 m）\n'
                         '安装高度 0.9 m · 距围墙 1.5~2.0 m · 立杆高 1.1 m',
            ha='left', va='top', fontsize=9.0, fontweight='bold', color=C_TITLE,
            bbox=dict(boxstyle='round,pad=0.3', fc='#eafaf1', ec='#a9dfbf'))

    ax.text(8.0, 1.72, '设计校核：段长 100 m ≤ 100 m（地标基准）[符合]｜交叉 20 m ≥ 3 m [符合]\n'
                       '供电压降 1.01 V ≤ 1.2 V（24 V · 2.5 mm² · 最远 212 m）[符合]',
            ha='center', va='center', fontsize=8.6, color='#5d6d7e',
            bbox=dict(boxstyle='round,pad=0.35', fc='#fbfcfc', ec='#d5dbdb'))
    ax.text(8.0, 1.18, '布点避让：车行大门（波束穿墙打到路面）、金属摄像立杆（强反射面）、树冠投影（净空走廊）\n'
                       '—— 三类点位两端各退 2~3 m，并改用短段过渡',
            ha='center', va='center', fontsize=8.2, color='#5d6d7e')

    out = os.path.join(OUT_DIR, 'scene-topology.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


if __name__ == '__main__':
    fig_arch()
    fig_geo()
    fig_flow()
    fig_scene()
    print('ALL DONE')
