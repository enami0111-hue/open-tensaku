---
name: article-file-conventions
description: 記事のディレクトリ構造・スラッグ命名・配置ルール。新しい記事を追加するとき・記事のファイル名やディレクトリを決めるとき・大学/学部/入試方式別記事を整理するとき必ず参照する。「記事追加して」「○○大学の記事をつくって」「ファイル名どうする？」と言われたら発動。
version: 1.0
---

# 記事ファイル命名・配置ルール

オープン添削サイトの記事を追加・整理する際の絶対ルール。`docs/article-naming-conventions.md` の正本に従う。

## 発動条件

- 新規記事のファイル配置を決めるとき
- 既存記事のリネーム/移動を検討するとき
- 大学別・学部別・入試方式別記事を追加するとき
- 一覧ページのカテゴリ整理に関わるとき

## 全体構造

```
src/content/articles/
├── basics/                # 基礎知識
├── schedule/              # 年度別スケジュール
├── writing/               # 志望理由書の書き方（汎用）
├── activity/              # 活動報告書
├── interview/             # 面接対策（汎用）
├── parent/                # 保護者向け
└── <大学スラッグ>/         # 大学別ハブ + 学部 × 入試方式
    ├── index.md           # 大学ハブ（必須）
    └── <学部>/
        └── <入試方式>.md
```

## 大学スラッグ一覧（追加するときも本表に追記）

| 大学 | スラッグ |
|---|---|
| 早稲田大学 | `waseda` |
| 慶應義塾大学 | `keio` |
| 上智大学 | `sophia` |
| 明治大学 | `meiji` |
| 青山学院大学 | `aoyama` |
| 立教大学 | `rikkyo` |
| 中央大学 | `chuo` |
| 法政大学 | `hosei` |

英字略称が公式に使われている場合は英字優先（例：`sfc`, `fnc`, `sils`）。それ以外はローマ字短縮（公式略称があればそれを使う：`seikei`, `shogaku`, `hogaku`, `kyoiku`, `shakai`, `bunkakoso`）。

## 入試方式スラッグ一覧

| 入試方式 | スラッグ |
|---|---|
| 指定校推薦・系属校推薦 | `suisen` |
| 自己推薦（学校長推薦） | `jisuisen` |
| 全国自己推薦 | `zenkoku-jisuisen` |
| 公募推薦 | `koubo` |
| AO入試（旧称） | `ao` |
| 総合型選抜 | `sogo` |
| グローバル入試（早稲田 政経・社学等） | `global` |
| 英文 SoP 出願（SILS等） | `eng-sop` |
| FIT入試（慶應 法） | `fit` |
| EDESSA・EDESS（早稲田 政経） | `edess` |
| 帰国生入試 | `kikoku` |

新方式が登場したら、本表と `docs/article-naming-conventions.md` に追記する。

## ❌ NEVER

- ハイフン繋ぎのフラット命名（× `waseda-seikei-shibou-riyu.md` → ✅ `waseda/seikei/global.md`）
- 1学部1ファイルで複数の入試方式を混在させる（読者が探しにくい・SEOで薄まる）
- スラッグに日本語・大文字・スペース
- 学部スラッグの不統一（例：早稲田だけローマ字、慶應だけ英字、では一貫性なし）
- 大学ハブを `index.md` 以外で作る（受験生は `/articles/<大学>/` で大学トップに到達したい）
- frontmatter の `category` を「早稲田」等の大学名にする（→ `category` はトピック分類専用、大学はディレクトリで判定される）

## ✅ MUST

### 新記事追加時の手順

1. **ファイル配置を決める**
   - 大学別 → `<大学>/<学部>/<入試方式>.md`
   - 大学ハブ → `<大学>/index.md`
   - 汎用 → `<カテゴリ>/<slug>.md`

2. **frontmatter を設定**
   - `title`、`description`、`date`、`audience`（必須）
   - `category` はトピック分類（基礎知識／志望理由書／面接対策／保護者向け 等）
   - `keywords`、`updatedDate`、`schema` は任意

3. **`correction-app/frontend/index.html` の ARTICLE_DB と ARTICLES_BY_FAC（または ARTICLES_BY_UNIV）を更新**
   - 新記事を「迷ったらまず読む」セクションに出す場合は必須

4. **既存URL からの誘導があれば `site/astro.config.mjs` の `redirects` を更新**

5. **`npm run build` で確認**：
   - `correction-app/frontend/articles/<新パス>/index.html` が生成されているか
   - `sitemap-0.xml` に新URLが含まれているか
   - 旧URL → 新URL のリダイレクトHTML が存在するか

## 例

### 早稲田 政経の自己推薦記事を追加するとき
```
ファイル:  src/content/articles/waseda/seikei/jisuisen.md
URL:      /articles/waseda/seikei/jisuisen/
```

### 慶應 SFC AO 記事を追加するとき
```
ファイル:
  src/content/articles/keio/index.md           # 大学ハブ（最初に作る）
  src/content/articles/keio/sfc/ao.md          # SFC AO
  src/content/articles/keio/sfc/jiyuukenkyu.md # SFC 自由研究方式
URL:
  /articles/keio/                              # 大学ハブ
  /articles/keio/sfc/ao/                       # 個別
```

### 上智 国際教養 公募推薦を追加するとき
```
ファイル:
  src/content/articles/sophia/index.md             # 上智ハブ（初回のみ）
  src/content/articles/sophia/global-studies/koubo.md
URL:      /articles/sophia/global-studies/koubo/
```

## 連携ポイント

- `motivation-article-writer` スキルで記事を書き起こすときは、本ルールに従ってファイル配置すること
- 一覧ページの `resolveCategory()` がディレクトリ先頭セグメント（`waseda`, `keio` 等）を見て「早稲田大学」「慶應義塾大学」等のセクションに自動振り分け
- ディレクトリ構造を変更する場合は `docs/article-naming-conventions.md` の本則を更新したうえで、本スキルにも反映する

## 正本

最新ルールは常に `docs/article-naming-conventions.md` 参照。本スキルは要点を抜粋した運用早見表。
