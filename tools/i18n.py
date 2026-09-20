#!/usr/bin/env python3
"""takasa-lp の共通部分（head の alternate・言語切替・フッター・更新日）を
全言語ぶん書き戻す。

各 HTML は次の3つの目印を持つ。目印のあいだはこのスクリプトが上書きするので、
手で書かない。目印の外（title / description / og / 本文）だけを手で書く。

    <!--chrome:alt-->  ... <!--/chrome:alt-->    canonical / hreflang / フォント / css
    <!--chrome:lang--> ... <!--/chrome:lang-->   言語切替（JS を使わないただのリンク）
    <!--chrome:foot--> ... <!--/chrome:foot-->   フッター

法務ページの更新日は `<p class="updated" data-updated="YYYY-MM-DD">` の日付から
言語ごとの書き方で埋める。**日付を直すのは1か所だけ**でよい。

使い方: python3 tools/i18n.py        （全ファイルを書き戻す）
        python3 tools/i18n.py --check（差分が出るなら異常終了）
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://fukuidinotech.github.io/takasa-lp/"

# ja は repo 直下。公開済みの URL（App Store の marketing_url・アプリ内リンク）を
# 動かさないため、ja だけサブディレクトリを持たない
PAGES = ["index.html", "privacy.html", "terms.html", "company.html"]
LEGAL = ["privacy.html", "terms.html", "company.html"]
CONTACT = "fukuidinotech@gmail.com"

LANGS = {
    "ja": {
        "dir": "", "native": "日本語", "pick": "言語を選ぶ",
        "app": "タカサ", "tagline": "建物の高さを測るiOSアプリ",
        "privacy.html": "プライバシーポリシー", "terms.html": "利用規約",
        "company.html": "運営者情報", "contact": "お問い合わせ",
        "updated": "最終更新日", "date": "{y}年{m}月{d}日",
    },
    "en": {
        "dir": "en", "native": "English", "pick": "Choose a language",
        "app": "Takasa", "tagline": "an iOS app for measuring height",
        "privacy.html": "Privacy Policy", "terms.html": "Terms of Use",
        "company.html": "Operator Information", "contact": "Contact",
        "updated": "Last updated", "date": "{month} {d}, {y}",
    },
    "zh-Hans": {
        "dir": "zh-Hans", "native": "简体中文", "pick": "选择语言",
        "app": "Takasa", "tagline": "测量高度的 iOS 应用",
        "privacy.html": "隐私政策", "terms.html": "使用条款",
        "company.html": "运营者信息", "contact": "联系我们",
        "updated": "最后更新", "date": "{y}年{m}月{d}日",
    },
    "zh-Hant": {
        "dir": "zh-Hant", "native": "繁體中文", "pick": "選擇語言",
        "app": "Takasa", "tagline": "測量高度的 iOS 應用程式",
        "privacy.html": "隱私政策", "terms.html": "使用條款",
        "company.html": "營運者資訊", "contact": "聯絡我們",
        "updated": "最後更新", "date": "{y}年{m}月{d}日",
    },
    "ko": {
        "dir": "ko", "native": "한국어", "pick": "언어 선택",
        "app": "Takasa", "tagline": "높이를 재는 iOS 앱",
        "privacy.html": "개인정보 처리방침", "terms.html": "이용약관",
        "company.html": "운영자 정보", "contact": "문의하기",
        "updated": "최종 업데이트", "date": "{y}년 {m}월 {d}일",
    },
    "es": {
        "dir": "es", "native": "Español", "pick": "Elegir idioma",
        "app": "Takasa", "tagline": "una app de iOS para medir alturas",
        "privacy.html": "Política de privacidad", "terms.html": "Términos de uso",
        "company.html": "Información del operador", "contact": "Contacto",
        "updated": "Última actualización", "date": "{d} de {month} de {y}",
    },
    "fr": {
        "dir": "fr", "native": "Français", "pick": "Choisir la langue",
        "app": "Takasa", "tagline": "une app iOS pour mesurer les hauteurs",
        "privacy.html": "Politique de confidentialité", "terms.html": "Conditions d'utilisation",
        "company.html": "Informations sur l'éditeur", "contact": "Contact",
        "updated": "Dernière mise à jour", "date": "{d} {month} {y}",
    },
}

# 月の名前が要る言語だけ持つ（ja / zh / ko は数字で書く）
MONTHS = {
    "en": ["", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"],
    "es": ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
           "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "fr": ["", "janvier", "février", "mars", "avril", "mai", "juin",
           "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
}


def url_for(lang: str, page: str) -> str:
    d = LANGS[lang]["dir"]
    return BASE + (f"{d}/{page}" if d else page)


def rel(from_lang: str, to_lang: str, page: str) -> str:
    src, dst = LANGS[from_lang]["dir"], LANGS[to_lang]["dir"]
    if src == dst:
        return page
    up = "../" if src else ""
    return f"{up}{dst}/{page}" if dst else f"{up}{page}"


def asset(lang: str, name: str) -> str:
    """css と images は repo 直下に1つだけ置く"""
    return f"../{name}" if LANGS[lang]["dir"] else name


_versions: dict[str, str] = {}


def css_version(name: str) -> str:
    """css の中身から作る短い印。**手で上げない。**

    HTML と CSS は別々にキャッシュされる。GitHub Pages は両方に `max-age=600` を
    付けるので、CSS を変えた直後は「新しい HTML ＋ 古い CSS」で見る人が出る。
    URL に中身の印を入れておけば、直した時点で URL も変わるので必ず取り直しになる。
    """
    if name not in _versions:
        _versions[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:8]
    return _versions[name]


def date_text(lang: str, iso: str) -> str:
    y, m, d = (int(v) for v in iso.split("-"))
    cfg = LANGS[lang]
    month = MONTHS[lang][m] if "{month}" in cfg["date"] else ""
    return f'{cfg["updated"]}: ' + cfg["date"].format(y=y, m=m, d=d, month=month)


def block_alt(lang: str, page: str) -> str:
    lines = [f'<link rel="canonical" href="{url_for(lang, page)}">']
    for other in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{other}" href="{url_for(other, page)}">')
    # 一致する言語が無い人には英語を出す
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{url_for("en", page)}">')
    lines.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    lines.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    lines.append('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600'
                 '&display=swap" rel="stylesheet">')
    css = "site.css" if page == "index.html" else "legal.css"
    lines.append(f'<link rel="stylesheet" href="{asset(lang, css)}?v={css_version(css)}">')
    return "\n".join(lines)


# **言語の自動振り分け（JS）は入れない。**
#
# 2026-09-20 に「1 URL ＋ JS で辞書を差し替え」から言語別サブディレクトリへ移した。
# 入口の振り分けは hreflang（block_alt）と言語切替（block_lang）に任せる。
# kakesu-lp で一度 JS の振り分けを入れて外した経緯がある（外から書ける値を遷移先に
# 使うので、検証を1つ落とすと外部 URL へ飛ばせる穴になる）。同じものを作り直さない。


def block_lang(lang: str, page: str) -> str:
    out = [f'<div class="langbar" role="navigation" aria-label="{LANGS[lang]["pick"]}">']
    for other, cfg in LANGS.items():
        cur = ' aria-current="true"' if other == lang else ""
        out.append(f'  <a lang="{other}" hreflang="{other}" '
                   f'href="{rel(lang, other, page)}"{cur}>{cfg["native"]}</a>')
    out.append('</div>')
    return "\n".join(out)


def block_foot(lang: str, page: str) -> str:
    cfg = LANGS[lang]
    out = ['<footer>']
    if page == "index.html":
        links = [f'<a href="{p}">{cfg[p]}</a>' for p in LEGAL]
        links.append(f'<a href="mailto:{CONTACT}">{cfg["contact"]}</a>')
        out.append('  <p>')
        out += [f'    {a}' for a in links]
        out.append('  </p>')
        out.append(f'  <p>{cfg["app"]} — {cfg["tagline"]}</p>')
    else:
        out.append(f'  <p><a href="index.html">{cfg["app"]}</a> — {cfg["tagline"]}</p>')
        others = " / ".join(f'<a href="{p}">{cfg[p]}</a>' for p in LEGAL if p != page)
        out.append(f'  <p>{others}</p>')
    out.append('  <p>&copy; 2026 Toru Fukui</p>')
    out.append('</footer>')
    return "\n".join(out)


BLOCKS = {"alt": block_alt, "lang": block_lang, "foot": block_foot}


def apply(text: str, lang: str, page: str) -> str:
    for key, fn in BLOCKS.items():
        pattern = re.compile(f"(<!--chrome:{key}-->).*?(<!--/chrome:{key}-->)", re.S)
        if not pattern.search(text):
            raise SystemExit(f"目印 chrome:{key} が無い: {lang}/{page}")
        text = pattern.sub(lambda m: f"{m.group(1)}\n{fn(lang, page)}\n{m.group(2)}", text)
    text = re.sub(r'(<p class="updated" data-updated="(\d{4}-\d{2}-\d{2})">).*?(</p>)',
                  lambda m: f"{m.group(1)}{date_text(lang, m.group(2))}{m.group(3)}", text, flags=re.S)
    text = re.sub(r'<html lang="[^"]*">', f'<html lang="{lang}">', text, count=1)
    return text


def main() -> int:
    check = "--check" in sys.argv
    stale, missing = [], []
    for lang, cfg in LANGS.items():
        for page in PAGES:
            path = (ROOT / cfg["dir"] / page) if cfg["dir"] else (ROOT / page)
            if not path.exists():
                missing.append(str(path.relative_to(ROOT)))
                continue
            before = path.read_text(encoding="utf-8")
            after = apply(before, lang, page)
            if before != after:
                stale.append(str(path.relative_to(ROOT)))
                if not check:
                    path.write_text(after, encoding="utf-8")

    for name in missing:
        print(f"無い: {name}")
    for name in stale:
        print(("ずれ: " if check else "直した: ") + name)
    if check and (stale or missing):
        return 1
    if missing:
        return 1
    if not stale:
        print("共通部分は全ページ一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
