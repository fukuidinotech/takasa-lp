# takasa-lp

タカサ（iOSアプリ）のランディングページ。

## ⚠️ セキュリティ（最重要）

このリポジトリは **public + GitHub Pages で公開予定**。
インターネット全公開・履歴永続・インデックス対象になる。

### 絶対にコミット禁止
- APIキー・トークン・シークレット類（`.env`, `secrets/`, `credentials.*` は`.gitignore`済み）
- 自宅住所、電話番号、プライベートメールアドレス
- その他の本人識別に直結する個人情報

### 特定商取引法の運営者情報
- 自宅住所: 「請求があれば遅滞なく開示」パターンを採用（直載せしない）
- 電話番号: 同様
- 連絡先: 問い合わせ専用メール or 問い合わせフォーム経由
- 公開名義: `Toru Fukui`（App Store の著作権表記と統一）。フッターは `© 2026 Toru Fukui`、ポリシー・規約の提供者名も同じ

### コミット前チェック
- 新規ファイルに個人情報・秘密情報が混入していないか
- 自動生成ファイル（ビルド成果物、env等）がステージされていないか
- 公開されて困る情報が一切含まれていないか

### 漏洩時の対応
- APIキー等が混入した場合は即ローテーション
- 履歴からの完全削除は困難（他人にクローンされている可能性あり）
- ユーザーに即報告

## GitHub
- `gh` CLIには複数アカウントがログインしているため、`fukumone` で操作するときは
  必ず `GH_TOKEN=$(gh auth token --user fukumone)` を環境変数に渡してから
  `gh` / `git` コマンドを実行すること

## リポジトリ構成
- `takasa-app/` → GitHub: `fukumone/takasa-app`（iOSアプリ本体、private）
- `../docs/`   → **ローカルgitのみ**（GitHubには上げない。企画書・チケット・設計書）
- `takasa-lp/` → GitHub: `fukuidinotech/takasa-lp`（このリポジトリ、**public**。GitHub Pages で公開中）

## 構成（2026-09-20〜）

**7言語。ja は repo 直下、ほかは同名のサブディレクトリ。**
公開済みの `…/takasa-lp/` を動かさないため、ja だけディレクトリを持たない。

```
takasa-lp/
├── index.html privacy.html terms.html company.html   ← ja
├── en/ zh-Hans/ zh-Hant/ ko/ es/ fr/                 ← 各4ページ（同じファイル名）
├── site.css legal.css images/                        ← 全言語で共有（1つだけ置く）
├── privacy-en.html terms-en.html company-en.html     ← 旧 URL の受け皿。消さない
└── tools/i18n.py                                     ← 共通部分の正本
```

- `<head>` の alternate・言語切替・フッター・更新日は **`tools/i18n.py` が生成する**。
  `<!--chrome:…-->` の目印のあいだは手で書かない。直したら `python3 tools/i18n.py`
- 手で書くのは `<title>` / `<meta name="description">` / og と本文だけ
- 更新日は `<p class="updated" data-updated="YYYY-MM-DD">` の日付だけ直せば7言語ぶん揃う
- **JS は置かない。** 言語の自動振り分けも入れない（入口は hreflang と言語切替に任せる）
- **文章の正本は日本語。** 直下を直してから6言語へ反映し、法務ページには
  「相違があれば日本語版が優先」の注記（`.i18n-note`）を入れる
- 言語を足す／減らすときは `tools/i18n.py` の `LANGS`、アプリの `SiteLinks.swift`、
  `fastlane/metadata/<locale>/marketing_url.txt`（と `support_url.txt`）を同時に直す
