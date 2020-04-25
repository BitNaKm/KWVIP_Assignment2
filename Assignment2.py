import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray

basic_ui = uic.loadUiType("PyQt_assignment.ui")[0]  # Qt Designer에서 저장한 .ui 파일 로드


class WindowClass(QMainWindow, basic_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda: self.load())  # load 버튼을 클릭한 경우
        self.pushButton_2.clicked.connect(lambda: self.vertical_flip())  # flip 버튼을 클릭한 경우

    def load(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", ".")

        if fileName:
            image = QImage(fileName)

            if image.isNull():  # if file does not exist
                QMessageBox.information(self, "Image Viewer", "Cannot load $s." % fileName)  # print error message
                return

            # QImage to QPixmap
            qPixmapVar = QPixmap.fromImage(image)
            qPixmapVar = qPixmapVar.scaled(256, 256)  # size 설정

            self.label.setPixmap(qPixmapVar)  # label에 이미지 출력

            self.show()

    def vertical_flip(self):
        qPixmapVar = self.label.pixmap()  # load한 qPixmap을 불러옴
        if qPixmapVar is None:  # load하지 않고 flip을 먼저 누른 경우 error message 출력
            print("Please load image first.")
            return

        # QPixmap to QImage
        image = qPixmapVar.toImage();

        # QImage to Numpy
        image_array = qimage2ndarray.rgb_view(image)

        height, width, _ = image_array.shape  # 세로, 가로 저장
        flip_image_array = image_array.copy()  # 배열의 shape 맞추기 위해 복사

        # 상하 반전
        for row in range(height):
            for col in range(width):
                flip_image_array[row][col] = image_array[height - 1 - row][col];

        # Numpy to QImage
        flip_image = qimage2ndarray.array2qimage(flip_image_array, normalize=False)

        # QImage to QPixmap
        flip_qPixmapVar = QPixmap.fromImage(flip_image)
        self.label.setPixmap(flip_qPixmapVar)  # label에 상하반전된 이미지 출력

        self.show()

        # qPixmap을 상하 반전
        # flip_qPixmapVar = qPixmapVar.transformed(QTransform().scale(1,-1));
        # self.label.setPixmap(flip_qPixmapVar)
        # self.show()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()