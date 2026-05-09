# ブランドアセット

## ロゴファイルの保存ルール

### マスター（このディレクトリ）

`assets/brand/` は**マスターアセット保管場所**。原寸・編集可能な形式（SVG・AI・PSD・PNG @ 高解像度）を置く。

```
assets/brand/
├── logo-full.{svg,png}              # フルロゴ（マーク + テキスト「オープン添削」+ タグライン）
├── logo-horizontal.{svg,png}        # 横型ロゴ（マーク + テキスト「オープン添削」、タグラインなし）
├── logo-mark.{svg,png}              # マークのみ（アイコン使用）
├── logo-text.{svg,png}              # テキストのみ
├── logo-monochrome.{svg,png}        # モノクロ版（白黒）
├── tagline.{svg,png}                # タグライン「ひらかれた、AI添削サービス」
└── README.md                        # 本ファイル（運用ルール）
```

### Web 配信（Astro）

`site/public/brand/` に**配信用コピー**を置く。サイズ違い・最適化版を生成して配置。

```
site/public/brand/
├── logo-full.svg                    # 原則 SVG 1ファイル
├── logo-horizontal.svg
├── logo-mark.svg
├── logo-mark-32.png                 # favicon等の派生
├── logo-mark-180.png                # apple-touch-icon
├── logo-mark-512.png                # PWA
└── og-default.png                   # OGP用 (1200x630)
```

ビルド時に Astro が `site/public/` の中身を `correction-app/frontend/` にミラーするので、配信URLは `/brand/<filename>` になる。

## 使用先

| 用途 | 参照先 | URL |
|---|---|---|
| ヘッダーロゴ（SPA） | `correction-app/frontend/index.html` | `/brand/logo-horizontal.svg` |
| 記事ヘッダー（Astro） | `site/src/components/Header.astro` | `/brand/logo-horizontal.svg` |
| favicon | `site/src/components/BaseHead.astro` | `/brand/logo-mark-32.png` |
| OGP 画像 | 各 frontmatter `ogImage` | `/brand/og-default.png` |
| メタ apple-touch-icon | `BaseHead.astro` | `/brand/logo-mark-180.png` |

## 配色

- メインブルー： `#1B468C`（マーク左半・テキスト「オープン」）
- アクセントターコイズ： `#3FBFB1`（マーク右半・テキスト「添削」・装飾ドット）
- グレーライン： `#A8AEB6`（マーク内 横線）
- 背景： `#FFFFFF`

## 禁止事項

- ロゴの色変更（赤系・別ブランドカラーへの差し替え）
- 縦横比の変形
- マークとテキストの相対位置変更
- タグライン文言の改変

## 履歴

- 2026-05-06 初回登録（フルロゴ）
