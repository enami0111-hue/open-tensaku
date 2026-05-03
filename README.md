# オープン添削

推薦・総合型選抜の志望理由書添削サービス「オープン添削」のマーケティングサイト。

## サービス概要

- AIによる書類添削サービスのサイト。総合型選抜や推薦入試（旧AO入試）に関する情報も発信
- 監修：採用人事10年×総合型選抜講師4年・指導100名以上
- 早慶上智MARCHを中心とした私立上位校を目指す高校3年生・保護者が対象

## 技術スタック

- **Astro v6**（静的サイトジェネレータ）
- **TypeScript** (strict)
- **Cloudflare Pages**（ホスティング・CDN）
- **GitHub**（リポジトリ）

## ディレクトリ構成

```
.
├── site/                      # Astroサイト本体
│   ├── src/
│   │   ├── pages/             # トップ・記事・運営者・お問合せ等
│   │   ├── layouts/           # ArticleLayout
│   │   ├── components/        # ヘッダ・フッタ・監修者ボックス・CTA等
│   │   ├── content/articles/  # 記事Markdown（articles/ から複製）
│   │   ├── consts.ts          # サイト全体の定数
│   │   └── content.config.ts  # コンテンツコレクションスキーマ
│   ├── public/                # 静的アセット（OGP画像・robots.txt等）
│   └── astro.config.mjs
├── articles/                  # 記事Markdown（マスター）
├── docs/
│   ├── templates/             # 記事制作の標準テンプレ・SEOチェックリスト
│   └── 事業計画書_AI志望理由書添削サービス.docx
├── assets/                    # ロゴ・画像素材
└── CLAUDE.md                  # Claude Code向けプロジェクトコンテキスト
```

## 開発

```bash
cd site
npm install
npm run dev    # ローカル開発サーバー http://localhost:4321
npm run build  # プロダクションビルド (dist/)
npm run preview  # ビルド成果物のプレビュー
```

## デプロイ（Cloudflare Pages）

- **ビルドコマンド**: `cd site && npm install && npm run build`
- **出力ディレクトリ**: `site/dist`
- **ルートディレクトリ**: `/`
- **Node バージョン**: 22.x 以上

## 記事制作フロー

1. 記事タイプに応じて `docs/templates/` のテンプレを使用
   - ハブ記事：`article-hub-template.md`
   - 学部別記事：`article-faculty-template.md`
   - 英語入試記事：`article-eigo-template.md`
2. `articles/{slug}.md` として記事を執筆
3. `site/src/content/articles/` にコピー（または直接書く）
4. 公開前に `docs/templates/seo-checklist.md` でチェック
5. `git push` で Cloudflare Pages が自動デプロイ
