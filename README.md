# 退職届

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![PDF](https://img.shields.io/badge/output-PDF-red.svg)](#)

横書きA4の退職届PDFを作ります。

宛先は左上、標題は中央、日付・所属・氏名は右下です。日付には曜日が入ります。印欄はありません。

## 準備

Python 3.9 以降が必要です。

```bash
python3 -m pip install -r requirements.txt
```

Cursor に入れる場合:

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn /path/to/resignation-letter ~/.cursor/plugins/local/resignation-letter
```

## 使い方

```bash
python3 skills/resignation-letter/scripts/generate.py \
  --company "株式会社見本" \
  --addressee "山田花子" \
  --department "営業部" \
  --name "佐藤　太郎" \
  --resign-date 2026-10-15
```

PDF はデスクトップに保存されます。デスクトップが無いときはホームに保存します。

必須:

| 項目 | 引数 |
| --- | --- |
| 会社名 | `--company` |
| 宛先氏名 | `--addressee` |
| 所属 | `--department` |
| 提出者氏名 | `--name` |
| 退職日 | `--resign-date` (`YYYY-MM-DD`) |

任意:

| 項目 | 引数 | 省略時 |
| --- | --- | --- |
| 宛先役職 | `--addressee-title` | 代表取締役 |
| 事由 | `--reason` | 一身上の都合 |
| 提出日 | `--submit-date` | 実行日（Asia/Tokyo） |
| 保存先 | `--output` | `~/Desktop/退職届_氏名.pdf` |

宛先は通称ではなく、登記上の漢字を書いてください。

## ライセンス

本体は MIT です。同梱の Noto Serif JP は [SIL Open Font License 1.1](skills/resignation-letter/assets/fonts/OFL.txt) です。
