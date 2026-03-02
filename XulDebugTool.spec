# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件

使用方法:
pyinstaller XulDebugTool.spec
"""

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
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWebChannel',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        # QtWebEngine 相关依赖
        'PyQt5.QtWebEnginePlugins.QtWebEngine',
        'PyQt5.QtWebEnginePlugins.QtPrint',
        # 其他依赖
        'lxml',
        'lxml._elementpath',
        'lxml.etree',
        'xmltodict',
        'urllib3',
        'pyperclip',
        'json',
    ],
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
    name='XulDebugTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 禁用 UPX 压缩，可能导致问题
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
