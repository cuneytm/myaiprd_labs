"""
Karşılaştırma için: benzer bir işi WORKFLOW olarak yapmak.

Workflow'da sonraki adımı KOD seçer. Adımlar ve sıra aşağıda sabittir; model
yalnız son adımda metni özetlemek için kullanılır. Tool yoktur, model hiçbir
karar vermez.

    python workflow.py
"""

import os

from openai import OpenAI

from tools import WORK_DIR, read_file

client = OpenAI(base_url=os.environ.get("MODEL_BASE_URL"), api_key=os.environ.get("MODEL_API_KEY", "yok"))

# Adım 1 (kod): bütün .md ve .txt dosyalarını bul
files = [str(f.relative_to(WORK_DIR)) for f in sorted(WORK_DIR.rglob("*"))
         if f.suffix in (".md", ".txt") and not f.name.startswith(".")]
print(f"Adım 1 · {len(files)} metin dosyası bulundu:\n  " + "\n  ".join(files))

# Adım 2 (kod): hepsini oku
texts = [f"### {f}\n{read_file(f)}" for f in files]
print("Adım 2 · dosyalar okundu.")

# Adım 3 (model): yalnız özetle
prompt = "Aşağıdaki dosyaları her biri için tek cümleyle Türkçe özetle:\n\n" + "\n\n".join(texts)
summary = client.chat.completions.create(
    model=os.environ.get("MODEL_NAME"), messages=[{"role": "user", "content": prompt}]
).choices[0].message.content or ""
print("\nAdım 3 · özet:\n" + summary)
