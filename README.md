# NLP-Natural-Language-Processing-
Final Project


### Otel attributelerinin belirlenmesi ve Word2Vect kullanımı:
<div class='text-justify'>
Programın anlamlı bir çıktı elde edebilmesi için, dataset üzerinde birçok işlevin ayrı ayrı çalıştırılması ve bu işlemler sonucunda belirli çıktılar üretmesi beklenen bir olaydır. Çoğu zaman oluşan bu çıktılar diğer işlemlerin girdileri mahiyetinde olmaktadır. Bu sebele bazı işlemler program çalışma sırasında değil önceden ayrı olarak çalıştırılıp sonuçlarının ayrı bir dizide daha sonra kullanaılmak üzere tutulması yöntemiyle yapılacaktır.  
  
Ayrıca tüm programı tek bir kod parçasıyla yapılması veya tüm işi sadece pc'ye bırakmak gibi de bir vaadimiz yoktu. Mevcut veri setinin küçüklüğü, bazı algoritmaları kullanırken gereklilikleri karşılayamamakta ve yetersiz kalmaktadır. Bu işlev pogramın sunum sırasında daha kısa sürede çalışmasına olanak verecektir. Bu sebeple program iki ana parçaya bölündü.  

#### İlk parçası: 
- Otel özelliklerinin, en çok kullanılan kelimler arasından belirlenmesi: L_WordCount.py ile yapılmakta olup sonuçları L_WordCount_output.txt dosyasında bulunmaktadır. Bu dosyadan faydalanarak 10 otel özelliği seçilmiştir.
- W2V yardımıyla bu attributelerle aynı anlam/görevde kullanılan kelimelerin, ismi geçen algoritmalardan da yararlanarak* bulunmasıdır: L_W2V.py ile yapılmakta olup sonuçları L_W2V_output dosyası içindedir. İki farklı preprocceessing işlemi uygulanarak 5+5 kez deneme yapılmış ve sonuçlarına kıyaslamalı bakılarak her bir otel özelliğini temsil eden 5 yeni kelime daha belirlenmiştir. 
- İş bu proje kapsamında bu iki işlem önceden yapılıp sonuçları kullanılacaktır.
</div>
