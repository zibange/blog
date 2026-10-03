# -*- coding: utf-8 -*-
"""
红外对射探测器配图生成脚本
遵循链路绘制规范：正交分支、双色线型编码、无悬空箭头
图例：主流程=绿实线、控制/状态=蓝虚线、异常/冗余/迭代=红虚线
"""
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
          label_pos=0.5, label_offset=(0, 0.05), lw=1.8):
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
        ax.text((x1 + x2) / 2, max(y1, y2) + 0.18, label, ha='center', va='bottom',
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


# ---------------------------------------------------------------- 图1 系统架构
def draw_arch_system():
    fig, ax = fig_setup('图1  红外对射周界报警系统四层架构（示意）', (0, 14), (0, 10.4))

    layers = [
        (8.0, '① 探测层', '#dff5e6'),
        (5.9, '② 传输与供电层', '#e3f0fb'),
        (3.8, '③ 报警控制层', '#fdeae6'),
        (1.7, '④ 平台与联动层', '#f1eaf7'),
    ]
    for y, name, color in layers:
        band = FancyBboxPatch((0.35, y - 0.25), 13.3, 1.7,
                              boxstyle="round,pad=0.01,rounding_size=0.05",
                              linewidth=1.0, edgecolor='#bdc3c7',
                              facecolor=color, zorder=1)
        ax.add_patch(band)
        ax.text(0.55, y + 1.15, name, ha='left', va='center', fontsize=9.5,
                fontweight='bold', color=C_TITLE, zorder=3)

    # ① 探测层
    draw_box(ax, 1.0, 8.0, 3.0, 1.2, '发射端 TX\n红外LED + 聚焦透镜', fill='#ffffff')
    draw_box(ax, 5.5, 8.0, 3.0, 1.2, '接收端 RX\n光敏管 + 窄带滤光片', fill='#ffffff')
    draw_box(ax, 10.0, 8.0, 3.0, 1.2, '立杆 / 支架 / 防拆开关', fill='#ffffff')
    arrow_bidir(ax, 4.0, 8.6, 5.5, 8.6, color=C_ERR, style='dashed',
                label='不可见调制红外光束')
    arrow(ax, 10.0, 8.6, 8.5, 8.6, color=C_BOX, style='dotted', label='机械承载',
          label_offset=(0, 0.1))

    # ② 传输与供电层
    draw_box(ax, 1.0, 5.9, 3.0, 1.2, '集中电源\nDC 12 / 24 V 稳压', fill='#ffffff')
    draw_box(ax, 5.5, 5.9, 3.0, 1.2, '信号线缆\n开关量 / 总线 / 网络', fill='#ffffff')
    draw_box(ax, 10.0, 5.9, 3.0, 1.2, '防雷器 / 接地\n≤ 4 Ω', fill='#ffffff')
    arrow(ax, 2.5, 7.1, 2.5, 8.0, color=C_MAIN, label='供电')
    arrow(ax, 7.0, 7.1, 7.0, 8.0, color=C_MAIN, label='报警信号')
    arrow(ax, 11.5, 7.1, 11.5, 8.0, color=C_MAIN, label='保护地')

    # ③ 报警控制层
    draw_box(ax, 1.0, 3.8, 3.0, 1.2, '防区扩展模块\n地址码 / 防区号', fill='#ffffff')
    draw_box(ax, 5.5, 3.8, 3.0, 1.2, '报警主机\n布撤防 / 防区管理', fill='#ffffff')
    draw_box(ax, 10.0, 3.8, 3.0, 1.2, '继电器输出\n警号 / 灯光 / 广播', fill='#ffffff')
    arrow(ax, 7.0, 5.9, 7.0, 5.0, color=C_MAIN)
    arrow(ax, 4.0, 4.4, 5.5, 4.4, color=C_MAIN)
    arrow(ax, 8.5, 4.4, 10.0, 4.4, color=C_MAIN)

    # ④ 平台与联动层
    draw_box(ax, 1.0, 1.7, 3.0, 1.2, '安防管理平台\n电子地图 / 预案', fill='#ffffff')
    draw_box(ax, 5.5, 1.7, 3.0, 1.2, '视频复核\n摄像机预置位联动', fill='#ffffff')
    draw_box(ax, 10.0, 1.7, 3.0, 1.2, '运维工单\n巡检 / 寿命台账', fill='#ffffff')
    arrow(ax, 7.0, 3.8, 7.0, 2.9, color=C_OUT, style='dashed', label='事件上传')
    arrow(ax, 4.0, 2.3, 5.5, 2.3, color=C_MAIN)
    arrow(ax, 8.5, 2.3, 10.0, 2.3, color=C_MAIN)

    # 图例
    items = [(C_MAIN, '-', '主链路 / 供电与信号流'),
             (C_ERR, '--', '红外光束（探测介质）'),
             (C_OUT, '--', '事件上传 / 平台联动')]
    for i, (c, ls, t) in enumerate(items):
        x = 1.0 + i * 4.1
        ax.plot([x, x + 0.4], [0.55, 0.55], color=c, linestyle=ls, linewidth=2, zorder=5)
        ax.text(x + 0.55, 0.55, t, ha='left', va='center', fontsize=8.5, color=C_TITLE, zorder=5)

    out = os.path.join(OUT_DIR, 'arch-system.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', out)


# ------------------------------------------------------------ 图2 判定信号链
def draw_flow_signal():
    fig, ax = fig_setup('图2  从发光到报警：遮断判定信号链（示意）', (0, 16), (0, 10.2))

    draw_box(ax, 9.0, 8.3, 3.2, 1.0, '干扰源：阳光 / 雨雾 / 飘落物',
             fill='#fdecea', edge=C_ERR, fontsize=9)

    chain = [
        (0.4, '① 红外发光\n850 / 940 nm', '#ffffff'),
        (3.4, '② 脉冲调制\n约 1000 pps', '#ffffff'),
        (6.4, '③ 聚焦与大气传输\n雨雾衰减', '#ffffff'),
        (9.4, '④ 滤光接收\n光敏管 + 窄带片', '#ffffff'),
        (12.4, '⑤ 解调放大\nAGC 自动增益', '#ffffff'),
    ]
    for x, t, f in chain:
        draw_box(ax, x, 6.2, 2.4, 1.2, t, fill=f, fontsize=8.5)

    for i in range(4):
        x1 = chain[i][0] + 2.4
        x2 = chain[i + 1][0]
        arrow(ax, x1, 6.8, x2, 6.8, color=C_MAIN)

    arrow(ax, 10.6, 8.3, 10.6, 7.4, color=C_ERR, style='dashed', label='叠加干扰')

    # 主链下行到判定
    arrow(ax, 13.6, 6.2, 13.6, 3.9, color=C_MAIN)
    arrow(ax, 13.6, 3.9, 10.2, 3.9, color=C_MAIN)
    draw_diamond(ax, 6.9, 3.0, 3.3, 1.8, '遮断时长\n≥ 设定阈值 ?', fontsize=9)

    draw_box(ax, 0.3, 3.3, 2.8, 1.2, '不报警\n返回监测', fill='#eef7ee', fontsize=9)
    arrow(ax, 6.9, 3.9, 3.1, 3.9, color=C_OUT, style='dashed', label='否')

    draw_box(ax, 6.4, 0.9, 3.8, 1.2, '输出报警：开关量 / 总线\n防区号上传主机',
             fill='#e6f7ee', edge=C_MAIN, fontsize=9)
    arrow(ax, 8.55, 3.0, 8.55, 2.1, color=C_MAIN, label='是', label_offset=(0.35, 0))

    # 遮光时间窗设定（虚线接入判定）
    draw_box(ax, 0.3, 0.9, 2.8, 1.2, '遮光时间窗设定\n20 / 40 ms，可调', fill='#ffffff',
             edge=C_BOX, fontsize=8.5)
    ax.plot([1.7, 1.7, 8.55], [2.1, 5.6, 5.6], color=C_OUT, linestyle='--', linewidth=1.6, zorder=3)
    arrow(ax, 8.55, 5.6, 8.55, 4.8, color=C_OUT, style='dashed')

    items = [(C_MAIN, '-', '主判定链路'),
             (C_ERR, '--', '环境干扰 / 衰减'),
             (C_OUT, '--', '参数设定 / 不报警分支')]
    for i, (c, ls, t) in enumerate(items):
        x = 0.6 + i * 5.0
        ax.plot([x, x + 0.4], [0.25, 0.25], color=c, linestyle=ls, linewidth=2, zorder=5)
        ax.text(x + 0.55, 0.25, t, ha='left', va='center', fontsize=8.5, color=C_TITLE, zorder=5)

    out = os.path.join(OUT_DIR, 'flow-signal.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', out)


# ------------------------------------------------------------ 图3 选型核算流程
def draw_flow_sizing():
    fig, ax = fig_setup('图3  红外对射选型核算七步流程（示意）', (0, 14), (-1.4, 13.8))

    steps = [
        (11.7, '① 收集周界条件：长度 / 走向 / 围墙形式 / 转角 / 植被 / 气候', '#ffffff'),
        (10.1, '② 按直线段分段，段长记为 L_seg（转角必分段）', '#ffffff'),
        (8.5, '③ 距离折减：L_use = L_nom × k_env（0.5 ~ 0.8）', '#ffffff'),
        (4.4, '④ 光束数与遮光时间设定（人体遮挡模型校核）', '#ffffff'),
        (2.8, '⑤ 防区划分与主机容量 / 防区号规划', '#ffffff'),
        (1.2, '⑥ 供电与压降核算、防雷接地、点位表出图', '#ffffff'),
    ]
    for y, t, f in steps[:3]:
        draw_box(ax, 3.5, y, 6.0, 1.1, t, fill=f, fontsize=9)
    for y, t, f in steps[3:]:
        draw_box(ax, 3.5, y, 6.0, 1.1, t, fill=f, fontsize=9)

    arrow(ax, 6.5, 11.7, 6.5, 11.2, color=C_MAIN)
    arrow(ax, 6.5, 10.1, 6.5, 9.6, color=C_MAIN)

    draw_diamond(ax, 4.4, 6.4, 4.2, 1.8, 'L_seg ≤ 0.8 × L_use ?', fontsize=9)
    draw_box(ax, 10.6, 6.75, 3.0, 1.1, '缩短分段\n或换长距型号', fill='#fdecea',
             edge=C_ERR, fontsize=8.5)
    arrow(ax, 8.6, 7.3, 10.6, 7.3, color=C_ERR, style='dashed', label='否',
          label_offset=(0, 0.08))
    ax.plot([12.1, 12.1, 9.5], [7.85, 10.65, 10.65], color=C_ERR, linestyle='--',
            linewidth=1.6, zorder=3)
    arrow(ax, 9.5, 10.65, 9.5, 10.65, color=C_ERR, style='dashed')
    ax.text(10.8, 10.9, '迭代重算', ha='center', va='bottom', fontsize=8, color=C_ERR)

    arrow(ax, 6.5, 6.4, 6.5, 5.5, color=C_MAIN, label='是', label_offset=(0.35, 0))
    arrow(ax, 6.5, 4.4, 6.5, 3.9, color=C_MAIN)
    arrow(ax, 6.5, 2.8, 6.5, 2.3, color=C_MAIN)

    draw_box(ax, 3.5, 0.0, 6.0, 0.9, '⑦ 调试与验收：光轴对准 → 受光电压峰值 → 遮光实测',
             fill='#e6f7ee', edge=C_MAIN, fontsize=9)
    arrow(ax, 6.5, 1.2, 6.5, 0.9, color=C_MAIN)

    items = [(C_MAIN, '-', '核算主流程'), (C_ERR, '--', '不满足时的迭代分支')]
    for i, (c, ls, t) in enumerate(items):
        x = 3.5 + i * 5.5
        ax.plot([x, x + 0.4], [-0.85, -0.85], color=c, linestyle=ls, linewidth=2, zorder=5)
        ax.text(x + 0.55, -0.85, t, ha='left', va='center', fontsize=8.5, color=C_TITLE, zorder=5)

    out = os.path.join(OUT_DIR, 'flow-sizing.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', out)


# ------------------------------------------------------------ 图4 部署拓扑
def draw_scene_topology():
    fig, ax = fig_setup('图4  四种典型周界部署拓扑（俯视示意）', (0, 14), (0, 10.4))

    def wall(xs, ys, lw=5):
        ax.plot(xs, ys, color=C_WALL, linewidth=lw, solid_capstyle='butt', zorder=2)

    def dev(x, y, label, color):
        r = Rectangle((x - 0.22, y - 0.22), 0.44, 0.44, facecolor=color,
                      edgecolor=C_BOX, linewidth=1.0, zorder=4)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=6.5,
                color='white' if color != '#ffffff' else C_TITLE,
                fontweight='bold', zorder=5)

    def beam(x1, y1, x2, y2, label=None, lo=0.0):
        if abs(y2 - y1) < 1e-6:
            yy = y1 + lo
            ax.annotate('', xy=(x2, yy), xytext=(x1, yy),
                        arrowprops=dict(arrowstyle='<->', color=C_ERR,
                                        linestyle='--', linewidth=1.4), zorder=3)
            if label:
                ax.text((x1 + x2) / 2, yy + 0.16, label, ha='center', va='bottom',
                        fontsize=7, color=C_ERR, zorder=5,
                        bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.8))
        else:
            xx = x1 + lo
            ax.annotate('', xy=(xx, y2), xytext=(xx, y1),
                        arrowprops=dict(arrowstyle='<->', color=C_ERR,
                                        linestyle='--', linewidth=1.4), zorder=3)

    # ① 直线段：背靠背 + 错频
    wall([0.7, 5.6], [7.6, 7.6])
    dev(1.2, 7.6, 'T', '#e67e22')
    dev(2.6, 7.6, 'R', '#2980b9')
    dev(3.4, 7.6, 'R', '#2980b9')
    dev(4.8, 7.6, 'T', '#e67e22')
    beam(1.2, 7.6, 2.6, 7.6, '对射 A', lo=0.45)
    beam(4.8, 7.6, 3.4, 7.6, '对射 B', lo=0.95)
    ax.text(2.75, 6.5, '① 直线段：TX/RX 背靠背 + 错频，避免串扰',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_TITLE)

    # ② 转角：双向对射
    wall([7.4, 12.6], [9.0, 9.0])
    wall([12.6, 12.6], [9.0, 5.9])
    dev(7.8, 9.0, 'T', '#e67e22')
    dev(12.1, 9.0, 'R', '#2980b9')
    beam(7.8, 9.0, 12.1, 9.0, '横向', lo=0.45)
    dev(12.6, 8.5, 'T', '#e67e22')
    dev(12.6, 6.4, 'R', '#2980b9')
    beam(12.6, 8.5, 12.6, 6.4, lo=-0.45)
    ax.text(11.9, 7.5, '纵向', ha='right', va='center', fontsize=7, color=C_ERR,
            bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.8))
    ax.text(10.0, 5.3, '② 转角：双向对射补点，消除拐角盲区',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_TITLE)

    # ③ 大门：旁路 + 视频复核
    wall([0.7, 2.5], [3.2, 3.2])
    wall([4.5, 5.6], [3.2, 3.2])
    dev(1.0, 3.2, 'T', '#e67e22')
    dev(2.2, 3.2, 'R', '#2980b9')
    beam(1.0, 3.2, 2.2, 3.2, lo=0.4)
    dev(4.8, 3.2, 'R', '#2980b9')
    dev(5.4, 3.2, 'T', '#e67e22')
    beam(5.4, 3.2, 4.8, 3.2, lo=0.4)
    ax.plot([2.5, 2.9], [2.85, 2.85], color='#16a085', linewidth=2.5, zorder=4)
    ax.plot([4.1, 4.5], [2.85, 2.85], color='#16a085', linewidth=2.5, zorder=4)
    ax.text(3.5, 2.5, '大门', ha='center', va='center', fontsize=7.5, color='#16a085')
    cam = plt.Circle((3.5, 4.35), 0.28, facecolor='#9b59b6', edgecolor=C_BOX, zorder=4)
    ax.add_patch(cam)
    ax.text(3.5, 4.35, 'C', ha='center', va='center', fontsize=7, color='white',
            fontweight='bold', zorder=5)
    ax.plot([3.5, 3.5], [4.07, 3.4], color=C_OUT, linestyle='--', linewidth=1.3, zorder=3)
    ax.text(2.75, 1.9, '③ 门区：门体旁路 + 摄像机预置位复核',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_TITLE)

    # ④ 高低差：错位补点
    wall([7.4, 10.0], [3.4, 3.4])
    wall([10.0, 10.0], [3.4, 2.5])
    wall([10.0, 12.8], [2.5, 2.5])
    dev(7.7, 3.4, 'T', '#e67e22')
    dev(9.7, 3.4, 'R', '#2980b9')
    beam(7.7, 3.4, 9.7, 3.4, lo=0.4)
    dev(10.3, 2.5, 'T', '#e67e22')
    dev(12.5, 2.5, 'R', '#2980b9')
    beam(10.3, 2.5, 12.5, 2.5, lo=0.4)
    dev(10.0, 2.95, 'T', '#e67e22')
    dev(10.0, 1.6, 'R', '#2980b9')
    beam(10.0, 2.95, 10.0, 1.6, lo=-0.4)
    ax.text(10.55, 3.55, '落差补点', ha='left', va='bottom', fontsize=7, color=C_ERR,
            bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.8))
    ax.text(10.2, 0.95, '④ 高低差 / 坡道：错位补点，覆盖竖向缝隙',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_TITLE)

    items = [('#e67e22', 's', '发射端 TX'), ('#2980b9', 's', '接收端 RX'),
             (C_ERR, '--', '红外光束'), ('#16a085', '-', '门体'),
             ('#9b59b6', 'o', '复核摄像机')]
    handles = []
    for c, m, t in items:
        if m == 's':
            h = mpatches.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor=C_BOX, label=t)
        elif m == 'o':
            h = plt.Line2D([], [], marker='o', color='none', markerfacecolor=c,
                           markersize=9, label=t)
        else:
            h = plt.Line2D([], [], color=c, linestyle='--', linewidth=2, label=t)
        handles.append(h)
    ax.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, -0.06),
              ncol=5, fontsize=8.5, frameon=False)

    out = os.path.join(OUT_DIR, 'scene-topology.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('OK', out)


if __name__ == '__main__':
    draw_arch_system()
    draw_flow_signal()
    draw_flow_sizing()
    draw_scene_topology()
