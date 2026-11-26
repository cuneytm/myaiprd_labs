# Claude modül 9 · Ne yapacaksınız

```bash
cd claude-modul09
```

## Adım 1 · Uzun bağlam

```bash
python uzun_baglam.py "BGP komşusu Idle durumunda kalıyorsa ilk ne kontrol edilir?"
python uzun_baglam.py "Leaf'lerde jumbo frame MTU değeri ne olmalı?"
```

İlk çalıştırmada `cache yazma`, ikincide `cache okuma` dolmalı. 40 runbook'un hepsi her soruda gidiyor ama önbellekten okunuyor.

## Adım 2 · İndeks

```bash
python rag/parcala.py
python rag/ara.py "jumbo frame MTU"
```

Sonra `rag/parcala.py`'deki contextual retrieval TODO'sunu Bölüm 9.2'deki örnekle tamamlayın ve indeksi bağlamla yeniden oluşturun:

```bash
python rag/parcala.py --baglam
```

## Adım 3 · RAG ile cevap

```bash
python rag/cevapla.py "BGP komşusu Idle durumunda kalıyorsa ilk ne kontrol edilir?"
```

Bulunan parçaları ve citations'ta dönen kaynakları kontrol edin.

## Adım 4 · Değerlendirme

```bash
python eval/calistir.py
```

İki yöntem 25 soruda karşılaştırılır (50 istek; maliyet tabloda yazar).

**Gözlemleyin:**

- Hangi yöntem daha doğru, hangisi daha ucuz? Fark hangi soru türünde ortaya çıkıyor?
- "Belgede yok" sorularında hangi yöntem daha çok uydurdu?
- Contextual retrieval'ı kapatıp (`python rag/parcala.py`) RAG'i tekrar ölçtüğünüzde kaynak isabeti ne kadar düştü?

## Alıştırma

`eval/sorular.jsonl`'e kendi işinizden 5 soru ekleyin ve `ortak.py`'deki `SISTEM` prompt'unda tek bir değişiklik yaparak skoru iyileştirmeye çalışın. Değişikliği ancak skor gerçekten arttıysa tutun.
