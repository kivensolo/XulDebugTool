#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

应用入口

author: Kenshin
last edited: 2017.10.14
"""

import sys

from PyQt5.QtWidgets import QApplication

from XulDebugTool.ui.ConnectWindow import ConnectWindow


class App(object):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    # 设置高 DPI 缩放
    QApplication.setAttribute(1, True)  # AA_EnableHighDpiScaling
    # QApplication.setAttribute(0, True)  # AA_UseHighDpiPixmaps
    app = QApplication(sys.argv)
    try:
        ex = ConnectWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
