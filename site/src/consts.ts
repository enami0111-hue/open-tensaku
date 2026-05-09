// サイト全体の定数。各ページ・コンポーネントから import して使う

export const SITE_TITLE = 'オープン添削';
export const SITE_DESCRIPTION =
	'新卒採用10年・1,000人以上の志望動機を評価した講師が監修する、推薦・総合型選抜の志望理由書添削サービス。早慶上智MARCHを目指す高校3年生・保護者向けの志望理由・面接・スケジュール解説。';
export const SITE_URL = 'https://open-tensaku.com';

// SEO・OGP
export const SITE_OG_IMAGE = '/brand/og-default.png';
export const TWITTER_HANDLE = '@open_tensaku'; // 取得後に更新

// 監修者プロフィール
export const SUPERVISOR = {
	name: 'オープン添削 主任講師',
	short:
		'新卒採用10年・1,000人以上の志望動機を評価｜総合型選抜専門塾4年・100名以上指導｜早慶上智MARCH多数合格',
	full: '上場企業にて新卒採用に10年携わり、1,000人以上の志望動機や自己PRを評価。その傍ら、大手総合型選抜専門塾で4年間に100名以上の受験生を指導し、早慶上智MARCHを中心に多数の合格者を輩出。「大学合格をゴールにしない志望理由書」を理念に、企業が将来求める人材像から逆算した指導を行う。人事担当者・現役大学生との直接接点で得た独自の知見を、添削とアドバイスに反映している。',
};

// ナビゲーション
export const NAV_LINKS = [
	{ href: '/', label: 'ホーム' },
	{ href: '/articles', label: '記事一覧' },
	{ href: '/about', label: '運営者情報' },
	{ href: '/contact', label: 'お問い合わせ' },
];

// CTA設定
export const CTA = {
	heading: '志望理由書の無料診断を受ける',
	body: '新卒採用10年・1,000人以上の志望動機を評価した講師が、あなたの志望理由書を無料で添削します。',
	buttonLabel: '無料で相談する',
	buttonHref: '/contact',
	note: '3分で完了｜LINEで結果が届く｜無料添削サンプル付き',
};

// 大学メタ情報（カラー・表示順・ハブURL）
// カラーは各大学の公式・伝統色から派生したアクセント色
export const UNIVERSITIES = [
	{ slug: 'waseda',  name: '早稲田大学',     short: '早稲田',   color: '#7a1f1f', bg: '#fef2f2' },
	{ slug: 'keio',    name: '慶應義塾大学',   short: '慶應',     color: '#1f3a8a', bg: '#eef2ff' },
	{ slug: 'sophia',  name: '上智大学',       short: '上智',     color: '#7c2d4a', bg: '#fdf2f8' },
	{ slug: 'meiji',   name: '明治大学',       short: '明治',     color: '#581c87', bg: '#faf5ff' },
	{ slug: 'aoyama',  name: '青山学院大学',   short: '青山学院', color: '#0f766e', bg: '#ecfdf5' },
	{ slug: 'rikkyo',  name: '立教大学',       short: '立教',     color: '#9f1239', bg: '#fff1f2' },
	{ slug: 'chuo',    name: '中央大学',       short: '中央',     color: '#9a3412', bg: '#fff7ed' },
	{ slug: 'hosei',   name: '法政大学',       short: '法政',     color: '#c2410c', bg: '#fff7ed' },
] as const;

export type UniversitySlug = typeof UNIVERSITIES[number]['slug'];

export const UNIV_COLOR_MAP: Record<string, { color: string; bg: string; name: string }> =
	Object.fromEntries(UNIVERSITIES.map((u) => [u.slug, { color: u.color, bg: u.bg, name: u.name }]));

// 大学スラッグから記事の冒頭セグメントを取得
export const getUnivFromSlug = (id: string): typeof UNIVERSITIES[number] | undefined => {
	const head = id.split('/')[0];
	return UNIVERSITIES.find((u) => u.slug === head);
};
