# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件

使用方法:
pyinstaller XulDebugTool.spec
"""

import json
import os
import sys
from datetime import datetime


def update_version_info():
    """
    自动更新 version.json 中的 releaseDate 和 buildTime
    返回版本号用于生成 exe 文件名
    """
    version_file = os.path.join('config', 'version.json')

    if not os.path.exists(version_file):
        print(f"[Build] 警告: version.json 文件不存在: {version_file}")
        return None

    try:
        # 读取现有配置
        with open(version_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 获取当前时间
        now = datetime.now()
        release_date = now.strftime('%Y-%m-%d')
        build_time = now.strftime('%Y-%m-%d %H:%M:%S')

        # 更新字段
        old_release_date = config.get('releaseDate', '')
        old_build_time = config.get('buildTime', '')

        config['releaseDate'] = release_date
        config['buildTime'] = build_time

        # 写回文件
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        version = config.get('version', '')
        print(f"[Build] version.json 已更新:")
        print(f"[Build]   version: {version}")
        print(f"[Build]   releaseDate: {old_release_date} -> {release_date}")
        print(f"[Build]   buildTime: {old_build_time} -> {build_time}")

        return version

    except Exception as e:
        print(f"[Build] 错误: 更新 version.json 失败: {e}")
        return None


# 在打包前自动更新版本信息，并获取版本号
APP_VERSION = update_version_info()

block_cipher = None

a = Analysis(
    ['XulDebugTool/App.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 配置文件
        ('config', 'config'),
        # 资源文件（图片等）
        ('resources', 'resources'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=f'XulDebugTool-{APP_VERSION}' if APP_VERSION else 'XulDebugTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 启用 UPX 压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口，便于调试
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可指定图标文件路径，如：'resources/images/icon.ico'
)
