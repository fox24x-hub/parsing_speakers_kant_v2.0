from __future__ import annotations

import json
from typing import Any

import httpx

from config.settings import Settings


def build_prompt(season: str, region: str, sports: list[str]) -> str:
    sports_list = ", ".join(sports)
    return (
        "Ты парсер спикеров для KANT.ru. "
        "Найди спикеров лекций по видам спорта этого сезона в указанном регионе. "
        "Верни ТОЛЬКО валидный JSON без Markdown. "
        "Формат JSON: {\n"
        "  \"season\": str,\n"
        "  \"region\": str,\n"
        "  \"sports\": [str],\n"
        "  \"speakers\": [\n"
        "    {\n"
        "      \"name\": str,\n"
        "      \"sport\": str,\n"
        "      \"location\": str,\n"
        "      \"expertise\": str,\n"
        "      \"url\": str | null\n"
        "    }\n"
        "  ]\n"
        "}. "
        "Если спикеров нет — верни \"speakers\": []. "
        f"Сезон: {season}. Регион: {region}. Виды спорта: {sports_list}."
    )


def _build_chat_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/v1"):
        return f"{normalized}/chat/completions"
    return f"{normalized}/v1/chat/completions"


async def gpt_search_speakers(
    *,
    season: str,
    region: str,
    sports: list[str],
    settings: Settings,
) -> dict[str, Any]:
    prompt = build_prompt(season, region, sports)
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": "Ты точный JSON-генератор. Никогда не добавляй Markdown."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    url = _build_chat_url(settings.openai_base_url)

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"]
    return json.loads(content)
