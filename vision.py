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
        self.photo.setPixmap(QtGui.QPixmap("visionImage/21 L90_OK.bmp"))
        self.photo.setScaledContents(True)
        self.result = self.findChild(QtWidgets.QLabel, 'result')     
        self.fnameEdit = self.findChild(QtWidgets.QLineEdit,'fnameEdit')
        
        # self.slidBar_1 = self.findChild(QtWidgets.QSlider, 'sliderBar_1')
        # self.slidBar_1.valueChanged[int].connect(self.changeValue)

        # self.slide1view = self.findChild(QtWidgets.QLabel, 'slide1view')
        self.value = 50
        self.fnameEdit.clear()
        self.show()


    # def changeValue(self,value):
    #     self.slide1view.setText('red : ' + str(value))
    #     self.value = value
    #     self.procRunClicked()



    def processingImage(self, grayImage, rgbImage):
        output = rgbImage.copy()
        ret, binary = cv2.threshold(output, 150,255,cv2.THRESH_BINARY)
        
 
        try:
            src = cv2.pyrDown(output)
            src_copy = src.copy()
            gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(gray, 150,255,cv2.THRESH_BINARY)
            kernel = np.ones((7,7), np.uint8)

            # 중앙 ====================
            img_middle = binary[380:500,205:1100]
            img_middle = cv2.morphologyEx(img_middle, cv2.MORPH_CLOSE, kernel)
            contours_c, hierarchy = cv2.findContours(img_middle, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

            mu = [None]*len(contours_c)
            for i in range(len(contours_c)):
                mu[i] = cv2.moments(contours_c[i])#중심점

            mc = [None]*len(contours_c)

            img_copy0 = src.copy()
            img_copy0 = img_copy0[380:500,205:1100]

            for i in range(len(contours_c)) :
                mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))

            center_i = 0

            for i in range(len(contours_c)) :
                c_area = cv2.contourArea(contours_c[i])
                okcolor = (0, 255, 0)
                ngcolor = (0, 0, 255)

                cv2.drawContours(img_copy0, contours_c, i, okcolor, 2)
                cv2.circle(img_copy0, (int(mc[i][0]), int(mc[i][1])), 4, okcolor, -1)
                cv2.putText(img_copy0,"{} : {}".format(i,c_area) ,tuple(contours_c[i][0][0]),
                    cv2.FONT_HERSHEY_COMPLEX,0.4, (0,255,0),1)
                
                if c_area > 3385 :
                    cv2.drawContours(img_copy0, contours_c, i, okcolor, 2)
                    cv2.circle(img_copy0, (int(mc[i][0]), int(mc[i][1])), 4, okcolor, -1)
                    cv2.putText(img_copy0,"{} : {}".format(i,c_area) ,tuple(contours_c[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,255,0),1)
                    
                else:#NG일경우
                    cv2.drawContours(img_copy0, contours_c, i, ngcolor, 2)
                    cv2.circle(img_copy0, (int(mc[i][0]), int(mc[i][1])), 4, ngcolor, -1)
                    cv2.putText(img_copy0,"{} : {}".format(i,c_area) ,tuple(contours_c[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,0,255),1)        
                    center_i += 1





            #왼쪽 ====================
            ret_1, binary_1 = cv2.threshold(gray, 150,255,cv2.THRESH_BINARY)
            kernel_1 = np.ones((7,7), np.uint8)

            img_left = binary_1[220:470, 35:200]#y1:y2, x1:x2
            img_left = cv2.morphologyEx(img_left, cv2.MORPH_CLOSE, kernel_1)
            contours_1, hierarchy_1 = cv2.findContours(img_left, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

            mu = [None]*len(contours_1)
            for i in range(len(contours_1)):
                mu[i] = cv2.moments(contours_1[i])#중심점

            mc = [None]*len(contours_1)

            img_copy1 = src.copy()
            img_copy1 = img_copy1[220:470, 35:200]

            for i in range(len(contours_1)) :
                mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))
            left_i = 0
            for i in range(len(contours_1)) :
                # print(i, ":", cv2.contourArea(contours_1[i]))
                c_area = cv2.contourArea(contours_1[i])
                okcolor = (0, 255, 0)
                ngcolor = (0, 0, 255)

                if c_area > 4000.0 :
                    cv2.drawContours(img_copy1, contours_1, i, okcolor, 2)
                    cv2.circle(img_copy1, (int(mc[i][0]), int(mc[i][1])), 4, okcolor, -1)
                    cv2.putText(img_copy1,"{} : {}".format(i,c_area) ,tuple(contours_1[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,255,0),1)
                    
                elif c_area < 1050.0 and c_area > 850.0 :
                    cv2.drawContours(img_copy1, contours_1, i, okcolor, 2)
                    cv2.circle(img_copy1, (int(mc[i][0]), int(mc[i][1])), 4, okcolor, -1)
                    cv2.putText(img_copy1,"{} : {}".format(i,c_area) ,tuple(contours_1[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,255,0),1)

                else:#NG일경우
                    cv2.drawContours(img_copy1, contours_1, i, ngcolor, 2)
                    cv2.circle(img_copy1, (int(mc[i][0]), int(mc[i][1])), 4, ngcolor, -1)
                    cv2.putText(img_copy1,"{} : {}".format(i,c_area) ,tuple(contours_1[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,0,255),1)
                    left_i += 1




            #오른쪽 ====================
            ret_2, binary_2 = cv2.threshold(gray, 150,255,cv2.THRESH_BINARY)
            kernel_2 = np.ones((7,7), np.uint8)

            img_right = binary_2[220:470, 1100:1270]#y1:y2, x1:x2
            img_right = cv2.morphologyEx(img_right, cv2.MORPH_CLOSE, kernel_2)
            contours_2, hierarchy_2 = cv2.findContours(img_right, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

            mu = [None]*len(contours_2)
            for i in range(len(contours_2)):
                mu[i] = cv2.moments(contours_2[i])#중심점

            mc = [None]*len(contours_2)

            img_copy2 = src.copy()
            img_copy2 = img_copy2[220:470, 1100:1270]

            for i in range(len(contours_2)) :
                mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))

            right_i = 0 
            for i in range(len(contours_2)) :

                # print(i, ":", cv2.contourArea(contours_2[i]))
                c_area = cv2.contourArea(contours_2[i])
                okcolor = (0, 255, 0)
                ngcolor = (0, 0, 255)

                if c_area > 3700.0 :
                    cv2.drawContours(img_copy2, contours_2, i, okcolor, 2)
                    cv2.circle(img_copy2, (int(mc[i][0]), int(mc[i][1])), 4, okcolor, -1)
                    cv2.putText(img_copy2,"{} : {}".format(i,c_area) ,tuple(contours_1[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,255,0),1)
                    
                elif c_area < 1100.0 and c_area > 840.0 :
                    cv2.drawContours(img_copy2, contours_2, i, okcolor, 2)
                    cv2.circle(img_copy2, (int(mc[i][0]), int(mc[i][1])), 4, okcolor, -1)
                    cv2.putText(img_copy2,"{} : {}".format(i,c_area) ,tuple(contours_1[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,255,0),1)

                else:#NG일경우
                    cv2.drawContours(img_copy2, contours_2, i, ngcolor, 2)
                    cv2.circle(img_copy2, (int(mc[i][0]), int(mc[i][1])), 4, ngcolor, -1)
                    cv2.putText(img_copy2,"{} : {}".format(i,c_area) ,tuple(contours_1[i][0][0]),
                        cv2.FONT_HERSHEY_COMPLEX,0.4, (0,0,255),1)
                    right_i += 1

            src_copy[220:470, 35:200] = img_copy1
            src_copy[380:500,205:1100] = img_copy0
            src_copy[220:470, 1100:1270] = img_copy2

            result = left_i + center_i + right_i

            if result == 0:
                cv2.putText(src_copy,"OK",(500,632), cv2.FONT_HERSHEY_COMPLEX,3, (0,255,0),1)
            else:
                cv2.putText(src_copy,"NG",(500,632), cv2.FONT_HERSHEY_COMPLEX,3, (0,0,255),1)
                
            cv2.rectangle(src_copy,(28,183) ,(200,491) ,(0,255,0),2)
            cv2.rectangle(src_copy,(210,396) ,(1105,500) ,(0,255,0),2)
            cv2.rectangle(src_copy,(1135,183) ,(1270,491) ,(0,255,0),2)

        except Exception:
            print(Exception.e)

        return src_copy

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
        path = 'visionImage'
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