# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\College Event Score System.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\assets', 'assets/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\backups', 'backups/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\data', 'data/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\gui', 'gui/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\logs', 'logs/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\reports', 'reports/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\themes', 'themes/'), ('C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\utils', 'utils/')],
    hiddenimports=['html.parser'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='College Event Score System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\AustinWelsh-Graham\\OneDrive - Austin ATTS\\Documents\\Work\\School\\IT\\4\\C\\cess\\assets\\icons\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='College Event Score System',
)
