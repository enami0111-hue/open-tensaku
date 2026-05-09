"""マスターデータ（大学・学部・コース・設問・アドミポリ）のロードと検索"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
UNIV_JSON = DATA_DIR / "universities.json"


class MasterData:
    def __init__(self) -> None:
        self._raw: dict[str, Any] = json.loads(UNIV_JSON.read_text(encoding="utf-8"))

    @property
    def version(self) -> str:
        return self._raw.get("version", "unknown")

    def hierarchy_for_frontend(self) -> dict[str, Any]:
        """フロント用の階層JSON。本文は除き、当年/前年の判定済みフラグを付与。"""
        out_universities = []
        for u in self._raw["universities"]:
            faculties = []
            for f in u["faculties"]:
                courses = []
                for c in f["courses"]:
                    active = self._select_active_question_set(c.get("questions", []))
                    courses.append({
                        "id": c["id"],
                        "name": c["name"],
                        "url": c.get("url"),
                        "meta": c.get("meta", {}),
                        "active_year": active["year"] if active else None,
                        "active_status": active["status"] if active else None,
                        "is_archived_fallback": (active["status"] == "archived") if active else False,
                        "source_docs": active.get("source_docs", []) if active else [],
                        "items": [
                            {
                                "id": it["id"],
                                "title": it["title"],
                                "char_limit": it.get("char_limit"),
                                "body": (DATA_DIR / it["path"]).read_text(encoding="utf-8") if "path" in it else "",
                            }
                            for it in (active["items"] if active else [])
                        ],
                    })
                faculties.append({"id": f["id"], "name": f["name"], "courses": courses})
            out_universities.append({"id": u["id"], "name": u["name"], "faculties": faculties})
        return {"version": self.version, "universities": out_universities}

    def _select_active_question_set(self, sets: list[dict]) -> dict | None:
        """当年/前年フォールバック：最新年度を採用。当年(official)がなければ次の年(archived)。"""
        if not sets:
            return None
        sorted_sets = sorted(sets, key=lambda s: s["year"], reverse=True)
        for s in sorted_sets:
            if s.get("items"):
                return s
        return None

    def get_course(self, univ_id: str, faculty_id: str, course_id: str) -> tuple[dict, dict, dict]:
        for u in self._raw["universities"]:
            if u["id"] != univ_id:
                continue
            for f in u["faculties"]:
                if f["id"] != faculty_id:
                    continue
                for c in f["courses"]:
                    if c["id"] == course_id:
                        return u, f, c
        raise KeyError(f"Course not found: {univ_id}/{faculty_id}/{course_id}")

    def get_active_question_item(
        self, univ_id: str, faculty_id: str, course_id: str, question_id: str
    ) -> tuple[dict, int, str]:
        """設問本文と year/status を返す。(item_dict, year, status)"""
        _, _, course = self.get_course(univ_id, faculty_id, course_id)
        active = self._select_active_question_set(course.get("questions", []))
        if not active:
            raise KeyError(f"No questions registered for course {course_id}")
        for it in active["items"]:
            if it["id"] == question_id:
                body = (DATA_DIR / it["path"]).read_text(encoding="utf-8") if "path" in it else ""
                return {**it, "body": body}, active["year"], active["status"]
        raise KeyError(f"Question not found: {question_id}")

    def get_admission_policy(self, univ_id: str, faculty_id: str) -> str:
        for u in self._raw["universities"]:
            if u["id"] != univ_id:
                continue
            for f in u["faculties"]:
                if f["id"] != faculty_id:
                    continue
                path = f.get("admission_policy_path")
                if not path:
                    return ""
                return (DATA_DIR / path).read_text(encoding="utf-8")
        return ""


_instance: MasterData | None = None


def get_master() -> MasterData:
    global _instance
    if _instance is None:
        _instance = MasterData()
    return _instance
