# Churn Projesi - Rapor

## 1. Özet (3-4 cümle)
TelcoTR'nin 7.043 müşterilik geçmiş kaydını kullanarak hangi müşterilerin ayrılma riski taşıdığını önceden tahmin eden bir model kurdum. Model, gerçekten ayrılacak müşterilerin yaklaşık **%78'ini önceden yakalayabiliyor** (ROC-AUC 0,84). En çarpıcı bulgu: ayrılan müşterilerin **%88'i aydan aya sözleşmeli** - elde tutma stratejisinin nereye odaklanması gerektiği çok net. Modeli otomatik karar makinesi olarak değil, müşteri temsilcilerine önceliklendirilmiş bir risk listesi çıkaran bir araç olarak kullanmanızı öneriyorum.

## 2. Veriyi tanıma ve temizlik
- **`TotalCharges` kolonu 11 satırda boştu.** İncelediğimde hepsinin `tenure=0` olan (henüz 1 ayını doldurmamış) yeni müşteriler olduğunu gördüm. Yani bunun "kayıp veri" değil, henüz oluşmamış bir toplam olduğunu değerlendirdim. Silmek yerine mantıklı olan `0` değeriyle doldurdum. Sadece 11/7.043 satır olduğu için sonucu etkilemiyor ama veriyi de israf etmiyor.
- **`customerID`'yi modele sokmadım.** Her müşteriye özel, tekrar eden bir sinyal taşımıyor.
- **Hedef değişken dengesiz:** %73,5 kalır / %26,5 ayrılır. Bu, hangi metriğe doğrudan bakacağımı belirledi. (Bkz. bölüm 4.)
- Geri kalan kolonlarda (hizmet türleri, sözleşme, ödeme yöntemi) beklenmedik değer, yazım tutarsızlığı ya da kopya satır bulmadım.

## 3. Kurduğum modeller ve karşılaştırma
İki model denedim: **Lojistik Regresyon** (basit, katsayıları doğrudan yorumlanabilir) ve **Random Forest** (doğrusal olmayan ilişkileri yakalayabilen). İkisini de aynı eğitim/test ayrımı, aynı ön işleme ve aynı metriklerle karşılaştırdım. Sonuç: ikisi de ~0,84 ROC-AUC verdi ve churn'ü yakalama gücünde (recall %78) eşitlerdi ama Random Forest bunu **daha az false positive ile** sağladı (daha yüksek precision). Bu yüzden final model olarak **Random Forest**'ı seçtim; Lojistik Regresyon'u ise "hangi faktör neden etkileniyor" sorusunu cevaplamak için yanında tuttum.

## 4. Model ne kadar güvenilir?
Accuracy yerine **recall, precision ve ROC-AUC**'a baktım. Sebebi: müşterilerin zaten %73,5'i kalıyor. Hiçbir şey öğrenmeyen, herkese körü körüne "kalır" diyen saf bir tahmin bile **%73,5 "doğru"** görünür. Yani "accuracy %76" tek başına modelin gerçek başarısını göstermiyor.

## 5. Model nerede yanılıyor?
Test setindeki gerçek ayrılan müşterilerin **~%22'sini kaçırıyorum** (model kalır diyor, müşteri aslında ayrılıyor). Bu en pahalı hata türü, çünkü bu müşteriye hiçbir elde tutma müdahalesi gitmiyor; müşteri sessizce kaybediliyor.

Kaçırdığım grupta dikkat çeken bir örüntü var: test setindeki **tüm** ayrılan müşterilerin %88'i aydan aya sözleşmeliyken **kaçırdığım** grupta bu oran **%49'a** düşüyor. Yani model "uzun sözleşme = güvenli müşteri" genellemesini güçlü öğrenmiş ama bu genellemeye **uymayan** (uzun sözleşmeli olup yine de ayrılan) istisnai müşterileri kaçırıyor. İşe maliyeti şu: uzun sözleşmeli bir müşteri model tarafından "düşük risk" işaretlense bile bu segmenti tamamen gözden çıkarmamak gerekir.

## 6. Tavsiyelerim
1. **"Aydan aya sözleşmeli" müşterilere öncelik verin.** Ayrılanların ezici çoğunluğu burada; uzun sözleşmeye geçiş teşviki (indirim, avantaj karşılığı taahhüt) muhtemelen en yüksek getirili aksiyon.
2. **Modeli aylık çalıştırıp risk skoruna göre sıralanmış bir liste olarak kullanın.** Müşteri temsilcileri "önce bunlarla ilgilenin" diye önceliklendirilsin, model otomatik karar vermesin.
3. **Uzun sözleşmeli ama şikayet/destek sinyali veren müşterileri ayrıca izleyin.** Modelin en zayıf olduğu, gözden kaçırma riskinin en yüksek olduğu segment burası.
4. **Fiber optic internet ve elektronik çek ile ödeme yapan segmentleri ayrıca araştırın.** İkisi de churn ile güçlü ilişkili çıktı ama kök neden (fiyat mı, hizmet kalitesi mi, ödeme sürtünmesi mi) bu veri setinde doğrudan görünmüyor. Anket veya şikayet verisiyle derinleştirilebilir.
