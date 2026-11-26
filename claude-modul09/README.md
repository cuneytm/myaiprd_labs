# Claude modül 9 · Runbook asistanı ve değerlendirme seti

Portaldaki karşılığı: **9. RAG, değerlendirme ve kapanış projesi**, Lab 9.1.

| Dosya | Kavram |
| --- | --- |
| `runbooklar/` | 40 kurgusal network runbook'u (KB-101 ... KB-140) |
| `ortak.py` | Runbook yükleme, system prompt, maliyet hesabı |
| `uzun_baglam.py` | Tüm runbook'lar bağlamda, prompt caching ve citations ile |
| `rag/parcala.py` | Başlığa göre parçalama, contextual retrieval (TODO) |
| `rag/ara.py` | BM25 + TF-IDF hibrit arama (bağımlılıksız; embedding modeline geçiş için tek fonksiyon) |
| `rag/cevapla.py` | Bulunan parçalarla cevap ve kaynak |
| `eval/sorular.jsonl` | 25 soru (5 tanesi "belgede yok") |
| `eval/calistir.py` | İki yöntemi çalıştırır; doğruluk, kaynak isabeti, uydurma oranı ve maliyeti tabloya yazar |

Adımlar [HOWTO.md](HOWTO.md)'de.
