---
name: resignation-letter
description: >-
  横書きA4の退職届PDFを、確定済みの公的書類フォーマットで生成する。
  Use when the user asks for 退職届, 退職願, a resignation letter, or to update
  an existing 退職届 PDF.
license: MIT
compatibility: Requires Python 3.9+, reportlab, and the bundled Noto Serif JP font
---

# 退職届 PDF

どの会社でも使える横書き退職届。体裁は確定済みなので、レイアウトをその場で組み直さない。生成は必ず同梱スクリプトに任せる。

会社名・宛先・所属・氏名はパッケージに持たない。ユーザーが明示した値だけ使う。足りなければ聞く。推測して埋めない。

## 確定フォーマット

- A4・1枚・横書き
- フォント: 同梱の Noto Serif JP Regular
- 宛先は左上、標題「退　職　届」は中央、日付・所属・氏名は右下
- 印欄・電子印は入れない
- 日付は必ず `2026年10月15日（木）` 形式（曜日つき、先頭ゼロなし）
- 宛先氏名は登記上の漢字。通称は使わない

## 必須（省略不可）

- 会社名
- 宛先氏名
- 所属
- 提出者氏名
- 退職日

## 任意（省略時のみ既定）

| 項目 | 省略時 |
| --- | --- |
| 宛先役職 | 代表取締役 |
| 事由 | 一身上の都合 |
| 提出日 | 実行日（Asia/Tokyo） |
| 保存先 | `~/Desktop/退職届_氏名.pdf`（Desktop が無ければホーム） |

## 手順

1. 必須項目が欠けていれば聞く。会社名・宛先・所属・氏名は会話の文脈があっても、ユーザーがこの書類用に言った値だけ使う。
2. 日付は `YYYY-MM-DD` に正規化する。
3. この `SKILL.md` と同じディレクトリをスキルルートにする。
4. プラグインルートで依存関係を入れる（未導入のときだけ）。

```bash
python3 -m pip install -r requirements.txt
```

5. スキル配下のスクリプトで PDF を生成する。

```bash
python3 scripts/generate.py \
  --company "株式会社見本" \
  --addressee-title "代表取締役" \
  --addressee "山田花子" \
  --department "営業部" \
  --name "佐藤　太郎" \
  --resign-date YYYY-MM-DD \
  --submit-date YYYY-MM-DD \
  --reason "一身上の都合" \
  --output "$HOME/Desktop/退職届_佐藤太郎.pdf"
```

`--addressee-title`、`--reason`、`--submit-date`、`--output` は省略してよい。

6. 生成後、プレビューして体裁を確認する。macOS では次でよい。

```bash
qlmanage -t -s 1600 -o /tmp "$HOME/Desktop/退職届_佐藤太郎.pdf"
```

確認ポイント: 宛先がユーザー指定の漢字、標題が中央、本文が3行で「をもって」が途中改行されていない、日付に曜日、印欄なし、見本の氏名が混入していない。

7. 保存パスをユーザーに伝える。印刷して提出する前提。書き換え依頼はその場でスクリプトを再実行して上書きする。

## 本文テンプレ

スクリプトが次の3行で組む。手で組み直さない。

```
このたび、{事由}により、
{退職日（曜日）}をもって
退職いたしたく、ここにお届けいたします。
```

## 禁止

- 同梱の `scripts/generate.py` 以外でレイアウトを再実装しない
- 印の円・「印」文字を描かない
- 宛先をカタカナ通称にする
- 会社名・宛先・所属・氏名を補完する
- reportlab が無いときにグローバルへ勝手にインストールしない。手順 4 を案内する
