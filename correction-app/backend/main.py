"""FastAPIエントリポイント。/api/master, /api/correct, /api/download/{token}, /api/google-docs/* を提供。"""
from __future__ import annotations

import io
import logging
import os
import time
import uuid
from pathlib import Path
from threading import Lock

# .envを最優先でロード（ANTHROPIC_API_KEY等）
# setdefault は既存の空値を上書きしないため、明示的に値があれば上書きする
_ENV_FILE = Path(__file__).resolve().parent / ".env"
if _ENV_FILE.exists():
    for raw in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if v:  # .envに値がある場合、既存環境変数を強制上書き
            os.environ[k] = v
        else:
            os.environ.setdefault(k, v)
from typing import Any
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from correction import correct_essay
from docx_builder import build_corrected_docx
from master_data import get_master

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("correction-app")

app = FastAPI(title="オープン添削 — 高校生のための志望理由書添削")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ダウンロードトークン → docxバイナリのインメモリキャッシュ（TTL 30分）
_DOWNLOAD_CACHE: dict[str, dict] = {}
_DOWNLOAD_LOCK = Lock()
_DOWNLOAD_TTL_SEC = 30 * 60


def _cache_set(token: str, payload: dict) -> None:
    with _DOWNLOAD_LOCK:
        _DOWNLOAD_CACHE[token] = {**payload, "_expire": time.time() + _DOWNLOAD_TTL_SEC}
        # 期限切れの掃除
        now = time.time()
        for k in [k for k, v in _DOWNLOAD_CACHE.items() if v["_expire"] < now]:
            _DOWNLOAD_CACHE.pop(k, None)


def _cache_get(token: str) -> dict | None:
    with _DOWNLOAD_LOCK:
        v = _DOWNLOAD_CACHE.get(token)
        if not v or v["_expire"] < time.time():
            return None
        return v


class CorrectRequest(BaseModel):
    university_id: str
    faculty_id: str
    course_id: str
    question_id: str
    body: str = Field(min_length=1)
    output_format: str = Field(default="docx", pattern="^(docx|gdocs)$")


@app.get("/api/master")
def api_master() -> dict[str, Any]:
    return get_master().hierarchy_for_frontend()


@app.get("/api/health")
def api_health() -> dict[str, Any]:
    """サーバー診断。APIキーは長さと先頭末尾4文字のみ返す（漏洩防止）。"""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    return {
        "ok": True,
        "api_key_set": bool(key),
        "api_key_length": len(key),
        "api_key_prefix": key[:8] + "..." if len(key) > 12 else "",
        "api_key_suffix": "..." + key[-4:] if len(key) > 12 else "",
        "env_file": str(_ENV_FILE),
        "env_file_exists": _ENV_FILE.exists(),
    }


@app.post("/api/correct")
def api_correct(req: CorrectRequest):
    md = get_master()

    try:
        univ, faculty, course = md.get_course(req.university_id, req.faculty_id, req.course_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="指定された大学・学部・コースが見つかりません")

    try:
        item, year, status = md.get_active_question_item(
            req.university_id, req.faculty_id, req.course_id, req.question_id
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="指定された設問が見つかりません")

    policy = md.get_admission_policy(req.university_id, req.faculty_id)

    log.info(
        "correct: %s/%s/%s/%s year=%s status=%s body_len=%d",
        req.university_id, req.faculty_id, req.course_id, req.question_id,
        year, status, len(req.body),
    )

    try:
        correction = correct_essay(
            university_name=univ["name"],
            faculty_name=faculty["name"],
            course_name=course["name"],
            admission_policy=policy,
            question_title=item["title"],
            question_body=item["body"],
            question_year=year,
            question_status=status,
            char_limit=item.get("char_limit"),
            student_body=req.body,
        )
    except Exception as e:
        log.exception("AI添削に失敗")
        raise HTTPException(status_code=502, detail=f"AI添削に失敗しました: {e}")

    result = build_corrected_docx(
        university_name=univ["name"],
        faculty_name=faculty["name"],
        course_name=course["name"],
        question_title=item["title"],
        question_body=item["body"],
        question_year=year,
        question_status=status,
        student_body=req.body,
        correction=correction,
    )

    filename = f"添削_{univ['name']}_{faculty['name']}_{course['name']}.docx"
    token = uuid.uuid4().hex
    matched_targets = {c.get("target_text") for c in result.unmatched}
    annotated_comments = []
    for c in correction.get("comments", []):
        annotated_comments.append({
            "target_text": c.get("target_text", ""),
            "type": c.get("type", "more"),
            "category": c.get("category", ""),
            "comment": c.get("comment", ""),
            "anchored": c.get("target_text") not in matched_targets,
        })

    summary = correction.get("summary", {})
    response_payload = {
        "token": token,
        "filename": filename,
        "summary": {
            "good_count": summary.get("good_count", sum(1 for c in annotated_comments if c["type"] == "good")),
            "more_count": summary.get("more_count", sum(1 for c in annotated_comments if c["type"] == "more")),
            "grade": summary.get("grade") or correction.get("diagnosis", {}).get("grade"),
        },
        "diagnosis": correction.get("diagnosis", {}),
        # opening は新スキーマで diagnosis.opening、後方互換で top-level の opening も参照
        "opening": (correction.get("diagnosis", {}) or {}).get("opening") or correction.get("opening", ""),
        "section_summary": correction.get("section_summary", []),
        "next_actions": correction.get("next_actions", []),
        "encouragement": correction.get("encouragement", ""),
        "matched": result.matched,
        "unmatched_count": len(result.unmatched),
        "year": year,
        "status": status,
        "comments": annotated_comments,
        "is_mock": correction.get("_mock", False),
        "context": {
            "university": univ["name"],
            "faculty": faculty["name"],
            "course": course["name"],
            "question_title": item["title"],
        },
    }

    _cache_set(token, {"docx_bytes": result.docx_bytes, "filename": filename})

    if req.output_format == "gdocs":
        try:
            from google_docs import upload_to_drive_as_gdoc
            link = upload_to_drive_as_gdoc(
                result.docx_bytes,
                title=f"添削_{univ['name']}_{faculty['name']}_{course['name']}",
            )
            response_payload["google_docs_url"] = link
            response_payload["output_format"] = "gdocs"
        except Exception as e:
            log.exception("Googleドキュメント出力に失敗")
            response_payload["google_docs_error"] = str(e)
            response_payload["output_format"] = "docx"
    else:
        response_payload["output_format"] = "docx"

    return response_payload


@app.get("/api/download/{token}")
def api_download(token: str):
    cached = _cache_get(token)
    if not cached:
        raise HTTPException(status_code=404, detail="ダウンロードトークンが無効または期限切れです（30分）")
    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{quote(cached['filename'])}",
    }
    return StreamingResponse(
        io.BytesIO(cached["docx_bytes"]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("APP_PORT", 8092)))
