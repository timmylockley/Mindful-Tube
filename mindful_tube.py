import sys
import os
import subprocess
import threading
import platform
import yt_dlp
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QCheckBox
)

class SearchableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        self.filter_model = QSortFilterProxyModel(self)
        self.filter_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.filter_model.setFilterKeyColumn(0)

        self.original_model = QStandardItemModel(self)
        self.filter_model.setSourceModel(self.original_model)
        self.setModel(self.filter_model)

        self.lineEdit().textEdited.connect(self.filter_model.setFilterFixedString)

    def addItem(self, text, userData=None):
        item = QStandardItem(text)
        if userData is not None:
            item.setData(userData, Qt.ItemDataRole.UserRole)
        self.original_model.appendRow(item)

    def clear(self):
        self.original_model.clear()
        self.lineEdit().clear()

    def currentData(self, role=Qt.ItemDataRole.UserRole):
        proxy_index = self.currentIndex()
        source_index = self.filter_model.mapToSource(self.filter_model.index(proxy_index, 0))
        return self.original_model.data(source_index, role)

class MindfulTubeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MindfulTube")
        self.resize(850, 600)

        self.added_channels = []
        self.download_dir = os.path.join(os.path.expanduser("~"), "MindfulTube_Downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.init_watch_tab()
        self.init_settings_tab()
        self.init_instructions_tab()

    def init_instructions_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Welcome to MindfulTube</h2>"))
        layout.addWidget(QLabel("<i>Designed for intentional viewing, free of algorithmic feeds.</i>"))
        layout.addSpacing(10)
        layout.addWidget(QLabel("1. Add your approved channels in the Settings tab."))
        layout.addWidget(QLabel("2. Choose a channel, select category (videos, shorts, or live), and load content."))
        layout.addWidget(QLabel("3. Select a video, choose whether to keep it after watching, and launch!"))
        layout.addStretch()  # Corrected typo from addStratch to addStretch
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Instructions")

    def init_watch_tab(self):
        self.watch_tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Your Curated Feed</b>"))
        layout.addWidget(QLabel("Select a channel:"))

        self.watch_dropdown = QComboBox()
        self.watch_dropdown.setEditable(True)
        self.watch_dropdown.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        layout.addWidget(self.watch_dropdown)

        layout.addWidget(QLabel("Select Content Category:"))
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["videos", "shorts", "live"])
        layout.addWidget(self.category_dropdown)

        self.load_feed_btn = QPushButton("Load Channel Content")
        self.load_feed_btn.clicked.connect(self.load_channel_videos)
        layout.addWidget(self.load_feed_btn)

        layout.addWidget(QLabel("Search & Select Video/Short/Live to Watch:"))
        self.video_dropdown = SearchableComboBox()
        layout.addWidget(self.video_dropdown)

        self.delete_checkbox = QCheckBox("Delete video file off device after watching")
        self.delete_checkbox.setChecked(True)
        layout.addWidget(self.delete_checkbox)

        self.play_btn = QPushButton("Download & Watch")
        self.play_btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 10px;")
        self.play_btn.clicked.connect(self.download_and_play)
        layout.addWidget(self.play_btn)

        layout.addStretch()
        self.watch_tab.setLayout(layout)
        self.tabs.addTab(self.watch_tab, "Watch")

    def init_settings_tab(self):
        self.settings_tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Manage Whitelisted Channels</b>"))

        input_layout = QHBoxLayout()
        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("Paste YouTube Channel URL (e.g., https://www.youtube.com/@Name)")
        input_layout.addWidget(self.channel_input)

        add_btn = QPushButton("Add Channel")
        add_btn.clicked.connect(self.add_channel)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        self.settings_dropdown = QComboBox()
        layout.addWidget(self.settings_dropdown)

        layout.addStretch()
        self.settings_tab.setLayout(layout)
        self.tabs.addTab(self.settings_tab, "Settings")

    def add_channel(self):
        url = self.channel_input.text().strip()
        if url and url not in self.added_channels:
            self.added_channels.append(url)
            self.watch_dropdown.addItem(url)
            self.settings_dropdown.addItem(url)
            self.channel_input.clear()
            QMessageBox.information(self, "Success", "Channel added to your curated list!")

    def load_channel_videos(self):
        channel_url = self.watch_dropdown.currentText().strip()
        if not channel_url:
            QMessageBox.warning(self, "Error", "Please select a channel first.")
            return

        category = self.category_dropdown.currentText().strip()
        base_url = channel_url.rstrip("/")
        sub_path = "streams" if category == "live" else category
        target_url = f"{base_url}/{sub_path}"

        self.video_dropdown.clear()
        self.video_dropdown.addItem("Fetching content... please wait...")
        QApplication.processEvents()

        try:
            ydl_opts = {
                'extract_flat': True,
                'playlistend': 50,
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=False)
                entries = info.get('entries', [])

                self.video_dropdown.clear()
                for entry in entries:
                    title = entry.get('title', 'Unknown Title')
                    vid_id = entry.get('id', '')

                    if vid_id:
                        watch_url = f"https://www.youtube.com/watch?v={vid_id}"
                        self.video_dropdown.addItem(title, watch_url)

                if self.video_dropdown.count() == 0:
                    self.video_dropdown.addItem("No content found in this category.")
        except Exception as e:
            self.video_dropdown.clear()
            self.video_dropdown.addItem("Error fetching content.")
            QMessageBox.critical(self, "Extraction Error", str(e))

    def download_and_play(self):
        video_url = self.video_dropdown.currentData()
        if not video_url:
            QMessageBox.warning(self, "Selection Error", "Please select a valid item from the list first.")
            return

        self.play_btn.setEnabled(False)
        self.play_btn.setText("Downloading... Please wait...")
        QApplication.processEvents()

        threading.Thread(target=self._process_download, args=(video_url,), daemon=True).start()

    def _process_download(self, video_url):
        file_path = None
        try:
            ydl_opts = {
                'format': 'best[height<=720]/best',
                'outtmpl': os.path.join(self.download_dir, '%(id)s.%(ext)s'),
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                file_path = ydl.prepare_filename(info)

            if file_path and os.path.exists(file_path):
                current_sys = platform.system().lower()

                if "android" in sys.platform.lower() or os.path.exists("/system/bin/app_process"):
                    subprocess.run(["termux-open", file_path])
                elif "linux" in current_sys:
                    subprocess.run(["xdg-open", file_path])
                elif "darwin" in current_sys:
                    subprocess.run(["open", file_path])
                else:
                    os.startfile(file_path)

        except Exception as e:
            QMessageBox.critical(None, "Download Error", f"Could not download video: {e}")
        finally:
            self.play_btn.setEnabled(True)
            self.play_btn.setText("Download & Watch")

            if file_path and os.path.exists(file_path) and self.delete_checkbox.isChecked():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setText("Did you finish watching?")
                msg.setInformativeText("Delete the downloaded video file from your device now?")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                ret = msg.exec()
                if ret == QMessageBox.StandardButton.Yes:
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MindfulTubeApp()
    window.show()
    sys.exit(app.exec())
