# -*- coding: utf-8 -*-
"""
用 reportlab 把《楼宇对讲系统技术综述.md》渲染为 PDF。
轻量解析 Markdown 常用结构：# / ## / ### 标题、段落、- / 数字 列表、| 表格、![] 图片、[x]清单。
中文字体：微软雅黑。
"""
import re, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, ListFlowable, ListItem)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

BASE = r"d:\AiPython\zhinengshebei\楼宇对讲系统"
MD = os.path.join(BASE, "楼宇对讲系统技术综述.md")
OUT = os.path.join(BASE, "楼宇对讲系统技术综述.pdf")

pdfmetrics.registerFont(TTFont("CJK", r"C:\Windows\Fonts\msyh.ttc"))
registerFontFamily("CJK", normal="CJK", bold="CJK", italic="CJK", boldItalic="CJK")

INK = colors.HexColor("#1B2333")
MUT = colors.HexColor("#66748F")
ACC = colors.HexColor("#0969DA")
RULE = colors.HexColor("#D9E0EC")
BG2 = colors.HexColor("#F6F8FB")

S_H1 = ParagraphStyle("h1", fontName="CJK", fontSize=18, leading=26, textColor=INK,
                      spaceBefore=14, spaceAfter=8, alignment=TA_LEFT)
S_H2 = ParagraphStyle("h2", fontName="CJK", fontSize=15, leading=22, textColor=ACC,
                      spaceBefore=16, spaceAfter=8)
S_H3 = ParagraphStyle("h3", fontName="CJK", fontSize=12.5, leading=18, textColor=colors.HexColor("#38435A"),
                      spaceBefore=10, spaceAfter=6)
S_P = ParagraphStyle("p", fontName="CJK", fontSize=10.5, leading=17, textColor=INK, spaceAfter=6)
S_LEAD = ParagraphStyle("lead", fontName="CJK", fontSize=11.5, leading=19, textColor=colors.HexColor("#38435A"),
                        spaceAfter=8, leftIndent=8, borderWidth=0, borderPadding=0)
S_CAP = ParagraphStyle("cap", fontName="CJK", fontSize=8.5, leading=12, textColor=MUT,
                       alignment=TA_CENTER, spaceAfter=10, spaceBefore=2)
S_ITEM = ParagraphStyle("item", fontName="CJK", fontSize=10.5, leading=16, textColor=INK)
S_CELL = ParagraphStyle("cell", fontName="CJK", fontSize=9, leading=13, textColor=INK)
S_CELLH = ParagraphStyle("cellh", fontName="CJK", fontSize=9, leading=13, textColor=colors.HexColor("#38435A"))

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") \
            .replace("**", "").replace("##", "").replace("#","")

def par(s):
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*([^*]+?)\*", r"<i>\1</i>", s)
    return Paragraph(s, S_P)

