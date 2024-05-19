import sys
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem


# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('etkinlik_bilet.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Etkinlik (
    etkinlik_id INTEGER PRIMARY KEY,
    etkinlik_adi TEXT,
    tarih TEXT,
    yer TEXT,
    kalan_bilet_sayisi INTEGER
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Kullanicilar (
                 kullanici_id INTEGER PRIMARY KEY,
                 kullanici_adi TEXT NOT NULL,
                 sifre TEXT NOT NULL
                 )''')

c.execute('''CREATE TABLE IF NOT EXISTS Bilet (
                bilet_id INTEGER PRIMARY KEY,
                etkinlik_id INTEGER,
                kullanici_id INTEGER,
                FOREIGN KEY(etkinlik_id) REFERENCES Etkinlik(etkinlik_id),
                FOREIGN KEY(kullanici_id) REFERENCES Kullanicilar(kullanici_id)
            )''')

etkinlikler = [
    (1, "Harry Potter ve Felsefe Taşı", "21.05.2024", "Forum Marmara", 250),
    (2, "Hızlı ve Öfkeli", "22.05.2024", "Cinemaximum", 300),
    (3, "Karlar Ülkesi", "23.05.2024", "City's", 200),
    (4, "Avatar", "24.05.2024", "Megaplex", 350),
    (5, "Örümcek-Adam: Eve Dönüş Yok", "25.05.2024", "Cinecity", 280),
    (6, "Paris", "03.06.2024", "Fransa", 250),
    (7, "Vaadhoo Adası", "05.06.2024", "Maldivler", 300),
    (8, "Roma", "10.06.2024", "İtalya", 200),
    (9, "Venedik", "15.06.2024", "İtalya", 180),
    (10, "New York", "20.06.2024", "ABD", 350),
    (11, "Sertap Erener","25.06.2024", "İstanbul", 350),
    (12, "Sezen Aksu","26.06.2024", "İzmir", 350),
    (13, "Mor ve Ötesi","27.06.2024", "Ankara", 350),
    (14, "Yıldız Tilbe","28.06.2024", "Antalya", 350),
    (15, "Kenan Doğulu","29.06.2024", "Bursa", 350),
    (16,"Real Madrid vs Barcelona", "01.07.2024", "Santiago Bernabeu Stadyumu", 500),
    (17,"AC Milan vs Fenerbahçe", "06.07.2024", "San Siro Stadyumu", 500),
    (18,"Beşiktaş vs Galatasaray", "10.07.2024", "Vodafone Park", 500),
    (19,"Fenerbahçe vs Galatasaray", "19.07.2024", "Şükrü Saracoğlu Stadyumu", 500),
    (20,"Manchester City vs İnter", "29.07.2024", "Etihad Stadyumu", 500)
]
for etkinlik in etkinlikler:
    c.execute("INSERT INTO Etkinlik (etkinlik_id, etkinlik_adi, tarih, yer, kalan_bilet_sayisi) VALUES (?, ?, ?, ?, ?)", etkinlik)

# Veritabanına değişiklikleri kaydet
conn.commit()
# Veritabanı bağlantısını kapat
conn.close()

class etkinlikbiletsistemi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etkinlik Bilet Sistemi")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):
        self.etkinlik_button = QPushButton("Etkinlik Yönetimi")
        self.katilimci_button = QPushButton("Katılımcı Yönetimi")
        self.bilet_button = QPushButton("Bilet Yönetimi")
        self.etkinlikpencere_button = QPushButton("Etkinlikleri Görüntüle")
        self.cikis_button = QPushButton("Çıkış")

        self.layout.addWidget(self.etkinlik_button)
        self.layout.addWidget(self.katilimci_button)
        self.layout.addWidget(self.bilet_button)
        self.layout.addWidget(self.etkinlikpencere_button)
        self.layout.addWidget(self.cikis_button)

        self.etkinlik_button.clicked.connect(self.etkinlik_penceresi)
        self.katilimci_button.clicked.connect(self.katilimci_penceresi)
        self.bilet_button.clicked.connect(self.bilet_penceresi)
        self.etkinlikpencere_button.clicked.connect(self.etkinlikpencere)
        self.cikis_button.clicked.connect(self.close)

    def etkinlik_penceresi(self):
        self.etkinlik_pencere = EtkinlikPenceresi()
        self.etkinlik_pencere.show()

    def katilimci_penceresi(self):
        self.katilimci_pencere = KatilimciPenceresi()
        self.katilimci_pencere.show()

    def bilet_penceresi(self):
        self.bilet_pencere = BiletPenceresi()
        self.bilet_pencere.show()

    def etkinlikpencere(self):
        self.etkinlikpencere = etkinlikpencere()
        self.etkinlikpencere.show()


class EtkinlikPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Etkinlik Bilgileri Ekleme ve Listeleme")
        self.setGeometry(100, 100, 600, 400)

        self.etkinlik_id_label = QLabel("Etkinlik ID:", self)
        self.etkinlik_id_label.move(50, 50)
        self.etkinlik_id = QLineEdit(self)
        self.etkinlik_id.move(150, 50)

        self.etkinlik_adi_label = QLabel("Etkinlik Adı:", self)
        self.etkinlik_adi_label.move(50, 100)
        self.etkinlik_adi = QLineEdit(self)
        self.etkinlik_adi.move(150, 100)

        self.tarih_label = QLabel("Tarih:", self)
        self.tarih_label.move(50, 150)
        self.tarih = QLineEdit(self)
        self.tarih.move(150, 150)

        self.yer_label = QLabel("Yer:", self)
        self.yer_label.move(50, 200)
        self.yer = QLineEdit(self)
        self.yer.move(150, 200)

        self.kalan_bilet_label = QLabel("Kalan Bilet Sayısı:", self)
        self.kalan_bilet_label.move(50, 250)
        self.kalan_bilet_sayisi = QLineEdit(self)
        self.kalan_bilet_sayisi.move(150, 250)

        self.kaydet_btn = QPushButton("Kaydet", self)
        self.kaydet_btn.move(150, 300)
        self.kaydet_btn.clicked.connect(self.kaydet)

        self.tablo = QTableWidget(self)
        self.tablo.setGeometry(300, 50, 280, 300)
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["Etkinlik ID","Etkinlik Adı", "Tarih", "Yer", "Kalan Bilet Sayısı"])

        self.baglanti = sqlite3.connect("etkinlik_bilet.db")
        self.cursor = self.baglanti.cursor()

        self.etkinlikleri_listele()

    def kaydet(self):
        etkinlik_adi = self.etkinlik_adi.text()
        tarih = self.tarih.text()
        yer = self.yer.text()
        kalan_bilet_sayisi = int(self.kalan_bilet_sayisi.text())

        self.cursor.execute("INSERT INTO Etkinlik (etkinlik_id, etkinlik_adi, tarih, yer, kalan_bilet_sayisi) VALUES (?, ?, ?, ?, ?)",
                            (self.etkinlik_id.text(), etkinlik_adi, tarih, yer, kalan_bilet_sayisi))
        self.baglanti.commit()
        print("Etkinlik başarıyla kaydedildi.")
        self.etkinlikleri_listele()

    def etkinlikleri_listele(self):
        self.cursor.execute("SELECT * FROM Etkinlik")
        etkinlikler = self.cursor.fetchall()

        self.tablo.setRowCount(0)
        for row_number, row_data in enumerate(etkinlikler):
            self.tablo.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tablo.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def closeEvent(self, event):
        self.baglanti.close()

class KatilimciPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Katılımcı Penceresi")
        self.setGeometry(0, 0, 800, 600)

        self.etkinlik_tableWidget = QTableWidget()
        self.etkinlik_tableWidget.setRowCount(0)
        self.etkinlik_tableWidget.setColumnCount(5)
        self.etkinlik_tableWidget.setHorizontalHeaderLabels(["Etkinlik ID","Etkinlik Adı", "Tarih", "Yer", "Kalan Bilet Sayısı"])

        self.kullanici_tableWidget = QTableWidget()
        self.kullanici_tableWidget.setRowCount(0)
        self.kullanici_tableWidget.setColumnCount(1)
        self.kullanici_tableWidget.setHorizontalHeaderLabels(["Kullanıcı Adı"])

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.etkinlik_tableWidget)
        self.layout.addWidget(self.kullanici_tableWidget)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.goster()

    def goster(self):
        self.baglanti = sqlite3.connect("etkinlik_bilet.db")
        self.cursor = self.baglanti.cursor()

        # Etkinlik tablosunu doldur
        self.cursor.execute("SELECT * FROM Etkinlik")
        etkinlikler = self.cursor.fetchall()

        self.etkinlik_tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(etkinlikler):
            self.etkinlik_tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.etkinlik_tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Kullanıcı tablosunu doldur
        self.cursor.execute("SELECT kullanici_adi FROM Kullanicilar")
        kullanicilar = self.cursor.fetchall()

        self.kullanici_tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(kullanicilar):
            self.kullanici_tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.kullanici_tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.baglanti.close()



class BiletPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bilet Alma Uygulaması")
        self.setGeometry(100, 100, 600, 400)

        self.etkinlik_id_label = QLabel("Etkinlik ID:", self)
        self.etkinlik_id_label.move(50, 50)
        self.etkinlik_id = QLineEdit(self)
        self.etkinlik_id.move(150, 50)

        self.kullanici_id_label = QLabel("Kullanıcı ID:", self)
        self.kullanici_id_label.move(50, 100)
        self.kullanici_id = QLineEdit(self)
        self.kullanici_id.move(150, 100)

        self.bilet_al_btn = QPushButton("Bilet Al", self)
        self.bilet_al_btn.move(150, 150)
        self.bilet_al_btn.clicked.connect(self.bilet_al)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 200, 500, 150)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Etkinlik ID", "Kullanıcı ID", "Kalan Bilet Sayısı"])

        self.baglanti_olustur()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("etkinlik_bilet.db")
        self.cursor = self.baglanti.cursor()

    def bilet_al(self):
        etkinlik_id = self.etkinlik_id.text()
        kullanici_id = self.kullanici_id.text()

        if not etkinlik_id or not kullanici_id:
            QMessageBox.warning(self, "Uyarı", "Etkinlik ID ve Kullanıcı ID alanları boş olamaz.")
            return

        try:
            etkinlik_id = int(etkinlik_id)
            kullanici_id = int(kullanici_id)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Etkinlik ID ve Kullanıcı ID tamsayı olmalıdır.")
            return

        self.cursor.execute("SELECT kalan_bilet_sayisi FROM Etkinlik WHERE etkinlik_id = ?", (etkinlik_id,))
        etkinlik = self.cursor.fetchone()

        if etkinlik:
            kalan_bilet_sayisi = etkinlik[0]
            if kalan_bilet_sayisi > 0:
                self.cursor.execute("INSERT INTO Bilet (etkinlik_id, kullanici_id) VALUES (?, ?)", (etkinlik_id, kullanici_id))
                self.baglanti.commit()
                self.cursor.execute("UPDATE Etkinlik SET kalan_bilet_sayisi = ? WHERE etkinlik_id = ?", (kalan_bilet_sayisi - 1, etkinlik_id))
                self.baglanti.commit()
                QMessageBox.information(self, "Bilgi", "Bilet başarıyla alındı.")
                self.guncelle_tablo()
            else:
                QMessageBox.warning(self, "Uyarı", "Üzgünüz, bu etkinlik için bilet kalmamıştır.")

    def guncelle_tablo(self):
        self.cursor.execute(
            "SELECT Bilet.etkinlik_id, Bilet.kullanici_id, Etkinlik.kalan_bilet_sayisi FROM Bilet LEFT JOIN Etkinlik ON Bilet.etkinlik_id = Etkinlik.etkinlik_id")
        biletler = self.cursor.fetchall()
        self.table_widget.setRowCount(len(biletler))
        for index, bilet in enumerate(biletler):
            etkinlik_id, kullanici_id, kalan_bilet_sayisi = bilet[0], bilet[1], bilet[2]
            self.table_widget.setItem(index, 0, QTableWidgetItem(str(etkinlik_id)))
            self.table_widget.setItem(index, 1, QTableWidgetItem(str(kullanici_id)))
            if kalan_bilet_sayisi is None:
                QMessageBox.warning(self, "Uyarı", f"Etkinlik ID: {etkinlik_id} ile eşleşen kayıt bulunamadı.")
            else:
                self.table_widget.setItem(index, 2, QTableWidgetItem(str(kalan_bilet_sayisi)))


class etkinlikpencere(QMainWindow):
    def __init__(self):
        super(etkinlikpencere, self).__init__()
        self.setWindowTitle("etkinlik pencere")
        self.setGeometry(0, 0, 950, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Resimler
        self.label_sinema_resim = QLabel(central_widget)
        self.label_sinema_resim.setGeometry(30, 200, 200, 200)
        self.set_image(self.label_sinema_resim, "C:\\Users\\pc\\Downloads\\proje4foto\\sinema_resmi.png")

        self.label_tatil_resim = QLabel(central_widget)
        self.label_tatil_resim.setGeometry(260, 200, 200, 200)
        self.set_image(self.label_tatil_resim, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil_resmi2.jpg")

        self.label_konser_resim = QLabel(central_widget)
        self.label_konser_resim.setGeometry(490, 200, 200, 200)
        self.set_image(self.label_konser_resim, "C:\\Users\\pc\\Downloads\\proje4foto\\konser_resmi.jpg")

        self.label_mac_resim = QLabel(central_widget)
        self.label_mac_resim.setGeometry(720, 200, 200, 200)
        self.set_image(self.label_mac_resim, "C:\\Users\\pc\\Downloads\\proje4foto\\maç_resmi.jpeg")

        self.label_sinema = QLabel("SİNEMA", central_widget)
        self.label_sinema.setGeometry(30, 290, 200, 30)
        self.setup_label_text(self.label_sinema)

        self.label_tatil = QLabel("TATİL", central_widget)
        self.label_tatil.setGeometry(260, 290, 200, 30)
        self.setup_label_text(self.label_tatil)

        self.label_konser = QLabel("KONSER", central_widget)
        self.label_konser.setGeometry(490, 290, 200, 30)
        self.setup_label_text(self.label_konser)

        self.label_mac = QLabel("MAÇ", central_widget)
        self.label_mac.setGeometry(720, 290, 200, 30)
        self.setup_label_text(self.label_mac)

        self.label_etkinlik = QLabel("Etkinlik Seç", central_widget)
        self.label_etkinlik.setGeometry(390, 100, 200, 30)
        self.setup_label_text(self.label_etkinlik)

        # Seç butonları
        self.pushButton_sinema = QPushButton("Seç", central_widget)
        self.pushButton_sinema.setGeometry(80, 430, 100, 30)
        self.setup_button(self.pushButton_sinema)

        self.pushButton_tatil = QPushButton("Seç", central_widget)
        self.pushButton_tatil.setGeometry(310, 430, 100, 30)
        self.setup_button(self.pushButton_tatil)

        self.pushButton_konser = QPushButton("Seç", central_widget)
        self.pushButton_konser.setGeometry(540, 430, 100, 30)
        self.setup_button(self.pushButton_konser)

        self.pushButton_mac = QPushButton("Seç", central_widget)
        self.pushButton_mac.setGeometry(770, 430, 100, 30)
        self.setup_button(self.pushButton_mac)

        self.pushButton_sinema.clicked.connect(self.open_sinema_window)
        self.pushButton_tatil.clicked.connect(self.open_tatil_window)
        self.pushButton_konser.clicked.connect(self.open_konser_window)
        self.pushButton_mac.clicked.connect(self.open_mac_window)

    def setup_label_text(self, label):
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 100);")
        label.setFont(QFont('Arial', 12))
    def set_image(self, label, path):
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)


    def setup_button(self, button):
        button.setStyleSheet("#pushButton_sinema{background-color: rgb(216, 216, 216);} #pushButton_sinema:pressed{background-color: rgb(170, 170, 255);}")
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet("color: #3B3B3B;")

    def setup_button(self, button):
        button.setStyleSheet("#pushButton_tatil{background-color: rgb(216, 216, 216);} #pushButton_tatil:pressed{background-color: rgb(170, 170, 255);}")
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet("color: #3B3B3B;")

    def setup_button(self, button):
        button.setStyleSheet("#pushButton_konser{background-color: rgb(216, 216, 216);} #pushButton_konser:pressed{background-color: rgb(170, 170, 255);}")
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet("color: #3B3B3B;")

    def setup_button(self, button):
        button.setStyleSheet("#pushButton_mac{background-color: rgb(216, 216, 216);} #pushButton_mac:pressed{background-color: rgb(170, 170, 255);}")
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet("color: #3B3B3B;")

    def open_sinema_window(self):
        self.sinema_window = sinemapencere()
        self.sinema_window.show()

    def open_tatil_window(self):
        self.tatil_window = tatilpencere()
        self.tatil_window.show()

    def open_konser_window(self):
        self.konser_window = konserpencere()
        self.konser_window.show()

    def open_mac_window(self):
        self.mac_window = macpencere()
        self.mac_window.show()

class sinemapencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Film Biletleri")

        film_ismi1 = QLabel("Harry Potter ve Felsefe Taşı", self)
        film_ismi1.setGeometry(5, 300, 180, 20)

        film_ismi2 = QLabel("Hızlı ve Öfkeli", self)
        film_ismi2.setGeometry(210, 300, 100, 20)

        film_ismi3 = QLabel("Karlar Ülkesi", self)
        film_ismi3.setGeometry(390, 300, 71, 20)

        film_ismi4 = QLabel("Avatar", self)
        film_ismi4.setGeometry(570, 300, 38, 20)

        film_ismi5 = QLabel("Örümcek-Adam: Eve Dönüş Yok", self)
        film_ismi5.setGeometry(675, 300, 185, 20)

        label_11 = QLabel("150 TL", self)
        label_11.setGeometry(65, 330, 40, 20)

        label_12 = QLabel("170 TL", self)
        label_12.setGeometry(230, 330, 40, 20)

        label_13 = QLabel("110 TL", self)
        label_13.setGeometry(410, 330, 40, 20)

        label_14 = QLabel("140 TL", self)
        label_14.setGeometry(570, 330, 40, 20)

        label_15 = QLabel("190 TL", self)
        label_15.setGeometry(740, 330, 40, 20)

        label_16 = QLabel("Hangi filme bilet alacaksınız?", self)
        label_16.setGeometry(300, 60, 300, 40)
        label_16.setFont(QFont("Arial", 14))

        label_17 = QLabel("ETKİNLİK ID:1", self)
        label_17.setGeometry(45, 400, 100, 20)

        label_18 = QLabel("ETKİNLİK ID:2", self)
        label_18.setGeometry(205, 400, 100, 20)

        label_19= QLabel("ETKİNLİK ID:3", self)
        label_19.setGeometry(380, 400, 100, 20)

        label_20 = QLabel("ETKİNLİK ID:4", self)
        label_20.setGeometry(550, 400, 100, 20)

        label_21 = QLabel("ETKİNLİK ID:5", self)
        label_21.setGeometry(720, 400, 100, 20)

        self.film_button1 = QPushButton("Bilet Al", self)
        self.film_button1.setGeometry(15, 440, 75, 23)
        self.film_button1.clicked.connect(self.bilet_penceresi_ac)

        self.film_button2 = QPushButton("Bilet Al", self)
        self.film_button2.setGeometry(180, 440, 75, 23)
        self.film_button2.clicked.connect(self.bilet_penceresi_ac)

        self.film_button3 = QPushButton("Bilet Al", self)
        self.film_button3.setGeometry(350, 440, 75, 23)
        self.film_button3.clicked.connect(self.bilet_penceresi_ac)

        self.film_button4 = QPushButton("Bilet Al", self)
        self.film_button4.setGeometry(520, 440, 75, 23)
        self.film_button4.clicked.connect(self.bilet_penceresi_ac)

        self.film_button5 = QPushButton("Bilet Al", self)
        self.film_button5.setGeometry(690, 440, 75, 23)
        self.film_button5.clicked.connect(self.bilet_penceresi_ac)

        film_spinbox1 = QSpinBox(self)
        film_spinbox1.setGeometry(105, 440, 42, 22)

        film_spinbox2 = QSpinBox(self)
        film_spinbox2.setGeometry(270, 440, 42, 22)

        film_spinbox3 = QSpinBox(self)
        film_spinbox3.setGeometry(440, 440, 42, 22)

        film_spinbox4 = QSpinBox(self)
        film_spinbox4.setGeometry(610, 440, 42, 22)

        film_spinbox5 = QSpinBox(self)
        film_spinbox5.setGeometry(780, 440, 42, 22)

        # Resimleri ekleyelim
        pixmap1 = QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\film1.jpg")
        label1 = QLabel(self)
        label1.setPixmap(pixmap1.scaled(141, 200, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        label1.setGeometry(10, 100, 141, 200)

        pixmap2 = QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\film2.jpg")
        label2 = QLabel(self)
        label2.setPixmap(pixmap2.scaled(141, 200, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        label2.setGeometry(180, 100, 141, 200)

        pixmap3 = QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\film3.jpg")
        label3 = QLabel(self)
        label3.setPixmap(pixmap3.scaled(141, 200, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        label3.setGeometry(350, 100, 141, 200)

        pixmap4 = QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\film4.jpeg")
        label4 = QLabel(self)
        label4.setPixmap(pixmap4.scaled(141, 200, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        label4.setGeometry(520, 100, 141, 200)

        pixmap5 = QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\film5.jpg")
        label5 = QLabel(self)
        label5.setPixmap(pixmap5.scaled(141, 200, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        label5.setGeometry(690, 100, 141, 200)

        self.setGeometry(100, 100, 860, 500)

    def bilet_penceresi_ac(self):
        # Bilet penceresini aç
        self.bilet_penceresi = BiletPenceresi()
        self.bilet_penceresi.show()




class tatilpencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 850, 600)
        self.setWindowTitle("Tatil Penceresi")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.initUI()

        self.tatilresim1 = QLabel(self.centralwidget)
        self.tatilresim1.setGeometry(10, 150, 150, 200)
        self.tatilresim1.setText("")
        self.set_image(self.tatilresim1, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil1.jpg")
        self.tatilresim1.setScaledContents(True)

        self.tatilresim2 = QLabel(self.centralwidget)
        self.tatilresim2.setGeometry(180, 150, 150, 200)
        self.tatilresim2.setText("")
        self.set_image(self.tatilresim2, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil2.jpg")
        self.tatilresim2.setScaledContents(True)

        self.tatilresim3 = QLabel(self.centralwidget)
        self.tatilresim3.setGeometry(350, 150, 150, 200)
        self.tatilresim3.setText("")
        self.set_image(self.tatilresim3, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil3.jpg")
        self.tatilresim3.setScaledContents(True)

        self.tatilresim4 = QLabel(self.centralwidget)
        self.tatilresim4.setGeometry(520, 150, 150, 200)
        self.tatilresim4.setText("")
        self.set_image(self.tatilresim4, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil4.jpg")
        self.tatilresim4.setScaledContents(True)

        self.tatilresim5 = QLabel(self.centralwidget)
        self.tatilresim5.setGeometry(690, 150, 150, 200)
        self.tatilresim5.setText("")
        self.set_image(self.tatilresim5, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil5.jpg")
        self.tatilresim5.setScaledContents(True)

        self.tatilisim1 = QLabel(self.centralwidget)
        self.tatilisim1.setGeometry(50, 235, 151, 31)
        font = self.tatilisim1.font()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.tatilisim1.setFont(font)
        self.tatilisim1.setStyleSheet("color: rgb(255, 255, 255);")
        self.tatilisim1.setText("Paris")

        self.tatilisim2 = QLabel(self.centralwidget)
        self.tatilisim2.setGeometry(195, 225, 151, 31)
        self.tatilisim2.setFont(font)
        self.tatilisim2.setStyleSheet("color: rgb(255, 255, 255);")
        self.tatilisim2.setText("Vaadhoo")

        self.tatilisim2_2 = QLabel(self.centralwidget)
        self.tatilisim2_2.setGeometry(215, 250, 151, 31)
        self.tatilisim2_2.setFont(font)
        self.tatilisim2_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.tatilisim2_2.setText("Adası")

        self.tatilisim3 = QLabel(self.centralwidget)
        self.tatilisim3.setGeometry(390, 235, 151, 31)
        self.tatilisim3.setFont(font)
        self.tatilisim3.setStyleSheet("color: rgb(255, 255, 255);")
        self.tatilisim3.setText("Roma")

        self.tatilisim4 = QLabel(self.centralwidget)
        self.tatilisim4.setGeometry(545, 235, 151, 31)
        self.tatilisim4.setFont(font)
        self.tatilisim4.setStyleSheet("color: rgb(255, 255, 255);")
        self.tatilisim4.setText("Venedik")

        self.tatilisim5 = QLabel(self.centralwidget)
        self.tatilisim5.setGeometry(703, 235, 151, 31)
        self.tatilisim5.setFont(font)
        self.tatilisim5.setStyleSheet("color: rgb(255, 255, 255);")
        self.tatilisim5.setText("New York")

        self.tatil_button1 = QPushButton("Bilet Al", self)
        self.tatil_button1.setGeometry(20, 400, 75, 23)
        self.tatil_button1.clicked.connect(self.bilet_penceresi_ac)

        self.tatil_button2 = QPushButton("Bilet Al", self)
        self.tatil_button2.setGeometry(190, 400, 75, 23)
        self.tatil_button2.clicked.connect(self.bilet_penceresi_ac)

        self.tatil_button3 = QPushButton("Bilet Al", self)
        self.tatil_button3.setGeometry(360, 400, 75, 23)
        self.tatil_button3.clicked.connect(self.bilet_penceresi_ac)

        self.tatil_button4 = QPushButton("Bilet Al", self)
        self.tatil_button4.setGeometry(530, 400, 75, 23)
        self.tatil_button4.clicked.connect(self.bilet_penceresi_ac)

        self.tatil_button5 = QPushButton("Bilet Al", self)
        self.tatil_button5.setGeometry(700, 400, 75, 23)
        self.tatil_button5.clicked.connect(self.bilet_penceresi_ac)

        self.tatilspinbox1 = QSpinBox(self.centralwidget)
        self.tatilspinbox1.setGeometry(110, 400, 42, 22)

        self.tatilspinbox2 = QSpinBox(self.centralwidget)
        self.tatilspinbox2.setGeometry(280, 400, 42, 22)

        self.tatilspinbox3 = QSpinBox(self.centralwidget)
        self.tatilspinbox3.setGeometry(450, 400, 42, 22)

        self.tatilspinbox4 = QSpinBox(self.centralwidget)
        self.tatilspinbox4.setGeometry(620, 400, 42, 22)

        self.tatilspinbox5 = QSpinBox(self.centralwidget)
        self.tatilspinbox5.setGeometry(790, 400, 42, 22)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setGeometry(70, 370, 47, 13)
        self.label_12.setText("2000 TL")

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setGeometry(240, 370, 47, 13)
        self.label_13.setText("1700 TL")

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setGeometry(410, 370, 47, 13)
        self.label_14.setText("1900 TL")

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setGeometry(580, 370, 47, 13)
        self.label_15.setText("1500 TL")

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setGeometry(750, 370, 47, 13)
        self.label_16.setText("2200 TL")

        label_17 = QLabel("ETKİNLİK ID:6", self)
        label_17.setGeometry(45, 450, 100, 20)

        label_18 = QLabel("ETKİNLİK ID:7", self)
        label_18.setGeometry(215, 450, 100, 20)

        label_19= QLabel("ETKİNLİK ID:8", self)
        label_19.setGeometry(390, 450, 100, 20)

        label_20 = QLabel("ETKİNLİK ID:9", self)
        label_20.setGeometry(560, 450, 100, 20)

        label_21 = QLabel("ETKİNLİK ID:10", self)
        label_21.setGeometry(720, 450, 100, 20)

        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setGeometry(230, 60, 420, 50)
        font = self.label_17.font()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label_17.setFont(font)
        self.label_17.setText("Nereye tatile gitmek istersiniz?")

    def initUI(self):
        self.label_tatil1_resim = QLabel(self)
        self.set_image(self.label_tatil1_resim, "C:\\Users\\pc\\Downloads\\proje4foto\\tatil1_resmi.jpg")

    def set_image(self, label, image_path):
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def bilet_penceresi_ac(self):
        # Bilet penceresini aç
        self.bilet_penceresi = BiletPenceresi()
        self.bilet_penceresi.show()


class konserpencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 850, 600)
        self.setWindowTitle("Konser pencere")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.konserafis1 = QLabel(central_widget)
        self.konserafis1.setGeometry(10, 150, 150, 200)
        self.konserafis1.setPixmap(QPixmap("C://Users//pc//Downloads//proje4foto//konser1.png"))
        self.konserafis1.setScaledContents(True)

        self.konserafis2 = QLabel(central_widget)
        self.konserafis2.setGeometry(180, 150, 150, 200)
        self.konserafis2.setPixmap(QPixmap("C://Users//pc//Downloads//proje4foto//konser2.jpg"))
        self.konserafis2.setScaledContents(True)

        self.konserafis3 = QLabel(central_widget)
        self.konserafis3.setGeometry(350, 150, 150, 200)
        self.konserafis3.setPixmap(QPixmap("C://Users//pc//Downloads//proje4foto//konser3.png"))
        self.konserafis3.setScaledContents(True)

        self.konserafis4 = QLabel(central_widget)
        self.konserafis4.setGeometry(520, 150, 150, 200)
        self.konserafis4.setPixmap(QPixmap("C://Users/pc//Downloads//proje4foto//konser4.jpeg"))
        self.konserafis4.setScaledContents(True)

        self.konserafis5 = QLabel(central_widget)
        self.konserafis5.setGeometry(690, 150, 150, 200)
        self.konserafis5.setPixmap(QPixmap("C://Users//pc//Downloads//proje4foto//konser5.jpeg"))
        self.konserafis5.setScaledContents(True)

        self.konser_button1 = QPushButton("Bilet Al", self)
        self.konser_button1.setGeometry(20, 440, 75, 23)
        self.konser_button1.clicked.connect(self.bilet_penceresi_ac)

        self.konser_button2 = QPushButton("Bilet Al", self)
        self.konser_button2.setGeometry(190, 440, 75, 23)
        self.konser_button2.clicked.connect(self.bilet_penceresi_ac)

        self.konser_button3 = QPushButton("Bilet Al", self)
        self.konser_button3.setGeometry(360, 440, 75, 23)
        self.konser_button3.clicked.connect(self.bilet_penceresi_ac)

        self.konser_button4 = QPushButton("Bilet Al", self)
        self.konser_button4.setGeometry(530, 440, 75, 23)
        self.konser_button4.clicked.connect(self.bilet_penceresi_ac)

        self.konser_button5 = QPushButton("Bilet Al", self)
        self.konser_button5.setGeometry(700, 440, 75, 23)
        self.konser_button5.clicked.connect(self.bilet_penceresi_ac)

        self.konserspinbox1 = QSpinBox(central_widget)
        self.konserspinbox1.setGeometry(110, 440, 42, 22)

        self.konserspinbox2 = QSpinBox(central_widget)
        self.konserspinbox2.setGeometry(280, 440, 42, 22)

        self.konserspinbox3 = QSpinBox(central_widget)
        self.konserspinbox3.setGeometry(450, 440, 42, 22)

        self.konserspinbox4 = QSpinBox(central_widget)
        self.konserspinbox4.setGeometry(620, 440, 42, 22)

        self.konserspinbox5 = QSpinBox(central_widget)
        self.konserspinbox5.setGeometry(790, 440, 42, 22)

        self.konserisim1 = QLabel(" Sertap Erener ", central_widget)
        self.konserisim1.setGeometry(10, 350, 170, 25)
        self.konserisim1.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")

        self.konserisim2 = QLabel("   Sezen Aksu", central_widget)
        self.konserisim2.setGeometry(175, 350, 160, 25)
        self.konserisim2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")

        self.konserisim3 = QLabel("  Mor ve Ötesi", central_widget)
        self.konserisim3.setGeometry(350, 350, 150, 25)
        self.konserisim3.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")

        self.konserisim4 = QLabel("   Yıldız Tilbe", central_widget)
        self.konserisim4.setGeometry(525, 350, 150, 25)
        self.konserisim4.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")

        self.konserisim5 = QLabel(" Kenan Doğulu", central_widget)
        self.konserisim5.setGeometry(690, 350, 150, 29)
        self.konserisim5.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")

        self.label_11 = QLabel("300 TL", central_widget)
        self.label_11.setGeometry(60, 410, 60, 20)
        self.label_11.setFont(QFont(None, 10))

        self.label_12 = QLabel("250 TL", central_widget)
        self.label_12.setGeometry(230, 410, 60, 20)
        self.label_12.setFont(QFont(None, 10))

        self.label_13 = QLabel("230 TL", central_widget)
        self.label_13.setGeometry(400, 410, 60, 20)
        self.label_13.setFont(QFont(None, 10))

        self.label_14 = QLabel("150 TL", central_widget)
        self.label_14.setGeometry(570, 410, 60, 20)
        self.label_14.setFont(QFont(None, 10))

        self.label_15 = QLabel("190 TL", central_widget)
        self.label_15.setGeometry(740, 410, 60, 20)
        self.label_15.setFont(QFont(None, 10))

        label_17 = QLabel("ETKİNLİK ID:11", self)
        label_17.setGeometry(45, 500, 100, 20)

        label_18 = QLabel("ETKİNLİK ID:12", self)
        label_18.setGeometry(215, 500, 100, 20)

        label_19= QLabel("ETKİNLİK ID:13", self)
        label_19.setGeometry(390, 500, 100, 20)

        label_20 = QLabel("ETKİNLİK ID:14", self)
        label_20.setGeometry(560, 500, 100, 20)

        label_21 = QLabel("ETKİNLİK ID:15", self)
        label_21.setGeometry(720, 500, 100, 20)


        self.label_16 = QLabel("Hangi konsere gitmek istersiniz?", central_widget)
        self.label_16.setGeometry(220, 60, 440, 50)
        font = self.label_16.font()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label_16.setFont(font)

    def bilet_penceresi_ac(self):
        # Bilet penceresini aç
        self.bilet_penceresi = BiletPenceresi()
        self.bilet_penceresi.show()

class macpencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 850, 600)
        self.setWindowTitle("Maç pencere")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.macresim1 = QLabel(central_widget)
        self.macresim1.setGeometry(30, 70, 250, 150)
        self.macresim1.setPixmap(QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\maç1.jpg"))
        self.macresim1.setScaledContents(True)

        self.macresim2 = QLabel(central_widget)
        self.macresim2.setGeometry(30, 240, 250, 150)
        self.macresim2.setPixmap(QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\maç2.png"))
        self.macresim2.setScaledContents(True)

        self.macresim3 = QLabel(central_widget)
        self.macresim3.setGeometry(30, 410, 250, 150)
        self.macresim3.setPixmap(QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\maç3.jpeg"))
        self.macresim3.setScaledContents(True)

        self.macresim4 = QLabel(central_widget)
        self.macresim4.setGeometry(540, 70, 250, 150)
        self.macresim4.setPixmap(QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\maç4.jpeg"))
        self.macresim4.setScaledContents(True)

        self.macresim5 = QLabel(central_widget)
        self.macresim5.setGeometry(540, 320, 250, 150)
        self.macresim5.setPixmap(QPixmap("C:\\Users\\pc\\Downloads\\proje4foto\\maç5.png"))
        self.macresim5.setScaledContents(True)

        self.label_16 = QLabel("Hangi maça gitmek istersiniz?", central_widget)
        self.label_16.setGeometry(240, 20, 420, 41)
        font = self.label_16.font()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label_16.setFont(font)

        self.macisim1 = QLabel("Real Madrid vs Barcelona", central_widget)
        self.macisim1.setGeometry(290, 90, 230, 20)
        self.macisim1.setFont(QFont(None, 10))

        self.macisim2 = QLabel("AC Milan vs Fenerbahçe", central_widget)
        self.macisim2.setGeometry(290, 260, 230, 20)
        self.macisim2.setFont(QFont(None, 10))

        self.macisim3 = QLabel("Beşiktaş vs Galatasaray", central_widget)
        self.macisim3.setGeometry(290, 430, 245, 20)
        self.macisim3.setFont(QFont(None, 10))

        self.macisim4 = QLabel("Fenerbahçe vs Galatasaray", central_widget)
        self.macisim4.setGeometry(545, 230, 245, 20)
        self.macisim4.setFont(QFont(None, 10))

        self.macisim5 = QLabel("Manchester City vs İnter", central_widget)
        self.macisim5.setGeometry(555, 480, 230, 20)
        self.macisim5.setFont(QFont(None, 10))

        self.label_11 = QLabel("1900 TL", central_widget)
        self.label_11.setGeometry(350, 140, 50, 16)

        self.label_12 = QLabel("1200 TL", central_widget)
        self.label_12.setGeometry(350, 310, 50, 16)

        self.label_13 = QLabel("1000 TL", central_widget)
        self.label_13.setGeometry(350, 480, 50, 16)

        self.label_14 = QLabel("1000 TL", central_widget)
        self.label_14.setGeometry(640, 260, 50, 16)

        self.label_15 = QLabel("1800 TL", central_widget)
        self.label_15.setGeometry(640, 510, 50, 16)

        label_17 = QLabel("ETKİNLİK ID:16", self)
        label_17.setGeometry(320, 190, 100, 20)

        label_18 = QLabel("ETKİNLİK ID:17", self)
        label_18.setGeometry(320, 360, 100, 20)

        label_19= QLabel("ETKİNLİK ID:18", self)
        label_19.setGeometry(320, 530, 100, 20)

        label_20 = QLabel("ETKİNLİK ID:19", self)
        label_20.setGeometry(730, 280, 100, 20)

        label_21 = QLabel("ETKİNLİK ID:20", self)
        label_21.setGeometry(730, 530, 100, 20)

        self.mac_button1 = QPushButton("Bilet Al", self)
        self.mac_button1.setGeometry(290, 160, 75, 23)
        self.mac_button1.clicked.connect(self.bilet_penceresi_ac)

        self.mac_button2 = QPushButton("Bilet Al", self)
        self.mac_button2.setGeometry(290, 330, 75, 23)
        self.mac_button2.clicked.connect(self.bilet_penceresi_ac)

        self.mac_button3 = QPushButton("Bilet Al", self)
        self.mac_button3.setGeometry(290, 500, 75, 23)
        self.mac_button3.clicked.connect(self.bilet_penceresi_ac)

        self.mac_button4 = QPushButton("Bilet Al", self)
        self.mac_button4.setGeometry(570, 280, 75, 23)
        self.mac_button4.clicked.connect(self.bilet_penceresi_ac)

        self.mac_button5 = QPushButton("Bilet Al", self)
        self.mac_button5.setGeometry(570, 530, 75, 23)
        self.mac_button5.clicked.connect(self.bilet_penceresi_ac)

        self.macspinbox1 = QSpinBox(central_widget)
        self.macspinbox1.setGeometry(380, 160, 42, 22)

        self.macspinbox2 = QSpinBox(central_widget)
        self.macspinbox2.setGeometry(380, 330, 42, 22)

        self.macspinbox3 = QSpinBox(central_widget)
        self.macspinbox3.setGeometry(380, 500, 42, 22)

        self.macspinbox4 = QSpinBox(central_widget)
        self.macspinbox4.setGeometry(680, 280, 42, 22)

        self.macspinbox5 = QSpinBox(central_widget)
        self.macspinbox5.setGeometry(680, 530, 42, 22)

    def bilet_penceresi_ac(self):
        # Bilet penceresini aç
        self.bilet_penceresi = BiletPenceresi()
        self.bilet_penceresi.show()

class UserLoginApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(100, 100, 400, 300)

        self.username_label = QLabel("Kullanıcı Adı:", self)
        self.username_entry = QLineEdit(self)
        self.password_label = QLabel("Şifre:", self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Giriş Yap", self)
        self.register_button = QPushButton("Kayıt Ol", self)
        self.help_button = QPushButton("Kullanım Kılavuzu", self)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.help_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.login_button.clicked.connect(self.open_etkinlikbiletsistemi)
        self.register_button.clicked.connect(self.register)
        self.help_button.clicked.connect(self.show_help)

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        connection = sqlite3.connect("etkinlik_bilet.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            QMessageBox.information(self, "Giriş Başarılı", f"Hoş Geldiniz, {username}!")
            self.open_etkinlikbiletsistemi()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")

    def open_etkinlikbiletsistemi(self):
        self.etkinlikbiletsistemi = etkinlikbiletsistemi()
        self.etkinlikbiletsistemi.setWindowTitle("Etkinlik Bilet Sistemi")
        self.etkinlikbiletsistemi.setGeometry(200, 200, 600, 400)
        self.etkinlikbiletsistemi.show()

    def register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        connection = sqlite3.connect("etkinlik_bilet.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()

        QMessageBox.information(self, "Başarılı", "Kayıt işlemi başarıyla tamamlandı.")

    def show_help(self):
        help_text = """
Kullanım Kılavuzu:

1. Kullanıcı Giriş Sayfası:
    - Kullanıcı adı ve şifrenizi ilgili alanlara girin.
    - "Giriş Yap" butonuna tıklayarak sisteme giriş yapın.
    - Eğer daha önce kayıt olmadıysanız, "Kayıt Ol" butonuna tıklayarak yeni bir hesap oluşturabilirsiniz.
    - Yardım almak için "Kullanım Kılavuzu" butonuna tıklayabilirsiniz.

2. Ana Sayfa:

Etkinlik Seçimi

Etkinlik biletleri almak için "Etkinlik ID" ve "Kullanıcı ID" alanlarını doldurun.
"Etkinlik ID" ve "Kullanıcı ID" alanları boş olamaz.
Girilen değerlerin tamsayı olduğundan emin olun.

Bilet Alma

"Bilet Al" düğmesine tıklayın.
Etkinlik için yeterli bilet sayısı varsa, bilet başarıyla alınır.
Yeterli bilet yoksa, uyarı mesajı görüntülenir.

        """
        QMessageBox.information(self, "Kullanım Kılavuzu", help_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = UserLoginApp()
    pencere.show()
    sys.exit(app.exec_())


