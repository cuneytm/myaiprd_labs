"""
Claude modül 2 · Tek bir Messages API çağrısı.

Kavramlar: istek alanları (model, max_tokens, system, messages), cevap alanları
(content, stop_reason, usage). Bölüm 2.2 ve 2.4.

    python ilk_cagri.py
"""
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

client = anthropic.Anthropic()

r = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=512,
    system="Sen bir NOC asistanısın. Kısa ve Türkçe cevap ver.",
    messages=[{"role": "user", "content": "BGP 'holdtimer expired' mesajı ne anlama gelir? Üç olası nedenini yaz."}],
)

print("".join(b.text for b in r.content if b.type == "text"))
print("\n--- cevap alanları ---")
print("id         :", r.id)
print("model      :", r.model)
print("stop_reason:", r.stop_reason)       # end_turn | max_tokens | tool_use | refusal ...
print("usage      :", r.usage.input_tokens, "girdi,", r.usage.output_tokens, "çıktı token")
