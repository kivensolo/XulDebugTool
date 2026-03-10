#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @File   : QuickTemplatesLoader.py
 @Time   : 2026/03/10
 @Author : ZekeWong
 @Description: 快捷属性模板配置加载器
              支持从配置文件加载快捷属性模板，支持开发和打包环境
"""

import json
import os
import sys


class QuickTemplatesLoader(object):
    """
    属性面板中的通过右键展示的快捷属性模板配置加载器
    """

    # 兜底的默认模板（当配置文件不存在或加载失败时使用）
    DEFAULT_TEMPLATES = {
        "attr": {
            'padding(TLRB)': {"key": "padding", "value": "5,5,5,5", "description": "默认padding"},
            "宽度100": {"key": "width", "value": "100", "description": "设置宽度为100"},
            "高度100": {"key": "height", "value": "100", "description": "设置高度为100"},
            "居中对齐": {"key": "align", "value": "center", "description": "设置居中对齐"},
            "文本内容": {"key": "text", "value": "sample text", "description": "设置示例文本"},
        },
        "style": {
            "快速添加border": {"key": "border", "value": "1,ff00ff99,0,0", "description": "添加调试边框"},
            "红色背景": {"key": "background-color", "value": "ffff0000", "description": "设置红色背景"},
            "白色字体": {"key": "font-color", "value": "ffffffff", "description": "设置白色字体"},
            "字体大小20": {"key": "font-size", "value": "20", "description": "设置字体大小为20"},
            "字体加粗": {"key": "font-weight", "value": "bold", "description": "设置字体加粗"},
            "隐藏": {"key": "display", "value": "none", "description": "隐藏控件"},
        }
    }

    _config_cache = None
    _config_file_path = None

    @staticmethod
    def _find_config_file():
        """
        查找配置文件路径
        优先级：
        1. exe 同目录下的 config 文件夹（打包后用户自定义配置）
        2. _MEIPASS 内的 config 文件夹（打包后的默认配置）
        3. 项目根目录下的 config 文件夹（开发环境）
        4. 当前工作目录下的 config 文件夹

        :return: 配置文件路径，如果不存在则返回 None
        """
        if QuickTemplatesLoader._config_file_path:
            return QuickTemplatesLoader._config_file_path

        possible_paths = []

        if getattr(sys, 'frozen', False):
            # PyInstaller 打包后环境
            exe_dir = os.path.dirname(sys.executable)

            # 优先使用用户自定义的配置：exe 同目录下的 config 文件夹
            possible_paths.append(os.path.join(exe_dir, 'config', 'quick_templates.json'))

            if hasattr(sys, '_MEIPASS'):
                # 其次：打包在 exe 内的默认配置
                possible_paths.append(os.path.join(sys._MEIPASS, 'config', 'quick_templates.json'))
        else:
            # 开发环境
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))

            # 项目根目录下的 config 文件夹
            possible_paths.append(os.path.join(project_root, 'config', 'quick_templates.json'))

            # 当前工作目录下的 config 文件夹
            possible_paths.append(os.path.join(os.getcwd(), 'config', 'quick_templates.json'))

        # 返回第一个存在的文件路径
        for path in possible_paths:
            if os.path.exists(path):
                QuickTemplatesLoader._config_file_path = path
                return path

        return None

    @staticmethod
    def _load_config():
        """
        从配置文件加载模板配置
        :return: 配置字典，如果加载失败则返回默认配置
        """
        if QuickTemplatesLoader._config_cache is not None:
            return QuickTemplatesLoader._config_cache

        config_file = QuickTemplatesLoader._find_config_file()

        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 验证配置格式
                    if 'templates' in config and 'attr' in config['templates'] and 'style' in config['templates']:
                        QuickTemplatesLoader._config_cache = config['templates']
                        print(f"[QuickTemplatesLoader] 已加载配置文件: {config_file}")
                        return QuickTemplatesLoader._config_cache
                    else:
                        print(f"[QuickTemplatesLoader] 自定义配置文件格式错误，使用内置文件配置")
            except Exception as e:
                print(f"[QuickTemplatesLoader] 加载配置文件失败: {e}")

        # 使用默认配置
        QuickTemplatesLoader._config_cache = QuickTemplatesLoader.DEFAULT_TEMPLATES
        print("[QuickTemplatesLoader] 使用默认快捷模板配置")
        return QuickTemplatesLoader._config_cache

    @staticmethod
    def get_attr_templates():
        """
        获取 Attr 区域的快捷模板
        :return: 字典，格式为 {显示名: (key, value)}
        """
        templates = QuickTemplatesLoader._load_config().get('attr', {})
        return {name: (item['key'], item['value']) for name, item in templates.items()}

    @staticmethod
    def get_style_templates():
        """
        获取 Style 区域的快捷模板
        :return: 字典，格式为 {显示名: (key, value)}
        """
        templates = QuickTemplatesLoader._load_config().get('style', {})
        return {name: (item['key'], item['value']) for name, item in templates.items()}

    @staticmethod
    def reload():
        """
        重新加载配置文件（清除缓存）
        :return: 重新加载后的配置
        """
        QuickTemplatesLoader._config_cache = None
        QuickTemplatesLoader._config_file_path = None
        return QuickTemplatesLoader._load_config()

    @staticmethod
    def get_config_file_path():
        """
        获取当前使用的配置文件路径
        :return: 配置文件路径，如果使用默认配置则返回 None
        """
        if QuickTemplatesLoader._config_file_path is None:
            QuickTemplatesLoader._find_config_file()
        return QuickTemplatesLoader._config_file_path

    @staticmethod
    def is_using_default():
        """
        判断是否使用默认配置
        :return: True 表示使用默认配置，False 表示从文件加载
        """
        return QuickTemplatesLoader._config_file_path is None
