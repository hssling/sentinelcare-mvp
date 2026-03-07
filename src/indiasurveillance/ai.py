from __future__ import annotations

import base64
import hashlib
import json
import os
from datetime import datetime, timezone

import requests
from cryptography.fernet import Fernet

from .contracts import AIAssistRequest, AIAssistResponse, AIProviderCatalogItem, AIProviderConfigStored, AIProviderName


def provider_catalog() -> list[AIProviderCatalogItem]:
    return [
        AIProviderCatalogItem(
            provider="openai",
            label="OpenAI",
            auth_url="https://platform.openai.com/api-keys",
            docs_url="https://platform.openai.com/docs/overview",
            default_base_url="https://api.openai.com/v1",
            supported_models=["gpt-4.1", "gpt-4o", "gpt-4.1-mini"],
            integration_mode="openai_compatible",
        ),
        AIProviderCatalogItem(
            provider="anthropic",
            label="Anthropic",
            auth_url="https://console.anthropic.com/settings/keys",
            docs_url="https://docs.anthropic.com/",
            default_base_url="https://api.anthropic.com/v1",
            supported_models=["claude-sonnet-4-5", "claude-3-7-sonnet-latest", "claude-3-5-haiku-latest"],
            integration_mode="anthropic_messages",
        ),
        AIProviderCatalogItem(
            provider="google",
            label="Google AI Studio",
            auth_url="https://aistudio.google.com/app/apikey",
            docs_url="https://ai.google.dev/gemini-api/docs",
            default_base_url="https://generativelanguage.googleapis.com/v1beta",
            supported_models=["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"],
            integration_mode="google_generate",
        ),
        AIProviderCatalogItem(
            provider="openrouter",
            label="OpenRouter",
            auth_url="https://openrouter.ai/settings/keys",
            docs_url="https://openrouter.ai/docs/quickstart",
            default_base_url="https://openrouter.ai/api/v1",
            supported_models=["openai/gpt-4.1-mini", "anthropic/claude-3.7-sonnet", "google/gemini-2.0-flash-001"],
            integration_mode="openai_compatible",
        ),
        AIProviderCatalogItem(
            provider="groq",
            label="Groq",
            auth_url="https://console.groq.com/keys",
            docs_url="https://console.groq.com/docs/overview",
            default_base_url="https://api.groq.com/openai/v1",
            supported_models=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            integration_mode="openai_compatible",
        ),
        AIProviderCatalogItem(
            provider="together",
            label="Together AI",
            auth_url="https://api.together.xyz/settings/api-keys",
            docs_url="https://docs.together.ai/docs/quickstart",
            default_base_url="https://api.together.xyz/v1",
            supported_models=["meta-llama/Llama-3.3-70B-Instruct-Turbo", "Qwen/Qwen2.5-72B-Instruct-Turbo"],
            integration_mode="openai_compatible",
        ),
        AIProviderCatalogItem(
            provider="cohere",
            label="Cohere",
            auth_url="https://dashboard.cohere.com/api-keys",
            docs_url="https://docs.cohere.com/docs/chat-api",
            default_base_url="https://api.cohere.com/v2",
            supported_models=["command-a-03-2025", "command-r-plus", "command-r"],
            integration_mode="cohere_chat",
        ),
        AIProviderCatalogItem(
            provider="xai",
            label="xAI",
            auth_url="https://console.x.ai/",
            docs_url="https://docs.x.ai/",
            default_base_url="https://api.x.ai/v1",
            supported_models=["grok-3-mini", "grok-3-beta"],
            integration_mode="openai_compatible",
        ),
    ]


def catalog_map() -> dict[AIProviderName, AIProviderCatalogItem]:
    return {item.provider: item for item in provider_catalog()}


def mask_api_key(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def _fernet() -> Fernet:
    secret = os.getenv("INDIA_SURVEILLANCE_AI_KEY_SECRET") or os.getenv("INDIA_SURVEILLANCE_JWT_SECRET") or "india-surveillance-ai-fallback"
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_api_key(value: str) -> str:
    return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_api_key(ciphertext: str) -> str:
    return _fernet().decrypt(ciphertext.encode("utf-8")).decode("utf-8")


def _system_prompt() -> str:
    return (
        "You are assisting a patient safety surveillance program. "
        "Return strict JSON with keys: summary, confidence, domain, deviation_class, severity_level, "
        "contributing_factors, corrective_action, preventive_action. "
        "Use concise factual language."
    )


def _user_prompt(request: AIAssistRequest) -> str:
    return json.dumps(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain": request.domain,
            "severity": request.severity,
            "event_summary": request.event_summary,
            "what_happened": request.what_happened,
            "immediate_action_taken": request.immediate_action_taken,
            "contributing_factors": request.contributing_factors,
        },
        ensure_ascii=True,
    )


def _parse_json_text(content: str) -> dict[str, object]:
    start = content.find("{")
    end = content.rfind("}")
    if start >= 0 and end > start:
        content = content[start : end + 1]
    data = json.loads(content)
    if not isinstance(data, dict):
        raise ValueError("AI response did not return a JSON object")
    return data


def assist_with_model(config: AIProviderConfigStored, request: AIAssistRequest, timeout: int = 45) -> AIAssistResponse:
    catalog = catalog_map()[config.provider]
    api_key = decrypt_api_key(config.api_key_ciphertext)
    prompt = _user_prompt(request)

    if catalog.integration_mode == "openai_compatible":
        response = requests.post(
            f"{config.base_url.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": config.model,
                "temperature": 0.1,
                "messages": [
                    {"role": "system", "content": _system_prompt()},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=timeout,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
    elif catalog.integration_mode == "anthropic_messages":
        response = requests.post(
            f"{config.base_url.rstrip('/')}/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": config.model,
                "max_tokens": 800,
                "system": _system_prompt(),
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=timeout,
        )
        response.raise_for_status()
        content = "".join(item.get("text", "") for item in response.json().get("content", []))
    elif catalog.integration_mode == "google_generate":
        response = requests.post(
            f"{config.base_url.rstrip('/')}/models/{config.model}:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "system_instruction": {"parts": [{"text": _system_prompt()}]},
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.1},
            },
            timeout=timeout,
        )
        response.raise_for_status()
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    elif catalog.integration_mode == "cohere_chat":
        response = requests.post(
            f"{config.base_url.rstrip('/')}/chat",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": config.model, "temperature": 0.1, "messages": [{"role": "user", "content": prompt}]},
            timeout=timeout,
        )
        response.raise_for_status()
        body = response.json()
        content = body.get("message", {}).get("content", [{}])[0].get("text", "")
    else:
        raise ValueError(f"Unsupported provider mode: {catalog.integration_mode}")

    parsed = _parse_json_text(content)
    summary = str(parsed.get("summary", request.event_summary))
    confidence = float(parsed.get("confidence", 0.5))
    structured_fields = {
        "domain": parsed.get("domain"),
        "deviation_class": parsed.get("deviation_class"),
        "severity_level": parsed.get("severity_level"),
        "contributing_factors": parsed.get("contributing_factors", []),
        "corrective_action": parsed.get("corrective_action"),
        "preventive_action": parsed.get("preventive_action"),
    }
    return AIAssistResponse(
        provider=config.provider,
        model=config.model,
        summary=summary,
        confidence=max(0.0, min(1.0, confidence)),
        structured_fields=structured_fields,
    )
