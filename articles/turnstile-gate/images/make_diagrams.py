# -*- coding: utf-8 -*-
"""
人行通道闸（摆闸/翼闸/三辊闸）架构图与流程图生成脚本
遵循链路绘制规范：正交分支、双色线型编码、双向箭头可见、无悬空箭头
图例：主流程=绿实线、输出/结果=蓝虚线、异常/回流=红虚线
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


def draw_legend(ax, y=0.35):
    items = [
        (C_MAIN, '-', '主流程 / 通行链路'),
        (C_OUT, '--', '控制下行 / 状态回传'),
        (C_ERR, '--', '异常 / 报警 / 应急'),
    ]
    x_start = 0.4
    spacing = 2.4
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
# 图1：通道闸系统整体架构（识读层 → 控制层 → 执行层 → 平台层）
# ============================================================
def draw_arch_system():
    fig, ax = fig_setup('图1 人行通道闸系统整体架构（示意）', xlim=(0, 12), ylim=(0, 9))

    ax.add_patch(mpatches.Rectangle((0.2, 7.0), 11.6, 1.7, facecolor='#e8f5e9',
                                    edgecolor='#a5d6a7', linewidth=1, zorder=0))
    ax.text(0.4, 8.5, '凭证识读层', fontsize=11, fontweight='bold', color='#2e7d32', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 4.4), 11.6, 2.4, facecolor='#e3f2fd',
                                    edgecolor='#90caf9', linewidth=1, zorder=0))
    ax.text(0.4, 6.6, '闸机控制层（本地自治）', fontsize=11, fontweight='bold', color='#1565c0', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 1.9), 11.6, 2.3, facecolor='#fff3e0',
                                    edgecolor='#ffcc80', linewidth=1, zorder=0))
    ax.text(0.4, 4.0, '机械执行层', fontsize=11, fontweight='bold', color='#e65100', zorder=1)

    ax.add_patch(mpatches.Rectangle((0.2, 0.3), 11.6, 1.4, facecolor='#f3e5f5',
                                    edgecolor='#ce93d8', linewidth=1, zorder=0))
    ax.text(0.4, 1.5, '平台 / 系统层', fontsize=11, fontweight='bold', color='#6a1b9a', zorder=1)

    # 识读层
    y = 7.5
    draw_box(ax, 0.5, y, 1.8, 0.9, '人脸识别\n终端', fontsize=9)
    draw_box(ax, 2.5, y, 1.8, 0.9, '二维码 /\n条码阅读器', fontsize=9)
    draw_box(ax, 4.5, y, 1.8, 0.9, 'IC / ID 卡\n读卡器', fontsize=9)
    draw_box(ax, 6.5, y, 1.8, 0.9, '身份证 /\n健康码核验', fontsize=9)
    draw_box(ax, 8.5, y, 1.8, 0.9, '指纹 / 掌静脉\n生物识别', fontsize=9)
    draw_box(ax, 10.5, y, 1.1, 0.9, '遥控器\n(旁路)', fontsize=8)

    # 控制层
    draw_box(ax, 0.8, 5.0, 2.4, 1.1, '闸机主控板\n(MCU / ARM)', fontsize=9, fontweight='bold')
    draw_box(ax, 3.6, 5.0, 2.4, 1.1, '通行逻辑判定\n权限/防尾随/防反潜', fontsize=9)
    draw_box(ax, 6.4, 5.0, 2.2, 1.1, '红外光幕\n(4~16 对)', fontsize=9)
    draw_box(ax, 8.9, 5.0, 2.7, 1.1, '状态指示 / 语音\nLED 灯带 / 蜂鸣', fontsize=9)

    # 执行层
    draw_box(ax, 0.8, 2.3, 2.6, 1.2, '电机 + 减速机构\n(无刷 / 伺服)', fontsize=9)
    draw_box(ax, 3.7, 2.3, 2.4, 1.2, '离合器 / 电磁抱闸\n断电自动释放', fontsize=9)
    draw_box(ax, 6.4, 2.3, 2.4, 1.2, '拦阻体\n摆臂 / 翼板 / 辊杆', fontsize=9, fontweight='bold')
    draw_box(ax, 9.1, 2.3, 2.5, 1.2, '防夹保护\n力矩 + 红外双保险', fontsize=9)

    # 平台层
    draw_box(ax, 0.8, 0.6, 2.6, 0.9, '门禁 / 通行管理平台', fontsize=9, fontweight='bold')
    draw_box(ax, 3.7, 0.6, 2.4, 0.9, '访客 / 考勤系统', fontsize=9)
    draw_box(ax, 6.4, 0.6, 2.4, 0.9, '消防报警主机\n(强切信号)', fontsize=9, fill='#ffebee', edge='#e74c3c')
    draw_box(ax, 9.1, 0.6, 2.5, 0.9, '视频监控 / 客流统计', fontsize=9)

    # 识读 → 主控板（下行，扇形汇聚）
    for x in [1.4, 3.4, 5.4, 7.4, 9.4]:
        arrow(ax, x, 7.5, 2.0, 6.1, C_MAIN, label='韦根26/34\nRS485' if x == 1.4 else '')
    # 遥控器 → 通行逻辑判定（旁路开闸）
    arrow(ax, 11.0, 7.5, 4.8, 6.1, C_MAIN)

    # 控制层内部
    arrow(ax, 3.2, 5.55, 3.6, 5.55, C_MAIN)
    arrow_bidir(ax, 6.0, 5.55, 6.4, 5.55, C_OUT, 'dashed')
    arrow(ax, 2.0, 5.0, 2.1, 3.5, C_OUT, 'dashed', label='驱动指令')
    arrow(ax, 4.8, 5.0, 4.9, 3.5, C_OUT, 'dashed')
    arrow(ax, 9.2, 5.0, 10.3, 3.5, C_OUT, 'dashed')

    # 执行层内部
    arrow(ax, 3.4, 2.9, 3.7, 2.9, C_MAIN)
    arrow(ax, 6.1, 2.9, 6.4, 2.9, C_MAIN)
    arrow(ax, 8.8, 2.9, 9.1, 2.9, C_ERR, 'dashed', label='遇阻反馈', label_offset=(0.15, 0.75))

    # 主控板 ↔ 门禁平台（左侧走线走廊）
    line(ax, [0.8, 0.45], [5.5, 5.5], C_OUT, 'dashed')
    line(ax, [0.45, 0.8], [1.05, 1.05], C_OUT, 'dashed')
    ax.annotate('', xy=(0.45, 5.5), xytext=(0.45, 1.05),
                arrowprops=dict(arrowstyle='<->', color=C_OUT, linestyle='--',
                                linewidth=1.8, mutation_scale=12), zorder=4)
    ax.text(0.68, 3.3, 'TCP/IP', rotation=90, ha='center', va='center', fontsize=8,
            color=C_OUT, zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))

    # 消防主机 → 离合器（正交三段折线，走在空白走廊）
    line(ax, [7.6, 7.6], [1.5, 1.95], C_ERR, 'dashed')
    line(ax, [7.6, 4.9], [1.95, 1.95], C_ERR, 'dashed')
    arrow(ax, 4.9, 1.95, 4.9, 2.3, C_ERR, 'dashed')
    ax.text(6.25, 2.1, '消防强切（最高优先级）', ha='center', va='bottom', fontsize=8,
            color=C_ERR, zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))

    draw_legend(ax, y=0.35)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'arch-system.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ arch-system.png')


# ============================================================
# 图2：一次通行的完整判定链路（状态机式）
# ============================================================
def draw_pass_flow():
    fig, ax = fig_setup('图2 一次通行的判定链路与状态机（示意）', xlim=(0, 12), ylim=(0, 9))

    draw_box(ax, 0.4, 7.6, 2.2, 0.9, '人员进入\n识别区域', fontsize=9)
    arrow(ax, 2.6, 8.05, 3.6, 8.05, C_MAIN)
    draw_box(ax, 3.6, 7.6, 2.2, 0.9, '凭证识读\n(刷脸 / 刷卡 / 扫码)', fontsize=9)
    arrow(ax, 5.8, 8.05, 6.6, 8.05, C_MAIN)

    draw_diamond(ax, 6.6, 7.5, 1.9, 1.2, '权限\n有效？', fontsize=9)
    arrow(ax, 7.6, 7.5, 7.6, 6.3, C_MAIN, label='是', label_offset=(-0.2, 0))
    arrow(ax, 8.5, 8.1, 10.6, 8.1, C_ERR, 'dashed', label='否', label_offset=(0, 0.08))
    draw_box(ax, 10.6, 7.6, 1.3, 0.9, '拒绝\n声光提示', fontsize=8, fill='#ffebee', edge='#e74c3c')

    draw_box(ax, 5.6, 5.4, 3.8, 0.9, '开闸指令下发（机芯解锁 / 摆臂打开）', fontsize=9,
             fontweight='bold', fill='#e8f5e9', edge='#2ecc71')
    arrow(ax, 9.4, 5.85, 10.6, 5.85, C_OUT, 'dashed')
    draw_box(ax, 10.6, 5.4, 1.3, 0.9, 'LED\n变绿', fontsize=8)

    draw_box(ax, 5.6, 4.0, 3.8, 0.9, '光幕实时跟踪（人数 / 方向 / 位置）', fontsize=9)
    arrow(ax, 7.5, 5.4, 7.5, 4.9, C_MAIN)

    draw_diamond(ax, 5.6, 2.7, 2.0, 1.1, '尾随\n(两人)？', fontsize=9)
    arrow(ax, 7.5, 4.0, 6.6, 3.8, C_MAIN)

    # 尾随 → 报警（左）
    arrow(ax, 5.6, 3.25, 3.0, 3.25, C_ERR, 'dashed', label='是 → 报警', label_offset=(0, 0.1))
    draw_box(ax, 0.4, 2.8, 2.6, 0.9, '声光报警\n抓拍留证（可选）', fontsize=8,
             fill='#ffebee', edge='#e74c3c')

    # 尾随 → 正常通行（右下角折线）
    line(ax, [7.6, 8.0], [3.25, 3.25], C_MAIN)
    arrow(ax, 8.0, 3.25, 8.0, 1.9, C_MAIN)
    ax.text(8.18, 2.55, '否', ha='left', va='center', fontsize=8, color=C_MAIN, zorder=5)

    draw_diamond(ax, 6.0, 1.3, 2.0, 1.1, '通行\n完成？', fontsize=9)
    # 超时 / 反向 → 关闸
    arrow(ax, 6.0, 1.85, 4.4, 1.85, C_ERR, 'dashed', label='超时 / 反向 → 关闸', label_offset=(0, 0.1))
    draw_box(ax, 2.0, 1.4, 2.4, 0.9, '撤销授权\n自动关闸', fontsize=8)

    arrow(ax, 7.0, 1.3, 7.0, 1.0, C_MAIN, label='是', label_offset=(0.45, 0))
    draw_box(ax, 5.0, 0.2, 4.2, 0.8, '关闸 + 计数上报平台（通行记录闭环）', fontsize=9,
             fontweight='bold', fill='#e8f5e9', edge='#2ecc71')

    # 防反潜回状态回写
    draw_box(ax, 0.4, 0.2, 3.0, 0.8, '防反潜回（APB）状态回写', fontsize=8)
    arrow_bidir(ax, 3.4, 0.6, 5.0, 0.6, C_OUT, 'dashed')

    draw_legend(ax, y=6.75)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-pass.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-pass.png')


# ============================================================
# 图3：断电 / 消防应急放行流程
# ============================================================
def draw_emergency_flow():
    fig, ax = fig_setup('图3 断电与消防应急放行流程（示意）', xlim=(0, 12), ylim=(0, 8))

    draw_box(ax, 0.4, 6.6, 2.0, 0.9, '市电中断', fontsize=9)
    draw_box(ax, 0.4, 5.2, 2.0, 0.9, '消防报警信号', fontsize=9, fill='#ffebee', edge='#e74c3c')

    # 两个触发源汇聚到判定菱形左顶点
    arrow(ax, 2.4, 7.05, 3.7, 6.45, C_ERR, 'dashed')
    arrow(ax, 2.4, 5.65, 3.7, 6.05, C_ERR, 'dashed')

    draw_diamond(ax, 3.7, 5.6, 1.9, 1.3, '任一触发？', fontsize=9)
    arrow(ax, 5.6, 6.25, 6.8, 6.25, C_ERR, 'dashed', label='是', label_offset=(0, 0.08))

    draw_box(ax, 6.8, 5.8, 4.4, 0.9, '离合器释放 / 断电开闸（拦阻体自由通行）', fontsize=9,
             fontweight='bold', fill='#ffebee', edge='#e74c3c')
    arrow(ax, 9.0, 5.8, 9.0, 4.2, C_ERR, 'dashed')

    draw_diamond(ax, 6.8, 3.6, 2.2, 1.1, '配置 UPS\n常开保持？', fontsize=9)
    arrow(ax, 6.8, 4.15, 4.4, 4.15, C_MAIN, label='否', label_offset=(0, 0.08))
    draw_box(ax, 1.6, 3.7, 2.8, 0.9, '落杆 / 自由通行\n(纯机械常开)', fontsize=9)
    arrow(ax, 9.0, 4.15, 10.2, 4.15, C_MAIN, label='是', label_offset=(0, 0.08))
    draw_box(ax, 10.2, 3.7, 1.6, 0.9, '保持开闸\n+ 记录', fontsize=8)

    # 反馈回消防主机：走箱体上方的走廊
    line(ax, [3.0, 3.0], [3.7, 2.95], C_OUT, 'dashed')
    line(ax, [3.0, 9.0], [2.95, 2.95], C_OUT, 'dashed')
    arrow(ax, 9.0, 2.95, 9.0, 2.7, C_OUT, 'dashed')
    ax.text(6.0, 3.05, '联动状态反馈', ha='center', va='bottom', fontsize=8, color=C_OUT,
            zorder=5, bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))

    draw_box(ax, 6.8, 1.8, 4.4, 0.9, '消防联动反馈：状态回传消防主机', fontsize=9)
    draw_box(ax, 6.8, 0.4, 4.4, 0.9, '恢复供电 → 自检 → 复位到常闭待机', fontsize=9,
             fontweight='bold', fill='#e8f5e9', edge='#2ecc71')
    arrow(ax, 9.0, 1.8, 9.0, 1.3, C_MAIN)

    draw_legend(ax, y=0.9)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-emergency.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-emergency.png')


# ============================================================
# 图4：通道数量选型核算速查（流程式）
# ============================================================
def draw_sizing_flow():
    fig, ax = fig_setup('图4 通道数量与机型选型核算流程（示意）', xlim=(0, 12), ylim=(0, 8))

    draw_box(ax, 0.4, 6.6, 2.2, 0.9, '高峰小时\n人流量 Q', fontsize=9)
    arrow(ax, 2.6, 7.05, 3.5, 7.05, C_MAIN)
    draw_box(ax, 3.5, 6.6, 2.4, 0.9, '单机通行能力\nC（人 / 分钟）', fontsize=9)
    arrow(ax, 5.9, 7.05, 6.7, 7.05, C_MAIN)
    draw_box(ax, 6.7, 6.6, 2.6, 0.9, '利用率 η\n(0.6~0.8)', fontsize=9)
    arrow(ax, 9.3, 7.05, 10.0, 7.05, C_MAIN)
    draw_box(ax, 10.0, 6.6, 1.7, 0.9, '通道数 N', fontsize=9, fontweight='bold')

    ax.text(6.0, 5.85, 'N = Q ÷ (C × 60 × η)，向上取整；再按规范补 1 条无障碍宽通道',
            ha='center', va='center', fontsize=10, color=C_TITLE, zorder=5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fff8e1', ec='#d4a017', alpha=0.95))

    # 场景机型映射：总线式分支（杜绝悬空箭头）
    draw_box(ax, 0.3, 2.65, 2.6, 0.9, '按使用场景\n定机型', fontsize=9, fontweight='bold')
    arrow(ax, 2.9, 3.1, 3.5, 3.1, C_MAIN)

    line(ax, [3.5, 3.5], [1.15, 5.05], C_MAIN)

    branches = [
        (4.6, '户外 / 工地 / 景区\n人多 · 预算紧', '三辊闸', '#fff3e0'),
        (3.3, '写字楼大堂\n追求效率与形象', '翼闸 / 速通门', '#e3f2fd'),
        (2.0, '行李 / 轮椅 / 婴儿车\n需宽通道', '摆闸（宽通道）', '#e8f5e9'),
        (0.7, '无人值守 / 高安全\n防翻越', '全高转闸', '#f3e5f5'),
    ]
    for by, cond, model, color in branches:
        cy = by + 0.45
        arrow(ax, 3.5, cy, 4.0, cy, C_MAIN)
        draw_box(ax, 4.0, by, 3.2, 0.9, cond, fontsize=8, fill=color)
        arrow(ax, 7.2, cy, 8.6, cy, C_MAIN)
        draw_box(ax, 8.6, by, 3.0, 0.9, model, fontsize=10, fontweight='bold', fill=color)

    draw_legend(ax, y=0.35)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'flow-sizing.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('✓ flow-sizing.png')


if __name__ == '__main__':
    draw_arch_system()
    draw_pass_flow()
    draw_emergency_flow()
    draw_sizing_flow()
    print('\n全部架构图生成完成')
