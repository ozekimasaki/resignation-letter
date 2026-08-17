#!/usr/bin/env python3
"""Generate a horizontal A4 Japanese resignation notice PDF."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[misc, assignment]


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def jst_today() -> date:
    if ZoneInfo is not None:
        try:
            return datetime.now(ZoneInfo("Asia/Tokyo")).date()
        except Exception:
            pass
    return date.today()


def parse_iso_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        fail(f"{label} は YYYY-MM-DD で指定してください: {value}")
        raise AssertionError


def format_jp_date(value: date) -> str:
    weekdays = ("月", "火", "水", "木", "金", "土", "日")
    return f"{value.year}年{value.month}月{value.day}日（{weekdays[value.weekday()]}）"


def display_name(name: str) -> str:
    return name.replace(" ", "　").replace("　　", "　")


def file_name_part(name: str) -> str:
    return name.replace(" ", "").replace("　", "")


def default_output_dir() -> Path:
    desktop = Path.home() / "Desktop"
    if desktop.is_dir():
        return desktop
    return Path.home()


def require_nonempty(value: str, flag: str) -> None:
    if not value.strip():
        fail(f"{flag} は必須です")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        add_help=True,
        description="退職届 PDF を生成する",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--company", default="", help="会社名（必須）")
    parser.add_argument("--addressee-title", default="代表取締役")
    parser.add_argument("--addressee", default="", help="宛先氏名（必須）")
    parser.add_argument("--department", default="", help="所属（必須）")
    parser.add_argument("--name", default="", help="提出者氏名（必須）")
    parser.add_argument("--resign-date", default="", help="退職日 YYYY-MM-DD（必須）")
    parser.add_argument("--submit-date", default="", help="提出日 YYYY-MM-DD")
    parser.add_argument("--reason", default="一身上の都合")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def font_path() -> Path:
    path = skill_root() / "assets" / "fonts" / "NotoSerifJP-Regular.ttf"
    if not path.is_file():
        fail(f"フォントが見つかりません: {path}")
    return path


def draw_text(canvas, text, x, y_from_top, font_name, size, align="left", char_space=0.5):
    from reportlab.pdfbase.pdfmetrics import stringWidth

    canvas.setFont(font_name, size)
    y = 841.89 - y_from_top - size
    width = stringWidth(text, font_name, size)
    if char_space:
        width += char_space * max(len(text) - 1, 0)
    if align == "center":
        x = x - width / 2
    text_obj = canvas.beginText(x, y)
    text_obj.setFont(font_name, size)
    text_obj.setFillColorRGB(0, 0, 0)
    if char_space:
        text_obj.setCharSpace(char_space)
    text_obj.textOut(text)
    canvas.drawText(text_obj)


def draw_multiline(canvas, lines, x, y_from_top, font_name, size, leading, char_space=0.5):
    for i, line in enumerate(lines):
        draw_text(
            canvas,
            line,
            x,
            y_from_top + i * leading,
            font_name,
            size,
            align="left",
            char_space=char_space,
        )


def generate(opts: argparse.Namespace) -> str:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen import canvas
    except ImportError:
        fail(
            "reportlab がありません。プラグインルートで "
            "pip install -r requirements.txt を実行してください。"
        )

    require_nonempty(opts.company, "--company")
    require_nonempty(opts.addressee, "--addressee")
    require_nonempty(opts.department, "--department")
    require_nonempty(opts.name, "--name")
    require_nonempty(opts.resign_date, "--resign-date")

    name = display_name(opts.name)
    resign_text = format_jp_date(parse_iso_date(opts.resign_date, "--resign-date"))
    submit_date = (
        jst_today()
        if not opts.submit_date.strip()
        else parse_iso_date(opts.submit_date, "--submit-date")
    )
    submit_text = format_jp_date(submit_date)

    output = Path(opts.output) if opts.output.strip() else default_output_dir() / f"退職届_{file_name_part(name)}.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    pdfmetrics.registerFont(TTFont("NotoSerifJP", str(font_path())))

    page_width, _page_height = A4
    c = canvas.Canvas(str(output), pagesize=A4)

    margin_l = 90
    margin_r = 90
    content_w = page_width - margin_l - margin_r

    draw_text(c, opts.company, margin_l, 100, "NotoSerifJP", 14)
    draw_text(
        c,
        f"{opts.addressee_title}　{opts.addressee}　殿",
        margin_l,
        128,
        "NotoSerifJP",
        14,
    )
    draw_text(
        c,
        "退　職　届",
        margin_l + content_w / 2,
        220,
        "NotoSerifJP",
        22,
        align="center",
        char_space=4,
    )
    draw_text(c, "私儀", margin_l, 300, "NotoSerifJP", 14)
    draw_multiline(
        c,
        [
            f"このたび、{opts.reason}により、",
            f"{resign_text}をもって",
            "退職いたしたく、ここにお届けいたします。",
        ],
        margin_l + 28,
        340,
        "NotoSerifJP",
        14,
        leading=26,
    )

    sig_w = 250
    sig_x = page_width - margin_r - sig_w
    draw_text(c, submit_text, sig_x, 610, "NotoSerifJP", 14)
    draw_text(c, f"所属　{opts.department}", sig_x, 658, "NotoSerifJP", 14)
    draw_text(c, f"氏名　{name}", sig_x, 694, "NotoSerifJP", 14)

    c.showPage()
    c.save()
    return str(output)


def main() -> None:
    opts = parse_args()
    print(generate(opts))


if __name__ == "__main__":
    main()
