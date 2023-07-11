from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
import requests
import re
regex = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validUrl(input):
    return re.match(regex, input) is not None

class WebView(QWebView):
    def __init__(self, parent=None):
        super(WebView, self).__init__(parent)
        settings = self.settings()
        settings.setAttribute(QWebSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebSettings.PluginsEnabled, True)

class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
 
        nameLabel = QLabel("URL")
        self.nameLine = QLineEdit()
        self.backButton = QPushButton(" <- ")
        self.newTabButton = QPushButton(" + ")
        self.rmTabButton = QPushButton(" - ")
        self.tabWidget = QTabWidget()
        self.zoomInButton = QPushButton("Zoom In")
        self.zoomOutButton = QPushButton("Zoom Out")

        self.lWebView = []

        Layout1 = QHBoxLayout()
        Layout1.addWidget(self.backButton)
        Layout1.addWidget(nameLabel)
        Layout1.addWidget(self.nameLine)
        Layout1.addWidget(self.rmTabButton)
        Layout1.addWidget(self.newTabButton)
        Layout1.addWidget(self.zoomInButton)
        Layout1.addWidget(self.zoomOutButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(Layout1)
        mainLayout.addWidget(self.tabWidget)
        self.addTab()

        self.nameLine.returnPressed.connect(self.requestUrl)
        self.backButton.clicked.connect(self.goBack)
        self.newTabButton.clicked.connect(self.addTab)
        self.rmTabButton.clicked.connect(self.rmTab)
        self.tabWidget.currentChanged.connect(self.changeTab)
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomOutButton.clicked.connect(self.zoomOut)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Browser")

    def addTab(self):
        webView = WebView()
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

    def changeTab(self):
        self.nameLine.setText(self.lWebView[self.tabWidget.currentIndex()].url().url())

    def requestUrl(self):
        if self.tabWidget.currentIndex() != -1:
            url_text = self.nameLine.text()
            if not url_text.startswith('http://') and not url_text.startswith('https://'):
                url_text = 'http://' + url_text
            url = QUrl(url_text)
            if validUrl(url_text):
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

    def zoomIn(self):
        self.lWebView[self.tabWidget.currentIndex()].setZoomFactor(self.lWebView[self.tabWidget.currentIndex()].zoomFactor() + 0.1)

    def zoomOut(self):
        self.lWebView[self.tabWidget.currentIndex()].setZoomFactor(self.lWebView[self.tabWidget.currentIndex()].zoomFactor() - 0.1)

if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Main()
    screen.show()
 
sys.exit(app.exec_())
