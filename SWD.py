from http.client import FORBIDDEN
from multiprocessing.resource_sharer import stop
import os
import threading
from PyQt5 import QtCore, QtGui, QtWidgets,QtNetwork
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineSettings, QWebEngineView
from time import sleep
from datetime import timezone
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtCore import QUrl, Qt, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QWidget
import calendar
from datetime import date
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
import requests
from bs4 import BeautifulSoup
import csv
import plot

isfile = os.getcwd() + '\\tmpPlots\\'
TEC_fil_dir = os.getcwd() + '\\TECfile\\'
if os.path.isdir(isfile):
    for f in os.listdir(isfile):
        os.remove(os.path.join(isfile, f))

else:
    os.mkdir(isfile)
if os.path.isdir(TEC_fil_dir):
    for ft in os.listdir(TEC_fil_dir):
        os.remove(os.path.join(TEC_fil_dir, ft))
else:
    os.mkdir(TEC_fil_dir)

stopping = False


popups = []


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWebEngineView()
        lay = QVBoxLayout(self)
        lay.addWidget(self.view)
        self.resize(640, 480)


class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        w = Widget()
        w.show()
        popups.append(w)
        return w.view.page()


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
        #pixmap3 = pixmap.scaled(720, 500,QtCore.Qt.KeepAspectRatio)
        self._label.setPixmap(pixmap)
        self._label.setScaledContents(True)
        QtCore.QTimer.singleShot(100, self.request)
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        #Form.showMaximized()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        # self.label.setObjectName("label")
        # self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        print(self.label_2.devicePixelRatioFScale())
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.canvas, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.label_5.setScaledContents(True)
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        
        url = "    "
        url1 = 'https://services.swpc.noaa.gov/images/swx-overview-small.gif'
        url2 = "https://services.swpc.noaa.gov/images/ace-mag-swepam-3-day.gif?time=1648530126000"
        url3 = 'https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png'
        self.url_kyoto = "https://wdc.kugi.kyoto-u.ac.jp/dst_realtime/presentmonth/"


        self.loader = Loader()
        self.loader1 = Loader()
        self.loader2 = Loader()
        self.loader3 = Loader()

        self.loader.start(url,self.label)
        self.loader1.start(url1,self.label_2)
        self.loader2.start(url2, self.label_3)
        self.loader3.start(url3,self.label_4)
        self.y = threading.Thread(target=self.kyoto_download)
        self.y.start()

        self.x = threading.Thread(target=self.window1)
        self.x.start()

        self.anifunc()
        self.retranslateUi(Form)
        

        self.z = threading.Thread(target=plot.Ionex_plot)
        self.z.start()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SPACE WEATHER MONITORING AND FORCASTING"))
        # self.label.setText(_translate("Form", "TextLabel"))
        # self.label_2.setText(_translate("Form", "TextLabel"))
        # self.label_6.setText(_translate("Form", "TextLabel"))
        # self.label_4.setText(_translate("Form", "TextLabel"))
        # self.label_5.setText(_translate("Form", "TextLabel"))
        # self.label_3.setText(_translate("Form", "TextLabel"))


    def window1(self):
        global stopping
        while True:
            print("thread ionex lable")
            dateChange = str(datetime.date.today())
            currentTime = datetime.datetime.now(timezone.utc).hour
            if currentTime >= 0 and currentTime < 10:
                currentTime = f"0{currentTime}"
            image1 = f'tmpPlots/{dateChange} {currentTime}.png'
            self.pixmap = QtGui.QPixmap(image1)
            #self.pixmap2 = self.pixmap.scaled(629, 495, QtCore.Qt.KeepAspectRatio)
            self.label_5.setPixmap(self.pixmap)
            sleep(1)
            if stopping:
                break


    def graph_plotter(self,i):
        series =pd.read_csv('kyotob.csv', engine='python',skiprows=6,skipfooter=4, delim_whitespace=True )

        series = series.astype(float)
        series =  series[series<999]
        series = series [series>-999]


        ax = plt.axes()
        length = len(series.index)*len(series.columns)
        data=np.asarray(series).reshape(1,length)

        plt.plot(np.linspace(1, length, length), data[0,:])
        plt.ylim(-200,50)
        plt.xlim(1,725)
        plt.title('Dst Index (Real-time)')
        plt.xlabel('Days')
        plt.ylabel('Dst(nT)')
        plt.text(350,-230,s="Source: WDC for Geomagnetism, Kyoto",fontsize=9)
        plt.text(5,55,f"{calendar.month_name[date.today().month]} {datetime.date.today().year}",weight='bold',fontsize=11.5)
        plt.grid(color='k', linestyle='--', linewidth=0.25)
        ax.set_xticks(np.arange(1,  length, 24))
        ax.set_xticklabels((np.arange(1,  length, 24)/24).astype(int),fontsize=6)

    def anifunc(self):
        self.ani = FuncAnimation(self.fig,self.graph_plotter,interval=10000)

    
    def kyoto_download(self):
        global stopping
        while True:
            print("thread kyoto")
            if stopping:
                break
            try:
                response  = requests.get(self.url_kyoto)
                soup = BeautifulSoup(response.content, "html.parser")
                jan_datas = soup.find_all("pre",class_= "data")

                for jan in jan_datas:
                    pass
                with open('kyotob.csv', 'w', encoding='UTF8') as f:
                # create the csv writer
                    writer = csv.writer(f)

                    # write a row to the csv file
                    writer.writerow(jan)
                
            except:
                print("check the connection")
            
            sleep(2)
    
class MainWindow(QtWidgets.QWidget,Ui_Form):
    def __init__(self) -> None:
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        print(self.label.size())
        self.showMaximized()
        central_widget = QWidget()
        self.webview = QWebEngineView()
        self.page = WebEnginePage()
        self.webview.setPage(self.page)
        """self.webview.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True
        )
        """

        self.webview.load(
            QUrl("https://www.youtube.com/embed/wQGR81PxBxM")
        )
        lay = QVBoxLayout(central_widget)
        lay.addWidget(self.webview)
        self.gridLayout.addWidget(self.webview, 0, 0, 1, 1)

        

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        print(self.label.size())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        global stopping
        stopping = True
        plot.stop_thread()
        fig_file_dir = os.getcwd() + '\\tmpPlots\\'
        TEC_fil_dir = os.getcwd() + '\\TECfile\\'
        if os.path.isdir(fig_file_dir):
            for file in os.listdir(fig_file_dir):
                os.remove(os.path.join(fig_file_dir, file))
            for file_TEC in os.listdir(TEC_fil_dir):
                os.remove(os.path.join(TEC_fil_dir, file_TEC))


def win():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    win()