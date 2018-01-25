from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
import requests

class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
 
        nameLabel = QLabel("URL")
        self.nameLine = QLineEdit()
        self.backButton = QPushButton(" <- ")
        self.newTabButton = QPushButton(" + ")
        self.rmTabButton = QPushButton(" - ")
        self.tabWidget = QTabWidget()

        self.lWebView = []

        Layout1 = QHBoxLayout()
        Layout1.addWidget(self.backButton)
        Layout1.addWidget(nameLabel)
        Layout1.addWidget(self.nameLine)
        Layout1.addWidget(self.rmTabButton)
        Layout1.addWidget(self.newTabButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(Layout1)
        mainLayout.addWidget(self.tabWidget)
        self.addTab()

        self.nameLine.returnPressed.connect(self.requestUrl)
        self.backButton.clicked.connect(self.goBack)
        self.newTabButton.clicked.connect(self.addTab)
        self.rmTabButton.clicked.connect(self.rmTab)
        self.tabWidget.currentChanged.connect(self.changeTab)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Browser")

    def addTab(self):
        webView = QWebView()
        webView.loadProgress.connect(self.loading)
        webView.loadFinished.connect(self.changePage)
        self.tabWidget.addTab(webView, "New Tab")
        self.lWebView.append(webView)
        self.tabWidget.setCurrentWidget(webView)

    def rmTab(self):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
            try:
                self.lWebView.remove(self.lWebView[self.tabWidget.currentIndex()])
            except IndexError:
                return False
            #self.lWebView.remove(self.tabWidget.currentIndex())

    def changeTab(self):
        self.nameLine.setText(self.lWebView[self.tabWidget.currentIndex()].url().url())

    def requestUrl(self):
        if self.tabWidget.currentIndex() != -1:
            url_text = self.nameLine.text()
            if not url_text.startswith('http://') and not url_text.startswith('https://'):
                url_text = 'http://' + url_text
            url = QUrl(url_text)
            try:
                response = requests.get(url_text).status_code
            except Exception:
                response = 600
            if response < 400:
                self.lWebView[self.tabWidget.currentIndex()].load(url)
            else:
                self.lWebView[self.tabWidget.currentIndex()].load(QUrl("https://www.google.com/search?q=" + self.nameLine.text()))

    def loading(self):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sender()), "Loading")

    def changePage(self):
        if len(self.sender().title()) > 15:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.sender()), self.sender().title()[:15] + "...")
        else:
             self.tabWidget.setTabText(self.tabWidget.indexOf(self.sender()), self.sender().title())
        self.nameLine.setText(self.sender().url().url())

    def goBack(self):
        try:
            self.lWebView[self.tabWidget.currentIndex()].back()
        except IndexError:
            return False

if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Main()
    screen.show()
 
sys.exit(app.exec_())
