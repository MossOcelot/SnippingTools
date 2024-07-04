import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import pyautogui
from PIL import ImageGrab, Image

import cv2
import numpy as np
import os

class SnippingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.type_machine = "normal"

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Snipping Tool')

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 580, 300)
        self.label.setPixmap(QPixmap(''))

        self.capture_btn = QPushButton('Capture', self)
        self.capture_btn.setGeometry(10, 320, 100, 30)
        self.capture_btn.clicked.connect(self.capture_screen)

        self.save_btn = QPushButton('Save', self)
        self.save_btn.setGeometry(120, 320, 100, 30)
        self.save_btn.clicked.connect(self.save_image)

        self.comboBox = QComboBox()
        self.comboBox.setGeometry(220, 320, 100, 30)
        self.comboBox.addItems(['normal', 'unbalance', 'bearing defect', 'misalignment', 'looseness', 'Blower'])
        self.comboBox.currentTextChanged.connect(self.text_changed)
        self.comboBox.setParent(self)

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        print("Type_machine:", self.type_machine)
        croppedImage = croppedFunction(screenshot)
        croppedImage = Image.fromarray(croppedImage)
        croppedImage = self.convert_pil_to_qimage(croppedImage)
        pixmap = QPixmap.fromImage(croppedImage.scaled(580, 300))
        self.label.setPixmap(pixmap)

    def save_image(self):
        pixmap = self.label.pixmap()
        if pixmap:
            count = len(os.listdir('./datasets'))
            pixmap.save(f'./datasets/picture{count + 1}.jpg', quality=100)  # บันทึกภาพที่แสดงบน Label เป็นไฟล์ PNG
            
            with open(f'./datasets/picture{count + 1}.txt', 'w') as file:
                file.write(f"{self.type_machine}")

            print('Image saved as saved_image.png')

    def convert_pil_to_qimage(self, pil_image):
        image = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QImage(image, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
        return qimage

    def text_changed(self, s):
        
        self.type_machine = s

        print("Text changed:", s)
    
def croppedimage(image, top_left, bottom_right):
    top_x, top_y = top_left
    bottom_x, bottom_y = bottom_right

    return image[top_y:bottom_y, top_x:bottom_x]

def croppedFunction(image):
    imaged = np.array(image)
    # imaged = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    top_left = (285, 101)
    bottom_right = (1856, 1012)

    return croppedimage(imaged, top_left, bottom_right)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SnippingTool()
    window.show()
    sys.exit(app.exec_())
