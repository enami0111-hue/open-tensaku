// @ts-check
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

export default defineConfig({
	site: 'https://open-tensaku.com',
	outDir: '../correction-app/frontend',
	integrations: [mdx(), sitemap()],
	markdown: {
		shikiConfig: {
			theme: 'github-light',
			wrap: true,
		},
	},
	// 旧フラットURL → 新カテゴリURL の 301 リダイレクト（SEO・既存リンク保護）
	redirects: {
		'/articles/basics-what-is-sougou':        '/articles/basics/what-is-sougou',
		'/articles/schedule-2026':                '/articles/schedule/2026',
		'/articles/writing-howto-basic':          '/articles/writing/howto-basic',
		'/articles/writing-kakidashi':            '/articles/writing/kakidashi',
		'/articles/activity-katsudou-houkoku':    '/articles/activity/katsudou-houkoku',
		'/articles/interview-top5':               '/articles/interview/top5',
		'/articles/interview-shiboudouki':        '/articles/interview/shiboudouki',
		'/articles/parent-system-guide':          '/articles/parent/system-guide',
		'/articles/parent-cost-guide':            '/articles/parent/cost-guide',
		'/articles/parent-support-guide':         '/articles/parent/support-guide',
		'/articles/parent-risk-management':       '/articles/parent/risk-management',
		'/articles/parent-after-admission':       '/articles/parent/after-admission',
		// 大学ハブは /articles/waseda/ に統一
		'/articles/waseda-shibou-riyu':           '/articles/waseda',
		'/articles/waseda/shibou-riyu':           '/articles/waseda',
		// 学部 → 学部/入試方式 へ移行
		'/articles/waseda-seikei-shibou-riyu':    '/articles/waseda/seikei/global',
		'/articles/waseda/seikei':                '/articles/waseda/seikei/global',
		'/articles/waseda-hogaku-shibou-riyu':    '/articles/waseda/hogaku/suisen',
		'/articles/waseda/hogaku':                '/articles/waseda/hogaku/suisen',
		'/articles/waseda-shogaku-shibou-riyu':   '/articles/waseda/shogaku/suisen',
		'/articles/waseda/shogaku':               '/articles/waseda/shogaku/suisen',
		'/articles/waseda-sils-shibou-riyu':      '/articles/waseda/sils/eng-sop',
		'/articles/waseda/sils':                  '/articles/waseda/sils/eng-sop',
		'/articles/waseda-kyoiku-shibou-riyu':    '/articles/waseda/kyoiku/suisen',
		'/articles/waseda/kyoiku':                '/articles/waseda/kyoiku/suisen',
		'/articles/waseda-shakai-shibou-riyu':    '/articles/waseda/shakai/zenkoku-jisuisen',
		'/articles/waseda/shakai':                '/articles/waseda/shakai/zenkoku-jisuisen',
		'/articles/waseda-bunkakoso-shibou-riyu': '/articles/waseda/bunkakoso/suisen',
		'/articles/waseda/bunkakoso':             '/articles/waseda/bunkakoso/suisen',
	},
	vite: {
		build: {
			emptyOutDir: false,
		},
	},
});
