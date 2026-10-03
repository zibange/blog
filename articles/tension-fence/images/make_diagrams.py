# -*- coding: utf-8 -*-
"""
张力围栏配图生成脚本
遵循链路绘制规范：正交分支、双色线型编码、无悬空箭头
图例：主链路=绿实线、控制/状态=蓝虚线、异常/报警=红虚线
输出：图1 arch-system / 图2 geo-install / 图3 flow-signal / 图4 scene-topology
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle
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


def draw_diamond(ax, x, y, w, h, text, fill='#fff3cd', edge='#d4a017', fontsize=9):
    pts = [(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)]
    poly = Polygon(pts, closed=True, facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=2)
    ax.add_patch(poly)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, color=C_TITLE, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None,
          label_pos=0.5, label_offset=(0, 0.06), lw=1.8):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=lw, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(lx, ly, label, ha='center', va='bottom', fontsize=8, color=color, zorder=5,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


def arrow_bidir(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None, lw=1.8):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='<->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=lw, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)
    if label:
        ax.text((x1 + x2) / 2, max(y1, y2) + 0.16, label, ha='center', va='bottom',
                fontsize=8, color=color, zorder=5,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


def fig_setup(title, xlim=(0, 10), ylim=(0, 8)):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', color=C_TITLE, pad=15)
    return fig, ax


def legend(ax, items, x=0.2, y=0.3):
    handles = [mpatches.Patch(facecolor='none', edgecolor=c, linewidth=2.2,
                              linestyle=ls, label=t) for t, c, ls in items]
    ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.02, -0.02),
              fontsize=9, frameon=True, ncol=len(items))


# ---------------------------------------------------------------- 图1 四层架构
def fig_arch():
    fig, ax = fig_setup('图1 张力围栏周界报警系统四层架构（示意）', (0, 10), (0, 9.4))

    layers = [
        (7.9, '① 前端机械层', '张力索 · 张紧弹簧 · 承力杆 / 滑轮杆 / 支撑杆 / 测控杆', '#d5f5e3', C_MAIN),
        (6.2, '② 张力探测控制层', '张力传感器 · 阈值比较 · 四态判别 · 气候自适应 · 自检/防拆', '#d6eaf8', C_OUT),
        (4.5, '③ 传输与供电层', '无电位常闭触点 / 总线地址码 · DC12-24V 或 AC220V · 防雷接地  ≤4Ω', '#fdebd0', '#d4a017'),
        (2.8, '④ 平台与联动层', '电子地图定位 · 视频预置位复核 · 声光警号 · 照明联动 · 运维工单', '#fadbd8', C_ERR),
    ]
    for y, title, desc, fill, edge in layers:
        bar = FancyBboxPatch((0.7, y), 8.6, 1.25,
                             boxstyle="round,pad=0.02,rounding_size=0.10",
                             linewidth=1.6, edgecolor=edge, facecolor=fill, zorder=2)
        ax.add_patch(bar)
        ax.text(5.0, y + 0.85, title, ha='center', va='center', fontsize=11.5,
                fontweight='bold', color=C_TITLE, zorder=3)
        ax.text(5.0, y + 0.34, desc, ha='center', va='center', fontsize=8.6,
                color='#34495e', zorder=3)

    for i in range(3):
        y1 = 7.9 - i * 1.7
        y2 = y1 - 0.45
        arrow(ax, 5.0, y2, 5.0, y1, color=C_MAIN, style='solid')

    # 左侧：力→电的标注
    ax.text(0.55, 8.5, '机械力\n（张力/位移）', ha='left', va='center', fontsize=8.5,
            color='#1e8449', fontweight='bold')
    ax.text(0.55, 6.85, '电量\n（mV/数字量）', ha='left', va='center', fontsize=8.5,
            color='#1a5490', fontweight='bold')
    ax.text(0.55, 5.15, '开关量 / 报文', ha='left', va='center', fontsize=8.5,
            color='#9a6d00', fontweight='bold')
    ax.text(0.55, 3.45, '处置动作', ha='left', va='center', fontsize=8.5,
            color='#a93226', fontweight='bold')

    # 右侧反馈回路
    arrow(ax, 9.55, 3.4, 9.55, 8.5, color=C_OUT, style='dashed',
          label='远程读取张力值 / 复位 / 校核', label_pos=0.5, label_offset=(-2.55, 0))

    ax.text(5.0, 1.35, '注：前端机械层是「传感器」的一部分 —— 索的材质、弹簧刚度、杆件壁厚与基础沉降\n'
                       '均直接影响探测性能；标准依据 GA/T 1032-2013。',
            ha='center', va='center', fontsize=8.4, color='#5d6d7e',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fbfcfc', ec='#d5dbdb'))

    legend(ax, [('主链路（力→电→报）', C_MAIN, '-'), ('控制 / 状态反馈', C_OUT, '--'),
                ('平台联动', C_ERR, '-')])
    out = os.path.join(OUT_DIR, 'arch-system.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


# ------------------------------------------------- 图2 附属式与落地式安装几何
def fig_geo():
    # 关键：附属式与落地式采用同一比例尺（1 单位 ≈ 0.25 m），保证视觉上可直接比较
    fig, ax = fig_setup('图2 附属式与落地式安装几何尺寸（示意，图内两栏同一比例尺）',
                        (0, 14.6), (0, 9.2))

    def wall(ax, x0, x1, ytop, colr='#bdc3c7'):
        ax.add_patch(Rectangle((x0, 0), x1 - x0, ytop, facecolor=colr,
                               edgecolor=C_WALL, linewidth=1.3, zorder=1))

    def cable(ax, x0, x1, y):
        ax.plot([x0, x1], [y, y], color=C_WIRE, linewidth=1.8, zorder=3)
        ax.plot([x0, x1], [y, y], color='white', linewidth=0.6,
                linestyle=(0, (3, 3)), zorder=4)

    def dim(ax, x, y0, y1, text, side=1):
        ax.annotate('', xy=(x, y1), xytext=(x, y0),
                    arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.2))
        ax.text(x + 0.12 * side, (y0 + y1) / 2, text, ha='left' if side > 0 else 'right',
                va='center', fontsize=8, color='#c0392b',
                bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.9))

    S = 1.75                     # 比例尺：1 单位 = 0.4 m（两栏同一比例）
    def m(v):                    # 米 → 画布单位
        return v * S

    # ================= 左：附属式 =================
    ax.text(3.3, 8.75, '附属式（加装于既有围墙上方）', ha='center', va='center',
            fontsize=11.5, fontweight='bold', color=C_TITLE)
    wall_top = m(2.2)                                  # 围墙 2.2 m
    wall(ax, 1.1, 5.5, wall_top)

    floor = wall_top + m(0.14)                          # 最下索：墙顶 +140 mm
    ys = [floor + i * m(0.20) for i in range(4)]        # 4 线，200 mm 间距 → 围栏高 800 mm
    for y in ys:
        cable(ax, 1.1, 5.5, y)

    for px in (1.35, 3.3, 5.25):
        ax.plot([px, px], [wall_top, ys[-1] + 0.20], color='#34495e', linewidth=3.4, zorder=2)
    ax.text(3.3, ys[-1] + 0.42, '测控杆 / 承力杆 / 支撑杆', ha='center', va='center',
            fontsize=8.2, color='#34495e')

    dim(ax, 0.90, wall_top, ys[-1], '围栏高度\n≥ 750 mm')
    dim(ax, 0.90, 0, ys[-1], '顶索离地 ≥ 2000 mm')
    dim(ax, 5.75, wall_top, floor, '130~150 mm', side=1)
    ax.annotate('', xy=(6.30, ys[1]), xytext=(6.30, ys[0]),
                arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.1))
    ax.text(6.40, (ys[0] + ys[1]) / 2, '200±10\nmm', ha='left', va='center',
            fontsize=7.8, color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.text(3.3, wall_top - m(1.0), '实体围墙（示例 2.2 m）', ha='center', va='center',
            fontsize=8.4, color='#5d6d7e')
    ax.text(1.15, ys[-1] + 0.55, '示例：4 线 / 200 mm\n围栏高 800 mm ≥ 750 mm [符合]',
            ha='left', va='bottom', fontsize=8.0, color='#1e8449',
            bbox=dict(boxstyle='round,pad=0.3', fc='#eafaf1', ec='#a9dfbf'))
    # ================= 右：落地式 =================
    ax.text(10.4, 8.75, '落地式（无围墙，独立成栏）', ha='center', va='center',
            fontsize=11.5, fontweight='bold', color=C_TITLE)

    lo = [m(0.10) + i * m(0.15) for i in range(9)]      # 1500 以下：9 道，150 mm（首道抬离基线）
    hi = [m(1.60), m(1.80), m(2.00)]                    # 1500 以上：3 道，200 mm
    ys2 = lo + hi
    for y in ys2:
        cable(ax, 7.6, 12.4, y)

    for px in (7.85, 10.4, 12.15):
        ax.plot([px, px], [-0.05, ys2[-1] + 0.18], color='#34495e', linewidth=3.6, zorder=2)
        ax.add_patch(Rectangle((px - 0.13, -m(0.10)), 0.26, m(0.10), facecolor='#5d6d7e',
                               edgecolor='#2c3e50', linewidth=1.0, zorder=2))
    ax.text(10.4, ys2[-1] + 0.40, '测控杆 / 承力杆 / 支撑杆（均须加固）', ha='center',
            va='center', fontsize=8.2, color='#34495e')

    dim(ax, 7.32, 0.0, ys2[-1], '围栏高度\n≥ 2000 mm')
    ax.annotate('', xy=(12.85, lo[1]), xytext=(12.85, lo[0]),
                arrowprops=dict(arrowstyle='<->', color='#1a5490', lw=1.1))
    ax.text(12.95, (lo[0] + lo[1]) / 2, '150±10', ha='left', va='center', fontsize=7.8,
            color='#1a5490', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.annotate('', xy=(12.85, hi[1]), xytext=(12.85, hi[0]),
                arrowprops=dict(arrowstyle='<->', color='#1a5490', lw=1.1))
    ax.text(12.95, (hi[0] + hi[1]) / 2, '200±10', ha='left', va='center', fontsize=7.8,
            color='#1a5490', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.plot([7.3, 13.3], [m(1.5), m(1.5)], color='#1a5490', linewidth=0.9,
            linestyle='--', zorder=1)
    ax.text(7.4, m(1.5) + 0.10, '1500 mm 分界（下密上疏）', ha='left', va='bottom',
            fontsize=8, color='#1a5490')
    ax.text(10.4, ys2[-1] + 0.20, '示例：12 线（9×150 mm + 3×200 mm）\n围栏高 2000 mm ≥ 2000 mm [符合]',
            ha='center', va='bottom', fontsize=8.0, color='#1e8449',
            bbox=dict(boxstyle='round,pad=0.3', fc='#eafaf1', ec='#a9dfbf'))

    ax.text(6.9, -0.30, '逻辑：1500 mm 以下易钻易蹬 → 加密至 150 mm；以上主要防跨越 → 200 mm 已足',
            ha='center', va='center', fontsize=8.6, color='#5d6d7e',
            bbox=dict(boxstyle='round,pad=0.35', fc='#fbfcfc', ec='#d5dbdb'))

    ax.text(6.9, -0.95, '注：尺寸依据 GA/T 1032-2013 附录 A.2.5（附属式）与 A.2.6（落地式）；'
                        '图内两栏同一比例尺，为示意非施工图。',
            ha='center', va='center', fontsize=8.4, color='#5d6d7e')

    out = os.path.join(OUT_DIR, 'geo-install.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


# ------------------------------------------- 图3 张力—位移转换与四态判定链路
def fig_flow():
    fig, ax = fig_setup('图3 张力—位移转换与四态判定链路（示意）', (0, 12.2), (0, 8.6))

    draw_box(ax, 0.35, 6.95, 2.5, 0.86, '外部载荷\n攀爬 / 蹬踏 / 剪断 / 环境',
             fill='#d5f5e3', edge=C_MAIN, fontsize=8.8)
    draw_box(ax, 3.35, 6.95, 2.5, 0.86, '张紧弦力学响应\nF = 2·T·sinθ\nδ ≈ F·S /(4·T)',
             fill='#d5f5e3', edge=C_MAIN, fontsize=8.4)
    draw_box(ax, 6.35, 6.95, 2.5, 0.86, '张紧弹簧缓冲\nK_total 串联降刚度\n吸收温漂位移',
             fill='#d5f5e3', edge=C_MAIN, fontsize=8.4)
    draw_box(ax, 9.35, 6.95, 2.5, 0.86, '张力传感模块\n应变 / 位移 / 矢量\n→ 电量输出',
             fill='#d6eaf8', edge=C_OUT, fontsize=8.4)

    for x1, x2 in ((2.85, 3.35), (5.85, 6.35), (8.85, 9.35)):
        arrow(ax, x1, 7.38, x2, 7.38, color=C_MAIN, style='solid')

    arrow(ax, 10.6, 6.95, 10.6, 6.35, color=C_OUT, style='solid')
    draw_diamond(ax, 8.55, 5.35, 4.1, 1.0, '变化速率判别\n慢变（温漂）→ 跟随\n快变（入侵）→ 判定',
                 fill='#fff3cd', edge='#d4a017', fontsize=8.4)

    # 慢变分支（左）
    arrow(ax, 8.85, 5.35, 8.85, 4.55, color=C_OUT, style='dashed')
    draw_box(ax, 5.35, 3.70, 4.2, 0.85, '气候自适应：自动调整警戒张力值\n（不报警，维持 100~450 N 区间）',
             fill='#d6eaf8', edge=C_OUT, fontsize=8.2)

    # 四态判定（右，与慢变分支横向错开）
    arrow(ax, 11.35, 5.35, 11.35, 4.55, color=C_ERR, style='solid')
    draw_box(ax, 9.75, 3.70, 2.55, 0.85, '四态判别\n响应 ≤ 3 s',
             fill='#fadbd8', edge=C_ERR, fontsize=8.8, fontweight='bold')

    states = [
        (1.15, '拉紧报警\n位移 ≥ 阈值\n（≤ 75 mm）', '#fadbd8', C_ERR),
        (3.55, '松弛报警\n张力 < 警戒值 1/3', '#fadbd8', C_ERR),
        (5.95, '剪断报警\n张力趋近于零', '#fadbd8', C_ERR),
        (8.35, '防拆报警\n外壳被打开', '#fadbd8', C_ERR),
    ]
    for x, t, f, e in states:
        draw_box(ax, x, 2.05, 2.1, 1.05, t, fill=f, edge=e, fontsize=8.2)
        arrow(ax, x + 1.05, 3.70, x + 1.05, 3.10, color=C_ERR, style='solid')

    # 汇总输出
    arrow(ax, 10.6, 2.05, 10.6, 1.45, color=C_ERR, style='solid')
    draw_box(ax, 8.6, 0.55, 3.6, 0.92, '报警输出\n无电位常闭触点 / 数据接口\n持续 > 1 s，10 s 内恢复警戒',
             fill='#d6eaf8', edge=C_OUT, fontsize=8.2)

    # 平台
    arrow(ax, 8.6, 1.01, 6.9, 1.01, color=C_MAIN, style='solid', label='上平台',
          label_pos=0.5, label_offset=(0, 0.08))
    draw_box(ax, 4.5, 0.55, 2.3, 0.92, '视频复核\n电子地图定位', fill='#d5f5e3',
             edge=C_MAIN, fontsize=8.4)

    # 关键数字
    ax.text(1.15, 5.0, '灵敏度算例（S = 4 m，δ = 75 mm）\n'
                       '  T = 100 N  →  F ≈ 7.5 N\n'
                       '  T = 200 N  →  F ≈ 15.0 N\n'
                       '  T = 450 N  →  F ≈ 33.7 N\n'
                       '张力越低越灵敏，也越易误报',
            ha='left', va='center', fontsize=8.2, color='#1e8449',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fbfcfc', ec='#a9dfbf'))

    ax.text(1.15, 0.95, '温漂算例（L = 40 m，Δt = 40 ℃）\n'
                        '  无弹簧：ΔT ≈ 105 N\n'
                        '  串弹簧 k = 2 N/mm：ΔT ≈ 36 N\n'
                        '弹簧是核心设计元件，不是配件',
            ha='left', va='center', fontsize=8.2, color='#1a5490',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fbfcfc', ec='#aed6f1'))

    legend(ax, [('主链路（力学→电量→判定）', C_MAIN, '-'),
                ('气候自适应 / 状态反馈', C_OUT, '--'),
                ('报警分支', C_ERR, '-')], x=0.4, y=0)
    out = os.path.join(OUT_DIR, 'flow-signal.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white', dpi=150)
    plt.close(fig)
    print('OK', out)


# ---------------------------------- 图4 不规则周界防区划分与拐角杆件配置
def fig_scene():
    fig, ax = fig_setup('图4 不规则周界防区划分与拐角杆件配置（示意）', (0, 12.4), (0, 8.8))

    # 周界折线（860 m 不规则周界，含 14 处拐角的简化表达）
    pts = [(0.9, 2.2), (3.2, 2.2), (4.5, 3.6), (4.5, 5.4), (6.4, 6.7),
           (8.6, 6.7), (10.0, 5.2), (11.5, 5.2), (11.5, 3.1), (9.6, 1.7)]

    ax.plot([p[0] for p in pts], [p[1] for p in pts], color='#34495e',
            linewidth=2.6, zorder=2, solid_capstyle='round')

    # 张力索（沿折线的平行多道，用偏移简化表达）
    for off in (-0.12, 0, 0.12):
        xs, ys = [], []
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            dx, dy = x2 - x1, y2 - y1
            L = (dx ** 2 + dy ** 2) ** 0.5
            nx, ny = -dy / L * off, dx / L * off
            xs += [x1 + nx, x2 + nx]
            ys += [y1 + ny, y2 + ny]
        ax.plot(xs, ys, color=C_WIRE, linewidth=1.0, zorder=3, alpha=0.9)

    # 拐角分类：锐角 < 120° → 承力杆（红方）；钝角 ≥ 120° → 滑轮杆（蓝圆）
    sharp = [1, 2, 3, 5, 6, 7, 8]          # 示意
    obtuse = [0, 4, 9]
    for i in sharp:
        x, y = pts[i]
        ax.add_patch(Rectangle((x - 0.13, y - 0.13), 0.26, 0.26, facecolor='#e74c3c',
                               edgecolor='white', linewidth=1.0, zorder=5))
    for i in obtuse:
        x, y = pts[i]
        ax.add_patch(plt.Circle((x, y), 0.14, facecolor='#3498db',
                                edgecolor='white', linewidth=1.0, zorder=5))

    # 测控杆：一律布置在直线段中部（绿三角），避让所有转角
    mid_pos = []
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        mid_pos.append(((x1 + x2) / 2, (y1 + y2) / 2))
    for (x, y) in mid_pos:
        ax.add_patch(Polygon([(x, y + 0.17), (x + 0.16, y - 0.11), (x - 0.16, y - 0.11)],
                             facecolor='#2ecc71', edgecolor='white', linewidth=1.0, zorder=5))

    # 支撑杆示意（一段上）
    (ax1, ay1), (ax2, ay2) = pts[0], pts[1]
    for t in (0.2, 0.4, 0.6, 0.8):
        sx = ax1 + (ax2 - ax1) * t
        sy = ay1 + (ay2 - ay1) * t
        ax.plot([sx, sx], [sy - 0.10, sy + 0.10], color='#7f8c8d', linewidth=1.6, zorder=4)
    ax.text((ax1 + ax2) / 2, ay1 - 0.55, '支撑杆 3~5 m', ha='center', va='center',
            fontsize=8, color='#5d6d7e')

    # 防区标注
    ax.annotate('', xy=(pts[1][0], pts[1][1] + 0.42), xytext=(pts[0][0] + 0.35, pts[0][1] + 0.42),
                arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.2))
    ax.text((pts[0][0] + pts[1][0]) / 2, pts[1][1] + 0.62, '防区长度 ≤ 40 m', ha='center',
            va='center', fontsize=8.2, color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.9))

    ax.annotate('', xy=(pts[3][0] + 0.45, pts[3][1]), xytext=(pts[3][0] + 0.45, pts[2][1]),
                arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.2))
    ax.text(pts[3][0] + 0.62, (pts[2][1] + pts[3][1]) / 2, '段长随拐角\n缩短至 30 m 级',
            ha='left', va='center', fontsize=8, color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.9))

    # 图例
    handles = [
        mpatches.Patch(facecolor='#e74c3c', edgecolor='white', label='承力杆（拐角 < 120°）'),
        mpatches.Patch(facecolor='#3498db', edgecolor='white', label='滑轮杆（拐角 ≥ 120°）'),
        mpatches.Patch(facecolor='#2ecc71', edgecolor='white', label='测控杆（仅布于直线段）'),
        plt.Line2D([0], [0], color='#7f8c8d', lw=2.0, label='支撑杆（3~5 m）'),
    ]
    ax.legend(handles=handles, loc='upper center', fontsize=8.6, ncol=2,
              frameon=True, bbox_to_anchor=(0.5, 1.005))

    ax.text(6.2, 0.75, '切分策略：① 每处拐角均置于防区边界，使每防区拐弯数 ≤ 1（优于标准要求的 ≤ 2）；\n'
                       '② 拐角处设承力杆形成可靠锚点，测控杆一律避让转角；③ 报警定位不跨拐角，处置路径唯一。',
            ha='center', va='center', fontsize=8.6, color='#5d6d7e',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fbfcfc', ec='#d5dbdb'))

    ax.text(0.9, 7.9, '案例三：860 m 别墅区不规则周界\n14 处拐角 → 24 个防区，平均段长 35.8 m',
            ha='left', va='center', fontsize=9.2, fontweight='bold', color=C_TITLE,
            bbox=dict(boxstyle='round,pad=0.3', fc='#eafaf1', ec='#a9dfbf'))

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
