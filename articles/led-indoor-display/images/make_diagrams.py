"""
室内 LED 显示屏产品图表生成脚本
生成三张矢量示意图：
  1. arch-system.png  - 室内 LED 显示系统架构图
  2. flow-display.png - LED 显示驱动链路图
  3. scene-indoor.png - 室内典型应用场景示意图

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

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
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
    """画箭头"""
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
    """图1: 室内 LED 显示系统架构图"""
    fig, ax = setup_figure(10, 7.5, "室内 LED 显示系统架构")

    # 三层结构：控制层（上）、发送层（中）、接收显示层（下）
    layer_y = [7.5, 5.0, 2.0]
    layer_h = [1.6, 2.0, 2.6]
    layer_titles = ["控制层 / 信号源与控制", "发送层 / 发送卡与视频处理", "接收显示层 / 接收卡与 LED 模组"]

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

    # 控制层设备
    control_devices = [
        (1.2, "视频源\n(电脑/监控)"),
        (3.5, "视频处理器"),
        (5.8, "发送卡"),
        (8.0, "控制软件"),
    ]
    for x, name in control_devices:
        draw_rounded_box(ax, x, 8.0, 1.5, 0.7, name, fontsize=8.5,
                         fill_color="#FCF3CF", border_color="#F39C12")

    # 发送层 - 发送卡与分配器
    # 主发送卡
    draw_rounded_box(ax, 3.5, 6.0, 3.0, 0.9, "发送卡 / 主控器",
                     fontsize=11, fontweight="bold",
                     fill_color="#D5F5E3", border_color="#27AE60")
    ax.text(5.0, 5.85, "DVI/HDMI输入 · 千兆网口输出 · 色度校正",
            ha="center", va="top", fontsize=8, color=COLOR_TEXT)

    # 发送层内部模块
    send_modules = ["信号接收", "图像处理", "数据打包", "网口输出"]
    for i, mod in enumerate(send_modules):
        x = 3.7 + i * 0.7
        draw_rounded_box(ax, x, 5.2, 0.6, 0.5, mod, fontsize=7,
                         fill_color="#D6EAF8", border_color="#2980B9")

    # 接收显示层 - LED箱体阵列
    # 画 3×4 的箱体示意
    for row in range(3):
        for col in range(4):
            x = 1.8 + col * 1.7
            y = 2.5 + row * 1.0
            draw_rounded_box(ax, x, y, 1.5, 0.85, f"箱体{row*4+col+1}",
                             fontsize=7.5,
                             fill_color="#D6EAF8", border_color="#2980B9")
            # 模组拼缝示意（横向和纵向各一条）
            ax.plot([x + 0.75, x + 0.75], [y + 0.1, y + 0.75],
                    color="#BDC3C7", linewidth=1, zorder=3)
            ax.plot([x + 0.1, x + 1.4], [y + 0.425, y + 0.425],
                    color="#BDC3C7", linewidth=1, zorder=3)

    ax.text(5.0, 2.2, "LED 屏体（3×4 箱体 / 每箱若干模组）",
            ha="center", va="top", fontsize=9, fontweight="bold",
            color=COLOR_TITLE)

    # 箭头：控制层 → 发送层
    draw_arrow(ax, 5.0, 8.0, 5.0, 6.95, color=COLOR_MAIN, linewidth=2)
    draw_arrow(ax, 1.95, 8.0, 1.95, 7.0, color=COLOR_MAIN)
    draw_arrow(ax, 4.25, 8.0, 4.25, 7.0, color=COLOR_MAIN)

    # 控制软件双向箭头
    draw_double_arrow(ax, 8.75, 8.0, 8.75, 7.0, color="#F39C12", linewidth=1.5)

    # 箭头：发送层 → 接收显示层（多路网线输出，青色虚线）
    # 从发送卡底部引出多路到箱体
    output_points = [2.55, 4.25, 5.95, 7.65]  # 4列中心
    for i, sx in enumerate(output_points):
        px = 3.8 + i * 0.8
        # 三段正交折线
        # 发送卡底部向下
        draw_arrow(ax, px, 6.0, px, 5.3, color=COLOR_OUTPUT, linestyle="--")
        # 水平到列上方
        ax.plot([px, sx], [5.3, 5.3], color=COLOR_OUTPUT, linestyle="--", linewidth=1.5, zorder=1)
        # 垂直向下到箱体顶部
        draw_arrow(ax, sx, 5.3, sx, 4.6, color=COLOR_OUTPUT, linestyle="--")
        # 分叉到3行箱体（只画到最上面一行，其余用虚线示意级联）
        for row in range(1, 3):
            box_top_y = 2.5 + row * 1.0 + 0.85
            draw_arrow(ax, sx, box_top_y + 0.15, sx, box_top_y,
                       color=COLOR_OUTPUT, linestyle="--", linewidth=1)

    # 标注网线级联
    ax.text(8.8, 3.5, "网线\n级联", ha="left", va="center",
            fontsize=7.5, color="#566573", style="italic")

    # 图例
    add_legend(ax, [
        (COLOR_MAIN, "-", "视频信号输入"),
        (COLOR_OUTPUT, "--", "网线数据传输"),
        ("#F39C12", "-", "控制信号"),
    ])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "arch-system.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成 arch-system.png")


def draw_flow_display():
    """图2: LED 显示驱动链路图"""
    fig, ax = setup_figure(10, 6.5, "LED 显示驱动链路")

    # 横向主流程：视频源 → 视频处理器 → 发送卡 → 接收卡 → 驱动IC → LED灯珠
    boxes = [
        (0.3, 5.2, 1.5, 1.0, "视频信号源\n(电脑/播放器)", "#FADBD8", "#C0392B"),
        (2.3, 5.2, 1.5, 1.0, "视频处理器\n(缩放/拼接)", "#FDEDEC", "#E74C3C"),
        (4.3, 5.2, 1.5, 1.0, "发送卡\n(数据打包编码)", "#EBF5FB", "#3498DB"),
        (6.3, 5.2, 1.5, 1.0, "接收卡\n(数据分发校正)", "#E8F8F5", "#1ABC9C"),
        (4.3, 2.5, 1.5, 1.0, "驱动 IC\n(恒流驱动/PWM)", "#E8F6F3", "#16A085"),
        (6.8, 2.5, 2.2, 1.0, "LED 灯珠\n(R/G/B 发光)", "#D5F5E3", "#27AE60"),
    ]

    for x, y, w, h, text, fill, border in boxes:
        draw_rounded_box(ax, x, y, w, h, text, fontsize=9, fontweight="bold",
                         fill_color=fill, border_color=border)

    # 主流程箭头（绿色实线，从左到右）
    draw_arrow(ax, 1.8, 5.7, 2.3, 5.7, color=COLOR_MAIN, linewidth=2)
    draw_arrow(ax, 3.8, 5.7, 4.3, 5.7, color=COLOR_MAIN, linewidth=2)
    draw_arrow(ax, 5.8, 5.7, 6.3, 5.7, color=COLOR_MAIN, linewidth=2)

    # 接收卡 → 驱动IC（向下，青色虚线）
    draw_arrow(ax, 5.05, 5.2, 5.05, 3.5, color=COLOR_OUTPUT, linestyle="--", linewidth=2)

    # 驱动IC → LED灯珠（向右，青色虚线）
    draw_arrow(ax, 5.8, 3.0, 6.8, 3.0, color=COLOR_OUTPUT, linestyle="--", linewidth=2)

    # 旁路：控制与校正（上方）
    draw_rounded_box(ax, 4.0, 7.5, 2.0, 0.8, "控制软件 / 校正系统\n(亮度/色度逐点校正)",
                     fontsize=8.5, fill_color="#FCF3CF", border_color="#F39C12")

    # 控制信号（双向，黄色虚线）
    draw_double_arrow(ax, 5.0, 7.5, 5.0, 6.2, color="#F39C12", linewidth=1.5)

    # 级联标注（右侧）
    ax.text(8.2, 5.7, "→ 级联下一张\n接收卡", ha="left", va="center",
            fontsize=7.5, color="#566573", style="italic")
    draw_arrow(ax, 7.8, 5.7, 8.2, 5.7, color=COLOR_OUTPUT, linestyle="--", linewidth=1)

    # 各阶段说明
    steps = [
        (1.05, 4.3, "原始视频信号\nHDMI/DVI/SDI"),
        (3.05, 4.3, "图像增强\n分辨率转换"),
        (5.05, 4.3, "DVI信号编码\n千兆网输出"),
        (7.05, 4.3, "数据接收\n逐点校正"),
    ]
    for x, y, text in steps:
        ax.text(x, y, text, ha="center", va="top", fontsize=7.5,
                color="#566573", style="italic")

    # 驱动原理说明（下方）
    ax.text(5.0, 1.5, "驱动IC以PWM方式控制LED灯珠的导通时间比例，\n"
            "通过R/G/B三色不同亮度组合，混合出各种颜色与灰阶。",
            ha="center", va="top", fontsize=8,
            color="#566573", style="italic",
            bbox=dict(boxstyle="round,pad=0.4", fc="#F2F3F4", ec="#BDC3C7"))

    # 图例
    add_legend(ax, [
        (COLOR_MAIN, "-", "主信号链路"),
        (COLOR_OUTPUT, "--", "数据/驱动输出"),
        ("#F39C12", "-", "控制/校正信号"),
    ])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "flow-display.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成 flow-display.png")


def draw_scene_indoor():
    """图3: 室内 LED 显示屏典型应用场景示意图"""
    fig, ax = setup_figure(10, 7, "室内 LED 屏典型应用场景")

    # 上方：LED大屏
    draw_rounded_box(ax, 2.0, 7.5, 6.0, 1.2, "室内 LED 小间距大屏\n(P1.5~P2.5 / 无缝拼接)",
                     fontsize=11, fontweight="bold",
                     fill_color="#D6EAF8", border_color="#2980B9")

    # 大屏下方：控制系统机柜
    draw_rounded_box(ax, 3.5, 5.8, 3.0, 0.9, "控制系统机柜\n(发送卡+接收卡+电源)",
                     fontsize=9, fontweight="bold",
                     fill_color="#D5F5E3", border_color="#27AE60")

    # 大屏 ↔ 机柜
    draw_double_arrow(ax, 5.0, 7.5, 5.0, 6.7, color=COLOR_OUTPUT, linewidth=2)

    # 左侧：信号与输入
    sources = [
        (0.3, 6.0, "视频会议\n终端", "#FADBD8"),
        (0.3, 4.7, "监控平台\n解码器", "#FDEDEC"),
        (0.3, 3.4, "数据可视化\n工作站", "#FAD7A0"),
        (0.3, 2.1, "媒体播放\n服务器", "#D5F5E3"),
    ]
    for x, y, name, fill in sources:
        draw_rounded_box(ax, x, y, 1.9, 0.85, name, fontsize=8,
                         fill_color=fill, border_color=COLOR_BOX)
        # 正交折线连接到机柜
        proc_x = 3.5
        proc_y = 6.25
        mid_x = 2.6
        # 水平段
        ax.plot([x + 1.9, mid_x], [y + 0.425, y + 0.425],
                color=COLOR_MAIN, linewidth=1.5, zorder=1)
        # 垂直段
        ax.plot([mid_x, mid_x], [y + 0.425, proc_y],
                color=COLOR_MAIN, linewidth=1.5, zorder=1)
        # 箭头头
        ax.annotate("", xy=(proc_x, proc_y), xytext=(mid_x, proc_y),
                    arrowprops=dict(arrowstyle="->", color=COLOR_MAIN, linewidth=1.5))

    # 右侧：控制与运维
    controls = [
        (7.8, 5.8, "操作电脑\n(控制软件)", "#FCF3CF"),
        (7.8, 4.5, "平板APP\n(移动调试)", "#FDEBD0"),
        (7.8, 3.2, "运维平台\n(状态监控)", "#E8DAEF"),
    ]
    for x, y, name, fill in controls:
        draw_rounded_box(ax, x, y, 1.9, 0.85, name, fontsize=8,
                         fill_color=fill, border_color=COLOR_BOX)
        # 双向控制
        ctrl_x = 6.5
        ctrl_y = y + 0.425
        ax.plot([ctrl_x + 0.2, x], [ctrl_y, ctrl_y],
                color="#F39C12", linewidth=1.5, zorder=1)
        ax.annotate("", xy=(x, ctrl_y), xytext=(x - 0.2, ctrl_y),
                    arrowprops=dict(arrowstyle="->", color="#F39C12", linewidth=1.5))
        ax.annotate("", xy=(ctrl_x + 0.2, ctrl_y), xytext=(ctrl_x + 0.4, ctrl_y),
                    arrowprops=dict(arrowstyle="->", color="#F39C12", linewidth=1.5))

    # 下方：观看区域
    draw_rounded_box(ax, 2.5, 0.5, 5.0, 0.8, "观看区域（视距 3~10m）",
                     fontsize=10, fontweight="bold",
                     fill_color="#EBF5FB", border_color="#2980B9")

    # 视距标注
    ax.annotate(
        "", xy=(5.0, 1.3), xytext=(5.0, 5.8),
        arrowprops=dict(arrowstyle="->", color="#85929E",
                        linestyle=":", linewidth=1.2)
    )
    ax.text(5.3, 3.5, "最佳视距\n≈ 屏高 × 2~4倍\nP1.5 约 3~6m",
            ha="left", va="center", fontsize=7.5,
            color="#566573", style="italic")

    # 适用场景标注（左下）
    ax.text(0.3, 0.7, "适用场景：\n· 指挥调度中心\n· 会议室与报告厅\n· 企业展厅与商业展示",
            ha="left", va="center", fontsize=7.5,
            color="#566573", style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="#F2F3F4", ec="#BDC3C7"))

    # 图例
    add_legend(ax, [
        (COLOR_MAIN, "-", "视频信号输入"),
        (COLOR_OUTPUT, "-", "显示驱动输出"),
        ("#F39C12", "-", "控制信号"),
    ])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "scene-indoor.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("✓ 生成 scene-indoor.png")


if __name__ == "__main__":
    print("正在生成室内 LED 显示屏产品图表...")
    draw_arch_system()
    draw_flow_display()
    draw_scene_indoor()
    print(f"\n所有图表已生成到: {OUTPUT_DIR}")
