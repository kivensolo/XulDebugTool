#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/13 17:10
# @Author  : Mrlsm -- starcor
"""
 @Update : 2026/2/26
 @Author: ZekeWong
 目前布局结构如下：
 UpdateProperty(QWidget)
  │
  └── QVBoxLayout (mainLayout)
      └── QSplitter (splitter) - Qt.Vertical 垂直方向，初始比例 60:40
          │
          ├── [0] QTreeWidget (inputWidget) - 上部分 60%
          │   ├── QTreeWidgetItem (inputAttr) - Attr 根节点
          │   │   └── 动态子项（属性键值对）
          │   └── QTreeWidgetItem (inputStyle) - Style 根节点
          │       └── 动态子项（样式键值对）
          │
          └── [1] QWidget (classBoxContainer) - 下部分 40%
              └── QVBoxLayout (buttomExtBoxLayout) - 顶部对齐
                  ├── QWidget (comboBoxContainer) - 固定高度，紧贴顶部
                  │   └── QHBoxLayout (comboBoxRow)
                  │       ├── QComboBox (classActionBox) - stretch=1 (25%)
                  │       └── QComboBox (classValuesBox) - stretch=3 (75%)
                  ├── QListView (listView) - 高度自适应内容
                  └── addStretch() - 占用剩余空间

   视觉效果
   ┌─────────────────────────────────────────┐
   │  ┌───────────────────────────────────┐  │
   │  │  ▲ QTreeWidget 自带滚动条           │  │ ← 可拖动分隔线
   │  │  ├─ Attr                          │  │   调整上下比例
   │  │  │   ├─ x           100           │  │
   │  │  │   ├─ y           200           │  │
   │  │  │   └─ ...         ...           │  │
   │  │  └─ Style                         │  │
   │  │      ├─ font-size   16            │  │
   │  │      └─ ...         ...           │  │
   │  └───────────────────────────────────┘  │
   │  ══════════════════════════════════════ │ ← 可拖动分隔线
   │  ┌───────────────────────────────────┐  │
   │  │ [add-class▼] [class selector▼]    │  │ ← 固定在顶部
   │  │ ┌─────────────────────────────┐   │  │
   │  │ │ event1                      │   │  │
   │  │ │ event2                      │   │  │ ← 高度自适应
   │  │ │ event3                      │   │  │
   │  │ └─────────────────────────────┘   │  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
            ↑                          ↑
     初始 60% (可拖动调整)       初始 40% (可拖动调整)
 """

import json

from PyQt5.QtCore import Qt, QStringListModel, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from XulDebugTool.logcatapi.Logcat import STCLogger
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper
from XulDebugTool.utils.QuickTemplatesLoader import QuickTemplatesLoader

# 数据的整理，需要把数据填充至内显示
ITEM_ATTR = {}
ITEM_STYLE = {}
ITEM_CLASS = []
ITEM_EVENT = []

ITEM_TAG = ['area', 'item', 'layout']
ATTR_AREA = ["x", "y", "height", "width", "align", "max-layers", "enabled", "animation", "animation-speed",
             "animation-type", "animation-duration", "animation-mode", "switching-mode", "animation-sizing",
             "animation-moving", "direction", "loop", "lock-focus", "component", "text", "multi-line", "auto-wrap",
             "marquee", "ellipsis", "indicator", "indicator.style", "indicator.align", "indicator.gap",
             "indicator.left", "indicator.right", "indicator.top", "indicator.bottom", "scrollbar", "auto-scroll",
             "incremental", "arrangement", "minimum-item", "cache-pages", "checked-class", "group"]

STYLE_AREA = ["font-face", "font-size", "font-color", "font-weight", "font-scale-x", "font-shadow",
              "font-align", "font-style-underline", "font-style-strike", "font-style-italic",
              "font-resample", "font-render", "start-indent", "end-indent", "do-not-match-text",
              "background-image", "background-color", "border", "margin", "margin-left", "margin-right",
              "margin-bottom", "margin-top", "padding", "padding-left", "padding-right", "padding-bottom",
              "padding-top", "display", "z-index", "scale", "animation-scale", "position", "border-dash-pattern",
              "fix-half-char", "animation-text-change", "preferred-focus-padding", "hint-text-color", "line-height",
              "clip-children", "clip-focus", "layout-mode", "opacity", "translate", "translate-x", "translate-y",
              "rotate", "quiver", "quiver-mode", "rotate-x", "rotate-y", "rotate-z", "rotate-center", "rotate-center-x",
              "rotate-center-y", "rotate-center-z", "lighting-color-filter", "round-rect", "max-width", "max-height",
              "min-width", "min-height", "preload", "keep-focus-visible"]

