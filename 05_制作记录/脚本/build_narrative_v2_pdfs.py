#!/usr/bin/env python3
"""Render the two narrative-v2 PDFs from the supplied JSON without changing it.

Run with the bundled Python runtime.  This script does not generate images and
does not run an artifact-operation marker; the calling agent handles that once.
No work is performed at import time.
"""

from __future__ import annotations

import argparse
import html
import io
import json
import math
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image as PILImage, ImageOps

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    Image,
    KeepTogether,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "01_制作文档" / "推光_叙事改版_v2.json"
DEFAULT_OUT = ROOT / "01_制作文档"
INK = colors.HexColor("#20252B")
MUTED = colors.HexColor("#626D76")
ACCENT = colors.HexColor("#896832")
RULE = colors.HexColor("#D7DCDF")
PALE = colors.HexColor("#F5F6F7")
WHITE = colors.white


def as_text(value: Any) -> str:
    return "" if value is None else str(value)


def seconds(value: Any) -> float:
    """Accept numeric seconds or MM:SS / HH:MM:SS timecodes."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    raw = as_text(value).strip().removesuffix("秒").strip()
    if ":" not in raw:
        return float(raw)
    parts = raw.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"Unsupported timecode: {value!r}")
    result = 0.0
    for part in parts:
        result = result * 60 + float(part)
    return result


def timecode(value: Any) -> str:
    number = seconds(value)
    if not math.isclose(number, round(number), abs_tol=0.0001):
        return f"{int(number // 60):02d}:{number % 60:05.2f}"
    whole = int(round(number))
    return f"{whole // 60:02d}:{whole % 60:02d}"


def shot_label(value: Any) -> str:
    raw = as_text(value).strip()
    if raw.startswith("镜"):
        return raw
    return f"镜{int(raw):02d}" if raw.isdigit() else f"镜{raw}"


def image_path(asset: dict[str, Any], root: Path) -> Path:
    value = Path(as_text(asset["file"]))
    if value.is_absolute():
        return value
    return root / value if len(value.parts) > 1 else root / "02_视觉资产" / value


def validate(data: dict[str, Any], root: Path) -> dict[str, Any]:
    required = {
        "version", "title", "logline", "master_prompt", "story_notes",
        "visual_rules", "existing_assets", "new_assets", "segments", "shots",
        "narration", "constraints", "acceptance", "sources",
    }
    missing = required.difference(data)
    if missing:
        raise ValueError("Missing JSON fields: " + ", ".join(sorted(missing)))
    for name in ("story_notes", "visual_rules", "existing_assets", "new_assets",
                 "segments", "shots", "narration", "constraints", "acceptance", "sources"):
        if not isinstance(data[name], list):
            raise ValueError(f"{name} must be a list")
    if not isinstance(data["master_prompt"], str) or not data["master_prompt"].strip():
        raise ValueError("master_prompt must be a non-empty string")

    existing, new = data["existing_assets"], data["new_assets"]
    assets = existing + new
    if not assets:
        raise ValueError("The combined asset list must not be empty")
    names = []
    for asset in assets:
        absent = {"code", "file", "label", "use", "note"}.difference(asset)
        if absent:
            raise ValueError(f"Asset missing fields {sorted(absent)}: {asset}")
        path = image_path(asset, root)
        if path.suffix.lower() != ".png":
            raise ValueError(f"Asset must be a PNG: {path}")
        names.append(path.name)
    if len(set(names)) != len(assets):
        raise ValueError(f"Asset filenames must be unique ({len(assets)} distinct PNGs required)")

    absent_images = [str(image_path(asset, root)) for asset in assets
                     if not image_path(asset, root).is_file()]
    if absent_images:
        raise ValueError("Missing image files:\n" + "\n".join(absent_images))
    for asset in assets:
        path = image_path(asset, root)
        width, height = ImageReader(str(path)).getSize()
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid PNG dimensions: {path}")

    shots = data["shots"]
    if not shots:
        raise ValueError("shots must not be empty")
    previous, total, ids = 0.0, 0.0, set()
    for shot in shots:
        needed = {"id", "start", "end", "duration", "title", "phase", "refs",
                  "prompt", "sound", "vo", "edit"}
        if needed.difference(shot):
            raise ValueError(f"Incomplete shot: {shot}")
        sid = shot_label(shot["id"])
        if sid in ids:
            raise ValueError(f"Duplicate shot id: {sid}")
        ids.add(sid)
        start, end, duration = map(seconds, (shot["start"], shot["end"], shot["duration"]))
        if not math.isclose(start, previous, abs_tol=0.001):
            raise ValueError(f"Timeline gap/overlap at {sid}: {start} vs {previous}")
        if duration <= 0 or not math.isclose(end - start, duration, abs_tol=0.001):
            raise ValueError(f"Duration mismatch at {sid}: {start}, {end}, {duration}")
        if not isinstance(shot["refs"], list):
            raise ValueError(f"refs must be a list at {sid}")
        if not as_text(shot["prompt"]).strip():
            raise ValueError(f"Empty prompt at {sid}")
        previous, total = end, total + duration
    if not math.isclose(total, 180, abs_tol=0.001) or not math.isclose(previous, 180, abs_tol=0.001):
        raise ValueError(f"The complete timeline must end at 180 seconds; got {previous}, sum={total}")

    if not data["segments"]:
        raise ValueError("segments must not be empty")
    segment_total = 0.0
    segment_previous = 0.0
    all_segment_ranges = True
    for segment in data["segments"]:
        if {"time", "title", "seconds", "note"}.difference(segment):
            raise ValueError(f"Incomplete segment: {segment}")
        segment_duration = seconds(segment["seconds"])
        segment_total += segment_duration
        pair = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?)\s*[-~—–至]\s*"
                         r"(\d{1,2}:\d{2}(?::\d{2})?)", as_text(segment["time"]))
        if pair:
            segment_start, segment_end = seconds(pair[1]), seconds(pair[2])
            if (all_segment_ranges and not math.isclose(segment_start, segment_previous, abs_tol=0.001)):
                raise ValueError(f"Segment gap/overlap at {segment['time']}")
            if not math.isclose(segment_end - segment_start, segment_duration, abs_tol=0.001):
                raise ValueError(f"Segment duration mismatch at {segment['time']}")
            segment_previous = segment_end
        else:
            all_segment_ranges = False
    if not math.isclose(segment_total, 180, abs_tol=0.001):
        raise ValueError(f"Segment durations must sum to 180; got {segment_total}")
    for row in data["visual_rules"]:
        if {"label", "text"}.difference(row):
            raise ValueError(f"Incomplete visual rule: {row}")
    for row in data["narration"]:
        if {"time", "text"}.difference(row):
            raise ValueError(f"Incomplete narration row: {row}")
    return {"shots": len(shots), "duration": total, "pngs": len(assets),
            "existing_pngs": len(existing),
            "new_pngs": len(new), "filenames": names}


def register_fonts() -> None:
    if "TuiguangCN" in pdfmetrics.getRegisteredFontNames():
        return
    light = Path("/System/Library/Fonts/STHeiti Light.ttc")
    medium = Path("/System/Library/Fonts/STHeiti Medium.ttc")
    arial = Path("/Library/Fonts/Arial Unicode.ttf")
    normal_file = light if light.is_file() else arial
    bold_file = medium if medium.is_file() else normal_file
    if not normal_file.is_file():
        raise FileNotFoundError("Embedded Chinese font unavailable: need STHeiti or Arial Unicode")
    pdfmetrics.registerFont(TTFont("TuiguangCN", str(normal_file), subfontIndex=0))
    pdfmetrics.registerFont(TTFont("TuiguangCNBold", str(bold_file), subfontIndex=0))
    pdfmetrics.registerFontFamily("TuiguangCN", normal="TuiguangCN", bold="TuiguangCNBold",
                                  italic="TuiguangCN", boldItalic="TuiguangCNBold")


def styles() -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("TGBody", fontName="TuiguangCN", fontSize=10.5, leading=15.5,
                          textColor=INK, wordWrap="CJK", spaceAfter=7,
                          splitLongWords=True, allowWidows=0, allowOrphans=0)
    return {
        "body": base,
        "small": ParagraphStyle("TGSmall", parent=base, fontSize=9.6, leading=13.6, spaceAfter=5),
        "title": ParagraphStyle("TGTitle", parent=base, fontName="TuiguangCNBold", fontSize=21,
                                leading=29, spaceAfter=13, keepWithNext=True),
        "h2": ParagraphStyle("TGH2", parent=base, fontName="TuiguangCNBold", fontSize=13,
                             leading=19, textColor=ACCENT, spaceBefore=12, spaceAfter=8,
                             keepWithNext=True),
        "h3": ParagraphStyle("TGH3", parent=base, fontName="TuiguangCNBold", fontSize=11,
                             leading=16, spaceBefore=6, spaceAfter=5, keepWithNext=True),
        "assethead": ParagraphStyle("TGAssetHead", parent=base, fontName="TuiguangCNBold",
                                    fontSize=10.5, leading=15, spaceBefore=0, spaceAfter=2),
        "tableheading": ParagraphStyle("TGTableHeading", parent=base, fontName="TuiguangCNBold",
                                       fontSize=13, leading=19, textColor=ACCENT,
                                       spaceBefore=10, spaceAfter=7, keepWithNext=False),
        "cell": ParagraphStyle("TGCell", parent=base, fontSize=10.1, leading=14.4, spaceAfter=4),
        "filename": ParagraphStyle("TGFilename", parent=base, fontSize=9, leading=12.6,
                                   spaceAfter=3, splitLongWords=True),
        "th": ParagraphStyle("TGTH", parent=base, fontName="TuiguangCNBold", fontSize=10,
                             leading=14.2, textColor=WHITE, spaceAfter=0),
        "shothead": ParagraphStyle("TGShotHead", parent=base, fontName="TuiguangCNBold",
                                   fontSize=11.1, leading=15.4, spaceAfter=3),
        "shot": ParagraphStyle("TGShot", parent=base, fontSize=10.5, leading=14.5, spaceAfter=3),
        "shotmeta": ParagraphStyle("TGShotMeta", parent=base, fontSize=10.2, leading=14, spaceAfter=2),
        "caption": ParagraphStyle("TGCaption", parent=base, fontSize=9.6, leading=13.1, spaceAfter=3),
    }


def markup(value: Any) -> str:
    escaped = html.escape(as_text(value), quote=True)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped, flags=re.S)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
                     lambda m: f'<a href="{m[2]}" color="#896832">{m[1]}</a>', escaped)
    return escaped.replace("\n", "<br/>")


def p(value: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(markup(value) or "&#160;", style)


def text_blocks(value: Any, style: ParagraphStyle) -> list[Any]:
    raw = as_text(value)
    return [p(block, style) for block in re.split(r"\n\s*\n", raw) if block.strip()]


def labeled(label: str, value: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(f"<b>{html.escape(label)}：</b>{markup(value) or '无'}", style)


def heading(flow: list[Any], title: str, st: dict[str, ParagraphStyle]) -> None:
    flow.append(p(title, st["h2"]))


def numbered(flow: list[Any], values: list[Any], st: dict[str, ParagraphStyle]) -> None:
    for index, value in enumerate(values, 1):
        flow.append(p(f"{index}. {as_text(value)}", st["body"]))


def make_doc(path: Path, data: dict[str, Any], label: str, wide: bool) -> SimpleDocTemplate:
    size = landscape(A4) if wide else A4
    return SimpleDocTemplate(str(path), pagesize=size, leftMargin=39 if wide else 43,
                             rightMargin=39 if wide else 43, topMargin=48,
                             bottomMargin=42, title=f"{data['title']} - {label} - v2",
                             author="", subject=as_text(data["logline"]), pageCompression=1)


def page_chrome(label: str):
    def draw(canvas, doc):
        width, height = doc.pagesize
        canvas.saveState()
        canvas.setFillColor(MUTED)
        canvas.setFont("TuiguangCN", 8.2)
        canvas.drawString(doc.leftMargin, height - 25, f"《推光》 / {label} / v2")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.45)
        canvas.line(doc.leftMargin, height - 33, width - doc.rightMargin, height - 33)
        canvas.drawString(doc.leftMargin, 23, "180秒纯AI工艺情境短片 · 叙事改版 v2")
        canvas.drawRightString(width - doc.rightMargin, 23, str(doc.page))
        canvas.restoreState()
    return draw


def usable_width(doc: SimpleDocTemplate) -> float:
    # SimpleDocTemplate's Frame retains 6pt padding on both horizontal sides.
    return doc.width - 12


def add_front(flow: list[Any], data: dict[str, Any], label: str,
              st: dict[str, ParagraphStyle], report: dict[str, Any]) -> None:
    flow.append(p(f"{data['title']}｜{label}", st["title"]))
    version = as_text(data["version"])
    flow.append(p(f"版本：{version}" + ("" if "v2" in version.lower() else " · v2"), st["small"]))
    flow.append(p(data["logline"], st["body"]))
    flow.append(p(f"时码校验：{report['shots']}段，从00:00连续至03:00，累计180秒，片尾计入总长。"
                  f"图像清单共{report['pngs']}张PNG，其中{report['existing_pngs']}张既有资产、"
                  f"{report['new_pngs']}张新增关键帧；L01保持文字规范。", st["small"]))
    heading(flow, "可直接复制的总制作提示词", st)
    flow.extend(text_blocks(data["master_prompt"], st["body"]))
    heading(flow, "叙事与制作说明", st)
    numbered(flow, data["story_notes"], st)
    heading(flow, "统一视觉与连续性规则", st)
    for rule in data["visual_rules"]:
        flow.append(labeled(as_text(rule["label"]), rule["text"], st["body"]))


def table_style() -> TableStyle:
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
    ])


def asset_table(assets: list[dict[str, Any]], width: float,
                st: dict[str, ParagraphStyle], *, compact: bool = False) -> LongTable:
    headings = ["编号与具体文件", "内容、镜号与用途", "调用边界"] if compact else ["编号与具体文件", "内容、镜号与调用边界"]
    rows: list[list[Any]] = [[p(value, st["th"]) for value in headings]]
    for asset in assets:
        file_width = width * (0.26 if compact else 0.36) - 16
        left = [p(asset["code"], st["assethead"]), filename_paragraph(asset["file"], file_width, st)]
        right = [p(asset["label"], st["assethead"]), labeled("用途", asset["use"], st["cell"])]
        if compact:
            rows.append([left, right, p(asset["note"], st["cell"])])
        elif as_text(asset["note"]).strip():
            right.append(labeled("边界", asset["note"], st["cell"]))
            rows.append([left, right])
        else:
            rows.append([left, right])
    ratios = [0.26, 0.40, 0.34] if compact else [0.36, 0.64]
    result = LongTable(rows, colWidths=[width * ratio for ratio in ratios], repeatRows=1,
                       hAlign="LEFT", splitByRow=1, splitInRow=1)
    result.setStyle(table_style())
    return result


def filename_paragraph(value: Any, width: float, st: dict[str, ParagraphStyle]) -> Paragraph:
    """Break long filenames at underscores, never leave a lone final letter."""
    text = as_text(value)
    style = st["filename"]
    if pdfmetrics.stringWidth(text, style.fontName, style.fontSize) <= width:
        return p(text, style)
    tokens = re.split(r"(?<=_)", text)
    lines, current = [], ""
    for token in tokens:
        if current and pdfmetrics.stringWidth(current + token, style.fontName, style.fontSize) > width:
            lines.append(current)
            current = token
        else:
            current += token
    if current:
        lines.append(current)
    return Paragraph("<br/>".join(markup(line) for line in lines), style)


def add_table_section(flow: list[Any], title: str, table: LongTable,
                      doc: SimpleDocTemplate, st: dict[str, ParagraphStyle]) -> None:
    """Keep a heading with the table header and first row, not the entire table."""
    width = usable_width(doc)
    table.wrap(width, 100000)
    first_rows = sum(table._rowHeights[:2])
    head = p(title, st["tableheading"])
    minimum = first_rows + head.wrap(width, 100000)[1] + head.getSpaceBefore() + head.getSpaceAfter() + 3
    flow.extend([CondPageBreak(minimum), head, table])


def segment_table(data: dict[str, Any], width: float,
                  st: dict[str, ParagraphStyle]) -> LongTable:
    rows = [[p("时间 / 秒数", st["th"]), p("段落与作用", st["th"])]]
    for item in data["segments"]:
        rows.append([p(f"{item['time']}\n{item['seconds']}秒", st["cell"]),
                     [p(item["title"], st["h3"]), p(item["note"], st["cell"])]])
    result = LongTable(rows, colWidths=[width * 0.25, width * 0.75], repeatRows=1,
                       hAlign="LEFT", splitByRow=1, splitInRow=1)
    result.setStyle(table_style())
    return result


def thumbnails(data: dict[str, Any], root: Path, width: float,
               st: dict[str, ParagraphStyle], *, page_height: float) -> Table:
    rows, row = [], []
    cell_width = width / 2
    row_count = max(1, math.ceil(len(data["new_assets"]) / 2))
    # Seven thumbnails use four compact rows on one portrait page instead of
    # leaving the seventh picture on an otherwise empty continuation page.
    image_box_height = min(126, max(54, (page_height - 90) / row_count - 65))
    for asset in data["new_assets"]:
        path = image_path(asset, root)
        iw, ih = ImageReader(str(path)).getSize()
        factor = min((cell_width - 16) / iw, image_box_height / ih)
        # Only the embedded PDF preview is resized/compressed.  The source PNG
        # remains untouched and continues to be the video-generation reference.
        preview = compressed_thumbnail(path, max_width=650)
        image = Image(preview, width=iw * factor, height=ih * factor)
        image.hAlign = "LEFT"
        row.append([image, Spacer(1, 5), p(f"{asset['code']}｜{asset['label']}", st["caption"]),
                    p(asset["file"], st["caption"])])
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row + [""])
    grid = Table(rows, colWidths=[cell_width, cell_width], hAlign="LEFT", splitByRow=1)
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
    ]))
    return grid


def compressed_thumbnail(path: Path, *, max_width: int = 650) -> io.BytesIO:
    with PILImage.open(path) as source:
        image = ImageOps.exif_transpose(source)
        scale = min(1.0, max_width / image.width)
        if scale < 1:
            image = image.resize((round(image.width * scale), round(image.height * scale)),
                                 PILImage.Resampling.LANCZOS)
        if image.mode in ("RGBA", "LA") or "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = PILImage.new("RGBA", rgba.size, (255, 255, 255, 255))
            image = PILImage.alpha_composite(background, rgba).convert("RGB")
        else:
            image = image.convert("RGB")
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=86, optimize=True, subsampling=0)
        buffer.seek(0)
        return buffer


def compact_shot_ranges(ids: list[Any]) -> str:
    numbers = []
    for value in ids:
        raw = as_text(value).removeprefix("镜")
        if not raw.isdigit():
            return "、".join(shot_label(item) for item in ids)
        numbers.append(int(raw))
    numbers = sorted(set(numbers))
    ranges = []
    for number in numbers:
        if ranges and number == ranges[-1][1] + 1:
            ranges[-1][1] = number
        else:
            ranges.append([number, number])
    return "、".join(f"{first:02d}" if first == last else f"{first:02d}-{last:02d}"
                    for first, last in ranges)


def direct_shot_refs(asset: dict[str, Any], data: dict[str, Any]) -> str:
    filename = Path(as_text(asset["file"])).name
    code = as_text(asset["code"])
    ids = []
    for shot in data["shots"]:
        refs = [as_text(ref) for ref in shot["refs"]]
        if any(Path(ref).name == filename or ref == code for ref in refs):
            ids.append(shot["id"])
    if ids:
        return "直接调用：镜" + compact_shot_ranges(ids)
    # The full use/note definitions remain in the asset PDF and Markdown.
    return "派生、间接或备用参考；详见资产册"


def short_asset_index_table(assets: list[dict[str, Any]], data: dict[str, Any],
                             width: float, st: dict[str, ParagraphStyle]) -> LongTable:
    rows = [[p("编号 + 完整文件名", st["th"]), p("名称 + 对应镜号", st["th"])]]
    for asset in assets:
        left = Paragraph(f"<b>{markup(asset['code'])}</b>　{markup(Path(as_text(asset['file'])).name)}",
                         st["shot"])
        right = Paragraph(f"<b>{markup(asset['label'])}</b><br/>{markup(direct_shot_refs(asset, data))}",
                          st["shot"])
        rows.append([left, right])
    table = LongTable(rows, colWidths=[width * 0.50, width * 0.50], repeatRows=1,
                      hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
    ]))
    return table


def balanced_chunks(values: list[Any], page_count: int) -> list[list[Any]]:
    base, extra = divmod(len(values), page_count)
    chunks, offset = [], 0
    for index in range(page_count):
        size = base + (1 if index < extra else 0)
        chunks.append(values[offset:offset + size])
        offset += size
    return chunks


def add_short_asset_index(flow: list[Any], doc: SimpleDocTemplate, data: dict[str, Any],
                          st: dict[str, ParagraphStyle], total: int) -> None:
    assets = data["existing_assets"] + data["new_assets"]
    pages = max(1, math.ceil(len(assets) / 10))
    width = usable_width(doc)
    available = doc.height - 12 - 72
    while True:
        chunks = balanced_chunks(assets, pages)
        tables = [short_asset_index_table(chunk, data, width, st) for chunk in chunks]
        if all(table.wrap(width, 100000)[1] <= available for table in tables):
            break
        pages += 1
        if pages > len(assets):
            raise ValueError("Asset index row is too long to fit at 10.5pt")
    for index, table in enumerate(tables, 1):
        flow.append(PageBreak())
        heading(flow, f"具体资产文件索引：{total}张PNG（{index}/{pages}）", st)
        flow.append(p("仅列文件与直接调用镜号；派生及备用规则见资产册。L01为03_光线规范中的文字文件，不计入图片。", st["small"]))
        flow.append(table)


def reference_text(refs: list[Any], data: dict[str, Any]) -> str:
    assets = data["existing_assets"] + data["new_assets"]
    by_code: dict[str, list[str]] = defaultdict(list)
    filenames = set()
    for asset in assets:
        name = as_text(asset["file"])
        by_code[as_text(asset["code"])].append(name)
        filenames.add(name)
        filenames.add(Path(name).name)
    expanded = []
    for ref in refs:
        text = as_text(ref)
        if text in filenames:
            expanded.append(text)
        elif text in by_code and len(by_code[text]) == 1:
            expanded.append(f"{text}（{by_code[text][0]}）")
        elif text in by_code:
            expanded.append(f"{text}（具体变体见资产文件索引，按本镜部位与工序选择）")
        elif text == "L01":
            expanded.append("L01_lighting.md（文字光线规范）")
        else:
            expanded.append(text)
    return "；".join(expanded) if expanded else "纯后期或既有片段复用，按本镜说明执行"


def shot_card(shot: dict[str, Any], data: dict[str, Any], width: float,
              st: dict[str, ParagraphStyle]) -> Table:
    duration = seconds(shot["duration"])
    dlabel = f"{duration:g}秒"
    head = (f"{shot_label(shot['id'])}  {timecode(shot['start'])}-{timecode(shot['end'])}"
            f"  /  {dlabel}  /  {shot['title']}")
    if as_text(shot["phase"]).strip():
        head += f"  ·  {shot['phase']}"
    inside = width - 20
    content = [p(head, st["shothead"]),
               labeled("资产调用", reference_text(shot["refs"], data), st["shotmeta"]),
               labeled("画面提示词", shot["prompt"], st["shot"])]
    left = [labeled("声音", shot["sound"], st["shotmeta"]),
            labeled("旁白", shot["vo"], st["shotmeta"])]
    right = [labeled("剪辑与后期", shot["edit"], st["shotmeta"])]
    lower = Table([[left, right]], colWidths=[inside * 0.50, inside * 0.50],
                  hAlign="LEFT", splitByRow=1, splitInRow=1)
    lower.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 10),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBEFORE", (1, 0), (1, 0), 0.4, RULE),
    ]))
    content.append(lower)
    card = Table([[content]], colWidths=[width], hAlign="LEFT", splitByRow=0)
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return card


def add_shots(flow: list[Any], doc: SimpleDocTemplate, data: dict[str, Any],
              st: dict[str, ParagraphStyle]) -> None:
    """Greedy pagination: at most 4 complete cards, usually 3-4 per page."""
    flow.append(PageBreak())
    used, count, first_page = 0.0, 0, True
    page_usable = doc.height - 12  # Platypus frame padding.
    width = usable_width(doc)
    for shot in data["shots"]:
        card = shot_card(shot, data, width, st)
        card_height = card.wrap(width, 100000)[1]
        title = p("逐镜制作提示词" if first_page else "逐镜制作提示词（续）", st["h2"])
        # Heading spaceBefore is discarded at the top of a new frame.
        title_height = title.wrap(width, 100000)[1] + title.getSpaceAfter()
        if card_height + title_height + 5 > page_usable:
            raise ValueError(f"{shot_label(shot['id'])} is too long for a complete 10.5pt card; "
                             "split this shot in the source JSON rather than shrinking or clipping text")
        if count and (count >= 4 or used + card_height + 5 > page_usable):
            flow.append(PageBreak())
            count, used, first_page = 0, 0.0, False
            title = p("逐镜制作提示词（续）", st["h2"])
            title_height = title.wrap(width, 100000)[1] + title.getSpaceAfter()
        if not count:
            flow.append(title)
            used = title_height
        flow.extend([KeepTogether([card]), Spacer(1, 5)])
        used += card_height + 5
        count += 1


def add_narration(flow: list[Any], data: dict[str, Any], st: dict[str, ParagraphStyle]) -> None:
    heading(flow, "完整旁白与时间窗", st)
    for row in data["narration"]:
        flow.append(labeled(as_text(row["time"]), row["text"], st["body"]))


def add_rules_and_sources(flow: list[Any], data: dict[str, Any],
                         st: dict[str, ParagraphStyle]) -> None:
    heading(flow, "生成通用约束与失败回退", st)
    numbered(flow, data["constraints"], st)
    heading(flow, "验收与交付检查", st)
    numbered(flow, data["acceptance"], st)
    heading(flow, "资料依据与来源", st)
    numbered(flow, data["sources"], st)


def render_asset_pdf(path: Path, data: dict[str, Any], root: Path,
                     report: dict[str, Any]) -> None:
    doc, st = make_doc(path, data, "资产与视觉提示词固定", False), styles()
    flow: list[Any] = []
    add_front(flow, data, "资产与视觉提示词固定", st, report)
    heading(flow, "180秒叙事段落", st)
    flow.append(segment_table(data, usable_width(doc), st))
    flow.append(PageBreak())
    heading(flow, f"全{report['pngs']}张PNG文件与调用清单", st)
    flow.append(p("本表保留具体文件名、用途和阶段边界；L01为文字规范，不计入PNG数量。", st["small"]))
    if data["existing_assets"]:
        add_table_section(flow, f"既有{report['existing_pngs']}张资产",
                          asset_table(data["existing_assets"], usable_width(doc), st), doc, st)
    if data["new_assets"]:
        # Keep the small new-keyframe list independent, so its final one or two
        # rows do not spill onto an otherwise empty page after the old assets.
        flow.append(PageBreak())
        add_table_section(flow, f"新增{report['new_pngs']}张叙事关键帧",
                          asset_table(data["new_assets"], usable_width(doc), st), doc, st)
        flow.append(PageBreak())
        heading(flow, f"新增{report['new_pngs']}图缩略览", st)
        flow.append(p("缩略图仅用于核对身份、器物及动作起点；逐镜生成调用原始PNG，不把总览当作首帧。", st["small"]))
        flow.append(thumbnails(data, root, usable_width(doc), st, page_height=doc.height - 12))
    flow.append(PageBreak())
    add_narration(flow, data, st)
    add_rules_and_sources(flow, data, st)
    chrome = page_chrome("资产与视觉提示词固定")
    doc.build(flow, onFirstPage=chrome, onLaterPages=chrome)


def render_shot_pdf(path: Path, data: dict[str, Any], report: dict[str, Any]) -> None:
    doc, st = make_doc(path, data, "分镜脚本", True), styles()
    flow: list[Any] = []
    add_front(flow, data, "分镜脚本", st, report)
    heading(flow, "180秒段落与节奏", st)
    flow.append(segment_table(data, usable_width(doc), st))
    add_shots(flow, doc, data, st)
    flow.append(PageBreak())
    add_narration(flow, data, st)
    add_rules_and_sources(flow, data, st)
    add_short_asset_index(flow, doc, data, st, report["pngs"])
    chrome = page_chrome("分镜脚本")
    doc.build(flow, onFirstPage=chrome, onLaterPages=chrome)


def md_sections(data: dict[str, Any]) -> str:
    parts = [f"版本：{data['version']} · v2", as_text(data["logline"]),
             "## 可直接复制的总制作提示词", data["master_prompt"], "## 叙事与制作说明"]
    parts.extend(f"{i}. {as_text(value)}" for i, value in enumerate(data["story_notes"], 1))
    parts.append("## 统一视觉与连续性规则")
    for rule in data["visual_rules"]:
        parts.extend([f"### {rule['label']}", as_text(rule["text"])])
    parts.append("## 180秒段落与节奏")
    for row in data["segments"]:
        parts.extend([f"### {row['time']}｜{row['title']}｜{row['seconds']}秒", as_text(row["note"])])
    return "\n\n".join(parts)


def md_asset_rows(assets: list[dict[str, Any]]) -> str:
    parts = []
    for asset in assets:
        parts.extend([f"### {asset['code']}｜{asset['label']}", f"文件：{asset['file']}",
                      f"用途：{asset['use']}", f"边界：{asset['note']}"])
    return "\n\n".join(parts)


def md_appendix(data: dict[str, Any]) -> str:
    parts = ["## 完整旁白与时间窗"]
    for row in data["narration"]:
        parts.extend([f"### {row['time']}", as_text(row["text"])])
    for key, label in [("constraints", "生成通用约束与失败回退"),
                       ("acceptance", "验收与交付检查"), ("sources", "资料依据与来源")]:
        parts.append(f"## {label}")
        parts.extend(f"{i}. {as_text(value)}" for i, value in enumerate(data[key], 1))
    return "\n\n".join(parts)


def markdown_exports(data: dict[str, Any]) -> dict[str, str]:
    existing_count, new_count = len(data["existing_assets"]), len(data["new_assets"])
    total = existing_count + new_count
    assets = [f"# {data['title']}｜资产与视觉提示词固定", md_sections(data),
              f"## 既有{existing_count}张PNG", md_asset_rows(data["existing_assets"]),
              f"## 新增{new_count}张PNG", md_asset_rows(data["new_assets"]), f"## 新增{new_count}图缩略览"]
    for asset in data["new_assets"]:
        filename = Path(as_text(asset["file"])).name
        assets.append(f"![{asset['code']} {asset['label']}](../02_视觉资产/{filename})")
    assets.append(md_appendix(data))

    shots = [f"# {data['title']}｜分镜脚本", md_sections(data), "## 逐镜制作提示词"]
    for shot in data["shots"]:
        shots.extend([
            f"### {shot_label(shot['id'])}｜{timecode(shot['start'])}-{timecode(shot['end'])}"
            f"｜{seconds(shot['duration']):g}秒｜{shot['title']}",
            f"阶段：{shot['phase']}",
            "资产调用：" + "；".join(as_text(ref) for ref in shot["refs"]),
            "画面提示词：\n\n" + as_text(shot["prompt"]),
            "声音：\n\n" + as_text(shot["sound"]),
            "旁白：\n\n" + as_text(shot["vo"]),
            "剪辑与后期：\n\n" + as_text(shot["edit"]),
        ])
    shots.extend([md_appendix(data), f"## 具体资产文件索引：{total}张PNG",
                  md_asset_rows(data["existing_assets"] + data["new_assets"])])
    return {"资产与视觉提示词固定.md": "\n\n".join(assets) + "\n",
            "分镜脚本.md": "\n\n".join(shots) + "\n"}


def verify_pdf(path: Path, report: dict[str, Any], *, shots: bool) -> dict[str, Any]:
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact = re.sub(r"\s+", "", text)
    missing = [name for name in report["filenames"] if re.sub(r"\s+", "", name) not in compact]
    if missing:
        raise ValueError(f"Filename text missing from {path.name}: {missing}")
    if "180秒" not in compact or "v2" not in text:
        raise ValueError(f"Timeline/version text missing from {path.name}")
    embedded = False
    for page in reader.pages:
        resources = page.get("/Resources", {})
        if hasattr(resources, "get_object"):
            resources = resources.get_object()
        fonts = resources.get("/Font", {})
        if hasattr(fonts, "get_object"):
            fonts = fonts.get_object()
        for font_ref in fonts.values():
            font = font_ref.get_object()
            descriptor = font.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                if any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                    embedded = True
    if not embedded:
        raise ValueError(f"No embedded TrueType/CJK font found in {path.name}")
    if shots and "画面提示词" not in compact:
        raise ValueError("Shot prompt labels are missing from the storyboard PDF")
    return {"file": path.name, "pages": len(reader.pages), "bytes": path.stat().st_size,
            "embedded_font": embedded, "all_asset_filenames_present": True,
            "asset_file_count": report["pngs"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                        help="Narrative-v2 JSON; read only")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                        help="Directory for the two PDFs and matching Markdown sources")
    parser.add_argument("--check-only", action="store_true",
                        help="Validate JSON, 180-second timeline and all listed PNGs without writing")
    args = parser.parse_args(argv)
    source = args.source.resolve()
    data = json.loads(source.read_text(encoding="utf-8"))
    report = validate(data, ROOT)
    if args.check_only:
        print(json.dumps({"source": str(source), "valid": True, **report}, ensure_ascii=False, indent=2))
        return 0

    register_fonts()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    # Render and check both temporary files before replacing either final PDF.
    with tempfile.TemporaryDirectory(prefix=".tuiguang-v2-", dir=out) as scratch:
        temporary = Path(scratch)
        asset_pdf = temporary / "资产与视觉提示词固定.pdf"
        shot_pdf = temporary / "分镜脚本.pdf"
        render_asset_pdf(asset_pdf, data, ROOT, report)
        render_shot_pdf(shot_pdf, data, report)
        outputs = [verify_pdf(asset_pdf, report, shots=False), verify_pdf(shot_pdf, report, shots=True)]
        for pdf in (asset_pdf, shot_pdf):
            pdf.replace(out / pdf.name)
        for name, text in markdown_exports(data).items():
            (out / name).write_text(text, encoding="utf-8")
    for row in outputs:
        row["file"] = str(out / row["file"])
    print(json.dumps({"timeline_seconds": 180, "pngs": report["pngs"],
                      "existing_pngs": report["existing_pngs"], "new_pngs": report["new_pngs"], "outputs": outputs,
                      "markdown_sources": [str(out / name) for name in markdown_exports(data)]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Narrative-v2 rendering failed: {exc}", file=sys.stderr)
        raise
