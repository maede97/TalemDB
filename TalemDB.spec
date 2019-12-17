# -*- mode: python -*-

block_cipher = None

specpath = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(['main.py'],
             pathex=[specpath],
             binaries=[],
             datas=[('logo.png', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[os.path.join(specpath,"database.db")],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='TalemDB',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='TalemDB',
			   icon=os.path.join(specpath,'logo.png')
			  )