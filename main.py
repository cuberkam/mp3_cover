from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QProgressBar,
)
from PyQt5.QtGui import QIcon
import sys
import os


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP3Cover")
        self.setMinimumSize(800, 500)

        # Set icon
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)

            QApplication.setWindowIcon(app_icon)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # MP3 File Selection
        mp3_layout = QVBoxLayout()
        mp3_top_layout = QHBoxLayout()

        mp3_title = QLabel("Selected MP3 Files:")
        mp3_title.setStyleSheet("font-weight: bold; color: #333;")
        mp3_top_layout.addWidget(mp3_title)

        mp3_button = QPushButton("Select MP3 Files")
        mp3_button.clicked.connect(self.select_mp3_file)
        mp3_button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        mp3_top_layout.addWidget(mp3_button)

        mp3_layout.addLayout(mp3_top_layout)

        # MP3 List View
        self.mp3_list = QListWidget()
        self.mp3_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: #fff;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
        """)
        mp3_layout.addWidget(self.mp3_list)

        main_layout.addLayout(mp3_layout)

        # Image File Selection
        image_layout = QHBoxLayout()
        self.image_label = QLabel("No image file selected")
        self.image_label.setStyleSheet(
            "padding: 5px; background-color: #f0f0f0; border-radius: 3px;"
        )
        image_button = QPushButton("Select Cover Image")
        image_button.clicked.connect(self.select_cover_file)
        image_button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(image_button)
        main_layout.addLayout(image_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Process Button
        self.process_button = QPushButton("Add Cover Image to Selected Files")
        self.process_button.clicked.connect(self.add_cover)
        self.process_button.setEnabled(False)
        self.process_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        main_layout.addWidget(self.process_button)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("padding: 10px; color: #666;")
        main_layout.addWidget(self.status_label)

        # Variables to store file paths
        self.mp3_paths = []
        self.image_path = None

    def select_mp3_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select MP3 Files", "", "MP3 Files (*.mp3)"
        )
        if files:
            self.mp3_paths = files
            self.mp3_list.clear()
            for file in files:
                self.mp3_list.addItem(os.path.basename(file))
            self.button_control()

    def select_cover_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select Image File", "", "Image Files (*.jpg *.jpeg *.png)"
        )
        if file:
            self.image_path = file
            self.image_label.setText(os.path.basename(file))
            self.button_control()

    def button_control(self):
        if self.mp3_paths and self.image_path:
            self.process_button.setEnabled(True)
        else:
            self.process_button.setEnabled(False)

    def add_cover(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.mp3_paths))
        self.progress_bar.setValue(0)
        self.process_button.setEnabled(False)

        successful = 0
        failed = 0

        for index, mp3_path in enumerate(self.mp3_paths):
            try:
                audio = MP3(mp3_path, ID3=ID3)

                with open(self.image_path, "rb") as album_cover:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc="Cover",
                            data=album_cover.read(),
                        )
                    )

                audio.save()
                successful += 1

            except Exception as e:
                failed += 1
                print(f"Error ({os.path.basename(mp3_path)}): {str(e)}")

            self.progress_bar.setValue(index + 1)

        # Show final status
        if failed == 0:
            self.status_label.setText(
                f"✅ Cover image successfully added to {successful} files!"
            )
            self.status_label.setStyleSheet("padding: 10px; color: green;")
        else:
            self.status_label.setText(
                f"⚠️ {successful} successful, {failed} failed operations"
            )
            self.status_label.setStyleSheet("padding: 10px; color: #ff9800;")

        self.process_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Window()
    window.show()
    sys.exit(app.exec_())
