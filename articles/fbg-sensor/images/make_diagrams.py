# -*- coding: utf-8 -*-
"""
FBG 光纤光栅传感器产品综述 - 架构图/原理图生成脚本
生成 3 张矢量框线示意图：
  1. arch-system.png - 系统三端架构图
  2. arch-principle.png - FBG 光栅原理与波长漂移
  3. arch-wdm.png - 波分复用串接原理

绘制规范：
- 正交分支、双色线型编码（主流程绿实线、输出青虚线、异常红虚线）
- 箭头无悬空、落点归位、标题避让、终点触边、线型一致
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 颜色定义
COLOR_SENSE = '#4CAF50'    # 传感端 - 绿色
COLOR_DEMOD = '#2196F3'    # 解调端 - 蓝色
COLOR_PLAT = '#9C27B0'     # 平台端 - 紫色
COLOR_MAIN = '#2E7D32'     # 主流程绿实线
COLOR_OUT = '#00BCD4'      # 输出青虚线
COLOR_ABN = '#F44336'      # 异常红虚线
COLOR_TEXT = '#212121'     # 正文文字
COLOR_BG = '#FAFAFA'       # 背景

def draw_rounded_box(ax, x, y, w, h, text, color='#2196F3', fontsize=11, text_color='white'):
    """绘制圆角矩形框"""
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         facecolor=color, edgecolor='#1565C0', linewidth=1.5,
                         alpha=0.9, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, fontweight='bold', zorder=4)

def draw_layer_box(ax, x, y, w, h, title, color='#E3F2FD'):
    """绘制层背景框"""
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor=color, edgecolor='#90CAF9', linewidth=1.2,
                         alpha=0.5, zorder=1)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 0.15, title, ha='center', va='top',
            fontsize=12, color='#1565C0', fontweight='bold', zorder=2)

def draw_arrow(ax, x1, y1, x2, y2, color='#2E7D32', style='->', lw=2, ls='-'):
    """绘制箭头"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style, color=color,
                            linewidth=lw, linestyle=ls,
                            mutation_scale=15, zorder=5)
    ax.add_patch(arrow)

def draw_label(ax, x, y, text, color='#212121', fontsize=9, bg=None, fontweight='normal'):
    """绘制标签"""
    if bg:
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
                color=color, fontweight=fontweight,
                bbox=dict(boxstyle='round,pad=0.2', facecolor=bg,
                          edgecolor='none', alpha=0.8), zorder=6)
    else:
        ax.text(x, y, text, ha='center', va='center',
                fontsize=fontsize, color=color, fontweight=fontweight, zorder=6)


