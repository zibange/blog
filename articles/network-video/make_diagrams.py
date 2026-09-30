# -*- coding: utf-8 -*-
"""NVR产品资料架构图/链路图绘制（框线矢量图）
审核修正：
- pipeline：否分支补事件回调终点框(消除悬空)、是分支锚定菱形左角点、判定输入垂直对齐
- architecture：接入箭头落在"接入服务"模块而非NVR层中部、查看层箭头同轴对齐、报警线落点改模块主体
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D

os.makedirs(os.path.join(os.path.dirname(__file__), "images"), exist_ok=True)
OUT = os.path.join(os.path.dirname(__file__), "images")

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

G = "#2E8B57"   # 主流程 / 双向数据控制 绿
C = "#1F77B4"   # 输出 / 码流 青
R = "#C0392B"   # 报警 / 异常 红
O = "#E67E22"   # 判定 橙

def box(ax, x, y, w, h, text, face="#F4F7FA", edge="#34495E", fs=11, lw=1.6):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=3)

def arrow_bi(ax, p, q, color=G, label=None, lab_d=(0.0, 0.0), fs=9):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>", mutation_scale=16,
                 color=color, lw=1.8, zorder=2))
    if label:
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ax.text(mx + lab_d[0], my + lab_d[1], label, ha="center", va="center",
                fontsize=fs, color=color, zorder=4)

def arrow_one(ax, p, q, color=O, ls="-", lw=1.8, ms=15):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms,
                 color=color, linestyle=ls, lw=lw, zorder=2))

def elbow(ax, seg, color=R, ls="--", lw=1.8):
    xs = [p[0] for p in seg]; ys = [p[1] for p in seg]
    ax.plot(xs, ys, color=color, linestyle=ls, lw=lw, zorder=1)
    ax.add_patch(FancyArrowPatch(seg[-2], seg[-1], arrowstyle="-|>",
                 mutation_scale=14, color=color, linestyle=ls, lw=lw, zorder=2))

def layer_title(ax, x, y, t, color="#34495E", size=12.5):
    ax.text(x, y, t, ha="left", va="center", fontsize=size, fontweight="bold", color=color)

# ============ 图1 三端系统架构 ============
fig, ax = plt.subplots(figsize=(10.5, 8.0))
ax.set_xlim(0, 100); ax.set_ylim(-16, 100); ax.axis("off")

layer_title(ax, 2, 93, "前端采集层 · 网络摄像机（IPC）", G)
for i, t in enumerate(["IPC-1", "IPC-2", "IPC-N"]):
    box(ax, 8 + i * 26, 74, 22, 12, t, fs=12)
layer_title(ax, 2, 64, "网络传输层", "#7F8C8D")
box(ax, 8, 46, 84, 12, "PoE 交换机 / 局域网 / VPN-NAT 透传", fs=11.5)
layer_title(ax, 2, 36, "NVR 中心节点层", C, size=12)
for i, t in enumerate(["接入服务", "编码 · 存储", "录像检索 · 回放", "报警联动 · 云转发"]):
    box(ax, 2 + i * 24.5, 15, 23, 12, t, fs=10.5)
layer_title(ax, 2, 5, "管理与查看层", R)
for i, t in enumerate(["本地客户端", "手机 APP", "云平台"]):
    box(ax, 8 + i * 26, -8, 22, 11, t, fs=11)

# IPC -> 传输（绿色双向）
for i, xc in enumerate([19, 45, 71]):
    arrow_bi(ax, (xc, 74), (xc, 47.5),
             label=("主码流 / 控制" if i == 1 else None), lab_d=(0, 0.2))
# 传输 -> NVR 接入服务（垂直同轴，落点避开标题文字，落在模块内）
arrow_bi(ax, (22, 46), (22, 28), label="接入", lab_d=(3.2, 0))
# NVR -> 查看层（垂直同轴，各对齐目标模块中心）
arrow_bi(ax, (13.5, 15), (13.5, 3), label="实时预览", lab_d=(3.2, 0))
arrow_bi(ax, (38, 15), (38, 3), label="录像回放", lab_d=(0, 3.0))
arrow_bi(ax, (62.5, 15), (62.5, 3), label="录像上云 / 配置", lab_d=(0, 3.0))
# 报警联动 -> 手机APP（红色虚线，落点在模块下缘主体内，末端触边无悬空）
elbow(ax, [(90, 15), (90, -14), (48, -14), (48, -8)], color=R, ls="--")
ax.text(55, -13.2, "报警推送", ha="center", fontsize=9, color=R, zorder=4)

handles = [
    Line2D([0], [0], color=G, lw=2, label="音视频数据 / 控制信令（双向）"),
    Line2D([0], [0], color=R, lw=2, linestyle="--", label="报警事件推送（→ 手机APP）"),
]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.10),
          ncol=2, frameon=False, fontsize=9.5)
fig.savefig(os.path.join(OUT, "architecture.png"), dpi=160, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("architecture.png done")

# ============ 图2 录像处理链路 ============
fig, ax = plt.subplots(figsize=(11.5, 7.0))
ax.set_xlim(0, 128); ax.set_ylim(-18, 58); ax.axis("off")

steps = ["IPC\n采集", "网络接入\n(时间校准)", "解码预览\n主码流", "编码存储\n录像", "检索 · 回放", "报警 · 上云"]
xs = [4, 25, 46, 67, 88, 106]; w = 16; h = 12; y = 36
for i, t in enumerate(steps):
    face = "#EAF6EF" if i in (0, 3) else "#F4F7FA"
    box(ax, xs[i], y, w, h, t, fs=11, face=face)
for i in range(len(steps) - 1):
    arrow_one(ax, (xs[i] + w, y + h / 2), (xs[i + 1], y + h / 2), color=G, ls="-", lw=2.2)

# 菱形判定：满足写盘策略？
dx, dy = 75, 22
tri = [(dx - 8, dy + 4), (dx, dy), (dx + 8, dy + 4), (dx, dy - 4)]
ax.add_patch(Polygon(tri, closed=True, facecolor="#FFF7E6", edgecolor=O, lw=1.8, zorder=2))
ax.text(dx, dy, "满足写盘\n策略？", ha="center", va="center", fontsize=8.5, color="#8a5a00", zorder=3)
# 判定输入：从 编码存储 底部垂直（同轴）到菱形顶点
arrow_one(ax, (dx, y), (dx, dy + 4), color=O, ls="-", lw=1.8)

# 是 -> 写入磁盘（从菱形左角点正交引出）
box(ax, 22, -10, 30, 9, "硬盘写入（定时 / 移动侦测）", face="#EAF6EF", edge=C, fs=9.5)
elbow(ax, [(dx - 8, dy), (37, dy), (37, -1)], color=C, ls="--")
ax.text(52, dy + 1.8, "是 · 写入磁盘", ha="center", fontsize=9, color=C, zorder=4)

# 否 -> 事件回调（从菱形右角点正交引出，落到终点框，不悬空）
box(ax, 97, -10, 26, 9, "事件回调 · 上报平台（不落盘）", face="#FBF0EF", edge=R, fs=8.5)
elbow(ax, [(dx + 8, dy), (110, dy), (110, -1)], color=R, ls="--")
ax.text(89, dy + 1.8, "否 · 事件回调不落地", ha="center", fontsize=9, color=R, zorder=4)

handles = [
    Line2D([0], [0], color=G, lw=2, label="主流程（码流处理主干）"),
    Line2D([0], [0], color=O, lw=2, label="存储策略判定"),
    Line2D([0], [0], color=C, lw=2, linestyle="--", label="是：写入磁盘（定时 / 移动侦测）"),
    Line2D([0], [0], color=R, lw=2, linestyle="--", label="否：事件回调 · 不落盘"),
]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.06),
          ncol=4, frameon=False, fontsize=9.5)
fig.savefig(os.path.join(OUT, "pipeline.png"), dpi=160, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("pipeline.png done")