item_color = QColor(233, 233, 233)
property_color_one = QColor(255, 255, 255)
property_color_two = QColor(255, 255, 255)
add_color = QColor(255, 255, 255)


class UpdateProperty(QWidget):
    def __init__(self, parent=None):
        super(UpdateProperty, self).__init__(parent)
        self.data = None
        self.viewId = ''
        self.sameFlag = True
        self.viewTag = ''
        self.pageId = ''

        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # 创建垂直分隔器 (QSplitter)
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)  # 禁止子组件折叠到0

        # 设置自身的尺寸策略 - 铺满父容器
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 初始化 inputWidget（QTreeWidget）
        self.inputWidget = QTreeWidget()
        self.inputWidget.setStyleSheet("QTreeWidget::item{height:" + str(Utils.getItemHeight()) + "px}")

        self.inputWidget.setHeaderLabels(['Key', 'Value'])
        # 设置上下文菜单策略
        self.inputWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.inputWidget.customContextMenuRequested.connect(self.openContextMenu)

        self.inputAttr = QTreeWidgetItem()
        self.inputAttr.setText(0, 'Attr')
        self.inputAttr.setBackground(0, item_color)
        self.inputAttr.setBackground(1, item_color)
        self.inputStyle = QTreeWidgetItem()
        self.inputStyle.setText(0, 'Style')
        self.inputStyle.setBackground(0, item_color)
        self.inputStyle.setBackground(1, item_color)
        self.inputWidget.insertTopLevelItem(0, self.inputAttr)
        self.inputWidget.insertTopLevelItem(1, self.inputStyle)
        self.inputAttr.setExpanded(True)
        self.inputWidget.expanded.connect(self.changeExpand)
        self.inputWidget.collapsed.connect(self.changeExpand)
        # 将 inputWidget 添加到分隔器（上部分）
        self.splitter.addWidget(self.inputWidget)

        # ========= 创建底部的 ClassBox 容器 Start============
        self.classBoxContainer = QWidget()
        buttomExtBoxLayout = QVBoxLayout(self.classBoxContainer)
        buttomExtBoxLayout.setContentsMargins(10, 5, 10, 5)
        buttomExtBoxLayout.setSpacing(5)
        # 设置布局对齐方式为顶部对齐
        buttomExtBoxLayout.setAlignment(Qt.AlignTop)

        # ComboBox 行 - 创建一个容器包裹以便统一管理
        comboBoxContainer = QWidget()
        # 设置 comboBoxContainer 的尺寸策略：水平方向可扩展，垂直方向固定
        comboBoxContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        comboBoxRow = QHBoxLayout(comboBoxContainer)
        comboBoxRow.setContentsMargins(0, 0, 0, 0)
        comboBoxRow.setSpacing(10)

        self.classActionBox = QComboBox()
        self.classActionBox.setEditable(False)
        self.classActionBox.setMaxVisibleItems(2)
        self.classActionBox.setInsertPolicy(QComboBox.InsertAtTop)
        self.classActionBox.addItem("add-class")
        self.classActionBox.addItem("remove-class")

        self.classValuesBox = QComboBox()
        self.classValuesBox.setEditable(False)
        # 设置固定高度，不随 splitter 调整而变化
        self.classValuesBox.setFixedHeight(30)
        self.classValuesBox.activated.connect(self.updateClass)

        comboBoxRow.addWidget(self.classActionBox, 1)
        comboBoxRow.addWidget(self.classValuesBox, 3)
        # comboBoxContainer 不拉伸，始终保持在顶部
        buttomExtBoxLayout.addWidget(comboBoxContainer, 0)
        # ========= 创建底部的 ClassBox 容器 End ============

        # 事件列表
        self.listView = QListView()
        self.listView.setStyleSheet("background-color: #FEF9E7;")
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.slm = QStringListModel()
        self.slm.setStringList(ITEM_EVENT)
        self.listView.setModel(self.slm)
        self.listView.clicked.connect(self.itemClickedEvent)
        # listView 高度自适应内容，不拉伸
        self.listView.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        buttomExtBoxLayout.addWidget(self.listView, 0)
        # 添加弹性空间占用剩余区域，确保内容紧贴顶部
        buttomExtBoxLayout.addStretch()

        # 将 classBoxContainer 添加到分隔器（下部分）
        self.splitter.addWidget(self.classBoxContainer)
        # 设置分隔器的初始比例为 6:4
        self.splitter.setStretchFactor(0, 6)
        self.splitter.setStretchFactor(1, 4)

        # 将分隔器添加到主布局
        self.mainLayout.addWidget(self.splitter)
        # 初始化类数据
        ITEM_CLASS.clear()
        self.initAllClassData()

        STCLogger().i('init UpdateProperty')

        # 初始化时检查是否需要滚动
        self._checkScrollNeeded()

    def inputString(self):
        STCLogger().i('input key = ')

    def changeExpand(self):
        # 布局管理器会自动处理，无需手动调整位置
        # 保留此方法以兼容现有信号连接
        pass

    def _checkScrollNeeded(self):
        """更新 listView 的大小（QTreeWidget 由布局管理器自动处理）"""
        # 更新 listView 的高度，让它自适应内容
        eventCount = len(ITEM_EVENT)
        if eventCount > 0:
            # 只设置最小高度，让高度自适应内容
            self.listView.setMinimumHeight(eventCount * 30)
            # 移除最大高度限制，让 listView 完全自适应内容高度
            self.listView.setMaximumHeight(16777215)  # QWIDGETSIZE_MAX
        else:
            self.listView.setMinimumHeight(0)
            self.listView.setMaximumHeight(0)

    def updateAttrUrl(self):
        num = 0
        for key, value in ITEM_ATTR.items():
            attr = self.inputAttr.child(num).text(1)
            if self.inputAttr.child(num).text(0) not in ITEM_ATTR:
                self.inputAttr.child(num).setText(0, list(ITEM_ATTR.keys())[num])
                QMessageBox.critical(self, "提示", self.tr("不能更改key值，请重新添加。"))
                return
            if attr != ITEM_ATTR[self.inputAttr.child(num).text(0)]:
                ITEM_ATTR[key] = attr
                XulDebugServerHelper.updateUrl('set-attr', self.viewId, key, attr)
            num += 1
        self.updateAddProperty('set-attr', num, self.inputAttr)

    def updateStyleUrl(self):
        num2 = 0
        for key, value in ITEM_STYLE.items():
            style = self.inputStyle.child(num2).text(1)
            if self.inputStyle.child(num2).text(0) not in ITEM_STYLE:
                self.inputStyle.child(num2).setText(0, list(ITEM_STYLE.keys())[num2])
                QMessageBox.critical(self, "提示", self.tr("不能更改key值，请重新添加。"))
                return
            if style != ITEM_STYLE[self.inputStyle.child(num2).text(0)]:
                ITEM_STYLE[key] = style
                XulDebugServerHelper.updateUrl('set-style', self.viewId, key, style)
            num2 += 1
        self.updateAddProperty('set-style', num2, self.inputStyle)

    def updateAddProperty(self, type, num, root):
        if root.child(num) is None:
            return
        item = root.child(num)
        if str(item.text(0)) == '' or str(item.text(1)) == '':
            return
        if type == 'set-attr':
            for key, value in ITEM_ATTR.items():
                if (key == str(item.text(0)) or str(item.text(0)) not in ATTR_AREA) and not str(item.text(0)).startswith("img"):
                    if str(item.text(0)) in STYLE_AREA:
                        QMessageBox.critical(self, "提示", self.tr("您输入的为style属性，请在style栏内输入。"))
                    item.setText(0, '')
                    item.setText(1, '')
                    return
            ITEM_ATTR.setdefault(str(item.text(0)), str(item.text(1)))
        elif type == 'set-style':
            for key, value in ITEM_STYLE.items():
                if key == str(item.text(0)) or str(item.text(0)) not in STYLE_AREA:
                    if str(item.text(0)) in ATTR_AREA:
                        QMessageBox.critical(self, "提示", self.tr("您输入的为attr属性，请在attr栏内输入。"))
                    item.setText(0, '')
                    item.setText(1, '')
                    return
            ITEM_STYLE.setdefault(str(item.text(0)), str(item.text(1)))

        result = XulDebugServerHelper.updateUrl(type, self.viewId, item.text(0), item.text(1))
        if result is None or result.status != 200:
            return
        STCLogger().i('updateAddProperty:' + item.text(0) + ',' + item.text(1))
        self.addQTreeWidgetItem(root)
        # 添加项目后检查是否需要滚动
        self._checkScrollNeeded()

    def updateItemUI(self):
        if self.sameFlag:
            return
        for pos1, item1 in enumerate(ITEM_ATTR.items()):
            item = self.getQTreeWidgetItem(pos1, item1[0], item1[1])
            self.inputAttr.addChild(item)
        for pos2, item2 in enumerate(ITEM_STYLE.items()):
            item = self.getQTreeWidgetItem(pos2, item2[0], item2[1])
            self.inputStyle.addChild(item)
        if self.viewTag in ITEM_TAG:
            self.addQTreeWidgetItem(self.inputAttr)
            self.addQTreeWidgetItem(self.inputStyle)

        self.inputWidget.itemChanged.connect(self.updateAttrUrl)
        self.inputWidget.itemChanged.connect(self.updateStyleUrl)
        self.changeExpand()

        # 更新UI后检查是否需要滚动
        self._checkScrollNeeded()

        # 更新事件列表（高度由 _checkScrollNeeded 自动调整）
        self.slm.setStringList(ITEM_EVENT)
        self.listView.setModel(self.slm)

    def itemClickedEvent(self, qModelIndex):
        print("click " + ITEM_EVENT[qModelIndex.row()])
        XulDebugServerHelper.fireItemEvent(ITEM_EVENT[qModelIndex.row()], self.viewId)

    def getQTreeWidgetItem(self, pos, key, value):
        item = QTreeWidgetItem()
        item.setText(0, key)
        item.setText(1, value)
        if pos % 2 == 1:
            item.setBackground(0, property_color_one)
            item.setBackground(1, property_color_one)
        else:
            item.setBackground(0, property_color_two)
            item.setBackground(1, property_color_two)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
        return item

    def addQTreeWidgetItem(self, root):
        addItem = QTreeWidgetItem()
        addItem.setIcon(0, IconTool.buildQIcon('add.png'))
        addItem.setText(0, '')
        addItem.setText(1, '')
        addItem.setBackground(0, add_color)
        addItem.setBackground(1, add_color)
        addItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        root.addChild(addItem)
        self.changeExpand()

    def initData(self, pageId, data):
        dict = json.loads(data)
        action = dict['action']
        if action == "click":
            id = dict['Id']
            xml = dict['xml']
            if id == self.viewId:
                self.sameFlag = True
            else:
                self.sameFlag = False
                ITEM_STYLE.clear()
                ITEM_ATTR.clear()
                self.inputAttr.takeChildren()
                self.inputStyle.takeChildren()
                self.viewId = id
            element = Utils.findNodeById(id, xml)
            self.viewTag = element.tag
            children = element.getchildren()
            ITEM_EVENT.clear()
            for item in children:
                if item.attrib is not None:
                    if item.tag == 'attr':
                        ITEM_ATTR.setdefault(item.attrib['name'], item.text)
                    if item.tag == 'style':
                        ITEM_STYLE.setdefault(item.attrib['name'], item.text)
                    if item.tag == 'action':
                        ITEM_EVENT.append(item.attrib['action'])
        self.initPageClassData(pageId)

    def initAllClassData(self):
        all = XulDebugServerHelper.getAllSelector()
        if all.data:
            selector = Utils.xml2json(all.data, 'selector')
            if selector == '':
                return
            for select in selector['select']:
                if '@class' in select.keys() and select['@class'] not in ITEM_CLASS:
                    ITEM_CLASS.append(select['@class'])

    def initPageClassData(self, pageId):
        if self.pageId == pageId:
            return
        all = XulDebugServerHelper.getPageSelector(pageId)
        if all.data:
            page = Utils.xml2json(all.data, 'page')
            if page == '':
                return
            for item in page:
                if item == 'selector':
                    selector = page['selector']
                    if selector is None or 'select' not in selector.keys():
                        return
                    try:
                        for select in selector['select']:
                            if '@class' in select.keys() and select['@class'] not in ITEM_CLASS:
                                ITEM_CLASS.append(select['@class'])
                    except:
                        print("select exception!")

        for name in ITEM_CLASS:
            self.classValuesBox.addItem(name)

    def updateClass(self):
        XulDebugServerHelper.updateClassUrl(self.classActionBox.currentText(), self.viewId, self.classValuesBox.currentText())

    def openContextMenu(self, point):
        """
        打开上下文菜单，根据点击位置显示不同的快捷选项
        """
        item = self.inputWidget.itemAt(point)
        if item is None:
            return

        # 判断点击的是哪个根节点区域
        root_item = item
        while root_item.parent() is not None:
            root_item = root_item.parent()

        # 检查是否是 Attr 或 Style 根节点或其子节点
        if root_item == self.inputAttr:
            templates = QuickTemplatesLoader.get_attr_templates()
            self._showQuickAddMenu(point, templates, 'set-attr', ITEM_ATTR, self.inputAttr)
        elif root_item == self.inputStyle:
            templates = QuickTemplatesLoader.get_style_templates()
            self._showQuickAddMenu(point, templates, 'set-style', ITEM_STYLE, self.inputStyle)

    def _showQuickAddMenu(self, point, templates, update_type, item_dict, root_item):
        """
        显示快速添加菜单

        :param point: 鼠标点击位置
        :param templates: 属性模板字典 {显示名: (key, value)}
        :param update_type: 更新类型 ('set-attr' 或 'set-style')
        :param item_dict: 当前属性字典 (ITEM_ATTR 或 ITEM_STYLE)
        :param root_item: 根节点 (inputAttr 或 inputStyle)
        """
        menu = QMenu(self)

        # 添加菜单标题
        title_action = menu.addAction("【快捷添加】")
        title_action.setEnabled(False)

        # 添加分隔线
        menu.addSeparator()

        # 添加模板选项
        for display_name, (key, value) in templates.items():
            action = menu.addAction(display_name)
            action.setData((key, value))

        # 添加分隔线
        menu.addSeparator()

        # 添加自定义选项
        custom_action = menu.addAction("自定义添加...")
        custom_action.setData(('custom', ''))

        # 显示菜单并获取用户选择
        action = menu.exec_(self.inputWidget.mapToGlobal(point))

        if action is not None:
            data = action.data()
            if data and data[0] == 'custom':
                # 自定义添加：定位到添加行
                self._focusOnAddRow(root_item)
            else:
                # 快速添加预设属性
                key, value = data
                self._addProperty(update_type, key, value, item_dict, root_item)

    def _focusOnAddRow(self, root_item):
        """
        定位到添加行并开始编辑
        """
        child_count = root_item.childCount()
        if child_count > 0:
            add_item = root_item.child(child_count - 1)
            self.inputWidget.setCurrentItem(add_item, 0)
            self.inputWidget.editItem(add_item, 0)

    def _addProperty(self, update_type, key, value, item_dict, root_item):
        """
        添加属性到列表并更新到服务器

        :param update_type: 更新类型 ('set-attr' 或 'set-style')
        :param key: 属性键
        :param value: 属性值
        :param item_dict: 当前属性字典 (ITEM_ATTR 或 ITEM_STYLE)
        :param root_item: 根节点 (inputAttr 或 inputStyle)
        """
        # 检查属性是否已存在
        if key in item_dict:
            reply = QMessageBox.question(
                self,
                "属性已存在",
                f"属性 '{key}' 已存在，是否覆盖现有值？\n当前值: {item_dict[key]}\n新值: {value}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        # 更新本地数据
        item_dict[key] = value

        # 发送到服务器
        result = XulDebugServerHelper.updateUrl(update_type, self.viewId, key, value)
        if result is None or result.status != 200:
            QMessageBox.warning(self, "警告", f"添加属性 '{key}' 失败")
            return

        STCLogger().i(f'快速添加属性: {key}={value}')

        # 刷新UI显示
        self._refreshPropertyUI(root_item, item_dict)

    def _refreshPropertyUI(self, root_item, item_dict):
        """
        刷新属性列表UI显示

        :param root_item: 根节点 (inputAttr 或 inputStyle)
        :param item_dict: 当前属性字典 (ITEM_ATTR 或 ITEM_STYLE)
        """
        # 临时断开信号连接，避免刷新时触发更新
        try:
            self.inputWidget.itemChanged.disconnect()
        except TypeError:
            pass

        # 清空子项
        root_item.takeChildren()

        # 重新填充数据
        for pos, (key, value) in enumerate(item_dict.items()):
            item = self.getQTreeWidgetItem(pos, key, value)
            root_item.addChild(item)

        # 添加空行用于新增
        self.addQTreeWidgetItem(root_item)

        # 重新连接信号
        if root_item == self.inputAttr:
            self.inputWidget.itemChanged.connect(self.updateAttrUrl)
        else:
            self.inputWidget.itemChanged.connect(self.updateStyleUrl)

        self.changeExpand()
