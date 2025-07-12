#create the Easy Editor photo editor here!
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Dialogue for opening files (and folders)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image

from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Sigma Editor')
main_win.resize(700, 900)

lb_image = QLabel('Image')
btn_dir = QPushButton('Folder')
lw_files = QListWidget()
btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
btn_mirror = QPushButton('Mirror')
btn_sharp = QPushButton('Sharpness')
btn_bw = QPushButton('B&W')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)

col2.addWidget(lb_image)
row_button = QHBoxLayout()
row_button.addWidget(btn_left)
row_button.addWidget(btn_right)
row_button.addWidget(btn_mirror)
row_button.addWidget(btn_sharp)
row_button.addWidget(btn_bw)
col2.addLayout(row_button)

row.addLayout(col1)
row.addLayout(col2)
main_win.setLayout(row)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(file, extentions):
    result = []
    for filename in file:
        for ext in extentions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenameList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenameList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, dir, filename):
        '''when loading, remember to breath'''
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        global lb_image
        lb_image.hide()
        pixmapsimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapsimage =  pixmapsimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapsimage)
        lb_image.show()

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)   
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)

main_win.show()
app.exec()
    