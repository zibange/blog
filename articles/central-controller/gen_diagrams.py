# -*- coding: utf-8 -*-
"""
智能中控网关 结构图生成（v2）
遵循 smart-hardware-product-doc 链路规范：
- 判定分支用正交三段折线
- 主流程=绿色实线, 结果=青色虚线, 异常/回流=红色虚线
- 双向箭头留间隙并双箭头头
- 底部统一等距文字图例（不用Unicode箭头字形）
修复：图例等距横排防重叠；层标题与模块分离防文字竞争；判定分支严格正交
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

OUT = r"d:\AiPython\zhinengshebei\智能中控网关\images"
DPI = 220

C_MAIN  = "#1F9E6A"
C_RES   = "#11A8D8"
C_ERR   = "#E0526E"
C_SYS   = "#2E5BFF"
C_EDGE  = "#F4A825"
C_TXT   = "#1B2430"
BOX_FACE = "#FFFFFF"


def box(ax, x, y, w, h, text, fc=BOX_FACE, ec=C_SYS, tc=C_TXT,
        lw=1.6, fs=11, rounded=False, bold=False, z=3):
    if rounded:
        b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.1",
                           linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z)
    else:
        b = Rectangle((x, y), w, h, linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=z+1, weight="bold" if bold else "normal")


def arrow(ax, p0, p1, style="-|>", color=C_MAIN, lw=2.0, ls="solid",
          scale=20, shrinkA=2, shrinkB=2):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=scale,
                        linewidth=lw, color=color, linestyle=ls,
                        shrinkA=shrinkA, shrinkB=shrinkB, zorder=5)
    ax.add_patch(a)


def ortho(ax, pts, color=C_MAIN, lw=2.0, ls="solid", scale=20):
    """正交折线入箭头：pts 为折点序列，最后一段带箭头。"""
    if len(pts) < 2:
        return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs[:-1], ys[:-1], color=color, lw=lw, ls=ls, zorder=4)
    arrow(ax, pts[-2], pts[-1], style="-|>", color=color, lw=lw, ls=ls, scale=scale)


def legend(ax, x0, x1, y, items):
    """items: list of (color, ls, label)。等距横排防重叠。"""
    n = len(items)
    per = (x1 - x0) / n
    for i, (c, ls, label) in enumerate(items):
        cx = x0 + i*per + per/2
        sx = cx - 0.62
        ax.plot([sx, sx+0.24], [y, y], color=c, lw=2.6, ls=ls, solid_capstyle="round", zorder=4)
        ax.plot(sx+0.22, y, marker=">", color=c, markersize=9, zorder=5)
        ax.text(sx+0.34, y, label, fontsize=10, color="#42506A", va="center", zorder=4)


def finish(fig, ax, path, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("saved", path)


# ============================================================
# 图1 端边云三层部署架构 arch-system.png
# ============================================================
def arch_system():
    fig, ax = plt.subplots(figsize=(11, 9.0))
    xlim, ylim = (0, 12), (0, 9)

    # 通用：每层级 = 容器框 + 左侧标题竖条 + 右侧模块框(与 arch-gateway 一致防重叠)
    # —— 云平台层 ——
    box(ax, 0.3, 7.55, 11.4, 1.5, "", fc="#EEF4FF", ec=C_SYS, lw=2.0)
    box(ax, 0.4, 7.68, 1.7, 1.24, "云\n端\n平\n台", fc="#F2F3F7", ec=C_SYS, fs=11, bold=True)
    cloud = ["数据中台\n汇聚存储", "场景编排\n远程下发", "开放 API\n系统集成", "远程运维\n告警与工单"]
    cw, cgap, x0 = 2.35, 0.24, 2.32
    for i, t in enumerate(cloud):
        box(ax, x0 + i*(cw+cgap), 7.85, cw, 0.9, t, ec="#7D96D8", fs=10.5)

    # —— 边缘接入层 ——
    box(ax, 0.3, 5.05, 11.4, 2.0, "", fc="#FFF6E6", ec=C_EDGE, lw=2.0)
    box(ax, 0.4, 5.3, 1.7, 1.5, "边\n缘\n接\n入", fc="#FDF3DD", ec=C_EDGE, fs=11, bold=True)
    box(ax, 2.35, 5.4, 2.35, 1.3, "智能中控网关\n边缘侧本地控制", ec=C_EDGE, fs=10.5, bold=True)
    gw = ["多协议解析\nModbus/BACnet/KNX", "边缘计算\n清洗·聚合·规则", "本地联动\n断网自主决策", "断点续传\n离线缓存回补"]
    gx = 5.0
    for i, t in enumerate(gw):
        box(ax, gx + i*1.72, 5.5, 1.56, 1.1, t, ec=C_EDGE, fs=9.3)
    ax.text(11.5, 5.18, "就地部署于弱电间 / 控制柜", ha="right", fontsize=9, color="#B57908")

    # —— 设备感知执行层 ——
    box(ax, 0.3, 2.05, 11.4, 1.5, "", fc="#EEFBF3", ec="#1F9E6A", lw=2.0)
    box(ax, 0.4, 2.18, 1.7, 1.24, "感\n知\n执\n行", fc="#E6F5EC", ec="#1F9E6A", fs=11, bold=True)
    dev = ["照明 / 调光", "暖通空调\nHVAC", "门禁 / 梯控", "环境 / 能耗\n传感计量", "窗帘遮阳", "其他 485 设备"]
    dw, dgap, dx0 = 1.50, 0.20, 2.32
    dev_c = []
    for i, t in enumerate(dev):
        cx = dx0 + i*(dw+dgap)
        dev_c.append(cx + dw/2)
        box(ax, cx, 2.35, dw, 0.9, t, ec="#569E76", fs=9.2)

    # —— 跨层双向箭头（空白带，留间隙）——
    for cx in [3.0, 6.0, 9.0]:
        arrow(ax, (cx, 7.32), (cx, 7.1), style="<->", color=C_SYS, lw=2.0)
    ax.text(9.6, 7.3, "数据上行 /\n指令下行", fontsize=8.5, color="#5A6B9A", ha="left")

    for cx in [3.0, 6.0, 9.0]:
        arrow(ax, (cx, 4.82), (cx, 4.02), style="<->", color=C_MAIN, lw=2.0)
    ax.text(9.6, 4.55, "总线汇聚\n上行 / 下行", fontsize=8.5, color="#33607A", ha="left")
    ax.text(6.0, 4.86, "RS485 / KNX / Zigbee / 以太网", ha="center", fontsize=9, color="#33607A")

    legend(ax, 0.5, 8.0, 0.72, [
        (C_MAIN, "solid", "主流程 / 上行采集"),
        (C_RES, "dashed", "结果 / 响应下行"),
        (C_SYS, "solid", "层级与模块框")])
    ax.text(6.0, 0.3, "图注：端 — 边 — 云三层部署架构（示意，设备与协议项可扩展）",
            ha="center", fontsize=10.5, color="#667085")
    finish(fig, ax, OUT + r"\arch-system.png", xlim, ylim)


# ============================================================
# 图2 网关内部模块架构 arch-gateway.png
# ============================================================
def arch_gateway():
    fig, ax = plt.subplots(figsize=(11, 9.2))
    xlim, ylim = (0, 12), (0, 11)

    # 每层：标题竖条(x0.4..2.1) + 模块区(x2.3..8.6)
    layers = [
        ("北向\n接入", ["MQTT", "HTTP / REST", "OPC UA", "BACnet/IP"], "#7D96D8", 8.2, 10.0),
        ("边缘\n计算", ["规则引擎\n本地联动", "数据清洗\n过滤去重", "聚合 / 时标\n边缘统计", "断点缓存\n离线续传"], C_EDGE, 6.0, 7.8),
        ("协议\n解析", ["Modbus\nRTU/TCP", "BACnet\nMS/TP / IP", "KNX /\nTP", "Zigbee /\nLoRaWAN", "DALI /\nM-Bus"], "#569E76", 3.8, 5.6),
        ("硬件\n接口", ["RS485 / RS232\n多路串口", "以太网\nWAN / LAN", "KNX / TP1\n总线口", "USB /\n调试口"], "#7C8499", 1.6, 3.4),
    ]
    tab_w = 1.7
    for title, items, ec, y0, y1 in layers:
        box(ax, 0.4, y0, tab_w, y1-y0, title, fc="#F2F3F7", ec=ec, fs=11, bold=True)
        area_x, area_w = 2.3, 6.3
        n = len(items)
        iw = area_w / n
        for i, t in enumerate(items):
            ix = area_x + i*iw + 0.10
            box(ax, ix, y0 + 0.35, iw - 0.20, y1-y0 - 0.70, t, ec=ec, fs=9.4)

    # 层间双向箭头（空白带）
    arrows = [(7.8, 8.2), (5.6, 6.0), (3.4, 3.8)]
    for (y0, y1) in arrows:
        arrow(ax, (2.0, y0+0.05), (2.0, y1-0.05), style="<->", color=C_MAIN, lw=2.0, scale=22)
    ax.text(1.15, 6.7, "上行 /\n下行", fontsize=9, color=C_MAIN, ha="center")

    # 右侧安全与运维
    box(ax, 9.0, 1.6, 2.6, 8.4, "", fc="#FDF2F4", ec=C_ERR, lw=1.8)
    ax.text(10.3, 9.15, "安全与运维", ha="center", fontsize=11.5, color=C_ERR, weight="bold")
    sec = ["双向 TLS\n传输加密", "设备证书\n双向认证", "访问控制\n分级授权", "日志审计\n本地留存", "远程升级\n看门狗复位"]
    sec_y = [8.1, 6.3, 4.5, 2.7, 1.7]
    for t, sy in zip(sec, sec_y):
        box(ax, 9.15, sy, 2.3, 0.72, t, ec=C_ERR, fs=9.4)

    # 安全链路 红色虚线（右侧吸入）
    for y in [9.3, 7.1, 4.9, 2.7]:
        arrow(ax, (8.6, y), (9.0, y), style="-|>", color=C_ERR, lw=1.7, ls="dashed")

    box(ax, 0.5, 0.72, 8.0, 0.55, "底部供电：DC 12–48V 宽压输入 · 冗余电源 · DIN 导轨安装",
        fc="#F7F8FB", ec="#9AA3B5", fs=10, rounded=True)
    legend(ax, 0.5, 11.6, 0.2, [
        (C_MAIN, "solid", "主流程（上行/下行）"),
        (C_ERR, "dashed", "安全 / 运维接入")])
    finish(fig, ax, OUT + r"\arch-gateway.png", xlim, ylim)


# ============================================================
# 图3 数据上行链路 flow-uplink.png
# ============================================================
def flow_uplink():
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    xlim, ylim = (0, 12), (0, 4.6)

    steps = [
        "采集触发\n周期 / 订阅回调", "驱动执行\n读写 + 解析", "统一点位值\n事件化",
        "边缘计算\n过滤·聚合", "北向编码\nMQTT 上报", "云平台\n数据中台落地",
    ]
    tags = ["感知采集", "协议解析", "数据建模", "边缘计算", "北向接入", "云端落地"]
    w, h = 1.72, 1.05
    xs = [0.35 + i*(w+0.26) for i in range(len(steps))]
    for i, (lab, tag) in enumerate(zip(steps, tags)):
        ec = C_RES if i == 5 else C_SYS
        box(ax, xs[i], 2.0, w, h, lab, ec=ec, fs=9.6)
        ax.text(xs[i]+w/2, 1.76, tag, ha="center", fontsize=10, color="#7790C0")
    for i in range(len(steps)-1):
        arrow(ax, (xs[i]+w+0.0, 2.53), (xs[i+1]-0.0, 2.53), style="-|>", color=C_MAIN, lw=2.4)
    ax.text(2.4, 3.55, "数据上行：现场点位 → 协议解析 → 边缘计算 → 云端",
            fontsize=12, color=C_TXT, weight="bold")

    box(ax, 0.55, 0.45, 5.0, 0.85, "网络中断：数据本地缓存，恢复后按序回补",
        fc="#F0FAFF", ec=C_RES, fs=9.8)
    arrow(ax, (3.0, 1.32), (3.0, 1.62), style="<->", color=C_RES, lw=1.8, ls="dashed")

    legend(ax, 6.4, 11.9, 0.86, [
        (C_MAIN, "solid", "主流程数据流"),
        (C_RES, "dashed", "断点续传 / 补报")])
    finish(fig, ax, OUT + r"\flow-uplink.png", xlim, ylim)


# ============================================================
# 图4 下行控制链路 flow-downlink.png（严格正交判定分支）
# ============================================================
def flow_downlink():
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    xlim, ylim = (0, 12), (0, 6.0)

    yrow = 3.2
    def prow(x, t, ec=C_SYS):
        box(ax, x, yrow, 1.8, 1.0, t, ec=ec, fs=9.6)

    prow(0.3, "云平台\n下发指令")
    prow(2.6, "网关\n鉴权 / 校验", ec=C_SYS)
    prow(4.9, "定位目标设备\n查点表 / 寻址")
    prow(7.2, "驱动写入\n协议封装分发")
    prow(9.5, "末端设备\n执行动作")

    # 判定菱形：中心(4.5,2.05)，水平半宽1.0，垂直半高0.78
    d_cx, d_cy = 4.5, 2.05
    hx, hy = 1.0, 0.78
    top, bottom = (d_cx, d_cy+hy), (d_cx, d_cy-hy)
    left, right = (d_cx-hx, d_cy), (d_cx+hx, d_cy)
    ax.add_patch(Polygon([top, right, bottom, left], closed=True,
                         ec=C_SYS, fc="#FFF6E6", lw=1.8, zorder=3))
    ax.text(d_cx, d_cy, "鉴权通过？", ha="center", va="center", fontsize=10)

    # 主链 A→B（绿色实线）；B→判定（绿色正交三段折线）
    arrow(ax, (2.1, 3.7), (2.6, 3.7), style="-|>", color=C_MAIN, lw=2.4)
    ortho(ax, [(3.5, 3.2), (3.5, 2.9), (d_cx, 2.9), top], C_MAIN, 2.2, "solid")

    # 通过→C（青色虚线正交：从菱形右侧向上→右→上入C底）
    ortho(ax, [right, (right[0], 2.78), (5.8, 2.78), (5.8, 3.2)], C_RES, 2.0, "dashed")
    ax.text(5.66, 2.32, "通过 →\n继续分发", fontsize=8.5, color=C_RES, va="center")

    # 未通过→拒绝（红色虚线正交，指向告警框）
    box(ax, 2.4, 0.35, 4.2, 0.62, "未通过 → 拒绝并回执告警\n（鉴权失败 / 指令非法）",
        fc="#FDF1F3", ec=C_ERR, fs=9.2)
    ortho(ax, [bottom, (d_cx, 1.03)], C_ERR, 2.0, "dashed")

    # C→D→E
    arrow(ax, (6.7, 3.7), (7.2, 3.7), style="-|>", color=C_MAIN, lw=2.4)
    arrow(ax, (9.0, 3.7), (9.5, 3.7), style="-|>", color=C_MAIN, lw=2.4)

    # 结果回传（青色虚线, 顶部走廊）
    ortho(ax, [(10.4, 4.2), (10.4, 4.8), (1.2, 4.8), (1.2, 4.2)], C_RES, 1.8, "dashed")
    ax.text(5.6, 4.62, "执行结果 / 状态回传（控制闭环）", ha="center", fontsize=9.6, color=C_RES)

    legend(ax, 2.6, 10.9, 0.14, [
        (C_MAIN, "solid", "主流程"),
        (C_RES, "dashed", "判定结果 / 状态回传"),
        (C_ERR, "dashed", "异常 / 回执告警")])
    ax.text(6.0, 5.58, "下行控制：平台指令 → 鉴权 → 寻址分派 → 设备执行 → 结果回传，形成闭环",
            ha="center", fontsize=11.5, color=C_TXT, weight="bold")
    finish(fig, ax, OUT + r"\flow-downlink.png", xlim, ylim)


arch_system()
arch_gateway()
flow_uplink()
flow_downlink()
print("ALL DIAGRAMS DONE")