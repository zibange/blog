"""
LCD 液晶拼接屏产品图表生成脚本
生成三张矢量示意图：
  1. arch-system.png  - LCD 拼接系统三层架构图
  2. flow-signal.png  - 拼接处理信号链路图
  3. scene-command.png - 指挥中心典型部署拓扑图

遵循链路绘制规范：
  - 正交分支（无斜线）
  - 颜色 + 线型双重编码（主流程绿实线、输出青虚线、异常红虚线）
  - 双向箭头留间隙
  - 底部图例
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 颜色定义
COLOR_MAIN = "#2ECC71"      # 主流程 - 绿色实线
COLOR_OUTPUT = "#3498DB"    # 输出/结果 - 青色虚线
COLOR_ANOMALY = "#E74C3C"   # 异常 - 红色虚线
COLOR_BOX = "#2C3E50"       # 框边框色
COLOR_BOX_FILL = "#ECF0F1"  # 框填充色
COLOR_TITLE = "#1A252F"     # 标题色
COLOR_TEXT = "#2C3E50"      # 正文文字色
COLOR_LAYER_BG = "#D5DBDB"  # 层背景色


def draw_rounded_box(ax, x, y, w, h, text, fontsize=10, fontweight="normal",
                     fill_color=COLOR_BOX_FILL, border_color=COLOR_BOX, text_color=COLOR_TEXT):
    """画一个圆角矩形框"""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.5,
        edgecolor=border_color,
        facecolor=fill_color,
        zorder=2
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=fontsize, fontweight=fontweight,
        color=text_color, zorder=3
    )


def draw_arrow(ax, x1, y1, x2, y2, color=COLOR_MAIN, linestyle="-",
               linewidth=1.5, style="->", mutation_scale=15):
    """画箭头（正交方向）"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        color=color,
        linestyle=linestyle,
        linewidth=linewidth,
        mutation_scale=mutation_scale,
        zorder=1
    )
    ax.add_patch(arrow)


