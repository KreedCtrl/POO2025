import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QToolBar,
                             QAction, QTabWidget, QVBoxLayout, QWidget, QListWidget, QInputDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser POO")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.history = []
        self.favorites = []

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_bar)

        favorit_btn = QPushButton("★")
        favorit_btn.clicked.connect(self.add_to_favorites)
        self.toolbar.addWidget(favorit_btn)

        back_btn = QPushButton("⮜")
        back_btn.clicked.connect(self.go_back)
        self.toolbar.addWidget(back_btn)

        forward_btn = QPushButton("⮞")
        forward_btn.clicked.connect(self.go_forward)
        self.toolbar.addWidget(forward_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_page)
        self.toolbar.addWidget(refresh_btn)

        stop_btn = QPushButton("⛔ Stop")
        stop_btn.clicked.connect(self.stop_loading)
        self.toolbar.addWidget(stop_btn)

        self.search_engines = {
            "Google": "https://www.google.com/search?q=",
            "Bing": "https://www.bing.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Yahoo": "https://search.yahoo.com/search?p=",
            "Wikipedia": "https://en.wikipedia.org/w/index.php?search="
        }
        self.current_engine = "Google"

        menu = self.menuBar()
        engine_menu = menu.addMenu("Motor de căutare")
        for name in self.search_engines:
            action = QAction(name, self)
            action.triggered.connect(lambda _, n=name: self.set_search_engine(n))
            engine_menu.addAction(action)

        menu.addAction("Lista de ★", self.show_favorites)
        menu.addAction("Istoric", self.show_history)
        menu.addAction("Nou Tab", self.add_new_tab)

        self.add_new_tab()

    def add_new_tab(self, url="https://www.google.com"):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(lambda qurl, b=browser: self.update_urlbar(qurl, b))
        index = self.tabs.addTab(browser, "Nou")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def load_url(self):
        text = self.url_bar.text()
        if not text.startswith("http"):
            search_url = self.search_engines[self.current_engine] + text.replace(" ", "+")
            url = QUrl(search_url)
        else:
            url = QUrl(text)

        browser = self.tabs.currentWidget()
        if isinstance(browser, QWebEngineView):
            browser.setUrl(url)
            self.history.append(url.toString())

    def update_urlbar(self, q, browser=None):
        # Actualizează bara de adrese când se schimbă pagina
        if self.tabs.currentWidget() == browser:
            self.url_bar.setText(q.toString())
            self.tabs.setTabText(self.tabs.currentIndex(), browser.page().title())

    def go_back(self):
        # Navigare înapoi
        browser = self.tabs.currentWidget()
        if browser: browser.back()

    def go_forward(self):
        # Navigare înainte
        browser = self.tabs.currentWidget()
        if browser: browser.forward()

    def refresh_page(self):
        # Reîncarcă pagina
        browser = self.tabs.currentWidget()
        if browser: browser.reload()

    def stop_loading(self):
        # Oprește încărcarea
        browser = self.tabs.currentWidget()
        if browser: browser.stop()

    def set_search_engine(self, name):
        # Setează motorul de căutare curent
        self.current_engine = name
        self.statusBar().showMessage(f"Motor setat: {name}")

    def add_to_favorites(self):
        # Adaugă pagina curentă la favorite
        browser = self.tabs.currentWidget()
        if browser:
            url = browser.url().toString()
            self.favorites.append(url)
            self.statusBar().showMessage("Adăugat la favorite")

    def show_favorites(self):
        # Afișează lista de favorite
        self.show_list_window("Favorite", self.favorites)

    def show_history(self):
        # Afișează istoricul de navigare
        self.show_list_window("Istoric", self.history)

    def show_list_window(self, title, items):
        # Fereastră cu listă de linkuri (favorite/istoric)
        win = QWidget()
        win.setWindowTitle(title)
        layout = QVBoxLayout()
        list_widget = QListWidget()
        list_widget.addItems(items)
        list_widget.itemDoubleClicked.connect(lambda item: self.load_from_list(item.text(), win))
        layout.addWidget(list_widget)
        win.setLayout(layout)
        win.resize(400, 300)
        win.show()

    def load_from_list(self, url, window):
        # Încarcă pagina selectată din listă
        self.url_bar.setText(url)
        self.load_url()
        window.close()

# Lansare aplicație
if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())