# ============================================================
# 图1：系统三端架构图
# ============================================================
def draw_system_arch():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # 三层背景框 - 横向三列
    # 传感端
    draw_layer_box(ax, 0.3, 0.5, 3.4, 6.0, '传感端（无源）', color='#E8F5E9')
    # 解调端
    draw_layer_box(ax, 4.3, 0.5, 3.4, 6.0, '解调端', color='#E3F2FD')
    # 平台端
    draw_layer_box(ax, 8.3, 0.5, 3.4, 6.0, '管理端', color='#F3E5F5')

    # 传感端设备
    draw_rounded_box(ax, 0.8, 4.5, 2.4, 0.9, 'FBG 温度传感器', color='#4CAF50', fontsize=10)
    draw_rounded_box(ax, 0.8, 3.3, 2.4, 0.9, 'FBG 应变传感器', color='#4CAF50', fontsize=10)
    draw_rounded_box(ax, 0.8, 2.1, 2.4, 0.9, 'FBG 位移/索力传感器', color='#4CAF50', fontsize=10)

    # 光纤串接线
    ax.plot([2.0, 2.0], [4.5, 1.5], color='#FF9800', linewidth=2.5, linestyle='-', zorder=4)
    for y in [4.95, 3.75, 2.55]:
        ax.plot([1.7, 2.3], [y, y], color='#FF9800', linewidth=2.5, zorder=4)
    draw_label(ax, 2.6, 1.8, '单纤串接\n几十个测点', color='#E65100', fontsize=9, bg='#FFF3E0')

    # 解调端
    draw_rounded_box(ax, 4.8, 3.8, 2.4, 1.2, '光纤光栅解调仪', color='#2196F3', fontsize=11)
    draw_label(ax, 6.0, 3.2, '波长解析 → 物理量换算', color='#0D47A1', fontsize=9, bg='#E3F2FD')

    # 解调仪内部示意
    draw_rounded_box(ax, 5.0, 5.2, 0.7, 0.5, '光源', color='#0D47A1', fontsize=8)
    draw_rounded_box(ax, 5.8, 5.2, 0.7, 0.5, '光谱分析', color='#0D47A1', fontsize=8)
    draw_rounded_box(ax, 6.4, 5.2, 0.7, 0.5, '数据处理', color='#0D47A1', fontsize=8)

    # 平台端
    draw_rounded_box(ax, 8.8, 4.2, 2.4, 0.9, '数据可视化', color='#9C27B0', fontsize=10)
    draw_rounded_box(ax, 8.8, 3.0, 2.4, 0.9, '阈值/速率告警', color='#9C27B0', fontsize=10)
    draw_rounded_box(ax, 8.8, 1.8, 2.4, 0.9, '健康评估/报表', color='#9C27B0', fontsize=10)

    # 连接箭头：传感端 → 解调端 （双向，光发射 + 反射回来）
    # 下行：光源 → 传感光栅
    draw_arrow(ax, 4.8, 5.45, 3.7, 5.45, color=COLOR_MAIN, style='->', lw=2.5, ls='-')
    draw_label(ax, 4.25, 5.7, '宽带/扫频光', color='#1B5E20', fontsize=8, bg='#E8F5E9')

    # 上行：反射光 → 解调
    draw_arrow(ax, 3.7, 4.95, 4.8, 4.95, color=COLOR_OUT, style='->', lw=2, ls='--')
    draw_label(ax, 4.25, 4.7, '反射光谱', color='#006064', fontsize=8, bg='#E0F7FA')

    # 光纤到各传感器的垂直连接
    draw_arrow(ax, 2.0, 5.4, 2.0, 5.45, color=COLOR_MAIN, style='->', lw=2, ls='-')
    # 用一根光纤线代替
    ax.plot([2.0, 3.7], [5.2, 5.2], color='#FF9800', linewidth=3, zorder=4)
    # 光纤跳线标识
    draw_label(ax, 2.85, 5.35, '单模光纤', color='#E65100', fontsize=8, bg='#FFF3E0')

    # 连接箭头：解调端 → 平台端
    draw_arrow(ax, 7.7, 4.2, 8.8, 4.65, color=COLOR_MAIN, style='->', lw=2.5, ls='-')
    draw_label(ax, 8.25, 4.7, '以太网/RS485\n监测数据', color='#1B5E20', fontsize=8, bg='#E8F5E9')

    # 告警输出
    draw_arrow(ax, 8.8, 2.55, 7.7, 2.0, color=COLOR_OUT, style='->', lw=2, ls='--')
    draw_label(ax, 8.1, 2.1, '告警联动\n(消防/视频)', color='#006064', fontsize=8, bg='#E0F7FA')

    # 底部图例
    legend_y = 0.2
    ax.plot([0.5, 1.2], [legend_y, legend_y], color=COLOR_MAIN, linewidth=2.5, linestyle='-')
    draw_label(ax, 1.8, legend_y, '主数据流向', color=COLOR_TEXT, fontsize=9)

    ax.plot([3.0, 3.7], [legend_y, legend_y], color=COLOR_OUT, linewidth=2, linestyle='--')
    draw_label(ax, 4.5, legend_y, '输出/反馈', color=COLOR_TEXT, fontsize=9)

    ax.plot([5.7, 6.4], [legend_y, legend_y], color='#FF9800', linewidth=3, linestyle='-')
    draw_label(ax, 7.4, legend_y, '光纤链路', color=COLOR_TEXT, fontsize=9)

    # 标题
    ax.text(6.0, 6.7, 'FBG 光纤光栅传感系统三端架构', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#212121')

    plt.tight_layout()
    plt.savefig('images/arch-system.png', dpi=150, bbox_inches='tight',
                facecolor='#FAFAFA', edgecolor='none')
    plt.close()
    print("arch-system.png 生成完成")


# ============================================================
# 图2：FBG 光栅原理与波长漂移
# ============================================================
def draw_principle():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # 标题
    ax.text(6.0, 6.6, 'FBG 光纤光栅传感原理：布拉格条件与波长漂移',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#212121')

    # 上半部分：光纤光栅结构示意
    # 光纤包层
    fiber_y = 5.0
    fiber_x_start = 1.0
    fiber_x_end = 11.0
    cladding_h = 0.8

    # 包层
    cladding = mpatches.FancyBboxPatch((fiber_x_start, fiber_y - cladding_h/2),
                                        fiber_x_end - fiber_x_start, cladding_h,
                                        boxstyle="round,pad=0.01,rounding_size=0.15",
                                        facecolor='#E0E0E0', edgecolor='#9E9E9E',
                                        linewidth=1, zorder=2)
    ax.add_patch(cladding)

    # 纤芯
    core_y = fiber_y
    core_h = 0.25
    core = mpatches.Rectangle((fiber_x_start + 0.3, core_y - core_h/2),
                               fiber_x_end - fiber_x_start - 0.6, core_h,
                               facecolor='#FFF9C4', edgecolor='#FBC02D',
                               linewidth=0.8, zorder=3)
    ax.add_patch(core)

    # 光栅区域（纤芯内的周期条纹）
    grating_start = 4.5
    grating_end = 7.5
    num_lines = 25
    for i in range(num_lines):
        x = grating_start + (grating_end - grating_start) * i / (num_lines - 1)
        ax.plot([x, x], [core_y - core_h/2, core_y + core_h/2],
                color='#E65100', linewidth=1.5, zorder=4)

    # 光栅区域标注
    ax.annotate('', xy=(grating_start, fiber_y + 0.6), xytext=(grating_end, fiber_y + 0.6),
                arrowprops=dict(arrowstyle='<->', color='#E65100', lw=1.5))
    draw_label(ax, 6.0, fiber_y + 0.85, '布拉格光栅区（折射率周期调制）',
               color='#BF360C', fontsize=9, bg='#FFF3E0')

    # 光入射箭头
    draw_arrow(ax, 0.3, fiber_y, 1.0, fiber_y, color='#2E7D32', style='->', lw=2.5, ls='-')
    draw_label(ax, 0.7, fiber_y + 0.3, '宽带入射光', color='#1B5E20', fontsize=9, bg='#E8F5E9')

    # 透射光
    draw_arrow(ax, 11.0, fiber_y, 11.7, fiber_y, color=COLOR_OUT, style='->', lw=2, ls='--')
    draw_label(ax, 11.35, fiber_y + 0.3, '透射光\n（缺反射峰）', color='#006064', fontsize=8, bg='#E0F7FA')

    # 反射光
    draw_arrow(ax, 4.5, fiber_y - 0.55, 2.5, fiber_y - 1.1, color='#9C27B0', style='->', lw=2, ls='-')
    draw_label(ax, 3.0, fiber_y - 1.3, '反射光\n（特定波长）', color='#4A148C', fontsize=8, bg='#F3E5F5')

    # 布拉格条件公式
    formula_box = mpatches.FancyBboxPatch((4.0, 3.2), 4.0, 0.8,
                                           boxstyle="round,pad=0.05,rounding_size=0.1",
                                           facecolor='#FFF8E1', edgecolor='#FFB300',
                                           linewidth=1.2, zorder=3)
    ax.add_patch(formula_box)
    ax.text(6.0, 3.6, 'λ_B = 2 n_eff · Λ', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#E65100', fontfamily='serif')

    # 公式说明
    draw_label(ax, 6.0, 2.7,
               'λ_B：布拉格波长（反射最强波长）\n'
               'n_eff：纤芯有效折射率\n'
               'Λ：光栅周期',
               color='#BF360C', fontsize=9, bg='#FFF3E0')

    # 下半部分：波长漂移示意
    drift_y_base = 0.8
    drift_h = 1.0

    # 左侧：常温状态
    ax.text(3.0, 1.95, '常温状态', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#1565C0')
    # 光谱图（反射峰）
    peak_x1 = 3.0
    peak_w = 0.3
    x1 = np.linspace(peak_x1 - 1.5, peak_x1 + 1.5, 200)
    y1 = 0.8 * np.exp(-((x1 - peak_x1) / peak_w) ** 2)
    ax.plot(x1, drift_y_base + y1 * drift_h, color='#2196F3', linewidth=2, zorder=3)
    ax.fill_between(x1, drift_y_base, drift_y_base + y1 * drift_h,
                    color='#2196F3', alpha=0.2, zorder=2)
    ax.axvline(x=peak_x1, color='#1565C0', linewidth=1, linestyle='--', alpha=0.7)
    draw_label(ax, peak_x1, drift_y_base - 0.15, 'λ_B\n(1550nm)', color='#0D47A1', fontsize=8)
    ax.set_xlim(0, 12)

    # 箭头：温度升高/应变增加
    draw_arrow(ax, 4.8, drift_y_base + 0.5, 7.2, drift_y_base + 0.5,
               color='#F44336', style='->', lw=2.5, ls='-')
    draw_label(ax, 6.0, drift_y_base + 0.7,
               '温度升高 / 应变增加\nλ_B 向长波方向漂移',
               color='#B71C1C', fontsize=9, bg='#FFEBEE')

    # 右侧：升温/应变状态
    ax.text(9.0, 1.95, '升温/加应变后', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#C62828')
    peak_x2 = 9.0
    x2 = np.linspace(peak_x2 - 1.5, peak_x2 + 1.5, 200)
    y2 = 0.8 * np.exp(-((x2 - peak_x2) / peak_w) ** 2)
    ax.plot(x2, drift_y_base + y2 * drift_h, color='#F44336', linewidth=2, zorder=3)
    ax.fill_between(x2, drift_y_base, drift_y_base + y2 * drift_h,
                    color='#F44336', alpha=0.2, zorder=2)
    ax.axvline(x=peak_x2, color='#C62828', linewidth=1, linestyle='--', alpha=0.7)
    draw_label(ax, peak_x2, drift_y_base - 0.15, "λ_B'\n(1550.Xnm)", color='#B71C1C', fontsize=8)

    # 波长轴标注
    ax.plot([1.0, 11.0], [drift_y_base - 0.3, drift_y_base - 0.3],
            color='#666', linewidth=1, zorder=1)
    draw_arrow(ax, 10.5, drift_y_base - 0.3, 11.0, drift_y_base - 0.3,
               color='#666', style='->', lw=1, ls='-')
    draw_label(ax, 6.0, drift_y_base - 0.5, '波长 λ（从短到长）', color='#666', fontsize=8)

    plt.tight_layout()
    plt.savefig('images/arch-principle.png', dpi=150, bbox_inches='tight',
                facecolor='#FAFAFA', edgecolor='none')
    plt.close()
    print("arch-principle.png 生成完成")


# ============================================================
# 图3：波分复用（WDM）串接原理
# ============================================================
def draw_wdm():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # 标题
    ax.text(6.0, 6.6, 'FBG 波分复用（WDM）串接原理：一纤多点，波长分立',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#212121')

    # 上半部分：光纤上串接多个光栅
    fiber_y = 5.5
    fiber_x_start = 1.5
    fiber_x_end = 10.5

    # 光纤包层
    cladding = mpatches.FancyBboxPatch((fiber_x_start, fiber_y - 0.4),
                                        fiber_x_end - fiber_x_start, 0.8,
                                        boxstyle="round,pad=0.01,rounding_size=0.15",
                                        facecolor='#E0E0E0', edgecolor='#9E9E9E',
                                        linewidth=1, zorder=2)
    ax.add_patch(cladding)

    # 纤芯
    core = mpatches.Rectangle((fiber_x_start + 0.2, fiber_y - 0.12),
                               fiber_x_end - fiber_x_start - 0.4, 0.24,
                               facecolor='#FFF9C4', edgecolor='#FBC02D',
                               linewidth=0.8, zorder=3)
    ax.add_patch(core)

    # 5 个光栅
    grating_positions = [2.5, 4.2, 5.9, 7.6, 9.3]
    grating_colors = ['#E53935', '#FB8C00', '#FDD835', '#43A047', '#1E88E5']
    grating_labels = ['λ₁', 'λ₂', 'λ₃', 'λ₄', 'λ₅']
    grating_names = ['测点1\n温度', '测点2\n应变', '测点3\n温度', '测点4\n应变', '测点5\n位移']

    for i, (gx, gc, gl, gn) in enumerate(zip(grating_positions, grating_colors, grating_labels, grating_names)):
        # 光栅条纹
        for j in range(8):
            x = gx - 0.25 + j * 0.07
            ax.plot([x, x], [fiber_y - 0.12, fiber_y + 0.12],
                    color=gc, linewidth=1.2, zorder=4)
        # 测点编号
        draw_label(ax, gx, fiber_y + 0.7, gn, color='#212121', fontsize=8, bg='#F5F5F5')
        draw_label(ax, gx, fiber_y - 0.75, gl, color=gc, fontsize=11, fontweight='bold')

    # 入射光（从左侧来）
    draw_arrow(ax, 0.3, fiber_y, 1.5, fiber_y, color='#2E7D32', style='->', lw=2.5, ls='-')
    draw_label(ax, 0.9, fiber_y + 0.4, '宽带入射光\n（含所有波长）', color='#1B5E20', fontsize=8, bg='#E8F5E9')

    # 反射光（向左返回）
    draw_arrow(ax, 1.5, fiber_y - 0.6, 0.3, fiber_y - 1.0, color='#9C27B0', style='->', lw=2, ls='-')
    draw_label(ax, 0.9, fiber_y - 1.2, '复合反射光\n（5个反射峰）', color='#4A148C', fontsize=8, bg='#F3E5F5')

    # 下半部分：光谱图
    spec_y_base = 0.8
    spec_h = 2.8
    spec_x_left = 1.5
    spec_x_right = 10.5

    # 光谱框
    spec_box = mpatches.FancyBboxPatch((spec_x_left, spec_y_base),
                                        spec_x_right - spec_x_left, spec_h,
                                        boxstyle="round,pad=0.02,rounding_size=0.1",
                                        facecolor='white', edgecolor='#BDBDBD',
                                        linewidth=1, zorder=1)
    ax.add_patch(spec_box)

    # 坐标轴
    ax.plot([spec_x_left + 0.3, spec_x_right - 0.3], [spec_y_base + 0.3, spec_y_base + 0.3],
            color='#666', linewidth=1, zorder=2)
    ax.plot([spec_x_left + 0.3, spec_x_left + 0.3], [spec_y_base + 0.3, spec_y_base + spec_h - 0.3],
            color='#666', linewidth=1, zorder=2)

    draw_label(ax, spec_x_right - 0.5, spec_y_base + 0.5, '波长 λ', color='#666', fontsize=9)
    draw_label(ax, spec_x_left + 0.7, spec_y_base + spec_h - 0.5, '反射强度', color='#666', fontsize=9)

    # 5 个反射峰
    peak_positions_x = [2.5, 4.2, 5.9, 7.6, 9.3]
    peak_heights = [2.0, 1.8, 2.2, 1.9, 1.7]
    peak_widths = [0.3, 0.3, 0.3, 0.3, 0.3]

    for px, ph, pw, pc, pl in zip(peak_positions_x, peak_heights, peak_widths,
                                   grating_colors, grating_labels):
        x = np.linspace(px - 1.0, px + 1.0, 200)
        y = ph * np.exp(-((x - px) / pw) ** 2)
        ax.plot(x, spec_y_base + 0.5 + y, color=pc, linewidth=2, zorder=3)
        ax.fill_between(x, spec_y_base + 0.5, spec_y_base + 0.5 + y,
                        color=pc, alpha=0.25, zorder=2)
        # 波长标注
        draw_label(ax, px, spec_y_base + 0.5 + ph + 0.15, pl, color=pc, fontsize=10, fontweight='bold')

    # 解调仪识别示意
    draw_label(ax, 6.0, spec_y_base + spec_h + 0.1,
               '↓ 解调仪按波长逐一识别，各测点独立读数',
               color='#1B5E20', fontsize=10, fontweight='bold')

    # 特点说明
    features_y = 3.8
    feature_box = mpatches.FancyBboxPatch((1.5, features_y - 0.5), 9.0, 0.9,
                                           boxstyle="round,pad=0.03,rounding_size=0.1",
                                           facecolor='#E8F5E9', edgecolor='#66BB6A',
                                           linewidth=1, zorder=2)
    ax.add_patch(feature_box)
    ax.text(6.0, features_y - 0.05,
            '核心特点：每个光栅有唯一的中心波长，反射谱在波长轴上互不重叠，'
            '因此可在同一根光纤上串接数十个测点',
            ha='center', va='center', fontsize=9, color='#1B5E20')

    plt.tight_layout()
    plt.savefig('images/arch-wdm.png', dpi=150, bbox_inches='tight',
                facecolor='#FAFAFA', edgecolor='none')
    plt.close()
    print("arch-wdm.png 生成完成")


if __name__ == '__main__':
    import os
    os.makedirs('images', exist_ok=True)
    draw_system_arch()
    draw_principle()
    draw_wdm()
    print("\n所有架构图/原理图生成完成！")
