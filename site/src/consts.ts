// サイト全体の定数。各ページ・コンポーネントから import して使う

export const SITE_TITLE = 'オープン添削';
export const SITE_DESCRIPTION =
	'採用人事10年・総合型選抜指導100名以上の講師が監修する、推薦・総合型選抜の志望理由書添削サービス。早慶上智MARCHを目指す高校3年生・保護者向けの志望理由・面接・スケジュール解説。';
export const SITE_URL = 'https://open-tensaku.com';

// SEO・OGP
export const SITE_OG_IMAGE = '/og/default.png';
export const TWITTER_HANDLE = '@open_tensaku'; // 取得後に更新

// 監修者プロフィール
export const SUPERVISOR = {
	name: 'オープン添削 主任講師',
	short:
		'上場企業 新卒採用10年｜総合型選抜講師4年・指導100名以上｜早慶上智MARCH合格者多数',
	full: '上場企業の人事部にて新卒採用を10年担当し、延べ数千人の志望動機・自己PRを面接官として評価。その後、大手総合型選抜専門塾で4年間に100名以上の受験生を指導し、早慶上智MARCHを中心に多数の合格者を輩出。「大学合格をゴールにしない志望理由書」を理念に、企業が将来求める人材像から逆算した指導を行う。人事担当者・現役大学生への一次取材で得た最新の知見を、添削とアドバイスに反映している。',
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
	body: '採用人事10年×総合型選抜指導100名以上の講師が、あなたの志望理由書を無料で添削します。',
	buttonLabel: '無料で相談する',
	buttonHref: '/contact',
};
