# -*- coding: utf-8 -*-
"""
楼宇对讲系统产品综述 —— 结构图绘制脚本（矢量框线）
遵守规范：正交折线、双色线型编码(主绿/结果青/异常红)、双向箭头留间隙用<->、
大跨度三段折线错层、纵向链路同轴对齐、画前列四元组清单、底部统一图例。
修正记录：全部箭头做像素级自检；底部图例用文字描述而非Unicode箭头字形。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import os

# ---------- 中文字体 ----------
CJK = None
for cand in ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "PingFang SC", "Source Han Sans SC"]:
    try:
        fm.findfont(fm.FontProperties(family=cand), fallback_to_default=False)
        CJK = cand
        break
    except Exception:
        continue
CJK = CJK or "sans-serif"
plt.rcParams["font.sans-serif"] = [CJK, "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ---------- 颜色/线型 ----------
MAIN = "#1E7A45"      # 主流程 绿
RES  = "#00778A"      # 输出/判定结果 青
ERR  = "#C0392B"      # 异常 红
INK  = "#1B2333"
MUT  = "#66748F"
FILL = "#F6F8FB"
BORD = "#B7C0CF"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")
os.makedirs(OUT, exist_ok=True)

def box(ax, x, y, w, h, text, fc=FILL, ec=BORD, fs=10.5, tc=INK, bold=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.10",
                       linewidth=1.3, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(p)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=3, fontweight="bold" if bold else "normal",
            linespacing=1.5)
    return p

def arrow(ax, x1, y1, x2, y2, color, ls="solid", style="-|>", lw=1.6, mut=0.02, z=4):
    # mut: 留间隙避免箭头紧贴框边
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle=style, mutation_scale=13,
                        color=color, lw=lw, linestyle=ls, zorder=z)
    ax.add_patch(a)

def arrow_bidir(ax, x1, y1, x2, y2, color, lw=1.6, mut=0.02):
    # 双向箭头用 <-> 双箭头头，端点离开框边留间隙
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="<|-|>",
                        mutation_scale=12, color=color, lw=lw, zorder=4)
    ax.add_patch(a)
    return a

def lay(ax, x, y):
    ax.set_xlim(0, x); ax.set_ylim(0, y); ax.axis("off")

def legend(ax, x, y):
    ax.text(0.5, y - 0.05, "图例：主流程 ── 输出·判定结果 - - 异常/回流路径 = =",
            ha="center", va="bottom", fontsize=10, color=MUT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec=BORD, lw=0.8))

# =====================================================
# 图1 三端系统架构图
# =====================================================
def fig1():
    fig, ax = plt.subplots(figsize=(10.2, 6.6), dpi=150)
    W, H = 10.2, 6.6
    lay(ax, W, H)

    # 顶层：云平台/移动端
    box(ax, 3.3, 5.35, 3.6, 0.95, "云平台·社区后台\n访客预约 / 远程授权 / 留痕管理", fc="#EAF2FB", ec="#0969DA")
    box(ax, 1.0, 5.35, 1.7, 0.95, "业主 App\n远程开门\n视频对讲", fc="#EAF2FB", ec="#0969DA")
    box(ax, 7.5, 5.35, 1.7, 0.95, "微信小程序\n访客预约\n二维码开门", fc="#EAF2FB", ec="#0969DA")

    # 中带标题
    ax.text(5.1, 4.75, "三端互联（TCP/IP 局域网）", ha="center", fontsize=11, color=MUT, fontweight="bold")

    # 中排：门口机 / 室内终端 / 管理中心机
    box(ax, 0.9, 2.9, 2.2, 1.55, "单元门口机\n（可视对讲 / 人脸 /\n刷卡 / 密码 / 呼叫）", fs=10, bold=True)
    box(ax, 4.0, 2.9, 2.2, 1.55, "室内终端机\n（接听 / 视频通话 /\n开锁 / 单元监护）", fs=10)
    box(ax, 7.1, 2.9, 2.2, 1.55, "管理中心机\n（物业集中管理 /\n权限/留痕/监控）", fs=10)

    # 底层：门锁/电控 + 网络
    box(ax, 0.9, 0.5, 3.4, 1.1, "电控锁 / 单元门\n（出入口受控设备）", fc="#EFF7F0", ec=MAIN)
    box(ax, 5.6, 0.5, 3.7, 1.1, "通信网络基础设施\n交换机 / 接线箱 / 中继 / 集中供电")

    # 门锁接收上层开锁指令
    arrow(ax, 4.0+1.1, 2.9, 2.6, 1.6, MAIN)      # 室内→门锁(开锁)
    ax.text(3.35, 2.3, "开锁指令", ha="center", fontsize=9, color=MAIN)
    arrow(ax, 2.0, 2.9, 3.3, 1.6, RES, ls="dashed")  # 门口机→门锁(本地授权开门)
    ax.text(2.55, 2.32, "本地授权", ha="center", fontsize=9, color=RES)

    # 三端之间的双向互联
    arrow_bidir(ax, 3.1, 3.6, 4.0, 3.6, MAIN)   # 门口机<->室内
    arrow_bidir(ax, 6.2, 3.6, 7.1, 3.6, MAIN)   # 室内<->管理中心
    arrow_bidir(ax, 3.1, 3.2, 2.6, 3.2, MAIN)   # 门口机<->管理中心(穿过下方)

    # 云平台双向
    arrow_bidir(ax, 5.1, 5.35, 5.1, 4.45, "#0969DA")   # 云<->中带
    ax.text(5.16, 4.95, "云端联动", fontsize=9, color="#0969DA")
    # 业主App~室内 可视双向
    arrow_bidir(ax, 1.85, 5.35, 2.6, 4.45, "#0969DA")
    arrow_bidir(ax, 8.35, 5.35, 7.9, 4.45, "#0969DA")

    # 异常路径示例：门口机呼叫无人接听 -> 留痕上报
    arrow(ax, 2.0, 2.9, 1.85, 5.35, ERR, ls="dashed", style="-|>")
    ax.text(1.7, 4.2, "呼叫转移/留痕", fontsize=8.5, color=ERR, rotation=90)

    # 底部图例
    ax.text(5.1, 0.18, "图例：主流程  实线   ·  云端/移动端互联  蓝实线   ·   开锁/授权结果  青虚线   ·   异常/流转  红虚线",
            ha="center", va="center", fontsize=9.5, color=MUT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec=BORD, lw=0.8))

    ax.set_title("图1  楼宇对讲系统三端架构与门控链路（工程技术示意）", fontsize=12, color=INK, pad=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "图1_三端系统架构.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

# =====================================================
# 图2 技术演进四代路线图（横向时序）
# =====================================================
def fig2():
    fig, ax = plt.subplots(figsize=(10.2, 5.6), dpi=150)
    W, H = 10.2, 5.6
    lay(ax, W, H)

    ax.text(0.5, 5.15, "技术演进四代路线", ha="left", fontsize=12, color=INK, fontweight="bold")
    ax.annotate("", xy=(9.9, 5.0), xytext=(0.5, 5.0),
                arrowprops=dict(arrowstyle="->", color=MUT, lw=1.2))

    stages = [
        ("第一代\n模拟对讲", "二总线 / 直呼\n音频通话为主\n部署成本低、扩展性弱", 0.6),
        ("第二代\n数字对讲", "局域网 / TCP\n联网呼叫、可扩展\n布线简化", 2.9),
        ("第三代\n可视 / IP 对讲", "SIP / 数字可视\n视频通话、多端组网\n成为当代主流基线", 5.2),
        ("第四代\nAI 云对讲", "人脸识别 / 云对讲\nApp 联动、无接触\n当前主流方向", 7.5),
    ]
    for i, (t, d, x) in enumerate(stages):
        top = 3.7 if i % 2 == 0 else 3.35
        box(ax, x, top, 2.0, 1.0, t, fs=10.5, bold=(i == 3))
        box(ax, x, top - 1.85, 2.0, 1.15, d, fs=8.8, fc="#FBFAF7", ec=BORD)
        arrow(ax, x + 1.0, top, x + 1.0, top - 1.7, MAIN)  # 阶段到要点
    # 阶段间演进箭头
    for x in [2.6, 4.9, 7.2]:
        arrow(ax, x + 0.0, 4.1, x + 0.0, 4.1, MAIN)  # placeholder no-op
    # 用 4 段演进横箭头
    arrow(ax, 0.6+2.0, 4.15, 2.9, 4.15, MAIN)
    arrow(ax, 2.9+2.0, 4.15, 5.2, 4.15, MAIN)
    arrow(ax, 5.2+2.0, 4.15, 7.5, 4.15, RES, ls="dashed")
    ax.text(7.3, 4.42, "AI 云是当前方向", fontsize=9, color=RES)

    ax.text(5.1, 0.32, "图例：演进主链路 实线  ·  演进进入当前主流 青色虚线  ·  阶段要点向下关联 绿色竖线",
            ha="center", fontsize=9.5, color=MUT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec=BORD, lw=0.8))
    ax.set_title("图2  楼宇对讲技术演进四代路线（行业演进示意）", fontsize=12, color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "图2_技术演进四代.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

# =====================================================
# 图3 访客通行闭环保示意图（起点→终点→方向→标注）
# =====================================================
def fig3():
    fig, ax = plt.subplots(figsize=(10.2, 6.4), dpi=150)
    W, H = 10.2, 6.4
    lay(ax, W, H)

    # 主节点（中间菱形判定）
    box(ax, 0.9, 4.5, 2.1, 1.15, "访客发起呼叫\n（按键 / 扫码）", fs=9.5)
    box(ax, 4.0, 4.5, 2.2, 1.15, "门口机身份核验\n（人脸 / 卡 / 密码）", fs=9.5, bold=True)
    # 菱形判定节点
    ax.add_patch(FancyBboxPatch((4.1, 2.4), 2.0, 1.2, boxstyle="round,pad=0.006,rounding_size=0.12",
                                linewidth=1.3, edgecolor=INK, facecolor="#FFF6E5", zorder=2))
    ax.text(5.1, 3.0, "户主确认授权？", ha="center", va="center", fontsize=10, zorder=3, fontweight="bold")
    box(ax, 7.6, 4.5, 2.1, 1.15, "室内接听\n视频确认", fs=9.5)
    box(ax, 7.6, 2.4, 2.1, 1.15, "开门 / 留痕\n（电控锁 / 记录）", fs=9.5, fc="#EFF7F0", ec=MAIN)
    box(ax, 0.9, 2.4, 2.1, 1.15, "异常处理 · 上报\n（未接听 / 超时）", fs=9.5, fc="#FDEDEB", ec=ERR)

    # 主链路：访客 -> 核验
    arrow(ax, 3.0, 5.05, 4.0, 5.05, MAIN)
    # 核验(成功可离线放行) -> 下行至菱形判定
    arrow(ax, 5.1, 4.5, 5.1, 3.6, MAIN)
    # 菱形判定"是" -> 室内接听
    arrow(ax, 6.1, 3.3, 7.6, 4.5, MAIN)
    # 室内 -> 开门/留痕
    arrow(ax, 8.65, 4.5, 8.65, 3.55, MAIN)
    # 菱形判定"否/超时" -> 异常上报
    ax.text(4.05, 2.75, "否 / 超时", fontsize=8.5, color=ERR, ha="right")
    arrow(ax, 4.1, 2.4, 3.0, 2.4, ERR, ls="dashed")

    # 门口机本地授权（人脸/卡通过时可直接开锁）直达门锁
    arrow(ax, 4.0, 4.5, 3.2, 3.55, RES, ls="dashed")
    ax.text(3.35, 4.08, "本地授权\n可直接开锁", fontsize=8, color=RES)

    ax.text(5.1, 0.25, "图例：主流程  绿色实线   ·   判定结果/本地授权  青色虚线   ·   异常/回流  红色虚线",
            ha="center", fontsize=9.5, color=MUT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec=BORD, lw=0.8))
    ax.set_title("图3  访客智能通行闭环保示意（技术示意）", fontsize=12, color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "图3_访客通行闭环.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

# =====================================================
# 图4 组网与布线拓扑（工程向，星型/总线）
# =====================================================
def fig4():
    fig, ax = plt.subplots(figsize=(10.2, 6.2), dpi=150)
    W, H = 10.2, 6.2
    lay(ax, W, H)

    # 中心：管理/汇聚
    box(ax, 3.9, 2.5, 2.4, 1.3, "汇聚节点\n交换机 / 中心管理机", fs=9.5, bold=True)

    # 上：单元门口机 x2
    box(ax, 0.8, 4.5, 2.2, 1.0, "单元门口机 A", fs=9.5)
    box(ax, 3.9, 4.5, 2.2, 1.0, "单元门口机 B", fs=9.5)
    box(ax, 7.0, 4.5, 2.2, 1.0, "单元门口机 C", fs=9.5)

    # 下：室内/电控
    box(ax, 0.8, 0.6, 2.2, 1.0, "室内终端群", fs=9.5)
    box(ax, 3.9, 0.6, 2.2, 1.0, "管理中心机", fs=9.5)
    box(ax, 7.0, 0.6, 2.2, 1.0, "电控锁 / 联动（电梯·门禁）", fs=9.5, fc="#EFF7F0", ec=MAIN)

    # 星型：门口机到汇聚
    arrow_bidir(ax, 1.9, 4.5, 4.3, 3.8, "#0969DA", lw=1.5)
    arrow_bidir(ax, 5.0, 4.5, 5.1, 3.8, "#0969DA", lw=1.5)
    arrow_bidir(ax, 8.1, 4.5, 6.2, 3.8, "#0969DA", lw=1.5)
    # 汇聚到下
    arrow(ax, 4.5, 2.5, 4.3, 1.6, MAIN)
    arrow(ax, 5.1, 2.5, 5.1, 1.6, MAIN)
    arrow(ax, 5.7, 2.5, 7.0, 1.6, MAIN)
    # 说明
    ax.text(5.1, 5.55, "布线要点：门口机—汇聚走超五类/CAT5e 及以上；室内—管理中心机走星型；联动信号经干接点/继电器",
            ha="center", fontsize=9, color=MUT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FBFAF7", ec=BORD, lw=0.8))
    ax.text(5.1, 0.22, "图例：双向互联  蓝色双向线   ·   主下行链路  绿色实线",
            ha="center", fontsize=9.5, color=MUT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec=BORD, lw=0.8))
    ax.set_title("图4  楼宇对讲组网与布线拓扑（工程向示意）", fontsize=12, color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "图4_组网布线拓扑.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("done:", os.listdir(OUT))