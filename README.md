# NLP-Natural-Language-Processing-
Final Project

### Dataset:
<div class='text-justify'>
  Sonuçlarının kalitesi Datasatinin kalitesi kadardır! a benzer güzel bir yorum vardı. Evet veriyle uğraşıyoruz veri üzerinde bir takım işlmeler yapıyoruz dolayısıyla verimizin güzellii ölçüsünde sonuçlarımızda güzel olacaktır. Dataseti aldığımız kaynakta datasette 27329 yorum olduğu söylensede yapılan incelemeler neticesinde bu yorumların:  431 tanesi "<U+03BD>" gibi geçersi karakterlerden oluştuğu ve 3350 tane yorumun ise farklı dillerle oluşturulduğu gözlemlenmiştir. Bu sayılar mevcut veri göz önünde bulundurulduğunda gözardı edilemeyecek kadar büyük olduğu için yukarıda bahsedilen alakasız yorumlar önce languageDetection.py vasıtasıyla tespit edildiler. Daha sonra bu cümlelerde tekrar edilen ve ingilizcede var olmayan harf ve kelimeler tespit edildi. Bu harf/kelime grupları (på, ich, wir, des, ò, ci, Bij, piu, Che dire, Ci, è, un, ed, ó, á, ä, å, di, ç, ğ, ş, ö, ü) excel yardımıyla datasetten çıkartıldı.

### Otel attributelerinin belirlenmesi ve Word2Vect kullanımı:
<div class='text-justify'>
Programın anlamlı bir çıktı elde edebilmesi için, dataset üzerinde birçok işlevin ayrı ayrı çalıştırılması ve bu işlemler sonucunda belirli çıktılar üretmesi beklenen bir olaydır. Çoğu zaman oluşan bu çıktılar diğer işlemlerin girdileri mahiyetinde olmaktadır. Bu sebele bazı işlemler program çalışma sırasında değil önceden ayrı olarak çalıştırılıp sonuçlarının ayrı bir dizide daha sonra kullanaılmak üzere tutulması yöntemiyle yapılacaktır.  
  
Ayrıca tüm programı tek bir kod parçasıyla yapılması veya tüm işi sadece pc'ye bırakmak gibi de bir vaadimiz yoktu. Mevcut veri setinin küçüklüğü, bazı algoritmaları kullanırken gereklilikleri karşılayamamakta ve yetersiz kalmaktadır. Bu işlev pogramın sunum sırasında daha kısa sürede çalışmasına olanak verecektir. Bu sebeple program iki ana parçaya bölündü.  

#### İlk parçası: 
- Otel özelliklerinin, en çok kullanılan kelimler arasından belirlenmesi: L_WordCount.py ile yapılmakta olup sonuçları L_WordCount_output.txt dosyasında bulunmaktadır. Bu dosyadan faydalanarak 10 otel özelliği seçilmiştir.Bunlar:  
  
  &nbsp;&nbsp;&nbsp;&nbsp;'hotel', 43923  
  &nbsp;&nbsp;&nbsp;&nbsp;'room', 39174  
  &nbsp;&nbsp;&nbsp;&nbsp;'staff', 18214  
  &nbsp;&nbsp;&nbsp;&nbsp;'service', 13370  
  &nbsp;&nbsp;&nbsp;&nbsp;'breakfast', 12217  
  &nbsp;&nbsp;&nbsp;&nbsp;'bar', 9490  
  &nbsp;&nbsp;&nbsp;&nbsp;'location', 8806  
  &nbsp;&nbsp;&nbsp;&nbsp;'restaurant', 7014  
  &nbsp;&nbsp;&nbsp;&nbsp;'bathroom', 5377  
  &nbsp;&nbsp;&nbsp;&nbsp;'food', 5368  
  &nbsp;&nbsp;&nbsp;&nbsp;'bed': 6015  
  &nbsp;&nbsp;&nbsp;&nbsp;'view': 4586  
  

- W2V ve Fasttext yardımıyla bu attributelerle aynı anlam/görevde kullanılan kelimelerin, ismi geçen algoritmalardan da yararlanarak* bulunmasıdır: L_W2V.py ile yapılmakta olup sonuçları L_W2V_output dosyası içindedir. İki farklı preprocceessing ve farklı train parametrelerikullanılarak 20 kez deneme yapılmış ve sonuçlarına kıyaslamalı bakılarak her bir otel özelliğini temsil eden birkaç yeni kelime daha belirlenmiştir. Bunlar:  
  
&nbsp;1. Most similar to ['staff'] 	-> ('team', 0.5600), ('employee', 0.49374), ('everyone', 0.5933), ('host', 0.5027), ('staf', 0.8581), ('staffer', 0.8724), ('staffmember', 0.7315)  
&nbsp;2. Most similar to ['location'] -> ('position', 0.7028), ('located', 0.5157), ('spot', 0.4717), ('locatie', 0.8049), ('located', 0.7731), ('localisation', 0.8129)  
&nbsp;3. Most similar to ['room']     -> ('bedroom', 0.5666), ('rooom', 0.9447), ('roooms', 0.8848) 
&nbsp;4. Most similar to ['breakfast']-> ('breackfast', 0.5005), ('breakfeast', 0.4910), ('breakfats', 0.9595), ('brekfast', 0.9437),('breakfest', 0.8730), ('bfast', 0.8107)  
&nbsp;5. Most similar to ['bed']      -> ('pillow', 0.5807), ('mattress', 0.5692), ('chair', 0.5139), ('bedding', 0.5044),  ('bedsheets', 0.8430), ('beds', 0.9087)  
&nbsp;6. Most similar to ['service']  -> ('sevice', 0.4480), ('presentation', 0.4408), ('deliver', 0.4151), ('housekeep', 0.4263),  ('seervice', 0.9216), ('roomservice', 0.9031), ('servicing', 0.8990)  
&nbsp;7. Most similar to ['bathroom'] -> ('bathrooms', 0.7026), ('bath', 0.6796), ('bathtub', 0.6052), ('shower', 0.5574), ('tub', 0.5549), ('toilet', 0.5324), ('bathrooom', 0.9944),  ('bathrom', 0.9467)  
&nbsp;8. Most similar to ['view']     -> ('overlook', 0.7513), ('facing', 0.5536), ('views', 0.9849), ('viewing', 0.8934), ('vieuw', 0.8517), ('viewpoint', 0.8269), ('overview', 0.8269)  
&nbsp;9. Most similar to ['food']     -> ('meal', 0.6452), ('dish', 0.5842), ('menu', 0.5589), ('lunch', 0.5225), ('dinner', 0.5218)
&nbsp;10. Most similar to ['restaurant'] -> ('restaurants', 0.5152), ('restaruant', 0.5104), ('eatery', 0.4917), ('dining', 0.4839), ('restuarant', 0.4917), ('hotelrestaurant', 0.9543)  
  


- İş bu proje kapsamında bu iki işlem önceden yapılıp sonuçları kullanılacaktır.
</div>
