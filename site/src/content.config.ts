import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// 記事コレクション（既存 articles/*.md のfrontmatterに合わせたスキーマ）
const articles = defineCollection({
	loader: glob({ base: './src/content/articles', pattern: '**/*.{md,mdx}' }),
	schema: z.object({
			title: z.string(),
			description: z.string(),
			category: z.string(),
			audience: z.string(),
			date: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			keywords: z.array(z.string()).optional(),
			supervisor: z.string().optional(),
			type: z.enum(['hub', 'faculty', 'exam-format', 'general']).optional(),
			parent_hub: z.string().optional(),
			schema: z.array(z.string()).optional(),
			heroImage: z.string().optional(),
			ogImage: z.string().optional(),
			draft: z.boolean().optional().default(false),
		showBanner: z.boolean().optional().default(false),
		}),
});

export const collections = { articles };
