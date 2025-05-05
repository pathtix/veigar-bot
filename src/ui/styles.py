MAIN_STYLE = """
QMainWindow {
    background-color: #1a1a1a;
    color: #ffffff;
}

QWidget {
    color: #ffffff;
    font-size: 12px;
}

#searchFrame {
    background-color: #2d2d2d;
    border-radius: 8px;
    margin-bottom: 20px;
    padding: 5px;
}

QLineEdit {
    padding: 8px;
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid #4a90e2;
    background-color: #323232;
}

QComboBox {
    padding: 8px;
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #ffffff;
    min-width: 6em;
    font-size: 13px;
}

QComboBox:hover {
    border: 1px solid #4a90e2;
    background-color: #323232;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 8px;
}

QComboBox:on {
    border: 1px solid #4a90e2;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    selection-background-color: #4a90e2;
    selection-color: #ffffff;
    outline: none;
}

QPushButton {
    padding: 8px 16px;
    background-color: #4a90e2;
    border: none;
    border-radius: 4px;
    color: #ffffff;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #357abd;
}

QPushButton:pressed {
    background-color: #2d6da3;
}

QLabel {
    color: #ffffff;
}

QStatusBar {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 4px;
}

#profileWidget, #matchHistoryWidget {
    background-color: #2a2a2a;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

#profileIcon {
    background-color: #1a1a1a;
    border-radius: 50%;
    padding: 4px;
}

#playerHeader {
    margin-bottom: 12px;
}

#rankInfo {
    font-size: 14px;
}

#rankTitle {
    color: #4a90e2;
    font-weight: bold;
    margin-top: 4px;
}

#matchHistoryTitle {
    font-size: 16px;
    font-weight: bold;
    color: #4a90e2;
    padding-bottom: 8px;
}

#matchWidget {
    background-color: #232323;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 12px;
    margin: 4px 8px;
}

#matchWidget:hover {
    background-color: #282828;
    border-color: #3d3d3d;
}

#matchResult {
    font-weight: bold;
    font-size: 13px;
    color: #4a90e2;
}

#matchResult[victory="true"] {
    color: #44b244;
}

#matchResult[victory="false"] {
    color: #e24a4a;
}

#championIcon {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 2px;
    min-width: 50px;
    min-height: 50px;
}

#itemIcon {
    background-color: #1a1a1a;
    border: 1px solid #333333;
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
}

QScrollBar:vertical {
    border: none;
    background-color: #2a2a2a;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #4a4a4a;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5a5a5a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QProgressBar {
    border: none;
    background-color: #232323;
    border-radius: 2px;
    height: 4px;
    text-align: center;
    margin: 0 10px;
}

QProgressBar::chunk {
    background-color: #4a90e2;
    border-radius: 2px;
}
""" 