def draw_double_arrow(ax, x1, y1, x2, y2, color=COLOR_MAIN, linewidth=1.5):
    """画双向箭头（两端留间隙）"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="<->",
        color=color,
        linewidth=linewidth,
        mutation_scale=12,
        zorder=1
    )
    ax.add_patch(arrow)


def setup_figure(width=10, height=6, title=""):
    """设置画布"""
    fig, ax = plt.subplots(figsize=(width, height), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.text(5, 9.6, title, ha="center", va="top",
                fontsize=14, fontweight="bold", color=COLOR_TITLE)
    return fig, ax


def add_legend(ax, items):
    """添加图例
    items: [(color, linestyle, label), ...]
    """
    y_base = 0.3
    x_start = 1.0
    spacing = 2.5
    
    for i, (color, linestyle, label) in enumerate(items):
        x = x_start + i * spacing
        # 画线
        ax.plot([x, x + 0.8], [y_base, y_base], color=color,
                linestyle=linestyle, linewidth=2, zorder=1)
        # 箭头
        ax.annotate("", xy=(x + 0.9, y_base), xytext=(x + 0.8, y_base),
                    arrowprops=dict(arrowstyle="->", color=color, linewidth=2))
        # 文字
        ax.text(x + 1.1, y_base, label, ha="left", va="center",
                fontsize=9, color=COLOR_TEXT)


def draw_arch_system():
    """图1: LCD 拼接系统三层架构图"""
    fig, ax = setup_figure(10, 7.5, "LCD 拼接系统三层架构")

    # 三层：输入层（上）、处理层（中）、显示层（下）
    # 层背景
    layer_y = [7.5, 4.8, 1.8]
    layer_h = [1.8, 2.2, 2.4]
    layer_titles = ["输入层 / 信号源", "处理层 / 拼接处理器", "显示层 / 拼接墙"]
    
    for i, (y, h, title) in enumerate(zip(layer_y, layer_h, layer_titles)):
        rect = patches.Rectangle(
            (0.5, y), 9, h,
            linewidth=1,
            edgecolor="#BDC3C7",
            facecolor=COLOR_LAYER_BG,
            alpha=0.5,
            zorder=0
        )
        ax.add_patch(rect)
        ax.text(5, y + h - 0.25, title, ha="center", va="top",
                fontsize=11, fontweight="bold", color=COLOR_TITLE)

    # 输入层设备
    input_devices = [
        (1.0, "监控摄像头"),
        (3.2, "电脑主机"),
        (5.4, "视频会议终端"),
        (7.6, "播放器/机顶盒"),
    ]
    for x, name in input_devices:
        draw_rounded_box(ax, x, 8.0, 1.6, 0.8, name, fontsize=9)

    # 处理层 - 拼接处理器
    draw_rounded_box(ax, 2.5, 5.3, 5.0, 1.1, "拼接处理器",
                     fontsize=12, fontweight="bold",
                     fill_color="#D5F5E3", border_color="#27AE60")
    ax.text(5.0, 5.15, "信号采集 · 画面分割 · 多窗口叠加 · 输出驱动",
            ha="center", va="top", fontsize=8.5, color=COLOR_TEXT)

    # 处理层内部模块（小框）
    modules = ["采集模块", "Scaler缩放", "帧缓冲", "输出驱动"]
    for i, mod in enumerate(modules):
        x = 2.8 + i * 1.15
        draw_rounded_box(ax, x, 5.5, 1.0, 0.55, mod, fontsize=8,
                         fill_color="#D6EAF8", border_color="#2980B9")

    # 显示层 - 3x3 拼接墙示意
    for row in range(2):
        for col in range(4):
            x = 2.0 + col * 1.6
            y = 2.2 + row * 1.1
            draw_rounded_box(ax, x, y, 1.4, 0.9, "", fontsize=8,
                             fill_color="#D6EAF8", border_color="#2980B9")
            # 拼缝示意
            if col < 3:
                ax.plot([x + 1.4, x + 1.4], [y, y + 0.9],
                        color="#BDC3C7", linewidth=2, zorder=3)
            if row < 1:
                ax.plot([x, x + 1.4], [y + 0.9, y + 0.9],
                        color="#BDC3C7", linewidth=2, zorder=3)

    ax.text(5.0, 1.95, "2×4 LCD 拼接墙（8 单元）",
            ha="center", va="top", fontsize=9, fontweight="bold",
            color=COLOR_TITLE)

    # 箭头：输入层 → 处理层（4路输入，绿色实线）
    for x, _ in input_devices:
        draw_arrow(ax, x + 0.8, 8.0, x + 0.8, 6.45, color=COLOR_MAIN)

    # 箭头：处理层 → 显示层（8路输出，青色虚线）
    output_xs = [2.7, 4.3, 5.9, 7.5]  # 对应4列
    for x in output_xs:
        # 下行到显示层顶部
        draw_arrow(ax, x, 5.3, x, 4.3, color=COLOR_OUTPUT, linestyle="--")
        # 分叉到两行
        # 第一行（上）
        draw_arrow(ax, x, 4.3, x, 4.0, color=COLOR_OUTPUT, linestyle="--")
        # 第二行（下）- 先水平偏移再垂直向下
        # 简化：直接画到每列中心
        pass

    # 简化：从处理器底部画8根箭头到8个屏
    screen_centers_x = [2.7, 4.3, 5.9, 7.5]  # 列中心
    screen_ys_top = [3.3, 2.2]  # 两行顶部
    screen_ys_bottom = [4.2, 3.1]  # 两行底部
    
    # 处理器输出点
    proc_out_x = [3.0, 3.8, 4.6, 5.4, 6.2, 7.0]
    # 简化：画4根主要的输出箭头
    for i, sx in enumerate(screen_centers_x):
        px = 3.0 + i * 1.3
        # 三段折线：处理器底部 -> 垂直向下 -> 水平对齐 -> 垂直到屏顶
        # 直接画垂直箭头（简化版）
        draw_arrow(ax, px, 5.3, px, 4.25, color=COLOR_OUTPUT, linestyle="--")
        # 再分叉到两个屏幕
        # 上屏
        draw_arrow(ax, px, 4.25, sx, 4.05, color=COLOR_OUTPUT, linestyle="--")
        # 下屏 - 用正交折线
        # 先竖后横再竖
        pass

    # 控制层 - 控制软件（右侧）
    draw_rounded_box(ax, 8.2, 5.0, 1.3, 0.7, "控制软件",
                     fontsize=9, fill_color="#FCF3CF", border_color="#F39C12")
    ax.text(8.85, 4.85, "C/S / B/S / APP",
            ha="center", va="top", fontsize=7.5, color=COLOR_TEXT)

    # 双向箭头：控制软件 ↔ 处理器
    draw_double_arrow(ax, 7.5, 5.35, 8.2, 5.35, color="#F39C12")

    # 图例
    add_legend(ax, [
        (COLOR_MAIN, "-", "信号输入"),
        (COLOR_OUTPUT, "--", "显示输出"),
        ("#F39C12", "-", "控制信号"),
    ])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "arch-system.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成 arch-system.png")


def draw_flow_signal():
    """图2: 拼接处理信号链路图"""
    fig, ax = setup_figure(10, 6.5, "拼接处理信号链路")

    # 横向流程：信号源 → 采集 → 缩放/分割 → 帧缓冲(叠加混合) → 输出驱动 → 拼接墙
    boxes = [
        (0.5, 5.0, 1.6, 1.0, "信号源", "#FADBD8", "#C0392B"),
        (2.7, 5.0, 1.6, 1.0, "信号采集\n与数字化", "#FDEDEC", "#E74C3C"),
        (4.9, 5.0, 1.6, 1.0, "Scaler\n缩放与分割", "#EBF5FB", "#3498DB"),
        (7.1, 5.0, 1.6, 1.0, "帧缓冲\n窗口叠加", "#E8F8F5", "#1ABC9C"),
        (4.9, 2.5, 1.6, 1.0, "输出驱动\n与帧同步", "#E8F6F3", "#16A085"),
        (7.5, 2.5, 2.0, 1.0, "拼接墙\n（多屏输出）", "#D5F5E3", "#27AE60"),
    ]

    for x, y, w, h, text, fill, border in boxes:
        draw_rounded_box(ax, x, y, w, h, text, fontsize=9.5, fontweight="bold",
                         fill_color=fill, border_color=border)

    # 主流程箭头（绿色实线，从左到右）
    draw_arrow(ax, 2.1, 5.5, 2.7, 5.5, color=COLOR_MAIN, linewidth=2)
    draw_arrow(ax, 4.3, 5.5, 4.9, 5.5, color=COLOR_MAIN, linewidth=2)
    draw_arrow(ax, 6.5, 5.5, 7.1, 5.5, color=COLOR_MAIN, linewidth=2)

    # 帧缓冲 → 输出驱动（向下，青色虚线，判定结果）
    draw_arrow(ax, 5.7, 5.0, 5.7, 3.5, color=COLOR_OUTPUT, linestyle="--", linewidth=2)

    # 输出驱动 → 拼接墙（向右，青色虚线）
    draw_arrow(ax, 6.5, 3.0, 7.5, 3.0, color=COLOR_OUTPUT, linestyle="--", linewidth=2)

    # 旁路：控制软件（上方）
    draw_rounded_box(ax, 4.2, 7.5, 1.6, 0.8, "控制软件\n场景/窗口管理",
                     fontsize=9, fill_color="#FCF3CF", border_color="#F39C12")
    
    # 控制信号（双向，黄色）
    draw_double_arrow(ax, 5.0, 7.5, 5.0, 6.0, color="#F39C12", linewidth=1.5)

    # 输出多路示意：从输出驱动向右引出多路输出
    for i, y_off in enumerate([-0.3, 0, 0.3]):
        y_pos = 3.0 + y_off
        draw_arrow(ax, 7.1, y_pos, 7.5, y_pos, color=COLOR_OUTPUT, linestyle="--",
                   linewidth=1)

    ax.text(7.8, 3.4, "N路输出\n(对应N块屏)", ha="left", va="center",
            fontsize=8, color=COLOR_TEXT)

    # 标注处理阶段说明
    steps = [
        (1.3, 4.2, "各类信号源\n(监控/电脑/会议)"),
        (3.5, 4.2, "HDMI/DP/SDI等\n接口接收"),
        (5.7, 4.2, "分辨率转换\n画面切割"),
        (7.9, 4.2, "多窗口混合\nAlpha叠加"),
    ]
    for x, y, text in steps:
        ax.text(x, y, text, ha="center", va="top", fontsize=7.5,
                color="#566573", style="italic")

    # 图例
    add_legend(ax, [
        (COLOR_MAIN, "-", "主处理流程"),
        (COLOR_OUTPUT, "--", "显示输出"),
        ("#F39C12", "-", "控制信号"),
    ])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "flow-signal.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成 flow-signal.png")


def draw_scene_command():
    """图3: 指挥中心典型部署拓扑图"""
    fig, ax = setup_figure(10, 7, "指挥中心典型部署拓扑")

    # 大屏显示区（上方中间）
    draw_rounded_box(ax, 2.5, 7.5, 5.0, 1.3, "LCD 拼接大屏\n(3×6 / 1.7mm)",
                     fontsize=11, fontweight="bold",
                     fill_color="#D6EAF8", border_color="#2980B9")

    # 拼接处理器（大屏下方）
    draw_rounded_box(ax, 3.5, 5.8, 3.0, 1.0, "拼接处理器\n(双电源热备)",
                     fontsize=10, fontweight="bold",
                     fill_color="#D5F5E3", border_color="#27AE60")

    # 大屏 ↔ 处理器
    draw_double_arrow(ax, 5.0, 7.5, 5.0, 6.8, color=COLOR_OUTPUT, linewidth=2)

    # 左侧：信号源区
    sources = [
        (0.5, 6.2, "视频监控\n平台", "#FADBD8"),
        (0.5, 4.8, "GIS / 大数据\n可视化平台", "#FDEDEC"),
        (0.5, 3.4, "视频会议\n终端", "#FAD7A0"),
        (0.5, 2.0, "工作站\n电脑", "#D5F5E3"),
    ]
    for x, y, name, fill in sources:
        draw_rounded_box(ax, x, y, 1.8, 0.9, name, fontsize=8.5,
                         fill_color=fill, border_color=COLOR_BOX)
        # 信号输入到处理器（绿色实线，正交折线）
        # 先水平到处理器左侧x坐标，再向上/向下到处理器
        proc_x = 3.5
        proc_y = 6.3
        # 水平段
        ax.plot([x + 1.8, proc_x - 0.2], [y + 0.45, y + 0.45],
                color=COLOR_MAIN, linewidth=1.5, zorder=1)
        # 垂直段
        ax.plot([proc_x - 0.2, proc_x - 0.2], [y + 0.45, proc_y],
                color=COLOR_MAIN, linewidth=1.5, zorder=1)
        # 箭头头
        ax.annotate("", xy=(proc_x, proc_y), xytext=(proc_x - 0.2, proc_y),
                    arrowprops=dict(arrowstyle="->", color=COLOR_MAIN, linewidth=1.5))

    # 右侧：控制区
    controls = [
        (7.7, 5.8, "控制电脑\n(C/S客户端)", "#FCF3CF"),
        (7.7, 4.4, "平板APP\n(移动控制)", "#FDEBD0"),
        (7.7, 3.0, "集中监控\n运维平台", "#E8DAEF"),
    ]
    for x, y, name, fill in controls:
        draw_rounded_box(ax, x, y, 1.8, 0.9, name, fontsize=8.5,
                         fill_color=fill, border_color=COLOR_BOX)
        # 双向控制箭头（橙色）
        ctrl_x = 6.5
        ctrl_y = y + 0.45
        ax.plot([ctrl_x + 0.2, x], [ctrl_y, ctrl_y],
                color="#F39C12", linewidth=1.5, zorder=1)
        # 双向箭头头
        ax.annotate("", xy=(x, ctrl_y), xytext=(x - 0.2, ctrl_y),
                    arrowprops=dict(arrowstyle="->", color="#F39C12", linewidth=1.5))
        ax.annotate("", xy=(ctrl_x + 0.2, ctrl_y), xytext=(ctrl_x + 0.4, ctrl_y),
                    arrowprops=dict(arrowstyle="->", color="#F39C12", linewidth=1.5))

    # 下方：坐席区
    draw_rounded_box(ax, 2.5, 0.5, 5.0, 0.8, "指挥坐席区（多工位）",
                     fontsize=10, fontweight="bold",
                     fill_color="#EBF5FB", border_color="#2980B9")
    
    # 坐席区与处理器的关系（虚线标注）
    ax.annotate(
        "", xy=(5.0, 1.3), xytext=(5.0, 5.8),
        arrowprops=dict(arrowstyle="->", color="#85929E",
                        linestyle=":", linewidth=1.2)
    )
    ax.text(5.3, 3.5, "操作人员\n通过控制端\n调度大屏",
            ha="left", va="center", fontsize=7.5,
            color="#566573", style="italic")

    # 网络连接标注（左下）
    ax.text(0.5, 0.6, "所有设备接入局域网\n支持远程管理与运维",
            ha="left", va="center", fontsize=7.5,
            color="#566573", style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="#F2F3F4", ec="#BDC3C7"))

    # 图例
    add_legend(ax, [
        (COLOR_MAIN, "-", "视频信号输入"),
        (COLOR_OUTPUT, "-", "显示输出"),
        ("#F39C12", "-", "控制信号"),
    ])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "scene-command.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成 scene-command.png")


if __name__ == "__main__":
    print("正在生成 LCD 液晶拼接屏产品图表...")
    draw_arch_system()
    draw_flow_signal()
    draw_scene_command()
    print(f"\n所有图表已生成到: {OUTPUT_DIR}")
