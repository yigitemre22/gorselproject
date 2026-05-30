CREATE DATABASE IF NOT EXISTS spor_salonu;
USE spor_salonu;

-- =========================
-- TABLOLAR
-- =========================

CREATE TABLE kullanicilar (
    kullanici_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    sifre VARCHAR(255) NOT NULL,
    rol ENUM('admin','personel','antrenor') DEFAULT 'personel',
    telefon VARCHAR(20),
    aktif BOOLEAN DEFAULT TRUE,
    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uyelik_tipleri (
    uyelik_tip_id INT AUTO_INCREMENT PRIMARY KEY,
    tip_adi VARCHAR(50) NOT NULL,
    sure_ay INT NOT NULL,
    fiyat DECIMAL(10,2) NOT NULL,
    aciklama TEXT
);

CREATE TABLE uyeler (
    uye_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    tc_no VARCHAR(11) UNIQUE,
    telefon VARCHAR(20),
    email VARCHAR(100),
    dogum_tarihi DATE,
    cinsiyet ENUM('Erkek','Kadın'),
    adres TEXT,
    uyelik_tip_id INT,
    kayit_tarihi DATE DEFAULT (CURRENT_DATE),
    uyelik_baslangic DATE,
    uyelik_bitis DATE,
    durum ENUM('aktif','pasif') DEFAULT 'aktif',
    FOREIGN KEY (uyelik_tip_id) REFERENCES uyelik_tipleri(uyelik_tip_id)
);

CREATE TABLE antrenorler (
    antrenor_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    uzmanlik VARCHAR(100),
    telefon VARCHAR(20),
    email VARCHAR(100),
    maas DECIMAL(10,2),
    ise_baslama DATE
);

CREATE TABLE dersler (
    ders_id INT AUTO_INCREMENT PRIMARY KEY,
    ders_adi VARCHAR(100) NOT NULL,
    antrenor_id INT,
    ders_saati TIME,
    kapasite INT,
    salon VARCHAR(50),
    FOREIGN KEY (antrenor_id) REFERENCES antrenorler(antrenor_id)
);

CREATE TABLE uyeDers (
    uye_ders_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT,
    ders_id INT,
    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uye_id) REFERENCES uyeler(uye_id),
    FOREIGN KEY (ders_id) REFERENCES dersler(ders_id)
);

CREATE TABLE uye_Antrenor (
    uye_antrenor_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT,
    antrenor_id INT,
    baslangic_tarihi DATE,
    FOREIGN KEY (uye_id) REFERENCES uyeler(uye_id),
    FOREIGN KEY (antrenor_id) REFERENCES antrenorler(antrenor_id)
);

CREATE TABLE ekipman_turleri (
    ekipman_tur_id INT AUTO_INCREMENT PRIMARY KEY,
    tur_adi VARCHAR(100) NOT NULL
);

CREATE TABLE ekipmanlar (
    ekipman_id INT AUTO_INCREMENT PRIMARY KEY,
    ekipman_adi VARCHAR(100) NOT NULL,
    ekipman_tur_id INT,
    adet INT DEFAULT 0,
    durum ENUM('aktif','bakimda','arizali') DEFAULT 'aktif',
    alim_tarihi DATE,
    FOREIGN KEY (ekipman_tur_id) REFERENCES ekipman_turleri(ekipman_tur_id)
);

