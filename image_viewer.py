import sys
import cv2
import numpy as np

from PyQt6 import QtCore, QtGui, QtWidgets

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsView,
    QGraphicsPixmapItem
)

from PyQt6.QtGui import (
    QPixmap,
    QImage,
    QWheelEvent,
    QTransform
)

from PyQt6.QtCore import Qt

class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.graphicsView = GraphicsView()
        self.ui.gridLayout.addWidget(self.graphicsView)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.showImage()
        self.graphicsView.show()

    def cv2QPixmapItem(self, data):
        qimg = QImage(data, data.shape[1], data.shape[0], data.strides[0], QImage.Format.Format_BGR888)
        qpixmapitem = QGraphicsPixmapItemNew(QPixmap(qimg), data)
        return qpixmapitem

    def showImage(self):
        img_name, ____ = QFileDialog.getOpenFileName(
            self,
            'Open Image File',
            '*.jpg;;*.png;;*.jpeg'
        )
        img = cv2.imdecode(np.fromfile(img_name, dtype=np.uint8), -1)
        item = self.cv2QPixmapItem(img)
        #selectable and movable
        item.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.scene.addItem(item)
        self.graphicsView.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)

class QGraphicsPixmapItemNew(QGraphicsPixmapItem):
    def __init__(self,Qpixmap ,img,parent=None):
        super().__init__(Qpixmap,parent=parent)
        self.img=img

    def wheelEvent(self, e: 'QGraphicsSceneWheelEvent'):
        scale = self.ratio
        y = e.pos().y()
        x = e.pos().x()
        if e.delta() > 0:
            self.ratio *= 1.3
        else:
            self.ratio *= 0.7
        self.setScale(self.ratio)
        #translate after scaling
        if e.delta() > 0:
            self.moveBy(-x*scale*0.3, -y*scale*0.3)
        else:
            self.moveBy(x*scale*0.3, y*scale*0.3)
    ratio = 1

    def mousePressEvent(self, e: 'QGraphicsSceneMouseEvent') -> None:
        x=e.pos().x()
        y=e.pos().y()
        print(tuple(reversed(self.img[int(y)][int(x)])))

    def mouseMoveEvent(self, e: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    im = ImageViewer()
    im.show()
    sys.exit(app.exec())
