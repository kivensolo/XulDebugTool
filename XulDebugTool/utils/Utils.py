#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import sqlite3

import xmltodict
from PyQt5.QtWebEngineWidgets import QWebEngineScript
from lxml import etree

from XulDebugTool.logcatapi.Logcat import STCLogger


class Utils(object):
    windowWidth = 1920
    windowHeight = 1080
    itemHeight = 30
    zoomFactor = 1.35

    @staticmethod
    def xml2json(xml, tag):
        # 将xml的某个tag转化成json
        doc = xmltodict.parse(xml)[tag]
        if doc != None:
            str = json.dumps(dict(doc))
            return json.loads(str)
        else:
            return ''

    @staticmethod
    def scriptCreator(path, name, page):
        script = QWebEngineScript()
        f = open(path, 'r')
        script.setSourceCode(f.read())
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setName(name)
        script.setWorldId(QWebEngineScript.MainWorld)
        page.scripts().insert(script)

    @staticmethod
    def findNodeById(id, xml):
        root = etree.fromstring(xml)
        # print(etree.tostring(root, pretty_print=True).decode('utf-8'))
        try:
            list = root.xpath("//*[@id=%s]" % id)
        except Exception as e:
            STCLogger().e(e)
        return list[0]

    @staticmethod
    def setWindowWidth(width):
        Utils.windowWidth = width

    @staticmethod
    def setWindowHeight(height):
        Utils.windowHeight = height
        Utils.itemHeight = int(Utils.windowHeight / 36.0)

    @staticmethod
    def getWindowWidth():
        return Utils.windowWidth

    @staticmethod
    def getWindowHeight():
        return Utils.windowHeight

    @staticmethod
    def getItemHeight():
        return Utils.itemHeight

    @staticmethod
    def getAdaptItemHeight():
        return Utils.itemHeight * Utils.zoomFactor

    @staticmethod
    def getAdaptSize(number):
        return number * Utils.zoomFactor

    @staticmethod
    def calculateZoomFactor():
        """
        根据屏幕分辨率计算合适的缩放因子
        以1920x1080为基准分辨率，缩放因子为1.3
        根据屏幕宽度动态调整缩放比例
        """
        baseWidth = 1920
        # width=1920
        baseZoomFactor = 1.35
        # 最小缩放因子，避免在低分辨率屏幕( width <= 1366)上字体过大
        minZoomFactor = 0.8
        # 最大缩放因子，避免在超高分辨率屏幕(width >= 3840 4K)上字体过大
        maxZoomFactor = 2.0
        # 根据屏幕宽度计算缩放因子
        zoomFactor = baseZoomFactor * (Utils.windowWidth / baseWidth)
        # 限制缩放因子在合理范围内
        zoomFactor = max(minZoomFactor, min(zoomFactor, maxZoomFactor))
        return zoomFactor

    @staticmethod
    def calculateDpiScale():
        """
        根据屏幕分辨率计算UI缩放因子
        以1920x1080为基准分辨率
        用于UI元素的位置、大小缩放
        """
        baseWidth = 1920
        # 计算缩放比例
        scale = Utils.windowWidth / baseWidth
        # 限制缩放范围在0.8到2.0之间
        scale = max(0.8, min(scale, 2.0))
        return scale

    @staticmethod
    def setAutoLoginState(loginState):
        try:
            conn = sqlite3.connect('XulDebugTool.db')
            cursor = conn.cursor()
            cursor.execute("delete from login")
            cursor.execute("insert into login (name) values ('" + str(loginState) + "')")
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getAutoLoginState():
        try:
            conn = sqlite3.connect('XulDebugTool.db')
            cursor = conn.cursor()
            cursor.execute('select * from login')
            result = cursor.fetchone()
        except Exception:
            return []
        finally:
            cursor.close()
            conn.close()
        return result