CREATE TABLE stoklar (
    stok_id INT AUTO_INCREMENT PRIMARY KEY,
    urun_adi VARCHAR(100),
    miktar INT,
    birim VARCHAR(20),
    son_guncelleme TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE odeme_yontemleri (
    odeme_yontem_id INT AUTO_INCREMENT PRIMARY KEY,
    yontem_adi VARCHAR(50)
);

CREATE TABLE odemeler (
    odeme_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT,
    odeme_yontem_id INT,
    tutar DECIMAL(10,2),
    odeme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aciklama TEXT,
    FOREIGN KEY (uye_id) REFERENCES uyeler(uye_id),
    FOREIGN KEY (odeme_yontem_id) REFERENCES odeme_yontemleri(odeme_yontem_id)
);

CREATE TABLE kasa (
    kasa_id INT AUTO_INCREMENT PRIMARY KEY,
    islem_tipi ENUM('gelir','gider'),
    tutar DECIMAL(10,2),
    aciklama TEXT,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE giderler (
    gider_id INT AUTO_INCREMENT PRIMARY KEY,
    gider_turu VARCHAR(100),
    tutar DECIMAL(10,2),
    gider_tarihi DATE,
    aciklama TEXT
);

CREATE TABLE girisCikisKayitlari (
    kayit_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT,
    giris_saati DATETIME,
    cikis_saati DATETIME,
    FOREIGN KEY (uye_id) REFERENCES uyeler(uye_id)
);

CREATE TABLE gelisim (
    gelisim_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT,
    kilo DECIMAL(5,2),
    boy DECIMAL(5,2),
    yag_orani DECIMAL(5,2),
    kayit_tarihi DATE,
    FOREIGN KEY (uye_id) REFERENCES uyeler(uye_id)
);

CREATE TABLE sistem_ayarlari (
    ayar_id INT AUTO_INCREMENT PRIMARY KEY,
    ayar_adi VARCHAR(100),
    ayar_degeri TEXT
);

-- =========================
-- ÖRNEK VERİLER
-- =========================

INSERT INTO kullanicilar(ad,soyad,email,sifre,rol,telefon) VALUES
('Ahmet','Yılmaz','admin@spor.com','123456','admin','05550000001'),
('Mehmet','Kara','personel@spor.com','123456','personel','05550000002'),
('Ayşe','Demir','antrenor@spor.com','123456','antrenor','05550000003');

INSERT INTO uyelik_tipleri(tip_adi,sure_ay,fiyat,aciklama) VALUES
('Aylık',1,1500,'1 aylık standart üyelik'),
('3 Aylık',3,4000,'3 aylık üyelik'),
('Yıllık',12,12000,'12 aylık premium üyelik');

INSERT INTO uyeler(ad,soyad,tc_no,telefon,email,dogum_tarihi,cinsiyet,adres,uyelik_tip_id,uyelik_baslangic,uyelik_bitis) VALUES
('Emre','Çelik','12345678901','05551112233','emre@gmail.com','2001-05-10','Erkek','İstanbul',1,'2026-05-01','2026-06-01'),
('Zeynep','Kurt','12345678902','05554443322','zeynep@gmail.com','1999-08-15','Kadın','Ankara',2,'2026-05-01','2026-08-01'),
('Burak','Aydın','12345678903','05556667788','burak@gmail.com','1998-01-20','Erkek','İzmir',3,'2026-01-01','2027-01-01'),
('Mert','Koç','12345678904','05551234567','mert@gmail.com','2000-03-11','Erkek','Bursa',1,'2026-04-10','2026-05-10'),
('Elif','Şahin','12345678905','05557654321','elif@gmail.com','2002-07-19','Kadın','Antalya',2,'2026-03-01','2026-06-01'),
('Can','Eren','12345678906','05553456789','can@gmail.com','1997-09-09','Erkek','Adana',1,'2026-05-05','2026-06-05'),
('Sude','Yılmaz','12345678907','05559876543','sude@gmail.com','2003-12-01','Kadın','Samsun',3,'2026-01-01','2027-01-01'),
('Furkan','Taş','12345678908','05554321987','furkan@gmail.com','1995-10-25','Erkek','Trabzon',1,'2026-05-08','2026-06-08');

INSERT INTO antrenorler(ad,soyad,uzmanlik,telefon,email,maas,ise_baslama) VALUES
('Can','Arslan','Fitness','05558889900','can@spor.com',35000,'2025-01-10'),
('Ece','Yıldız','Pilates','05559998877','ece@spor.com',32000,'2025-02-15'),
('Kaan','Bulut','Crossfit','05557774411','kaan@spor.com',36000,'2025-03-12'),
('Melis','Aksoy','Yoga','05556661122','melis@spor.com',31000,'2025-04-18');

INSERT INTO dersler(ders_adi,antrenor_id,ders_saati,kapasite,salon) VALUES
('Fitness Başlangıç',1,'10:00:00',20,'Salon A'),
('Pilates',2,'14:00:00',15,'Salon B'),
('Crossfit',3,'18:00:00',12,'Salon C'),
('Yoga',4,'09:00:00',18,'Salon D'),
('İleri Seviye Fitness',1,'20:00:00',10,'Salon A');

INSERT INTO uyeDers(uye_id,ders_id) VALUES
(1,1),
(1,3),
(2,2),
(2,4),
(3,3),
(4,1),
(5,2),
(6,5),
(7,4),
(8,3);

INSERT INTO uye_Antrenor(uye_id,antrenor_id,baslangic_tarihi) VALUES
(1,1,'2026-05-01'),
(2,2,'2026-05-02');

INSERT INTO ekipman_turleri(tur_adi) VALUES
('Kardiyo'),
('Ağırlık'),
('Fonksiyonel');

INSERT INTO ekipmanlar(ekipman_adi,ekipman_tur_id,adet,durum,alim_tarihi) VALUES
('Koşu Bandı',1,5,'aktif','2025-03-01'),
('Eliptik Bisiklet',1,4,'aktif','2025-03-10'),
('Dikey Bisiklet',1,3,'aktif','2025-04-01'),
('Dambıl Seti',2,20,'aktif','2025-04-10'),
('Bench Press',2,4,'aktif','2025-04-15'),
('Leg Press',2,2,'aktif','2025-04-20'),
('Smith Machine',2,2,'bakimda','2025-04-22'),
('Kettlebell',3,10,'bakimda','2025-05-12'),
('Battle Rope',3,6,'aktif','2025-05-15'),
('TRX Askı Sistemi',3,5,'aktif','2025-05-18');

INSERT INTO stoklar(urun_adi,miktar,birim) VALUES
('Protein Tozu',25,'adet'),
('BCAA',15,'adet'),
('Enerji İçeceği',40,'kutu'),
('Su',100,'şişe'),
('Havlu',50,'adet'),
('Temizlik Spreyi',20,'adet'),
('Eldiven',35,'çift'),
('Yoga Matı',12,'adet');

INSERT INTO odeme_yontemleri(yontem_adi) VALUES
('Nakit'),
('Kredi Kartı'),
('Havale');

INSERT INTO odemeler(uye_id,odeme_yontem_id,tutar,aciklama) VALUES
(1,2,1500,'Aylık üyelik ödemesi'),
(2,1,4000,'3 aylık üyelik'),
(3,3,12000,'Yıllık üyelik'),
(4,2,1500,'Aylık üyelik'),
(5,1,4000,'3 aylık üyelik'),
(6,2,1500,'Aylık üyelik'),
(7,3,12000,'Yıllık üyelik'),
(8,1,1500,'Aylık üyelik');

INSERT INTO kasa(islem_tipi,tutar,aciklama) VALUES
('gelir',1500,'Üyelik ödemesi'),
('gelir',4000,'Üyelik ödemesi'),
('gider',2500,'Elektrik faturası');

INSERT INTO giderler(gider_turu,tutar,gider_tarihi,aciklama) VALUES
('Elektrik',2500,'2026-05-01','Aylık elektrik faturası'),
('Su',1200,'2026-05-03','Su faturası'),
('Temizlik',3000,'2026-05-05','Temizlik gideri'),
('İnternet',850,'2026-05-06','Fiber internet faturası'),
('Bakım',5000,'2026-05-10','Ekipman bakım gideri'),
('Personel Yemek',2200,'2026-05-11','Personel yemek gideri');

INSERT INTO girisCikisKayitlari(uye_id,giris_saati,cikis_saati) VALUES
(1,'2026-05-15 10:00:00','2026-05-15 12:00:00'),
(2,'2026-05-15 13:00:00','2026-05-15 15:00:00'),
(3,'2026-05-15 09:00:00','2026-05-15 11:00:00'),
(4,'2026-05-15 18:00:00','2026-05-15 20:00:00'),
(5,'2026-05-16 08:00:00','2026-05-16 10:00:00'),
(6,'2026-05-16 12:00:00','2026-05-16 14:00:00');

INSERT INTO gelisim(uye_id,kilo,boy,yag_orani,kayit_tarihi) VALUES
(1,78.5,1.80,18.5,'2026-05-01'),
(2,60.2,1.68,22.1,'2026-05-01'),
(3,92.3,1.85,25.0,'2026-05-02'),
(4,81.4,1.78,19.7,'2026-05-02'),
(5,55.6,1.65,20.4,'2026-05-03'),
(6,74.0,1.76,17.2,'2026-05-03'),
(7,58.5,1.70,21.3,'2026-05-04'),
(8,88.8,1.82,24.5,'2026-05-04');

INSERT INTO sistem_ayarlari(ayar_adi,ayar_degeri) VALUES
('Salon Adi','TitanFit Gym'),
('Acilis Saati','07:00'),
('Kapanis Saati','23:00');

-- =========================
-- PROCEDURELER
-- =========================

DELIMITER $$

CREATE PROCEDURE uye_ekle(
    IN p_ad VARCHAR(50),
    IN p_soyad VARCHAR(50),
    IN p_tc VARCHAR(11),
    IN p_tel VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_tip INT
)
BEGIN
    INSERT INTO uyeler(
        ad, soyad, tc_no, telefon, email,
        uyelik_tip_id, uyelik_baslangic, uyelik_bitis
    )
    VALUES(
        p_ad,
        p_soyad,
        p_tc,
        p_tel,
        p_email,
        p_tip,
        CURDATE(),
        DATE_ADD(CURDATE(), INTERVAL 1 MONTH)
    );
END $$

CREATE PROCEDURE ekipman_ekle(
    IN p_ekipman_adi VARCHAR(100),
    IN p_tur_id INT,
    IN p_adet INT
)
BEGIN
    INSERT INTO ekipmanlar(
        ekipman_adi,
        ekipman_tur_id,
        adet,
        durum,
        alim_tarihi
    )
    VALUES(
        p_ekipman_adi,
        p_tur_id,
        p_adet,
        'aktif',
        CURDATE()
    );
END $$

CREATE PROCEDURE odeme_ekle(
    IN p_uye_id INT,
    IN p_odeme_yontemi INT,
    IN p_tutar DECIMAL(10,2),
    IN p_aciklama TEXT
)
BEGIN
    INSERT INTO odemeler(
        uye_id,
        odeme_yontem_id,
        tutar,
        aciklama
    )
    VALUES(
        p_uye_id,
        p_odeme_yontemi,
        p_tutar,
        p_aciklama
    );

    INSERT INTO kasa(
        islem_tipi,
        tutar,
        aciklama
    )
    VALUES(
        'gelir',
        p_tutar,
        p_aciklama
    );
END $$

CREATE PROCEDURE uye_giris(
    IN p_uye_id INT
)
BEGIN
    INSERT INTO girisCikisKayitlari(
        uye_id,
        giris_saati
    )
    VALUES(
        p_uye_id,
        NOW()
    );
END $$

CREATE PROCEDURE uye_cikis(
    IN p_uye_id INT
)
BEGIN
    UPDATE girisCikisKayitlari
    SET cikis_saati = NOW()
    WHERE uye_id = p_uye_id
    ORDER BY kayit_id DESC
    LIMIT 1;
END $$

DELIMITER ;

-- =========================
-- TRIGGERLER
-- =========================

DELIMITER $$

CREATE TRIGGER trg_gider_kasa
AFTER INSERT ON giderler
FOR EACH ROW
BEGIN
    INSERT INTO kasa(islem_tipi,tutar,aciklama)
    VALUES('gider',NEW.tutar,NEW.aciklama);
END $$

DELIMITER ;

-- =========================
-- VIEWLER
-- =========================

CREATE VIEW aktif_uyeler AS
SELECT
    u.uye_id,
    u.ad,
    u.soyad,
    ut.tip_adi,
    u.uyelik_bitis
FROM uyeler u
JOIN uyelik_tipleri ut
ON u.uyelik_tip_id = ut.uyelik_tip_id
WHERE u.durum = 'aktif';

CREATE VIEW kasa_ozeti AS
SELECT
    islem_tipi,
    SUM(tutar) AS toplam
FROM kasa
GROUP BY islem_tipi;

-- =========================
-- ÖRNEK KULLANIMLAR
-- =========================

CALL uye_ekle(
    'Ali',
    'Vural',
    '12312312312',
    '05557778899',
    'ali@gmail.com',
    1
);

CALL ekipman_ekle(
    'Bench Press',
    2,
    3
);

CALL odeme_ekle(
    1,
    2,
    2000,
    'Ek ödeme'
);

CALL uye_giris(1);
CALL uye_cikis(1);

SELECT * FROM aktif_uyeler;
SELECT * FROM kasa_ozeti;



ALTER TABLE antrenorler 
ADD COLUMN sifre VARCHAR(255) NOT NULL DEFAULT '123456',
ADD UNIQUE (email);
