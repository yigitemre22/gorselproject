# TitanFit Spor Salonu Yönetim Sistemi

## Proje Ekibi

* **22010708052 - Yiğit Emre Yörük**
* **23010708038 - Akif Enes Sığırcı**

---

# Kurulum ve Çalıştırma

Uygulamayı çalıştırmak için:

1. Proje klasöründeki **giris.exe** dosyasını çalıştırın.
2. Giriş ekranından kullanıcı rolünüze uygun hesap bilgileriyle sisteme giriş yapın.

---

# Admin Girişi

**E-posta:** [admin@spor.com](mailto:admin@spor.com)
**Şifre:** 123456

## Admin Paneli Özellikleri

### Genel Bakış (Dashboard)

Sisteme giriş yapıldığında görüntülenen ana ekrandır.

Bu bölümde:

* Toplam üye sayısı
* Bu ay elde edilen toplam gelir
* Aktif antrenör sayısı
* Son eklenen üyeler

bilgileri görüntülenebilir.

---

### Üye Yönetimi

Bu bölümden:

* Üye listesi görüntülenebilir.
* Üyelerin aktif/pasif durumları takip edilebilir.
* Üyelik bitiş tarihleri görülebilir.
* Yeni üye eklenebilir.
* Mevcut üyeler düzenlenebilir.
* Üyeler silinebilir.

---

### Antrenör Yönetimi

Bu bölümde:

* Antrenör listesi görüntülenebilir.
* Uzmanlık alanları takip edilebilir.
* İletişim bilgileri görüntülenebilir.
* Maaş bilgileri yönetilebilir.
* Yeni antrenör eklenebilir.
* Antrenör bilgileri güncellenebilir.
* Antrenör kayıtları silinebilir.

---

### Ders Programı

Bu modül sayesinde:

* Ders adı
* Eğitmen
* Ders saati
* Kapasite
* Salon bilgisi

görüntülenebilir ve yönetilebilir.

Ayrıca:

* Yeni ders ekleme
* Ders güncelleme
* Ders silme

işlemleri gerçekleştirilebilir.

---

### Ödeme Kayıtları

Üyelerden alınan ödemelerin takibi yapılır.

Özellikler:

* Tahsilat kaydı oluşturma
* Ödeme yöntemi seçme
* Ödeme tutarı kaydetme
* Ödeme tarihi kaydetme
* Geçmiş ödemeleri listeleme

---

### Ekipman Yönetimi

Bu bölümde spor salonundaki ekipmanlar takip edilir.

Görüntülenen bilgiler:

* Ekipman adı
* Türü
* Adedi
* Durumu (Aktif/Bakımda)
* Alım tarihi

Yapılabilecek işlemler:

* Ekipman ekleme
* Ekipman güncelleme
* Ekipman silme

---

### Stok Takibi

Spor salonunda kullanılan ürünlerin stok yönetimi yapılır.

Örnek ürünler:

* Protein Tozu
* Su
* Havlu
* Takviye Ürünleri

Özellikler:

* Yeni ürün ekleme
* Stok güncelleme
* Mevcut stokları görüntüleme

---

### Kasa ve Giderler

İşletmenin finansal durumunu takip etmek için kullanılır.

Bu bölümde:

* Toplam gelir
* Toplam gider
* Net kasa durumu

görüntülenebilir.

Ayrıca:

* Kira giderleri
* Elektrik giderleri
* Personel maaşları
* Diğer işletme giderleri

sisteme kaydedilebilir.

---

### Raporlar

İşletme verilerinin analiz edilmesini sağlar.

Dışa aktarılabilen raporlar:

* Üye Listesi
* Ödeme Geçmişi
* Kasa ve Gider Raporları
* Antrenör Listesi

Desteklenen format:

* CSV

Ek olarak:

* Kasa Özeti Grafiği
* Üyelik Dağılımı Grafiği

görüntülenebilir.

---

# Antrenör Girişi

### Hesap Bilgileri

| E-posta                                 | Şifre  |
| --------------------------------------- | ------ |
| [ece@spor.com](mailto:ece@spor.com)     | 123456 |
| [kaan@spor.com](mailto:kaan@spor.com)   | 123456 |
| [melis@spor.com](mailto:melis@spor.com) | 123456 |
| [can@spor.com](mailto:can@spor.com)     | 123456 |

---

## Antrenör Paneli Özellikleri

### Genel Bakış (Dashboard)

Antrenör giriş yaptığında:

* Toplam ders sayısını
* Sorumlu olduğu üye sayısını
* Güncel ders programını

görüntüleyebilir.

---

### Derslerim

Bu bölümde antrenör:

* Ders ID
* Ders adı
* Ders saati
* Kapasite
* Salon bilgisi

gibi detayları görüntüleyebilir.

Ayrıca derslere kayıtlı üyelerin:

* Adı
* Soyadı
* Kayıt tarihi

bilgileri listelenir.

---

### Üyelerim

Antrenörün sorumlu olduğu üyeler görüntülenir.

Takip edilebilen bilgiler:

* Ad
* Soyad
* Telefon
* E-posta
* Üyelik tipi
* Üyelik bitiş tarihi
* Üyelik durumu (Aktif/Pasif)

Ayrıca yeni üye kaydı oluşturulabilir.

---

### Üye Gelişim Takibi

Üyelerin fiziksel gelişim süreçleri takip edilir.

Kaydedilen bilgiler:

* Boy
* Kilo
* Yağ oranı

Antrenörler bu verileri görüntüleyebilir ve güncelleyebilir.

---

# Kullanılan Teknolojiler

* Python
* PyQt5
* SQLite
* Pandas
* Matplotlib

---

# Not

Bu proje, spor salonlarının üye, antrenör, ders, ödeme, ekipman ve finansal süreçlerini merkezi bir sistem üzerinden yönetebilmesi amacıyla geliştirilmiştir.
