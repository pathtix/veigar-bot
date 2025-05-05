MAIN_STYLE = """
QMainWindow {
    background-color: #0e0a18;
    color: #ffffff;
    background-image: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #0e0a18, stop:1 #16123a);
}

QWidget {
    color: #ffffff;
    font-size: 12px;
}

#searchFrame {
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 8px;
    margin-bottom: 20px;
    padding: 8px;
}

QLineEdit {
    padding: 8px;
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 4px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid #9061c2;
    background-color: #231a38;
}

QComboBox {
    padding: 8px;
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 4px;
    color: #ffffff;
    min-width: 6em;
    font-size: 13px;
}

QComboBox:hover {
    border: 1px solid #9061c2;
    background-color: #231a38;
}

QComboBox::drop-down {
    border: none;
    width: 0px;
    background-color: transparent;
}

QComboBox:on {
    border: 1px solid #9061c2;
}

QComboBox QAbstractItemView {
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    selection-background-color: #9061c2;
    selection-color: #ffffff;
    outline: none;
}

QPushButton {
    padding: 8px 16px;
    background-color: #9061c2;
    border: none;
    border-radius: 4px;
    color: #ffffff;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #b07fde;
}

QPushButton:pressed {
    background-color: #7a4ca5;
}

QLabel {
    color: #ffffff;
}

QStatusBar {
    background-color: #1a1429;
    color: #ffffff;
    padding: 4px;
}

#profileWidget {
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
    background-image: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1a1429, stop:1 #231a38);
}

#iconContainer {
    background: transparent;
    margin: 0;
    padding: 4px;
    position: relative;
}

#profileIcon {
    background-color: transparent;
    border: 4px solid #9061c2;
    border-radius: 50%;
    min-width: 92px;
    min-height: 92px;
    max-width: 92px;
    max-height: 92px;
    padding: 0;
    margin: 4px;
}

#playerHeader {
    margin-bottom: 8px;
}

#levelLabel {
    color: #ffffff;
    font-size: 14px;
    font-weight: bold;
    background-color: #9061c2;
    border: 2px solid #b07fde;
    border-radius: 10px;
    padding: 2px 8px;
    margin-top: 5px;
    position: relative;
    z-index: 2;
}

#rankTitle {
    color: #b07fde;
    font-weight: bold;
    font-size: 14px;
}

#rankStats {
    color: #a0a0a0;
    font-size: 13px;
}

#rankSeparator {
    background-color: #3d2f63;
    width: 1px;
    margin: 0 10px;
}

#matchHistoryWidget {
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
    background-image: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1a1429, stop:1 #231a38);
}

#matchHistoryHeader {
    background-color: transparent;
    padding: 0 0 12px 0;
    margin-bottom: 12px;
}

#matchHistoryTitle {
    font-size: 20px;
    font-weight: bold;
    color: #b07fde;
    padding-bottom: 0;
    margin-bottom: 5px;
}

#countLabel {
    color: #a0a0a0;
    font-size: 13px;
    margin-right: 4px;
}

#matchCount {
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 4px;
    color: #ffffff;
    padding: 4px 8px;
    margin-right: 8px;
    font-size: 13px;
}

#matchCount::up-button, #matchCount::down-button {
    width: 16px;
    background-color: #231a38;
    border: none;
}

#matchCount::up-button:hover, #matchCount::down-button:hover {
    background-color: #9061c2;
}

#matchWidget {
    background-color: #231a38;
    border: 1px solid #3d2f63;
    border-radius: 6px;
    padding: 12px;
    margin: 4px 0;
}

#matchWidget:hover {
    background-color: #2c2046;
    border-color: #9061c2;
}

#matchResult {
    font-weight: bold;
    font-size: 13px;
    color: #9061c2;
}

#matchResult[victory="true"] {
    color: #44b244;
}

#matchResult[victory="false"] {
    color: #e65c52;
}

#championIcon {
    background-color: #0e0a18;
    border: 1px solid #3d2f63;
    border-radius: 6px;
    padding: 2px;
    min-width: 50px;
    min-height: 50px;
}

#itemIcon {
    background-color: #0e0a18;
    border: 1px solid #3d2f63;
    border-radius: 4px;
    padding: 1px;
    margin: 0 1px;
    min-width: 30px;
    min-height: 30px;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

QScrollArea#matchScroll {
    margin: 8px 0;
    min-height: 150px;
    border: none;
}

QScrollArea#matchScroll > QWidget {
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background-color: #1a1429;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #3d2f63;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9061c2;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QProgressBar {
    border: none;
    background-color: #1a1429;
    border-radius: 2px;
    height: 6px;
    text-align: center;
    margin: 0;
}

QProgressBar::chunk {
    background-color: #9061c2;
    border-radius: 2px;
}

#loadMoreButton {
    background-color: #9061c2;
    border-radius: 4px;
    padding: 8px 16px;
    color: #ffffff;
    font-weight: bold;
    min-width: 180px;
    margin: 10px 0;
}

#loadMoreButton:hover {
    background-color: #b07fde;
}

#loadMoreButton:pressed {
    background-color: #7a4ca5;
}

#filtersContainer {
    margin-left: 20px;
}

/* Settings styles */
QToolBar {
    background-color: #1a1429;
    border: none;
    border-bottom: 1px solid #3d2f63;
    padding: 0;
    spacing: 5px;
}

QToolBar QToolButton {
    background-color: transparent;
    border: none;
    padding: 6px 12px;
    color: #ffffff;
    font-size: 13px;
    margin: 2px 5px;
}

QToolBar QToolButton:hover {
    background-color: #231a38;
}

QToolBar QToolButton:pressed {
    background-color: #3d2f63;
}

#settingsFrame {
    background-color: #1a1429;
    border: 1px solid #3d2f63;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

QDialog {
    background-color: #0e0a18;
    color: #ffffff;
    background-image: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #0e0a18, stop:1 #16123a);
}

QFormLayout {
    spacing: 12px;
}

QCheckBox {
    color: #ffffff;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #3d2f63;
    border-radius: 3px;
    background-color: #1a1429;
}

QCheckBox::indicator:checked {
    background-color: #9061c2;
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiI+PHBhdGggZmlsbD0iI2ZmZmZmZiIgZD0iTTYuNzUgMTAuMDk2bDQuOTIzLTQuOTIzYy4xOTgtLjE5OC41Mi0uMTk4LjcxOCAwbC43MDYuNzA3Yy4xOTgtLjE5OC4xOTguNTE5IDAgLjcxOGwtNi4wNDggNi4wNDhjLS4xOTcuMTk4LS41MTkuMTk4LS43MTcgMEwzLjU4IDguODkzYy0uMTk4LS4xOTgtLjE5OC0uNTIwIDAtLjcxN2wuNzA3LS43MDdjLjE5OC0uMTk4LjUyLS4xOTguNzE4IDBsMS43NDMgMS43NDN6Ii8+PC9zdmc+);
}

QCheckBox::indicator:hover {
    border-color: #9061c2;
}

QDialogButtonBox QPushButton {
    min-width: 70px;
}

QDialogButtonBox QPushButton[text="Reset"] {
    background-color: #3d2f63;
}

QDialogButtonBox QPushButton[text="Reset"]:hover {
    background-color: #5a4694;
}
""" 