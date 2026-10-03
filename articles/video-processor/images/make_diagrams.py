# -*- coding: utf-8 -*-
"""
视频处理器架构图与流程图生成脚本
遵循链路绘制规范：正交分支、双色线型编码、双向箭头可见、无悬空箭头
图例：主流程=绿实线、输出/结果=蓝虚线、异常/冗余=红虚线
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
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


def draw_box(ax, x, y, w, h, text, fill=C_FILL, edge=C_BOX, fontsize=10, fontweight='normal'):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=1.5, edgecolor=edge, facecolor=fill, zorder=2)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, color=C_TITLE, zorder=3)


def draw_diamond(ax, x, y, w, h, text, fill='#fff3cd', edge='#d4a017', fontsize=9):
    pts = [(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)]
    poly = Polygon(pts, closed=True, facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=2)
    ax.add_patch(poly)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, color=C_TITLE, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=C_MAIN, style='solid', label=None,
          label_pos=0.5, label_offset=(0, 0.05)):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=1.8, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(lx, ly, label, ha='center', va='bottom', fontsize=8, color=color, zorder=5,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


def arrow_bidir(ax, x1, y1, x2, y2, color=C_MAIN, style='solid'):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='<->,head_width=0.08,head_length=0.12',
                        color=color, linewidth=1.8, linestyle=ls,
                        mutation_scale=12, zorder=4)
    ax.add_patch(a)


def line(ax, xs, ys, color=C_MAIN, style='solid'):
    ls = '-' if style == 'solid' else ('--' if style == 'dashed' else ':')
    ax.plot(xs, ys, color=color, linewidth=1.8, linestyle=ls, zorder=3,
            solid_capstyle='round')


def draw_legend(ax, y=0.35, x_start=0.4, spacing=2.9):
    items = [
        (C_MAIN, '-', '主流程 / 图像链路'),
        (C_OUT, '--', '控制下行 / 状态回传'),
        (C_ERR, '--', '冗余 / 备份 / 异常'),
    ]
    for i, (c, ls, text) in enumerate(items):
        x = x_start + i * spacing
        ax.plot([x, x + 0.35], [y, y], color=c, linestyle=ls, linewidth=2, zorder=5)
        ax.text(x + 0.5, y, text, ha='left', va='center', fontsize=8, color=C_TITLE, zorder=5)


def fig_setup(title, xlim=(0, 10), ylim=(0, 8)):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', color=C_TITLE, pad=15)
    return fig, ax


# ============================================================
# 图1：视频处理器在显示系统中的分层架构
# ============================================================
def draw_arch_system():
    fig, ax = fig_setup('图1 视频处理器在显示系统中的分层架构（示意）', xlim=(0, 12), ylim=(0, 10.6))

    ax.add_patch(mpatches.Rectangle((0.2, 8.3), 11.6, 1.75, facecolor='#e8f5e9',
                                    edgecolor='#a5d6a7', linewidth=1, zorder=0))
    ax.text(11.65, 9.88, '信号源层', fontsize=11, fontweight='bold', color='#2e7d32',
            ha='right', va='center', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 5.7), 11.6, 2.4, facecolor='#e3f2fd',
                                    edgecolor='#90caf9', linewidth=1.5, zorder=0))
    ax.text(11.65, 7.98, '视频处理器（接入与处理核心）', fontsize=11, fontweight='bold',
            color='#1565c0', ha='right', va='center', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 3.8), 11.6, 1.7, facecolor='#fff3e0',
                                    edgecolor='#ffcc80', linewidth=1, zorder=0))
    ax.text(11.65, 5.40, '发送与分发层', fontsize=11, fontweight='bold', color='#e65100',
            ha='right', va='center', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 2.1), 11.6, 1.5, facecolor='#f3e5f5',
                                    edgecolor='#ce93d8', linewidth=1, zorder=0))
    ax.text(11.65, 3.50, '显示终端层', fontsize=11, fontweight='bold', color='#6a1b9a',
            ha='right', va='center', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 0.6), 11.6, 1.35, facecolor='#eceff1',
                                    edgecolor='#b0bec5', linewidth=1, zorder=0))
    ax.text(11.65, 1.88, '管控与运维层', fontsize=11, fontweight='bold', color='#455a64',
            ha='right', va='center', zorder=1)

    # 信号源层
    y = 8.6
    draw_box(ax, 0.5, y, 1.7, 1.1, '摄像机 / IPC\n(网络码流)', fontsize=9)
    draw_box(ax, 2.5, y, 2.0, 1.1, 'PC / 工作站\n(HDMI / DP)', fontsize=9)
    draw_box(ax, 4.8, y, 2.0, 1.1, '播控 / 矩阵\n(SDI / DVI)', fontsize=9)
    draw_box(ax, 7.1, y, 1.8, 1.1, '视频会议\n终端', fontsize=9)
    draw_box(ax, 9.2, y, 2.2, 1.1, '第三方平台 /\n解码上报流', fontsize=9)

    # 处理器内部
    draw_box(ax, 0.6, 6.0, 2.6, 1.6, '输入采集与解码\nHDMI/DP/SDI/网流', fontsize=9)
    draw_box(ax, 3.5, 6.0, 2.9, 1.6, '图像处理引擎\n缩放/去隔行/降噪/色彩',
             fontsize=9, fontweight='bold', fill='#e8f5e9', edge='#2ecc71')
    draw_box(ax, 6.7, 6.0, 2.6, 1.6, '开窗与图层管理\n漫游/叠加/透明度', fontsize=9)
    draw_box(ax, 9.6, 6.0, 1.9, 1.6, '同步与帧率\nGenlock/VSync', fontsize=9)

    # 发送与分发层
    draw_box(ax, 0.6, 4.0, 2.6, 1.2, '输出板卡 / 网口组\nGbE / 10GbE', fontsize=9)
    draw_box(ax, 3.5, 4.0, 2.6, 1.2, '发送卡 / 光电转换\n多模 / 单模', fontsize=9)
    draw_box(ax, 6.5, 4.0, 2.2, 1.2, '网线 / 光纤\n传输链路', fontsize=9)
    draw_box(ax, 9.0, 4.0, 2.4, 1.2, '环备 / 双链路\n冗余通道', fontsize=9,
             fill='#ffebee', edge='#e74c3c')

    # 显示终端层
    draw_box(ax, 0.6, 2.3, 2.6, 1.1, 'LED 箱体 / 接收卡', fontsize=9, fontweight='bold')
    draw_box(ax, 3.5, 2.3, 2.4, 1.1, 'LCD 拼接单元', fontsize=9)
    draw_box(ax, 6.3, 2.3, 2.2, 1.1, '投影 / 监视器', fontsize=9)
    draw_box(ax, 9.0, 2.3, 2.4, 1.1, '坐席预览屏', fontsize=9)

    # 管控层
    draw_box(ax, 0.6, 0.8, 3.0, 1.0, '可视化管控平台\n预案/调度/权限', fontsize=9, fontweight='bold')
    draw_box(ax, 3.9, 0.8, 2.4, 1.0, '中控系统 / 触摸屏', fontsize=9)
    draw_box(ax, 6.6, 0.8, 2.2, 1.0, 'KVM / 坐席协作', fontsize=9)
    draw_box(ax, 9.1, 0.8, 2.4, 1.0, '运维监测 / 日志告警', fontsize=9)

    # 信号源 → 输入采集（扇形汇聚）
    for cx in [1.35, 3.5, 5.8, 8.0, 10.3]:
        arrow(ax, cx, 8.6, 1.9, 7.6, C_MAIN,
              label='HDMI/SDI/RTSP' if cx == 1.35 else '')

    # 处理器内部横向
    arrow(ax, 3.2, 6.8, 3.5, 6.8, C_MAIN)
    arrow(ax, 6.4, 6.8, 6.7, 6.8, C_MAIN)
    arrow_bidir(ax, 9.3, 6.8, 9.6, 6.8, C_OUT, 'dashed')

    # 处理器 → 发送层
    arrow(ax, 1.9, 6.0, 1.9, 5.2, C_MAIN, label='处理后像素流', label_offset=(0.95, 0))
    arrow(ax, 4.95, 6.0, 4.8, 5.2, C_OUT, 'dashed')
    arrow(ax, 8.0, 6.0, 7.6, 5.2, C_OUT, 'dashed')

    # 发送层 → 终端层
    for cx, tx in [(1.9, 1.9), (4.8, 4.7), (7.6, 7.4), (10.2, 10.2)]:
        arrow(ax, cx, 4.0, tx, 3.4, C_MAIN)

    # 管控层 ↔ 处理器层（左侧走线走廊）
    line(ax, [0.6, 0.34], [1.3, 1.3], C_OUT, 'dashed')
    line(ax, [0.34, 0.34], [1.3, 6.6], C_OUT, 'dashed')
    line(ax, [0.34, 0.6], [6.6, 6.6], C_OUT, 'dashed')
    ax.annotate('', xy=(0.34, 6.6), xytext=(0.34, 1.3),
                arrowprops=dict(arrowstyle='<->', color=C_OUT, linestyle='--',
                                linewidth=1.8, mutation_scale=12), zorder=4)
    ax.text(0.34, 3.9, 'TCP/IP / RS232', rotation=90, ha='center', va='center',
            fontsize=8, color=C_OUT, zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))

    draw_legend(ax, y=0.2, x_start=0.4, spacing=3.0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'arch-system.png'), dpi=150,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ arch-system.png')


# ============================================================
# 图2：单路信号从接入到灯珠点亮的完整处理链路
# ============================================================
def draw_signal_chain():
    fig, ax = fig_setup('图3 单路信号从接入到灯珠点亮的完整处理链路（示意）',
                        xlim=(0, 13), ylim=(0, 10.4))

    ax.text(6.5, 9.6, '端到端处理延迟典型 2~4 帧（60Hz 下约 33~67ms，工程基准）',
            ha='center', va='center', fontsize=10, color=C_TITLE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fff8e1', ec='#d4a017', alpha=0.95), zorder=5)

    xs = [0.4, 3.3, 6.2, 9.1]
    w, h = 2.6, 1.1

    # 第一行（左 → 右）
    row_a = [
        '信号接入\nHDMI2.0 / DP1.4 / SDI / 网流',
        'EDID 与时序识别\n分辨率 / 帧率 / 色深',
        '解码与色空间转换\nYUV→RGB / HDR 映射',
        '去隔行与降噪\nI→P / 3D 降噪',
    ]
    for i, t in enumerate(row_a):
        draw_box(ax, xs[i], 7.6, w, h, t, fontsize=8.5,
                 fontweight='bold' if i == 0 else 'normal')
    for i in range(3):
        arrow(ax, xs[i] + w, 8.15, xs[i + 1], 8.15, C_MAIN)

    # 蛇形过渡
    arrow(ax, 10.4, 7.6, 10.4, 6.5, C_MAIN)

    # 第二行（右 → 左）
    row_b = [
        '缩放与画质增强\n多相滤波 / 锐化',
        '图层开窗与裁剪\n位置 / 大小 / 叠加',
        '帧率与同步对齐\n帧缓存 / VSync',
        '逐点校正与 Gamma\n亮度色度一致性',
    ]
    for i, t in enumerate(row_b):
        draw_box(ax, xs[3 - i], 5.4, w, h, t, fontsize=8.5)
    for i in range(3):
        x_r, x_l = xs[3 - i], xs[2 - i]
        arrow(ax, x_r, 5.95, x_l + w, 5.95, C_MAIN)

    # 蛇形过渡
    arrow(ax, 1.7, 5.4, 1.7, 4.3, C_MAIN)

    # 第三行（左 → 右）
    row_c = [
        '位深抖动处理\n10/12bit → 面板位深',
        '低灰校正与刷新率\nPWM 调制 / 消影',
        '数据重组与打包\n发送卡协议帧',
        '网口 / 光纤输出\nGbE / 10GbE / 光口',
    ]
    for i, t in enumerate(row_c):
        draw_box(ax, xs[i], 3.2, w, h, t, fontsize=8.5)
    for i in range(3):
        arrow(ax, xs[i] + w, 3.75, xs[i + 1], 3.75, C_MAIN)

    # 输出 → 终端
    arrow(ax, 10.4, 3.2, 10.4, 2.1, C_OUT, 'dashed')
    draw_box(ax, 9.1, 1.0, 2.6, 1.1, '接收卡 → 灯珠点亮',
             fontsize=9, fontweight='bold', fill='#e8f5e9', edge='#2ecc71')

    # 状态回传
    arrow(ax, 9.1, 1.55, 6.7, 1.55, C_OUT, 'dashed', label='状态回传', label_offset=(0, 0.12))
    draw_box(ax, 3.1, 1.0, 3.6, 1.1, '箱体状态回传\n温度 / 电压 / 链路误码', fontsize=9)

    draw_legend(ax, y=0.25, x_start=0.4, spacing=3.0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-signal.png'), dpi=150,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-signal.png')


# ============================================================
# 图3：带载能力与拼接配置核算流程
# ============================================================
def draw_sizing_flow():
    fig, ax = fig_setup('图2 带载能力与拼接配置核算流程（示意）', xlim=(0, 12), ylim=(0, 10.4))

    ax.text(6.0, 9.6, 'N = ceil(P ÷ Pmax，向上取整)    网口数 = ceil(P ÷ Pport)    P = 屏体宽(点) × 屏体高(点)',
            ha='center', va='center', fontsize=10, color=C_TITLE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fff8e1', ec='#d4a017', alpha=0.95), zorder=5)

    # ---- 第一阶段：算出台数 ----
    draw_box(ax, 0.5, 8.0, 2.2, 1.2, '屏体分辨率\nW × H（点）', fontsize=9)
    draw_box(ax, 3.2, 8.0, 2.2, 1.2, '总像素 P\n= W × H', fontsize=9)
    draw_box(ax, 5.9, 8.0, 2.6, 1.2, '单台带载上限 Pmax\n（查设备规格书）', fontsize=9)
    draw_box(ax, 9.0, 8.0, 2.6, 1.2, '处理器台数 N\n（向上取整）', fontsize=10, fontweight='bold',
             fill='#e8f5e9', edge='#2ecc71')
    for x1, x2 in [(2.7, 3.2), (5.4, 5.9), (8.5, 9.0)]:
        arrow(ax, x1, 8.6, x2, 8.6, C_MAIN)

    # ---- 第二阶段：带载与网口复核（判定菱形） ----
    arrow(ax, 10.3, 8.0, 10.3, 7.3, C_MAIN)
    draw_diamond(ax, 8.9, 6.0, 2.8, 1.3, '带载 / 网口\n是否超标？', fontsize=9)

    # 是 → 拆分拼接域（红色，并回流重新核算）
    arrow(ax, 8.9, 6.65, 7.4, 6.65, C_ERR, 'dashed', label='是（超标）',
          label_pos=0.45, label_offset=(0, 0.1))
    draw_box(ax, 4.2, 6.1, 3.2, 1.1, '拆分拼接域 /\n提升设备档位', fontsize=9,
             fill='#ffebee', edge='#e74c3c')
    arrow(ax, 5.8, 7.2, 5.8, 7.6, C_ERR, 'dashed')
    ax.text(5.9, 7.72, '回到第一步重新核算', ha='left', va='center', fontsize=8,
            color=C_ERR, zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))

    # 否 → 汇流到三项复核
    line(ax, [10.3, 10.3], [6.0, 5.75], C_MAIN)
    line(ax, [2.2, 10.3], [5.75, 5.75], C_MAIN)
    ax.text(10.45, 5.88, '否', ha='left', va='center', fontsize=8.5, color=C_MAIN,
            zorder=5, bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.9))

    draw_box(ax, 0.5, 3.8, 3.4, 1.6, '刷新率与灰度复核\n≥1920Hz / ≥14bit（工程基准）', fontsize=9)
    draw_box(ax, 4.3, 3.8, 3.4, 1.6, '输入路数与开窗数复核\n处理引擎档位匹配', fontsize=9)
    draw_box(ax, 8.1, 3.8, 3.5, 1.6, '冗余与链路复核\n主控 1+1 / 双光链路', fontsize=9)
    for cx in [2.2, 6.0, 9.85]:
        arrow(ax, cx, 5.75, cx, 5.4, C_MAIN)

    # ---- 第三阶段：汇入配置清单 ----
    draw_box(ax, 1.4, 1.2, 9.2, 1.3,
             '形成配置清单：处理器台数 / 板卡规格 / 网口数 / 光模块 / 光纤芯数 / 备件',
             fontsize=10, fontweight='bold', fill='#e8f5e9', edge='#2ecc71')
    line(ax, [2.2, 2.2], [3.8, 3.0], C_MAIN)
    line(ax, [2.2, 9.85], [3.0, 3.0], C_MAIN)
    line(ax, [9.85, 9.85], [3.8, 3.0], C_MAIN)
    arrow(ax, 6.0, 3.8, 6.0, 2.5, C_MAIN)

    draw_legend(ax, y=0.3, x_start=0.4, spacing=3.0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-sizing.png'), dpi=150,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-sizing.png')


# ============================================================
# 图4：多机级联与主备冗余拓扑
# ============================================================
def draw_redundancy_topology():
    fig, ax = fig_setup('图4 指挥中心多机级联与主备冗余拓扑（示意）', xlim=(0, 13.2), ylim=(0, 9.2))

    # 信号源列
    srcs = ['摄像机 / IPC', 'PC / 工作站', '会议终端', '播控 / 平台']
    for i, t in enumerate(srcs):
        draw_box(ax, 0.3, 7.0 - i * 1.4, 2.2, 1.0, t, fontsize=9)

    # 主控 / 备控
    draw_box(ax, 3.4, 4.6, 3.2, 2.4, '主控处理器 A\n开窗调度 / 输出映射',
             fontsize=10, fontweight='bold', fill='#e8f5e9', edge='#2ecc71')
    draw_box(ax, 3.4, 1.4, 3.2, 2.2, '备控处理器 B\n热备 1+1', fontsize=10,
             fill='#ffebee', edge='#e74c3c')
    arrow_bidir(ax, 5.0, 4.6, 5.0, 3.6, C_ERR, 'dashed')
    ax.text(5.15, 4.1, '心跳 / 状态同步', ha='left', va='center', fontsize=8,
            color=C_ERR, zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))

    # 信号源 → 主控
    for i in range(4):
        arrow(ax, 2.5, 7.5 - i * 1.4, 3.4, 5.8, C_MAIN)

    # 核心交换机 / 传输链路
    draw_box(ax, 7.6, 4.8, 2.0, 2.0, '核心交换机\n组播 / 主备', fontsize=9)
    draw_box(ax, 7.6, 2.4, 2.0, 1.8, '网线 / 光纤\n传输链路', fontsize=9)
    arrow(ax, 6.6, 5.8, 7.6, 5.8, C_MAIN)
    arrow(ax, 8.6, 4.8, 8.6, 4.2, C_MAIN)
    arrow(ax, 6.6, 2.5, 7.6, 2.5, C_ERR, 'dashed', label='主备切换', label_offset=(0, 0.1))

    # 管控平台
    draw_box(ax, 7.6, 7.4, 2.0, 1.2, '可视化管控平台\n预案 / 坐席 / 权限', fontsize=8.5,
             fontweight='bold')
    line(ax, [7.6, 7.05], [8.0, 8.0], C_OUT, 'dashed')
    line(ax, [7.05, 7.05], [8.0, 7.0], C_OUT, 'dashed')
    arrow(ax, 7.05, 7.0, 6.6, 7.0, C_OUT, 'dashed')

    # 大屏箱体阵列（3×3）
    ax.text(11.5, 7.6, 'LED 大屏（接收卡阵列）', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_TITLE, zorder=5)
    gx = [10.3, 11.1, 11.9]
    gy = [3.1, 4.4, 5.7]
    for r in range(3):
        for c in range(3):
            draw_box(ax, gx[c], gy[r], 0.78, 1.28, '', fill='#f8f9fa', edge='#90a4ae')
    ax.add_patch(mpatches.Rectangle((10.15, 2.95), 2.9, 4.2, facecolor='none',
                                    edgecolor='#7f8c8d', linewidth=1.5, zorder=3))
    arrow(ax, 9.6, 3.3, 10.15, 3.3, C_MAIN)

    draw_legend(ax, y=0.5, x_start=0.4, spacing=3.0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'scene-topology.png'), dpi=150,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ scene-topology.png')


if __name__ == '__main__':
    draw_arch_system()
    draw_signal_chain()
    draw_sizing_flow()
    draw_redundancy_topology()
    print('\n全部架构图生成完成')
