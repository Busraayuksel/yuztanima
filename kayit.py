from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from form import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import sys
import cv2
import os
import database as db


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("ÖĞRENCİ KAYIT ")
        self.setWindowIcon(QIcon('icon.png'))
        self.showMaximized()

        
        self.camera.setToolTip('kamera butonu')
        self.takephoto.setToolTip('resim çek butonu')
        self.Kaydet.setToolTip('kaydet butonu')

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        self.camera.clicked.connect(self.start_camera)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.sinifComboBox.addItems(['1','2','3','4'])
        self.cinsiyetComboBox.addItems(['KIZ','ERKEK'])

        self.Kaydet.setEnabled(False)

    def enable_save_button(self):
        if self.ogrNoEdit.text() == '' and self.yuz is None:
            self.Kaydet.setEnabled(False)
        else:
            self.Kaydet.setEnabled(True)
            self.Kaydet.clicked.connect(self.save)
            self.Kaydet.clicked.connect(lambda:QApplication.quit())
        
    def save(self):
        no = self.ogrNoEdit.text()
        ad = self.adEdit.text().upper()
        soyad = self.soyadEdit.text().upper()
        dgmtrh = self.dgmtrhEdit.text()
        sinif = self.sinifComboBox.currentText()
        cinsiyet = self.cinsiyetComboBox.currentText()

        database = db.DataBase(no, ad, soyad, dgmtrh, sinif, cinsiyet)
        
        database.add_Student()

    def box(self,x):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("BİLDİRİM")
        msg.setWindowTitle("!!!!!!")
        msg.setInformativeText(x)
        msg.exec_()

    def start_camera(self):
        no = self.ogrNoEdit.text()
        if no == '':
            self.box('ÖNCELİKLE AŞAĞIDAKİ KİŞİSEL BİLGİLERİ EKSİKSİZ DOLDURUN. BİLGİLERİNİZ GİRİLMEDEN RESİM ÇEKEMEZSİNİZ!!!')
        elif len(no) != 9:
            message = "Öğrenci No ALANINI KONTROL EDİN. EKSİK YA DA FAZLA KARAKTER GİRMİŞ OLABİLİRSİNİZ"
            self.box(message)
        elif no.isdigit() == False:
            message ="Öğrenci No ALANINI KONTROL EDİN. RAKAM GİRDİĞİNİZDEN EMİN OLUN."
            self.box(message)
        else:
            self.capture = cv2.VideoCapture(0)
            self.timer.start(30)
            self.enable_save_button()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_image(image)

    def display_image(self, image):
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image.setPixmap(pixmap)
        self.takephoto.clicked.connect(self.takephotos)
    
    def studentFaceDirectory(self,face):
        path = "C:/Users/busra/Desktop/yuztanima/StudentFace"
        if not os.path.exists(path):
            os.makedirs("StudentFace")
        else:
            print('dosya zaten var')
        
        studentNO = self.ogrNoEdit.text()
        dosya_adi = "{}.png".format(studentNO)
        file_path = os.path.join(path, dosya_adi)
        if os.path.exists(file_path):
            self.box("ÖĞRENCİ NO'YU KONTROL ET. BU NUMARA KAYITLI!!!")
            self.Kaydet.setEnabled(False)
            return False
        else:
            cv2.imwrite(file_path, face)
        
    def takephotos(self):
        ret, frame = self.capture.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 2)
            if len(faces) == 1:
                for (x, y, w, h) in faces:
                    face = frame[y:y + h, x:x + w]
                    self.studentFaceDirectory(face)     
                    ogrNo = self.ogrNoEdit.text()
                    image_file = "{}.jpg".format(ogrNo)
                    cv2.imwrite(image_file, face)
                    pixmap = QPixmap(image_file)
                    self.yuz.setPixmap(pixmap)
                    os.remove(image_file)
                    self.takephoto.setText("Resmi Tekrar Çek")
                    self.takephoto.clicked.connect(lambda :self.again_take_photo())
                    break
            elif len(faces) > 1:
                self.box("TEK BİR KİŞİ FOTOĞRAF ÇEKEBİLİR.")
            else :
                self.box("YÜZÜNÜZ TAM GÖRÜNECEK ŞEKİLDE TEKRAR RESMİ ÇEKİN.")
        
        self.capture.release()
        cv2.destroyAllWindows()

    def again_take_photo(self):
        self.takephoto.clicked.disconnect()
        self.takephoto.clicked.connect(self.takephotos)
        self.yuz.setPixmap(QPixmap()) # resmi ekrandan sil 
        studentNO = self.ogrNoEdit.text()
        file_path = "StudentFace/{}.png".format(studentNO)
        if os.path.exists(file_path):
            os.remove(file_path)
        self.takephoto.setText("Resim Çek")

def app():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

app()