import sys
import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.VersionInfo import VersionInfo


class AboutWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.scale = Utils.calculateDpiScale()
        super().initWindow()
        self.setupUi()
        self.show()

    def setupUi(self):
        # 创建中心容器和主布局
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(int(20 * self.scale), int(20 * self.scale),
                                            int(20 * self.scale), int(20 * self.scale))
        self.mainLayout.setSpacing(int(10 * self.scale))
        self.centralWidget.setLayout(self.mainLayout)

        # 按顺序从上往下添加组件
        self.initWindowTitle()
        self.initAboutTitle()
        self.initProduction()
        self.initGitAddress()
        self.initCompanyAddress()
        self.initVersionNumber()
        self.initBuildInfo()  # 新增：编译信息

        # 添加底部的弹性空间，将内容向上对齐
        self.mainLayout.addStretch(1)

    def initVersionNumber(self):
        # 版本号标签
        self.versionNumber = QtWidgets.QLabel()
        self.versionNumber.setObjectName("label_4")
        self.versionNumber.setText(f"版本号：{VersionInfo.get_version_full()}")
        self.versionNumber.setAlignment(Qt.AlignCenter)  # 文字居中

        # 字体设置
        font = self.versionNumber.font()
        font.setPointSize(int(10 * self.scale))
        self.versionNumber.setFont(font)

        # 添加到布局，固定高度
        self.versionNumber.setFixedHeight(int(30 * self.scale))
        self.mainLayout.addWidget(self.versionNumber)

    def initBuildInfo(self):
        # 编译信息标签
        self.buildInfo = QtWidgets.QLabel()
        self.buildInfo.setObjectName("label_5")

        # 从版本管理模块读取编译时间
        self.buildInfo.setText(f"编译时间：{VersionInfo.get_display_build_time()}")
        self.buildInfo.setAlignment(Qt.AlignCenter)

        # 字体设置（稍小一些，灰色）
        font = self.buildInfo.font()
        font.setPointSize(int(8 * self.scale))
        self.buildInfo.setFont(font)

        # 添加到布局，固定高度
        self.buildInfo.setFixedHeight(int(25 * self.scale))
        self.mainLayout.addWidget(self.buildInfo)

    def initCompanyAddress(self):
        # 公司链接按钮
        self.company = QtWidgets.QPushButton()
        self.company.setCursor(Qt.PointingHandCursor)
        self.company.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: blue;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.company.setObjectName("pushButton")
        self.company.clicked.connect(self.openCompanyUrl)
        self.company.setText("www.starcor.com")

        # 字体设置
        font = self.company.font()
        font.setPointSize(int(10 * self.scale))
        self.company.setFont(font)

        # 添加到布局，固定高度
        self.company.setFixedHeight(int(30 * self.scale))
        self.mainLayout.addWidget(self.company)

    def initGitAddress(self):
        # GitHub 链接按钮
        self.gitAddress = QtWidgets.QPushButton()
        self.gitAddress.setCursor(Qt.PointingHandCursor)
        self.gitAddress.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: blue;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.gitAddress.setObjectName("label_3")
        self.gitAddress.clicked.connect(self.openGitUrl)
        self.gitAddress.setText("Github/XulDebugTool")

        # 字体设置
        font = self.gitAddress.font()
        font.setPointSize(int(10 * self.scale))
        self.gitAddress.setFont(font)

        # 添加到布局，固定高度
        self.gitAddress.setFixedHeight(int(30 * self.scale))
        self.mainLayout.addWidget(self.gitAddress)

    def initProduction(self):
        # 版权信息标签
        self.production = QLabel()
        self.production.setWordWrap(True)
        self.production.setText("Copyright (c) 2026\n北京视达科科技有限责任公司")
        self.production.setAlignment(Qt.AlignCenter)

        # 字体设置
        font = self.production.font()
        font.setPointSize(int(9 * self.scale))
        self.production.setFont(font)

        # 添加到布局，固定高度
        self.production.setFixedHeight(int(50 * self.scale))
        self.mainLayout.addWidget(self.production)

    def initAboutTitle(self):
        # 标题标签容器
        titleContainer = QWidget()
        titleContainer.setFixedHeight(int(100 * self.scale))
        titleLayout = QVBoxLayout()
        titleLayout.setContentsMargins(0, 0, 0, 0)
        titleContainer.setLayout(titleLayout)

        self.aboutTitle = QtWidgets.QLabel()
        self.aboutTitle.setStyleSheet("QLabel{background: black; color: white; padding: 10px;}")
        self.aboutTitle.setAlignment(Qt.AlignCenter)

        # 字体设置
        font = QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.aboutTitle.setFont(font)
        self.aboutTitle.setObjectName("label_2")
        self.aboutTitle.setText("XulDebugTool")

        titleLayout.addWidget(self.aboutTitle)
        self.mainLayout.addWidget(titleContainer)

    def initWindowTitle(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 根据 DPI 缩放调整窗口大小
        baseWidth, baseHeight = 500, 320
        windowWidth = int(baseWidth * self.scale)
        windowHeight = int(baseHeight * self.scale)
        # 设置最大窗口大小限制
        windowWidth = min(windowWidth, 600)
        windowHeight = min(windowHeight, 500)

        self.setFixedSize(windowWidth, windowHeight)
        self.setStyleSheet("QMainWindow{border-color: black; background: white;}")
        self.setWindowTitle("关于")

    def openCompanyUrl(self):
        webbrowser.open("https://www.starcor.com/ch/index.html")

    def openGitUrl(self):
        webbrowser.open("https://github.com/starcor-company/XulDebugTool")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    aboutWindow = AboutWindow()
    aboutWindow.show()
    sys.exit(app.exec_())
