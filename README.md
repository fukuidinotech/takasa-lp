<p align="center">
  <img src="images/app-icon.png" width="120" alt="タカサ アイコン">
</p>

<h1 align="center">タカサ</h1>

<p align="center">
  Measure building heights with your iPhone camera and your own steps.<br>
  iPhone のカメラと歩数だけで、建物の高さをその場で測れる iOS アプリです。
</p>

<p align="center">
  <a href="https://apps.apple.com/jp/app/id6808973098">
    <img src="https://toolbox.marketingtools.apple.com/api/badges/download-on-the-app-store/black/ja-jp?size=250x83" alt="App Store からダウンロード" height="44">
  </a>
</p>

<p align="center">
  <a href="https://fukuidinotech.github.io/takasa-lp/">https://fukuidinotech.github.io/takasa-lp/</a>
</p>

## 構成

**7言語。ja は repo 直下、ほかは同名のサブディレクトリ。**
公開済みの `…/takasa-lp/` を動かさないため、ja だけディレクトリを持ちません。

```
takasa-lp/
├── index.html privacy.html terms.html company.html   ← ja
├── en/ zh-Hans/ zh-Hant/ ko/ es/ fr/                 ← 各4ページ（同じファイル名）
├── site.css  legal.css  images/                      ← 全言語で共有（1つだけ置く）
├── privacy-en.html terms-en.html company-en.html     ← 旧 URL の受け皿。消さない
└── tools/i18n.py                                     ← 共通部分の正本
```

2026-09-20 に「JS で辞書を差し替える1 URL」からこの形へ移しました。
言語別の URL があると、App Store の `marketing_url` をロケール別に出せて、
`hreflang` で検索エンジンにも言語別のページとして拾ってもらえます。
**ページに JS は1行も置きません。**

`privacy-en.html` / `terms-en.html` / `company-en.html` は出荷済みアプリ（v1.0.0）が
直接開く URL です。いまは `en/` へ送るだけの受け皿なので、消さないでください。

### 共通部分は手で書かない

各ページの `<head>` の alternate、言語切替、フッター、法務ページの更新日は
**`tools/i18n.py` が生成します。** 目印のあいだは上書きされます。

```
<!--chrome:alt-->  …  <!--/chrome:alt-->    canonical / hreflang / フォント / css
<!--chrome:lang--> …  <!--/chrome:lang-->   言語切替（JS を使わないただのリンク）
<!--chrome:foot--> …  <!--/chrome:foot-->   サイトフッター
```

```
python3 tools/i18n.py           # 全ページに書き戻す
python3 tools/i18n.py --check   # ずれていたら異常終了（/lp-sync が使う）
```

手で書くのは `<title>` と `<meta name="description">`、og、そして本文だけです。
更新日は `<p class="updated" data-updated="YYYY-MM-DD">` の日付だけ直せば、
7言語ぶんの書き方（`2026年9月5日` / `September 5, 2026` / …）が揃います。

**言語を足す／減らすときは3か所を同時に直します。**
`tools/i18n.py` の `LANGS`、アプリの `Takasa/Services/SiteLinks.swift`、
`fastlane/metadata/<locale>/marketing_url.txt`（と `support_url.txt`）。

### 文章の正本は日本語

本文を変えるときは **日本語（repo 直下の4ページ）を直してから、6言語へ反映**します。
法務ページの翻訳には「本翻訳は参考用であり、相違がある場合は日本語版が優先する」旨の
注記（`.i18n-note`）を各言語で入れてあります。
