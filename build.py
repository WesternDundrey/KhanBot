import subprocess
import sys
import os
from pathlib import Path
import shutil

def setup_icons():
    """Set up icon directories and files"""
    # Create icons directory if it doesn't exist
    icons_dir = Path('icons')
    icons_dir.mkdir(exist_ok=True)

    # Ensure the logo is in the icons directory
    if not (icons_dir / 'khanbot_logo.png').exists():
        print("Please place khanbot_logo.png in the icons directory")
        sys.exit(1)

    # Create system icon directories if they don't exist
    icon_sizes = ['16x16', '32x32', '48x48', '128x128', '256x256']
    for size in icon_sizes:
        icon_path = Path(f'~/.local/share/icons/hicolor/{size}/apps').expanduser()
        icon_path.mkdir(parents=True, exist_ok=True)

        # Convert and copy icon to system directory
        subprocess.run([
            'convert',
            str(icons_dir / 'khanbot_logo.png'),
            '-resize', size,
            str(icon_path / 'khanbot.png')
        ])

def build_executable():
    # Install PyInstaller if not already installed
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Create the spec file
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend-api', 'backend-api'),
        ('dashboard', 'dashboard'),
        ('icons/khanbot_logo.png', 'icons'),
    ],
    hiddenimports=[
        'fastapi',
        'uvicorn',
        'streamlit',
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
    name='khanbot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='icons/khanbot_logo.png',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    # Write the spec file
    with open('launcher.spec', 'w') as f:
        f.write(spec_content)

    # Build the executable
    subprocess.run([
        "pyinstaller",
        "--clean",
        "launcher.spec"
    ])

    print("\nBuild complete! The executable is in the 'dist' directory.")
    print("You can run it with: ./dist/khanbot")

if __name__ == "__main__":
    setup_icons()
    build_executable()
