import sqlite3
from prettytable import PrettyTable


conn = sqlite3.connect('ogrenci_isleri.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS ogrenciler
             (ogrenci_id INTEGER PRIMARY KEY ,
             ad TEXT,
             soyad TEXT,
             bolum TEXT)''')


c.execute('''CREATE TABLE IF NOT EXISTS dersler
             (ders_id TEXT PRIMARY KEY,
             ders_adi TEXT)''')


c.execute('''CREATE TABLE IF NOT EXISTS notlar
             (not_id INTEGER PRIMARY KEY AUTOINCREMENT,
             ogrenci_id INTEGER,
             ders_adi TEXT,
             not_degeri INTEGER,
             FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(ogrenci_id),
             FOREIGN KEY (ders_adi) REFERENCES dersler(ders_adi))''')


c.execute('''CREATE TABLE IF NOT EXISTS staj_bilgisi
             (staj_id INTEGER PRIMARY KEY AUTOINCREMENT,
             ogrenci_id INTEGER,
             staj_yeri TEXT,
             durum TEXT CHECK(durum IN ('yapildi', 'yapilmadi')),
             FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(ogrenci_id))''')


conn.commit()
conn.close()


def ogrenci_ekle(ogrenci_id, ad, soyad, bolum):
    try:
        conn = sqlite3.connect('ogrenci_isleri.db')
        c = conn.cursor()
        c.execute("INSERT INTO ogrenciler (ogrenci_id, ad, soyad, bolum) VALUES (?, ?, ?, ?)", (ogrenci_id, ad, soyad, bolum))
        conn.commit()
        print("Öğrenci başarıyla eklendi.")
    except sqlite3.Error as e:
        print("Hata:", e)
    finally:
        conn.close()


def ders_ekle(ders_id, ders_adi):
    try:
        conn = sqlite3.connect('ogrenci_isleri.db')
        c = conn.cursor()
        c.execute("INSERT INTO dersler (ders_id, ders_adi) VALUES (?, ?)", (ders_id, ders_adi))
        conn.commit()
        print("Ders başarıyla eklendi.")
    except sqlite3.Error as e:
        print("Hata:", e)
    finally:
        conn.close()


def not_ekle(ogrenci_id, ders_adi, not_degeri):
    try:
        conn = sqlite3.connect('ogrenci_isleri.db')
        c = conn.cursor()
        c.execute("INSERT INTO notlar (ogrenci_id, ders_adi, not_degeri) VALUES (?, ?, ?)", (ogrenci_id, ders_adi, not_degeri))
        conn.commit()
        print("Not başarıyla eklendi.")
    except sqlite3.Error as e:
        print("Hata:", e)
    finally:
        conn.close()


def staj_bilgisi_ekle(ogrenci_id, staj_yeri, durum):
    try:
        conn = sqlite3.connect('ogrenci_isleri.db')
        c = conn.cursor()
        c.execute("INSERT INTO staj_bilgisi (ogrenci_id, staj_yeri, durum) VALUES (?, ?, ?)", (ogrenci_id, staj_yeri, durum))
        conn.commit()
        print("Staj bilgisi başarıyla eklendi.")
    except sqlite3.Error as e:
        print("Hata:", e)
    finally:
        conn.close()


def ogrenci_bilgisi_ekrani():
    try:
        conn = sqlite3.connect('ogrenci_isleri.db')
        c = conn.cursor()

        c.execute('''SELECT ogrenciler.ogrenci_id, ogrenciler.ad, ogrenciler.soyad, ogrenciler.bolum, dersler.ders_adi, notlar.not_degeri, staj_bilgisi.durum
                     FROM ogrenciler
                     
                     LEFT JOIN notlar ON ogrenciler.ogrenci_id = notlar.ogrenci_id
                     LEFT JOIN dersler ON notlar.ders_adi = dersler.ders_adi
                     LEFT JOIN staj_bilgisi ON ogrenciler.ogrenci_id = staj_bilgisi.ogrenci_id''')
        rows = c.fetchall()

        table = PrettyTable(['Öğrenci No', 'Ad', 'Soyad', 'Bölüm', 'Ders Adı', 'Not', 'Staj Durumu'])
        for row in rows:
            table.add_row(row)


        print(table)
    except sqlite3.Error as e:
        print("Hata:", e)
    finally:
        conn.close()



while True:
    print("\n--- Öğrenci İşleri Otomasyonu ---")
    print("1. Öğrenci Ekle")
    print("2. Ders Ekle")
    print("3. Not Ekle")
    print("4. Staj Bilgisi Ekle")
    print("5. Öğrenci Bilgisi Ekranı")
    print("0. Çıkış")

    secim = input("Seçiminizi yapın (0-5): ")

    if secim == '1':
        ogrenci_id = input("Öğrenci No: ")
        ad = input("Öğrenci adı: ")
        soyad = input("Öğrenci soyadı: ")
        bolum = input("Öğrenci bölümü: ")
        ogrenci_ekle(ogrenci_id, ad, soyad, bolum)

    elif secim == '2':
        ders_id = input("Ders Kodu: ")
        ders_adi = input("Ders adı: ")
        ders_ekle(ders_id, ders_adi)

    elif secim == '3':
        ogrenci_id = input("Öğrenci No: ")
        ders_adi = input("Ders Adı: ")
        not_degeri = input("Not değeri: ")
        not_ekle(ogrenci_id, ders_adi, not_degeri)

    elif secim == '4':
        ogrenci_id = input("Öğrenci No: ")
        staj_yeri = input("Staj yeri: ")
        durum = input("Staj durumu ('yapildi' veya 'yapilmadi'): ")
        staj_bilgisi_ekle(ogrenci_id, staj_yeri, durum)

    elif secim == '5':
        ogrenci_bilgisi_ekrani()

    elif secim == '0':
        break

    else:
        print("Geçersiz seçim. Tekrar deneyin.")
