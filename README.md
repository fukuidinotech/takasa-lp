# タカサ LP

「タカサ」アプリ（iOS）のランディングページ。公開先は
<https://fukuidinotech.github.io/takasa-lp/>。

**7言語。ja は repo 直下、ほかは同名のサブディレクトリ**（`en/` `zh-Hans/` `zh-Hant/`
`ko/` `es/` `fr/`）。4ページ × 7言語 = 28ページ。

```
takasa-lp/
├── index.html privacy.html terms.html company.html   ← ja
├── en/ zh-Hans/ zh-Hant/ ko/ es/ fr/                 ← 各4ページ
├── site.css legal.css images/                        ← 全言語で共有
├── privacy-en.html terms-en.html company-en.html     ← 旧 URL の受け皿。消さない
└── tools/i18n.py                                     ← 共通部分の正本
```

共通部分（canonical / hreflang / 言語切替 / フッター / 更新日）は `tools/i18n.py` が
`<!--chrome:…-->` の目印のあいだに書き戻す。本文を直したら通すこと。

```
python3 tools/i18n.py           # 全ページに書き戻す
python3 tools/i18n.py --check   # ずれていたら異常終了
```

詳細は `CLAUDE.md` と `../docs/` を参照。
