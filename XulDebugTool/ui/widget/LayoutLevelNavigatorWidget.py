#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Create : 2026/3/11
 @Author: ZekeWong
布局层级导航组件

显示当前选中节点的完整路径，支持点击跳转

示例: Page > HomePage > Container > Button[OK]
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy


class LayoutLevelNavigatorWidget(QWidget):
    """布局层级导航组件，显示当前选中节点的完整路径，支持点击跳转"""

    # 节点点击信号，参数为节点ID
    nodeClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(LayoutLevelNavigatorWidget, self).__init__(parent)
        self.pathItems = []  # [(node_name, display_name, node_id, node_type), ...]
        self._container = None
        self.initUI()

    def initUI(self):
        """初始化UI布局"""
        # 内部容器布局 - 减少上下边距
        innerLayout = QHBoxLayout()
        innerLayout.setAlignment(Qt.AlignLeft)
        innerLayout.setContentsMargins(5, 2, 5, 2)  # 上下边距从 5 改为 2
        innerLayout.setSpacing(2)

        self._container = QWidget()
        self._container.setLayout(innerLayout)
        # 容器设置调试背景
        # self._container.setStyleSheet("background-color: #ff00ff;")

        # 主布局，使用弹性空间
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self._container)
        mainLayout.addStretch()

        # 设置整体样式
        self.setStyleSheet("""
            PathNavagatorWidget {
                background-color: #f5f5f5;
                border-bottom: 1px solid #ddd;
            }
        """)

    def updatePath(self, pathItems):
        """
        更新布局层级导航路径

        :param pathItems: 路径节点列表 [(node_name, display_name, node_id, node_type), ...]
                         - node_name: 按钮显示的节点名称
                         - display_name: 悬浮提示名称（优先级 xulId > type > 节点名称）
                         - node_id: 节点ID
                         - node_type: 节点类型
        """
        self.pathItems = pathItems
        self._refreshUI()

    def clearPath(self):
        """清空布局层级导航"""
        self.pathItems = []
        self._refreshUI()

    def _refreshUI(self):
        """刷新UI显示"""
        layout = self._container.layout()
        # 清空现有内容
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.pathItems:
            return

        # 重建布局层级导航
        for i, (node_name, display_name, node_id, node_type) in enumerate(self.pathItems):
            # 添加分隔符（除第一个）
            if i > 0:
                separator = QLabel(">")
                separator.setStyleSheet("color: #000; font-weight: bold; padding: 0px; background: transparent;")
                layout.addWidget(separator)

            # 最后一个节点：当前节点，不可点击
            if i == len(self.pathItems) - 1:
                label = QLabel(display_name)
                font = QFont()
                font.setPointSize(12)
                font.setBold(True)
                label.setFont(font)
                label.setStyleSheet("padding: 0px; font-weight: bold; color: #000; background: transparent;")
                layout.addWidget(label)
            else:
                # 中间节点：可点击，显示节点名称，悬浮显示display_name
                button = QPushButton(node_name)
                # 使用 QFont 对象设置字体，确保 DPI 缩放行为一致
                font = QFont()
                font.setPointSize(12)
                button.setFont(font)
                # 设置尺寸策略：水平方向固定，不允许扩展
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                button.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                        color: #0066cc;
                        padding: 0px 3px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #e6f2ff;
                        text-decoration: underline;
                    }
                """)
                button.setCursor(QCursor(Qt.PointingHandCursor))
                # 设置 tooltip 显示display_name（优先级 xulId > type > 节点名称）
                button.setToolTip(display_name)
                button.clicked.connect(lambda checked, nid=node_id: self.nodeClicked.emit(nid))
                layout.addWidget(button)
