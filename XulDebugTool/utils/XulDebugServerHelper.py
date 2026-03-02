#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.parse import quote

import urllib3

from XulDebugTool.logcatapi.Logcat import STCLogger


# 全局 HTTP 连接池，带超时和重试配置
# 超时设置：连接超时3秒，读取超时3秒
# 重试设置：总共重试2次，连接失败重试1次
_http_pool = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=3.0, read=3.0),
    retries=urllib3.Retry(total=2, connect=1)
)

class XulDebugServerHelper(object):
    HOST = ''
    __LIST_PAGE = 'list-pages'
    __GET_LAYOUT = 'get-layout'
    __LIST_USER_OBJECTS = 'list-user-objects'
    __GET_USER_OBJECT = 'get-user-object'
    __SET_ATTR = 'set-attr'
    __SET_STYLE = 'set-style'
    __ADD_CLASS = 'add-class'
    __REMOVE_CLASS = 'remove-class'
    __CLEAR_ALL_CACHES = 'clear-all-caches'
    __REQUEST_FOCUS = 'request-focus'
    __GET_SELECTOR = 'get-selector'
    __FIRE_EVENT = 'fire-event'

    @staticmethod
    def listPages():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__LIST_PAGE
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getLayout(pageId, skipProp=True, withBindingData=True, withPosition=True, withSelector=True):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(XulDebugServerHelper.__GET_LAYOUT + '/' + pageId)
                r = _http_pool.request('GET', url, fields={'skip-prop': skipProp,
                                         'with-binding-data': withBindingData,
                                         'with-position': withPosition,
                                         'with-selector': withSelector})
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def isXulDebugServerAlive():
        r = XulDebugServerHelper.listPages()
        if r:
            return r.status == 200
        else:
            return False

    @staticmethod
    def listUserObject():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__LIST_USER_OBJECTS
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getUserObject(objectId):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(XulDebugServerHelper.__GET_USER_OBJECT + '/' + objectId)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def updateUrl(type, id, key, value):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(type + '/' + id + '/' + key + '/' + value)
                STCLogger().i("updateUrl = " + url)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def clearAllCaches():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__CLEAR_ALL_CACHES
                STCLogger().i("clearAllCaches = " + url)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def focusChooseItemUrl(id):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__REQUEST_FOCUS + '/' + id
                STCLogger().i("focusChooseItemUrl = " + url)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getAllSelector():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__GET_SELECTOR
                STCLogger().i("getAllSelector = " + url)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getPageSelector(pageId):
        return XulDebugServerHelper.getLayout(pageId, False, False, False, True)

    @staticmethod
    def updateClassUrl(type, id, className):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(type + '/' + id + '/' + className)
                STCLogger().i("updateClassUrl = " + url)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def fireItemEvent(action, id):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(XulDebugServerHelper.__FIRE_EVENT + '/' + id + '/' + action)
                STCLogger().i("fireItemEvent = " + url)
                r = _http_pool.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return r