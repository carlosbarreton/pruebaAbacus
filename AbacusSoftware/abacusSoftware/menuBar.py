import abacusSoftware.__GUI_images__ as __GUI_images__

import pyAbacus as pa
from abacusSoftware.constants import __version__
from PyQt5 import QtCore, QtGui, QtWidgets
from abacusSoftware.__about__ import Ui_Dialog as Ui_Dialog_about

class AboutWindow(QtWidgets.QDialog, Ui_Dialog_about):
    def __init__(self, parent = None):
        super(AboutWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.parent = parent

        image = QtGui.QPixmap(':/splash.png')
        image = image.scaled(220, 220, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(image)

        tausand = '<a href="https://www.tausand.com/"> https://www.tausand.com </a>'
        pages =  '<a href="https://github.com/Tausand-dev/AbacusSoftware"> https://github.com/Tausand-dev/AbacusSoftware </a>'
        message = "That time when I wanted to improve a webpage \n\n by Carlos Barreto \n\n A few years ago, a friend introduced me to veganism. I hadn't heard about this diet/lifestyle before, so I looked more into it. \n I found a website about vegan nutrition that had high quality information backed with scientific studies. \n I thought the page was really great, but it looked kind of outdated. Therefore, I decided to give it a \n fresh look and then try to sell it to the author of the page. So I set out to learn HTML, CSS and \n Javascript, so I could build an interactive, responsive and mobile-friendly website. It took me some \n time, but at the end, I was pretty happy with the result. I made one page that looked way more atractive \n than it used to be and it even had accesibility features. Unfortunately, I didn't contact the owner of the website \n right away because I wanted to build a couple more pages, and after a couple of \n months the website had already been renewed. Anyway, it was a very positive experience not only \n because I really enjoyed learning a little bit about web development, but also because I really liked \n what I built.\n\nAbacus Software is a suite of tools build to ensure your experience with Tausand's coincidence counters becomes simplified. \n\nSoftware Version: %s\nPyAbacus Version: %s\n\n"%(__version__, pa.__version__)
        self.message_label.setText(message)
        self.visit_label = QtWidgets.QLabel()
        self.github_label = QtWidgets.QLabel()
        self.pages_label = QtWidgets.QLabel()

        self.visit_label.setText("Visit us at: %s "%tausand)
        self.github_label.setText("More information on Abacus Software implementation can be found at: %s"%pages)
        self.verticalLayout.addWidget(self.visit_label)
        self.verticalLayout.addWidget(self.github_label)

        self.visit_label.linkActivated.connect(self.open_link)
        self.github_label.linkActivated.connect(self.open_link)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def open_link(self, link):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))
