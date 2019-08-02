import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTextEdit, QAction, QApplication, QLabel, QHBoxLayout, QMenuBar, \
    QFileDialog
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from sqlalchemy import Column, ForeignKey, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.dialects.sqlite
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DBImage(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    Data = Column(BLOB)


def sql_save(img):
    engine = create_engine('sqlite:///image.db')
    engine.echo = True

    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()
    images = DBImage(Data=img)
    s.add(images)
    s.commit()


class img:
    def __init__(self, imageFile):
        self.pict = Image.open(imageFile)
        self.pict = self.pict.convert("RGBA")

    def orig(self):
        return self.pict

    def bytes(self):
        return self.pict.tobytes()

    def gray(self):
        new_pic = self.pict
        draw = ImageDraw.Draw(new_pic)
        width = new_pic.size[0]
        height = new_pic.size[1]
        pix = new_pic.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c)
                draw.point((i, j), (S, S, S))

        return new_pic

    def sepia(self):
        new_pic = self.pict
        draw = ImageDraw.Draw(new_pic)
        width = new_pic.size[0]
        height = new_pic.size[1]
        pix = new_pic.load()

        depth = 30
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c)
                a = S + depth * 2
                b = S + depth
                c = S
                if (a > 255): a = 255
                if (b > 255): b = 255
                if (c > 255): c = 255
                draw.point((i, j), (a, b, c))

        return new_pic

    def negate(self):
        new_pic = self.pict
        draw = ImageDraw.Draw(new_pic)
        width = new_pic.size[0]
        height = new_pic.size[1]
        pix = new_pic.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), (255 - a, 255 - b, 255 - c))

        return new_pic

    def resize(self, width, height):
        self.pict = self.pict.resize((width, height), Image.BILINEAR)
        return self.pict

    def crop(self, width, height):
        self.pict = self.pict.crop((0, 0, width, height))
        return self.pict


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pic = ''

    def openDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", ".", "Image Files (*.png *.jpg *.bmp)")[0]
        self.pic = img(fname)
        img_tmp = ImageQt(self.pic.resize(300, 300))
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.resize(300, 300)
        self.lbl.setPixmap(pixmap)

    def crop_action(self):
        img_tmp = ImageQt(self.pic.crop(150, 150))
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.resize(150, 150)
        self.lbl.setPixmap(pixmap)

    def resize_action(self):
        img_tmp = ImageQt(self.pic.resize(600, 600))
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.resize(600, 600)
        self.lbl.setPixmap(pixmap)

    def gray_action(self):
        img_tmp = ImageQt(self.pic.gray())
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.resize(300, 300)
        self.lbl.setPixmap(pixmap)

    def sepia_action(self):
        img_tmp = ImageQt(self.pic.sepia())
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.resize(300, 300)
        self.lbl.setPixmap(pixmap)

    def negate_action(self):
        img_tmp = ImageQt(self.pic.negate())
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.resize(300, 300)
        self.lbl.setPixmap(pixmap)

    def save_db_action(self):
        sql_save(self.pic.bytes())

    def initUI(self):
        self.lbl = QLabel(self)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть файл')
        openFile.triggered.connect(self.openDialog)

        save_to_db = QAction('Save to DB', self)
        save_to_db.triggered.connect(self.save_db_action)

        gray_a = QAction("Gray scale", self)
        gray_a.triggered.connect(self.gray_action)

        sepia_a = QAction("Sepia", self)
        sepia_a.triggered.connect(self.sepia_action)

        negate_a = QAction("Negative", self)
        negate_a.triggered.connect(self.negate_action)

        crop_a = QAction("Crop", self)
        crop_a.triggered.connect(self.crop_action)

        resize_a = QAction("Resize", self)
        resize_a.triggered.connect(self.resize_action)

        menubar = QMenuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(save_to_db)

        imgMenu = menubar.addMenu("Image")
        imgMenu.addAction(gray_a)
        imgMenu.addAction(sepia_a)
        imgMenu.addAction(negate_a)
        imgMenu.addAction(crop_a)
        imgMenu.addAction(resize_a)

        hbox = QHBoxLayout(self)
        hbox.addChildWidget(menubar)
        self.setLayout(hbox)
        self.move(300, 300)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Main form")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainForm()
    sys.exit(app.exec_())
