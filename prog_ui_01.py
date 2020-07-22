from PyQt5 import QtWidgets, uic, QtGui

import sys
import cv2
import numpy as np

#1. qt를 사용하여 GUI 프로그램 환경 구축
class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('test4.ui', self)

        self.loadBtn = self.findChild(QtWidgets.QPushButton, 'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked)
        self.procBtn = self.findChild(QtWidgets.QPushButton, 'procBtn')
        self.procBtn.clicked.connect(self.procRunClicked) 
        self.photo = self.findChild(QtWidgets.QLabel, 'photo')     
        self.photo.setPixmap(QtGui.QPixmap("images/pawns.jpg"))
        self.photo.setScaledContents(True)
        self.result = self.findChild(QtWidgets.QLabel, 'result')     
        self.fnameEdit = self.findChild(QtWidgets.QLineEdit,'fnameEdit')
        
        self.slidBar_1 = self.findChild(QtWidgets.QSlider, 'sliderBar_1')
        self.slidBar_1.valueChanged[int].connect(self.changeValue)

        self.slide1view = self.findChild(QtWidgets.QLabel, 'slide1view')
        self.value = 50
        self.fnameEdit.clear()
        self.show()


    def changeValue(self,value):
        self.slide1view.setText('red : ' + str(value))
        self.value = value
        self.procRunClicked()



    def processingImage(self, grayImage, rgbImage):
        output = rgbImage.copy()
        ret, th = cv2.threshold(output,127,255,cv2.THRESH_BINARY)
        try:
            circles = cv2.HoughCircles(grayImage, cv2.HOUGH_GRADIENT, 1, self.value,param1=50,param2=30,minRadius=60, maxRadius=100)
            for i in circles[0]:
                cv2.circle(output,(int(i[0]),int(i[1])),int(i[2]),(0,255,0),2)
        except Exception:
            print(Exception.e)

        return output

    def displayOutputImage(self, outImage, mode):
        img_info = outImage.shape
        if outImage.ndim == 2 :
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], img_info[1]*1, QtGui.QImage.Format_Grayscale8)
        else :
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], img_info[1]*img_info[2], QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        if mode == 0 :
            self.photo.setPixmap(pixmap)
            self.photo.setScaledContents(True)
        else :
            self.result.setPixmap(pixmap)
            self.result.setScaledContents(True)

    #cv2.imread가 한글 지원하지 않으므로 새로운 방식으로 파일 조합
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8): 
        try: 
            n = np.fromfile(filename, dtype) 
            img = cv2.imdecode(n, flags) 
            return img 
        except Exception as e: 
            print(e) 
            return None


    def procRunClicked(self):
        # src = self.imread(self.filename) #cv2.imread가 한글경로를 지원하지 않음
        imgRGB = cv2.cvtColor(self.src, cv2.COLOR_BGR2RGB)
        imgGRAY = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        outImg = self.processingImage(imgGRAY,imgRGB)        
        self.displayOutputImage(outImg,1)
        

    def loadBtnClicked(self):
        path = 'images'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일로드", path, filter)
        filename = str(fname[0])
        self.fnameEdit.setText(filename)
        self.src = self.imread(filename) #cv2.imread가 한글경로를 지원하지 않음
        img_rgb = cv2.cvtColor(self.src,cv2.COLOR_BGR2RGB)
        self.displayOutputImage(self.src,0)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()