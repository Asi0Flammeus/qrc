<p align="center">
  <img src="qrc.png" alt="QR code linking to this repo" width="200">
</p>

# qrc

Generate QR codes directly in the terminal. Minimal dependencies, compact Unicode rendering.

## Install

```bash
uv tool install qrc
```

Or with PNG export support:

```bash
uv tool install "qrc[png]"
```

## Usage

```bash
qrc 'https://example.com'
echo 'hello world' | qrc
qrc -u 'lnbc1...'              # uppercase → smaller QR (bech32/Lightning)
qrc -i 'text'                  # inverted colors (light terminals)
qrc -b 4 'text'                # wider quiet zone border
qrc -o code.png 'text'         # save as PNG (requires pillow)
```

### Flags

| Flag | Description |
|------|-------------|
| `-u`, `--upper` | Uppercase input before encoding. QR alphanumeric mode is ~40% more efficient than byte mode — produces significantly smaller codes for case-insensitive data (bech32, Lightning invoices). |
| `-i`, `--invert` | Invert colors for light terminal backgrounds. |
| `-b N`, `--border N` | Quiet zone width in modules (default: 1). |
| `-o FILE`, `--output FILE` | Save as PNG instead of terminal output. Requires `pillow`. |
| `-V`, `--version` | Show version. |

## How it works

Uses Unicode half-block characters (`▀▄█`) to render 2 QR modules per terminal row, keeping output compact. Error correction is set to L (lowest) for minimum size.

## Dependencies

- `qrcode` — pure Python QR encoder
- `pillow` — optional, only for PNG export