def parse_table(rows):
    heads = [esc(c.strip()) for c in rows[0] if c.strip()]
    data = []
    for r in rows[1:]:
        data.append([Paragraph(esc(c.strip()) or "—", S_CELL) for c in r])
    t = Table([ [Paragraph(h, S_CELLH) for h in heads] ] + data, colWidths=None)
    t.setStyle(TableStyle([
        ("FONTNAME",(0,0),(-1,-1),"CJK"),
        ("BACKGROUND",(0,0),(-1,0),BG2),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#38435A")),
        ("GRID",(0,0),(-1,-1),0.5,RULE),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#FBFCFD")]),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    return t

def build():
    with open(MD, encoding="utf-8") as f:
        lines = f.read().split("\n")

    story = []
    # 首页嵌入式封面（横版 16:9 图，全页宽）
    _cover = os.path.join(BASE, "assets", "cover.png")
    if os.path.exists(_cover):
        try:
            cimg = Image(_cover, width=174*mm, height=174*mm*0.5625)
            cimg.hAlign = "CENTER"
            story.append(cimg)
            story.append(Spacer(1, 4))
            story.append(Paragraph("楼宇对讲系统技术综述 · 面向工程端", S_H1))
            story.append(Paragraph("AI 概念示意图封面，用于版式呈现（非实证图）。", S_CAP))
            story.append(Spacer(1, 4))
        except Exception:
            pass
    temp_table_rows = []
    in_table = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        # front matter 封面块引用忽略 > 封面
        if line.startswith("> 封面图"):
            i += 1; continue
        if line.startswith(">"):
            i += 1; continue
        # 表格识别
        if line.startswith("|") and ("|" in line[1:]):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c.strip()):
                in_table = True; i += 1; continue
            if in_table:
                temp_table_rows.append([c for c in cells])
            else:
                temp_table_rows = [cells]
                in_table = True
            # 表格结束判断：下一行非 | 收集
        else:
            if in_table and temp_table_rows and len(temp_table_rows) > 1:
                story.append(Spacer(1,4)); story.append(parse_table(temp_table_rows)); story.append(Spacer(1,8))
                temp_table_rows = []; in_table = False
            # 图片
            m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if m:
                alt, rel = m.group(1), m.group(2)
                path = os.path.join(BASE, rel.replace("/", os.sep))
                if os.path.exists(path):
                    try:
                        img = Image(path, width=150*mm, height=150*mm*0.9)
                        img.hAlign = "CENTER"
                        story.append(img)
                    except Exception:
                        story.append(par(f"[图 {alt}]"))
                # 图注在下一行（加粗），由下方标题逻辑处理
                i += 1
                if i < len(lines) and lines[i].strip().startswith("**图"):
                    story.append(S_CAP and Paragraph(esc(lines[i].replace("**","")), S_CAP))
                i += 1; continue
            # 标题
            if line.startswith("###"):
                story.append(Paragraph(esc(line[3:].strip()), S_H3))
            elif line.startswith("##"):
                story.append(Paragraph(esc(line[2:].strip()), S_H2))
            elif line.startswith("#"):
                story.append(Paragraph(esc(line[1:].strip()), S_H1))
            # 清单 check
            elif re.match(r"^\- \[.*\]", line):
                txt = esc(re.sub(r"^\- \[x?\]\s*", "", line))
                story.append(ListFlowable([ListItem(Paragraph(txt+"  ✓", S_ITEM),
                                                   leftIndent=6)], bulletType="bullet", bulletColor=colors.HexColor("#2DA44E")))
            # 列表
            elif re.match(r"^\- ", line):
                txt = esc(line[2:].strip())
                story.append(ListFlowable([ListItem(Paragraph(txt, S_ITEM), leftIndent=2)], bulletType="bullet", bulletColor=ACC))
            elif re.match(r"^\d+\.\s", line):
                txt = esc(re.sub(r"^\d+\.\s*", "", line))
                story.append(ListFlowable([ListItem(Paragraph(txt, S_ITEM), leftIndent=2)], bulletType="1", bulletColor=ACC))
            # 表格残留
            elif in_table and temp_table_rows:
                story.append(parse_table(temp_table_rows)); temp_table_rows=[]; in_table=False
            else:
                story.append(par(line))
        i += 1
    if in_table and temp_table_rows and len(temp_table_rows) > 1:
        story.append(parse_table(temp_table_rows))

    doc = BaseDocTemplate(OUT, pagesize=A4,
                          leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=16*mm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    def footer(canv, doc_):
        canv.saveState()
        canv.setFont("CJK", 8)
        canv.setFillColor(MUT)
        canv.drawCentredString(A4[0]/2, 10*mm, f"楼宇对讲系统技术综述 · 面向工程端   |   第 {canv.getPageNumber()} 页")
        canv.restoreState()
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])
    doc.build(story)
    print("PDF OK", os.path.getsize(OUT))

if __name__ == "__main__":
    build()