"""Build the final CS599 course-report PDF from Markdown.

The script intentionally keeps dependencies small and uses ReportLab directly so
the submission can be regenerated without Pandoc or a GUI editor.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "CS599_大作业报告.md"
OUTPUT = ROOT / "docs" / "CS599_大作业报告.pdf"


def register_fonts() -> tuple[str, str]:
    regular = Path("C:/Windows/Fonts/msyh.ttc")
    bold = Path("C:/Windows/Fonts/msyhbd.ttc")
    try:
        if regular.exists():
            pdfmetrics.registerFont(TTFont("MicrosoftYaHei", str(regular)))
            if bold.exists():
                pdfmetrics.registerFont(TTFont("MicrosoftYaHei-Bold", str(bold)))
            else:
                pdfmetrics.registerFont(TTFont("MicrosoftYaHei-Bold", str(regular)))
            return "MicrosoftYaHei", "MicrosoftYaHei-Bold"
    except Exception:
        pass
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light", "STSong-Light"


FONT, FONT_BOLD = register_fonts()


class CourseDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, Paragraph):
            text = getattr(flowable, "_plain_text", "")
            level = getattr(flowable, "_outline_level", None)
            key = getattr(flowable, "_bookmark_key", "")
            if text and level is not None and key:
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


def build_styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    base = ParagraphStyle(
        "Base",
        parent=sample["BodyText"],
        fontName=FONT,
        fontSize=10.5,
        leading=17,
        textColor=colors.HexColor("#1f2937"),
        alignment=TA_LEFT,
        spaceAfter=6,
        wordWrap="CJK",
    )
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base,
            fontName=FONT_BOLD,
            fontSize=22,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=18,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base,
            fontName=FONT,
            fontSize=14,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#374151"),
            spaceAfter=12,
        ),
        "body": base,
        "small": ParagraphStyle("Small", parent=base, fontSize=8.5, leading=12, spaceAfter=3),
        "quote": ParagraphStyle(
            "Quote",
            parent=base,
            leftIndent=12,
            borderColor=colors.HexColor("#d1d5db"),
            borderWidth=0.7,
            borderPadding=6,
            backColor=colors.HexColor("#f9fafb"),
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base,
            fontName=FONT,
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#e5e7eb"),
            borderWidth=0.5,
            borderPadding=5,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base,
            fontName=FONT_BOLD,
            fontSize=17,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base,
            fontName=FONT_BOLD,
            fontSize=14,
            leading=21,
            textColor=colors.HexColor("#1e3a8a"),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base,
            fontName=FONT_BOLD,
            fontSize=12,
            leading=18,
            textColor=colors.HexColor("#334155"),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
    }


STYLES = build_styles()


def clean_inline(text: str) -> str:
    text = text.strip()
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font color='#374151'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = text.replace("&lt;br&gt;", "<br/>")
    return text


def plain_text(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[`*_#]", "", text)
    return text.strip()


def heading_para(text: str, level: int, index: int) -> Paragraph:
    style = STYLES["h1" if level <= 2 else "h2" if level == 3 else "h3"]
    para = Paragraph(clean_inline(text), style)
    outline_level = 0 if level <= 2 else 1 if level == 3 else 2
    para._outline_level = outline_level
    para._bookmark_key = f"heading-{index}"
    para._plain_text = plain_text(text)
    return para


def paragraph(text: str, style_name: str = "body") -> Paragraph:
    return Paragraph(clean_inline(text), STYLES[style_name])


def extract_cover_fields(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] not in {"字段", "---"}:
            fields[cells[0]] = cells[1]
    return fields


def cover_story(fields: dict[str, str]) -> list[Flowable]:
    rows = [
        ("课程名称", fields.get("课程名称", "企业级应用软件设计与开发")),
        ("项目名称", fields.get("项目名称", "ResearchFlow")),
        ("方向", fields.get("方向", "方向一：Agentic AI 原生开发")),
        ("学号", fields.get("学号", "")),
        ("姓名", fields.get("姓名", "")),
        ("专业", fields.get("专业", "")),
        ("指导教师", fields.get("指导教师", "")),
        ("提交日期", fields.get("提交日期", "")),
    ]
    table = Table(
        [[paragraph(k, "body"), paragraph(v, "body")] for k, v in rows],
        colWidths=[3.2 * cm, 11.8 * cm],
    )
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#111827")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return [
        Spacer(1, 2.0 * cm),
        Paragraph("CS599 期末大作业报告", STYLES["title"]),
        Paragraph("ResearchFlow：证据可追溯的多智能体文献调研 Agent", STYLES["subtitle"]),
        Spacer(1, 1.1 * cm),
        table,
        PageBreak(),
    ]


def table_from_rows(rows: list[list[str]], available_width: float) -> Table:
    col_count = max(len(row) for row in rows)
    normalized = [row + [""] * (col_count - len(row)) for row in rows]
    widths = [available_width / col_count] * col_count
    style_name = "small" if col_count >= 4 else "body"
    data = [[paragraph(cell, style_name) for cell in row] for row in normalized]
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5edf9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def parse_table(lines: list[str], start: int) -> tuple[Table, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        raw = lines[i].strip()
        cells = [cell.strip() for cell in raw.strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            rows.append(cells)
        i += 1
    return table_from_rows(rows, A4[0] - 4 * cm), i


def image_flowable(markdown_image: str) -> Flowable | None:
    match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", markdown_image.strip())
    if not match:
        return None
    alt_text, raw_path = match.groups()
    image_path = (SOURCE.parent / raw_path).resolve()
    if not image_path.exists():
        return paragraph(f"图片缺失：{raw_path}", "quote")

    image = RLImage(str(image_path))
    max_width = A4[0] - 4 * cm
    max_height = 10.5 * cm
    ratio = min(max_width / image.drawWidth, max_height / image.drawHeight, 1.0)
    image.drawWidth *= ratio
    image.drawHeight *= ratio
    caption = paragraph(alt_text or raw_path, "small")
    return KeepTogether([image, Spacer(1, 4), caption, Spacer(1, 8)])


def parse_markdown(lines: list[str]) -> list[Flowable]:
    story: list[Flowable] = []
    in_code = False
    code_lines: list[str] = []
    heading_index = 0
    start = 0
    for idx, line in enumerate(lines):
        if line.startswith("## 一、"):
            start = idx
            break

    i = start
    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                code = "\n".join(code_lines).strip()
                if code:
                    story.append(Preformatted(code, STYLES["code"], maxLineLength=95))
                    story.append(Spacer(1, 5))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not stripped:
            story.append(Spacer(1, 4))
            i += 1
            continue
        image = image_flowable(stripped)
        if image is not None:
            story.append(image)
            i += 1
            continue
        if stripped.startswith("|"):
            table, i = parse_table(lines, i)
            story.append(table)
            story.append(Spacer(1, 6))
            continue
        if stripped.startswith("#"):
            match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
            if match:
                heading_index += 1
                story.append(heading_para(match.group(2), len(match.group(1)), heading_index))
                i += 1
                continue
        if stripped.startswith("- "):
            story.append(Paragraph(clean_inline(stripped[2:]), STYLES["body"], bulletText="-"))
            i += 1
            continue
        if re.match(r"^\d+\.\s+", stripped):
            text = re.sub(r"^\d+\.\s+", "", stripped)
            story.append(Paragraph(clean_inline(text), STYLES["body"], bulletText="•"))
            i += 1
            continue
        if stripped.startswith(">"):
            story.append(paragraph(stripped.lstrip("> ").strip(), "quote"))
            i += 1
            continue
        if stripped in {"---", "***"}:
            i += 1
            continue
        story.append(paragraph(stripped))
        i += 1
    return story


def make_toc() -> list[Flowable]:
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC1", fontName=FONT, fontSize=10.5, leading=16, leftIndent=0, firstLineIndent=0),
        ParagraphStyle("TOC2", fontName=FONT, fontSize=9.5, leading=14, leftIndent=16, firstLineIndent=0),
        ParagraphStyle("TOC3", fontName=FONT, fontSize=9, leading=13, leftIndent=32, firstLineIndent=0),
    ]
    return [Paragraph("目录", STYLES["h1"]), Spacer(1, 6), toc, PageBreak()]


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(2 * cm, 1.15 * cm, "ResearchFlow CS599 期末大作业报告")
    canvas.drawRightString(A4[0] - 2 * cm, 1.15 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


def build_pdf() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    lines = text.splitlines()
    fields = extract_cover_fields(lines[:30])
    doc = CourseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="CS599 期末大作业报告 - ResearchFlow",
        author=fields.get("姓名", ""),
    )
    story: list[Flowable] = []
    story.extend(cover_story(fields))
    story.extend(make_toc())
    story.extend(parse_markdown(lines))
    doc.multiBuild(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
