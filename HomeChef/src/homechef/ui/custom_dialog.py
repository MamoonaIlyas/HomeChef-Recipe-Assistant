# src/homechef/ui/custom_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt, QPoint, QSize  # <<< QSize IS NOW IMPORTED HERE
from PySide6.QtGui import QPixmap
import pathlib

# This should point to your main 'HomeChef' folder
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent

class CustomDialog(QDialog):
    def __init__(self, title, message, icon_type='info', parent=None):
        super().__init__(parent)

        # Make the dialog frameless and with a translucent background
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True) # Block interaction with the main window

        # Main widget that will hold the content and have the styled background
        self.background_widget = QWidget(self)
        self.background_widget.setObjectName("custom_dialog_widget")
        
        # Main layout
        main_layout = QVBoxLayout(self.background_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setObjectName("custom_dialog_icon")
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        icon_map = {
            'success': 'check-circle.svg',
            'info': 'info.svg',
            'warning': 'alert-triangle.svg'
        }
        icon_path = PROJECT_ROOT / "icons" / icon_map.get(icon_type, 'info.svg')
        if icon_path.exists():
            icon_pixmap = QPixmap(str(icon_path))
            self.icon_label.setPixmap(icon_pixmap.scaled(QSize(48, 48), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Title
        self.title_label = QLabel(title)
        self.title_label.setObjectName("custom_dialog_title")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Message
        self.message_label = QLabel(message)
        self.message_label.setObjectName("custom_dialog_message")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)

        # OK Button
        self.ok_button = QPushButton("OK")
        self.ok_button.setObjectName("custom_dialog_button")
        self.ok_button.clicked.connect(self.accept) # Closes the dialog
        
        # Button layout to control button size
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addStretch()

        # Add widgets to layout
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.message_label)
        main_layout.addLayout(button_layout)
        
        # Set the main widget as the dialog's layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.background_widget)

        # Logic for dragging the frameless window
        self._drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()