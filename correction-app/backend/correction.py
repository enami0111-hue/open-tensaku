"""Claude APIで志望理由書を添削。Good&More + アドミポリ動的注入 + プロンプトキャッシュ。"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
# 新スキル（130件分析ベース）。frontmatter付きSKILL.md形式で `correction-app/skills.md` に配置。
SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "skills.md"
# fallback: skills.md が読めない場合は旧プロンプトに戻す（retire予定）
LEGACY_PROMPT_PATH = Path(__file__).parent / "prompts" / "red_pen_system.md"


def _strip_frontmatter(text: str) -> str:
    """SKILL.md形式の先頭YAMLフロントマター（--- ... ---）を除去。"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip()
    return text


def _load_system_prompt() -> str:
    try:
        raw = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
        return _strip_frontmatter(raw)
    except FileNotFoundError:
        return LEGACY_PROMPT_PATH.read_text(encoding="utf-8")


def _build_context_block(
    university_name: str,
    faculty_name: str,
    course_name: str,
    admission_policy: str,
    question_title: str,
    question_body: str,
    question_year: int,
    question_status: str,
    char_limit: int | None,
) -> str:
    year_label = "当年度" if question_status == "official" else "前年度（参考）"
    char_note = f"推奨字数：{char_limit}字程度" if char_limit else "字数指定なし"
    return f"""# 受験生のコンテキスト

## 志望先
- 大学：{university_name}
- 学部：{faculty_name}
- コース：{course_name}

## アドミッションポリシー（添削の根拠とすること）
{admission_policy}

## 設問（{year_label}：{question_year}年度）
### {question_title}
{char_note}

{question_body}
"""


def correct_essay(
    *,
    university_name: str,
    faculty_name: str,
    course_name: str,
    admission_policy: str,
    question_title: str,
    question_body: str,
    question_year: int,
    question_status: str,
    char_limit: int | None,
    student_body: str,
) -> dict[str, Any]:
    """添削実行。返却は {comments, encouragement, summary} のJSONそのまま。

    ANTHROPIC_API_KEY が未設定の場合はモック添削を返す（UI検証・デモ用）。
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _mock_correction(student_body, question_title, university_name, faculty_name)
    client = Anthropic(api_key=api_key)
    system_prompt = _load_system_prompt()
    context_block = _build_context_block(
        university_name=university_name,
        faculty_name=faculty_name,
        course_name=course_name,
        admission_policy=admission_policy,
        question_title=question_title,
        question_body=question_body,
        question_year=question_year,
        question_status=question_status,
        char_limit=char_limit,
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=[
            {"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": context_block, "cache_control": {"type": "ephemeral"}},
        ],
        messages=[
            {
                "role": "user",
                "content": f"# 受験生の志望理由書（添削対象）\n\n{student_body}\n\n上記を Good＆More アプローチで添削し、JSONで返してください。",
            }
        ],
    )

    text = "".join(block.text for block in response.content if block.type == "text")
    return _parse_json(text)


def _mock_correction(student_body: str, question_title: str, university_name: str, faculty_name: str) -> dict[str, Any]:
    """APIキーが無い時のダミー添削。feedbackスキルの新スキーマに準拠。"""
    paragraphs = [p for p in (line.strip() for line in student_body.splitlines()) if p]
    if not paragraphs:
        paragraphs = [student_body.strip() or "（本文）"]

    def pick(p: str, max_len: int = 30) -> str:
        return p[: min(len(p), max_len)]

    target1 = pick(paragraphs[0])
    target2 = pick(paragraphs[len(paragraphs) // 2])
    target3 = pick(paragraphs[-1])
    n = len(student_body)
    grade = "B" if n >= 600 else ("C" if n >= 200 else "D")

    comments = [
        {"target_text": target1, "type": "good", "category": "設問適合", "section": "志望理由",
         "comment": "冒頭で立ち位置と志望先が明確に示されています。読み手が最初の数行で「何の話か」を掴める書き出しは、評価者の理解を助ける良い設計です。"},
        {"target_text": target1, "type": "good", "category": "志望校必然性", "section": "志望理由",
         "comment": f"{university_name} {faculty_name}を志望する理由を冒頭で示せている点は、アドミッションポリシーとの接続を意識した良い構造です。"},
        {"target_text": target2, "type": "good", "category": "論理", "section": "学びたいこと",
         "comment": "問題意識から学びたい内容への流れが論理的に展開できています。読み手が筆者の関心の動機をたどれる構成です。"},
        {"target_text": target2, "type": "more", "category": "具体性", "section": "学びたいこと",
         "comment": "ここをもう一段具体化できるとさらに響きます。例：「町役場で〇〇という相談を受けた」「データ上は××％の人が△△と感じている」など、固有名詞・数字を含む一文を追加してみてはいかがでしょうか。"},
        {"target_text": target3, "type": "more", "category": "志望校必然性", "section": "将来像",
         "comment": f"締めくくりで「{faculty_name}で学ぶ何を活かして」が明示されると、説得力がさらに増します。具体的な科目名・教員名・プログラム名を1つでも入れられると、読み手は学部の必然性を感じ取れます。"},
    ]
    return {
        "diagnosis": {
            "grade": grade,
            "opening": "拝読しました。書類の作成お疲れ様でした。",
            "headline": "立ち位置と問題意識は明確。研究テーマの解像度と学部の必然性を磨くと一段上がります。",
        },
        "comments": comments,
        "section_summary": [
            {"section": "志望理由", "comment": "なぜこの分野なのか、原体験との接続が示せています。志望先の独自性を1〜2点引用すると説得力が増します。"},
            {"section": "学びたいこと", "comment": "問いの方向性は見えています。対象・方法・評価軸の3点を明示できると研究計画として立ち上がります。"},
            {"section": "将来像", "comment": "進路の方向性は伝わります。学部での学びと卒業後の像を1本の線で繋ぐ一文を追加してみてください。"},
        ],
        "next_actions": [
            {"priority": 1, "action": "学びたいことの段落に固有名詞・数値を含む原体験の一文を追加"},
            {"priority": 2, "action": "学部のアドミッションポリシーから1文を引用し、自分の関心と接続させる"},
            {"priority": 3, "action": "将来像を「学んだ〇〇を活かして××する」の構文で書き直す"},
        ],
        "encouragement": "あなたの問題意識は他の誰にも書けない強みです。",
        "summary": {"good_count": 3, "more_count": 2, "grade": grade},
        "_mock": True,
    }


def _parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    else:
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1:
            text = text[first : last + 1]
    return json.loads(text)


if __name__ == "__main__":
    import sys
    from master_data import get_master

    md = get_master()
    item, year, status = md.get_active_question_item("waseda", "law", "shinshikou", "q1")
    policy = md.get_admission_policy("waseda", "law")
    sample_body = (sys.stdin.read() or "私は早稲田大学法学部の新思考入試を志望します。出身地である過疎地の高齢化問題を解決したく、法的観点から地域を支える仕組みを学びたいです。").strip()
    result = correct_essay(
        university_name="早稲田大学",
        faculty_name="法学部",
        course_name="新思考入学試験（地域連携型）",
        admission_policy=policy,
        question_title=item["title"],
        question_body=item["body"],
        question_year=year,
        question_status=status,
        char_limit=item.get("char_limit"),
        student_body=sample_body,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
