from __future__ import annotations
from typing import Protocol
from pathlib import Path
import os
import requests

from dotenv import load_dotenv

# Load .env from project root so HF_API_TOKEN is always visible here.
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class LLMClient(Protocol):
    """
    Minimal, vendor-neutral interface for the reasoning layer.
    """
    def summarise(self, text: str) -> str:
        ...


class HuggingFaceSummariser:
    """
    Uses Hugging Face's router (OpenAI-compatible chat completions API)
    to generate an executive summary from the rule-based report.
    """
    def __init__(self) -> None:
        model = os.getenv("LLM_MODEL", "HuggingFaceTB/SmolLM3-3B:hf-inference")
        token = os.getenv("HF_API_TOKEN")

        if not token:
            raise RuntimeError("HF_API_TOKEN not set")

        self.model = model
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self.endpoint = "https://router.huggingface.co/v1/chat/completions"

    def summarise(self, text: str) -> str:
        """
        Sends the rule-based summary to a small language model via the
        HF router and returns an AI-generated executive summary.
        """
        system_msg = (
            "You are a concise financial analyst. "
            "Summarise market movements for busy executives. "
            "Use 4–6 short bullet points, in clear business English."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text},
            ],
            "max_tokens": 200,
            "temperature": 0.3,
        }

        resp = requests.post(
            self.endpoint,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        if resp.status_code >= 400:
            raise RuntimeError(
                f"Hugging Face router error {resp.status_code}: {resp.text[:200]}"
            )

        data = resp.json()

        # OpenAI-style response: choices[0].message.content
        try:
            content = data["choices"][0]["message"]["content"]
            return content.strip()
        except Exception:
            return f"[Unexpected router response: {data}]"
