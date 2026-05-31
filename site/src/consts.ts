// サイト全体の定数。各ページ・コンポーネントから import して使う

export const SITE_TITLE = 'オープン添削';
export const SITE_DESCRIPTION =
	'推薦・総合型選抜の志望理由書添削サービス。早慶上智MARCHを目指す高校3年生・保護者向けに、志望理由・面接・スケジュールをわかりやすく解説。';
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

// ナビゲーション（ヘッダー）— 運営者情報/お問い合わせはフッターのみ
export const NAV_LINKS = [
	{ href: '/articles', label: '記事一覧' },
];

// CTA設定
export const CTA = {
	heading: '志望理由書の無料診断を受ける',
	body: '大学・学部の評価観点をふまえて、あなたの志望理由書の改善点を無料で確認できます。',
	buttonLabel: '無料で相談する',
	buttonHref: '/#step1Sec',
	note: '3分で完了｜LINEで結果が届く｜無料添削サンプル付き',
};

// 大学メタ情報（カラー・表示順・ハブURL）
// カラーは各大学の公式・伝統色から派生したアクセント色
export const UNIVERSITIES = [
	// 1行目：早慶上智MARCH ＋ 関関同立
	{ slug: 'waseda',       name: '早稲田大学',     short: '早稲田',   color: '#7a1f1f', bg: '#fef2f2' },
	{ slug: 'keio',         name: '慶應義塾大学',   short: '慶應',     color: '#1f3a8a', bg: '#eef2ff' },
	{ slug: 'sophia',       name: '上智大学',       short: '上智',     color: '#7c2d4a', bg: '#fdf2f8' },
	{ slug: 'meiji',        name: '明治大学',       short: '明治',     color: '#581c87', bg: '#faf5ff' },
	{ slug: 'aoyama',       name: '青山学院大学',   short: '青山学院', color: '#0f766e', bg: '#ecfdf5' },
	{ slug: 'rikkyo',       name: '立教大学',       short: '立教',     color: '#9f1239', bg: '#fff1f2' },
	{ slug: 'chuo',         name: '中央大学',       short: '中央',     color: '#9a3412', bg: '#fff7ed' },
	{ slug: 'hosei',        name: '法政大学',       short: '法政',     color: '#c2410c', bg: '#fff7ed' },
	{ slug: 'kwansei',      name: '関西学院大学',   short: '関学',     color: '#16288b', bg: '#eef1ff' }, // 公式CSS「KGネイビー」
	{ slug: 'kansai',       name: '関西大学',       short: '関大',     color: '#313198', bg: '#eeeeff' }, // 公式SVG「紫紺」
	{ slug: 'doshisha',     name: '同志社大学',     short: '同志社',   color: '#660066', bg: '#faeeff' }, // 公式SVG「ロイヤルパープル」
	{ slug: 'ritsumeikan',  name: '立命館大学',     short: '立命館',   color: '#ac181e', bg: '#ffeef0' }, // 公式SVG「えんじ」
	// 2行目：ICU・理科大・日東駒専・産近甲龍
	{ slug: 'icu',          name: '国際基督教大学', short: 'ICU',      color: '#0055b8', bg: '#e8f2ff' }, // 公式SVG「ミッションブルー」
	{ slug: 'rikadai',      name: '東京理科大学',   short: '理科大',   color: '#009944', bg: '#e8f8ef' }, // 公式PNG「緑」
	{ slug: 'nihon',        name: '日本大学',       short: '日大',     color: '#d3381c', bg: '#fff1ee' }, // スクールカラー「緋色」
	{ slug: 'toyo',         name: '東洋大学',       short: '東洋',     color: '#17194c', bg: '#eef0ff' }, // PANTONE 281C「鉄紺」
	{ slug: 'komazawa',     name: '駒澤大学',       short: '駒澤',     color: '#492d65', bg: '#f5f0ff' }, // 公式CSS「紫」
	{ slug: 'senshu',       name: '専修大学',       short: '専修',     color: '#006f37', bg: '#edfaf3' }, // 公式SVG「グリーン」
	{ slug: 'kyoto-sangyo', name: '京都産業大学',   short: '京産大',   color: '#0d3387', bg: '#eef3ff' }, // 公式SVG「紺藍」
	{ slug: 'kindai',       name: '近畿大学',       short: '近大',     color: '#00507e', bg: '#e8f4fb' }, // 公式CSS「近大ブルー」
	{ slug: 'konan',        name: '甲南大学',       short: '甲南',     color: '#b31621', bg: '#ffeef0' }, // 公式CSS「臙脂」
	{ slug: 'ryukoku',      name: '龍谷大学',       short: '龍谷',     color: '#d60000', bg: '#fff0f0' }, // 公式CSS「龍谷レッド」
] as const;

export type UniversitySlug = typeof UNIVERSITIES[number]['slug'];

export const UNIV_COLOR_MAP: Record<string, { color: string; bg: string; name: string }> =
	Object.fromEntries(UNIVERSITIES.map((u) => [u.slug, { color: u.color, bg: u.bg, name: u.name }]));

// 大学スラッグから記事の冒頭セグメントを取得
export const getUnivFromSlug = (id: string): typeof UNIVERSITIES[number] | undefined => {
	const head = id.split('/')[0];
	return UNIVERSITIES.find((u) => u.slug === head);
};
