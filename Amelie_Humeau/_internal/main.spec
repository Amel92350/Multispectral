# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['C:\\Users\\AHUMEAU\\git\\Multispectral\\Amelie_Humeau\\main\\main.py'],
    pathex=['C:\\Users\\AHUMEAU\\git\\Multispectral\\Amelie_Humeau\\main'],
    binaries=[('C:\\Users\\AHUMEAU\\AppData\\Local\\Programs\\Python\\Python311\\DLLs', '.')], # Ajoutez ici toutes les DLLs nécessaires
    datas=[('C:\\Users\\AHUMEAU\\git\\Multispectral\\Amelie_Humeau\\main', '.')],
    hiddenimports=['Metashape','matplotlib','imutils'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
