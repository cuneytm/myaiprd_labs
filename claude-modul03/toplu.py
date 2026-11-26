"""
Claude modül 3 · 50 talebi Message Batches API ile göndermek.

Kavramlar: %50 indirim, asenkron işleme, custom_id ile eşleme (sonuçlar sırasız gelir). Bölüm 3.8.

    python toplu.py                 # gönderir ve bitene kadar bekler
    python toplu.py --id msgbatch_...   # daha önce gönderilmiş bir batch'in sonucunu alır
"""
import argparse
import json
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming  # noqa: E402
from anthropic.types.messages.batch_create_params import Request  # noqa: E402

from sema import DegisiklikTalebi  # noqa: E402

VERI = Path(__file__).parent / "veri"
RUNBOOK = (VERI / "runbook.md").read_text(encoding="utf-8")
SEMA = {
    "type": "json_schema",
    "schema": {**DegisiklikTalebi.model_json_schema(), "additionalProperties": False},
}


def gonder(client: anthropic.Anthropic) -> str:
    talepler = [json.loads(s) for s in open(VERI / "talepler.jsonl", encoding="utf-8")]
    istekler = [
        Request(
            custom_id=t["id"],
            params=MessageCreateParamsNonStreaming(
                model="claude-sonnet-5-5",
                max_tokens=1024,
                system=[{"type": "text", "text": "DC1 runbook'una göre değişiklik talebini analiz et.\n\n<runbook>\n"
                         + RUNBOOK + "\n</runbook>", "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": t["metin"]}],
                output_config={"format": SEMA},
            ),
        )
        for t in talepler
    ]
    batch = client.messages.batches.create(requests=istekler)
    print("Gönderildi:", batch.id)
    return batch.id


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id")
    args = ap.parse_args()
    client = anthropic.Anthropic()
    bid = args.id or gonder(client)

    while (b := client.messages.batches.retrieve(bid)).processing_status != "ended":
        print("Bekleniyor...", b.request_counts)
        time.sleep(30)

    girdi = cikti = 0
    for s in client.messages.batches.results(bid):          # sıra gönderdiğiniz sıra DEĞİL
        if s.result.type != "succeeded":
            print(s.custom_id, s.result.type)
            continue
        m = s.result.message
        girdi += m.usage.input_tokens + (m.usage.cache_read_input_tokens or 0)
        cikti += m.usage.output_tokens
        print(s.custom_id, m.content[0].text)
    # Batch fiyatı normal fiyatın yarısıdır (Sonnet 5.5: 2/10 USD → 1/5 USD per 1M)
    print(f"\nToplam ~{girdi} girdi, {cikti} çıktı token. Normal: {girdi/1e6*2 + cikti/1e6*10:.4f} USD, "
          f"batch: ~{girdi/1e6*1 + cikti/1e6*5:.4f} USD (önbellek indirimi hariç)")


if __name__ == "__main__":
    main()
