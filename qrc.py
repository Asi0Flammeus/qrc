#!/usr/bin/env python3
"""Generate QR codes in the terminal."""

__version__ = "0.1.0"

import argparse
import sys

import qrcode


def render(matrix, invert=False):
    """Render QR matrix using Unicode half-blocks (2 modules per cell height)."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0

    lines = []
    for y in range(0, rows, 2):
        line = []
        for x in range(cols):
            top = matrix[y][x]
            bot = matrix[y + 1][x] if y + 1 < rows else False
            if top and bot:
                line.append(" ")
            elif top:
                line.append("▄")
            elif bot:
                line.append("▀")
            else:
                line.append("█")
        lines.append("".join(line))

    output = "\n".join(lines)
    if invert:
        output = output.translate(str.maketrans(" ▄▀█", "█▀▄ "))
    return output


def save_png(matrix, path, scale=10):
    """Save QR matrix as PNG. Requires pillow."""
    try:
        from PIL import Image
    except ImportError:
        print("error: PNG output requires pillow: uv pip install pillow", file=sys.stderr)
        sys.exit(1)

    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    img = Image.new("1", (cols * scale, rows * scale), 1)
    pixels = img.load()
    for y in range(rows):
        for x in range(cols):
            if matrix[y][x]:
                for dy in range(scale):
                    for dx in range(scale):
                        pixels[x * scale + dx, y * scale + dy] = 0
    img.save(path)


def main():
    ap = argparse.ArgumentParser(
        prog="qrc",
        description="Generate QR codes in the terminal",
    )
    ap.add_argument("text", nargs="?", help="text to encode")
    ap.add_argument("-i", "--invert", action="store_true", help="invert colors (light terminals)")
    ap.add_argument("-u", "--upper", action="store_true",
                    help="uppercase input (smaller QR for case-insensitive data like Lightning invoices)")
    ap.add_argument("-b", "--border", type=int, default=1, metavar="N",
                    help="quiet zone border width in modules (default: 1)")
    ap.add_argument("-o", "--output", metavar="FILE",
                    help="save as PNG (requires pillow)")
    ap.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args()

    text = args.text
    if not text:
        if sys.stdin.isatty():
            ap.error("usage: qrc <text>  or  echo <text> | qrc")
        text = sys.stdin.read().strip()
    if not text:
        ap.error("empty input")

    if args.upper:
        text = text.upper()

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=args.border)
    qr.add_data(text)
    qr.make(fit=True)
    matrix = qr.get_matrix()

    if args.output:
        save_png(matrix, args.output)
        print(f"saved: {args.output}", file=sys.stderr)
    else:
        print(render(matrix, invert=args.invert))


if __name__ == "__main__":
    main()
