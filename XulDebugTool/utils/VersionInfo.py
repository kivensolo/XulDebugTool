#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
版本信息管理模块

统一管理版本号、编译时间等信息
支持开发和打包环境
"""

import json
import os
import sys


class VersionInfo:
    VERSION = ""
    VERSION_FULL = ""
    BUILD_TIME = ""
    RELEASE_DATE = ""
    DESCRIPTION = ""

    @staticmethod
    def _find_version_file():
        """
        查找 version.json 文件
        支持多种路径，兼容开发和打包环境
        """
        possible_paths = []

        if getattr(sys, 'frozen', False):
            # 运行环境是打包后的环境
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller 打包后，资源文件在 _MEIPASS 目录
                possible_paths.append(os.path.join(sys._MEIPASS, 'config', 'version.json'))
            # exe 同目录下的 config 文件夹
            possible_paths.append(os.path.join(os.path.dirname(sys.executable), 'config', 'version.json'))
        else:
            # 开发环境
            # 获取项目根目录：从本模块向上三级
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            # 优先从 config 目录读取
            possible_paths.append(os.path.join(project_root, 'config', 'version.json'))
            # 也尝试当前目录下的 config
            possible_paths.append(os.path.join(os.getcwd(), 'config', 'version.json'))

        # 2. 查找第一个存在的文件
        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    @classmethod
    def load(cls):
        """加载版本信息"""
        version_file = cls._find_version_file()

        if version_file:
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cls.VERSION = data.get('version', '1.0.0')
                    cls.VERSION_FULL = f"v{cls.VERSION}"
                    cls.BUILD_TIME = data.get('buildTime', '')
                    cls.RELEASE_DATE = data.get('releaseDate', '')
                    cls.DESCRIPTION = data.get('description', '')
            except Exception as e:
                print(f"Error loading version file: {e}")
                cls._set_default_values()
        else:
            cls._set_default_values()

    @classmethod
    def _set_default_values(cls):
        """设置默认值（开发版本）"""
        cls.VERSION = "1.0.0-dev"
        cls.VERSION_FULL = f"v{cls.VERSION}"
        cls.BUILD_TIME = "开发版本"
        cls.RELEASE_DATE = ""
        cls.DESCRIPTION = ""

    @classmethod
    def get_version(cls):
        """获取版本号，如 1.3.1"""
        return cls.VERSION

    @classmethod
    def get_version_full(cls):
        """获取完整版本号，如 v1.3.1"""
        return cls.VERSION_FULL

    @classmethod
    def get_build_time(cls):
        """获取编译时间"""
        return cls.BUILD_TIME if cls.BUILD_TIME else "未知"

    @classmethod
    def get_display_build_time(cls):
        """获取用于显示的编译时间（带默认文本）"""
        if cls.BUILD_TIME:
            return cls.BUILD_TIME
        return "开发版本"


# 模块加载时自动加载版本信息
VersionInfo.load()
