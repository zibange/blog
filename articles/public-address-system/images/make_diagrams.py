# -*- coding: utf-8 -*-
"""
公共广播系统（PA）架构图与流程图生成脚本
遵循链路绘制规范：正交分支、双色线型编码、双向箭头可见、跨层三段折线
图例：主流程=绿实线、输出/结果=青虚线、异常/回流=红虚线
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import os

# 中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 颜色定义
C_MAIN = '#2ecc71'       # 主流程 绿实线
C_OUT = '#3498db'        # 输出/结果 青虚线
C_ERR = '#e74c3c'        # 异常 红虚线
C_BOX = '#2c3e50'        # 框边
C_FILL = '#ecf0f1'       # 框填充
C_LAYER = '#dfe6e9'      # 层背景
C_TITLE = '#2d3436'      # 标题色
C_LEGEND_BG = '#f8f9fa'  # 图例背景


def draw_box(ax, x, y, w, h, text, fill=C_FILL, edge=C_BOX, fontsize=10, fontweight='normal'):
    """画圆角矩形框 + 居中文字"""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=1.5, edgecolor=edge, facecolor=fill, zorder=2)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, color=C_TITLE, zorder=3)


def draw_diamond(ax, x, y, w, h, text, fill='#fff3cd', edge='#d4a017', fontsize=9):
    """画菱形判定框"""
    pts = [(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)]
    poly = Polygon(pts, closed=True, facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=2)
    ax.add_patch(poly)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, color=C_TITLE, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None, label_pos=0.5, label_offset=(0, 0.05)):
    """画箭头"""
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=1.8, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(lx, ly, label, ha='center', va='bottom',
                fontsize=8, color=color, zorder=5,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


def arrow_bidir(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None):
    """画双向箭头，两端离开框边"""
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='<->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=1.8, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, label, ha='center', va='center',
                fontsize=8, color=color, zorder=5,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


def draw_legend(ax, y=0.03):
    """画底部图例"""
    items = [
        (C_MAIN, '-', '主流程 / 数据上行'),
        (C_OUT, '--', '输出 / 控制下行'),
        (C_ERR, '--', '异常 / 告警'),
    ]
    x_start = 0.15
    spacing = 0.25
    for i, (c, ls, text) in enumerate(items):
        x = x_start + i * spacing
        ax.plot([x, x + 0.08], [y, y], color=c, linestyle=ls, linewidth=2, zorder=5)
        ax.text(x + 0.1, y, text, ha='left', va='center', fontsize=8, color=C_TITLE, zorder=5)


def fig_setup(title, xlim=(0, 10), ylim=(0, 8)):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', color=C_TITLE, pad=15)
    return fig, ax


# ============================================================
# 图1：PA 系统整体架构（音源→主机→分区→终端）
# ============================================================
def draw_arch_system():
    fig, ax = fig_setup('图1 公共广播系统整体架构（示意）', xlim=(0, 12), ylim=(0, 8.5))

    # 三层背景
    ax.add_patch(mpatches.Rectangle((0.2, 6.2), 11.6, 2.0, facecolor='#e8f5e9', edgecolor='#a5d6a7', linewidth=1, zorder=0))
    ax.text(0.4, 7.9, '音源 / 输入层', fontsize=11, fontweight='bold', color='#2e7d32', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 3.2), 11.6, 2.6, facecolor='#e3f2fd', edgecolor='#90caf9', linewidth=1, zorder=0))
    ax.text(0.4, 5.5, '主机 / 控制处理层', fontsize=11, fontweight='bold', color='#1565c0', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 0.3), 11.6, 2.6, facecolor='#fff3e0', edgecolor='#ffcc80', linewidth=1, zorder=0))
    ax.text(0.4, 2.6, '分区 / 终端输出层', fontsize=11, fontweight='bold', color='#e65100', zorder=1)

    # 音源层
    src_y = 6.6
    draw_box(ax, 0.6, src_y, 1.6, 0.9, '麦克风\n(呼叫站)')
    draw_box(ax, 2.7, src_y, 1.6, 0.9, '音源播放器\n(CD/MP3)')
    draw_box(ax, 4.8, src_y, 1.6, 0.9, '消防联动\n信号输入')
    draw_box(ax, 6.9, src_y, 1.6, 0.9, '电话寻呼\n接口')
    draw_box(ax, 9.0, src_y, 2.2, 0.9, '广播软件\n(PC/管理端)')

    # 主机层
    host_y = 3.7
    draw_box(ax, 1.0, host_y + 0.7, 2.2, 1.0, '前置放大器\n信号混合/增益', fontsize=9)
    draw_box(ax, 3.8, host_y + 0.7, 2.4, 1.0, '数字音频矩阵\n分区/路由/优先级', fontsize=9, fontweight='bold')
    draw_box(ax, 6.8, host_y + 0.7, 2.2, 1.0, '功率放大器\n定压输出 100V', fontsize=9)
    draw_box(ax, 9.5, host_y + 0.7, 2.0, 1.0, '系统控制器\n定时/联动/监测', fontsize=9)

    # 分区层
    zone_y = 0.6
    draw_box(ax, 0.5, zone_y, 2.0, 1.3, '分区 A\n吸顶喇叭 × N', fontsize=9)
    draw_box(ax, 2.9, zone_y, 2.0, 1.3, '分区 B\n壁挂音箱 × N', fontsize=9)
    draw_box(ax, 5.3, zone_y, 2.0, 1.3, '分区 C\n草坪音箱 × N', fontsize=9)
    draw_box(ax, 7.7, zone_y, 2.0, 1.3, '分区 D\n号角扬声器\n(室外/大空间)', fontsize=9)
    draw_box(ax, 10.1, zone_y, 1.7, 1.3, '寻呼话筒\n(就地呼叫)', fontsize=9)

    # 音源 → 主机（下行）
    arrow(ax, 1.4, 6.6, 2.1, 5.4, C_MAIN, label='音频输入')
    arrow(ax, 3.5, 6.6, 5.0, 5.4, C_MAIN)
    arrow(ax, 5.6, 6.6, 5.5, 5.4, C_MAIN, label='干接点\n触发', label_offset=(-0.1, 0.05))
    arrow(ax, 7.7, 6.6, 5.8, 5.4, C_MAIN)
    arrow(ax, 10.1, 6.6, 10.5, 5.4, C_MAIN, label='RS232/\nTCP/IP', label_offset=(0.3, 0))

    # 主机内部链路
    arrow(ax, 3.2, 4.4, 3.8, 4.4, C_MAIN)  # 前置→矩阵
    arrow(ax, 6.2, 4.4, 6.8, 4.4, C_MAIN)  # 矩阵→功放
    arrow(ax, 10.5, 4.4, 9.0, 4.4, C_OUT, 'dashed', label='控制信号', label_pos=0.5)
    arrow(ax, 5.0, 4.4, 5.0, 4.0, C_OUT, 'dashed')  # 矩阵→控制器（垂直向下一小段示意，再水平）
    # 控制器双向到矩阵
    arrow_bidir(ax, 6.2, 4.1, 6.2, 3.9, C_OUT, 'dashed')

    # 功放 → 分区
    pw_y = 4.2
    # 功放输出到底部分区
    for i, x_start in enumerate([1.5, 3.9, 6.3, 8.7]):
        arrow(ax, 7.9 - i*0.3, 4.0, x_start + 1.0, 1.9, C_MAIN, label=f'100V\n定压线' if i==0 else '',
              label_offset=(0.2, 0.3) if i==0 else (0, 0))

    # 控制器 → 分区（监测/状态回采）
    arrow(ax, 10.5, 3.7, 11.0, 1.9, C_OUT, 'dashed', label='状态\n回采', label_offset=(0.2, 0))

    # 消防联动 应急
    arrow(ax, 5.6, 6.6, 5.6, 5.6, C_ERR, 'dashed', label='消防强切\n(最高优先级)', label_offset=(0.7, -0.2))

    draw_legend(ax, y=0.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'arch-system.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ arch-system.png')


# ============================================================
# 图2：广播信号处理链路（音源输入 → 分区输出 + 优先级判定）
# ============================================================
def draw_signal_flow():
    fig, ax = fig_setup('图2 广播信号处理链路与优先级判定（示意）', xlim=(0, 12), ylim=(0, 8.5))

    # 左侧多音源输入
    src_y_list = [7.2, 6.0, 4.8, 3.6]
    src_labels = ['业务广播\n(话筒/寻呼)', '背景音\n(音乐/通知)', '应急广播\n(消防联动)', '紧急寻呼\n(电话/终端)']
    src_colors = [C_MAIN, C_MAIN, C_ERR, C_MAIN]

    for i, (y, label, c) in enumerate(zip(src_y_list, src_labels, src_colors)):
        draw_box(ax, 0.3, y, 2.2, 0.7, label, fontsize=9)
        arrow(ax, 2.5, y + 0.35, 4.2, y + 0.35, c, 'solid' if c != C_ERR else 'dashed')

    # 优先级判定菱形
    draw_diamond(ax, 4.2, 4.8, 1.8, 1.4, '优先级\n判定', fontsize=9)

    # 判定输出
    arrow(ax, 6.0, 5.5, 7.2, 5.5, C_MAIN, 'solid', label='当前音源', label_offset=(0, 0.08))

    # 音频处理模块
    draw_box(ax, 7.2, 5.2, 2.0, 0.8, '前置放大\n/ 均衡', fontsize=9)
    arrow(ax, 9.2, 5.6, 9.8, 5.6, C_MAIN)

    draw_box(ax, 9.8, 5.2, 1.8, 0.8, 'A/D 采样\n数字处理', fontsize=9)
    arrow(ax, 10.7, 5.2, 10.7, 4.2, C_MAIN)

    # 分区路由矩阵
    draw_box(ax, 7.5, 3.2, 4.0, 1.0, '数字音频矩阵 / 分区路由', fontsize=10, fontweight='bold')

    arrow(ax, 10.7, 4.2, 10.7, 4.2, C_MAIN)  # 已连
    # 从A/D到矩阵
    arrow(ax, 10.7, 5.2, 10.7, 4.2, C_MAIN)

    # 定时/联动控制输入
    draw_box(ax, 4.8, 3.3, 1.8, 0.8, '定时任务\n/ 联动规则', fontsize=9)
    arrow(ax, 6.6, 3.7, 7.5, 3.7, C_OUT, 'dashed', label='调度指令', label_offset=(0, 0.08))

    # 功放级
    draw_box(ax, 7.5, 1.8, 4.0, 0.9, '功率放大 (D类)  定压输出 100V/70V', fontsize=9, fontweight='bold')
    arrow(ax, 9.5, 3.2, 9.5, 2.7, C_MAIN, label='音频信号', label_offset=(0.4, 0))

    # 分区输出
    zones = ['分区1\n办公区', '分区2\n走廊', '分区3\n大堂', '分区4\n地下车库']
    for i, z in enumerate(zones):
        x = 1.0 + i * 2.7
        draw_box(ax, x, 0.4, 2.2, 0.9, z, fontsize=8)
        # 从功放到底部分区，用三段折线（跨层）
        # 功放底 → 垂直降到走廊 → 水平 → 垂直到分区顶
        pw_bottom_x = 7.7 + i * 1.1
        mid_y = 1.4
        # 垂直段
        arrow(ax, pw_bottom_x, 1.8, pw_bottom_x, mid_y, C_MAIN)
        # 水平段
        ax.plot([pw_bottom_x, x + 1.1], [mid_y, mid_y], color=C_MAIN, linewidth=1.8, zorder=3)
        # 垂直段（到分区顶）
        arrow(ax, x + 1.1, mid_y, x + 1.1, 1.3, C_MAIN)

    # 优先级抢占反馈
    arrow(ax, 6.0, 4.8, 2.5, 4.8, C_ERR, 'dashed', label='低优先级被打断', label_pos=0.5, label_offset=(0, -0.15))

    draw_legend(ax, y=0.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-signal.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-signal.png')


# ============================================================
# 图3：消防应急广播强切流程（状态机式）
# ============================================================
def draw_emergency_flow():
    fig, ax = fig_setup('图3 消防应急广播强切流程（示意）', xlim=(0, 12), ylim=(0, 8))

    # 起点
    draw_box(ax, 0.5, 6.8, 2.0, 0.8, '消防主机报警信号', fontsize=9)
    arrow(ax, 2.5, 7.2, 3.5, 7.2, C_ERR, 'dashed', label='干接点 / RS232')

    # 第一步：信号接收与解析
    draw_box(ax, 3.5, 6.8, 2.2, 0.8, 'PA 主机\n消防信号接收', fontsize=9)
    arrow(ax, 5.7, 7.2, 6.5, 7.2, C_MAIN)

    # 判定：是否有效报警
    draw_diamond(ax, 6.5, 6.6, 1.8, 1.2, '有效\n报警？', fontsize=9)

    # 否 → 日志记录（回流）
    arrow(ax, 7.4, 6.6, 9.0, 6.6, C_ERR, 'dashed', label='否', label_offset=(0, 0.08))
    draw_box(ax, 9.0, 6.8, 2.2, 0.8, '记录日志 / 不动作', fontsize=9)

    # 是 → 向下到应急音源切换
    arrow(ax, 7.4, 6.0, 7.4, 5.2, C_MAIN, 'solid', label='是', label_offset=(-0.15, 0))

    draw_box(ax, 5.5, 4.4, 3.8, 0.9, '强制切换至应急音源（最高优先级）', fontsize=9, fontweight='bold', fill='#ffebee', edge='#e74c3c')
    arrow(ax, 7.4, 4.4, 7.4, 4.4, C_MAIN)  # already

    # 分区判定
    draw_diamond(ax, 5.5, 3.0, 2.0, 1.1, '按报警区域\n选择分区？', fontsize=9)
    arrow(ax, 7.4, 4.4, 6.5, 4.1, C_MAIN, label='', label_pos=0)

    # 是 → 对应分区广播
    arrow(ax, 5.5, 3.0, 3.0, 3.0, C_MAIN, 'solid', label='是', label_offset=(0, 0.08))
    draw_box(ax, 0.5, 2.6, 2.5, 0.8, '对应报警分区\n播放疏散语音', fontsize=9)
    arrow(ax, 3.0, 2.6, 3.0, 1.5, C_MAIN)
    arrow(ax, 3.0, 1.5, 9.5, 1.5, C_OUT, 'dashed')  # 水平走到底

    # 否 → 全楼广播
    arrow(ax, 7.5, 3.0, 9.5, 3.0, C_ERR, 'dashed', label='否 / 全楼', label_offset=(0, 0.08))
    draw_box(ax, 9.5, 2.6, 2.0, 0.8, '全楼应急广播', fontsize=9)
    arrow(ax, 10.5, 2.6, 10.5, 1.5, C_ERR, 'dashed')

    # 终点
    draw_box(ax, 8.5, 0.5, 3.0, 0.9, '疏散引导 + 状态回传消防主机', fontsize=9, fontweight='bold', fill='#e8f5e9', edge='#2ecc71')

    draw_legend(ax, y=0.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-emergency.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-emergency.png')


if __name__ == '__main__':
    draw_arch_system()
    draw_signal_flow()
    draw_emergency_flow()
    print('\n全部架构图生成完成')
