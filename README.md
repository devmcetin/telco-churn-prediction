# TelcoTR — Müşteri Kaybı (Churn) Tahmin Projesi

**Bitirme Projesi · Veri Bilimi** • Tahmini süre: ~6-10 saat • Değerlendirme: **eğitmen incelemesi (manuel)**

---

## 📨 Durum

TelcoTR'de **data scientist** olarak yeni işe başladın. İlk haftanın sonunda pazarlama direktöründen şu mesaj düşüyor:

> "Merhaba, hoş geldin. Bir sıkıntımız var: her ay ciddi sayıda müşteri bizi bırakıp gidiyor (buna **churn** diyoruz) ama kimin gideceğini önceden göremiyoruz. Elimizde binlerce müşterinin geçmiş kaydı var — sana ham halini bırakıyorum. Senden ricam: bu veriyle **hangi müşterilerin ayrılma riski taşıdığını tahmin eden bir model** kur ve bana **gerçek bir performans raporu** getir. Nasıl yapacağın sana kalmış; ben sonuçları ve senin yorumunu görmek istiyorum. Özellikle: modeline ne kadar güvenebilirim, nerede yanılıyor, ve elimizdeki bu bilgiyle **ne yapmamı önerirsin**?"

Bu senin **bitirme projen**. Sana adım adım talimat vermiyoruz — gerçek bir işte de vermezler. Sana **veriyi ve işin hedefini** veriyoruz; çözümü bir data scientist gibi sen tasarlayacaksın.

## 🎯 İş hedefi

Geçmiş müşteri verisinden yola çıkarak, bir müşterinin **ayrılıp ayrılmayacağını (Churn: Yes/No)** tahmin eden bir model kur. Sonra bu modelin **ne kadar güvenilir** olduğunu dürüstçe ölç ve **iş diliyle** raporla.

## 📦 Elindeki veri

- `data/telco.csv` — 7043 müşterinin ham kaydı, 21 kolon.
- `data/veri_sozlugu.md` — kolonların ne anlama geldiği (data dictionary).

⚠️ **Bu gerçek dünya verisi.** Temiz, hazır bir tablo değil — içinde bir data scientist'in fark edip çözmesi gereken gerçek dünya sorunları var. Bunları senin için **tek tek saymıyoruz**; keşfetmek ve doğru şekilde ele almak işin bir parçası. (Küçük bir dürüstlük notu: hedef değişken dengeli değil.)

## 🛠️ Başlarken

```bash
# 1. Bu repoyu fork'la, sonra kendi fork'unu klonla
git clone <senin-fork-url>
cd data-science-project-52

# 2. Sanal ortam (önerilir)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Önerilen kütüphaneleri kur
pip install -r requirements.txt

# 4. Analiz defterini aç ve başla
jupyter lab
```

Boş bir `analiz.ipynb` oluşturup keşifle başlayabilirsin.

## ✅ Bizden beklentiler

**Nasıl** çözeceğin sana kalmış (hangi kütüphane, hangi model, hangi yaklaşım — özgürsün). Ama iyi bir teslimatta şunları görmek istiyoruz:

1. **Veriyi tanı ve temizle** — veride ne var, ne eksik, ne bozuk? Sorunları kendin bul ve gerekçesiyle çöz.
2. **En az 2 model dene ve adil karşılaştır** — sonuçları bir modele değil, kıyaslamaya dayandır. (İpucu: ön işlemeyi eğitim/test ayrımına dikkat ederek yap — yoksa modelin olduğundan iyi görünür.)
3. **Doğru metriği seç ve gerekçelendir** — "accuracy %80" demek burada neden yanıltıcı olabilir? Hangi metrik(ler) bu iş için daha anlamlı, neden?
4. **Modelin nerede yanıldığını incele** — kimleri kaçırıyor, bunun işe maliyeti ne? (Ayrılacak bir müşteriyi "kalır" diye işaretlemek ne demek?)
5. **İş diliyle raporla** — teknik olmayan bir yöneticinin anlayacağı şekilde: ne buldun, modele ne kadar güvenilir, **ne yapılmasını öneriyorsun**.

## 📤 Teslim edeceklerin

Repo'nda şu üç şey olmalı:

| Dosya | Ne olmalı |
|---|---|
| `analiz.ipynb` | Uçtan uca analiz defterin: keşif → temizlik → modelleme → değerlendirme, aradaki kararlarını markdown hücrelerinde **anlatarak**. |
| `train.py` | Yeniden çalıştırılabilir bir script: veriyi okur, final modelini eğitir, sonuç metriklerini ekrana basar. (Biz `python train.py` diyip çalıştırabilmeliyiz.) — yani notebook'ta keşfettiğin akışın temiz, tek komutla çalışan hali. |
| `RAPOR.md` | İş diliyle raporun. `RAPOR_SABLONU.md`'deki soruları cevapla. |

## 🧭 Nasıl değerlendirilecek

Otomatik test yok — projeni bir eğitmen inceleyip aşağıdaki rubriğe göre değerlendirecek:

| Boyut | Puan |
|---|---:|
| Veri anlama & temizlik (sorunları buldun ve doğru çözdün mü) | 20 |
| Modelleme & doğru metodoloji (≥2 model, data leakage yok) | 25 |
| Değerlendirme & metrik muhakemesi (doğru metrik + gerekçe) | 20 |
| Hata analizi & iş içgörüsü (model nerede yanılıyor, iş etkisi) | 15 |
| Rapor & iletişim (RAPOR.md net ve iş diliyle mi) | 15 |
| Kod kalitesi & tekrar çalıştırılabilirlik (`train.py` çalışıyor mu) | 5 |
| **Toplam** | **100** |

Geçmek için ~70/100 hedefle. **Puanın çoğu "doğru sonucu bulmakta" değil, sonucu nasıl elde edip yorumladığında.**

## 📈 Başarı hedefi

Katı bir eşik yok. Naif bir tahminden (herkese "kalır" demek gibi) **anlamlı biçimde daha iyi**, savunabilir bir sonuç hedefle (yön verelim: iyi bir çözüm bu veride ROC-AUC olarak ~0.80 ve üzerini yakalar). Ama asıl değerlendirilen: bu sonuca **nasıl** ulaştığın ve onu nasıl **yorumladığın**.

## 🚀 Nasıl gönderirsin

1. Bu repoyu **fork'la**, kendi hesabında çöz. Repo'nun **public** olduğundan emin ol.
2. Kaizu'da bu projede **"İncelet 🔍"** butonuna bas.
3. **GitHub repo linkini** ve **neler yaptığını** (yaklaşımın, kararların, özellikle bakmamızı istediğin yerler) yaz, gönder.
4. Eğitmenin projeni inceleyecek — yanıt **2-3 iş günü** sürebilir; sonucu ve geri bildirimi Kaizu'da göreceksin. Takıldığın yer olursa eğitmenine de danışabilirsin.

> Not: Bu projenin onayı, sıradaki bitirme projeni açar.

## 💡 Hatırlatmalar

- Kütüphane seçimi sana ait. `requirements.txt`'te önerilen bir başlangıç seti var; dilediğini ekleyebilirsin.
- Kod ve rapor **senin** olmalı — anlamadığın bir şeyi teslim etme; eğitmen sana yaklaşımını soracak.
- Amaç mükemmel bir model değil; **bir data scientist gibi düşünüp** sonucunu dürüstçe ölçmen ve anlatman.

Başarılar 🚀
