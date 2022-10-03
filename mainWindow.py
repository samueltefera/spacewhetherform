import sys
from time import sleep, timezone
from PyQt5 import QtCore, QtNetwork, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading
import datetime
from datetime import timezone
currentTime = 0

class Loader(QtCore.QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        manager = QtNetwork.QNetworkAccessManager()
        manager.finished.connect(self.onFinished)
        self._manager = manager
        
    def start(self, url, label):
        self._url = url
        self._label = label
        self.request()

    def request(self):
        manager = self._manager
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(self._url))
        res = manager.get(req)
    
    def onFinished(self, reply):
        data = reply.readAll()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        self._label.setPixmap(pixmap)
        self._label.setScaledContents(True)
        QtCore.QTimer.singleShot(100, self.request)
def trackTime():
    global currentTime
    while True:
        t = datetime.datetime.now(timezone.utc).hour
        if currentTime != t:
            currentTime = t
        sleep(1) # Stop maxing out CPU

#threadTime = threading.Thread(target=trackTime)
#threadTime.start()

# def window():
app = QApplication(sys.argv)

w = QWidget()
grid = QGridLayout()

lbl1 = QLabel()
lbl1.setStyleSheet("border: 1px solid black")
lbl2 = QLabel()
lbl2.setStyleSheet("border: 1px solid black")

lbl3 = QLabel()
lbl3.setStyleSheet("border: 1px solid black")

lbl4 = QLabel()
lbl4.setStyleSheet("border: 1px solid black")

lbl5 = QLabel()
lbl5.setStyleSheet("border: 1px solid black")

lbl6 = QLabel()
lbl6.setStyleSheet("border: 1px solid black")

def window1():
    
    while True:
        dateChange = str(datetime.date.today())
        currentTime = datetime.datetime.now(timezone.utc).hour
        if currentTime >= 0 and currentTime < 10:
            currentTime = f"0{currentTime}"
        image1 = f'tmpPlots/{dateChange} {currentTime}.png'
        pixmap = QPixmap(image1)
        lbl5.setPixmap(pixmap)
        sleep(1)
        
x = threading.Thread(target=window1)
x.start()
grid.addWidget(lbl1, 0, 0)
grid.addWidget(lbl2, 0, 1)
grid.addWidget(lbl3, 0, 2)
grid.addWidget(lbl4, 1, 0)
grid.addWidget(lbl5, 1, 1)
grid.addWidget(lbl6, 1, 2)
w.setLayout(grid)
w.setGeometry(300, 300, 420, 200)
w.setWindowTitle('SSARD Space Weather Display')
w.show()


pixmap1 = QPixmap('Picture1.png')

loader = Loader()
loader1 = Loader()
loader2 = Loader()
loader3 = Loader()
url = "https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png"
url1 = 'https://services.swpc.noaa.gov/images/swx-overview-small.gif'
url2 = "https://services.swpc.noaa.gov/images/ace-mag-swepam-3-day.gif?time=1648530126000"
url3 = 'https://services.swpc.noaa.gov/images/animations/sdo-hmii/latest.jpg'
loader.start(url, lbl1)
loader1.start(url1,lbl2)
loader2.start(url2, lbl3)
loader3.start(url3,lbl4)
lbl5.setScaledContents(True)
lbl6.resize(50,50)
sleep(5)
sys.exit(app.exec_())
# if __name__ == '__main__':
#    window()