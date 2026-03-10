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
    name='XulDebugTool',
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
