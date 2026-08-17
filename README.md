# resignation-letter

[Agent Plugins 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) 形式のプラグインです。日本の退職届を、横書きA4のPDFとして生成します。Win / macOS / Linux で動作します。

会社名・宛先・氏名などの個人情報はパッケージに含みません。実行のたびに指定します。

## 必要環境

- Python 3.9+
- `reportlab`（`requirements.txt` を参照）
- 同梱の Noto Serif JP Regular（`assets/fonts/`）

## レイアウト

- A4・1枚・横書き
- 宛先は左上、標題「退　職　届」は中央、日付・所属・氏名は右下
- 日付は `2026年10月15日（木）` 形式（曜日つき）
- 印欄なし
- 宛先氏名は通称ではなく、登記上の漢字を使う

## インストール

このディレクトリをクライアントが読み込むプラグイン配置へコピーまたはシンボリックリンクします。

Cursor の場合:

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn /path/to/resignation-letter ~/.cursor/plugins/local/resignation-letter
```

依存関係:

```bash
python3 -m pip install -r requirements.txt
```

Agent Plugins 対応クライアントは、ルートの `plugin.json` を見て `skills/resignation-letter/` を発見します。

## 必須項目

エージェントは次をユーザーから取り、足りなければ聞きます。推測して埋めません。

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
| 保存先 | `--output` | `~/Desktop/退職届_氏名.pdf`（Desktop が無ければホーム） |

## 生成

スキルディレクトリをカレントにして実行します。

```bash
python3 skills/resignation-letter/scripts/generate.py \
  --company "株式会社見本" \
  --addressee "山田花子" \
  --department "営業部" \
  --name "佐藤　太郎" \
  --resign-date 2026-10-15
```

## 構成

```text
resignation-letter/
├── plugin.json
├── requirements.txt
├── skills/
│   └── resignation-letter/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── generate.py
│       └── assets/
│           └── fonts/
│               ├── NotoSerifJP-Regular.ttf
│               └── OFL.txt
├── LICENSE
├── CHANGELOG.md
└── README.md
```

Noto Serif JP は SIL Open Font License 1.1 です。ライセンス全文は `skills/resignation-letter/assets/fonts/OFL.txt` にあります。
